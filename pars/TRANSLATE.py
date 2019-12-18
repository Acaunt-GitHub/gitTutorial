import requests
import proxy
import os
import time, csv
from bs4 import BeautifulSoup
import xlsxwriter

def main():
    translate = []
    with open('reciepe.csv', 'r',encoding='utf-8') as fp:
        reader = csv.reader(fp, delimiter=',', quotechar='"')
        # next(reader, None)  # skip the headers
        data = [row for row in reader]
        data = [list(dict.fromkeys(i)) for i in data]

    qq = 1
    tm = time.time()
    for i in data:
        tt = time.time()
        try:
            Article = perevod(i[0], 'ru',qq)
            # time.sleep(random.randint(1,3)/10)
            Picture = i[1]
            Ingredients = perevod(i[2], 'ru',qq)
            # time.sleep(random.randint(1, 3) / 10)
            Method = perevod(i[3], 'ru',qq)
            translate.append([Article, Picture, Ingredients, Method])
            print(qq, '/',len(data),'\t', round(time.time()- tt),'/',round(time.time()- tm),'сек','\t',Article)
            xwrt(translate)
            qq += 1
        except BaseException as ex:
            continue

def xwrt(translate):
    workbook = xlsxwriter.Workbook("RU_RECIEPE.xlsx")
    worksheet1 = workbook.add_worksheet()
    for i in range(len(translate)):
        for j in range(len(translate[i])):
            worksheet1.write(i, j,translate[i][j])
    worksheet1.set_column(0, 0, 20)
    worksheet1.set_column(1, 0, 75)
    worksheet1.set_column(2, 0, 75)
    worksheet1.set_column(3, 0, 75)
    workbook.close()
    pass

def perevod(text,lang,index):
     URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate?'
     KEY = 'trnsl.1.1.20171024T135728Z.3dba81de8cb572e1.b090ab30fc00d261cbfb2a787343ba3e4ee7c9ea'
     # if index % 1 == 0:
     #     try:
     #        f = open('proxies.txt', 'r')
     #        prox = f.read()
     #        f.close()
     #        result = prox.split('\n')
     #        open('red_ip.txt', 'a').write(str(result[0]) + '\n')
     #        os.remove('proxies.txt')
     #     except FileNotFoundError as f:
     #         pass

     proxy_ = proxy.Proxy()
     proxy_ = proxy_.get_proxy()
     r = requests.post(URL, data={'key': KEY, 'text':text, 'lang': lang}, proxies = {'https': proxy_},timeout=60).text
     time.sleep(0.5)
     trans_text = eval(r)
     return trans_text['text'][0]

if __name__ == '__main__':
    main()
