from flask import render_template,redirect,request,flash,Blueprint,url_for
from database import *

admin=Blueprint('admin',__name__)

@admin.route('/home',methods=['get','poast'])
def home():
	data={}
	return render_template('admin_home.html',data=data)


@admin.route('/viewblind',methods=['get','post'])
def viewblind():
	data={}
	q="select *,concat(blind.first_name,' ',blind.last_name)as bname,concat(caretaker.first_name,' ',caretaker.last_name)as cname from blind inner join caretaker using(caretaker_id) inner join location using(blind_id)"
	res=select(q)
	data['blind']=res
	return render_template('adminviewblind.html',data=data)

@admin.route('/viewcaretaker',methods=['get','post'])
def viewcaretaker():
	data={}
	q="select * from caretaker"
	res=select(q)
	data['blind']=res
	return render_template('admin_view_caretaker.html',data=data)


@admin.route('/trackrequest',methods=['get','post'])
def trackrequest():
	data={}
	q="select *,concat(blind.first_name,' ',blind.last_name)as bname,concat(caretaker.first_name,' ',caretaker.last_name)as cname from blind inner join caretaker using(caretaker_id) inner join location on blind.blind_id=location.blind_id inner join track on blind.blind_id=track.blind_id "
	res=select(q)
	data['blind']=res
	return render_template('adminviewtrackrequest.html',data=data)
@admin.route('/view_comp',methods=['get','post'])
def view_comp():
	data={}
	u="select * from complaint inner join caretaker on complaint.caretaker_id=caretaker.login_id"
	data['view']=select(u)
	res=data['view']
	j=0
	for i in range(1,len(res)+1):
		if 'submit'+str(i) in request.form:
			reply=request.form['reply'+str(i)]
			print(res[j]['complaint_id'])

			q="update complaint set reply='%s' where complaint_id='%s'"%(reply,res[j]['complaint_id'])
			update(q)
			flash("message send successfully")
			return redirect(url_for('admin.view_comp'))
		j=j+1
	
	return render_template('admin_view_comp.html',data=data)
@admin.route('/logout',methods=['get','post'])
def logout():
	data={}
	return redirect(url_for('public.login'))