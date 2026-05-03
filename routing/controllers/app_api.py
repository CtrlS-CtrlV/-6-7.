from flask import Flask, request, jsonify, abort

app = Flask(__name__)

items_db = {}
next_id = 1


@app.route("/api/items", methods=["GET"])
def get_items():
    category = request.args.get("category")
    items = list(items_db.values())

    if category:
        items = [i for i in items if i["category"] == category]

    return jsonify(items)


@app.route("/api/items", methods=["POST"])
def create_item():
    global next_id
    data = request.get_json()

    if not data or "name" not in data:
        return jsonify({"error": "Invalid"}), 400

    item = {"id": next_id, **data}
    items_db[next_id] = item
    next_id += 1

    return jsonify(item), 201


@app.route("/api/items/<int:item_id>")
def get_item(item_id):
    item = items_db.get(item_id)
    if not item:
        abort(404)
    return jsonify(item)


@app.route("/api/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    data = request.get_json()
    if item_id not in items_db:
        abort(404)
    items_db[item_id].update(data)
    return jsonify(items_db[item_id])


@app.route("/api/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    if item_id not in items_db:
        abort(404)
    del items_db[item_id]
    return "", 204


if __name__ == "__main__":
    app.run(port=5001, debug=True)
