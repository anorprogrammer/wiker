import os
import pathlib
import re
from typing import List

import requests
from bs4 import BeautifulSoup

CLEANER = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')


def is_valid(url):
    re_pattern = "^[\w]+$"
    if re.match(pattern=re_pattern, string=url):
        return True
    return False


def xa0_remover(text: str):
    cleantext = text.replace(u'\xa0', u' ')
    return cleantext


def tag_remover(text: str):
    cleantext = re.sub(CLEANER, "", str(text))
    return cleantext


def make_dirs():
    data_path = os.getcwd() + '/data'
    extra_path = os.getcwd() + '/extra'

    if os.path.exists(data_path):
        pass
    else:
        os.mkdir(data_path)

    if os.path.exists(extra_path):
        f = open(extra_path + '/pre_urls.txt', 'w')
        f.close()
        f = open(extra_path + '/post_urls.txt', 'w')
        f.close()
    else:
        os.mkdir(extra_path)
        f = open(extra_path + '/pre_urls.txt', 'w')
        f.close()
        f = open(extra_path + '/post_urls.txt', 'w')
        f.close()

        
class Wiker:
    """
    Class for wikipedia dataset collection
    """

    def __init__(self, lang, first_article_link, log: bool = False, data_folder='data', extra_folder='extra'):
        """
        Creates a new instance of Wiker
        Parameters
        ----------
        lang : str
            wikipedia language (default = 'en')
        first_article_link : str
            first article link beginning scrape. Example: Uzbekistan for scraping this url https://en.wikipedia.org/wiki/Uzbekistan
        data_folder : str
            data folder name for saving data (default = 'data')
        extra_folder : str
            extra files folder, folder for storing all wiki page links, invalid wiki page links and etc (default = 'extra')
        """

        self.lang = lang
        self.first_article_link = first_article_link
        self.log = log
        self.data_folder = data_folder
        self.extra_folder = extra_folder

    def __repr__(self):
        return f"Wikipedia is scrapping in {self.lang} language"

    def extra_file_writer(self):
        if self.read_url_count() == 0:
            file_folder = self.extra_folder
            file_name = "pre_urls.txt"
            with open(file=r"{0}\{1}".format(file_folder, file_name), mode='a+') as file:
                file.write(self.first_article_link)
        return "extra file were written successfully"

    def reader(self) -> List:
        file_folder = self.extra_folder
        file_name = "pre_urls.txt"
        with open(file=r"{0}\{1}".format(file_folder, file_name), mode='r') as file:
            names = list(map(lambda x: x.rstrip(), file.readlines()))
        return names

    def read_url_count(self) -> int:
        return len(self.reader())

    def scraper(self) -> dict:
        raw_set = {}
        for url in self.reader():
            try:
                page = requests.get(f"https://{self.lang}.wikipedia.org/wiki/{url}")
                soup = BeautifulSoup(page.content, 'html.parser')
                raw_text = soup.find_all('p')[1]
                raw_set[url] = raw_text
            except Exception as e:
                print(e)
        return raw_set

    def text_cleaner(self) -> dict:
        raw_dict = self.scraper()
        clean_dict = {key: xa0_remover(tag_remover(text=value)) for (key, value) in raw_dict.items()}

        return clean_dict

    def next_urls(self) -> List:
        """
        raw_texts[0].find_all("a")[0].attrs['href']
        """
        raw_texts = self.scraper().values()
        new_list = []
        try:
            for text in raw_texts:
                for url in text.find_all("a"):
                    if str(url.attrs['href']).startswith("/wiki/"):
                        clear_url = str(url.attrs['href']).lstrip("/wiki/")
                        if is_valid(url=clear_url):
                            new_list.append(clear_url)

        except Exception as e:
            print(e)

        return new_list

    def dir_scanner(self):
        dir_name = self.data_folder
        abs_path = pathlib.Path(dir_name)
        count = 0
        for path in os.scandir(abs_path):
            if path.is_file():
                count += 1
        return count

    def cleaned_text_writer(self, text_dict: dict):
        file_folder = self.data_folder
        for name in text_dict.keys():
            with open(r'{0}\{1}.txt'.format(file_folder, name), 'w', encoding="utf-8") as f:
                f.write(text_dict[name])

    def pre_url_writer(self, url_list):
        file_folder = self.extra_folder
        file_name = "pre_urls.txt"
        with open(file=r"{0}\{1}".format(file_folder, file_name), mode='w') as file:
            file.write("\n".join(url_list))
            return "Pre URLs were written successfully"

    def post_url_writer(self, url_list):
        file_folder = self.extra_folder
        file_name = "post_urls.txt"
        with open(file=r"{0}\{1}".format(file_folder, file_name), mode='a') as file:
            file.write("\n".join(url_list))
            return "Post URLs were written successfully"

    def worker(self):
        jobs = (
            self.__repr__(),
            self.reader(),
            self.read_url_count(),
            self.extra_file_writer(),
            self.scraper(),
            self.text_cleaner(),
            self.next_urls(),
            self.dir_scanner(),
            self.cleaned_text_writer(text_dict=self.text_cleaner()),
            self.post_url_writer(url_list=self.scraper().keys()),
            self.pre_url_writer(url_list=self.next_urls()),
        )
        if self.log:
            print(jobs)
        return jobs

    def run(self, scrape_limit):
        make_dirs()
        while self.dir_scanner() < scrape_limit:
            self.worker()
