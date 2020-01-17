#!usr/env/bin py
#-*- coding : utf-8 -*-

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    selects = ['かぐや様は','かわいい','綺麗','尊い','神']
    ip = request.cookies
    return render_template('index.html', selects = selects, ip = ip)

@app.route('/test', methods = ['GET','POST'])
def test():
    selects = ['かぐや様は','かわいい','綺麗','尊い','神']
    ip = request.environ
    if request.method == 'GET':
        res = request.args.get('get_value')
    elif request.method == 'POST':
        res = request.form['text']
        res2 = request.form['radio_type']

    return render_template('index.html', x = res, s = request.method, selects = selects, x1 = res2, ip = ip)

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 80)