import requests
from bs4 import BeautifulSoup
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def topic_crawl():
    req = requests.get('https://languagedrops.com/word/en/english/icelandic')
    soup = BeautifulSoup(req.text, 'html.parser')

    topics = []
    for topic in soup.select('h2.linkable-word-box-text'):
        topic = topic.text.lower().replace(" ", "_").replace(".", "_")
        topics.append(topic)

    return topics


def word_crawl(topic_name):
    req = requests.get('https://languagedrops.com/word/en/english/icelandic/topics/%s' % topic_name)
    soup = BeautifulSoup(req.text, 'html.parser')

    voca_eng = soup.select('div.topic-row-first-word')
    voca_isk = soup.select('div.topic-row-second-word')
    voca = {}

    # of = open('Out/%s.txt' % topic_name, mode='w')
    for i in range(len(voca_eng)):
        word_eng = voca_eng[i].text.encode('latin-1')
        word_isk = voca_isk[i].text.encode('latin-1')
        # of.write(word_eng + '\t' + word_isk + '\n')
        voca[word_eng] = word_isk

    # of.close();
    return voca

if __name__ == '__main__':
    data = {}
    flag = True
    for topic in topic_crawl():
        if topic == '_com':
            flag = True
        if flag:
            print(topic)
            data[topic] = word_crawl(topic)

    with open(os.path.join(BASE_DIR, 'Icelandic.json'), 'w+') as json_file:
        json.dump(data, json_file)

