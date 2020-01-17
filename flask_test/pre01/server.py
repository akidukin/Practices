#usr/env/bin py
#-*- encoding : utf-8 -*-

from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from py_modules import modules_temporary
import os, time

upload_folder = './static/image/uploader/'
allowed_extension = set(['png','jpg','tsv','csv'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = upload_folder

@app.route('/')
def index():
    graph_types = ['sphere', 'banana']
    return render_template('index.html', graph_types = graph_types, x = os.getcwd())

@app.route('/test', methods = ['GET'])
def test():
    res = request.args.get('input the number')
    tm = modules_temporary.temporary(int(res))
    tm_res = tm.get_result()
    return render_template('result01.html', x = res, y = tm_res)

@app.route('/uploader', methods = ['POST'])
def test01():
    res = request.files['pict']
    res.save(os.path.join(app.config['UPLOAD_FOLDER'], res.filename))
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], res.filename)
    tm = modules_temporary.temporary_pict(file_path)
    tm_res = tm.get_result()
    return render_template('result02.html', x = file_path, y = tm_res)

@app.route('/plot_temporary', methods = ['GET'])
def test02():
    res = request.args.get('graph_type')
    tm = modules_temporary.temporary_pict02()
    save_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'sphere.png')
    result_fig = tm.plot()
    result_fig.savefig(save_filepath)
    return render_template('result03.html', x = save_filepath, y = res)

@app.route('/plot_xyz_point', methods = ['GET'])
def test03():
    res_x = request.args.get('x')
    res_y = request.args.get('y')
    tm = modules_temporary.temporary_pict02()
    save_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'sphere.png')
    if os.path.exists(save_filepath):
        os.remove(save_filepath)
    result_fig = tm.plot_point(float(res_x), float(res_y))
    result_fig.savefig(save_filepath)
    return render_template('result03.html', x = save_filepath, y=(float(res_x),float(res_y)))

if __name__ == '__main__':
    app.debug = True
    print(app.url_map)
    app.run(host = '0.0.0.0', port = 8080)