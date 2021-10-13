from flask import Flask, jsonify, make_response, request
from flask.templating import render_template
app = Flask(__name__)

# Fake DB
stock = {
    "fruits": {
        "banana": 600,
        "apple": 400,
        "pineapple": 1000,
        "cherry": 1000
    },
    "vegetables": {
        "tomatoes": 500,
        "lettuce": 300,
        "pepper": 400,
        "onion": 650
    }
}

# This route returns a static page in the "templates" folder
# Here you can return Python data in HTML page or just a template.
# Unnecessary, right?
@app.route("/")
def main():
    return render_template("index.html")


# GET all data from stock
@app.route("/stock")
def return_stock():
    res = make_response(jsonify(stock), 200)
    return res


# GET an specific section
@app.route("/stock/<section>")
def return_selection(section):
    if section in stock:
        res = make_response(jsonify(stock[section]))
        return res
    
    res = make_response(jsonify({ "message": "Section not found" }), 404)
    return res


# GET value from section stock
@app.route("/stock/<section>/<product>")
def get_product_stock(section, product):
    if section in stock:
        quantity = stock[section].get(product)
        if quantity:
            res = make_response(jsonify({ "product": product, "quantity": quantity }), 200)
            return res
        res = make_response(jsonify({ "message": "Product not found" }), 404)
        return res
    
    res = make_response(jsonify({ "message": "Product not found" }), 404)
    return res


# POST for insert a new section 
@app.route("/stock/<section>", methods=["POST"])
def create_section(section):
    req = request.get_json()
    if section in stock:
        res = make_response(jsonify({ "message": "Section already exists" }), 400)
        return res
    stock.update({ section: req })
    res = make_response(jsonify({ "message": "Section created!"}), 201)
    return res


# PUT to create or replace something
@app.route("/stock/<section>", methods=["PUT"])
def put_section(section):
    req = request.get_json()
    if section in stock:
        stock[section] = req
        res = make_response(jsonify({ "message": "Section replaced!"}), 200)
        return res

    stock[section] = req
    res = make_response(jsonify({ "message": "Section created!"}), 201)
    return res


# PATCH to create or update an item in stock
@app.route("/stock/<section>", methods=["PATCH"])
def update_item(section):
    req = request.get_json()
    if section in stock:
        for key, value in req.items():
            stock[section][key] = value
        res = make_response(jsonify({"message": "Products stock updated"}), 200)
        return res
    
    stock[section] = req
    res = make_response(jsonify({"message": "Section created"}), 201)
    return res


# DELETE an entire section
@app.route("/stock/<section>", methods=["DELETE"])
def delete_section(section):
    if section in stock:
        del stock[section]
        res = make_response(jsonify({"message": "Section delected"}), 204)
        return res

    res = make_response(jsonify({ "message": "Section not found" }), 404)
    return res


# DELETE a product from section
@app.route("/stock/<section>/<product>", methods=["DELETE"])
def delete_product(section, product):
    if section in stock:
        if product in stock[section]:
            del stock[section][product]
            res = make_response(jsonify({ "message": "Product deleted"}), 204)
            return res

        res = make_response(jsonify({ "message": "Product not found"}), 404)
        return res
    
    res = make_response(jsonify({ "message": "Section not found"}), 404)
    return res


# Deploy server
if __name__ == "__main__":
    app.run(debug=True, port=7700)