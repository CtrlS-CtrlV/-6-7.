from flask import Flask, request, redirect, abort

app = Flask(__name__)

posts = [{"id": 1, "title": "Test"}]


@app.route("/posts/<int:id>/edit", methods=["POST"])
def edit(id):
    post = next((p for p in posts if p["id"] == id), None)
    if not post:
        abort(404)
    post["title"] = request.form["title"]
    return redirect("/posts")


@app.route("/posts/<int:id>/delete", methods=["POST"])
def delete(id):
    global posts
    posts = [p for p in posts if p["id"] != id]
    return redirect("/posts")
