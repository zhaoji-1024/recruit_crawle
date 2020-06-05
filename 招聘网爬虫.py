import requests
from bs4 import BeautifulSoup
import json

class ZhaoPin(object):

    def __init__(self):
        self.url = "https://search.51job.com/list/000000,000000,0000,00,9,99,python,2,{}.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
        }


    def get_html_text(self, url):
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            try:
                return response.content.decode("gbk")
            except UnicodeDecodeError:
                return response.content.decode()
        else:
            return None


    def parse_list_page(self, text):
        soup = BeautifulSoup(text, "lxml")
        detail_urls = []
        p = soup.find_all("p", attrs={"class":"t1"})
        for e in p:
            url = e.find("a").get("href")
            detail_urls.append(url)
        return detail_urls


    def parse_detail_page(self, text):
        soup = BeautifulSoup(text, "lxml")
        cn = soup.find("div", attrs={"class":"cn"})
        position_title = cn.find("h1").get("title")
        company = cn.find("a", attrs={"class":"catn"}).get("title")
        info = "".join(cn.find("p", attrs={"class":"msg ltype"}).stripped_strings)
        position_message = "".join(soup.find("div", attrs={"class":"bmsg job_msg inbox"}).stripped_strings)
        try:
            contact_way = "".join(soup.find("div", attrs={"class":"bmsg inbox"}).stripped_strings)
        except AttributeError:
            contact_way = None
        company_message = "".join(soup.find("div", attrs={"class":"tmsg inbox"}).stripped_strings)
        item = {}
        item["position_title"] = position_title
        item["company"] = company
        item["info"] = info
        item["position_message"] = position_message
        item["contact_way"] = contact_way
        item["company_message"] = company_message
        return item


    def save_item_toJson(self, item):
        with open("./data/recruit_crawel.json", "a", encoding="utf-8") as fp:
            json.dump(item, fp, ensure_ascii=False)
            fp.write("\n")
            print(item["position_title"] + "save to local document successfully...")


    def run(self):
        for i in range(2,70):
            text = self.get_html_text(self.url.format(i))
            detail_urls = self.parse_list_page(text)
            detail_urls = [u for u in detail_urls if u[-1] == "0"]
            for d_u in detail_urls:
                text = self.get_html_text(d_u)
                item = self.parse_detail_page(text)
                self.save_item_toJson(item)