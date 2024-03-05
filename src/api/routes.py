"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""

from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, Users
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

api = Blueprint('api', __name__)


# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
# The create_access_token() function is used to actually generate the JWT.
@api.route("/login", methods=["POST"])
def login():
    response_body = {}
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    # Reemplazar por lógica consultando la DB.
    # Debo buscar en la base de datos un usuario cuyo email y password sea igual de lo que reciba en el body, ademas debe tener is_active = true 
    
    if email != "test@test" or password != "test":
        response_body['message'] = "Bad username or password"
        return response_body, 401      

    access_token = create_access_token(identity=user)  # Lo que el back quiere agregar en el token
    response_body['access_token'] = access_token
    response_body['message'] = "Usuario logeado con éxito"
    response_body['results'] = {"user": user, "profile": profile}
    return response_body, 200

# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@api.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@api.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    response_body = {}
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    if current_user[0]["name"]=="Ary":
        response_body["message"]="Perfil de Ary,"
        return response_body,200
    response_body["message"]="Perfil de Ary,sin acceso"
    return response_body, 401

@api.route('/users/<int:id>', methods=['GET'])
def handle_user_id(id):
    response_body = {} 
    # Buscar usuario por ID
    user = db.session.get(Users,id)
    response_body["results"] = user.serialize()
    response_body["message"] = "Usuario encontrado con éxito."
    return response_body, 200  # Código de estado para "Éxito"


