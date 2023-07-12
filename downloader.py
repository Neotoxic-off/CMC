import os
import json
import zipfile
import requests
import xmltodict, json

class Downloader:
    def __init__(self):
        self.host = "https://crackmes.one"
        self.feed = f"{self.host}/rss/crackme"
        self.download = f"{self.host}/static/crackme"
        self.crackme = []

        self.__load__()

    def __load__(self):
        response = requests.get(self.feed)
        xml = xmltodict.parse(response.content)
        data = json.loads(json.dumps(xml))
        path = None

        for item in data["rss"]["channel"]["item"]:
            id = item["guid"][29:]
            path = f"{item['author']}/{id}"
            print(f"{id}:")
            self.__setup__(item["author"], path)
            self.__download__(id, item["author"], path)
            self.__about__(path, item)

    def __setup__(self, author, path):
        if (os.path.exists(author) == False):
            os.mkdir(author)
        if (os.path.exists(path) == False):
            os.mkdir(path)

    def __about__(self, path, item):
        print(f"\tinformation")
        info = [
            f"Title: {item['title']}\n",
            f"Author: {item['author']}\n",
            f"OS: {item['category']}\n",
            f"Description: {item['description']}\n",
            f"Release date: {item['pubDate']}\n"
        ]

        with open(f"{path}/about.txt", "w") as f:
            f.writelines(info)

    def __download__(self, id, author, path):
        print(f"\tdownloading")
        response = requests.get(f"{self.download}/{id}.zip")

        with open(f"{path}/{id}.zip", "wb") as f:
            f.write(response.content)
        self.__extract__(path, f"{id}.zip")

    def __extract__(self, path, file):
        print(f"\textracting")

        with zipfile.ZipFile(f"{path}/{file}", 'r') as zip:
            zip.extractall(path, pwd=self.host[8:].encode())

if (__name__ == "__main__"):
    Downloader()
