from flask import Flask, request, jsonify

app = Flask(__name__)

students = {}
next_id = 1


@app.route("/api/students", methods=["GET"])
def get_all():
    return jsonify(list(students.values()))


@app.route("/api/students", methods=["POST"])
def create():
    global next_id
    data = request.get_json()
    students[next_id] = {"id": next_id, **data}
    next_id += 1
    return jsonify(data), 201


@app.route("/api/students/<int:id>")
def get_one(id):
    return jsonify(students.get(id))


@app.route("/api/students/<int:id>", methods=["DELETE"])
def delete(id):
    students.pop(id, None)
    return "", 204
