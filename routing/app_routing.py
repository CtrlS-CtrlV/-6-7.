from flask import Flask, request, redirect, url_for, render_template_string, abort

app = Flask(__name__)

posts_db = [
    {"id": 1, "title": "Python", "content": "Intro", "author": "Ivan"},
    {"id": 2, "title": "Flask", "content": "Microframework", "author": "Maria"},
]
next_id = 3


def render(title, content):
    return render_template_string(f"""
    <h1>{title}</h1>
    <a href="/">Home</a> | <a href="/posts">Posts</a>
    <hr>{content}
    """)


@app.route("/")
def index():
    return render("Home", "Welcome!")


@app.route("/posts")
def post_list():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 2))

    start = (page - 1) * per_page
    items = posts_db[start:start + per_page]

    content = "".join([f"<p><a href='/posts/{p['id']}'>{p['title']}</a></p>" for p in items])
    return render("Posts", content)


@app.route("/posts/<int:post_id>")
def post_detail(post_id):
    post = next((p for p in posts_db if p["id"] == post_id), None)
    if not post:
        abort(404)
    return render(post["title"], post["content"])


@app.route("/posts/create", methods=["GET", "POST"])
def post_create():
    global next_id

    if request.method == "POST":
        title = request.form.get("title")
        posts_db.append({"id": next_id, "title": title, "content": "", "author": "anon"})
        next_id += 1
        return redirect(url_for("post_list"))

    return render("Create", """
    <form method='post'>
        <input name='title'>
        <button>Create</button>
    </form>
    """)


@app.route("/search")
def search():
    q = request.args.get("q", "")
    results = [p for p in posts_db if q.lower() in p["title"].lower()]
    return render("Search", str(results))


@app.route("/archive/<int:year>/<int:month>")
def archive(year, month):
    return render("Archive", f"{month}/{year}")


@app.route("/user/<username>")
def user_profile(username):
    return render("User", f"Profile: {username}")


if __name__ == "__main__":
    app.run(port=5000, debug=True)
