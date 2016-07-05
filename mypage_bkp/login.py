from flask import *
import sqlite3
import database

app = Flask(__name__)

@app.route('/')
def default():
    """ handles the index page """

    return render_template ("welcome.html")

@app.route('/login', methods = ['GET','POST'])
def login():
    """ handles the login request """
    
    error = None
    if(request.method == 'GET'):
        return render_template ("login.html", input = 'login')
    elif(request.method == 'POST'):
        #username & password are the inputs by the user
        user = request.form['user']
        password = request.form['password']
        
        print request.method 
        if ((not user) and (not password)):
            error = "credentials missing"
        elif(not user):
	    error = "username missing"
        elif(not password):
            error = "password missing"
        else:
            #try block to handle when database is empty, indicates no user has registered yet   
            try:
                db = database.read_db('register')
                for row in db:
                    if((row[0] == user) & (row[1] == password)):
	                return render_template("login.html", input = "login_success", user = user)
                    elif((row[0] == user) & (row[1] != password)):
	                error = "wrong credentials"
                    else:
	                error = "user_unregistered"
            except TypeError:
	        error = "user_unregistered"
    return render_template("login.html", input = 'login', error = error) 

@app.route('/register', methods = ["GET", "POST"])
def register():
    """ hanldes the registration page """
  
    error = None  
    if( request.method == 'GET'):  
        return render_template("register.html", input = "register")
    elif( request.method == 'POST'):  
        #username and password are the inputs by the user 
        user = request.form['user']
        password = request.form['pwd']
        if ((not user) and (not password)): 
            error = "credentials missing"
        elif (not user):
            error = "username missing"
        elif (not password):
            error = "password missing"
        #verify, if username exists or not, if exists inform to the user to select a different username
        else:
            try :
                db = database.read_db('register')  
                for row in db:
                    if(row[0] == user):
                        error = "username already exists"
            except TypeError:
                database.register_table(user, password)
                return render_template("register.html", input = "register_success", user = user)
            #if (error != "username already exists"):
            if (not error):
                database.register_table(user, password)
                return render_template("register.html", input = "register_success", user = user)
        return render_template("register.html",  input = "register_fail", error = error)


@app.route('/<user>/add_family', methods = ['GET', 'POST'])
def add_family(user):
    """ handles the addition of new family """
    
    if('GET' == request.method):
        return render_template("register.html", input = "check_family_presence", user = user)
    elif('POST' == request.method):
        family_name = request.form['family_name']
        
        if (not family_name):
            error = "family name missing"
            return render_template("register.html", input = "check_family_presence", user = user, error = error)
        check = database.read_db(family_name)
        
        #check to verify if any table exists with the same family name
        if(0 == check):
            check_family_name = database.login_table(family_name)
            #check to verify if table creation with family name has failed
            if (check_family_name is not "Fail"):
   	        return render_template("register.html", input = "add_member_final", user = user, family_name = family_name)
            else:
                return render_template("500.html", error = "table creation failed")
	else:     
            return render_template("register.html", input = "add_member_final", flag = "family_present", user = user \
                                 , family_name = family_name)

@app.route('/<user>/add_member', methods = ['GET','POST'])
def add_member(user):
    """ adds family details based on user input """
 
    if('GET' == request.method):
        return render_template("register.html", input = "check_family_presence", user = user)
    elif('POST' == request.method):
        family_name = request.form['family_name']
        if (not family_name):
            error = "family name missing"
            return render_template("register.html", input = "register", user = user, error = error)
        else: 
            check = database.read_db(family_name)
        
            if(0 == check):
   	        return render_template("register.html", input = "family_empty", user = user, family_name = family_name)
	    else:     
                return render_template("register.html", input = "family_exists", user = user, family_name = family_name)

@app.route('/<user>/<family_name>/add_member', methods = ['GET','POST'])
def add_member_final(user, family_name):
    """ adds family details based on user input """
    
    error = None
    if('GET' == request.method):
        return render_template("register.html", input = "add_member_final", user = user, family_name = family_name)
    elif('POST' == request.method):
        member = request.form['member']
        age = request.form['age']
        
        if ((not member) and (not age)):
            error = "details missing"
        elif(not member):
            error = "member name missing"
        elif (not age):
            error = "member age missing"
        else:
            #check to verify if member exists in the family table with same name - NEEDS TO BE ADDED
            try: 
                db = database.read_db(family_name)
                for row in db:
                    if(row[0] == member):
                        error = "member already exists" 
            except TypeError:    
                database.login_table(family_name, member, age)
                return render_template("register.html", input = "mem_add_succ", user = user, family_name = family_name \
				   , member = member)
            if(not error):
                database.login_table(family_name, member, age)
                return render_template("register.html", input = "mem_add_succ", user = user, family_name = family_name \
				   , member = member)

        return render_template("register.html", input = "add_member_final", error = error)

@app.route('/<user>/family_details', methods = ['GET', 'POST'])
def family_details(user):
    """ handles displaying the family_details to the user """

    if('GET' == request.method):
        return render_template("register.html", input = "display_details", user = user)
    elif('POST' == request.method):
        family_name = request.form['family_name']
       
        if(not family_name):
            error = "missing family name"
        else:
            try :
                db = database.read_db(family_name)
                return render_template("register.html", input = 'display', user = user, db = db)
            except TypeError:
                error = "family db empty"
    
        return render_template("register.html", input = "display_details", error = error, user = user)
 

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

@app.route('/error_handler')
def error_handler():
    try:
        return render_template("welcome.html", input = z)
    except Exception as e:
        return render_template("500.html", error = e)

if __name__ == "__main__":
    app.run(debug=True)


