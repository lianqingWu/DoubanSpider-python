# DoubanSpider-python
这是一个用于爬取豆瓣书籍信息的 Python 爬虫项目，同时也可作为书籍推荐系统的基础数据采集部分。通过该项目，你可以从豆瓣网站上抓取大量书籍的详细信息，包括书名、作者、出版社、评分等，并将这些信息保存到本地文件中，为后续的数据分析和推荐算法提供数据支持。

## 功能特点
1. **多页面爬取**：支持从豆瓣书籍 Top 250 列表和特定标签页面（如科幻）开始爬取，自动发现并跟进新的书籍链接。
2. **数据持久化**：将已爬取的 URL 和书籍信息保存到本地文件，避免重复爬取，确保数据的连续性和完整性。
3. **封面下载**：自动下载书籍的封面图片，并保存到本地指定目录。
4. **随机延迟**：在爬取过程中加入随机延迟，模拟人类行为，降低被网站反爬机制封禁的风险。

## 安装步骤
### 环境要求
- Python 3.x
- 相关依赖库：`requests`, `beautifulsoup4`

### 安装依赖
在项目根目录下，打开终端并执行以下命令来安装所需的依赖库：
```bash
pip install requests beautifulsoup
```

## 使用方法
### 1. 配置 Cookie
在进行爬取之前，你需要在 `config.py` 文件中完善自己的 Cookie 信息，以避免被豆瓣的反爬机制拦截。获取 Cookie 的步骤如下：
1. 打开 Chrome 或 Firefox 浏览器，登录豆瓣网站。
2. 打开开发者工具（通常可以通过右键点击页面，选择“检查”或使用快捷键 `Ctrl + Shift + I`（Windows/Linux）或 `Cmd + Opt + I`（Mac））。
3. 切换到“网络”（Network）面板。
4. 刷新豆瓣页面，在请求列表中找到任意一个请求，点击它，然后在右侧的“请求头”（Request Headers）中找到 `Cookie` 字段。
5. 将 `Cookie` 字段的值复制到 `config.py` 文件中的 `Cookie` 变量中，示例如下：
```python
Cookie = 'your_cookie_here'
url = ''
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
    'Cookie': f'{Cookie}',
    'Referer': f'{url}',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site':'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.3 Safari/605.1.15'
}
```

### 2. 获取书籍 URL
运行 `get_urls.py` 脚本，该脚本会从指定的种子 URL 开始爬取，提取书籍的 URL 并保存到 `book_urls.txt` 文件中。
```bash
python get_urls.py
```

### 3. 爬取书籍详细信息
运行 `main.py` 脚本，该脚本会读取 `book_urls.txt` 文件中的书籍 URL，依次爬取每本书的详细信息，并将信息保存到 `books_data.json` 文件中，同时下载书籍封面图片到 `covers` 目录。
```bash
python main.py
```

## 代码结构
```
DoubanSpider-python/
├── get_urls.py       # 用于获取书籍 URL 的脚本
├── main.py           # 用于爬取书籍详细信息的主脚本
├── crawled_urls.txt  # 保存已爬取的页面 URL
├── book_urls.txt     # 保存所有发现的书籍 URL
├── books_data.json   # 保存爬取到的书籍详细信息
├── covers/           # 保存下载的书籍封面图片
├── config.py         # 配置文件，包含请求头和 Cookie 信息
└── README.md         # 项目说明文件
```

## 注意事项
- **反爬机制**：豆瓣网站有反爬机制，为避免被封禁 IP，建议在爬取过程中适当增加随机延迟时间，同时确保 `config.py` 中的 Cookie 信息有效。
- **数据更新**：如果需要更新已爬取的数据，可以删除 `crawled_urls.txt` 和 `books_data.json` 文件，然后重新运行脚本。
- **版权问题**：本项目仅用于学习和研究目的，请勿将爬取到的数据用于商业用途。

## 贡献
如果你对本项目有任何改进建议或发现了 bug，请随时提交 issue 或 pull request。

## 许可证
本项目采用 [MIT 许可证](LICENSE)。
