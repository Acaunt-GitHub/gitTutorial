import requests
from  bs4 import BeautifulSoup
import re

def get_html(url):
    u = 'http://www.papiltd.ru/personal/?login=yes'
    data = {'USER_LOGIN': 'aleksandrabramova@gmail.com', 'USER_PASSWORD': 'aleksandrabramova@gmail.com'}
    response = requests.post(u,data)
    response = requests.get(url)
    return response.text

def get_all_links(html):
    soup = BeautifulSoup(html,'lxml')
    tbs = soup.findAll('a')

    mass = []
    for tb in tbs:
        if re.search(r'\bТовары\b','{0}'.format(tb)) or re.search(r'\bДом\b','{0}'.format(tb)) or re.search(r'\bАксессуары\b','{0}'.format(tb)):
            mass.append('http://www.papiltd.ru'+tb['href'])
    return mass

def get_all_product(html):
    soup = BeautifulSoup(html, 'lxml')
    tbs = soup.find('section',class_='sec-catalog').find('div',class_='container').find('div',class_='row').find_all('a',class_='row catalog-el-title')
    mass = []
    for tb in tbs:
        mass.append('http://www.papiltd.ru'+str(tb['href']))
    return mass

def get_all_page(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    try:
        tbs = soup.find('div', class_='col catalog-pagination-right')
        mass = []
        for tb in tbs:
            mass.append(tb)
        mas_titul = mass[-3]
        page = mas_titul['title']
        namber = page[9:]
        all_links_page = [url]
        for i in range(1,int(namber)+1):
            all_links_page.append('{0}'.format(url)+'?PAGEN_1={0}&SIZEN_1=28'.format(i))
        return all_links_page
    except :
        return url

def data_page(url):
    html = get_html(url)
    soup = BeautifulSoup(html,'lxml')
    name = soup.find('h1', class_='col sec-title-txt').text
    print(name)
    #cen = soup.find('div',itemprop='offers')
    razm = soup.find('div', itemprop='brand').findAll('li')
    for raz in razm:
        if re.search(r'\bРазмер\b','{0}'.format(raz)) or re.search(r'\bАртикул\b', '{0}'.format(raz)):
            print(raz.text)
    #ostatok = ()
    opisaniye = soup.find('div', class_='row product-desc').text
    print(opisaniye)



def main():
    url = 'http://www.papiltd.ru/catalog/'
    all_links = get_all_links(get_html(url))
    links = []
    for link in all_links:
        a = get_all_page(link)
        if isinstance(a, list):
            for i in a :
                links.append(i)
        elif isinstance(a, str):
            links.append(a)
    mass = []
    for i in links:
        page = get_all_product(get_html(i))
        [mass.append(pages) for pages in page]

    #data_page('http://www.papiltd.ru/catalog/kupit/banka_dlya_sypuchikh_produktov_essential/')
    print([data_page(i) for i in mass])

main()
