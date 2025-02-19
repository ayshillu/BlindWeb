from flask import Blueprint,render_template,request,flash,session,redirect,url_for
from database import *
public = Blueprint('public',__name__)

@public.route('/',methods=['get','post'])
def home():
	data={}
	return render_template('index.html',data=data)

@public.route('/login',methods=['get','post'])
def login():
	data={}
	if 'login' in request.form:
		username=request.form['username']
		password=request.form['password']
		q="Select * from login where username='%s' and password='%s'"%(username,password)
		# print (q)
		res=select(q)
		if res:
			session['login_id']=res[0]['login_id']

			if res[0]['usertype']=='admin':
				return redirect(url_for('admin.home'))
			if res[0]['usertype']=='caretaker':
				return redirect(url_for('caretaker.home'))

		else:
			flash('Invalid Username or Password')
	return render_template('login.html',data=data)


@public.route('/register',methods=['get','post'])
def register():
	data={}
	if 'register' in request.form:
		fname=request.form['fname']
		lname=request.form['lname']
		phone=request.form['phone']
		email=request.form['email']
		user=request.form['username']
		passs=request.form['password']

		q="insert into login(username,password,usertype) values('%s','%s','caretaker')" %(user,passs)
		s=insert(q)
		q="insert into caretaker values(null,'%s','%s','%s','%s','%s')" %(s,fname,lname,phone,email)
		insert(q)
		flash('Inserted Successfully')
		return redirect(url_for('public.login'))
	return render_template('register.html',data=data)




	