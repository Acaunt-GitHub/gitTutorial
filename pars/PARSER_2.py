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
def parser_reciepe():
	# Read CSV file
	try:
		open('reciepe_list.csv', 'r', encoding="utf-8")
	except FileNotFoundError as ex:
		open('reciepe_list.csv', "w+").write('')
	with open('reciepe_list.csv', 'r', encoding="utf-8") as fp:
		reader = csv.reader(fp, delimiter=',', quotechar='"')
		# next(reader, None)  # skip the headers
		data_read = [row for row in reader]

	list_ref = [''.join(i)for i in data_read]
	#list_ref = list_ref[0]
	data = []  # Artile | Picture | Ingredients | Method
	tm = time.time()
	qq = 1
	for z in  list_ref:

		try:
			req = Request(site1+z, headers=hdr)
			page = urlopen(req)
			soup = BeautifulSoup(page, features="lxml")
			Article = soup.find_all('h1')[0].text
			rec = soup.find(class_="img-container ratio-11-10")
			Picture = str(rec.find_all('img')[0].attrs['src']).replace("//", '')
			rec = soup.find(class_="ingredients-list__content")

			e = rec.find_all('li')
			ee = [i.text for i in e]
			for x in range(len(ee)):
				sp = re.search(r'[ABCDEFGHIJKLMNOPQRSTUVWXYZ]', ee[x][1:])
				if sp != None:
					ee[x] = ee[x][:sp.span()[0]+1]
			Ingredients = '. '.join(ee)
			rec = soup.find(class_="method")
			Method = rec.text
			data.append([Article, Picture, Ingredients, Method])

			print(qq,round(time.time() - tm), z)

			qq+=1
			time.sleep(random.randint(1, 2)/10)
		except BaseException as e:
			# print(e)
			# print("ВНИМАНИЕ!!! Ошибка парсинга рецептов")
			with open('reciepe_savecopy.csv', 'w', encoding='utf-8',newline='') as fp:
				writer = csv.writer(fp, delimiter=',')
				writer.writerows(data)
	# Write CSV file
	with open('reciepe.csv', 'w',encoding='utf-8',newline='') as fp:
		writer = csv.writer(fp, delimiter=',')
		writer.writerows(data)

	#Read CSV file
	try:
		open('reciepe.csv', 'r')
	except FileNotFoundError as ex:
		open('reciepe.csv', "w+",encoding='utf-8',newline='')
		writer = csv.writer(fp, delimiter=',')
		writer.writerows('')

	with open('reciepe.csv', 'r',encoding='utf-8') as fp:
		reader = csv.reader(fp, delimiter=',', quotechar='"')
		# next(reader, None)  # skip the headers
		data = [row for row in reader]
		data = [list(dict.fromkeys(i)) for i in data]
		data2=[]
		for i in data:
			on,tw = i.pop(0),i.pop(0)
			if i[-1] !='':
				lst = i.pop(-1)
			else:
				lst = i.pop(-2)
			md = ''.join(i)
			data2.append([on,tw,md,lst])
	with open('reciepe.csv', 'w',encoding='utf-8',newline='') as fp:
		writer = csv.writer(fp, delimiter=',')
		writer.writerows(data2)
	return data


if __name__ == '__main__':
	parser_reciepe()