#------------------
#Modules importing:
#------------------
from flask import Flask,render_template,request,session,url_for,session,redirect
from database import * #User defined module. All dbms operation function are defined in this module
from flask_mail import *  #module user to send a message to email
import random
#-----------------------------------------------------------------------------------------------------------------------------
#------------------
#Creating an flask app instance:
#------------------
app = Flask(__name__)
app.secret_key = 'abc' #set a secret_key to flask app instance 
#-----------------------------------------------------------------------------------------------------------------------------
#------------------
#Creating an flask mail app instance:
#------------------
app.config['MAIL_SERVER']='smtp.gmail.com'  
app.config['MAIL_PORT']=465  
app.config['MAIL_USERNAME'] = 'avinashimmadisetty10@gmail.com'  
app.config['MAIL_PASSWORD'] = 'tpgwnqrhidutoqht'  
app.config['MAIL_USE_TLS'] = False  
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)  
def generateOTP():
    return random.randint(000000,999999) 

def sendOTP(email,otp):
    msg = Message('OTP',sender = 'avinashimmadisetty10@gmail.com', recipients = [email])  
    msg.body = str(otp) 
    mail.send(msg)     
#-----------------------------------------------------------------------------------------------------------------------------
#------------------
#page routings:
#------------------
@app.route('/')
def index():
    return render_template("mywebsite.html")

@app.route('/frames/<page>')
def frames(page):
    return render_template("frames/"+page+".html")
    
@app.route('/index/<page>')
def index_pages(page):
    return render_template("index/"+page+".html")
    
#-----------------------------------------------------------------------------------------------------------------------------
#------------------
#Admin page routings:
#------------------    
@app.route('/admin/<page>')
def admin(page):
    if page=='admindashboard':
        return render_template('admin/admindashboard.html',name=session['username'])
    elif page=='welcome':
        return render_template('common/welcome.html',name=session['data'][0])
    elif page=='viewprofile':
        return render_template('common/viewprofile.html',dt=session['data'])
    elif page=='newpassword':
        return render_template('common/newpassword.html')
    elif page=='admin':
        adminlist = getlist('admin')
        return render_template('admin/adminlist.html',l = adminlist,name=session['username'])
    elif page=='user':
        userlist = getlist('user')
        return render_template('admin/userlist.html',l = userlist)
    elif page=='registration':
        return render_template('admin/registration.html')
    elif page=='tourpackage':
        tourpackagelist = getlist('tourpackage')
        return render_template('common/tourpackagelist.html',l = tourpackagelist,role='admin')
    elif page=='packagecreation':
        return render_template('admin/create_tourpackage.html')
    elif page=='Paymenthistory':
        updatestatus()
        return render_template('common/payment_history_page.html',l = getpaymenthistory())
    elif page=='issue':
        i = getissue()
        return render_template('user/issue.html',l = i,role='admin')
#-----------------------------------------------------------------------------------------------------------------------------    
#------------------
#User page routings:
#------------------    
@app.route('/user/<page>')
def user(page):
    if page=='userdashboard':
        return render_template('user/userdashboard.html')
    elif page=='welcome':
        return render_template('common/welcome.html',name=session['data'][0])
    elif page=='viewprofile':
        return render_template('common/viewprofile.html',dt=session['data'])
    elif page=='newpassword':
        return render_template('common/newpassword.html')
    elif page=='registration':
        return render_template('user/registration.html')
    elif page=='tourpackage':
        tourpackagelist = getlist('tourpackage')
        return render_template('common/tourpackagelist.html',l = tourpackagelist,role='user')
    elif page=='Paymenthistory':
        updatestatus()
        return render_template('common/payment_history_page.html',l = getpaymenthistory(session['username']))    
    elif page=='issue':
        i = getissue(session['username'])
        return render_template('user/issue.html',l = i,role='user')    
#-----------------------------------------------------------------------------------------------------------------------------    
#------------------
#login and logout operations:
#------------------        
@app.route('/login/<page>')
def login(page):
    if 'username' in session:
        if session['role'] == 'admin':
            return render_template("admin/adminsite.html")
        else:
            return render_template("user/usersite.html")
    return render_template("index/"+page+"login.html")

