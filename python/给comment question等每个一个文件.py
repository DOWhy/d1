# -*- coding: utf-8 

import markdown
import os
import sys
import re
import time
from shutil import copyfile # 复制文件用的
import shutil
import uuid


# 删除 comments questions summarizes 文件夹
def recreateDirOfCommentsQuestionsSummarizes(mpath):
	if os.path.exists(mpath + 'comments'):
		shutil.rmtree(mpath + 'comments')
		os.makedirs(mpath + 'comments')
	if os.path.exists(mpath + 'questions'):
		shutil.rmtree(mpath + 'questions')
		os.makedirs(mpath + 'questions')
	if os.path.exists(mpath + 'summarizes'):
		shutil.rmtree(mpath + 'summarizes')
		os.makedirs(mpath + 'summarizes')



# 获取所有文件中的图片链接，并写入一个文件中
def getAllCommentsQuestionsSummarizes(path):

	global comments
	global questions
	global summarizes
	
	filelist = os.listdir(path)

	for file in filelist:

		if os.path.isdir(path + file):
			if file == '.git' or file == '.obsidian' or file == 'assets' or file == 'python' or file == '030-commen question summarize':
				continue
			else:
				getAllCommentsQuestionsSummarizes(path + file + '\\')
		
		if file.endswith('.md'):
			file1 = open(path + file, encoding='utf-8')
			content = file1.read()
			file1.close()
			comments = comments + re.findall(r'(#my-comment.*?#my-comment-end)', content)
			questions = questions + re.findall(r'(#my-question.*?#my-question-end)', content)
			summarizes = summarizes + re.findall(r'(#my-summarize.*?#my-summarize-end)', content)



def writeToFile(mpath):

	global comments
	global questions
	global summarizes

	for c in comments:
		filename = str(uuid.uuid4()) + '.md'
		file = open(mpath + 'comments\\' + filename, 'w', encoding='utf-8')
		file.write(c)
		file.close()
	for q in questions:
		filename = str(uuid.uuid4()) + '.md'
		file = open(mpath + 'questions\\' + filename, 'w', encoding='utf-8')
		file.write(c)
		file.close()
	for s in summarizes:
		filename = str(uuid.uuid4()) + '.md'
		file = open(mpath + 'summarizes\\' + filename, 'w', encoding='utf-8')
		file.write(c)
		file.close()
	


if __name__ == "__main__":

	comments = []
	questions = []
	summarizes = []

	path = 'C:\\Users\\john\\my_collection\\Articles_and_Books2\\'
	mpath = 'C:\\Users\\john\\my_collection\\Articles_and_Books2\\030-commen question summarize\\'

	
	recreateDirOfCommentsQuestionsSummarizes(mpath)
	getAllCommentsQuestionsSummarizes(path)

	writeToFile(mpath)