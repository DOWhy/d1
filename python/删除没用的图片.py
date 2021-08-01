# -*- coding:utf-8 -*-

import os
import re
import time
import shutil


# 获取上一次导运行这个代码的时间
def getLastTime(path):
    file = open(path + '\\python\\上一次删除图片的时间', encoding='utf-8')
    lastTime = file.read()
    file.close()

    lastTime = float(lastTime)

    return lastTime


# 将这次运行这个代码的时间记录在文件中
def saveTheTimeOfToAnki(path, time):
    file = open(path + '\\python\\上一次删除图片的时间', 'w', encoding='utf-8')
    file.write(str(time))
    file.close()


# 获取所有文件中的图片链接，并写入一个文件中
def addNewAssetInFileToAFile(mpath, path):
	
	filelist = os.listdir(path)

	for file in filelist:

		if os.path.isdir(path + file):
			if file == '.git' or file == '.obsidian' or file == 'assets' or file == 'python':
				continue
			else:
				addNewAssetInFileToAFile(mpath, path + file + '\\')
		
		if file.endswith('.md'):
			mtime = os.path.getmtime(path + file)
			lastTime = getLastTime(mpath)
			if mtime > lastTime:
				file1 = open(path + file, encoding='utf-8')
				content = file1.read()
				file1.close()
				assets = re.findall(r'(!\[\[.*?\]\])', content)

				i = 0
				for i in range(len(assets)):
					assets[i] = assets[i][3:-2] + '\n'
					if assets[i] not in allAssetsLinksInFiles:
						allAssetsLinksInFiles.append(assets[i])

	

# 获取所有没有被用到图片的名字，并写入一个文件中
def getAllNoUseingAssets(mpath):

	noUseingAssets = []

	allAssets = os.listdir(mpath + 'assets\\')

	for asset in allAssets:
		if asset + '\n' not in allAssetsLinksInFiles:
			noUseingAssets.append(asset + '\n')

	file = open(mpath + 'python\\没有在文件中被引用的图片', 'w', encoding='utf-8')
	file.writelines(noUseingAssets)
	file.close()


# 将那些没有在任何文件中引用的图片移动到 assets.trash 文件夹中
def moveAllNoUseingAssets(mpath, trashPath):

	file = open(mpath + 'python\\没有在文件中被引用的图片', encoding='utf-8')
	noUseingAssets = file.readlines()
	file.close()

	i = 0
	for i in range(len(noUseingAssets)):
		noUseingAssets[i] = noUseingAssets[i][:-1]

	if not os.path.exists(trashPath):
		os.makedirs(trashPath)

	for asset in noUseingAssets:
		shutil.move(mpath + 'assets\\' + asset, trashPath + asset)



if __name__ == "__main__":

	mpath = "C:\\Users\\john\my_collection\\Articles_and_Books2\\"
	path = mpath
	trashPath = "C:\\Users\\john\my_collection\\assets.trash\\"

	file2 = open(mpath + 'python\\所有文件中的用到的图片', encoding='utf-8')
	allAssetsLinksInFiles = file2.readlines()
	file2.close()
	# i = 0
	# for i in range(len(allAssetsLinksInFiles)):
	# 	allAssetsLinksInFiles[i] = allAssetsLinksInFiles[i][:-1]

	addNewAssetInFileToAFile(mpath, path)

	file2 = open(mpath + 'python\\所有文件中的用到的图片', 'w', encoding='utf-8')
	file2.writelines(allAssetsLinksInFiles)
	file2.close()


	getAllNoUseingAssets(mpath)
	
	moveAllNoUseingAssets(mpath, trashPath)
			

	# saveTheTimeOfToAnki(mpath, time.time()) #现在不能写入时间，要不然那些在文件中删除的链接依然保存在“所有文件中用到的图片”文件中，就删除不了对应的图片了