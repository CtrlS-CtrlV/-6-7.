from flask import Flask, request, session, make_response, jsonify, redirect

app = Flask(__name__)
app.secret_key = "secret"


@app.route("/set-theme/<theme>")
def set_theme(theme):
    resp = make_response("Theme set")
    resp.set_cookie("theme", theme, max_age=60*60*24*30)
    return resp


@app.route("/get-theme")
def get_theme():
    return request.cookies.get("theme", "light")


@app.route("/cart/add/<int:id>")
def add_cart(id):
    cart = session.get("cart", [])
    cart.append(id)
    session["cart"] = cart
    return jsonify(cart)


@app.route("/cart")
def cart():
    return jsonify(session.get("cart", []))


@app.route("/login", methods=["POST"])
def login():
    session["user"] = request.form.get("username")
    return redirect("/profile")


@app.route("/profile")
def profile():
    if "user" not in session:
        return redirect("/login")
    return f"Hello {session['user']}"


if __name__ == "__main__":
    app.run(port=5002, debug=True)
