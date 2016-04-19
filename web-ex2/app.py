from flask import Flask, request, jsonify, abort, render_template, make_response

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    return "hello"

@app.route('/welcome')
def wlecome():
    return render_template('welcome.html', name="hi")

@app.errorhandler(404)
def page_no_found(e):
    return jsonify(Error='Page No Found', status=404)

if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0', port=8080)
    # setting host='0.0.0.0' and port=8080 running on cloud9

