from flask import Flask, abort,render_template,request,redirect
from models import db,StudentModel
import sqlite3
 
app = Flask(__name__)
 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'           #here we can assign the database name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
 
@app.before_first_request
def create_table():
    db.create_all()        #it can create the table in this schema name student
 
@app.route('/create' , methods = ['GET','POST'])
def create():
    if request.method == 'GET':                #when the request is in get method then it can render the create page
        return render_template('createpage.html')
 
    if request.method == 'POST':

        hobby = request.form.getlist('hobbies')    #it is count an array
        #hobbies = ','.join(map(str, hobby))       #it is use to checkbox
        hobbies=",".join(map(str, hobby))          #Here we can convert the array into the string in the by the help of join  swparated by comma

        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        gender = request.form['gender']
        hobbies = hobbies               #hobbies variabe stored here
        country = request.form['country']


        #it is an table name  || it can the model
        students = StudentModel(          #map here with model
            first_name=first_name,        #this value became stored in the left side in the this mapping
            last_name=last_name,
            email=email,
            password=password,
            gender=gender, 
            hobbies=hobbies,
            country = country
        )
        db.session.add(students)      #here we can add the data in the database with table name students
        db.session.commit()
        db.create_all()
        return redirect('/')
 
 
@app.route('/')
def RetrieveList():
    students = StudentModel.query.all()      #selecting all queries stored here in students in datalist.html
    return render_template('datalist.html',students = students)    #here we can created a object
 
 
@app.route('/<int:id>')
def RetrieveStudent(id):
    students = StudentModel.query.filter_by(id=id).first()
    if students:
        return render_template('data.html', students = students)
        return f"Employee with id ={id} Doenst exist"
 
 
@app.route('/<int:id>/edit',methods = ['GET','POST'])
def update(id):
    student = StudentModel.query.filter_by(id=id).first()

   
    if request.method == 'POST':
        if student:
            db.session.delete(student)
            db.session.commit()
  
        hobby = request.form.getlist('hobbies')
        hobbies =  ",".join(map(str, hobby)) 
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        gender = request.form['gender']
        hobbies = hobbies 
        country = request.form['country']

        student = StudentModel(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            gender=gender, 
            hobbies=hobbies,
            country = country
        )
        db.session.add(student)
        db.session.commit()
        return redirect('/')
 
    return render_template('update.html', student = student)
 
 
@app.route('/<int:id>/delete', methods=['GET','POST'])
def delete(id):           #we will pass id
    students = StudentModel.query.filter_by(id=id).first()        #based on id it will find which data is can delete
    if request.method == 'POST':
        if students:
            db.session.delete(students)
            db.session.commit()
            return redirect('/')       #it can return datalist.html
        abort(404)
    return render_template('delete.html')      #here it can click here to delete or not
 
app.run(host='localhost', port=5000)