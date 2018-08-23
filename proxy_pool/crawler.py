import json
import re
from utils import get_page
from pyquery import PyQuery as pq

#通过元类实现动态获取所有以crawl开头的方法列表
class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    #此处未遍历调用所有以crawl开头的函数返回代理，直接使用了付费代理
    def get_proxies(self):
        proxies = []
        for proxy in self.crawl_xiguadaili():
            proxies.append(proxy)
        print('成功抓取代理')
        return proxies
    def crawl_premproxy(self):
        for i in ['China-01','China-02','China-03','China-04','Taiwan-01']:
            start_url = 'https://premproxy.com/proxy-by-country/{}.htm'.format(i)
            html = get_page(start_url)
            if html:
                ip_address = re.compile('<td data-label="IP:port ">(.*?)</td>') 
                re_ip_address = ip_address.findall(html)
                for address_port in re_ip_address:
                    yield address_port.replace(' ','')

    def crawl_xroxy(self):
        for i in ['CN','TW']:
            start_url = 'http://www.xroxy.com/proxylist.php?country={}'.format(i)
            html = get_page(start_url)
            if html:
                ip_address1 = re.compile("title='View this Proxy details'>\s*(.*).*")
                re_ip_address1 = ip_address1.findall(html)
                ip_address2 = re.compile("title='Select proxies with port number .*'>(.*)</a>") 
                re_ip_address2 = ip_address2.findall(html)
                for address,port in zip(re_ip_address1,re_ip_address2):
                    address_port = address+':'+port
                    yield address_port.replace(' ','')
    
    def crawl_kuaidaili(self):
        for i in range(1, 4):
            start_url = 'http://www.kuaidaili.com/free/inha/{}/'.format(i)
            html = get_page(start_url)
            if html:
                ip_address = re.compile('<td data-title="IP">(.*?)</td>') 
                re_ip_address = ip_address.findall(html)
                port = re.compile('<td data-title="PORT">(.*?)</td>')
                re_port = port.findall(html)
                for address,port in zip(re_ip_address, re_port):
                    address_port = address+':'+port
                    yield address_port.replace(' ','')

    def crawl_xicidaili(self):
        for i in range(1, 3):
            start_url = 'http://www.xicidaili.com/nn/{}'.format(i)
            headers = {
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Cookie':'_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWRjYzc5MmM1MTBiMDMzYTUzNTZjNzA4NjBhNWRjZjliBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMUp6S2tXT3g5a0FCT01ndzlmWWZqRVJNek1WanRuUDBCbTJUN21GMTBKd3M9BjsARg%3D%3D--2a69429cb2115c6a0cc9a86e0ebe2800c0d471b3',
                'Host':'www.xicidaili.com',
                'Referer':'http://www.xicidaili.com/nn/3',
                'Upgrade-Insecure-Requests':'1',
            }
            html = get_page(start_url, options=headers)
            if html:
                find_trs = re.compile('<tr class.*?>(.*?)</tr>', re.S)
                trs = find_trs.findall(html)
                for tr in trs:
                    find_ip = re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td>') 
                    re_ip_address = find_ip.findall(tr)
                    find_port = re.compile('<td>(\d+)</td>')
                    re_port = find_port.findall(tr)
                    for address,port in zip(re_ip_address, re_port):
                        address_port = address+':'+port
                        yield address_port.replace(' ','')
    
    def crawl_ip3366(self):
        for i in range(1, 4):
            start_url = 'http://www.ip3366.net/?stype=1&page={}'.format(i)
            html = get_page(start_url)
            if html:
                find_tr = re.compile('<tr>(.*?)</tr>', re.S)
                trs = find_tr.findall(html)
                for s in range(1, len(trs)):
                    find_ip = re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td>')
                    re_ip_address = find_ip.findall(trs[s])
                    find_port = re.compile('<td>(\d+)</td>')
                    re_port = find_port.findall(trs[s])
                    for address,port in zip(re_ip_address, re_port):
                        address_port = address+':'+port
                        yield address_port.replace(' ','')
    
    def crawl_iphai(self):
        start_url = 'http://www.iphai.com/'
        html = get_page(start_url)
        if html:
            find_tr = re.compile('<tr>(.*?)</tr>', re.S)
            trs = find_tr.findall(html)
            for s in range(1, len(trs)):
                find_ip = re.compile('<td>\s+(\d+\.\d+\.\d+\.\d+)\s+</td>', re.S)
                re_ip_address = find_ip.findall(trs[s])
                find_port = re.compile('<td>\s+(\d+)\s+</td>', re.S)
                re_port = find_port.findall(trs[s])
                for address,port in zip(re_ip_address, re_port):
                    address_port = address+':'+port
                    yield address_port.replace(' ','')

    def crawl_89ip(self):
        start_url = 'http://www.89ip.cn/apijk/?&tqsl=1000&sxa=&sxb=&tta=&ports=&ktip=&cf=1'
        html = get_page(start_url)
        if html:
            find_ips = re.compile('(\d+\.\d+\.\d+\.\d+:\d+)', re.S)
            ip_ports = find_ips.findall(html)
            for address_port in ip_ports:
                yield address_port

    def crawl_data5u(self):
        start_url = 'http://www.data5u.com/free/gngn/index.shtml'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'JSESSIONID=47AA0C887112A2D83EE040405F837A86',
            'Host': 'www.data5u.com',
            'Referer': 'http://www.data5u.com/free/index.shtml',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
        }
        html = get_page(start_url, options=headers)
        if html:
            ip_address = re.compile('<span><li>(\d+\.\d+\.\d+\.\d+)</li>.*?<li class=\"port.*?>(\d+)</li>', re.S)
            re_ip_address = ip_address.findall(html)
            for address, port in re_ip_address:
                result = address + ':' + port
                yield result.replace(' ', '')

    def crawl_xiguadaili(self):
        start_url = 'http://tpv.daxiangdaili.com/ip/?tid=556460803786746&num=10&filter=on'
        html = get_page(start_url)
        if html:
            find_ips = re.compile('(\d+\.\d+\.\d+\.\d+:\d+)', re.S)
            ip_ports = find_ips.findall(html)
            for address_port in ip_ports:
                yield address_port




if __name__ == '__main__':
    crawler = Crawler()
    iplist = crawler.get_proxies()
    print(iplist)
    








                


            
