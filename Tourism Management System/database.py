#------------------
#Modules importing:
#------------------
import mysql.connector
#-----------------------------------------------------------------------------------------------------------------------------
#------------------
#Establish connection between dabatase and application:
#------------------
mydb = mysql.connector.connect(
    host = 'localhost',
    username = 'root',
    password = 'Avinash@123',
    database = 'tms')

mycursor = mydb.cursor()#creating a cursor to my database to execute the sql statments.
#-----------------------------------------------------------------------------------------------------------------------------
#------------------
#isvalidate method
#The defined function validate login userid, password is correct or not:
#------------------ 
def isvalidate(username,password,role):
    if role=='admin':
        mycursor.execute("select password from admin where id='"+username+"'")
    else:
        mycursor.execute("select password from user where id='"+username+"'")
    pwd = mycursor.fetchall()
    if pwd:
        return password==pwd[0][0]
    return 0
#-----------------------------------------------------------------------------------------------------------------------------
#------------------
#createprofile method
#The defined function create new account:
#------------------ 
def createprofile_function(role,data):
    mycursor.execute("insert into person(name,gender,date_of_birth,phone_number,mail_id) values(%s,%s,%s,%s,%s)",
    (data['name'],data['gender'],data['date_of_birth'],data['phone_number'],data['mail_id']))
    if role=='admin':
        mycursor.execute("select count(*) from admin")
        i = str(int(mycursor.fetchall()[0][0])+1)
        mycursor.execute("insert into admin(id,password,mail_id) values(%s,%s,%s)",
        ('admin'+i,'Test@123',data['mail_id']))
    else:
        mycursor.execute("insert into user(id,password) values(%s,%s)",(data['mail_id'],'Test@123'))
    mydb.commit()        
#-----------------------------------------------------------------------------------------------------------------------------
#------------------
#updateprofile method
#The defined function udpate account:
#------------------ 
def updateprofile_function(username,data):
    mycursor.execute("update person set name='"+data['name']+"',gender='"+data['gender']+"',date_of_birth='"+data['date_of_birth']+"',phone_number='"+data['phone_number']+"' where mail_id='"+username+"'")
    mydb.commit()
#-----------------------------------------------------------------------------------------------------------------------------
#------------------
#updatepwd method
#The defined function update current password:
#------------------ 
def updatepwd(username,currentpassword,newpassword,role):
    mycursor.execute("select password from "+role+" where id='"+username+"'")
    pwd = mycursor.fetchall()[0][0]
    if pwd == currentpassword:
        mycursor.execute("update "+role+" set password='"+newpassword+"' where id='"+username+"'")
        mydb.commit()
        return 1
    return 0

def updatepwd1(username,newpassword,role):
    if role=='admin':
        mycursor.execute("update "+role+" set password='"+newpassword+"' where mail_id='"+username+"'")
    elif role=='user':
        mycursor.execute("update "+role+" set password='"+newpassword+"' where id='"+username+"'")
    mydb.commit()   
#-----------------------------------------------------------------------------------------------------------------------------
#------------------
#getdata method
#The defined function return the complete personal data of the login person:
#------------------
def getdata(username,role):
    if role=='admin':
        mycursor.execute("select mail_id from admin where id='"+username+"'")
        mail_id = mycursor.fetchall()[0][0]
        mycursor.execute("select * from person where mail_id='"+mail_id+"'")
    elif role=='admin0':
        mycursor.execute("select * from person where mail_id='"+username+"'")
    else:
        mycursor.execute("select * from person where mail_id='"+username+"'")
    return mycursor.fetchall()[0]
#-----------------------------------------------------------------------------------------------------------------------------        
#------------------
#iscorrect method
#The defined function validate login userid, mail correct or not:
#------------------
def isvalidmail(mailid,role):
    if role=='admin':
        mycursor.execute("select mail_id from "+role+" where mail_id='"+mailid+"'")
    else:
        mycursor.execute("select id from "+role+" where id='"+mailid+"'")
    if mycursor.fetchall():
        return 1
    return 0
#-----------------------------------------------------------------------------------------------------------------------------        
#------------------
#get role
#The defined return the role:
#------------------
def getrole(mail_id):
    mycursor.execute("select * from admin where mail_id='"+mail_id+"'")
    if mycursor.fetchall():
        return 'admin'
    return 'user'
#-----------------------------------------------------------------------------------------------------------------------------        
#------------------
#Profile list
#The defined function return the profiles:
#------------------
def getlist(role):
    if role=='admin':
        mycursor.execute("select p.name,p.gender,p.date_of_birth,p.phone_number,p.mail_id from person p,admin a where p.mail_id=a.mail_id")
    elif role=='user':
        mycursor.execute("select p.name,p.gender,p.date_of_birth,p.phone_number,p.mail_id from person p,user u where p.mail_id=u.id")
    elif role=='tourpackage':
        mycursor.execute("select * from tourpackage")
    result = mycursor.fetchall()
    return result
#-----------------------------------------------------------------------------------------------------------------------------            
#------------------
#delete account list
#The defined function delete account:
#------------------
def delete_account(mail_id):
    mycursor.execute("delete from user where id='"+mail_id+"'")
    mycursor.execute("delete from person where mail_id='"+mail_id+"'")
    mydb.commit()
