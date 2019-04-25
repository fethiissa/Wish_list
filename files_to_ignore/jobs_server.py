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
    
    mysql = connectToMySQL("employee_jobs_db")
    query = "SELECT * FROM employee_jobs_db.registered_users WHERE email = %(email)s;"
    
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

        mysql = connectToMySQL("employee_jobs_db")
        
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

    # see if the username provided exists in the database
    
    mysql = connectToMySQL("employee_jobs_db")
    query = "SELECT * FROM registered_users WHERE email = %(username)s;"
    
    data = { "username" : request.form["username"] }
    result = mysql.query_db(query, data)

    print(result)


    # if we didn't find anything in the database by searching by username or if the passwords don't match,
    # flash an error message and redirect back to a safe route
    # flash("You could not be logged in")
    # return redirect("/")

    if len(result) < 1:
        login_valid = False
        flash("User Doesn't exit", "login_error")


    if len(request.form["username"]) < 1:
        login_valid = False
        flash("Username must be provided", "login_error")   #username_
        # return redirect('/')

    if len(request.form["password"]) < 1:
        login_valid = False
        flash("Password field can not be left blank. \n Use any of Upper and Lower case letters, Numbers and Special Characters", "login_error")    #password_blank
        # return redirect('/')


    if not bcrypt.check_password_hash(result[0]['password_hash'], request.form['password']):
        flash("Wrong Password. Try Again", "bad_password_error")   #wrong_password
        login_valid = False
        # return redirect('/')


    if not login_valid:
        flash("You could not be logged in", "login_error")
        return redirect("/")
    
    #     # assuming we only have one user with this username, the user would be first in the list we get back
    #     # of course, we should have some logic to prevent duplicates of usernames when we create users


    # use bcrypt's check_password_hash method, passing the hash from our database and the password from the form

    # else: bcrypt.check_password_hash(result[0]['password_hash'], request.form['password']):
    # if we get True after checking the password, we may put the user and their id in session

    session['logged_in_user'] = result[0]['first_name']
    session['logged_in_user_id'] = result[0]['id']

    flash("Login Successful", "success")
    print(result)

    # never render on a post, always redirect!
    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():

    logged_in_user_id = session['logged_in_user_id']
    logged_in_user = session['logged_in_user']


    mysql = connectToMySQL("employee_jobs_db")

    query_all_jobs = "select jobs.id, title, location, posted_by_id from jobs where assigned_to_id is NULL;"

    all_jobs = mysql.query_db(query_all_jobs)

    print(all_jobs)


    mysql = connectToMySQL("employee_jobs_db")

    query_my_jobs = f"select jobs.id, title from jobs where assigned_to_id = {logged_in_user_id};"

    my_jobs = mysql.query_db(query_my_jobs)
    
    print("********ALL MY JOBS*********")
    print(my_jobs)    
    print("********ALL MY JOBS*********")

    return render_template("dashboard.html", logged_in_user = logged_in_user, logged_in_user_id = logged_in_user_id, all_jobs = all_jobs, my_jobs = my_jobs)

###

@app.route("/jobs/new")
def add_new_job():

    logged_in_user_id = session['logged_in_user_id']
    logged_in_user = session['logged_in_user']


    return render_template("create_new.html", logged_in_user = logged_in_user, logged_in_user_id = logged_in_user_id)

