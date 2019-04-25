from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
import re
import datetime

# we are creating an object called bcrypt, # which is made by invoking the function Bcrypt with our app as an argument

app = Flask(__name__)
app.secret_key = "Guess_5#y2L_What I am? SECRET KEY!!!"
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template("index.html")

# VALIDATE AND REGISTER A NEW USER
@app.route('/registration', methods=['POST'])
def validate_registration():
    # create a regular expression object that we'll use later
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    PASSWORD_REGEX = re.compile(r'[A-Za-z0-9@#$%^&+=]{8,}$')

    # include some logic to validate user input before adding them to the database!
    
    is_valid = True


    # see if the username provided exists in the database
    
    mysql = connectToMySQL("private_wall_db")
    query = "SELECT * FROM private_wall_db.registered_users WHERE email = %(email)s;"
    
    data = { "email" : request.form["email"] }
    result = mysql.query_db(query, data)

    print(result)
    if len(result) > 0:
        is_valid = False
        flash("A user with this email (username) already exits.", "error")
        #     # assuming we only have one user with this username, the user would be first in the list we get back
        #     # of course, we should have some logic to prevent duplicates of usernames when we create users


    if len(request.form["first-name"]) < 2:
        is_valid = False
         #first_name_
        flash("Name must be at least 2 characters long", "first_name_error")

    if len(request.form["last-name"]) < 1:
        is_valid = False
         #last_name_
        flash("Last name can not be left blank", "last_name_error")

    if not EMAIL_REGEX.match(request.form['email']):
        is_valid = False
        flash("Email is NOT valid!", "email_error")

    if (request.form['password-confirm'] != request.form['entered-password']):
        is_valid = False
         #paswword_mismatch_
        flash("Passwords DO NOT Match!", "mismatch_error")

    if not PASSWORD_REGEX.match(request.form['entered-password']):
        is_valid = False
         #password_
        flash("Password is NOT valid!", "passkey_error")

    if len(request.form["about"]) > 120:
        is_valid = False
          #wordy_
        flash("Comments must not exceed 120 characters, Twitterfingers!", "wordy_error")
    
    BDAY_STR = request.form["birthday"] # is a string
    
    birthday_arr = BDAY_STR.split("-") # parse this into a list
    print(birthday_arr) # prints birhday as list ['2019', '04', '17']

    # now we concat everything Back together - Quyen is a Genius!!!
    BDAY_INT = datetime.datetime(int(birthday_arr[0]), int(birthday_arr[1]), int(birthday_arr[2]))
    print(BDAY_STR) # prints 2019-04-17

    print(type(BDAY_INT)) # correctly prints <class 'datetime.datetime'>

    # print(datetime.datetime(year=2000, month=1,day=1)) --- is wrong coz datetime extracts date from a given int value but can not understand or parse strings --- Obv. there must be a shorter way of doing this but for now, the condition below works

    if (datetime.datetime(year=2000, month=1,day=1) < BDAY_INT <= datetime.datetime.now() or BDAY_STR == ''):
        print("******** DATE *******")
        print(datetime.date(year=2000, month=1,day=1))

        is_valid = False
        flash("You must be a real human already born AND at least 18 my friend ;)", "too_young_error")


        # If year of provided date isn't over 2000 [i.e if user is not 18 yet]
        #  <= datetime.datetime.now()


    # if len(request.form["gender"]) == None:
    #     is_valid = False
    #     flash("Please select a gender or don't disclose")
        # print(request.form["form-gender"])

    # if request.form["interests"] == None:
    #     # print(" @@@@@@@@@ ", request.form["rating"])
    #     is_valid = False
    #     flash("Please indicate at least one Inerest")

    if not is_valid:
        session["reg_message"] = True
        return redirect("/")
    
    else:
        
        print("******** DATE of ELSE BLOCK *******")
        print(datetime.date(year=2000, month=1,day=1))
        print(request.form["birthday"])
        print("******** END ELSE BLOCK *******")


        # Then create the hash
        password_hash = bcrypt.generate_password_hash(request.form['entered-password'])
        print(password_hash)  
        # prints something like b'$2b$12$sqjyok5RQccl9S6eFLhEPuaRaJCcH3Esl2RWLm/cimMIEnhnLb7iC'
        # be sure you set up your database so it can store password hashes this long (60 characters)

        mysql = connectToMySQL("private_wall_db")
        
        insert_query = "INSERT INTO registered_users (first_name, last_name, email, password_hash, gender, birthday, interests, about, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password_hash)s, %(gender)s, %(birthday)s, %(interests)s, %(about)s, NOW(), NOW());"

        data = {
                "first_name": request.form["first-name"],
                "last_name": request.form["last-name"], 
                "email": request.form["email"],
                "password_hash": password_hash,
                "gender": request.form["gender"],
                "birthday": request.form["birthday"],
                "interests": request.form["interests"],
                "about": request.form["about"] 
                }

        new_user_id = mysql.query_db(insert_query, data)
        session["new_user"] = request.form["first-name"]
        new_user = session["new_user"]

        flash("Registration Successful. Please Log In", "success")
        session["reg_message"] = True
        
        return redirect("/")

        # never render on a post, always redirect!
        # return redirect("/")

