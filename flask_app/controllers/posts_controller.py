from flask import render_template,redirect,request,session,flash
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.pet_model import Pet
from flask_app.models.post_model import Post

# Post page that allows you to veiw all your specific pet posts
@app.route("/all/<int:id>/post")
def all_pet_posts(id):
    if "user_id" not in session:
        return redirect("/sign_in_page")
    data={
        "id": id
    }
    comments = Post.get_one_with_pet(data)
    return render_template("posts.html", comments = comments, pet=Pet.get_pet_id(data))

# This function allows you to add a post on under your specific pet.
@app.route("/pet/post", methods=["POST"])
def pet_post():
    if "user_id" not in session:
        return redirect("/sign_in_page")

    post = Post.val_comment(request.form)
    if not post:
        return redirect(f"/pet/{request.form['pet_id']}")

    data = {
        "comment":request.form["comment"],
        "pet_id":request.form["pet_id"]
    }
    Post.save(data)
    return redirect(f"/pet/{request.form['pet_id']}")

# This will delete your pets post
@app.route('/post/<int:id>/delete/<int:pet_id>')
def delete_post(id,pet_id):
    if "user_id" not in session:
        return redirect("/sign_in_page")
    data = {
        'id': id
    }
    pet = pet_id
    Post.delete(data)
    return redirect(f'/pet/update/{pet}')