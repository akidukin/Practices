# Qiita Advent Calender の可視化するよ

この記事は、All About Group（株式会社オールアバウト） Advent Calendar 2019 20日目の記事です。
もういくつ寝るとクリスマスですね。
大人になった今サンタクロースが本当に来てくれると信じています。

初めての方は初めまして、Akidukin14 です。
普段は AllAbout の広告配信システムの機械学習周りや、分析結果の可視化等を担当しています。

今回初めて Advent Calendar 書くので、思いついたことをやってみようと思います。

# やった事(概要)

Qiita Advent Calender の各カレンダー内部の記事データを可視化をしてみる
(Qiitaに投稿されている記事のみを対象...)

# 記載の内容(Topics)

- 背景
- やった事(箇条書き)
- 結果
- やった事(詳細)
  - アドベントカレンダーの記事本文を抽出
  - 記事本文を自然言語処理する(分かち書き)
  - WordCloudで可視化
- 参考
- AdventCalender索引

# 背景

(2019/12/n 時点)
**カレンダー数 : 770**
**参加者数 : 13,414**

初めてAdvent Calender参加するんですが、真っ先に思ったこと。

ぱねぇ。カレンダー数ぱねぇ。参加者ぱねぇ。

ピンポイントで自分の興味のあるカレンダーってどこだ...??
って思ったのが動機です。

# やった事(箇条書き)

1. アドベントカレンダーの記事本文を抽出
2. 記事本文を自然言語処理する(分かち書き)
3. WordCloudで可視化

# 結果

先に結果を載せます。
結果だけで十分という方はこちらをご確認ください。
(凄くライトにやったので、結果に偏りがあると思います、すみません...)

## 画像1
## 画像2
## 画像3
## 画像4
## 画像5
## 画像6
## 画像7
## 画像8
## 画像9
## 画像10
## 画像11
## 画像12
## 画像13
## 画像14
## 画像15
## 画像16
## 画像17
## 画像18
## 画像19
## 画像20
## 画像21
## 画像22
## 画像23
## 画像24
## 画像25
## 画像26
## 画像27
## 画像28
## 画像29
## 画像30
## 画像31
## 画像32


# 1. アドベントカレンダーの記事本文を抽出

1. QiitaAPIをPythonから叩き記事のデータを取得

```python:call_qiita_api
def call_qiita_api(header, per_page = None, query = None, page = None):
    ## api指定
    get_items_api = 'https://qiita.com/api/v2/items'
    params = {'per_page' : per_page
        , 'query' : query
        , 'page' : page}
    datas = requests.get(get_items_api, params = params, headers = header)
    return datas
```
2. これはアドベントカレンダーだ！と思わしき記事を取得対象にしてデータを取得する

```python:regs_body_text
### コードがめっちゃ汚い...
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
```

# 2. 記事本文を自然言語処理する(分かち書き)

1. MeCabで品詞を指定し単語に分割する

```python:parse_text
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
```

# 3. WordCloudで可視化

1. 9x9のエリアに随時描画していくように対応

```python:make_wordcloud
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
        sys.stdout.write('\r {}/{}'.format(k, keys_len))
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
        axes[n,m].set_title('AdventCalendar : {}'.format(target_key), FontProperties = fp, color = 'gray', fontsize = 10)
        axes[n,m].axis('off')
        k += 1
    plt.subplots_adjust(left=0.1, right=0.95, bottom=0.1, top=0.95)
    plt.savefig('{}_wordcloud.png'.format(pp))
    plt.close()
```

# 参考URL
QiitaAPIの利用 :
    https://qiita.com/arai-qiita/items/94902fc0e686e59cb8c5

# AdventCalender 索引

今回利用させて頂きましたカレンダーの種類です。
索引として用意させていただきました。

|画像No|AdventCalenderNo|AdventCalender名|
|:--:|:--:|:--:|