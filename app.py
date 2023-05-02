from flask import Flask,request,redirect,render_template,url_for,flash,session,send_file,abort
from flask_mysqldb import MySQL
from flask_session import Session
from otp import genotp
from sotp import tokgenotp
from sstoken import stoken
from cmail import sendmail
import flask_excel as excel
import random
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from tokenreset import token
from io import BytesIO
app=Flask(__name__)
app.secret_key='KS@917_PATHIVADA038'
app.config['SESSION_TYPE']='filesystem'
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='admin'
app.config['MYSQL_DB']='spm'
Session(app)
mysql=MySQL(app)
excel.init_excel(app)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/home',methods=['GET','POST'])
def home():
    return render_template('home.html')
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        fid=request.form['fid']
        fname=request.form['fname']
        email=request.form['email']
        dept=request.form['dept']
        password=request.form['password']
        cursor=mysql.connection.cursor()
        cursor.execute('select fid from faculty')
        data=cursor.fetchall()
        cursor.execute('SELECT email from faculty')
        edata=cursor.fetchall()
        cursor.close()
        #print(data)
        if (fid,) in data:
            flash('User already already exists')
            return render_template('register.html')
        if (email,) in edata:
            flash('Email id already already exists')
            return render_template('register.html')
        otp=genotp()
        subject='Thanks for registering to the application'
        body=f'Use this otp to register {otp}'
        sendmail(email,subject,body)
        return render_template('otp.html',otp=otp,fid=fid,fname=fname,email=email,dept=dept,password=password)
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if session.get('user'):
        return render_template('dashboard.html')
    else:
        return redirect(url_for('login'))
@app.route('/create',methods=['GET','POST']) 
def create():
    if session.get('user'):
        if request.method=='POST':
            time=int(request.form['time'])
            sid=tokgenotp()
            url=url_for('survey_start',token=stoken(sid,time),_external=True)
            cursor=mysql.connection.cursor()
            cursor.execute('insert into survey(surveyid,url,fid) values(%s,%s,%s)',[sid,url,session.get('user')])
            mysql.connection.commit()
            return redirect(url_for('dashboard'))
        return render_template('create.html')
    else:
        return redirect(url_for('login')) 
@app.route('/survey',methods=['GET','POST']) 
def survey():
    if session.get('user'):
        return render_template('survey.html')
    
    

@app.route('/survey/<token>',methods=['GET','POST'])
def survey_start(token):
    try:
        s=Serializer(app.config['SECRET_KEY'])
        survey_dict=s.loads(token)
        sid=survey_dict['sid']
        if request.method=='POST':
            
            
            name=request.form['name']
            rollno=request.form['rollno']
            email=request.form['email']
            dept=request.form['dept']
            specailization=request.form['specialization']
            one=request.form['one']
            two=request.form['two']
            three=request.form['three']
            four=request.form['four']
            five=request.form['five']
            six=request.form['six']
            seven=request.form['seven']
            eight=request.form['eight']
            nine=request.form['nine']
            ten=request.form['ten']
            eleven=request.form['eleven']
            twelve=request.form['twelve']
            thirteen=request.form['thirteen']
            fourteen=request.form['fourteen']
            fifteen=request.form['fifteen']
            sixteen=request.form['sixteen']
            seventeen=request.form['seventeen']
            eighteen=request.form['eighteen']
            nineteen=request.form['nineteen']        
            cursor=mysql.connection.cursor()
            cursor.execute('insert into sur_data values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',[sid,name,rollno,email,dept,specailization,one,two,three,four,five,six,seven,eight,nine,ten,eleven,twelve,thirteen,fourteen,fifteen,sixteen,seventeen,eighteen,nineteen])
            mysql.connection.commit()
            return 'Survey submitted successfully'
        return render_template("survey.html")
    except Exception as e:
        print(e)
        abort(410,description='SUrvey link expired')

@app.route('/feedbackform/<token>')
def feedbackform(token):
    return 'success'
    

@app.route('/preview')
def preview():
    if session.get('user'):
        return render_template('survey.html')
    else:
        return redirect(url_for('login'))       


        

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')    

@app.route('/contactus',methods=['GET','POST'])
def contactus():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        message=request.form['message']
        cursor=mysql.connection.cursor()
        email=session.get('user')
        cursor.execute('insert into contact values(name,email,message)values(%s,%s,%s)',[name,email,message])
        mysql.commit()

        return redirect(url_for('index'))
    return render_template('contactus.html')  

       
