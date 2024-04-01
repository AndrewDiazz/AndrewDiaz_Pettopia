from flask import render_template,redirect,request,session,flash
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.pet_model import Pet
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


# Sign in functions routes
@app.route("/sign_in_page")
def sign_in_page():
    return render_template("sign_in.html")

@app.route("/sign_in", methods=["POST"])
def sign_in():
    user = User.val_sign_in(request.form)
    if not user:
        return redirect("/sign_in_page")
    session["user_id"] = user.id
    return redirect(f"/user/account/{session['user_id']}")

# Register Functions routes
@app.route("/register_page")
def register_page():
    return render_template("create_account.html")

@app.route("/registration", methods=["POST"])
def registration():
    if not User.val_account(request.form):
        return redirect("/register_page")
    data={
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": bcrypt.generate_password_hash(request.form["password"])
    }
    user_id = User.save(data)
    session["user_id"] = user_id
    return redirect(f"/user/account/{session['user_id']}")

# Acoount
@app.route('/user/account/<int:id>')
def user_account(id):
    data = {
        "id": id
    }
    pets = Pet.get_one_with_user(data)
    user=User.get_id(data)
    return render_template('account.html', user=user, pets=pets)

# Update Account
@app.route('/user/update',methods=['POST'])
def update():
    is_valid = User.is_valid(request.form)
    if is_valid:
        User.update(request.form)
        return redirect(f'/user/account/{request.form["id"]}')
    return redirect(f'/user/account/{request.form["id"]}')

# Sign Out
@app.route("/sign_out")
def sign_out():
    session.clear()
    return redirect("/sign_in_page")




