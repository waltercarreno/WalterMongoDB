import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from flask_paginate import Pagination
from objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegisterForm, LoginForm, RecipeForm, EditRecipeForm, DeleteForm
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


def get_recipes(offset=0, per_page=5):
    return mongo.db.recipes.find()[offset: offset + per_page]


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route('/allrecipes')
def allrecipes():
    page = int(request.args.get('page', 1))
    per_page = 2
    offset = (page - 1) * per_page
    paginated_recipes = get_recipes(offset=offset, per_page=per_page)
    total=paginated_recipes.count()
    pagination = Pagination(page=page, per_page=per_page, total=total)
    return render_template( "allrecipes.html", recipes=paginated_recipes,
                            page=page,
                            per_page=per_page,
                            pagination=pagination)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        found_username = mongo.db.users.find_one({'username': request.form['username']})

        if found_username:
            existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username")})
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                session["username"] = request.form.get("username")
                session['logged-in'] = True
                flash(f'Login successfully.', 'primary')
                return redirect(url_for("profile", username=session["username"]))

            else:
                flash( f'Password incorrect. Please try again.', 'danger')
                return redirect(url_for('login'))

        else:
            flash(f'Username not found. Please try again.', 'danger')
        return redirect(url_for('login'))


    return render_template('login.html',form=login_form)


@app.route("/register", methods=["GET", "POST"])
def register():
    register_form = RegisterForm()

    if register_form.validate_on_submit():
        found_username = mongo.db.users.find_one({'username': request.form['username']})

        if not found_username:
            hashed_pw = generate_password_hash(request.form.get("password"))
            mongo.db.users.insert_one({'username': register_form.username.data,
                              'password': hashed_pw})
            session["username"] = request.form.get("username")
            return render_template('profile.html',username=session["username"])
    
        else:
            flash(f'Duplicate username detected. Please try again', 'danger')
            return redirect(url_for('register'))

    return render_template('register.html',form=register_form)


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    username = mongo.db.users.find_one(
        {"username": session["username"]})["username"]
    recipes = mongo.db.recipes.find()
    return render_template("profile.html", username=username, recipes=recipes)


@app.route("/logout")
def logout():
    flash("You have been logged out")
    session.clear()
    return redirect(url_for("home"))


@app.route('/addrecipe', methods=['GET', 'POST'])
def addrecipe():
    recipe_form = RecipeForm()

    if request.method == 'POST':
        mongo.db.recipes.insert_one({
            'username': session['username'],
            'recipe_name': recipe_form.recipe_name.data,
            'description': recipe_form.description.data,
            'ingredients': recipe_form.ingredients.data,
            'cooking_time': recipe_form.cooking_time.data,
            'calories': recipe_form.calories.data,
            'recipe_image': recipe_form.recipe_image.data,
        })
        flash(f'Recipe added.', 'primary')
        return render_template("profile.html")
    return render_template('newtask.html',form=recipe_form)


@app.route('/recipe_view/<recipe_id>')
def recipe_view(recipe_id):
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template('recipe_view.html', recipe=recipe)


@app.route('/edit_recipe/<recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    recipe_edit = EditRecipeForm()

    if request.method == 'POST':
        mongo.db.recipes.update_one({'_id': ObjectId(recipe_id)},
                                {'$set':
                                    {
            'recipe_name': recipe_edit.recipe_name.data,
            'description': recipe_edit.description.data,
            'ingredients': recipe_edit.ingredients.data,
            'cooking_time': recipe_edit.cooking_time.data,
            'calories': recipe_edit.calories.data,
            'recipe_image': recipe_edit.recipe_image.data,
        }})
        
        flash(f'Recipe updated.', 'primary')
        return render_template("profile.html")

    return render_template('edit_recipe.html', form=recipe_edit)


@app.route('/delete_recipe/<recipe_id>', methods=['GET', 'POST'])
def delete_recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    recipe_delete = DeleteForm()
    if request.method == 'POST':
        if session['username'] == request.form.get('username'):
            mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
            flash(f'Recipe removed.', 'danger')
            return render_template("profile.html")
        else:
            flash(f'Error ocurred.', 'danger')
            return render_template("profile.html")

    return render_template('delete_recipe.html', form=recipe_delete, recipe = recipe)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
