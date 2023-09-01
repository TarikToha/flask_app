import json
from flask import Flask, request, jsonify
import mongoengine as db

prod = True

app = Flask(__name__)

if prod:
    db.connect(host="mongxodb+srv://ttoha12:unccs123@cluster0.hfkl9bk.mongodb.net/flaskapp")
else:
    db.connect("flaskapp")


class ImageLabels(db.Document):
    image_name = db.StringField()
    labels = db.ListField()

    def to_json(self):
        return {"image_name": self.image_name,
                "labels": self.labels}


@app.route('/', methods=['GET'])
def query_records():
    image_labels = ImageLabels.objects
    if not image_labels:
        return jsonify({'error': 'data not found'})
    else:
        return jsonify(image_labels.to_json())


@app.route('/', methods=['PUT'])
def create_record():
    record = json.loads(request.data)
    image_labels = ImageLabels(image_name=record['image_name'], labels=record['labels'])
    image_labels.save()
    return jsonify(image_labels.to_json())


#
# @app.route('/', methods=['POST'])
# def update_record():
#     record = json.loads(request.data)
#     user = User.objects(name=record['name']).first()
#     if not user:
#         return jsonify({'error': 'data not found'})
#     else:
#         user.update(email=record['email'])
#     return jsonify(user.to_json())

#
# @app.route('/', methods=['DELETE'])
# def delete_record():
#     record = json.loads(request.data)
#     user = User.objects(name=record['name']).first()
#     if not user:
#         return jsonify({'error': 'data not found'})
#     else:
#         user.delete()
#     return jsonify(user.to_json())


if not prod:
    if __name__ == "__main__":
        app.run(debug=True)
