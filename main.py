from flask import Flask

app = Flask(__name__)

app.secret_key='pearl_ready'

from public import public 
app.register_blueprint(public)

from admin import admin
app.register_blueprint(admin,url_prefix='/admin')

from caretaker import caretaker
app.register_blueprint(caretaker,url_prefix='/caretaker')




app.run(debug=True,port=5059,host="0.0.0.0")
