# -*- coding:utf-8 -*-


import requests
import time
from bs4 import BeautifulSoup
import re
import os
import random
import urllib3
import datetime
import uuid
from io import BytesIO  #用来获取图片的格式的
from PIL import Image
import datetime


# 下载一张图片
def downloadOneImg(url, path, proxies, headers):
	try:
		# -----------------------------------------------------------------------
		# 参考：https://www.jianshu.com/p/acb6a1b95fcb  基本上意思就是发出的网络请求比较频繁，requests内置的urllibs3不能及时的为我们断开连接
		#设置重连次数
		requests.adapters.DEFAULT_RETRIES = 15
		# 设置连接活跃状态为False
		s = requests.session()
		s.keep_alive = False
		#------------------------------------------------------------------------
		time.sleep(1.5)
		response = requests.get(url=url, headers=headers, proxies=proxies)
		# 关闭请求  释放内存
		response.close() # 这段代码的作用就是解决远程服务器主动断开连接的 参考：https://www.jianshu.com/p/acb6a1b95fcb  基本上意思就是发出的网络请求比较频繁，requests内置的urllibs3不能及时的为我们断开连接
		# del(response)  
	except Exception:
		time.sleep(5)
		response = requests.get(url=url, headers=headers, proxies=proxies) # 发送请求时使用代理
	img = response.content # content 返回二进制数据
	if not os.path.exists(path + 'd1\\'):
		print('没有 assets 目录，将创建它')
		os.mkdir(path + 'd1\\')
	imageName = getImageName(response)
	fp = open(path + 'd1\\' + imageName, 'wb')
	fp.write(img)
	fp.close()
	
	return imageName


# 从图片的网络链接中获取图片的名字，并且将 ? 这样的不能做文件名的符号换成 _ ,然后对于没有扩展名的，要添加扩展名
def getImageName(response):

	# uid = uuid.uuid4()
	# imageName = str(uid)
	imageName = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
	try:
		imageFormat = Image.open(BytesIO(response.content))
		imageFormat = imageFormat.format.lower()  #将图片的扩展名变成类似 .png 这样的格式
		if imageFormat == 'webp':
			imageFormat = 'png'
			imageName = imageName + '.' + imageFormat
		else:
			# imageName = str(uid) + '.' + imageFormat
			imageName = imageName + '.' + imageFormat
	except Exception:
		imageName = imageName + '.png'

	return imageName


# 获取上一次导运行这个代码的时间
def getLastTime(path):
    file = open(path + 'd1\\python\\上一次导运行这个代码的时间', encoding='utf-8')
    lastTime = file.read()
    file.close()

    lastTime = float(lastTime)

    return lastTime


# 将这次运行这个代码的时间记录在文件中
def saveTheTimeOfToAnki(path, time):
    file = open(path + 'd1\\python\\上一次导运行这个代码的时间', 'w', encoding='utf-8')
    file.write(str(time))
    file.close()


if __name__ == "__main__":

	# 使用代理
	proxy='127.0.0.1:7890'  #本地代理
	#proxy='username:password@123.58.10.36:8080'
	proxies={  # 需要安装：pip install -U requests[socks]==2.12.0
		'http':'socks5://'+proxy, # 出现SOCKSHTTPSConnectionPool，所以用 socks5h, 参考：https://blog.csdn.net/csdn_inside/article/details/89817871 这个方法不管用，最终我安装了 pip install -U requests[socks]==2.12.0（需要去掉 socks5h 中的 h） 参考：https://github.com/psf/requests/issues/4310
		'https':'socks5://'+proxy
	}
	# UA 伪装
	headers = {
		# 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
		# 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
		'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.99 Mobile Safari/537.36',
		# 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
		# 'Accept-Encoding': 'gzip, deflate',
		# 'Accept-Language': 'zh-CN,zh;q=0.9',
		# 'Cache-Control': 'max-age=0',
		# # 'Cookie': 'PHPSESSID=aeg2qnc64hh05kbklgvjlovhj3; nav_switch=booklist',
		# 'Host': 'ccrip.com.',
		# 'Proxy-Connection': 'keep-alive',
		# # 'Referer': 'http://ccrip.com./book/37',
		# 'Upgrade-Insecure-Requests': '1'
	}

	# path = 'C:\\Users\\john\\Documents\\Articles_and_Books2\\pages\\'
	# path = "C:\\Users\\john\\Documents\\Articles_and_Books2\\pages\\"
	# path = "C:\\Users\\john\my_collection\\Articles_and_Books2\\020-pages\\"
	path = 'C:\\Users\\john\\Downloads\\葫芦笔记-文件处理-图片仓库\\'

	filelist = os.listdir(path)

	# file = "刘润：如何把一天用到极致？.md"

	for file in filelist:

		if os.path.isdir(path + file):
			continue

		markdown_link_list = []
		file1 = open(path + file, encoding='utf-8')
		content = file1.read()
		file1.close()
		markdown_link_list = markdown_link_list + re.findall(r'(!\[.*?\]\(.*?\))', content)

		if markdown_link_list:
			for markdown_link in markdown_link_list:
				file1 = open(path + file, encoding='utf-8')
				content = file1.read()
				file1.close()

				if re.search(r'(http.*?)\)', markdown_link):
					url = re.search(r'(http.*?)\)', markdown_link).group(1)
					print(url)
					imageName = downloadOneImg(url, path, proxies, headers)
					content = content.replace(markdown_link, '![](https://raw.githubusercontent.com/DOWhy/d1/master/' + imageName + ')')

					file2 = open(path + file, 'w', encoding='utf-8')
					file2.write(content)
					file2.close()
			

	saveTheTimeOfToAnki(path, time.time())