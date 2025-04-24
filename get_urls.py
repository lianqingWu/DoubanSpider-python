import requests
from bs4 import BeautifulSoup
import time
import random
import json
from queue import Queue
import re
from fetch_data import *
# 配置
seed_urls = [
    "https://book.douban.com/top250?start=0",  # Top 250第一页
    "https://book.douban.com/tag/科幻?start=0"  # 科幻标签第一页
]

# 初始化
to_crawl = Queue()  # 待爬URL队列
crawled = set()     # 已爬URL集合
book_urls = set()   # 书籍URL集合

# 加载已有数据（避免重复爬取）
try:
    with open('crawled_urls.txt', 'r', encoding='utf-8') as f:
        crawled = set(line.strip() for line in f if line.strip())
except FileNotFoundError:
    pass

try:
    with open('book_urls.txt', 'r', encoding='utf-8') as f:
        book_urls = set(line.strip() for line in f if line.strip())
except FileNotFoundError:
    pass

# 添加种子URL到队列
for url in seed_urls:
    if url not in crawled:
        to_crawl.put(url)

# 提取书籍URL的正则表达式
book_url_pattern = r'https://book\.douban\.com/subject/\d+/?'

def crawl_page(url):
    """爬取单个页面，提取书籍URL和新链接"""
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # 提取书籍URL
        new_book_urls = set(re.findall(book_url_pattern, response.text))
        for book_url in new_book_urls:
            if book_url not in book_urls:
                book_urls.add(book_url)
                print(f"发现新书籍URL: {book_url}")

        # 提取其他链接（如分页、标签页）
        for link in soup.find_all('a', href=True):
            next_url = link['href']
            if next_url.startswith('/'):
                next_url = 'https://book.douban.com' + next_url
            if next_url.startswith('https://book.douban.com') and next_url not in crawled:
                to_crawl.put(next_url)

        return True
    except Exception as e:
        print(f"爬取 {url} 失败: {e}")
        return False

def save_data():
    """保存已爬URL和书籍URL"""
    with open('crawled_urls.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(crawled))
    with open('book_urls.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(book_urls))

def main():
    """主循环"""
    while not to_crawl.empty():
        url = to_crawl.get()
        if url in crawled:
            continue

        print(f"正在爬取: {url}")
        if crawl_page(url):
            crawled.add(url)
        
        # 保存进度
        save_data()
        
        # 随机延迟，避免反爬
        time.sleep(random.uniform(1, 3))

    print("爬取完成！")
    print(f"总共爬取页面: {len(crawled)}")
    print(f"总共发现书籍URL: {len(book_urls)}")

if __name__ == "__main__":
    main()