#-----------------------------------------------------------------------------------------------------------------------------
#------------------
#get details:
#The defined function return package details:
#------------------
def getdetails(pkid):
    mycursor.execute("select * from tourpackage where pkid='"+pkid+"'")
    return mycursor.fetchall()[0]
#-----------------------------------------------------------------------------------------------------------------------------            
#------------------
#createtourpackage function
#This function create a new tour package:
#------------------
def createtourpackage(data):
    mycursor.execute("select * from tourpackage")
    i = str(len(mycursor.fetchall())+1)
    mycursor.execute("insert into tourpackage(pkid,pkname,pktype,pklocation,pkprice,pkfetures,pkdetails,pkimage) values(%s,%s,%s,%s,%s,%s,%s,%s)",
    (i,data['pkname'],data['pktype'],data['pklocation'],data['pkprice'],data['pkfetures'],data['pkdetails'],data['pkimage']))
    mydb.commit()
#-----------------------------------------------------------------------------------------------------------------------------
#updatetourpackage function
#This function update tour package:
#------------------
def updatetourpackage(pkid,data):
    mycursor.execute("update tourpackage set pkname='"+data['pkname']+"',pktype='"+data['pktype']+"',pklocation='"+data['pklocation']+"',pkprice='"+data['pkprice']+"',pkfetures='"+data['pkfetures']+"',pkdetails='"+data['pkdetails']+"',pkimage='"+data['pkimage']+"' where pkid='"+pkid+"'")
    mydb.commit()
#-----------------------------------------------------------------------------------------------------------------------------                        
#-----------------------------------------------------------------------------------------------------------------------------
#Saving Paymnet details in Payment details:
#------------------
def makepayment(user_id,pkid,FromDate,ToDate,status):
    mycursor.execute("insert into payment(user_id,pkid,FromDate,ToDate,status) values(%s,%s,%s,%s,%s)",
    (user_id,pkid,FromDate,ToDate,status))
    mydb.commit()
    mycursor.execute("select payid from payment where FromDate='"+FromDate+"' and ToDate='"+ToDate+"'")
    return mycursor.fetchall()[0][0]
#-----------------------------------------------------------------------------------------------------------------------------                        
#-----------------------------------------------------------------------------------------------------------------------------
#This function return Payments history:
#------------------
def getpaymenthistory(username=None):
    if username:
        mycursor.execute("select payid,user_id,pkid,Booked_on,FromDate,ToDate,status from payment where user_id='"+username+"'")
    else:    
        mycursor.execute("select payid,user_id,pkid,Booked_on,FromDate,ToDate,status from payment")
        
    return mycursor.fetchall()
    
def getpayment_history(payid):
    mycursor.execute("select * from payment where payid='"+payid+"'")
    return mycursor.fetchall()    
#-----------------------------------------------------------------------------------------------------------------------------                        
#-----------------------------------------------------------------------------------------------------------------------------
#This function Cancel the tour payment history:
#------------------
def cancel_tour(payid):
    mycursor.execute("update payment set status='cancelled' where payid='"+payid+"'")
    mydb.commit()

def update_payment(payid,fromdate,todate):
    mycursor.execute("update payment set FromDate='"+fromdate+"',ToDate='"+todate+"' where payid='"+payid+"'")
    mydb.commit()    
#----------------------------------------------------------------------------------------------------------------------------- 
#update payment status everytime:
#----------------------------------------------------------------------------------------------------------------------------- 
def updatestatus():
    mycursor.execute("select payid,datediff(date(current_date()),FromDate),status from payment")
    l = mycursor.fetchall()
    for i in l:
        if i[2]!='cancelled':
            if i[1]>=-3 and i[1]<0:
                mycursor.execute("update payment set status='pending' where payid='"+str(i[0])+"'")
            elif i[1]<-3 and i[1]>=-7:
                mycursor.execute("update payment set status='process' where payid='"+str(i[0])+"'")    
            elif i[1]<=-7:
                mycursor.execute("update payment set status='active' where payid='"+str(i[0])+"'")
            elif i[1]>0:
                mycursor.execute("update payment set status='completed' where payid='"+str(i[0])+"'")
#------------------------------------------------------------------------------------------------------------------------------
def getpackagename(pkid):
    mycursor.execute("select pkname,pkprice from tourpackage where pkid='"+str(pkid)+"'")
    return mycursor.fetchall()[0]
#-------------------------------------------------------------------------------------------------------------------------------                
#------------------------------------------------------------------------------------------------------------------------------
def getissue(username=None):
    if username:
        mycursor.execute("select id,username,issue_on,raised_on from issue where username='"+username+"'")
    else:
        mycursor.execute("select * from issue")
    return mycursor.fetchall()
#-------------------------------------------------------------------------------------------------------------------------------
def updateissue_table(username,issue_on):
    mycursor.execute("insert into issue(username,issue_on) values(%s,%s)",(username,issue_on));
    mydb.commit()
#-------------------------------------------------------------------------------------------------------------------------------                
'''data = {
        'role':'user',
        'name':'dummy',
        'age':'20',
        'gender':'male',
        'date_of_birth':'2002-05-10',
        'phone_number':'9876543210',
        'mail_id':'dummy@gmail.com',
        'address':'dummy address'}
        
'''