# LOGIN USER AFTER SUCCESSFUL VALIDATION
@app.route('/login', methods=['POST'])
def login():

    login_valid = True

    if len(request.form["username"]) < 1:
        login_valid = False
        flash("Username must be provided", "login_error")   #username_
        return redirect('/')

    if len(request.form["password"]) < 1:
        login_valid = False
        flash("Password field can not be left blank. \n Use any of Upper and Lower case letters, Numbers and Special Characters", "login_error")    #password_blank
        return redirect('/')

    
    # see if the username provided exists in the database
    
    mysql = connectToMySQL("private_wall_db")
    query = "SELECT * FROM registered_users WHERE email = %(username)s;"
    
    data = { "username" : request.form["username"] }
    result = mysql.query_db(query, data)

    print(result)


    # if we didn't find anything in the database by searching by username or if the passwords don't match,
    # flash an error message and redirect back to a safe route
    # flash("You could not be logged in")
    # return redirect("/")

    if len(result) == 0:
        login_valid = False
        flash("User Doesn't exit", "login_error")

    if not bcrypt.check_password_hash(result[0]['password_hash'], request.form['password']):
        flash("Wrong Password. Try Again", "bad_password_error")   #wrong_password
        login_valid = False
        return redirect('/')


    if not login_valid:
        flash("You could not be logged in", "login_error")
        return redirect("/")
    
    #     # assuming we only have one user with this username, the user would be first in the list we get back
    #     # of course, we should have some logic to prevent duplicates of usernames when we create users


    # use bcrypt's check_password_hash method, passing the hash from our database and the password from the form

    elif bcrypt.check_password_hash(result[0]['password_hash'], request.form['password']):
        # if we get True after checking the password, we may put the user and their id in session
    
        session['logged_in_user'] = result[0]['first_name']
        session['logged_in_user_id'] = result[0]['id']
        print(result)

        # never render on a post, always redirect!
        return redirect('/success')


# SUCCESS ROUTE LOGS USER IN and DISPLAYS ALL SENT AND RECEIVED MESSAGES 
@app.route('/success')
def success():

    logged_in_user_id = session['logged_in_user_id']
    logged_in_user = session['logged_in_user']

    
    mysql = connectToMySQL("private_wall_db")

    # # -- join command to get messages by sender and recipient -- WOW
    # super_query = " SELECT * from messages JOIN registered_users ON registered_users.id = messages.recipient_id JOIN registered_users AS users ON users.id = messages.recipient_id; "


    # -- single join command to get all INBOX messages of curent user -- SWEET

    # -- Note the DateTime Ussage

    # Old Select without Date Time Lapse
    msgs_to_current_usr = f" SELECT * from messages JOIN registered_users ON registered_users.id = messages.sender_id where recipient_id = {logged_in_user_id}; "

    ############# DATEDIFF TIMELAPSE ##############

    # mysql = connectToMySQL("private_wall_db")

    # -- 30 days ago


    # timelapse = SELECT DATEADD(DAY, DATEDIFF(DAY, 0, GETDATE()), -30) from messages;


    ###############################################

    # select messages.id, sender.first_name, content, TIME_FORMAT(TIMEDIFF(now(),messages.created_at), %(datetime)s) as timediff
    
    
    # msgs_to_current_usr = " SELECT messages.id, sender.first_name, content, TIME_FORMAT(TIMEDIFF(now(),messages.created_at), %(datetime)s) as timediff from messages JOIN registered_users ON registered_users.id = messages.sender_id where recipient_id = %(logged_in_user_id)s; "

    # messageData = {
    #     'logged_in_user_id':session["logged_in_user_id"],
    #     'datetime':'%%'+'H:'+'%%'+'i'
    #     }


    # count of rows is number of messages
    inbox = mysql.query_db(msgs_to_current_usr)
    inbox_count = len(inbox)
    # inbox = session["inbox"]
    print(inbox)

    # find all contacts whose id is other than id of logged in user

    mysql = connectToMySQL("private_wall_db")

    contacts_query = f" select id, first_name from registered_users where id <> {logged_in_user_id}; "
    all_contacts = mysql.query_db(contacts_query)
    print(all_contacts)



# -- SWITCHED SENDER WITH RECEIVER IN single join QUERY ABOVE to get all Outbox of current user -- SWEET

    mysql = connectToMySQL("private_wall_db") # But connect to db first

    msgs_from_current_usr = f" SELECT first_name, sender_id, recipient_id, msg_content FROM messages JOIN registered_users ON registered_users.id = messages.recipient_id where sender_id = {logged_in_user_id}; "

    # count of rows is number of messages
    outbox = mysql.query_db(msgs_from_current_usr)
    outbox_count = len(outbox)
    # outbox = session["outbox"]
    print(outbox)


    return render_template("success.html", logged_in_user = logged_in_user, logged_in_user_id = logged_in_user_id, inbox = inbox, inbox_count = inbox_count, outbox_count = outbox_count, all_contacts = all_contacts)

