# -*- coding:utf-8 -*-

import os
import datetime




path = 'C:\\Users\\john\\Downloads\\葫芦笔记-文件处理-图片仓库\\'

filelist = os.listdir(path)

images = []

image = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

for file in filelist:

	if os.path.isdir(path + file):
		continue

	image = str(int(image)+10)
	k = file.rfind('.')
	imageName = image + file[k:]

	os.rename(path+file, path+imageName)
	images.append('![](https://raw.githubusercontent.com/DOWhy/d1/master/' + imageName + ')\n')

file = open('test.md', 'w', encoding='utf-8')
file.writelines(images)
file.close()
	