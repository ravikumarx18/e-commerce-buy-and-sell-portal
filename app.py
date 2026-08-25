from flask import Flask, render_template, request, redirect, flash, session, url_for
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
from datetime import datetime
import random
import os
from passlib.hash import sha256_crypt
from PIL import Image
import shutil
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configure database
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', '127.0.0.1')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'website')

# Configure mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mysql = MySQL(app)
mail = Mail(app)

# -------------------------------------------------------USER---------------------------------------------------------

def send_otp(reciever, otp):
    msg = Message(
        'OTP',
        sender='vaggaravikumar118@gmail.com',
        recipients=[reciever]
    )
    msg.body = "here is your one time password :" + str(otp)
    mail.send(msg)
    return redirect(url_for("verify"))


def send_otp_for_forgotPassword(reciever, otp):
    msg = Message(
        'OTP',
        sender='vaggaravikumar118@gmail.com',
        recipients=[reciever]
    )
    msg.body = "here is your one time password to reset your account password is :" + str(otp)
    mail.send(msg)
    return redirect(url_for("verify_to_reset_password"))


@app.route('/verify_to_reset_password', methods=['GET', 'POST'])
def verify_to_reset_password():

    if session.get('type') == "buyer":
        return redirect(url_for('home'))

    if session.get('type') == "seller":
        return redirect(url_for('myOrder'))

    if session.get('type') == "admin":
        return redirect(url_for('newProduct'))

    if request.method == "POST":

        if "otp" in session:

            if session["otp"] == int(request.form["otp"]):

                session['verify'] = True

                return redirect(url_for('newpassword'))

            else:
                flash('OTP is Wrong')

                return render_template(
                    'user/verify_to_reset.html'
                )

    return render_template('user/verify_to_reset.html')

# RESET PASSWORD
@app.route('/newpassword', methods=['GET', 'POST'])
def newpassword():

    # User must verify OTP first
    if not session.get('verify'):
        return redirect(url_for('forgotPassword'))

    # Make sure email and recipient are available
    if 'email' not in session or 'recipent' not in session:
        session.clear()
        session['type'] = "none"
        flash("Password reset session expired. Please try again.")
        return redirect(url_for('forgotPassword'))

    if request.method == 'POST':

        new_password = request.form.get('new', '').strip()
        confirm_password = request.form.get('confirm', '').strip()

        # Check empty password
        if not new_password or not confirm_password:

            flash("Please enter the password!")

            return render_template(
                'user/newpassword.html'
            )

        # Check whether passwords match
        if new_password != confirm_password:

            flash("Passwords do not match!")

            return render_template(
                'user/newpassword.html'
            )

        # Check account type
        if session['recipent'] not in ['buyer', 'seller', 'admin']:
            session.clear()
            session['type'] = "none"
            flash("Invalid account type.")
            return redirect(url_for('forgotPassword'))
        # Encrypt password
        encrypted_password = sha256_crypt.encrypt(new_password)
        cur = mysql.connection.cursor()

        # ---------------- BUYER ----------------
        if session['recipent'] == 'buyer':
            cur.execute(
                "UPDATE users SET password=%s WHERE email=%s",
                (
                    encrypted_password,
                    session['email']
                )
            )

        # ---------------- SELLER ----------------
        elif session['recipent'] == 'seller':

            cur.execute(
                "UPDATE seller SET password=%s WHERE email=%s",
                (
                    encrypted_password,
                    session['email']
                )
            )

        # ---------------- ADMIN ----------------
        elif session['recipent'] == 'admin':

            cur.execute(
                "UPDATE admin SET password=%s WHERE email=%s",
                (
                    encrypted_password,
                    session['email']
                )
            )

        # Save database changes
        mysql.connection.commit()
        cur.close()
        # Clear reset-password session
        session.clear()
        # Set default login state
        session['type'] = "none"
        flash("Password reset successfully! Please login.")
        return redirect(url_for('login'))
    return render_template('user/newpassword.html')


@app.route('/forgotPassword', methods=['GET', 'POST'])
def forgotPassword():

    print(session['type'])
    if session['type'] == "buyer":
        return redirect(url_for('home'))
    if session['type'] == "seller":
        return redirect(url_for('myOrder'))
    if session['type'] == "admin":
        return redirect(url_for('newProduct'))
    if request.method == "POST":
        email = request.form['email']
        recipent = request.form['recipent']

        if len(email) == 0:

            flash("Please Enter valid email")

        elif recipent == 'buyer':

            cursor = mysql.connection.cursor()

            cursor.execute(
                'SELECT * FROM users WHERE email=%s',
                (email,)
            )

            account = cursor.fetchone()
            row_count = cursor.rowcount

            if row_count == 0:

                flash("You Don't have an account, Please sign up")
            else:
                otp = random.randrange(111111, 999999)
                session["otp"] = otp
                session['email'] = email
                session['recipent'] = request.form.get('recipent')
                session['verify'] = False
                Y = send_otp_for_forgotPassword(
                    email,
                    otp
                )
                return Y
        elif recipent == 'seller':

            cursor = mysql.connection.cursor()

            cursor.execute(
                'SELECT * FROM seller WHERE email=%s',
                (email,)
            )

            account = cursor.fetchone()
            row_count = cursor.rowcount

            if row_count == 0:

                flash("You Don't have an account, Please sign up")

            else:

                otp = random.randrange(111111, 999999)
                session["otp"] = otp
                session['email'] = email
                session['recipent'] = request.form.get('recipent')
                session['verify'] = False
                Y = send_otp_for_forgotPassword(
                    email,
                    otp
                )
                return Y
        elif recipent == 'admin':

            cursor = mysql.connection.cursor()

            cursor.execute(
                'SELECT * FROM admin WHERE email=%s',
                (email,)
            )

            account = cursor.fetchone()
            row_count = cursor.rowcount

            if row_count == 0:

                flash("This is not an Admin email!")

            else:

                otp = random.randrange(111111, 999999)

                session["otp"] = otp
                session['email'] = email
                session['recipent'] = request.form.get('recipent')
                session['verify'] = False

                Y = send_otp_for_forgotPassword(
                    email,
                    otp
                )

                return Y

    return render_template('user/forgot_password.html')

