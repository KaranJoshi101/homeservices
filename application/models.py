from .database import db
class User(db.Model):
    id=db.Column(db.String(),primary_key=True)
    name=db.Column(db.String(),nullable=False)
    email=db.Column(db.String(),nullable=False,unique=True)
    password=db.Column(db.String(),nullable=False)
    address=db.Column(db.String())
    pincode=db.Column(db.Integer)
    phone=db.Column(db.Integer)
    requests=db.relationship('Request',backref='user')

class Professional(db.Model):
    id=db.Column(db.String(),primary_key=True)
    name=db.Column(db.String(),nullable=False)
    email=db.Column(db.String(),nullable=False,unique=True)
    password=db.Column(db.String(),nullable=False)
    service=db.Column(db.String(),nullable=False)
    experience=db.Column(db.Integer)
    doc=db.Column(db.String(120))
    address=db.Column(db.String())
    phone=db.Column(db.Integer)
    pincode=db.Column(db.Integer)
    rejectIds=db.Column(db.String(),default='')
    requests=db.relationship('Request',backref='professional')

class Service(db.Model):
    id=db.Column(db.String(),primary_key=True)
    name=db.Column(db.String(),nullable=False)
    price=db.Column(db.String(),nullable=False)
    t_req=db.Column(db.Integer)
    desc=db.Column(db.String())
    logo=db.Column(db.String(120))
    catId=db.Column(db.String(),db.ForeignKey('category.id'),nullable=False)
    requests=db.relationship('Request',backref='service')

class Category(db.Model):
    id=db.Column(db.String(),primary_key=True)
    name=db.Column(db.String(),nullable=False)
    count=db.Column(db.Integer,default=0)
    proCount=db.Column(db.Integer,default=0)
    logo=db.Column(db.String(120))
    services=db.relationship('Service',backref='category')

class Request(db.Model):
    id=db.Column(db.String(),primary_key=True)
    userId=db.Column(db.String(),db.ForeignKey('user.id'))
    proId=db.Column(db.String(),db.ForeignKey('professional.id'))
    sId=db.Column(db.String(),db.ForeignKey('service.id'))
    d_req=db.Column(db.DateTime)
    d_comp=db.Column(db.DateTime)
    status=db.Column(db.String(),default='Requested')
    rating=db.Column(db.String(3))
    remarks=db.Column(db.String())
