# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, abort, render_template, make_response
from crawler import mobo_crawler

app = Flask(__name__)

# mobo-crawler-router
@app.route('/mobo', methods=['POST'])
def mobo():
    # import mobo_crawler() from crawler.py
    mobo_crawler()
    return "end"

#目前是使用兩次encode到'CP950'，推測是Input1.csv是在win建立的，在linux要encode
@app.route('/download')
def download():
    f = open("Input1.csv", "r", encoding='CP950')
    response = make_response(f.read().encode('CP950'))
    response.headers["Content-Disposition"] = "attachment; filename=download.csv"
    return response

@app.route('/')
def hello(name = None):
    return render_template('hello.html', name=name)

@app.route('/123')
def hi():
    a = ['中王']
    string= "中文"
    print("嗨嗨")
    print(string[1])
    return ("False")

@app.errorhandler(404)
def page_no_found(e):
    return jsonify(Error='Page No Found', status=404)

if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0', port=8080)
    # setting host='0.0.0.0' and port=8080 running on cloud9

