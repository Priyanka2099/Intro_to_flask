from flask import Flask, render_template,redirect,url_for,request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY']='Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
Bootstrap(app)
db= SQLAlchemy(app)

login_manager= LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'

class User(UserMixin, db.Model):
    id= db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(20),unique=True)
    email=db.Column(db.String(50), unique=True)
    password= db.Column(db.String(80))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8,max=80)])
    remember= BooleanField('Remember me')

class RegisterForm(FlaskForm):
    email=StringField('email',validators=[InputRequired(),Email(message='Invalid email'), Length(max=50) ])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/Student')
def student():
    conn = sqlite3.connect('project.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Student")
    data=cursor.fetchall()
    return render_template('Student.html',Data=data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if  form.validate_on_submit():
        user=User.query.filter_by(username= form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('home'))
        return '<h1>Invalid username or password</h1>'

    return render_template('login.html', form= form)

@app.route('/signup',methods=['GET', 'POST'])
def signup():
    form= RegisterForm()

    if form.validate_on_submit():
        hashed_password= generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return  '<h1>Signup successful</h1>'
    return render_template('signup.html',form=form)

@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/logout')
@login_required
def logout():
    return redirect(url_for('index'))

@app.route('/sid1',methods=['GET','POST'])
def stu():
    return render_template('home.html',checkvar3=True)
@app.route('/pid1',methods=['GET','POST'])
def pid1():
    return render_template('home.html',checkvar4=True)
@app.route('/gid2',methods=['GET','POST'])
def gid1():
    return render_template('home.html',checkvar5=True)
@app.route('/studid',methods=['POST'])
def stud1():
    global ssid
    global demo1
    global demo2
    global dem2
    msg4="Invalid Sid"
    conn = sqlite3.connect('project.db')
    cursor = conn.cursor()
    ssid = request.form['sid']
    cursor.execute("SELECT sid from Student WHERE sid=%s " % ssid)
    data1 = cursor.fetchall()
    for i in data1:
        for j in i:
            demo1=j
    cursor.execute("SELECT Fname from Student WHERE sid=%s " % ssid)
    dat1 = cursor.fetchall()
    for i in dat1:
        for j in i:
            dem2 = j
    cursor.execute("SELECT Pname from Proctor P,Student S  WHERE S.Pid=P.Pid and sid=%s " % ssid)
    data2= cursor.fetchall()
    for i in data2:
        for j in i:
            demo2=j
    if(str(demo1)==ssid):
        return render_template('links.html',Dat1=dem2,Data=demo2,check=False)
    else:
        return render_template('home.html',Data8=msg4)

@app.route('/proctid',methods=['POST'])
def proct1():
    global ppid
    global demo3
    global dem3
    msg15 = "Invalid pid"
    conn=sqlite3.connect('project.db')
    cursor=conn.cursor()
    ppid=request.form['prid']
    cursor.execute("SELECT Pid from Proctor WHERE pid=%s " % ppid )
    data3=cursor.fetchall()
    for i in data3:
        for j in i:
            demo3=j
    cursor.execute("SELECT Pname from Proctor  WHERE Pid=%s " % ppid)
    dat2 = cursor.fetchall()
    for i in dat2:
        for j in i:
            dem3 = j
    cursor.execute("SELECT S.Sid,S.Fname,S.Lname,S.Branch,S.DOB,S.Phone,S.Address,S.Problem,S.Suggestion from Student S,Proctor P WHERE S.Pid=P.Pid AND P.Pid=%s " % ppid)
    data4=cursor.fetchall()
    if(str(demo3)==ppid):
        return render_template('Student.html',Dat5=dem3,Data=data4)
    else:
        return render_template('home.html',Data11=msg15)

@app.route('/parentid', methods=['GET','POST'])
def guard1():
    global var3
    global var4
    global var6
    msg6="Invalid Sid or name"
    conn = sqlite3.connect('project.db')
    cursor = conn.cursor()
    var3=request.form['gid']
    var4=request.form['gname']
    cursor.execute("SELECT G.Sid from Guardian G where G.Gname='%s' " % var4)
    var5 = cursor.fetchall()
    for i in var5:
        for j in i:
            var6=j
    if (str(var6) == var3):
        cursor.execute("SELECT S.Sid,S.Fname,S.Lname,S.Branch,S.DOB,S.Phone,S.Address,S.Problem,S.Suggestion from Student S where S.Sid=%s" % var6)
        var7=cursor.fetchall()
        return render_template('parent.html',Data=var7)
    else:
        return render_template('home.html',Data10=msg6)
@app.route('/links', methods=['GET','POST'])
def link():
    return render_template('links.html')
@app.route('/action', methods=['GET','POST'])
def link1():
    return render_template('index.html',checkvar=True)

@app.route('/ia', methods=['GET','POST'])
def marks():
    return render_template('form.html')
@app.route('/ia3', methods=['GET','POST'])
def marks5():
    conn = sqlite3.connect('project.db')
    cursor = conn.cursor()
    cursor.execute("SELECT S.Suggestion from Student S where S.Sid=%s " % ssid)
    var10=cursor.fetchall()
    for i in var10:
        for j in i:
            var11=j
    return render_template('links.html',check=True,Dat10=var11)

@app.route('/sug', methods=['GET','POST'])
def suggest():
    global var1
    var1=request.form['inp']
    return render_template('Student.html',checkvar1=True)
@app.route('/sug1', methods=['GET','POST'])
def suggest1():
    global var2
    conn = sqlite3.connect('project.db')
    cursor = conn.cursor()
    msg4 = "Successfully submitted!"
    var2 = request.form['inp1']
    cursor.execute("""UPDATE Student set Suggestion= ? where Sid=?""", (var2, var1))
    conn.commit()
    return render_template('Student.html',Data4=msg4)
@app.route('/sug2', methods=['GET','POST'])
def suggest2():
    conn = sqlite3.connect('project.db')
    cursor = conn.cursor()
    cursor.execute("SELECT Res_type,Sub_code,Marks from Results where Sid=%s " % var1)
    data35=cursor.fetchall()
    return render_template('marks.html',Data=data35)
@app.route('/sug3', methods=['GET','POST'])
def suggest3():
    conn = sqlite3.connect('project.db')
    cursor = conn.cursor()
    cursor.execute("SELECT Term,Sub_code,Atd_percentage from Attendance where Sid=%s " % var1)
    data36=cursor.fetchall()
    return render_template('attendance.html',Data=data36)

@app.route('/submit', methods=['GET','POST'])
def sub():
    try:
        conn = sqlite3.connect('project.db')
        cursor = conn.cursor()
        ma1=request.form['m1']
        ma2=request.form['m2']
        ma3=request.form['m3']
        ma4=request.form['m4']
        ma5=request.form['m5']
        ma6=request.form['m6']
        prb=request.form['pr']
        rad=request.form['t']
        cursor.execute("INSERT INTO Results (Sid,Res_type,Sub_code,Marks) values (?,?,'17CS61',?)",(ssid,rad,ma1))
        cursor.execute("INSERT INTO Results (Sid,Res_type,Sub_code,Marks) values (?,?,'17CS62',?)", (ssid,rad ,ma2))
        cursor.execute("INSERT INTO Results (Sid,Res_type,Sub_code,Marks) values (?,?,'17CS63',?)", (ssid,rad, ma3))
        cursor.execute("INSERT INTO Results (Sid,Res_type,Sub_code,Marks) values (?,?,'17CS64',?)", (ssid,rad, ma4))
        cursor.execute("INSERT INTO Results (Sid,Res_type,Sub_code,Marks) values (?,?,'17CS65',?)", (ssid,rad, ma5))
        cursor.execute("INSERT INTO Results (Sid,Res_type,Sub_code,Marks) values (?,?,'17CS66',?)", (ssid,rad, ma6))
        cursor.execute("""UPDATE Student set Problem= ? where Sid=?""",(prb,ssid))
        conn.commit()
        msg1="Your response has successfully submitted, thank you!"
        return render_template('form.html',Data1=msg1)

    except:
        message="Marks should be less than 40,try again"
        return render_template('form.html',Data=message)
@app.route('/ia1', methods=['GET','POST'])
def sub3():
    return render_template('atd.html')
@app.route('/sub2', methods=['GET','POST'])
def sub4():
        conn = sqlite3.connect('project.db')
        cursor = conn.cursor()
        at1=request.form['atd1']
        at2=request.form['atd2']
        at3=request.form['atd3']
        at4=request.form['atd4']
        at5=request.form['atd5']
        at6=request.form['atd6']
        prb1=request.form['atd7']
        rad1=request.form['t1']
        cursor.execute("INSERT INTO Attendance (Sid,Term,Sub_code,Atd_percentage) values (?,?,'17CS61',?)",(ssid,rad1,at1))
        cursor.execute("INSERT INTO Attendance (Sid,Term,Sub_code,Atd_percentage) values (?,?,'17CS62',?)", (ssid,rad1 ,at2))
        cursor.execute("INSERT INTO Attendance (Sid,Term,Sub_code,Atd_percentage) values (?,?,'17CS63',?)", (ssid,rad1, at3))
        cursor.execute("INSERT INTO Attendance (Sid,Term,Sub_code,Atd_percentage) values (?,?,'17CS64',?)", (ssid,rad1, at4))
        cursor.execute("INSERT INTO Attendance (Sid,Term,Sub_code,Atd_percentage) values (?,?,'17CS65',?)", (ssid,rad1, at5))
        cursor.execute("INSERT INTO Attendance (Sid,Term,Sub_code,Atd_percentage) values (?,?,'17CS66',?)", (ssid,rad1, at6))
        cursor.execute("""UPDATE Student set Problem= ? where Sid=?""",(prb1,ssid))
        conn.commit()
        msg2="Your response has successfully submitted, thank you!"
        return render_template('atd.html',Data1=msg2)



if __name__ == '__main__':
    app.run(debug=True)