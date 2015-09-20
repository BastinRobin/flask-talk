from flask import Flask, render_template, url_for, request

app = Flask(__name__)

@app.route("/")
def get_root():
    stock_price = 75.43
    return render_template('index.html', data=stock_price)

@app.route("/data")
def get_data():
    return render_template('other_file.html')

@app.route("/data", methods=["POST"])
def post_data():
    query = request.args.get('q')
    print "Query: %s" % query
    return "Your data has been received!"

if __name__ == "__main__":
    app.run(debug=True)
