from flask import render_template,redirect,request,session,flash
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.pet_model import Pet
from flask_app.models.post_model import Post

# Pettopia Home Page that displays all posts by all users with pets
@app.route("/home/<int:id>")
def home(id):
    if "user_id" not in session:
        return redirect("/sign_in_page")
    data={
        "id": id
    }
    posts = Post.get_all_with_pets()
    return render_template("pettopia_home.html", posts = posts, user=User.get_id(data))

# Pet Profile Page That displays pets info
@app.route("/pet/<int:id>")
def display_one_pet(id):
    if "user_id" not in session:
        return redirect("/sign_in_page")

    data = {
        "id":id
    }
    user_data = {
        "id":session["user_id"]
    }
    pet = Pet.get_pet_id(data)
    user = User.get_id(user_data)

    return render_template("pet_profile.html", pet=pet, user=user)

# Add Pet Page that also contains a form to add another pet
@app.route("/pet/new/<int:id>")
def add_pet_dashboard(id):
    if "user_id" not in session:
        return redirect("/sign_in_page")
    data = {
        "id": id
    }
    user=User.get_id(data)
    return render_template("add_pet.html",user=user)

@app.route("/pet", methods=["POST"])
def create_pet():
    if "user_id" not in session:
        return redirect("/sign_in_page")
    pet = Pet.val_pet(request.form)
    if not pet:
        return redirect(f"/pet/new/{session['user_id']}")

    data = {
        "pet_name":request.form["pet_name"],
        "age":request.form["age"],
        "type":request.form["type"],
        "breed":request.form["breed"],
        "description":request.form["description"],
        "user_id":session["user_id"]
    }
    Pet.save(data)
    return redirect(f"/user/account/{session['user_id']}")

# Update page that allows you to update your pets info as well as delete your pets comments
# These are the functions
@app.route("/pet/update/<int:id>")
def update_pet_dashboard(id):
    if "user_id" not in session:
        return redirect("/sign_in_page")
    data = {
        "id": id
    }
    pet = Pet.get_pet_id(data)
    comment = Post.get_one_with_pet(data)

    return render_template("update_pet.html",pet=pet, comment=comment)

@app.route('/pet/update',methods=['POST'])
def update_pet():
    is_valid = Pet.val_pet(request.form)
    if is_valid:
        Pet.pet_update(request.form)
        return redirect(f'/pet/update/{request.form["id"]}')
    return redirect(f'/pet/update/{request.form["id"]}')


@app.route('/pet/<int:id>/delete')
def delete_pet(id):
    if "user_id" not in session:
        return redirect("/sign_in_page")
    data = {
        'id': id
    }
    Pet.delete(data)
    return redirect(f"/user/account/{session['user_id']}")