import requests
from bs4 import BeautifulSoup
import time
class Proxy (object):
    proxy_url = 'https://www.ip-adress.com/proxy-list'
    proxy_list = []

    def __init__(self):
        try:
            f = open('proxies.txt', 'r')
            prox = f.read()
            f.close()
            result = prox.split('\n')
        except:
            print('[i] No file proxies.txt')
            r = requests.get(self.proxy_url).text
            soup = BeautifulSoup(r, "lxml")
            table = soup.find('tbody')
            result = []
            for i in table.find_all('tr'):
                prox = i.find('td').text
                result.append(prox)

        self.proxy_list = result

    def get_proxy(self):
        for proxy in self.proxy_list:
            f2 = open('proxies.txt', 'r')
            prox = f2.read()
            f2.close()
            result2 = prox.split('\n')
            if proxy in result2:
                continue
            url = 'http://' + proxy
            try:
                r = requests.get('https://vk.com', proxies = {'https': url},timeout=3)
                time.sleep(0.3)
                if r.status_code == 200:
                    print ('Proxy--- ',proxy)
                    open('proxies.txt','w+').write(proxy)
                    return url
                if proxy == self.proxy_list[-1]:
                    time.sleep(0.2)
                    r = requests.get(self.proxy_url).text
                    soup = BeautifulSoup(r, "lxml")
                    table = soup.find('tbody')
                    result = []
                    for i in table.find_all('tr'):
                        prox = i.find('td').text
                        result.append(prox)
                    self.proxy_list = result
                    self.get_proxy()
            except requests.exceptions.ConnectionError:
                continue

        return None


if __name__ == '__main__':
    proxy = Proxy()
    proxy = proxy.get_proxy()
    print(proxy)
    r = requests.get('https://vk.com/', proxies={'https': proxy})
    print(r.text)
    input()