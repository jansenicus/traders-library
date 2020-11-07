#!/usr/bin/env python
# coding: utf-8

class stoclover():

    def __init__(self, jenis='saham', directory='data'):
        # jenis ini bisa saham atau ihsg
        self.url = "https://www.stoclover.com/download-data-eod-chart-{}-amibroker/".format(jenis.lower())
        self.jenis = jenis
        self.directory = directory
        self.files_urls = self.visit()

        from os.path import isdir
        from os import mkdir
        if not isdir(directory):
            mkdir(directory)

    def url(self):
        print(self.url)

    def jenis(self):
        print(self.jenis)

    def directory(self):
        print(self.directory)
      
    def visit(self):
        from bs4 import BeautifulSoup
        from requests import get
        html = get(self.url).text
        soup = BeautifulSoup(html, features="lxml")
        files_urls = soup.select('a[href*="dropbox.com/s/"]')
        return files_urls

    def file_downloader(self, href):
        from requests import get
        from re import search
        from os.path import isfile
        import sys 
        r = get(href)
        filename = self.directory + "/" + search(r'filename="(.+)"', r.headers.get('content-disposition')).group(1)
        str_display = "downloading: " + filename
        str_display = '{:>50}'.format(str_display)
        sys.stdout.write(str_display +"\n")
        if not isfile(filename):
            open(filename, 'wb').write(r.content)
        sys.stdout.flush()

    def download_last_file(self):
        href = self.files_urls[-1]
        self.file_downloader(href['href'])

    def download_last_files(self, days_back=7):
        import sys
        hrefs = self.files_urls[-1*int(abs(days_back)):-1]
        for i in range(0, len(hrefs)):
            str_percentage = '{:5.2f}'.format(i/len(hrefs)*100)
            str_display = '{:>50}'.format(str(i)+" of "+str(len(hrefs))+ " " + self.jenis +" files downloaded: " + str_percentage + "% ")
            sys.stdout.write(str_display +"\r")
            self.file_downloader(hrefs[i]['href'])


stoclover(jenis='saham', directory='saham').download_last_files(days_back=7)
stoclover(jenis='ihsg', directory='ihsg').download_last_files(days_back=7)