@app.route('/verify', methods=['GET', 'POST'])
def verify():

    if session['type'] == "buyer":
        return redirect(url_for('home'))

    if session['type'] == "seller":
        return redirect(url_for('myOrder'))

    if session['type'] == "admin":
        return redirect(url_for('newProduct'))

    if request.method == "POST":
        if "otp" in session:

            if session["otp"] == int(request.form["otp"]):

                cur = mysql.connection.cursor()

                now = datetime.now()
                formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

                # BUYER
                if session['recipent'] == 'buyer':

                    cur.execute(
                        "INSERT INTO users(username, email, password, join_date) "
                        "VALUES(%s, %s, %s, %s)",
                        (
                            session["username"],
                            session["email"],
                            session["password"],
                            formatted_date
                        )
                    )

                    mysql.connection.commit()

                    session['id'] = cur.lastrowid
                    session['type'] = "buyer"

                    cur.close()

                    return redirect(url_for('home'))

                # SELLER
                elif session['recipent'] == 'seller':

                    cur.execute(
                        "INSERT INTO seller(seller_name, email, password, join_date) "
                        "VALUES(%s, %s, %s, %s)",
                        (
                            session["username"],
                            session["email"],
                            session["password"],
                            formatted_date
                        )
                    )

                    mysql.connection.commit()

                    session['id'] = cur.lastrowid
                    session['type'] = "seller"

                    cur.close()

                    return redirect(url_for('myOrder'))

                # ADMIN
                else:

                    cur.execute(
                        "INSERT INTO admin(username, email, password, join_date) "
                        "VALUES(%s, %s, %s, %s)",
                        (
                            session["username"],
                            session["email"],
                            session["password"],
                            formatted_date
                        )
                    )

                    mysql.connection.commit()

                    session['id'] = cur.lastrowid
                    session['type'] = "admin"

                    cur.close()

                    return redirect(url_for('newProduct'))

            else:
                flash("OTP is Wrong")
    return render_template('user/verify.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if session['type'] == "buyer":
        return redirect(url_for('home'))
    if session['type'] == "seller":
        return redirect(url_for('myOrder'))
    if session['type'] == "admin":
        return redirect(url_for('newProduct'))
    session.clear()
    session['type'] = "none"
    if request.method == "POST":
        # Fetch form data
        userDetails = request.form
        username = userDetails['username']
        email = userDetails['email']
        password = userDetails['password']
        recipent = userDetails['recipent']
        session['recipent'] = recipent
        if len(username) == 0 or len(email) == 0 or len(password) == 0:
            flash("Please fill the form completely!")
        else:            
            password = sha256_crypt.encrypt(password)
            if (recipent == 'buyer'):
                cursor = mysql.connection.cursor()
                cursor.execute('SELECT * FROM users WHERE email=%s', (email,))
                account = cursor.fetchone()
                row_count = cursor.rowcount
                if row_count != 0:
                    flash("You already have an account, Please sign in")
                else:
                    session["email"] = email
                    session["password"] = password
                    session["username"] = username
                    otp = random.randrange(111111, 999999)
                    session["otp"] = otp
                    Y = send_otp(email, otp)
                    return Y
            elif (recipent == 'seller'):
                cursor = mysql.connection.cursor()
                cursor.execute('SELECT * FROM seller WHERE email=%s', (email,))
                account = cursor.fetchone()
                row_count = cursor.rowcount
                if row_count != 0:
                    flash("You already have an account, Please sign in")
                else:
                    session["email"] = email
                    session["password"] = password
                    session["username"] = username
                    otp = random.randrange(111111, 999999)
                    session["otp"] = otp
                    Y = send_otp(email, otp)
                    return Y
            elif (recipent == 'admin'):
                cursor = mysql.connection.cursor()
                cursor.execute('SELECT * FROM' + 'admin' + ' WHERE email=%s', (email,))
                account = cursor.fetchone()
                row_count = cursor.rowcount
                if row_count != 0:
                    flash("You already have an account, Please sign in")
                else:
                    session["email"] = email
                    session["password"] = password
                    session["username"] = username
                    otp = random.randrange(111111, 999999)
                    session["otp"] = otp
                    Y = send_otp(email, otp)
                    return Y
    return render_template('user/signup.html')


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()
    session["type"] = "none"
    if request.method == "POST":
        if len(request.form['email']) == 0 or len(request.form['password']) == 0:
            flash("Invalid credentials!")
        else:
            email = request.form['email']
            password = (request.form['password'])
            recipent = request.form['recipent']
            # Check if account exists using MySQL
            cursor = mysql.connection.cursor()
            if (recipent == 'buyer'):
                cursor.execute('SELECT * FROM users WHERE email LIKE %s', ([email]))
                account = cursor.fetchone()
                row_count = cursor.rowcount
                if row_count == 0:
                    flash("You don't have a buyer account, Please create an account!")
                elif account[2] == email and (sha256_crypt.verify(password,account[3])):
                    session["id"] = account[0]
                    session["username"] = account[1]
                    session['type'] = "buyer"
                    return redirect(url_for('home'))
                else:
                    flash("Wrong password!")
            elif (recipent == 'seller'):
                cursor.execute('SELECT * FROM seller WHERE email LIKE %s', ([email]))
                account = cursor.fetchone()
                row_count = cursor.rowcount
                if row_count == 0:
                    flash("You don't have a seller account, Please create an account!")
                elif account[2] == email and (sha256_crypt.verify(password,account[10])):
                    session["loggedin"] = True
                    session["id"] = account[0]
                    session['username']=account[1]
                    session['type'] = "seller"
                    return redirect(url_for('myOrder'))
                else:
                    flash("Wrong password!")
            elif (recipent == 'admin'):
                cursor.execute('SELECT * FROM admin WHERE email LIKE %s', ([email]))
                account = cursor.fetchone()
                row_count = cursor.rowcount
                if row_count == 0:
                    flash("You don't have an Admin account, Please create an account!")
                elif account[1] == email and (sha256_crypt.verify(password,account[3])):
                    session["loggedin"] = True
                    session["id"] = account[0]
                    session['username']=account[2]
                    session['type'] = "admin"
                    return redirect(url_for('newProduct'))
                else:
                    flash("Wrong password!")
    return render_template("user/login.html")

@app.route('/logout')
def logout():
    session.clear()
    session['type']="none"
    return redirect(url_for('login'))

@app.route('/home')
def home():
    print(session['type'])
    if session['type'] == "none":
        return redirect(url_for('login'))
    if session['type'] == "seller":
        return redirect(url_for('myOrder'))
    if session['type'] == "admin":
        return redirect(url_for('newProduct'))
    cur = mysql.connection.cursor()
    category1 = []
    cur.execute('SELECT * FROM products WHERE category=%s', ('clothing',))
    allproducts = cur.fetchall()
    for products in allproducts:
        Dict = {}
        Dict['pid'] = products[0]
        Dict['proname'] = products[1]
        Dict['price'] = products[2]
        Dict['category'] = products[5]
        Dict['new']=products[4]
        Dict['rating']=int(products[7])
        Dict['no_of_ppl']=int(products[8])
        cur.execute("SELECT * FROM price WHERE pid=%s ORDER BY disprice", [products[0]])
        if cur.rowcount != 0:
            row = cur.fetchone()
            cur.execute("SELECT * FROM seller WHERE vid=%s", [row[2]])
            seller = cur.fetchone()
            Dict['sellerid'] = seller[0]
            Dict['disprice'] = row[4]
            category1.append(Dict)
    return render_template('user/index.html', category1=category1, )


@app.route('/contact')
def contact():
    if session['type'] == "none":
        return redirect(url_for('login'))
    if session['type'] == "seller":
        return redirect(url_for('myOrder'))
    if session['type'] == "admin":
        return redirect(url_for('newProduct'))
    return render_template("user/contact.html")


@app.route('/Catagories')
def catagories():
    if session['type'] == "none":
        return redirect(url_for('login'))
    if session['type'] == "seller":
        return redirect(url_for('myOrder'))
    if session['type'] == "admin":
        return redirect(url_for('newProduct'))
    cur = mysql.connection.cursor()
    category1 = []
    cur.execute('SELECT * FROM products WHERE category=%s', ('clothing',))
    allproducts = cur.fetchall()
    for products in allproducts:
        Dict = {}
        Dict['pid'] = products[0]
        Dict['proname'] = products[1]
        Dict['price'] = products[2]
        Dict['category'] = products[5]
        Dict['new']=products[4]
        Dict['rating']=int(products[7])
        Dict['no_of_ppl']=int(products[8])
        cur.execute("SELECT * FROM price WHERE pid=%s ORDER BY disprice", [products[0]])
        if cur.rowcount != 0:
            row = cur.fetchone()
            cur.execute("SELECT * FROM seller WHERE vid=%s ", [row[2]])
            seller = cur.fetchone()
            Dict['sellerid'] = seller[0]
            Dict['disprice'] = row[4]
            category1.append(Dict)
    category2 = []
    cur.execute('SELECT * FROM products WHERE category=%s', ('homedecor',))
    allproducts = cur.fetchall()
    for products in allproducts:
        Dict = {}
        Dict['pid'] = products[0]
        Dict['proname'] = products[1]
        Dict['price'] = products[2]
        Dict['category'] = products[5]
        Dict['new']=products[4]
        Dict['rating']=int(products[7])
        Dict['no_of_ppl']=int(products[8])
        cur.execute("SELECT * FROM price WHERE pid=%s ORDER BY disprice", [products[0]])
        if cur.rowcount != 0:
            row = cur.fetchone()
            cur.execute("SELECT * FROM seller WHERE vid=%s", [row[2]])
            seller = cur.fetchone()
            Dict['sellerid'] = seller[0]
            Dict['disprice'] = row[4]
            category2.append(Dict)
    category3 = []
    cur.execute('SELECT * FROM products WHERE category=%s', ('watches',))
    allproducts = cur.fetchall()
    for products in allproducts:
        Dict = {}
        Dict['pid'] = products[0]
        Dict['proname'] = products[1]
        Dict['price'] = products[2]
        Dict['category'] = products[5]
        Dict['new']=products[4]
        Dict['rating']=int(products[7])
        Dict['no_of_ppl']=int(products[8])
        cur.execute("SELECT * FROM price WHERE pid=%s ORDER BY disprice", [products[0]])
        if cur.rowcount != 0:
            row = cur.fetchone()
            cur.execute("SELECT * FROM seller WHERE vid=%s", [row[2]])
            seller = cur.fetchone()
            Dict['sellerid'] = seller[0]
            Dict['disprice'] = row[4]
            category3.append(Dict)

    category4 = []
    cur.execute('SELECT * FROM products WHERE category=%s', ('pantry',))
    allproducts = cur.fetchall()
    for products in allproducts:
        Dict = {}
        Dict['pid'] = products[0]
        Dict['proname'] = products[1]
        Dict['price'] = products[2]
        Dict['category'] = products[5]
        Dict['new']=products[4]
        Dict['rating']=int(products[7])
        Dict['no_of_ppl']=int(products[8])
        cur.execute("SELECT * FROM price WHERE pid=%s ORDER BY disprice", [products[0]])
        if cur.rowcount != 0:
            row = cur.fetchone()
            cur.execute("SELECT * FROM seller WHERE vid=%s", [row[2]])
            seller = cur.fetchone()
            Dict['sellerid'] = seller[0]
            Dict['disprice'] = row[4]
            category4.append(Dict)
    return render_template('user/Catagori.html', category1=category1, category2=category2, category3=category3,
                           category4=category4)


# A FUNCTION TO update the cart of people whose quantity of that item in cart is more than the current updated stock
def update_cart(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM cart WHERE user_id =%s", [user_id])
    rows = cur.fetchall()
    for row in rows:
        cur.execute("SELECT * FROM price WHERE vid =%s AND pid = %s", [row[4], row[2]])
        prod = cur.fetchone()
        if prod[6] < row[3]:
            cur.execute("UPDATE cart SET quantity = %s WHERE id = %s", [prod[6], row[0]])
            mysql.connection.commit()
            
    cur.close()


@app.route('/single_product_page/<int:pro_id>/<int:v_id>', methods=['GET', 'POST'])
def single_product_page(pro_id, v_id):
    if session['type'] == "none":
        return redirect(url_for('login'))
    if session['type'] == "seller":
        return redirect(url_for('myOrder'))
    if session['type'] == "admin":
        return redirect(url_for('newProduct'))
    # updates cart first
    update_cart(session['id'])
    cur = mysql.connection.cursor()
    # select the specific product
    cur.execute("SELECT * FROM products WHERE pid LIKE %s", [pro_id])
    curr_product = cur.fetchone()
    pro_name = curr_product[1]
    # data of current seller
    # data of current seller
    cur.execute("SELECT * FROM seller WHERE vid = %s", [v_id])
    curr_seller = list(cur.fetchone())

    # select current price row
    cur.execute("SELECT * FROM price WHERE vid=%s AND pid=%s", [v_id, pro_id])
    curr_price = cur.fetchone()

    # use product-specific seller name from price table
    curr_seller[1] = curr_price[7]
    # select all vendors who r selling
    cur.execute("SELECT * FROM price WHERE pid = %s ORDER BY disprice", [pro_id])
    rows = cur.fetchall()
    sellerList = []

    # extract the data of all sellers selling that product
    for row in rows:
        vid = int(row[2])
        cur.execute("SELECT * FROM seller WHERE vid = %s", [vid])
        vendor = cur.fetchone()
        Dict = {}
        Dict["vid"] = vendor[0]
        Dict["s_name"] = vendor[7]
        Dict["sell_at_price"] = row[4]
        sellerList.append(Dict)
    # to check that product in cart:- if it already exists or not (from all seller)
    cur.execute("SELECT* FROM cart WHERE user_id = %s AND pid = %s", [session["id"], pro_id])
    all_in_cart = cur.fetchall()
    total_in_cart = 0
    for row in all_in_cart:
        total_in_cart += row[3]
    # to check that product in cart:- if it already exists or not (from current seller)
    cur.execute("SELECT* FROM cart WHERE user_id = %s AND pid = %s AND vid = %s", [session["id"], pro_id, v_id])
    row_cnt = cur.rowcount
    in_cart = 0
    prod = 0
    # agr already exist karta hai vo product cart me...
    if row_cnt != 0:
        prod = cur.fetchone()
        # quantity in cart already
        in_cart = prod[3]
    cur.close()
    if request.method == 'POST':
        if request.form['btn1'] == "Add to cart":
            quan = 1
            # if cart me exist nahi karta
            if row_cnt == 0:
                in_cart = 1
                total_in_cart += 1
                cur = mysql.connection.cursor()
                # saath me vid me daal dena idhar.....
                cur.execute("INSERT INTO cart(user_id, pid, quantity, vid) Values( %s, %s, %s, %s)",
                            [session["id"], pro_id, quan, v_id])
                mysql.connection.commit()
                cur.close()
            else:
                total_in_cart -= in_cart
                count = min(curr_price[6], in_cart + 1)
                in_cart = count
                total_in_cart += count
                cur = mysql.connection.cursor()
                # vid here too
                cur.execute("UPDATE cart SET quantity = %s WHERE user_id = %s AND pid = %s AND vid = %s",
                            [count, session["id"], pro_id, v_id])
                mysql.connection.commit()
                cur.close()
            return render_template('user/single-product.html', singleproduct=curr_product, minprice=curr_price[4],
                                   sellerList=sellerList, curr_seller=curr_seller, in_cart=in_cart,
                                   total_in_cart=total_in_cart, actualPrice=curr_product[2])
        # ye "elif" me error aa raha tha.....but "else" is working fine
        elif request.form['btn1'] == "Buy now":
            return redirect(url_for('checkout1', v_id=v_id, pro_id=pro_id))
        else:
            vid=request.form.get('selectseller')
            return redirect(url_for('single_product_page', v_id=vid, pro_id=pro_id))
    return render_template('user/single-product.html', singleproduct=curr_product, minprice=curr_price[4],
                           sellerList=sellerList, curr_seller=curr_seller, in_cart=in_cart, total_in_cart=total_in_cart, actualPrice=curr_product[2])


@app.route('/decrease_in_cart/<int:pro_id>/<int:v_id>')
def decrease_in_cart(pro_id, v_id):
    if session['type'] == "none":
        return redirect(url_for('login'))
    if session['type'] == "seller":
        return redirect(url_for('myOrder'))
    if session['type'] == "admin":
        return redirect(url_for('newProduct'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM cart WHERE user_id = %s AND pid=%s AND vid = %s", [session["id"], pro_id, v_id])
    row = cur.fetchone()
    count = row[3] - 1
    cur.execute("UPDATE cart SET quantity = %s WHERE user_id = %s AND pid = %s AND vid = %s",
                [count, session["id"], pro_id, v_id])
    mysql.connection.commit()
    if count == 0:
        cur.execute("DELETE FROM cart WHERE user_id = %s AND pid=%s AND vid = %s", [session["id"], pro_id, v_id])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('cart'))


@app.route('/delete_in_cart/<int:pro_id>/<int:v_id>')
def delete_in_cart(pro_id, v_id):
    if session['type'] == "none":
        return redirect(url_for('login'))
    if session['type'] == "seller":
        return redirect(url_for('myOrder'))
    if session['type'] == "admin":
        return redirect(url_for('newProduct'))
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM cart WHERE user_id = %s AND pid=%s AND vid = %s", [session["id"], pro_id, v_id])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('cart'))


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if session['type'] == "none":
        return redirect(url_for('login'))
    if session['type'] == "seller":
        return redirect(url_for('myOrder'))
    if session['type'] == "admin":
        return redirect(url_for('newProduct'))
    cur = mysql.connection.cursor()
    update_cart(session['id'])
    cur.execute("SELECT * FROM cart WHERE user_id LIKE %s", [session["id"]])
    cartitems = cur.fetchall()
    cartlist = []
    tprice = 0
    for item in cartitems:
        cur = mysql.connection.cursor()
        pid = int(item[2])
        cur.execute("SELECT * FROM products WHERE pid LIKE %s", [pid])
        allproducts = cur.fetchall()
        Dict = {}
        for products in allproducts:
            Dict['pid'] = products[0]
            Dict['proname'] = products[1]
            Dict['price'] = products[2]
            Dict['quantity'] = item[3]
            Dict['totalprice'] = item[3] * Dict['price']
            cur.execute("SELECT * FROM seller WHERE vid=%s", [item[4]])
            seller = cur.fetchone()
            Dict['seller'] = seller[1]
            Dict['sellerid'] = seller[0]
            Dict['category'] = products[5]
            cartlist.append(Dict)
            tprice = tprice + Dict['totalprice']
    return render_template('user/cart.html', carts=cartlist, totalprice=tprice)



@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if session['type'] == "none":
        return redirect(url_for('login'))
    if session['type'] == "seller":
        return redirect(url_for('myOrder'))
    if session['type'] == "admin":
        return redirect(url_for('newProduct'))
    if request.method == "POST":
        
        first_name = request.form['first']
        last_name = request.form['last']
        company = request.form['company']
        number = request.form['number']
        email = request.form['email']
        add1 = request.form['add1']
        add2 = request.form['add2']
        city = request.form['city']
        district = request.form['district']
        Postcode = request.form['Postcode']
        order_notes = request.form['message']
        payment_method = request.form.get('selector')
        tandc = request.form.get('tandc')

        if len(request.form['first'])==0 or len(request.form['last'])==0 or len(request.form['number'])==0 or len(request.form['email'])==0 or len(request.form['add1'])==0 or len(request.form['add2'])==0 or len(request.form['city'])==0 or len(request.form['district'])==0 or len(request.form['Postcode'])==0:
        
            flash("Please Fill all the necessary details!")
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM cart WHERE user_id LIKE %s", [session["id"]])
            cartitems = cur.fetchall()
            cartlist = []
            tprice = 0
            for item in cartitems:
                cur = mysql.connection.cursor()
                pid = int(item[2])
                cur.execute("SELECT * FROM products WHERE pid LIKE %s", [pid])
                allproducts = cur.fetchall()
                Dict = {}
                for products in allproducts:
                    Dict['pid'] = products[0]
                    Dict['proname'] = products[1]
                    Dict['price'] = products[2]
                    Dict['quantity'] = item[3]
                    Dict['totalprice'] = item[3] * Dict['price']
                    cur.execute("SELECT * FROM seller WHERE vid=%s", [item[4]])
                    seller = cur.fetchone()
                    Dict['seller'] = seller[1]
                    Dict['seller_id'] = seller[0]
                    Dict['category'] = products[5]
                    cartlist.append(Dict)
                    tprice = tprice + Dict['totalprice']
                    print(tprice)
            return render_template("user/checkout.html", carts=cartlist, totalprice=tprice)

        elif payment_method == None:
            flash("select Payment Method")
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM cart WHERE user_id LIKE %s", [session["id"]])
            cartitems = cur.fetchall()
            cartlist = []
            tprice = 0
            for item in cartitems:
                cur = mysql.connection.cursor()
                pid = int(item[2])
                cur.execute("SELECT * FROM products WHERE pid LIKE %s", [pid])
                allproducts = cur.fetchall()
                Dict = {}
                for products in allproducts:
                    Dict['pid'] = products[0]
                    Dict['proname'] = products[1]
                    Dict['price'] = products[2]
                    Dict['quantity'] = item[3]
                    Dict['totalprice'] = item[3] * Dict['price']
                    cur.execute("SELECT * FROM seller WHERE vid=%s", [item[4]])
                    seller = cur.fetchone()
                    Dict['seller'] = seller[1]
                    Dict['seller_id'] = seller[0]
                    Dict['category'] = products[5]
                    cartlist.append(Dict)
                    tprice = tprice + Dict['totalprice']
                    print(tprice)
            return render_template("user/checkout.html", carts=cartlist, totalprice=tprice)
            
        elif tandc == None:
            flash("Please accept term and conditions")
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM cart WHERE user_id LIKE %s", [session["id"]])
            cartitems = cur.fetchall()
            cartlist = []
            tprice = 0
            for item in cartitems:
                cur = mysql.connection.cursor()
                pid = int(item[2])
                cur.execute("SELECT * FROM products WHERE pid LIKE %s", [pid])
                allproducts = cur.fetchall()
                Dict = {}
                for products in allproducts:
                    Dict['pid'] = products[0]
                    Dict['proname'] = products[1]
                    Dict['price'] = products[2]
                    Dict['quantity'] = item[3]
                    Dict['totalprice'] = item[3] * Dict['price']
                    cur.execute("SELECT * FROM seller WHERE vid=%s", [item[4]])
                    seller = cur.fetchone()
                    Dict['seller'] = seller[1]
                    Dict['seller_id'] = seller[0]
                    Dict['category'] = products[5]
                    cartlist.append(Dict)
                    tprice = tprice + Dict['totalprice']
                    print(tprice)
            return render_template("user/checkout.html", carts=cartlist, totalprice=tprice)


        else:
            cur = mysql.connection.cursor()
            now = datetime.now()
            formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

            # inserting into order details

            cur.execute(
                "INSERT INTO order_details(first_name, last_name, company, number, email, add1, add2, city, district, Postcode, order_notes, payment_method, datetime) Values(%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (first_name, last_name, company, number, email, add1, add2, city, district, Postcode, order_notes,
                    payment_method, formatted_date))
            mysql.connection.commit()

            cur.execute("SELECT * FROM cart WHERE user_id LIKE %s", [session["id"]])
            cartitems = cur.fetchall()
            cur.close()
            tprice = 0

            for item in cartitems:
                cur = mysql.connection.cursor()
                cur.execute("SELECT * FROM price WHERE vid=%s AND pid=%s", [item[4], item[2]])
                curr_price = cur.fetchone()
                # for order id
                cur.execute(
                    "SELECT * FROM order_details WHERE first_name=%s AND last_name=%s AND company=%s AND number=%sAND email=%s AND add1=%s AND add2=%s AND city=%s AND district=%s AND Postcode=%s AND order_notes=%s AND payment_method=%s AND datetime=%s",
                    [first_name, last_name, company, number, email, add1, add2, city, district, Postcode, order_notes,
                        payment_method, formatted_date])
                curr_order = cur.fetchone()
                cur.close()
            return redirect(url_for('confirmation', did=curr_order[0]))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM cart WHERE user_id LIKE %s", [session["id"]])
    cartitems = cur.fetchall()
    cartlist = []
    tprice = 0
    for item in cartitems:
        cur = mysql.connection.cursor()
        pid = int(item[2])
        cur.execute("SELECT * FROM products WHERE pid LIKE %s", [pid])
        allproducts = cur.fetchall()
        Dict = {}
        for products in allproducts:
            Dict['pid'] = products[0]
            Dict['proname'] = products[1]
            Dict['price'] = products[2]
            Dict['quantity'] = item[3]
            Dict['totalprice'] = item[3] * Dict['price']
            cur.execute("SELECT * FROM seller WHERE vid=%s", [item[4]])
            seller = cur.fetchone()
            Dict['seller'] = seller[1]
            Dict['seller_id'] = seller[0]
            Dict['category'] = products[5]
            cartlist.append(Dict)
            tprice = tprice + Dict['totalprice']
            print(tprice)
    return render_template("user/checkout.html", carts=cartlist, totalprice=tprice)

@app.route('/checkout1/<int:pro_id>/<int:v_id>', methods=['GET', 'POST'])
def checkout1(pro_id, v_id):
    if session['type'] == "none":
        return redirect(url_for('login'))
    if session['type'] == "seller":
        return redirect(url_for('myOrder'))
    if session['type'] == "admin":
        return redirect(url_for('newProduct'))
    if request.method == "POST":
        
        first_name = request.form['first']
        last_name = request.form['last']
        company = request.form['company']
        number = request.form['number']
        email = request.form['email']
        add1 = request.form['add1']
        add2 = request.form['add2']
        city = request.form['city']
        district = request.form['district']
        Postcode = request.form['Postcode']
        order_notes = request.form['message']
        payment_method = request.form.get('selector')
        tandc = request.form.get('tandc')

        if len(request.form['first'])==0 or len(request.form['last'])==0 or len(request.form['number'])==0 or len(request.form['email'])==0 or len(request.form['add1'])==0 or len(request.form['add2'])==0 or len(request.form['city'])==0 or len(request.form['district'])==0 or len(request.form['Postcode'])==0:
            
            flash("Please Fill all the necessary details!")
            
            cur = mysql.connection.cursor()
            cartlist = []
            tprice = 0
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM products WHERE pid LIKE %s", [pro_id])
            allproducts = cur.fetchall()
            Dict = {}
            for products in allproducts:
                Dict['pid'] = products[0]
                Dict['proname'] = products[1]
                Dict['price'] = products[2]
                Dict['quantity'] = 1
                Dict['totalprice'] = 1 * Dict['price']
                cur.execute("SELECT * FROM seller WHERE vid=%s", [v_id])
                seller = cur.fetchone()
                Dict['seller'] = seller[1]
                Dict['seller_id'] = seller[0]
                Dict['category'] = products[5]
                cartlist.append(Dict)
                tprice = tprice + Dict['totalprice']
                print(tprice)

        elif payment_method == None:
            flash("select Payment Method")

            cur = mysql.connection.cursor()
            cartlist = []
            tprice = 0
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM products WHERE pid LIKE %s", [pro_id])
            allproducts = cur.fetchall()
            Dict = {}
            for products in allproducts:
                Dict['pid'] = products[0]
                Dict['proname'] = products[1]
                Dict['price'] = products[2]
                Dict['quantity'] = 1
                Dict['totalprice'] = 1 * Dict['price']
                cur.execute("SELECT * FROM seller WHERE vid=%s", [v_id])
                seller = cur.fetchone()
                Dict['seller'] = seller[1]
                Dict['seller_id'] = seller[0]
                Dict['category'] = products[5]
                cartlist.append(Dict)
                tprice = tprice + Dict['totalprice']
                print(tprice)

        elif tandc == None:
            flash("Please accept term and conditions")
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM cart WHERE user_id LIKE %s", [session["id"]])
            cartitems = cur.fetchall()
            cartlist = []
            tprice = 0
            for item in cartitems:
                cur = mysql.connection.cursor()
                pid = int(item[2])
                cur.execute("SELECT * FROM products WHERE pid LIKE %s", [pid])
                allproducts = cur.fetchall()
                Dict = {}
                for products in allproducts:
                    Dict['pid'] = products[0]
                    Dict['proname'] = products[1]
                    Dict['price'] = products[2]
                    Dict['quantity'] = item[3]
                    Dict['totalprice'] = item[3] * Dict['price']
                    cur.execute("SELECT * FROM seller WHERE vid=%s", [item[4]])
                    seller = cur.fetchone()
                    Dict['seller'] = seller[1]
                    Dict['seller_id'] = seller[0]
                    Dict['category'] = products[5]
                    cartlist.append(Dict)
                    tprice = tprice + Dict['totalprice']
                    print(tprice)
            return render_template("user/checkout.html", carts=cartlist, totalprice=tprice)
        else:
            cur = mysql.connection.cursor()
            now = datetime.now()
            formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
            # inserting into order details
            cur.execute(
                "INSERT INTO order_details(first_name, last_name, company, number, email, add1, add2, city, district, Postcode, order_notes, payment_method, datetime) Values(%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (first_name, last_name, company, number, email, add1, add2, city, district, Postcode, order_notes,
                payment_method, formatted_date))
            mysql.connection.commit()
            tprice = 0

            cur.execute("SELECT * FROM price WHERE vid=%s AND pid=%s", [v_id, pro_id])
            curr_price = cur.fetchone()
            # for order id
            cur.execute(
                "SELECT * FROM order_details WHERE first_name=%s AND last_name=%s AND company=%s AND number=%sAND email=%s AND add1=%s AND add2=%s AND city=%s AND district=%s AND Postcode=%s AND order_notes=%s AND payment_method=%s AND datetime=%s",
                [first_name, last_name, company, number, email, add1, add2, city, district, Postcode, order_notes,
                payment_method, formatted_date])
            curr_order = cur.fetchone()
            cur.close()
            return redirect(url_for('confirmation1', pro_id=pro_id, v_id=v_id, did=curr_order[0]))

    cur = mysql.connection.cursor()
    cartlist = []
    tprice = 0
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products WHERE pid LIKE %s", [pro_id])
    allproducts = cur.fetchall()
    Dict = {}
    for products in allproducts:
        Dict['pid'] = products[0]
        Dict['proname'] = products[1]
        Dict['price'] = products[2]
        Dict['quantity'] = 1
        Dict['totalprice'] = 1 * Dict['price']
        cur.execute("SELECT * FROM seller WHERE vid=%s", [v_id])
        seller = cur.fetchone()
        Dict['seller'] = seller[1]
        Dict['seller_id'] = seller[0]
        Dict['category'] = products[5]
        cartlist.append(Dict)
        tprice = tprice + Dict['totalprice']
        print(tprice)
    return render_template("user/checkout.html", carts=cartlist, totalprice=tprice)
@app.route('/confirmation/<int:did>', methods=['GET', 'POST'])
def confirmation(did):
    if session['type'] == "none":
        return redirect(url_for('login'))
    if session['type'] == "seller":
        return redirect(url_for('myOrder'))
    if session['type'] == "admin":
        return redirect(url_for('newProduct'))
    cur = mysql.connection.cursor()
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

    cur.execute("SELECT * FROM cart WHERE user_id LIKE %s", [session["id"]])
    cartitems = cur.fetchall()

    cur.execute("SELECT * FROM order_details WHERE did = %s", [did])
    details = cur.fetchone()

    cartlist = []
    tprice = 0
    tquantity = 0
    for item in cartitems:
        pid = int(item[2])
        cur.execute("SELECT * FROM products WHERE pid LIKE %s", [pid])
        allproducts = cur.fetchall()
        Dict = {}
        for products in allproducts:
            Dict['pid'] = products[0]
            Dict['proname'] = products[1]
            Dict['price'] = products[2]
            Dict['quantity'] = item[3]
            tquantity += item[3]
            Dict['totalprice'] = item[3] * Dict['price']
            cur.execute("SELECT * FROM seller WHERE vid=%s", [item[4]])
            seller = cur.fetchone()
            Dict['seller'] = seller[1]
            Dict['sellerid'] = seller[0]
            Dict['category'] = products[5]
            cartlist.append(Dict)
            tprice = tprice + Dict['totalprice']

    for item in cartitems:
        cur.execute("SELECT * FROM price WHERE vid=%s AND pid=%s", [item[4], item[2]])
        curr_price = cur.fetchone()

        cur.execute(
            "INSERT INTO orders( user_id, pro_id, quantity, price, datetime, vid, did) Values( %s, %s, %s, %s, %s, %s, %s)",
            [session["id"], item[2], item[3], curr_price[3], formatted_date, item[4], details[0]])
        mysql.connection.commit()
        
        cur.execute("UPDATE price SET stock=%s WHERE vid=%s AND pid=%s", [curr_price[6]-item[3],item[4], item[2]])
        mysql.connection.commit()
    cur.execute("DELETE FROM cart WHERE user_id LIKE %s", [session["id"]])
    mysql.connection.commit()
    cur.close()

    return render_template("user/confirmation.html", carts=cartlist, totalprice=tprice, totalquantity=tquantity,
                           details=details)
@app.route('/confirmation1/<int:pro_id>/<int:v_id>/<int:did>', methods=['GET', 'POST'])
def confirmation1(pro_id, v_id, did):
    if session['type'] == "none":
        return redirect(url_for('login'))
    if session['type'] == "seller":
        return redirect(url_for('myOrder'))
    if session['type'] == "admin":
        return redirect(url_for('newProduct'))
    cur = mysql.connection.cursor()

    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

    cur.execute("SELECT * FROM order_details WHERE did = %s", [did])
    details = cur.fetchone()

    cartlist = []
    tprice = 0
    tquantity = 0
    cur.execute("SELECT * FROM products WHERE pid LIKE %s", [pro_id])
    allproducts = cur.fetchall()
    Dict = {}
    for products in allproducts:
        Dict['pid'] = products[0]
        Dict['proname'] = products[1]
        Dict['price'] = products[2]
        Dict['quantity'] = 1
        tquantity += 1
        Dict['totalprice'] = 1 * Dict['price']
        cur.execute("SELECT * FROM seller WHERE vid=%s", [v_id])
        seller = cur.fetchone()
        Dict['seller'] = seller[1]
        Dict['sellerid'] = seller[0]
        Dict['category'] = products[5]
        cartlist.append(Dict)
        tprice = tprice + Dict['totalprice']    
    cur.execute("SELECT * FROM price WHERE vid=%s AND pid=%s", [v_id, pro_id])
    curr_price = cur.fetchone()

    cur.execute(
        "INSERT INTO orders( user_id, pro_id, quantity, price, datetime, vid, did) Values( %s, %s, %s, %s, %s, %s, %s)",
        [session["id"], pro_id, 1, curr_price[3], formatted_date, v_id, did])
    mysql.connection.commit()
    cur.execute("UPDATE price SET stock=%s WHERE vid=%s AND pid=%s", [curr_price[6]-1,v_id, pro_id])
    mysql.connection.commit()
    
    return render_template("user/confirmation.html", carts=cartlist, totalprice=tprice, totalquantity=tquantity)

@app.route('/order')
def order():
    if session['type'] == "none":
        return redirect(url_for('login'))
    if session['type'] == "seller":
        return redirect(url_for('myOrder'))
    if session['type'] == "admin":
        return redirect(url_for('newProduct'))
    mycursor = mysql.connection.cursor()
    sql = "SELECT * FROM orders WHERE user_id = %s"
    adr = (session['id'], )
    mycursor.execute(sql, adr)
    myresult = mycursor.fetchall()
    orderlist=[]
    for result in myresult:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM products WHERE pid=%s',[result[2]])
        account = cursor.fetchone()
        Dict={}
        Dict['id']=result[0]
        Dict['pname']=account[1]
        Dict['pid'] = account[0]
        Dict['quantity']=result[3]
        Dict['price']=result[4]
        Dict['status']=result[6]
        Dict['date']=result[5]
        Dict['category']=account[5]
        orderlist.append(Dict)
    return render_template("user/orderHistory.html",orders=orderlist) 

@app.route('/review/<int:proid>',methods=['GET','POST'])
def review(proid):
    if session['type'] == "none":
        return redirect(url_for('login'))
    if session['type'] == "seller":
        return redirect(url_for('myOrder'))
    if session['type'] == "admin":
        return redirect(url_for('newProduct'))
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM reviews WHERE pid=%s and uid=%s',[proid,session['id']])
    account = cursor.fetchone()
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM products WHERE pid=%s',[proid])
    account1 = cursor.fetchone()
    reviewed=False
    if account:
        reviewed=True
    if request.method == "POST":
        userDetails=request.form
        Rating=userDetails['rating']
        comment=userDetails['comment']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM reviews WHERE pid=%s',[proid])
        count = cursor.rowcount
        now = datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO reviews(pid,uid,rating,comment,datetime) Values(%s,%s,%s,%s,%s)", [proid,session['id'],Rating,comment,formatted_date])
        mysql.connection.commit()
        cur.close()
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM products WHERE pid=%s',[proid])
        r = cursor.fetchone()
        rating=((count*r[7])+int(Rating))/(count+1)
        mycursor = mysql.connection.cursor()
        sql = "UPDATE products SET rating = %s WHERE pid = %s"
        val = (rating,proid)
        mycursor.execute(sql, val)
        mysql.connection.commit()
        return redirect(url_for("order"))
    return render_template('user/review.html',singleproduct=account1,reviewed=reviewed)

@app.route('/showreview/<int:pid>', methods=['POST','GET'])
def showreview(pid):
    if session['type'] == "none":
        return redirect(url_for('login'))
    if session['type'] == "seller":
        return redirect(url_for('myOrder'))
    if session['type'] == "admin":
        return redirect(url_for('newProduct'))
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM reviews WHERE pid=%s',[pid])
    reviews = cursor.fetchall()
    return render_template('user/showreviews.html',reviews=reviews)

#----------------------------------------------------- VENDOR PAGE ------------------------------------------------
@app.route('/addProduct', methods=["GET", "POST"])
def addProduct():

    if session['type'] == "buyer":
        return redirect(url_for('home'))

    if session['type'] == "none":
        return redirect(url_for('login'))

    if session['type'] == "admin":
        return redirect(url_for('newProduct'))

    # ADD PRODUCT
    if request.method == 'POST':

        productDetails = request.form

        pname = productDetails['pname']
        category = productDetails['category']
        price = float(productDetails['price'].replace(',', '').replace('INR', '').strip())
        disprice = float(productDetails['disprice'].replace(',', '').replace('INR', '').strip())
        pdetails = productDetails['pdetails']
        stock = int(productDetails['stock'])

        # Current date and time
        now = datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

        # INSERT PRODUCT INTO TEMPORARY PRODUCT TABLE
        cur = mysql.connection.cursor()

        cur.execute(
            """
            INSERT INTO temporary_product
            (
                pname,
                vid,
                category,
                pdetails,
                price,
                disprice,
                stock,
                datetime
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                pname,
                session['id'],
                category,
                pdetails,
                price,
                disprice,
                stock,
                formatted_date
            )
        )

        mysql.connection.commit()

        # SAVE PRODUCT IMAGE
        rid = cur.lastrowid

        file = request.files.get('file')

        if file and file.filename != '':

            upload_folder = os.path.join(
                app.root_path,
                'static',
                'img',
                'categori',
                'temporaryProduct'
            )

            os.makedirs(upload_folder, exist_ok=True)

            img_filename = '(' + str(rid) + ',).png'

            temp_filename = secure_filename(file.filename)
            temp_path = os.path.join(upload_folder, temp_filename)

            file.save(temp_path)

            # Convert uploaded image to PNG
            img1 = Image.open(temp_path)
            img2 = img1.convert('RGB')

            final_path = os.path.join(
                upload_folder,
                img_filename
            )

            img2.save(final_path)

            # Remove original uploaded file
            os.remove(temp_path)

        # CREATE PENDING NOTIFICATION
        cur.execute(
            """
            INSERT INTO notification
            (
                person1_id,
                pname,
                content,
                date
            )
            VALUES (%s, %s, %s, %s)
            """,
            (
                session['id'],
                pname,
                "Pending",
                formatted_date
            )
        )
        mysql.connection.commit()

        cur.close()

        # PRODUCT ADDED SUCCESSFULLY
        flash("Product submitted successfully. Waiting for admin approval.")

        return redirect(url_for('myProduct'))

    # GET REQUEST
    return render_template('vendor/add-product.html')

@app.route('/allProduct')
def allProduct():
    if session['type'] == "buyer":
        return redirect(url_for('home'))
    if session['type'] == "none":
        return redirect(url_for('login'))
    if session['type'] == "admin":
        return redirect(url_for('newProduct'))
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM products ')
    account1 = cursor.fetchall()
    return render_template('vendor/product_list_vendor.html', item1=account1)

@app.route('/myProduct')
def myProduct():
    if session['type'] == "buyer":
        return redirect(url_for('home'))
    if session['type'] == "none":
        return redirect(url_for('login'))
    if session['type'] == "admin":
        return redirect(url_for('newProduct'))
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM price WHERE vid=%s',[session['id']])
    productlist = cursor.fetchall()
    prodlist = []
    for product in productlist:
        cur = mysql.connection.cursor()
        cur.execute( "SELECT * FROM products WHERE pid LIKE %s", [product[1]] )
        products = cur.fetchone()
        Dict = {}
        Dict['proname']=products[1]
        Dict['pid']=products[0]
        Dict['price']=products[2]
        Dict['disprice']=product[4]
        Dict['category']=products[5]
        Dict['stock']=product[6]
        prodlist.append(Dict)
    return render_template("vendor/myProduct.html",prodlist=prodlist)

@app.route('/productsvendor/<int:pid>', methods=['POST','GET'])
def productsvendor(pid):
    if session['type'] == "buyer":
        return redirect(url_for('home'))
    if session['type'] == "none":
        return redirect(url_for('login'))
    if session['type'] == "admin":
        return redirect(url_for('newProduct'))
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM price WHERE vid=%s and pid=%s',[session['id'],pid])
    productlist = cursor.fetchone()
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM products WHERE pid=%s',[pid])
    product = cursor.fetchone()
    if request.method=='POST':
        productDetails=request.form
        stock=productDetails['stock']
        disprice=productDetails['disprice']
        mycursor = mysql.connection.cursor()
        sql = "UPDATE price SET disprice= %s,stock=%s WHERE pid = %s and vid = %s"
        val = (disprice,stock,pid,session['id'])
        mycursor.execute(sql, val)
        mysql.connection.commit()
        return redirect(url_for('myProduct'))
    return render_template('vendor/productpage-vendor.html',productlist=productlist,singleproduct=product)

@app.route('/deliver/<int:oid>',methods=['POST','GET'])
def deliver(oid):
    if session['type'] == "buyer":
        return redirect(url_for('home'))
    if session['type'] == "none":
        return redirect(url_for('login'))
    if session['type'] == "admin":
        return redirect(url_for('newProduct'))
    if request.method=='POST':
        mycursor = mysql.connection.cursor()
        sql = "UPDATE orders SET delivery_status = %s WHERE (order_id = %s)"
        adr = ('Delivered',oid )
        mycursor.execute(sql, adr)
        mysql.connection.commit()
        mycursor.close()
    return redirect(url_for('myOrder'))
@app.route('/myOrder')
def myOrder():
    if session['type'] == "buyer":
        return redirect(url_for('home'))
    if session['type'] == "none":
        return redirect(url_for('login'))
    if session['type'] == "admin":
        return redirect(url_for('newProduct'))
    
    mycursor = mysql.connection.cursor()
    sql = "SELECT * FROM orders WHERE vid = %s AND delivery_status = %s ORDER BY order_id DESC"
    adr = (session['id'], 'Not Delivered')
    mycursor.execute(sql, adr)
    myresult = mycursor.fetchall()
    mycursor.close()
    return render_template("vendor/vendor-orders.html", orders=myresult) 

@app.route('/vendororderhistory')
def vendororderhistory():
    if session['type'] == "buyer":
        return redirect(url_for('home'))

    if session['type'] == "none":
        return redirect(url_for('login'))

    if session['type'] == "admin":
        return redirect(url_for('newProduct'))

    mycursor = mysql.connection.cursor()

    sql = "SELECT * FROM orders WHERE vid = %s AND delivery_status = %s ORDER BY order_id DESC"
    adr = (session['id'],'Delivered')

    mycursor.execute(sql, adr)
    myresult = mycursor.fetchall()

    mycursor.close()

    return render_template(
        "vendor/orderhistory-vendor.html",
        orders=myresult
    )

@app.route('/notifications')
def notifications():
    if session['type'] == "buyer":
        return redirect(url_for('home'))

    if session['type'] == "none":
        return redirect(url_for('login'))

    if session['type'] == "admin":
        return redirect(url_for('newProduct'))

    mycursor = mysql.connection.cursor()

    sql = "SELECT * FROM notification WHERE person1_id = %s ORDER BY date DESC"

    adr = (session['id'],)

    mycursor.execute(sql, adr)

    myresult = mycursor.fetchall()

    mycursor.close()

    return render_template(
        "vendor/notifications-vendor.html",
        messages=myresult
    )

@app.route('/productpagevendor/<int:pid>' ,methods=['POST','GET'])
def productpagevendor(pid):
    if session['type'] == "buyer":
        return redirect(url_for('home'))
    if session['type'] == "none":
        return redirect(url_for('login'))
    if session['type'] == "admin":
        return redirect(url_for('newProduct'))
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM price WHERE vid=%s and pid=%s',[session['id'],pid])
    productlist = cursor.fetchone()
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM products WHERE pid=%s',[pid])
    product = cursor.fetchone()
    return render_template('vendor/productfororder-vendor.html',productlist=productlist,singleproduct=product)

@app.route('/orderdetailsvendor/<int:oid>',methods=['POST','GET'])
def orderdetailsvendor(oid):
    if session['type'] == "buyer":
        return redirect(url_for('home'))
    if session['type'] == "none":
        return redirect(url_for('login'))
    if session['type'] == "admin":
        return redirect(url_for('newProduct'))
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM orders WHERE order_id=%s',[oid])
    orderlist = cursor.fetchone()
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM order_details WHERE did=%s',[orderlist[8]])
    orderdetails = cursor.fetchone()
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM products WHERE pid=%s',[orderlist[2]])
    prodetails = cursor.fetchone()
    return render_template('vendor/orderdetails-vendor.html',orderlist = orderlist,orderdetails=orderdetails,prodetails=prodetails)

@app.route('/verifyProduct/<int:req_id>', methods=['GET', 'POST'])
def verifyProduct(req_id):
    if session['type'] == "buyer":
        return redirect(url_for('home'))

    if session['type'] == "none":
        return redirect(url_for('login'))

    if session['type'] == "seller":
        return redirect(url_for('myOrder'))

    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT * FROM temporary_product WHERE rid LIKE %s",
        [req_id]
    )
    singleproduct = cur.fetchone()
    cur.close()

    if request.method == "POST":

        if request.form['btn2'] == "Accept":

            # INSERT PRODUCT INTO PRODUCTS TABLE
            cur = mysql.connection.cursor()

            cur.execute(
                """
                INSERT INTO products
                (pname, price, pdetails, category)
                VALUES (%s, %s, %s, %s)
                """,
                [
                    singleproduct[2],
                    singleproduct[3],
                    singleproduct[4],
                    singleproduct[6]
                ]
            )

            mysql.connection.commit()

            prodtid = cur.lastrowid
            cur.close()

            # INSERT PRICE DETAILS
            now = datetime.now()
            formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

            cur = mysql.connection.cursor()

            cur.execute(
                """
                INSERT INTO price
                (pid, vid, price, disprice, dateadded, stock)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                [
                    prodtid,
                    singleproduct[1],
                    singleproduct[3],
                    singleproduct[5],
                    formatted_date,
                    singleproduct[7]
                ]
            )

            mysql.connection.commit()
            cur.close()

            # SEND ACCEPTED NOTIFICATION
            cur = mysql.connection.cursor()

            cur.execute(
                """
                INSERT INTO notification
                (person1_id, pname, content, date)
                VALUES (%s, %s, %s, %s)
                """,
                [
                    singleproduct[1],
                    singleproduct[2],
                    "Accepted",
                    formatted_date
                ]
            )

            mysql.connection.commit()
            cur.close()

            # MOVE PRODUCT IMAGE
            upload_folder = os.path.join(
                app.root_path,
                'static',
                'img',
                'categori',
                'temporaryProduct'
            )

            # Image uploaded when the seller submitted the product
            source = os.path.join(
                upload_folder,
                '(' + str(req_id) + ',).png'
            )

            # Create category folder
            destination_folder = os.path.join(
                upload_folder,
                str(singleproduct[6])
            )

            os.makedirs(
                destination_folder,
                exist_ok=True
            )

            # New image name = product ID
            destination = os.path.join(
                destination_folder,
                str(prodtid) + '.png'
            )

            # Move image from temporaryProduct to category folder
            dest = shutil.move(
                source,
                destination
            )
            # DELETE TEMPORARY PRODUCT
            cur = mysql.connection.cursor()
            cur.execute(
                "DELETE FROM temporary_product WHERE rid = %s",
                [singleproduct[0]]
            )
            mysql.connection.commit()
            cur.close()
        else:
            # REJECT PRODUCT
            now = datetime.now()
            formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
            cur = mysql.connection.cursor()
            cur.execute(
                """
                INSERT INTO notification
                (person1_id, pname, content, date)
                VALUES (%s, %s, %s, %s)
                """,
                [
                    singleproduct[1],
                    singleproduct[2],
                    "Rejected",
                    formatted_date
                ]
            )

            mysql.connection.commit()
            cur.close()

            # Delete rejected temporary product
            cur = mysql.connection.cursor()

            cur.execute(
                "DELETE FROM temporary_product WHERE rid = %s",
                [singleproduct[0]]
            )

            mysql.connection.commit()
            cur.close()
        return redirect(url_for("newProduct"))
    return render_template(
        'admin/verify-product.html',
        singleproduct=singleproduct
    )

@app.route('/allProduct_admin')
def allProduct_admin():
    if session['type'] == "buyer":
        return redirect(url_for('home'))
    if session['type'] == "none":
        return redirect(url_for('login'))
    if session['type'] == "seller":
        return redirect(url_for('myOrder'))
    return "eifjei"

@app.route('/usersadmin')
def usersadmin():
    if session['type'] == "buyer":
        return redirect(url_for('home'))
    if session['type'] == "none":
        return redirect(url_for('login'))
    if session['type'] == "seller":
        return redirect(url_for('myOrder'))
    cur = mysql.connection.cursor()
    cur.execute( "SELECT * FROM users" )
    users = cur.fetchall()
    return render_template('admin/userlist.html' ,odelist=users)

@app.route('/vendorList')
def vendorList():
    if session['type'] == "buyer":
        return redirect(url_for('home'))
    if session['type'] == "none":
        return redirect(url_for('login'))
    if session['type'] == "seller":
        return redirect(url_for('myOrder'))
    cur = mysql.connection.cursor()
    cur.execute( "SELECT * FROM seller WHERE deleted=0" )
    sellers = cur.fetchall()
    return render_template("admin/vendorList.html",sellers=sellers)

@app.route('/vendorproducts/<int:vid>')
def vendorproducts(vid):
    if session['type'] == "buyer":
        return redirect(url_for('home'))
    if session['type'] == "none":
        return redirect(url_for('login'))
    if session['type'] == "seller":
        return redirect(url_for('myOrder'))
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM price WHERE vid=%s',[vid])
    productlist = cursor.fetchall()
    prodlist = []
    for product in productlist:
        cur = mysql.connection.cursor()
        cur.execute( "SELECT * FROM products WHERE pid LIKE %s", [product[1]] )
        products = cur.fetchone()
        Dict = {}
        Dict['vid']=vid
        Dict['proname']=products[1]
        Dict['pid']=products[0]
        Dict['price']=products[2]
        Dict['disprice']=product[4]
        Dict['category']=products[5]
        Dict['stock']=product[6]
        prodlist.append(Dict)
    return render_template("admin/venprolist_admin.html",prodlist=prodlist)
@app.route('/productpageadmin/<int:vid>/<int:pid>' , methods=['POST','GET'])
def productpageadmin(vid,pid):
    if session['type'] == "buyer":
        return redirect(url_for('home'))
    if session['type'] == "none":
        return redirect(url_for('login'))
    if session['type'] == "seller":
        return redirect(url_for('myOrder'))
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM price WHERE vid=%s and pid=%s',[vid,pid])
    productlist = cursor.fetchone()
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM products WHERE pid=%s',[pid])
    product = cursor.fetchone()
    return render_template('admin/productpage-admin.html',productlist=productlist,singleproduct=product)
@app.route('/vendororders/<int:vid>')
def vendororders(vid):
    if session['type'] == "buyer":
        return redirect(url_for('home'))
    if session['type'] == "none":
        return redirect(url_for('login'))
    if session['type'] == "seller":
        return redirect(url_for('myOrder'))
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM orders WHERE vid=%s',[vid])
    orderslist = cursor.fetchall()
    return render_template("admin/venodelist_admin.html",odelist=orderslist)

@app.route('/vendordetails/<int:vid>', methods=['POST','GET'])
def vendordetails(vid):
    if session['type'] == "buyer":
        return redirect(url_for('home'))
    if session['type'] == "none":
        return redirect(url_for('login'))
    if session['type'] == "seller":
        return redirect(url_for('myOrder'))
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM seller WHERE vid=%s',[vid])
    vendor = cursor.fetchone()
    return render_template('admin/vendordetails-admin.html',vendor=vendor)

@app.route('/removevendor/<int:vid>', methods=['POST','GET'])
def removevendor(vid):
    if session['type'] == "buyer":
        return redirect(url_for('home'))
    if session['type'] == "none":
        return redirect(url_for('login'))
    if session['type'] == "seller":
        return redirect(url_for('myOrder'))
    mycursor = mysql.connection.cursor()
    sql = "UPDATE seller SET deleted = %s WHERE (vid = %s)"
    adr = (1,vid )
    mycursor.execute(sql, adr)
    mysql.connection.commit()
    mycursor.close()
    mycursor = mysql.connection.cursor()
    sql = "DELETE FROM price WHERE vid=%s"
    adr = (vid,)
    mycursor.execute(sql, adr)
    mysql.connection.commit()
    mycursor.close()
    return redirect(url_for('vendorList'))

@app.route('/ordersforadmin')
def ordersforadmin():
    if session['type'] == "buyer":
        return redirect(url_for('home'))
    if session['type'] == "none":
        return redirect(url_for('login'))
    if session['type'] == "seller":
        return redirect(url_for('myOrder'))
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM orders ORDER BY datetime DESC')
    orderslist = cursor.fetchall()
    return render_template('admin/allordersadmin.html',odelist=orderslist)

@app.route('/buyerList')
def buyerList():
    if session['type'] == "buyer":
        return redirect(url_for('home'))
    if session['type'] == "none":
        return redirect(url_for('login'))
    if session['type'] == "seller":
        return redirect(url_for('myOrder'))
    return render_template("admin/BuyerList.html")

@app.route('/newProduct')
def newProduct():
    if session['type'] == "buyer":
        return redirect(url_for('home'))
    if session['type'] == "none":
        return redirect(url_for('login'))
    if session['type'] == "seller":
        return redirect(url_for('myOrder'))
    mycursor = mysql.connection.cursor()
    sql = "SELECT * FROM temporary_product"
    mycursor.execute(sql)
    tempproducts = mycursor.fetchall()
    return render_template("admin/newProduct.html",tempproducts=tempproducts)

if __name__=='__main__':
    app.run(debug=True)
