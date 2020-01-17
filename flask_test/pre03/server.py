#!usr/enb/bin py
#-*- coding : utf-8 -*-

from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import random, os
from bin.get_predict_number import get_number

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/upload'

@app.route('/')
def initialize():
    return render_template('index.html', finish = False)

@app.route('/identify_number', methods = ['POST'])
def defined_number():
    post_request = request.files['upload_picture']
    random_number = str(random.random())[5:]
    file_name = random_number + post_request.filename
    save_filepath = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    post_request.save(save_filepath)

    gn = get_number(save_filepath)
    res1, res2 = gn.call_value()
    res2 = [(x[0], round(x[1] * 100,2)) for x in res2]

    return render_template('index.html', finish = True, picture_path = save_filepath, predict_value1 = res1, predict_value2 = res2)

if __name__=='__main__':
    app.debug=True
    app.run('0.0.0.0', port = 8080)