@app.route('/login',methods=['GET','POST'])
def login():
    if session.get('user'):
        return redirect(url_for('dashboard'))
    if request.method=='POST':
        fid=request.form['fid']
        password=request.form['password']
        cursor=mysql.connection.cursor()
        cursor.execute('select count(*) from faculty where fid=%s  and password=%s',[fid,password])
        count=cursor.fetchone()[0]
        if count==0:
           
            flash('Invalid id or password')
            return render_template('login.html')
        else:
            session['user']=fid
            return redirect(url_for('dashboard'))
    return render_template('login.html')
   

@app.route('/forget',methods=['GET','POST'])
def forget():
    if request.method=='POST':
        email=request.form['email']
        cursor=mysql.connection.cursor()
        cursor.execute('select email from faculty')
        data=cursor.fetchall()
        print(data)
        if (email,) in data:
            cursor.execute('select %s from faculty',[email])
            deta=cursor.fetchone()[0]
            print(deta)
            cursor.close()
            subject=f'Reset Password for {deta}'
            body=f'Reset the password using {request.host+url_for("createpassword",token=token(email,360),_external=True)}'
            sendmail(deta,subject,body)
            flash('Reset link sent to your mail')
            '''return redirect(url_for('login'))'''
        else:
            flash('Invalid fid')
    return render_template('forget.html')
@app.route('/otp/<otp>/<fid>/<fname>/<email>/<dept>/<password>',methods=['GET','POST'])
def otp(otp,fid,fname,email,dept,password):
    if request.method=='POST':
        uotp=request.form['otp']
        if otp==uotp:
            cursor=mysql.connection.cursor()
            lst=[fid,fname,email,dept,password]
            query='insert into faculty values(%s,%s,%s,%s,%s)'
            cursor.execute(query,lst)
            mysql.connection.commit()
            cursor.close()
            flash('Details registered')
           
            return redirect(url_for('login'))
        else:
            flash('Wrong otp')
            return render_template('otp.html',otp=otp,fid=fid,fname=fname,email=email,dept=dept,password=password)
@app.route('/createpassword/<token>',methods=['GET','POST'])

def createpassword(token):
    try:
        s=Serializer(app.config['SECRET_KEY'])
        fid=s.loads(token)['user']
        if request.method=='POST':
                npass=request.form['npassword']
                cpass=request.form['cpassword']
                if npass==cpass:
                    cursor=mysql.connection.cursor()
                    cursor.execute('update faculty set password=%s where fid=%s',[npass,fid])
                    mysql.connection.commit()
                    cursor.close()
                    flash('Password reset Successfull')
                
                else:
                    flash('Password mismatch')
        return render_template('createpassword.html')
    except Exception as e:
        print(e)
        return 'Link expired try again'
    else:
        return redirect(url_for('login'))
@app.route('/logout')
def logout():
    if session.get('user'):
        session.pop('user')
        return redirect(url_for('index'))
    else:
        flash('already logged out!')
        return redirect(url_for('login'))  

@app.route('/allsurveys')
def allsurveys():
    if session.get('user'):
        cursor=mysql.connection.cursor()
        cursor.execute('SELECT * FROM survey where fid=%s',[session.get('user')])
        data=cursor.fetchall()
        return render_template('allsurveys.html',surveys=data)
    else:
        return redirect(url_for('login'))  
@app.route('/download/<sid>')
def download(sid):
    cursor=mysql.connection.cursor()
    lst=['Name','Roll no','Email','dept','1.Considering your overall experience with our college rate your ratings?',
    '2.The professors are well-trained and deliver the syllabus efficiently?',
    '3.Are you satisfied with the teaching staff and their teaching methods?',
    '4.How satisfied are you with the facilities provided by the college?',
    '5.How satisfied are you with your admission process in college?',
    '6.What are your views on the cafeteria and its hygiene and food quality?',
    '7.How satisfied are you with your admission process in college?',
    '8.Were the faculty and support staff helpful enough when you needed them?',
    '9.What are your views on the extra-curricular activities carried out in this college?',
    '10.What are your views on the cafeteria and its hygiene and food quality?',
    '11.What are the views on the sports area?',
    '12.How Professors are reliable and helpful?',
    '13.Is This college has well equipped computer access facility?',
    '14.Is it easy to gain access to the resources through the college library?',
    '15.Do you think it is a good idea for your siblings or friends to pursue their career in this college?',
    '16.Do you think college pays enough attention to the racial and ethnic biases?',
    '17.Do you think the college responds accurately to bullying cases?',
    '18.What is your overall experience with the college?',
    '19.Please feel free to give your additional inputs on your experience with this college?']
    

    cursor.execute('SELECT * from sur_data where sid=%s',[sid])
    user_data=[list(i)[1:] for i in cursor.fetchall()]
    user_data.insert(0,lst)
    print(user_data)
    return excel.make_response_from_array(user_data, "xlsx",file_name="Faculty_data")



if __name__=='__main__':
    app.run(debug=True,use_reloader=True)

   

       







           
           
       


