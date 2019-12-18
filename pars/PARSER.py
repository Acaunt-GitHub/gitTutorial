#! -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import time,random
import re, csv

hdr = {'User-Agent': 'Mozilla/5.0'}
site1 = 'https://www.bbcgoodfood.com'
site = 'https://www.bbcgoodfood.com/recipes/category/'
addd = ['healthy', 'dinner-ideas-0', 'family-kids', 'cakes-baking', 'cuisines',
		'dishes', 'everyday', 'cocktails-drinks', 'ingredients', 'occasions',
		'quick-easy', 'seasonal', 'special-diets', 'vegetarian', 'more-recipe-ideas']

def unique(a):
	s = set()
	for i in a:
		if i not in s:
			s.add(i)
	return list(s)

def parser_link():
	#addd = ['more-recipe-ideas']
	list_ref = []

	try:
		tt = time.time()
		for i in addd:

			st = site + i
			try:
				req = Request(st, headers=hdr)
			except BaseException as exp:
				print(exp,st)
				continue
			page = urlopen(req)
			soup = BeautifulSoup(page, features="lxml")
			rec = soup.find(class_='view-content')
			fnd = rec.find_all('li', attrs={'class': ''})
			r = [fnd[i].find_all('a') for i in range(len(fnd))]
			ref = [r[i][0].attrs['href'] for i in range(len(r))]
			time.sleep(random.randint(1, 3)/10)
			for j in ref:
				ii=0
				stt = site1 + j
				req = Request(stt, headers=hdr)
				page = urlopen(req)
				soup = BeautifulSoup(page, features="lxml")
				rec = soup.find(class_='view-content')
				fnd = rec.find_all('h3')
				r = [fnd[ii].find_all('a') for i in range(len(fnd))]
				list_ref.extend([r[i][0].attrs['href'] for i in range(len(r))])
				list_ref = unique(list_ref)
				time.sleep(random.randint(1, 3)/10)
				print(len(list_ref), round(time.time() - tt), i, j)
				ii=+1
				with open('reciepe_list.csv', 'w',encoding='utf-8',newline='') as fp:
					writer = csv.writer(fp, delimiter=',')
					writer.writerows(list_ref)

	except BaseException as e:
		print(e)
		print("ВНИМАНИЕ!!! Ошибка парсинга ссылок на рецепты")
		with open('reciepe_list_savecopy.csv', 'w',encoding='utf-8',newline='') as fp:
			writer = csv.writer(fp, delimiter=',')
			writer.writerows(list_ref)



if __name__ == '__main__':
	parser_link()
