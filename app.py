from flask import Flask, render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/parameters'
app.config['SQLALCHEMY_ECHO'] = True 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

class UPS(db.Model):
       # __table__ == 'UPS'
	id = db.Column(db.Integer, primary_key=True)
	ip = db.Column(db.String(64), nullable=False)
	community = db.Column(db.String(64), nullable=False)
	version = db.Column(db.String(64), nullable=False)
	time_of_probe = db.Column(db.Time(64), nullable=False)
	rem_time = db.Column(db.Time(64), nullable=False)
	nex_probe = db.Column(db.Time(64), nullable=False)
	out_power = db.Column(db.Integer, nullable=False)
	out_stat = db.Column(db.String(64), nullable=False)
	
	def __init__(self, ip, version, community):
		self.ip = ip
		self.version=version
		self.community=community



@app.route('/', methods=['GET','POST'])

def home():
	if request.method == 'POST':
		if not request.form['ip'] or not request.form['version'] or not request.form['community']:
			flash('Please enter all the fields', 'error')
		else:
			entry =  UPS(ip = request.form.get("ip"), version = request.form.get("version"), community = request.form.get("community"))
                	db.session.add(entry)
			db.session.commit()
         		flash('entry successful')
        entries = UPS.query.all()
        return render_template("home.html", entries=entries)

@app.route('/edit', methods = ['POST'])
def edit():
	if request.method == 'POST':
		try:
			
			oldid = request.form.get("oldid")
			
			newip = request.form.get("newip")
			oldip = request.form.get("oldip")
			
			
			newversion = request.form.get("newversion")
                        oldversion = request.form.get("oldversion")
			#if newip != oldip and newversion!=oldversion:
							
#oldversion = request.form.get("oldversion") 
			
			newcommunity = request.form.get("newcommunity")
                        oldcommunity = request.form.get("oldcommunity") 
			#entry = UPS.query.filter_by(community=oldcommunity).update(dict(community=newcommunity))
			#def update_table(session, ID, ip, version, community):
			#ids = request.form.get("change")		
	
			#entry = UPS.query.filter_by(id=ids).update(dict(ip=newip))
			#UPS.ip = newip			
			#db.session.commit()
			#entry = UPS.query.filter_by(version=oldversion).update(dict(version=newversion))
			#db.session.commit()

			#entry = UPS.query.filter_by(community=oldcommunity).update(dict(community=newcommunity))
			#db.session.commit()
			change= UPS.query.filter_by(id=oldid).first()
                        
			change.ip = newip

			change.version = newversion
			change.community = newcommunity
			#UPS.version = newversion
			db.session.commit()
			return redirect("/")
		except Exception as e:
			print("Couldn't update")
			print e
		return 'Ok'

@app.route('/delete' , methods = ['POST'])

def delete():
	if request.method == 'POST':
		try:
			ip = request.form.get("ip")
			entry = UPS.query.filter_by(ip=ip).first()
			db.session.delete(entry)
			db.session.commit()
			return redirect("/")
		except Exception as e:
			print("Couldnt delete")
			print e
	return 'Yes'


if __name__ == "__main__":
	db.create_all()
	app.run(debug=True)
