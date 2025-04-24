from get_urls import *
from fetch_data import *

import requests
from bs4 import BeautifulSoup
import time
import random
import json
from queue import Queue
import re
import os
from urllib.parse import urlparse

covers_dir = 'covers'  # 封面图片存储目录
if not os.path.exists(covers_dir):
    os.makedirs(covers_dir)  
book_url_pattern = r'https://book\.douban\.com/subject/\d+/?'

# 初始化
to_crawl = Queue()       # 待爬书籍URL队列
crawled_books = set()    # 已爬书籍URL集合
book_urls = set()        # 所有书籍URL集合
books_data = []          # 书籍详情列表

# 加载已有数据
try:
    with open('crawled_books.txt', 'r', encoding='utf-8') as f:
        crawled_books = set(line.strip() for line in f if line.strip())
except FileNotFoundError:
    pass

try:
    with open('book_urls.txt', 'r', encoding='utf-8') as f:
        book_urls = set(line.strip() for line in f if line.strip())
except FileNotFoundError:
    print("未找到 book_urls.txt，请确保文件存在！")
    exit(1)

try:
    with open('books_data.json', 'r', encoding='utf-8') as f:
        books_data = json.load(f)
except FileNotFoundError:
    pass

# 将未爬取的URL加入队列
for url in book_urls:
    if url not in crawled_books:
        to_crawl.put(url)

def download_cover(url, book_id):
    """下载封面图片到本地"""
    headers['Referer'] = url
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        # 从URL提取文件名，或使用book_id
        file_ext = os.path.splitext(urlparse(url).path)[1] or '.jpg'
        file_name = f"{book_id}{file_ext}"
        file_path = os.path.join(covers_dir, file_name)
        
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"封面下载完成: {file_path}")
        return file_path
    except Exception as e:
        print(f"下载封面 {url} 失败: {e}")
        return None

def extract_book_info(soup, url):
    """提取书籍详细信息，包括封面URL"""
    book_info = {'url': url}
    book_id = url.split('/')[-2]  # 从URL提取书籍ID，如27015840

    # 书名
    title_tag = soup.find('span', property='v:itemreviewed')
    book_info['title'] = title_tag.text.strip() if title_tag else 'N/A'

    # 作者
    author_tag = soup.find('span', class_='pl', string=' 作者')
    book_info['author'] = author_tag.find_next('a').text.strip() if author_tag else 'N/A'

    # 出版社
    publisher_tag = soup.find('span', class_='pl', string='出版社:')
    book_info['publisher'] = publisher_tag.find_next('a').text.strip() if publisher_tag else 'N/A'

    # 出版年
    pub_year_tag = soup.find('span', class_='pl', string='出版年:')
    book_info['pub_year'] = pub_year_tag.next_sibling.strip() if pub_year_tag else 'N/A'

    # 页数
    pages_tag = soup.find('span', class_='pl', string='页数:')
    book_info['pages'] = pages_tag.next_sibling.strip() if pages_tag else 'N/A'

    # 定价
    price_tag = soup.find('span', class_='pl', string='定价:')
    book_info['price'] = price_tag.next_sibling.strip() if price_tag else 'N/A'

    # ISBN
    isbn_tag = soup.find('span', class_='pl', string='ISBN:')
    book_info['isbn'] = isbn_tag.next_sibling.strip() if isbn_tag else 'N/A'

    # 评分
    rating_tag = soup.find('strong', class_='ll rating_num')
    book_info['rating'] = rating_tag.text.strip() if rating_tag else 'N/A'

    # 评价人数
    votes_tag = soup.find('span', property='v:votes')
    book_info['votes'] = votes_tag.text.strip() if votes_tag else 'N/A'

    # 简介
    intro_tag = soup.find('div', class_='intro')
    book_info['intro'] = '\n'.join(p.text.strip() for p in intro_tag.find_all('p')) if intro_tag else 'N/A'

    # 封面URL
    cover_tag = soup.find('img', alt=book_info['title'])
    cover_url = cover_tag['src'] if cover_tag else None
    book_info['cover_url'] = cover_url

    # 下载封面并记录本地路径
    if cover_url:
        local_path = download_cover(cover_url, book_id)
        book_info['cover_local_path'] = local_path if local_path else 'N/A'
    else:
        book_info['cover_local_path'] = 'N/A'

    return book_info

def crawl_book_page(url):
    """爬取书籍页面，提取详情和新URL"""
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # 提取书籍信息
        book_info = extract_book_info(soup, url)
        books_data.append(book_info)
        print(f"爬取书籍: {book_info['title']} ({url})")

        # 提取新书籍URL
        new_book_urls = set(re.findall(book_url_pattern, response.text))
        for new_url in new_book_urls:
            if new_url not in book_urls:
                book_urls.add(new_url)
                to_crawl.put(new_url)
                print(f"发现新书籍URL: {new_url}")

        return True
    except Exception as e:
        print(f"爬取 {url} 失败: {e}")
        return False

def save_data():
    """保存爬取结果"""
    with open('crawled_books.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(crawled_books))
    with open('book_urls.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(book_urls))
    with open('books_data.json', 'w', encoding='utf-8') as f:
        json.dump(books_data, f, ensure_ascii=False, indent=2)

def main():
    """主循环"""
    while not to_crawl.empty():
        url = to_crawl.get()
        if url in crawled_books:
            continue

        print(f"正在爬取: {url}")
        if crawl_book_page(url):
            crawled_books.add(url)

        # 保存进度
        save_data()

        # 随机延迟
        time.sleep(random.uniform(4, 6))

    print("爬取完成！")
    print(f"总共爬取书籍: {len(crawled_books)}")
    print(f"总共发现书籍URL: {len(book_urls)}")

if __name__ == "__main__":
    main()