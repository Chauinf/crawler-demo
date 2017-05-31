import requests
import pdfkit
import re
import os
from bs4 import BeautifulSoup

#A simple demo for making web pages into pdf


import sys
reload(sys)
sys.setdefaultencoding('utf8')

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>
{content}
</body>
</html>
"""

def parse_url_to_html(url, file_name):
	response = requests.get(url)
	soup = BeautifulSoup(response.content,"html.parser")
	body = soup.find_all("div","article-content")[0]
	html = str(body)
	pattern = "(<img .*?src=\")(.*?)(\")"

        def func(m):
        	if not m.group(2).startswith("http"):
                    rtn = "".join([m.group(1), 'http://cs.xidian.edu.cn', m.group(2), m.group(3)])
                    return rtn
                else:
                    return "".join([m.group(1), m.group(2), m.group(3)])

        html = re.compile(pattern).sub(func, html)
        html = html_template.format(content=html)
        html = html.encode("utf-8")
	 
	with open(file_name, 'wb') as f:
		f.write(html)
		return file_name

def get_url_list():
	response = requests.get("http://cs.xidian.edu.cn/html/news/")
	soup = BeautifulSoup(response.content,"html.parser")
	list_tag = soup.find_all("div","list-content")[0]
	urls = []
	for li in list_tag.find_all("li"):
		url = li.a.get("href")
		urls.append(url)
	return urls

def save_pdf(htmls, file_name):
	options = {
        'page-size': 'Letter',
        'encoding': "UTF-8",
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ]
    }
	pdfkit.from_file(htmls, file_name, options=options)


if __name__ == '__main__':
	urls = get_url_list()
	htmls = [parse_url_to_html(url, str(index) + ".html") for index, url in enumerate(urls)]
	print(htmls)
	save_pdf(htmls, "CS_XDU.pdf")
	for html in htmls:
		os.remove(html)	
