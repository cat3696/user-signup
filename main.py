from flask import Flask, request, redirect, render_template

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def index():
    return render_template("main.html")
# route to display form

@app.route('/main.html')
def display_user_signup_form():
    return render_template('main.html')

# Validation functions

def empty_val(x):
    if x:
        return True
    else:
        return False

def char_length(x):
    if len(x) > 2 and len(x) < 21:
        return True
    else:
        return False

def at_symbol(x):
    if x.count('@') >= 1:
        return True
    else:
        return False

def at_symbol_plural(x):
    if x.count('@') <= 1:
        return True
    else:
        return False

def email_period(x):
    if x.count('.') == 1:
        return True
    else:
        return False


# route to process and validate form

@app.route("/main.html", methods=['POST'])
def user_signup_complete():

    username = request.form['username']
    password = request.form['password']
    password_validate = request.form['password_validate']
    email = request.form['email']

    # empty strings for es

    username_e = ""
    password_e = ""
    password_validate_e = ""
    email_e = ""

    #e Messages
    e_required = "Required field"
    e_reenter_password = "Please re-enter password"
    e_char_count = "must be between 3 and 20 characters"
    e_no_space = "must not contain space"
    # password validation

    if not empty_val(password):
        password_e = e_required
        password = ''
        password_validate = ''
    elif not char_length(password):
        password_e = "password " + e_char_count
        password = ''
        password_validate = ''
        password_validate_e = e_reenter_password
    else:
        if " " in password:
            password_e = "password " + e_no_space
            password = ''
            validation_e = ''
            password_validate_e = e_reenter_password

    # password match validation

    if password_validate != password:
        password_validate_e = "passwords must match."
        password = ''
        password_validate = ''
        password_e = 'passwords must match.'
            

    # Username validation

    if not empty_val(username):
        username_e = e_required
        password = ''
        password_validate = ''
        password_e = e_reenter_password
        password_validate_e = e_reenter_password
    elif not char_length(username):
        username_e = "Username " + e_char_count
        password = ''
        password_validate = ''
        password_e = e_reenter_password
        password_validate_e = e_reenter_password
    else:
        if " " in username:
            username_e = "Username " + e_no_space
            password = ''
            password_validate = ''
            password_e = e_reenter_password
            password_validate_e = e_reenter_password
    #Email validation

    # See if email contains text prior to running validations
    if empty_val(email):
        # validations start here
        if not char_length(email):
            email_e = "Email " + e_char_count
            password = ''
            password_validate = ''
            password_e = e_reenter_password
            password_validate_e = e_reenter_password
        elif not at_symbol(email):
            email_e = "Email must contain the @ symbol."
            password = ''
            password_validate = ''
            password_e = e_reenter_password
            password_validate_e = e_reenter_password
        elif not at_symbol_plural(email):
            email_e = "Email must contain only one @ symbol."
            password = ''
            password_validate = ''
            password_e = e_reenter_password
            password_validate_e = e_reenter_password
        elif not email_period(email):
            email_e = "Email must contain one period."
            password = ''
            password_validate = ''
            password_e = e_reenter_password
            password_validate_e = e_reenter_password
        else:
            if " " in email:
                email_e = "Email " + e_no_space
                password = ''
                password_validate = ''
                password_e = e_reenter_password
                password_validate_e = e_reenter_password

    if not username_e and not password_e and not password_validate_e and not email_e:
        username = username
        return redirect('/welcome?username={0}'.format(username))
    else:
        return render_template('main.html', username_e=username_e, username=username, password_e=password_e, password=password, password_validate_e=password_validate_e, password_validate=password_validate, email_e=email_e, email=email)

# redirect to welcome

@app.route('/welcome')
def valid_signup():
    username = request.args.get('username')
    return render_template('welcome.html', username=username)

app.run()