@app.route('/validate/<role>',methods=['POST'])
def validate(role):
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        if isvalidate(username,password,role):
            session['username'] = username
            session['data'] = getdata(username,role)
            session['role'] = role
            return render_template(role+"/"+role+"site.html")
        return render_template("index/"+role+"login.html")    
 
@app.route('/logout')
def logout():
    session.pop('username',None)
    session.pop('data',None)
    role = session['role']
    session.pop('role',None)
    return render_template("index/"+role+"login.html")
#-----------------------------------------------------------------------------------------------------------------------------
#------------------
#create new profile or update profile operations:
#------------------
@app.route('/create/<role>',methods=['POST'])
def createprofile(role):
    if request.method=='POST':
        data = request.form
        createprofile_function(role,data)
        if 'username' in session:
            list1 = getlist(role)
            return render_template(session['role']+"/"+role+"list.html",l = list1,name=session['username'])
        return render_template("index/"+role+"login.html")
        
@app.route('/updateprofile')
def updateprofile():
    return render_template('common/updateprofile.html',dt=session['data'])

@app.route('/update/<username>',methods=['POST'])
def update(username):
    if request.method=='POST':
        data = request.form
        updateprofile_function(username,data)
        if username == session['data'][4]:
            if session['role'] == 'admin':
                session['data'] = getdata(session['username'],'admin')
            else:
                session['data'] = getdata(username,'user')
            return render_template('common/viewprofile.html',dt=session['data'])
        else:
            if getrole(username) == 'admin':
                list1 = getlist('admin')
                return render_template("admin/adminlist.html",l = list1)
            else:
                list1 = getlist('user')
                return render_template("admin/userlist.html",l = list1)
#-----------------------------------------------------------------------------------------------------------------------------
#------------------
#forget password or update password operations:
#------------------
@app.route("/forgetpassword/<role>")
def forgetpassword(role):
    return render_template(role+'/forgetpassword.html')

@app.route('/check/<role>',methods=['POST'])
def check(role):
    if request.method=='POST':
        mailid = request.form['mailid']
        if isvalidmail(mailid,role):
            session['mail_id'] = mailid
            session['role'] = role
            session['otp'] = generateOTP()
            sendOTP(mailid,session['otp'])
            return render_template("otpverifypage.html",email=mailid)
        return render_template(role+'/forgetpassword.html')

@app.route('/otpcheck',methods=['POST'])
def otpcheck():
    if request.method=='POST':
        otp = int(request.form['otp'])
        if otp==session['otp']:
            session.pop('otp',None)
            return render_template("forgetpassword1.html")
        return render_template("otpverifypage.html",email=session['mail_id'])    

@app.route('/forgetpassword1',methods=['POST'])
def forgetpassword1():
    if request.method=='POST':
        newpassword = request.form['newpassword']
        conformpassword = request.form['conformpassword']
        if newpassword == conformpassword:
            updatepwd1(session['mail_id'],newpassword,session['role'])
            session.pop('mail_id',None)
            role = session['role']
            session.pop('role',None)
            return render_template("index/"+role+"login.html")
        return render_template("forgetpassword1.html")
    
@app.route('/updatepassword',methods=['POST'])
def updatepassword():
    if request.method=='POST':
        currentpassword = request.form['currentpassword']
        newpassword = request.form['newpassword']
        conformpassword = request.form['newpassword']
        if newpassword == conformpassword:
            if updatepwd(session['username'],currentpassword,newpassword,session['role']):
                return render_template('common/welcome.html',name=session['data'][0])
            return render_template("common/newpassword.html")    
        return render_template("common/newpassword.html")
#-----------------------------------------------------------------------------------------------------------------------------
#------------------
#edit or delete profile(admin/login) operations by admin:
#------------------
@app.route('/deleteuser/<mail_id>')
def delete(mail_id):
    delete_account(mail_id)
    list1 = getlist('user')
    return render_template("admin/userlist.html",l = list1)

@app.route('/edituser/<mail_id>')
def edit(mail_id):
    return render_template('common/updateprofile.html',dt=getdata(mail_id,'user'))

