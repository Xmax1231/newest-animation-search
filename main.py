import time
import requests
from urllib.parse import quote
from bs4 import BeautifulSoup
import json
import re
import getpass

favorites = []
newest_ep_index = []
title = []
total_count = []
week = []
season_id = []
CV = []

def start():
	n = 1
	# url = 'https://bangumi.bilibili.com/web_api/timeline_global' # 時間標記
	url = 'https://bangumi.bilibili.com/web_api/season/index_global'

	year = time.strftime("%Y")
	if int(time.strftime("%m")) >= 10:
		quarter = 4
	elif int(time.strftime("%m")) >= 7:
		quarter = 3
	elif int(time.strftime("%m")) >= 4:
		quarter = 2
	elif int(time.strftime("%m")) >= 1:
		quarter = 1

	for page in range(100):
		Param = {	'page_size':'20',
					'start_year':year, 
					'quarter':quarter,
					'page':page
				}
		r = requests.get(url, params=Param)

		obj = json.loads(r.text)
		result = obj['result']
		limit_page = int(result['pages'])

		for L in result['list']:
			print(str(n)+': '+L['title'])
			favorites.append(L['favorites'])
			newest_ep_index.append(L['newest_ep_index'])
			title.append(L['title'])
			total_count.append(L['total_count'])
			week.append(L['week'])
			season_id.append(L['season_id'])
			n += 1
		if limit_page >= page:
			break
def wiki_search(t):
	# 有個很大的問題就是 .... 從bilibili抓下來的資料都是簡體字或是大陸翻譯，導致WIKI找不到結果
	url = 'https://zh.wikipedia.org/wiki/'+quote(t)
	r = requests.get(url)
	obj = BeautifulSoup(r.text, "html.parser")
	nn = 0 # 空次數
	ret = ''
	for p in obj.find_all('div', {'class':'mw-content-ltr'})[0].find_all('p'):
		if p.text == '':
			nn +=1
		else:
			ret += p.text
		if nn >= 2:
			return ret
'''
因網頁排版無統一格式導致很難抓到想要的東西 QQ
def moegirl_search(t):
	url = 'https://zh.moegirl.org/'+quote(t)
	r = requests.get(url)
	obj = BeautifulSoup(r.text, "html.parser")
	body = obj.find_all('div', {'id':'bodyContent'})[0].text
	body = re.sub('\s+', '', body)
	s = re.search('劇情簡介([^0-9].*?)登場人物', body)
	if s:
		return s.group(1)
	else:
		return ''
'''

def main():
	start()

def show_search(s):
	url = 'https://bangumi.bilibili.com/anime/'+season_id[s]
	r = requests.get(url)
	obj = BeautifulSoup(r.text, "html.parser")
	txt = obj.find_all("div", {'class':'info-row info-cv'})[0].get_text('', strip=True).replace('：、', '：')
	txt2 = obj.find_all("div", {'class':'info-row info-update'})[0].get_text('', strip=True)
	txt2 = re.sub('[0-9]+年[0-9]+月.+,', '', re.sub('\s+', '', txt2))
	wiki = wiki_search(title[s])
	print("番名：",title[s])
	print(txt)
	print("人氣：",favorites[s])
	print("最新集數：",newest_ep_index[s])
	print("總共集數：",total_count[s])
	print(txt2)
	print('簡介\n', wiki)
	# if int(week[s]) == 0:
	# 	print("星期日更新！")
	# else:
	# 	print("星期",week[s],"更新！")


if __name__ == '__main__':
	main()
	s = input('\n\nplz choose?(only index number) ')
	while s:
		try:
			if s != -1:
				show_search(int(s)-1)
		# except ValueError:
		# 	print(getpass.getuser(), '! Your input has a ValueError !', 'plz see ReadMe file or shutdown your pc.')
		# 	s = -1
		# except IndexError:
		# 	print(getpass.getuser(), '! Your input has a IndexError !', 'plz see index range or shutdown your pc.')
		# 	s = -1
		except:
			print(getpass.getuser(), '! This project has some Errors !', 'I will shutdown your pc soon.')
			for i in range(5,0, -1):
				print(i)
				time.sleep(1)
			print('Just kidding!')
			s = False
		else:
			s = input('\n\nplz choose? ')