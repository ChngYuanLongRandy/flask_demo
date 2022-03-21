# jsonify takes care of converting stuff into JSON as well
# as changing the content type of our HTTP response to application/JSON

# request will take care of incoming requests
from crypt import methods
from flask import Flask, jsonify, request

# HTTPstatus informs us of the different HTTPstatuses like httpstatus.created(201)
from http import HTTPStatus

# by convention
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World"

# the methods in the decorater defines what it is, by default it will be a GET method
@app.route("/recipes",methods=['GET'])
def get_recipes():
    return jsonify({'data':recipes}) 

@app.route("/recipes/<int:recipe_id>",methods=['GET'])
def get_recipe(recipe_id):
    recipe = next((recipe for recipe in recipes if recipes['id']==recipe_id), None)
    if recipe:
        return jsonify(recipe)
    return jsonify({'message':'recipe not found'}), HTTPStatus.NOT_FOUND 

# despite the same "route", this is a POST method and not a GET method
@app.route('/recipes', methods= ['POST'])
def create_recipe():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    recipe = {
        'id': len(recipes) + 1,
        'name' : name,
        'description': description
    }

    recipes.append(recipe)
    return jsonify(recipe), HTTPStatus.CREATED

@app.route('/recipes/<int:recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    recipe = next((recipe for recipe in recipes if recipes['id']== recipe_id), None)
    if not recipe:
        return jsonify({'message':'Recipe not found'}), HTTPStatus.NOT_FOUND
    data = request.get_json()
    recipe.update({
        'name' : data.get('name'),
        'description' : data.get('description')
    })
    return jsonify(recipe), HTTPStatus.OK

@app.route('/recipes/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    recipe = next((recipe for recipe in recipes if recipes['id']== recipe_id), None)
    if not recipe:
        return jsonify({'message':'Recipe not found'}), HTTPStatus.NOT_FOUND
    recipes.remove(recipe)

    return '', HTTPStatus.NO_CONTENT

if __name__ == "__main__":
    app.run()


recipes = [{
    'id':1,
    'name': 'Egg Salad',
    'description': 'This is a lovely egg salad recipe'
},
{
    'id':2,
    'name': 'Tomato Pasta',
    'description': 'This is a lovely Tomato Pasta Receipe'
}]