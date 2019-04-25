from flask import Flask, render_template, request, redirect, session
from mysqlconnection import connectToMySQL

app = Flask(__name__)
app.secret_key = "SECRETKEY"

# --- USE GLOBAL VARIABLES FOR DATABASE NAMES AND WHATNOT --- #
# database_1 = "marco_db_name"
# database_2 = "polo_db_name"

# /users/new- GET - method should return a template containing the form for adding a new user

@app.route("/users/new", methods=["GET"])
def add_user():
    print(request.form)
    return render_template("create_new.html")

# /users/create - POST - method should add the user to the database, then redirect to /users/<id>

@app.route("/users/create", methods=["POST"])
def add_user_to_db():
    print(request.form)
    mysql = connectToMySQL("users_db")

    insert_query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, NOW(), NOW());"

    data = {
            "first_name": request.form["f_name"],
            "last_name": request.form["l_name"], 
            "email": request.form["e_mail"], 
            }

    new_user_id = mysql.query_db(insert_query, data)
    return redirect("/users/" + str(new_user_id))


#  /users/<id> - GET - method should return a template that displays the specific user's information

@app.route("/users/<id>", methods = ["GET"])
def display_user_by_id(id):
    print(request.form)

    mysql = connectToMySQL("users_db")

    select_by_id = f"SELECT * from users where user_id = {id};"
    print(select_by_id)

    displayed_user = mysql.query_db(select_by_id)
    print(displayed_user)

    return render_template("user_by_id.html", displayed_user = displayed_user)


#  /users - GET - method should return a template that displays all the users in the table

@app.route("/users", methods = ["GET"])
# could have left it just "/users" without GET Method: coz it is the default. POST must be explicitly mentioned
def display_all_users():
    # call the function, passing in the name of our db
    mysql = connectToMySQL('users_db')

    # call the query_db function, pass in the query as a string
    users = mysql.query_db('SELECT * FROM users;')

    print(users)
    return render_template("index.html", all_users = users)


#  /users/<id>/edit - GET - method should return a template that displays a form for editing the user with the id specified in the url

@app.route("/users/<id>/edit") # -- , methods=["GET"] commented out as it is the default
def edit_user(id):
    print(request.form)

    mysql = connectToMySQL('users_db')

    select_by_id = f"SELECT * from users where user_id = {id};"

    displayed_user = mysql.query_db(select_by_id)

    # displayed_user = mysql.query_db(select_by_id)[0] <--- use index 0 here once and dont type it many times in jinja
    # print(displayed_user)

    return render_template("update.html", displayed_user = displayed_user)



#  /users/<id>/update - POST - method should update the specific user in the database, then redirect to /users/<id>

@app.route("/users/<id>/update", methods=["POST"])
def update_user_in_db(id):
    print("Hola")
    mysql = connectToMySQL("users_db")

    update_query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, updated_at = NOW() WHERE user_id = %(user_id)s;"
    # print(update_query)
    print("Hola" + id)
    
    data = {
            "first_name": request.form["f_name"],
            "last_name": request.form["l_name"], 
            "email": request.form["e_mail"],
            "user_id": int(id)
            }

    mysql.query_db(update_query, data)

    return redirect("/users/" + str(id))



#  /users/<id>/destroy - GET - method should delete the user with the specified id from the database, then redirect to /users

@app.route("/users/<id>/destroy", methods = ["GET"])
def delete_user_by_id(id):
    print(request.form)

    mysql = connectToMySQL("users_db")

    delete_by_id = f"DELETE from users where user_id = {id};"

    mysql.query_db(delete_by_id)

    return redirect("/users")



if __name__ == "__main__":
    app.run(debug=True)

#  /users/<id>/edit - GET - method should return a template that displays a form for editing the user with the id specified in the url
#  /users/<id>/update - POST - method should update the specific user in the database, then redirect to /users/<id>
#  NINJA BONUS: Add a description (textarea) field to the user table and update the templates appropriately
#  NINJA BONUS: Ensure all the fields on the edit form are pre-populated (not just with placeholders)
# 
