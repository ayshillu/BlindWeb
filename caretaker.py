from flask import flash,Blueprint,redirect,url_for,render_template,session,request
from database import *
import uuid
# from core import *
import os

caretaker=Blueprint('caretaker',__name__)

@caretaker.route('/home',methods=['get','post'])
def home():
	data={}
	return render_template('caretaker.html',data=data)

@caretaker.route('/blind',methods=['get','post'])
def blind():
	data={}
	lid=session['login_id']
	if 'action' in request.args:
		action=request.args['action']
		id=request.args['id']
	else:
		action=None

	if action=="delete":
		q="delete from blind where blind_id='%s'" %(id)
		delete(q)
		return redirect(url_for('caretaker.blind'))

	if action=="trackrequest":
		q="select * from track where blind_id='%s'" %(id)
		res=select(q)
		if res:
			flash("Already Requested")
		else:
			q="insert into track values(null,'%s')" %(id)
			insert(q)
			flash("Request Send To Admin")
		return redirect(url_for('caretaker.blind'))

	if 'register' in request.form:
		fname=request.form['fname']
		lname=request.form['lname']
		phone=request.form['phone']
		imei=request.form['imei']
		types=request.form['type']
		# user=request.form['username']
		# passs=request.form['password']

		# q="insert into login(username,password,usertype) values('%s','%s','blind')" %(user,passs)
		# s=insert(q)
		q="insert into blind values(null,'0',(select caretaker_id from caretaker where login_id='%s'),'%s','%s','%s','%s','%s')" %(lid,fname,lname,phone,imei,types)
		bid=insert(q)
		q="insert into location values(null,'%s','0','0',curdate())" %(bid)
		insert(q)
		flash('Inserted Successfully')
		return redirect(url_for('caretaker.blind'))
	q="select *,concat(first_name,' ',last_name)as name from blind inner join location using(blind_id) where caretaker_id=(select caretaker_id from caretaker where login_id='%s')" %(lid)
	res=select(q)
	data['blind']=res
	return render_template('blindregister.html',data=data)
	
@caretaker.route('/emergency', methods=['GET', 'POST'])
def emergency():
	data = {}
	lid = session['login_id']

	# Query to get the blind individuals associated with the caretaker
	q = "SELECT *, CONCAT(first_name, ' ', last_name) AS Name FROM blind WHERE caretaker_id = (SELECT caretaker_id FROM caretaker WHERE login_id='%s')" % (lid)
	print(q)
	res = select(q)
	print(res)
	data['viewblind'] = res

	# Check if any blind individuals are found
	if not res:
		flash('No blind individuals found for this caretaker.')
		return redirect(url_for('caretaker.home'))  # Redirect to the home page (update 'home' to the actual endpoint)

	ids = res[0]['blind_id']

	# Query to get the emergency contacts associated with the blind individuals
	q = "SELECT * FROM emergency WHERE blind_id IN (SELECT blind_id FROM blind WHERE caretaker_id = (SELECT caretaker_id FROM caretaker WHERE login_id='%s'))" % (ids)
	res = select(q)

	# Check if any emergency contacts are found
	if not res:
		flash('No emergency contacts yet.')
		return redirect(url_for('caretaker.home'))  # Redirect to the home page (update 'home' to the actual endpoint)

	data['blind'] = res

	# Handle action if specified
	if 'action' in request.args:
		action = request.args['action']
		id = request.args['id']
	else:
		action = None

	if action == "delete":
		q = "DELETE FROM emergency WHERE emergency_id='%s'" % (id)
		delete(q)
		return redirect(url_for('caretaker.emergency'))

	if 'register' in request.form:
		name = request.form['bname']
		print(name)
		names = request.form['name']
		phone = request.form['phone']
		relation = request.form['relation']
		image1 = request.files['image1']

		q = "INSERT INTO emergency VALUES (NULL, '%s', '%s', '%s', '%s','')" % (name, phone, names, relation)
		id1 = insert(q)

		pid = str(id1)

		isFile = os.path.isdir(r"static/trainimages/" + pid)  
		print(isFile)

		if not isFile:
			os.mkdir(r'static/trainimages/' + pid)

		path1 = "static/trainimages/" + pid + "/imag1.jpg"
		image1.save(path1)

		image2 = request.files['image2']
		path2 = "static/trainimages/" + pid + "/imag2.jpg"
		image2.save(path2)

		image3 = request.files['image3']
		path3 = "static/trainimages/" + pid + "/imag3.jpg"
		image3.save(path3)

		q = "UPDATE emergency SET image='%s' WHERE emergency_id='%s'" % (path1, pid)
		update(q)

		# enf(r"static/trainimages/")

		flash('Inserted Successfully')
		return redirect(url_for('caretaker.emergency'))

	return render_template('manageemergency.html', data=data)



@caretaker.route('/helprequest',methods=['get','post'])
def helprequest():
	data={}
	q="select * from helprequest inner join blind using(blind_id) "
	res=select(q)
	data['viewcomplaints']=res
	j=0
	for i in range(1,len(res)+1):
		if 'submit'+str(i) in request.form:
			reply=request.form['reply'+str(i)]
			print(res[j]['request_id'])

			q="update helprequest set reply_message='%s',status='reply' where request_id='%s'"%(reply,res[j]['request_id'])
			update(q)
			flash("message send successfully")
			return redirect(url_for('caretaker.helprequest'))
		j=j+1

	return render_template('message.html',data=data)

@caretaker.route('/send_comp',methods=['post','get'])
def send_comp():
	data={}
	if 'action' in request.args:
		action=request.args['action']
		id=request.args['id']
	else:
		action=None
	if action=='delete':
		t="delete from complaint where complaint_id='%s'"%(id)
		delete(t)
		flash("Deleted Successfully")
		return redirect(url_for('caretaker.send_comp'))


	if 'comp' in request.form:
		comp=request.form['comp']
		i="insert into complaint values(null,'%s','%s','pending',curdate())"%(session['login_id'],comp)
		insert(i)
		flash("Sent Successfully")
		return redirect(url_for('caretaker.send_comp'))
	t="select * from complaint where caretaker_id='%s'"%(session['login_id'])
	data['view']=select(t)

	return render_template('caretaker_send_comp.html',data=data)
@caretaker.route('/caretaker_pro_update',methods=['get','post'])
def caretaker_pro_update():
	data={}
	t="select * from caretaker inner join login using(login_id) where login_id='%s'"%(session['login_id'])
	data['up']=select(t)
	if 'register' in request.form:
		fname=request.form['fname']
		lname=request.form['lname']
		phone=request.form['phone']
		email=request.form['email']
		user=request.form['username']
		passs=request.form['password']
		id=request.form['login_id']
		i="update caretaker set first_name='%s',last_name='%s',phone='%s',email='%s' where login_id='%s'"%(fname,lname,phone,email,id)
		update(i)
		up="update login set username='%s',password='%s' where login_id='%s'"%(user,passs,id)
		update(up)
		flash("profile Updated successfully")
		return redirect(url_for('public.login'))
	return render_template('caretaker_proupdate.html',data=data)
@caretaker.route('/logout',methods=['get','post'])
def logout():
	data={}
	return redirect(url_for('public.login'))