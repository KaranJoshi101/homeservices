#import flask module
from flask import Flask
from application.database import db
#create flask object
app=None
def create_app():
    app=Flask(__name__) #__name__ gives file and we encapsulate with flask
    app.debug=True
    
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///wvote.sqlite3'
    UPLOAD_FOLDER='C:\Documents\mad1_proj\homeservices\static\images'
    app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
    app.config['SECRET_KEY']="this is my secret key"
    db.init_app(app)
 
    app.app_context().push() #not very clear about this as of now but it kind of tells the 
    return app
    
app=create_app()
from application.controllers import * #imports endpoints from controllers.py

if __name__=='__main__':
    app.run(debug=True) #runs the flask object with debug on so that every change reflects on server automatically