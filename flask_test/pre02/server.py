#!usr/enb/bin py
#-*- coding : utf-8 -*-

from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import os, pandas as pd

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/uploader'

@app.route('/', methods = ['GET'])
def test():
    return '11111'

@app.route('/uploader', methods = ['POST'])
def uploader():
    res = request.files['uploader']
    save_filepath = os.path.join(app.config['UPLOAD_FOLDER'], res.filename)
    res.save(save_filepath)
    return redirect(url_for('return_values', filepath=save_filepath))

@app.route('/uploader/<filepath>')
def return_values(filepath):
    df = pd.read_table(filepath, sep = ',', header = None)
    print(df.head())
    return df.head()

if __name__=='__main__':
    app.debug=True
    app.run('0.0.0.0', port = 8080)