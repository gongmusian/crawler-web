from flask import Flask, request, jsonify, abort, render_template

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

# begig-mobo-crawler
from datetime import date
import csv
import codecs
import requests, datetime
from bs4 import BeautifulSoup
import xlsxwriter


def mobo_crawler():
    # from datetime import date
    # print(date.today())
    # print('感謝使用Robert 爬蟲軟體')
    # ouput_file_name = input("請填寫輸出檔名(優先英文數字命名)：")
    ouput_file_name = str(date.today())
    # import csv
    # import codecs
    def readcsv(filename):
        with open(filename, 'r', encoding='CP950') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            Item_Categorys = []
            Category_1s = []
            Category_2s = []
            Category_3s = []
            urls = []
            for row in reader:
                Item_Category = row[0]
                Category_1 = row[1]
                Category_2 = row[2]
                Category_3 = row[3]
                url = row[4]
                Item_Categorys.append(Item_Category)
                Category_1s.append(Category_1)
                Category_2s.append(Category_2)
                Category_3s.append(Category_3)
                urls.append(url)        
        return Item_Categorys, Category_1s, Category_2s, Category_3s, urls
    
    # import requests, datetime
    # from bs4 import BeautifulSoup
    # import xlsxwriter
    Item_Categorys, Category_1s, Category_2s, Category_3s, urls =readcsv('Input.csv')
    
    soup_was = []
    def GetASoup(url):
        x = 1
        # print('抓取中; 共有 ', end='')
        # print(len(url)-1, end='')
        # print(' 項')
        # print('目前執行至')
        while x < len(url):
            soup_was.append(BeautifulSoup(requests.get(url[x]).content, 'html.parser'))
            x += 1
            print('第  ',end='')
            print(x-1, end='')
            print(' 項')
        print('抓取完成!')
        print('***********')

    def exportxlxs(file_name, soup_was, Item_Categorys, Category_1s, Category_2s, Category_3s):
        # today = date.today()
        i = 0
        row = 1
        col = 0
        workbook = xlsxwriter.Workbook(file_name+'.xlsx')
        # workbook = xlsxwriter.Workbook(str(datetime.datetime.now())+ '.xlxs')
        worksheet = workbook.add_worksheet()
        worksheet.write(0, 0,'日期')
        worksheet.write(0, 1,'商品類別')
        worksheet.write(0, 2,'第一層')
        worksheet.write(0, 3,'第二層')
        worksheet.write(0, 4,'第三層')
        worksheet.write(0, 5,'商品名稱')
        worksheet.write(0, 6,'商品連結')
        worksheet.write(0, 7,'狀態')
        # print('')
        # print('')
        # print('輸出中')
    # output xlxs
        while i < len(soup_was):
                for item_name in soup_was[i].select(".PDItem"):
                    worksheet.write(row, col, '3')                
                    worksheet.write(row, col+1, Item_Categorys[i+1])
                    worksheet.write(row, col+2, Category_1s[i+1])
                    worksheet.write(row, col+3, Category_2s[i+1])
                    worksheet.write(row, col+4, Category_3s[i+1])
                    worksheet.write(row, col+5, item_name.select('.pdname a')[0].text)
                    worksheet.write(row, col+6, "https://www.mo-bo.com.tw/"+item_name.select('.pdname a')[0].get('href'))
                    if item_name.select('.pdSoldout'):
                        worksheet.write(row, col+7, item_name.select('.pdSoldout')[0].text)
                    row +=1
                # print(i, end='')
                i += 1
        # print(i)
        workbook.close()
        print("輸出檔名 : "+file_name+".xlsx")
    GetASoup(urls)
    exportxlxs(ouput_file_name, soup_was, Item_Categorys, Category_1s, Category_2s, Category_3s)
    return "HI ENDING"
# input("完成任務   請按下 Enter 關閉程式  2016-03-30 Robert Gong \'_>\'")

# end-mobo-crawler
app = Flask(__name__)

# mobo-crawler-router
@app.route('/mobo')
def mobo():
    print("hello1")
    mobo_crawler()

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