@app.route("/add_new", methods = ["POST"])
def add_this_job():
    # Book VAlidation Here
    # book_valid = True
    # end of Validation

    logged_in_user_id = session['logged_in_user_id']
    logged_in_user = session['logged_in_user']

    job_valid = True

    if len(request.form["title"]) < 1:
        job_valid = False
        flash("Field cannot be Blank!","title_error")
        return redirect("/jobs/new")

    if len(request.form["job_desc"]) < 1:
        job_valid = False
        flash("Field cannot be Blank!","desc_error")
        return redirect("/jobs/new")

    # if not book_valid:
    #     redirect("/books")
    
    # else:
    # Since validation passed
    mysql1 = connectToMySQL("employee_jobs_db")

    # Get this to work SOON
    # insert_book = " START TRANSACTION; \n DECLARE BookKey int; \n INSERT INTO books (uploaded_by_id, title, description, created_at, updated_at) VALUES (%(uploaded_by_id)s, %(title)s, %(book_desc)s, NOW(), NOW()); \n  SET bookKey = LAST_INSERT_ID(); \n INSERT INTO favorites(book_id, user_id) VALUES (bookKey, %(user_id)s); \n COMMIT;"

    # Old tag before I used transaction and Last Insert ID() 
    insert_job = "INSERT INTO jobs (title, job_desc, location, posted_by_id, job_category, other, created_at, updated_at) VALUES (%(title)s, %(job_desc)s, %(location)s, %(posted_by_id)s, %(job_category)s, %(other)s, NOW(), NOW());"

    print(request.form)

    if "job_category" not in request.form:

        new_job_data = {
        # "assigned_to_id": -1, -- %(assigned_to_id)s, 
        "title": request.form["title"],
        "job_desc": request.form["job_desc"],
        "location": request.form["location"],
        "job_category": " ",     # session["job_category"]: request.form.getlist["job_category"],          # -- session["interest"] = request.form.getlist("chkInterest")
        "other": request.form["other"],
        "posted_by_id": logged_in_user_id
    }
    
    new_job_data = {
    # "assigned_to_id": -1, -- %(assigned_to_id)s, 
    "title": request.form["title"],
    "job_desc": request.form["job_desc"],
    "location": request.form["location"],
    "job_category": " items ",           # -- session["interest"] = request.form.getlist("chkInterest")   + request.form.getlist["job_category"],
    "other": request.form["other"],
    "posted_by_id": logged_in_user_id
    }


    added_job_id = mysql1.query_db(insert_job, new_job_data)
    # newly_added_job_id = session["added_job_id"]
    print(added_job_id)

    return redirect("/jobs/"+str(added_job_id))

@app.route("/jobs/edit")
def edit_job():

    logged_in_user_id = session['logged_in_user_id']
    logged_in_user = session['logged_in_user']


    return render_template("update.html")

@app.route("/jobs/edit/<job_id>")
def edit_job_by_id(job_id):

    print("In EDIT JOB Mode")
    update_valid = True

    logged_in_user_id = session['logged_in_user_id']
    logged_in_user = session['logged_in_user']

    # # Update Validations
    # if len(request.form["title"]) < 1:
    #     update_valid = False
    #     flash("Field cannot be Blank!","update_title_error")
    #     return redirect("/jobs/edit/" + job_id)

    # if len(request.form["job_desc"]) < 1:
    #     update_valid = False
    #     flash("Field cannot be Blank!","update_desc_error")
    #     return redirect("/jobs/edit" + job_id)

    mysql = connectToMySQL("employee_jobs_db")

    select_job_by_id = f"SELECT * from jobs where id = {job_id};"
    print(select_job_by_id)

    displayed_job = mysql.query_db(select_job_by_id)
    print(displayed_job)

    return render_template("update.html", logged_in_user = logged_in_user, logged_in_user_id = logged_in_user_id, displayed_job = displayed_job)


@app.route("/jobs/edit/<job_id>", methods = ["POST"])
def edit_this_job(job_id):
    # Book VAlidation Here
    # book_valid = True
    # end of Validation

    logged_in_user_id = session['logged_in_user_id']
    logged_in_user = session['logged_in_user']


    # if not book_valid:
    #     redirect("/books")

    mysql = connectToMySQL("employee_jobs_db")


    update_query = "UPDATE jobs SET title = %(title)s, job_desc = %(job_desc)s, location = %(location)s, updated_at = NOW() WHERE id = %(job_id)s;"
    print(update_query)
    print("########### UBDATING THIS BOOK ###########")
    
    update_data = {
            "title": request.form["title"],
            "job_desc": request.form["job_desc"], 
            "location": request.form["location"],
            "job_id": job_id
            }

    updated_job_id =  mysql.query_db(update_query, update_data)


    print(updated_job_id)

    print("********JOB JUST GOT UPDATED*********")

    return redirect("/jobs/"+str(job_id))


