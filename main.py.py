from flask import Flask

milk_amount = 10
juice_amount = 10
water_amount =10

app = Flask(__name__)

template = """
<!DOCTYPE html>
<html lang="">
  <head>
    <meta charset="utf-8">
    <title>Products</title>
  </head>
  <body>
  <h1>Avlible products</h1>
  <ul>
    <li><a href="http://127.0.0.1:5000/milk">Milk</a></li>
    <li><a href="http://127.0.0.1:5000/juice">Juice</a></li>
    <li><a href="http://127.0.0.1:5000/water">Water</a></li>
  </ul>
  </body>
</html>
"""

@app.route('/')
def index():
    return template

@app.route('/milk')
def milk_products():
    return f"We have {milk_amount} litres of milk <br> <a href=http://127.0.0.1:5000/order_result>Order now 1 liter</a>"

@app.route('/juice')
def juice_products():
    return f"We have {juice_amount} litres of juice <br> <a href=http://127.0.0.1:5000/order_result>Order now 1 liter</a>"

@app.route('/water')
def water_products():
    return f"We have {water_amount} litres of water <br> <a href=http://127.0.0.1:5000/order_result>Order now 1 liter</a>"

@app.route('/order_result')
def order_result():
    return "<h1>Order success</h1>"

@app.route('/<name>')
def print_name(name):
    return f"<h1>Hello {name} </h1>"

app.run(debug=True)