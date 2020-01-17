#!usr/env/bin py
#-*- coding : utf-8 -*-

import numpy as np
import pandas as pd
import requests, json, time, MeCab, sys, re, pickle, gzip, wordcloud
from PIL import Image
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties

with gzip.open('qiita_adventcalender.pickle.gz', 'rb') as f:
    dataset = pickle.load(f)

def check_word(word):
    compiler = re.compile('(https|http|\(|\)|//|co|jp|[0-9]|adventcalender|2019|calendar|アドベントカレンダー|/|\.|\.png|x|\||www|adventcalendar|adventar|org|calendars)')
    return re.sub(compiler, '', word) == ''

fonts = '/usr/share/fonts/ipa-gothic/ipag.ttf'

## WordCloudで可視化
keys_len = len(dataset.keys())
plot_picture = int(keys_len / 9) + 1
plot_area = np.arange(0,9,1).reshape(3,3)
keys = sorted(dataset.keys())
fp = FontProperties(fname = fonts)
k = 0
for pp in range(plot_picture):
    fig,axes = plt.subplots(nrows = 3, ncols = 3, figsize = (10,10))
    for i in range(9):
        target_key = keys[k]
        wc = wordcloud.WordCloud(
                font_path = fonts
                , prefer_horizontal = 1
                , max_words = 300
                , background_color = 'white'
                , colormap = 'RdYlBu'
                , contour_color='pink'
                , width = 750
                , height = 750)
        n,m = [x.item() for x in np.where(plot_area == i)]
        plot_data = ' '.join([y for x in dataset[target_key]['parsed_text'] for y in x if not check_word(y)])
        wc_gen = wc.generate(plot_data)
        axes[n,m].imshow(wc_gen, interpolation = 'bilinear')
        axes[n,m].set_title('AdventCalendar No{} : {}'.format(k, target_key), FontProperties = fp, color = 'gray', fontsize = 10)
        axes[n,m].axis('off')
        k += 1
    plt.subplots_adjust(left=0.1, right=0.95, bottom=0.1, top=0.95)
    plt.savefig('{}_wordcloud.png'.format(pp))
    plt.close()

## 索引出力
for i in range(keys_len):
    print('|{}|{}|{}|'.format(int(i/9)+1,i,keys[i]))