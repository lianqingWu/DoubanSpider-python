
import requests
from bs4 import BeautifulSoup
from config import headers
url = 'https://book.douban.com/subject/27015840/'
def fetch_data(url, headers=headers):
    try:
        response = requests.get(url, headers=headers)
        # 手动设置编码
        response.encoding = response.apparent_encoding
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup
        else:
            print(f'请求失败，状态码: {response.status_code}')
    except requests.RequestException as e:
        print(f'请求过程中出现错误: {e}')

def extract_book_data(soup):

    # 存储提取的信息
    book_info = {}

    # 1. 书名
    book_info['title'] = soup.find('span', property='v:itemreviewed').text.strip()

    # 2. 作者
    author_tag = soup.find('span', class_='pl', text=' 作者')
    if author_tag:
        book_info['author'] = author_tag.find_next('a').text.strip()

    # 3. 出版社
    publisher_tag = soup.find('span', class_='pl', text='出版社:')
    if publisher_tag:
        book_info['publisher'] = publisher_tag.find_next('a').text.strip()

    # 4. 出品方
    producer_tag = soup.find('span', class_='pl', text='出品方:')
    if producer_tag:
        book_info['producer'] = producer_tag.find_next('a').text.strip()

    # 5. 出版年
    pub_year_tag = soup.find('span', class_='pl', text='出版年:')
    if pub_year_tag:
        book_info['pub_year'] = pub_year_tag.next_sibling.strip()

    # 6. 页数
    pages_tag = soup.find('span', class_='pl', text='页数:')
    if pages_tag:
        book_info['pages'] = pages_tag.next_sibling.strip()

    # 7. 定价
    price_tag = soup.find('span', class_='pl', text='定价:')
    if price_tag:
        book_info['price'] = price_tag.next_sibling.strip()

    # 8. 装帧
    binding_tag = soup.find('span', class_='pl', text='装帧:')
    if binding_tag:
        book_info['binding'] = binding_tag.next_sibling.strip()

    # 9. ISBN
    isbn_tag = soup.find('span', class_='pl', text='ISBN:')
    if isbn_tag:
        book_info['isbn'] = isbn_tag.next_sibling.strip()

    # 10. 评分
    rating_tag = soup.find('strong', class_='ll rating_num')
    if rating_tag:
        book_info['rating'] = rating_tag.text.strip()

    # 11. 评价人数
    votes_tag = soup.find('span', property='v:votes')
    if votes_tag:
        book_info['votes'] = votes_tag.text.strip()

    # 12. 星级分布
    stars = {}
    for star in soup.find_all('span', class_='starstop'):
        rating_per = star.find_next('span', class_='rating_per').text.strip()
        stars[star.text.strip()] = rating_per
    book_info['star_distribution'] = stars

    # 13. 封面图片URL
    img_tag = soup.find('img', alt=book_info['title'])
    if img_tag:
        book_info['cover_url'] = img_tag['src']

    # 14. 简介（短简介和完整简介）
    short_intro = soup.find('span', class_='short').find('div', class_='intro')
    if short_intro:
        book_info['short_intro'] = '\n'.join(p.text.strip() for p in short_intro.find_all('p') if p.text.strip())

    full_intro = soup.find('span', class_='all hidden').find('div', class_='intro')
    if full_intro:
        book_info['full_intro'] = '\n'.join(p.text.strip() for p in full_intro.find_all('p') if p.text.strip())

    # 输出结果
    for key, value in book_info.items():
        print(f"{key}: {value}")
    # print(soup.find('img', alt=book_info['title']))
    return book_info
# 主程序
if __name__ == "__main__":
    # 假设html_content是你的HTML内容
    # 在实际使用时需要读取文件或从网络获取

    # url = 'https://book.douban.com/subject/27015840/'
    # soup = fetch_data(url)
    # with open('test.txt','w') as f:
    #     f.write(str(soup.find_all))
    # if soup:
    #     book_data = extract_book_data(soup)
    #     print_book_data(book_data)
    with open('test.txt', 'r', encoding='utf-8') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    # 提取数据
    book_data = extract_book_data(soup)
    
    
