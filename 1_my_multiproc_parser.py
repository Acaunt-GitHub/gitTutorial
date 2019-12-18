#! -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import time, random
import re, csv
from multiprocessing import Pool

hdr = {'User-Agent': 'Mozilla/5.0'}

addd = ['healthy', 'dinner-ideas-0', 'family-kids', 'cakes-baking', 'cuisines',
        'dishes', 'everyday', 'cocktails-drinks', 'ingredients', 'occasions',
        'quick-easy', 'seasonal', 'special-diets', 'vegetarian', 'more-recipe-ideas']

'''
            page = urlopen(req)
            soup = BeautifulSoup(page, features="lxml")
            rec = soup.find(class_='view-content')
            fnd = rec.find_all('li', attrs={'class': ''})
            r = [fnd[i].find_all('a') for i in range(len(fnd))]
            ref = [r[i][0].attrs['href'] for i in range(len(r))]
            
            
            with open('reciepe_list.csv', 'w', encoding='utf-8', newline='') as fp:
            writer = csv.writer(fp, delimiter=',')
            writer.writerows(list_ref)
            
            def unique(a):
                s = set()
                for i in a:
                    if i not in s:
                        s.add(i)
                return list(s)
                
            req = Request(st, headers=hdr)
'''

def get_all_links(html):
    page = urlopen(html)
    soup = BeautifulSoup(page, features="lxml")
    rec = soup.find(class_='index-content-2lnSO').find_all('a', attrs={'class': 'snippet-link'})
    print([i.attrs['href'] for i in rec])


def main():
    ref = ['https://www.avito.ru/rossiya/hobbi_i_otdyh?p={0}'.format(i) for i in range(1,100,1)]
    get_all_links('https://www.avito.ru/rossiya/hobbi_i_otdyh?p=1')

    start = time.time()
    with Pool(10) as p:
        p.map(get_all_links, ref)
    # for i in ref:
    #     get_all_links(i)
    finish = time.time() - start
    print(finish)
    pass
if __name__ == '__main__':
    main()
