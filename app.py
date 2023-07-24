from flask import Flask, render_template, request,session
import ibm_db
app = Flask(__name__)

conn = ibm_db.connect("DATABASE=bludb; HOSTNAME=9938aec0-8105-433e-8bf9-0fbb7e483086.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud; PORT=32459; UID=gzg63402; PWD=8OF1eYRZXMiVNEMM; SECURITY=SSL; sslcertificate=DigiCertGlobalRootCA.crt","","")
print(conn)
connState = ibm_db.active(conn)
print(connState)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/jobbrowse")
def jobbrowse():
    return render_template("job-list.html")

@app.route("/jobpost")
def jobpost():
    return render_template("job-post.html")

@app.route("/jobview")
def jobview():
    return render_template("job-view.html")

@app.route("/login",methods = ['GET','POST'])
def login():
    global email
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        details = [email,password]
        print(details)
        sql = "SELECT * FROM REGISTER_HC where EMAILID=? AND PASSWORD=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.bind_param(stmt, 2, password)
        ibm_db.execute(stmt)
        acc = ibm_db.fetch_assoc(stmt)
        print(acc)

        if acc:
            session['email'] = email
            session['username'] = acc['NAME']
            uemail = session['email']
            uname = acc['NAME']
            return render_template("profile.html", name=uname, email=uemail)
        else:
            msg = "Invalid Credentials"

            return render_template("login.html", msg= msg)

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("email",None)
    session.pop("username",None)
    return render_template("index.html")


@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        details = [name,email,password,role]
        print(details)

        sql = "SELECT * FROM REGISTER_HC where EMAILID=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.execute(stmt)
        acc = ibm_db.fetch_assoc(stmt)
        print(acc)
        if acc:

            msg = "You have been already REGISTERED! Please Log In"

            return render_template("login.html", msg = msg)
        else:
            sql = "INSERT into REGISTER_HC VALUES (?,?,?,?)"
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.bind_param(stmt, 1, name)
            ibm_db.bind_param(stmt, 2, email)
            ibm_db.bind_param(stmt, 3, password)
            ibm_db.bind_param(stmt, 4, role)
            ibm_db.execute(stmt)
            msg = "You have Successfully REGISTERED, Please LOGIN"

            return render_template("login.html", msg=msg)
        
    return render_template("login.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)