################

@app.route("/jobs/<job_id>")
def view_job_by_id(job_id):

    print("In DISPLAY JOB Mode")

    logged_in_user_id = session['logged_in_user_id']
    logged_in_user = session['logged_in_user']


    # def display_user_by_id(id):
    # print(request.form)

    mysql = connectToMySQL("employee_jobs_db")

    select_job_by_id = f"SELECT * from jobs where id = {job_id};"
    print(select_job_by_id)

    displayed_job = mysql.query_db(select_job_by_id)
    print(displayed_job)

    return render_template("view_job_by_id.html", logged_in_user = logged_in_user, logged_in_user_id = logged_in_user_id, displayed_job = displayed_job)



@app.route("/jobs/add_to_my_jobs/<job_id>")
def add_to_my_jobs(job_id):

    logged_in_user_id = session['logged_in_user_id']
    logged_in_user = session['logged_in_user']


    mysql1 = connectToMySQL("employee_jobs_db")

    make_job_mine = f"UPDATE jobs SET assigned_to_id = {logged_in_user_id} where id = {job_id};"
    # add_to_mine = "INSERT INTO assigned_tasks (job_id, user_id) VALUES (%(job_id)s, %(user_id)s);"

    # job_to_add_data = {
    #     "job_id": job_id,
    #     "user_id": logged_in_user_id
    # }

    #  job_to_add_data)

    my_new_job = mysql1.query_db(make_job_mine)

    return redirect("/dashboard")

@app.route("/jobs/give_up/<job_id>")
def give_up(job_id):

    logged_in_user_id = session['logged_in_user_id']
    logged_in_user = session['logged_in_user']

    print("--------> JOB TO GIVE UP <---------")

    mysql1 = connectToMySQL("employee_jobs_db")

    give_up_this_job = f"UPDATE jobs SET assigned_to_id = NULL where id = {job_id};"
    # give_up_this_one = "DELETE FROM employee_jobs_db.assigned_tasks WHERE job_id = %(job_id)s and user_id = %(logged_in_user_id)s;" -- # , all_jobs = all_jobs, my_jobs = my_jobs)

    # which_job = {
    #     "assigned_to_id": "NULL",
    #      "job_id": job_id
    # }

    mysql1.query_db(give_up_this_job)

    print(give_up_this_job)

    # session.pop(my_job["title"])

    return redirect("/dashboard")


@app.route("/jobs/remove/<job_id>")
def delete_job_by_id(job_id):
    print("!!!!!!!!!!!REMOVE JOB ENTIRELY!!!!!!!!!!!")

    logged_in_user_id = session['logged_in_user_id']
    logged_in_user = session['logged_in_user']


    mysql = connectToMySQL("employee_jobs_db")

    delete_by_id = f"DELETE from jobs where id = {job_id};"

    mysql.query_db(delete_by_id)

    return redirect("/dashboard")

@app.route("/jobs/done/<job_id>")
def remove_job_coz_it_is_done(job_id):

    print("@@@@@@@@@ JOB IS DONE SO I CALL REMOVE METHOD ABOVE @@@@@@@@@@")

    delete_job_by_id(job_id) # calling remove job method from above

    return redirect("/jobs/remove/<job_id>")


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)




#  /users/<id>/edit - GET - method should return a template that displays a form for editing the user with the id specified in the url
#  /users/<id>/update - POST - method should update the specific user in the database, then redirect to /users/<id>
#  NINJA BONUS: Add a description (textarea) field to the user table and update the templates appropriately
#  NINJA BONUS: Ensure all the fields on the edit form are pre-populated (not just with placeholders)
# 