@app.route('/editadmin/<mail_id>')
def edit1(mail_id):
    return render_template('common/updateprofile.html',dt=getdata(mail_id,'admin0'))
#-----------------------------------------------------------------------------------------------------------------------------
#------------------
#Tour Package view page:
#------------------
@app.route('/view_tour_package/<pkid>')
def view_tour_package(pkid):
    pkid = getdetails(pkid)
    return render_template('common/packagepage.html',dt=pkid,role=session['role'])

@app.route('/create_tour_package',methods=['POST'])
def create_tour_package():
    if request.method=='POST':
        data = request.form
        createtourpackage(data)
        tourpackagelist = getlist('tourpackage')
        return render_template('common/tourpackagelist.html',l = tourpackagelist,role='admin')

@app.route('/edit_tour_package/<pkid>')
def edit_tour_package(pkid):
    pkid = getdetails(pkid)
    return render_template('admin/update_tourpackage.html',dt=pkid)

@app.route('/update_tour_package/<pkid>',methods=['POST'])
def update_tour_package(pkid):
    if request.method=='POST':
        data = request.form
        updatetourpackage(pkid,data)
        tourpackagelist = getlist('tourpackage')
        return render_template('common/tourpackagelist.html',l = tourpackagelist,role='admin')
#-----------------------------------------------------------------------------------------------------------------------------
#------------------
#Payment page:
#------------------
@app.route('/payment/<pkid>',methods=['GET'])
def payment(pkid):
    if request.method=='GET':
        pkid = getdetails(pkid)
        return render_template('user/paymentpage.html',package = pkid,data = session['data'])
        
@app.route('/pay/<pkid>',methods=['POST'])
def pay(pkid):
    if request.method=='POST':
        fromdate = request.form['fromdate']
        todate = request.form['todate']
        payid = makepayment(session['username'],pkid,fromdate,todate,'active')
        updatestatus()
        payid = getpayment_history(str(payid))
        pkid = getpackagename(payid[0][2])
        return render_template('common/invoice.html',payid = payid[0][0],status = payid[0][5],username = payid[0][1],fromdate=payid[0][3],todate=payid[0][4],packagename = pkid[0],price=pkid[1])
        
@app.route('/cancel_tour_payment/<payid>')
def cancel_tour_payment(payid):
    cancel_tour(payid)
    updatestatus()
    if session['username'][:5] == 'admin':
        return render_template('common/payment_history_page.html',l = getpaymenthistory())
    else:
        return render_template('common/payment_history_page.html',l = getpaymenthistory(session['username']))    

@app.route('/edit_tour_payment/<payid>')
def edit_tour_payment(payid):
    payid = getpayment_history(payid)
    updatestatus()
    pkid = getdetails(str(payid[0][2]))
    return render_template('common/update_payment_history.html',payid = payid[0][0],dt = pkid,fromdate=payid[0][3],todate=payid[0][4] )    


@app.route('/update_pay/<payid>',methods=['POST'])
def update_pay(payid):
    if request.method=='POST':
        fromdate = request.form['fromdate']
        todate = request.form['todate']
        update_payment(payid,fromdate,todate)
        if session['role'] == 'admin':
            updatestatus()
            return render_template('common/payment_history_page.html',l = getpaymenthistory())
        else:
            updatestatus()
            return render_template('common/payment_history_page.html',l = getpaymenthistory(session['username']))
 
@app.route('/invoice/<payid>')
def invoice(payid):
        updatestatus()
        payid = getpayment_history(payid)
        pkid = getpackagename(payid[0][2])
        return render_template('common/invoice.html',payid = payid[0][0],status = payid[0][5],username = payid[0][1],fromdate=payid[0][3],todate=payid[0][4],packagename = pkid[0],price=pkid[1])
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#Issue raise page:
#-----------------------------------------------------------------------------------------------------------------------------
@app.route('/issue_raise',methods=['POST'])
def issue_raise():
    if request.method=='POST':
        issue_on = request.form['issue_on']
        updateissue_table(session['username'],issue_on)
        i = getissue(session['username'])
        return render_template('user/issue.html',l = i,role='user')
#-----------------------------------------------------------------------------------------------------------------------------
if __name__=='__main__':
    app.run(debug=True)