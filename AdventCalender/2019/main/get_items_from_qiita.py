#!usr/env/bin py
#-*- coding : utf-8 -*-

import numpy as np
import pandas as pd
import requests, json, time, MeCab, sys, re, pickle, gzip, wordcloud
from PIL import Image
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties

## 関数定義
def call_qiita_api(header, per_page = None, query = None, page = None):
    ## api指定
    get_items_api = 'https://qiita.com/api/v2/items'
    params = {'per_page' : per_page
        , 'query' : query
        , 'page' : page}
    datas = requests.get(get_items_api, params = params, headers = header)
    return datas

def regs_body_text(text):
    ## 正規化パターン
    reg_pattern = re.compile('(\n|\t| |　|-|~|-|`|:|;|_|\*|\!|\?|！|？|\+|\$|#|\[|\])')
    tmp = re.sub(reg_pattern, '', text.lower())
    target_type = re.compile('(アドベントカレンダー|adventcalendar)')
    if not re.search(target_type, tmp):
        return None, None
    calender_type = re.compile('(この記事は)\w+?(adventcalendar2019)')
    if not re.search(calender_type, tmp):
        return None, None,
    url_strings = re.search(calender_type, tmp).group()
    get_calender_type = re.sub('(この記事は|adventcalendar2019)', '', url_strings)
    return get_calender_type, tmp

mecab = MeCab.Tagger('-Owakati')
mecab.parse('')

def parse_text(text, parser = mecab):
    part = ['名詞','動名詞']
    parsed_text = []
    t = parser.parseToNode(text)
    while t:
        parts = t.feature.split(',')
        if parts[0] in part:
            parsed_text.append(t.surface)
        t = t.next
    return parsed_text

## 各種設定
time_sleeper = 1.0

## 日付をAdventCalendar仕様にする
start_date = '2019/12/01'
end_date = '2019/12/20'
date_list = [d.strftime('%Y-%m-%d') for d in pd.date_range(start_date, end_date)]
from_list = date_list[:-1]
to_list = date_list[1:]

## access_keyの読み込み
with open('config/api_key.txt') as f:
    k = f.read()
header = {'Authorization' : 'Bearer {}'.format(k)}

## データ取得
dataset = {}
for f,t in zip(from_list, to_list):
    print('FromDate : {} ToDate : {}'.format(f,t))
    time.sleep(time_sleeper)
    datas = call_qiita_api(header = header, per_page = 100, query = 'created:>{} created:>{}'.format(f, t))
    rows = 100 if int(datas.headers['Total-Count']) / 100 >= 100 else int(datas.headers['Total-Count']) / 100
    for r in range(int(rows)):
        r += 1
        data_r = call_qiita_api(header = header, per_page = 100, query = 'created:>{} created:>{}'.format(f, t), page = r)
        for i in range(100):
            sys.stdout.write('\r {}/{} | {}/100'.format(r, int(rows)+1, i+1))
            data = data_r.json()[i]
            if not regs_body_text(data['body'])[0]:
                continue
            calender, texts = regs_body_text(data['body'])
            parsed_texts = parse_text(texts)
            if calender not in dataset.keys():
                dataset[calender] = {}
                dataset[calender]['texts'] = []
                dataset[calender]['parsed_text'] = []
            dataset[calender]['texts'].append(texts)
            dataset[calender]['parsed_text'].append(parsed_texts)
    print()

## データ保存
with gzip.open('qiita_adventcalender.pickle.gz','w') as f:
    pickle.dump(dataset, f)
