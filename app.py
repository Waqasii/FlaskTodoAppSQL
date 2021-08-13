from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class Todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(500),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.now())
    
    def __repr__(self) -> str:
        return f"{self.sno}  - {self.title}"

@app.route("/",methods=['GET','POST'])
def addTodo():
    if(request.method =='POST'):
        title=request.form['title']
        desc=request.form['description']
        todo=Todo(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()
        print('Add Todo')
        
    all_todo=Todo.query.all()
    return render_template('index.html',allTodo=all_todo)

@app.route("/show")
def show():
    all_todo=Todo.query.all()
    print('Show Todo')
    
    return render_template('index.html',allTodo=all_todo)

@app.route("/delete/<int:sno>")
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    print('Delete Todo')
    return redirect('/show')

@app.route("/update/<int:sno>",methods=['GET','POST'])
def update(sno):
    if(request.method=='POST'):
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title=request.form['title']
        todo.desc=request.form['description']
        db.session.add(todo)
        db.session.commit()
        print('Update Todo')
        return redirect('/show')
    else:
        print('Update Show Todo')
        todo=Todo.query.filter_by(sno=sno).first()
        return render_template('update.html',todo=todo)


if __name__== "__main__":
    # app.run(debug=True)
    app.run()