from flask import Flask, request, redirect, url_for

app = Flask(__name__)

posts = []
next_id = 1


@app.route("/posts")
def list_posts():
    return str(posts)


@app.route("/posts/create", methods=["POST"])
def create():
    global next_id
    posts.append({"id": next_id, "title": request.form["title"]})
    next_id += 1
    return redirect(url_for("list_posts"))
