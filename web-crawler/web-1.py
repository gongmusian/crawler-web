from flask import Flask, request, jsonify, abort, render_template, make_response
from crawler import mobo_crawler
from requests import get


def isfloat(s):
    try: 
        float(s)
        return True
    except ValueError:
        return False

def check_parameter(param, op):
    msg = []
    if op not in ['sum', 'minus', 'multiply', 'divide']:
        msg.append('Operation is not availabe')
    if None in param:
        msg.append('Lose key')
    if '' in param:
        msg.append('Lose Value')
    for x in param:
        # float() need string or number not None
        if x != None and x != '':
            if isfloat(x) == False:
                msg.append('Value Type Error')
    if len(msg) > 0:
        # list to str
        return False, 406, str(msg)[1:-1]
    else:
        return True, 200, 'OK'

def float_2_dec(number):
    return ('%.2f' %number)

app = Flask(__name__)

# mobo-crawler-router
@app.route('/mobo')
def mobo():
    print("hello1")
    ouput_file_name = mobo_crawler()
    # with open(ouput_file_name, 'r') as csvfile:
    #     response = make_response(csvfile)
    #     response.headers["Content-Disposition"] = "attachment; filename=" + ouput_file_name
    #     return response
    return"end"

@app.route('/download')
def download():
    f = open("Input1.csv", "r", encoding='utf-8')
    csv = """"REVIEW_DATE","AUTHOR","ISBN","DISCOUNTED_PRICE"
"1985/01/21","Douglas Adams",0345391802,5.95
"1990/01/12","Douglas Hofstadter",0465026567,9.95
"1998/07/15","Timothy ""The Parser"" Campbell",0968411304,18.99
"1999/12/03","Richard Friedman",0060630353,5.95
"2004/10/04","Randel Helms",0879755725,4.50"""
    # We need to modify the response, so the first thing we 
    # need to do is create a response out of the CSV string
    f.encode('utf-8').strip()
    response = make_response(f.read())
    # print(f.read())
    # response = make_response(csv)
    # This is the key: Set the right header for the response
    # to be downloaded, instead of just printed on the browser
    response.headers["Content-Disposition"] = "attachment; filename=Input.csv"
    # print("down")
    return response

# @app.route('/downloadjpg')
# def downloadjpg():
#     with open('a.jpg', "wb") as file:
#         response = get("https://preview.c9users.io/gongmusian/flask-hw/crawler-web/web-exercise/999.jpg")
#         file.write(response.content)
#     return file


@app.route('/')
def hello(name = None):
    return render_template('hello.html', name=name)

@app.route('/count', methods=['GET'])
def count():
    op = request.args.get('op')
    value1 = request.args.get('value1')
    value2 = request.args.get('value2')
    param = []
    param.append(value1)
    param.append(value2)
    chk, status, error_msg = check_parameter(param, op)
    if chk:
        if op == 'sum':
            return render_template('count.html', status=status, value1=value1, op='+', value2=value2, answer=float_2_dec(float(value1) + float(value2)), msg=error_msg)
        elif op == 'minus':
            return render_template('count.html', status=status, value1=value1, op='-', value2=value2, answer=float_2_dec(float(value1) - float(value2)), msg=error_msg)
        elif op == 'multiply':
            return render_template('count.html', status=status, value1=value1, op='×', value2=value2, answer=float_2_dec(float(value1) * float(value2)), msg=error_msg)
        elif op == 'divide':
            if float(value2) == 0:
                return render_template('count.html', status=status, value1=value1, op='÷', value2=value2, answer=" value2 can not equal 0", msg=error_msg)
            else:
                return render_template('count.html', status=status, value1=value1, op='÷', value2=value2, answer=float_2_dec(float(value1) / float(value2)), msg=error_msg)
    else:
       return render_template('count.html', msg=error_msg)

@app.errorhandler(404)
def page_no_found(e):
    return jsonify(Error='Page No Found', status=404)

if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0', port=8080)
    # setting host='0.0.0.0' and port=8080 running on cloud9

