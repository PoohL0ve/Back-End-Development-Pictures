from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """ returns the list of picture urls """
    picture_urls = []
    for item in data:
        if 'pic_url' in item:
            picture_urls.append(item['pic_url'])
    
    if picture_urls:
        return jsonify(picture_urls), 200
    else:
        return jsonify(message='No pictures found'), 404

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """ returns the picture url that matches the id """
    value = id
    for item in data : 
        if item['id'] == int(value) :
            return jsonify(item), 200
    
    return jsonify(message='Invalid id'), 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """ Add a new picture to the list """
    picture = request.json
    pic_id = picture.get('id')  

    for item in data:
        if item.get('id') == pic_id:
            return jsonify({'Message': f"picture with id {pic_id} already present"}), 302

    data.append(picture)
    return jsonify({'id': pic_id, 'Message': 'New picture added'}), 201



######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """ Updates the dictionary's data """
    # Extract the picture data from the request body
    updated_pic = request.json

    for item in data:
        if item.get('id') == id:
            item.update(updated_pic)
            return jsonify({'message': 'Picture updated successfully'}), 200

    return jsonify({'message': 'Picture not found'}), 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """ Deletes an item from the list """
    for index, item in enumerate(data):
        if item['id'] == id:
            del data[index]
            return '', 204

    return jsonify({'message': 'Picture not found'}), 404
   
