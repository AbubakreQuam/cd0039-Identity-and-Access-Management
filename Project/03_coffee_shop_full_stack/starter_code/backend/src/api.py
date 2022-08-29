import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth


def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)
    setup_db(app)
   
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE,')
        return response
    
    '''
    To generate new token
    https://kepman.us.auth0.com/authorize?audience=image&response_type=token&client_id=lmtL0J1riBz7ZWQ0tpzvZAvQCfxM8A7L&redirect_uri=http://localhost:8100

    Barista (email:sakanurudeen200@gmail.com, password:Saka@123 )

    Manager (email:sakanurudeen2000@gmail.com, password:Saka@123 )
    
    '''

    @app.route('/')
    def home():
        return 'I Want to drink a Coffe Please!!!'
    

    @app.route('/drinks', methods=['GET'])
    def short_drinks():
        try:
            drinks = Drink.query.all()
            return jsonify  (
                {
                    "success": True, 
                    "Status code": 200,
                    "drinks": json.loads(str(drinks))
                }
                            ) 
        except Exception:
            abort(422)


    @app.route('/drinks-detail', methods=['GET'])
    @requires_auth('get:drinks-detail')
    def long_drinks_detail(payload):
        try:
            drinks = Drink.query.all()
            return jsonify  (
                {
                    "success": True, 
                    "Status code": 200,
                    "drinks": json.loads(str(drinks))
                }
                            ) 
        except Exception:
            abort(422)


    @app.route('/drinks', methods=['POST'])
    @requires_auth('post:drinks')
    def create_long_drinks(payload):
        body = request.get_json()
        title_data = body.get("title", None)
        recipe_data = body.get("recipe", None)
        print(recipe_data)
        print(title_data)
        print(body)
        #Checking if data is not null

        if title_data is None:
            abort(400)
        
        if recipe_data is None:
            abort(400)

        check_title_exit = Drink.query.filter(title_data==Drink.title).one_or_none()
        
        if check_title_exit is not None:
            abort(409)
        try:
            new_drink = Drink(title=title_data, recipe=str(recipe_data))
            new_drink.insert()

            drinks = Drink.query.all()
            return jsonify  (
                {
                    "success": True, 
                    "status code": 200,
                    "drinks": json.loads(str(new_drink))
                }
                            )
        except Exception:
            print(recipe_data)
            print(title_data)
            print(body)
            abort(422)

    

    @app.route('/drinks/<int:id>', methods=['PATCH'])
    @requires_auth('patch:drinks')
    def update_long_drinks_detail(payload, id):
        body = request.get_json()

        title_new = body.get('title', None)
        recipe_new = body.get('recipe', None)

        drink_to_update= Drink.query.filter(Drink.id==id).one_or_none()

        if drink_to_update is None:
            abort(404)

        try:
            
            drink_to_update.title = title_new
            drink_to_update.update()

            drinks = Drink.query.filter(Drink.id==id).one_or_none()
            return jsonify(
                {
                    "success": True,
                    "status code": 200,
                    "drinks":json.loads(str(drinks))

                }
            )
        except Exception:
            abort(422)
       

    

    @app.route('/drinks/<int:id>', methods=['DELETE'])
    @requires_auth('delete:drinks')
    def delete_drinks_detail(payload, id):
        drink_to_delete= Drink.query.filter(Drink.id==id).one_or_none() 

        if drink_to_delete is None:
            abort(404)
        try:
            drink_to_delete.delete()

            return jsonify(
                {
                    "success": True,
                    "status code": 200,
                    "delete": id

                }
            )
        except Exception:
            abort(422)
       

    # Error Handling
    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "Forbidden message "
        }), 403

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Unauthorized Access"
        }), 401

    @app.errorhandler(404)
    def Not_found(error):
        return jsonify({
        "success": False, 
        "error": 404,
        "message": "Resource Not Found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
        "success": False, 
        "error": 400,
        "message": "Bad Request"
        }), 400

    @app.errorhandler(409)
    def conflict(error):
        return jsonify({
        "success": False, 
        "error": 409,
        "message": "Resource Already Exist"
        }), 409

    @app.errorhandler(405)
    def wrong_method(error):
        return jsonify({
        "success": False, 
        "error": 405,
        "message": "Method Not Allowed"
        }), 405

    return app
    
    '''
    @TODO implement error handler for AuthError
        error handler should conform to general task above
    '''