@app.route("/delete_msg/<msg_id>", methods = ["GET"])
def delete_msg_by_id(msg_id):
    print("HI")

    mysql = connectToMySQL("private_wall_db")

    delete_by_id = f"DELETE from messages where id = {msg_id};"

    deleted_msg = mysql.query_db(delete_by_id)
    print(deleted_msg)

    return redirect("/success")

@app.route("/send_msg/<contact_id>", methods = ["POST"])
def send_msg_to_id(contact_id):
    print("------SENDING------")

    mysql = connectToMySQL("private_wall_db")

    send_msg_to_id_query = "INSERT into messages (sender_id, recipient_id, msg_content, created_at) VALUES (%(sender_id)s, %(recipient_id)s, %(msg_content)s, NOW());"

    # recipient_id_ff means recipient from form
    data = {
            "sender_id": session["logged_in_user_id"],
            "recipient_id": request.form["recipient_id_ff"], 
            "msg_content": request.form["msg_content_ff"],
            }

    send_this_msg = mysql.query_db(send_msg_to_id_query, data)

    return redirect("/success")


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)

# /users/new- GET - method should return a template containing the form for adding a new user

# @app.route("/users/new", methods=["GET"])
# def add_user():
#     print(request.form)
#     return render_template("create_new.html")

# /users/create - POST - method should add the user to the database, then redirect to /users/<id>

# @app.route("/users/create", methods=["POST"])
# def add_user_to_db():
#     print(request.form)
#     mysql = connectToMySQL("users_db")

#     insert_query = "INSERT INTO users (first_name, last_name, email, password_hash, gender, birthday, interests, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password_hash)s, %(gender)s, %(birthday)s, %(interests)s, NOW(), NOW());"

#     data = {
#             "first_name": request.form["f_name"],
#             "last_name": request.form["l_name"], 
#             "email": request.form["e_mail"],
#             "password_hash": {password_hash},
#             "gender": request.form["gender"],
#             "birthday": request.form["birthday"],
#             "interests": request.form["interests"] 
#             }

#     new_user_id = mysql.query_db(insert_query, data)
#     return redirect("/users/" + str(new_user_id))


#  /users/<id> - GET - method should return a template that displays the specific user's information

# @app.route("/users/<id>", methods = ["GET"])
# def display_user_by_id(id):
#     print(request.form)

#     mysql = connectToMySQL("users_db")

#     select_by_id = f"SELECT * from users where user_id = {id};"
#     print(select_by_id)

#     displayed_user = mysql.query_db(select_by_id)
#     print(displayed_user)

#     return render_template("user_by_id.html", displayed_user = displayed_user)


# #  /users - GET - method should return a template that displays all the users in the table

# @app.route("/users", methods = ["GET"])
# # could have left it just "/users" without GET Method: coz it is the default. POST must be explicitly mentioned
# def display_all_users():
#     # call the function, passing in the name of our db
#     mysql = connectToMySQL('users_db')

#     # call the query_db function, pass in the query as a string
#     users = mysql.query_db('SELECT * FROM users;')

#     print(users)
#     return render_template("index.html", all_users = users)


# #  /users/<id>/edit - GET - method should return a template that displays a form for editing the user with the id specified in the url

# @app.route("/users/<id>/edit") # -- , methods=["GET"] commented out as it is the default
# def edit_user(id):
#     print(request.form)

#     mysql = connectToMySQL('users_db')

#     select_by_id = f"SELECT * from users where user_id = {id};"

#     displayed_user = mysql.query_db(select_by_id)
#     # print(displayed_user)

#     return render_template("update.html", displayed_user = displayed_user)



#  /users/<id>/update - POST - method should update the specific user in the database, then redirect to /users/<id>

# @app.route("/users/<id>/update", methods=["POST"])
# def update_user_in_db(id):
#     print("Hola")
#     mysql = connectToMySQL("users_db")

#     update_query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, updated_at = NOW() WHERE user_id = %(user_id)s;"
#     # print(update_query)
#     print("Hola" + id)
    
#     data = {
#             "first_name": request.form["f_name"],
#             "last_name": request.form["l_name"], 
#             "email": request.form["e_mail"],
#             "user_id": int(id)
#             }

#     mysql.query_db(update_query, data)

#     return redirect("/users/" + str(id))



#  /users/<id>/destroy - GET - method should delete the user with the specified id from the database, then redirect to /users

# @app.route("/users/<id>/destroy", methods = ["GET"])
# def delete_user_by_id(id):
#     print(request.form)

#     mysql = connectToMySQL("users_db")

#     delete_by_id = f"DELETE from users where user_id = {id};"

#     deleted_user = mysql.query_db(delete_by_id)
#     print(deleted_user)

#     return redirect("/users")


#  /users/<id>/edit - GET - method should return a template that displays a form for editing the user with the id specified in the url
#  /users/<id>/update - POST - method should update the specific user in the database, then redirect to /users/<id>
#  NINJA BONUS: Add a description (textarea) field to the user table and update the templates appropriately
#  NINJA BONUS: Ensure all the fields on the edit form are pre-populated (not just with placeholders)
# 
