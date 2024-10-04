def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif','webp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def idGen(name=None):
    import uuid
    if(name):
        return name[:2].upper()+str(uuid.uuid4())[:4]
    else:
        return str(uuid.uuid4())[:6]
    db.session.commit()

#methods imported from flask module
from flask import Flask,render_template, redirect, request,url_for, flash
from werkzeug.utils import secure_filename
from flask import current_app as app
import uuid as uuid
import os

#models content imported in this file
from .models import *

@app.route('/')
def index():
    return render_template('index.html',categories=Category.query.all(),services=Service.query.all())

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        
        e=request.form.get('email')
        if(e=='iamadmin@gmail.com' and request.form.get('pass')=='123'):
            return redirect('/admin/dashboard')
        u=User.query.filter_by(email=e).first()
        p=Professional.query.filter_by(email=e).first()
        if(u and u.password==request.form.get('pass')):
            return redirect(f'/{u.id}/dashboard') 
        
        elif(p and p.password==request.form.get('pass')):
            return redirect(f'/{p.id}/professional/dashboard')
        else:
            return 'invalid email or password'
    return render_template('login.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        e=request.form.get('email')
        if(User.query.filter_by(email=e).first()):
            return 'email already exist'
        p=request.form.get('pass')
        n=request.form.get('name')
        a=request.form.get('address')
        pin=request.form.get('pin')
        phone=request.form.get('phone')
        u=User(id=idGen(n),email=e,name=n,password=p,address=a,pincode=pin,phone=phone)
        db.session.add(u)
        db.session.commit()
        user=User.query.filter_by(email=e).first()
        return redirect(f'/{user.id}/dashboard')
    return render_template('register.html')

@app.route('/proRegister',methods=['GET','POST'])
def proRegister():
    if request.method=='POST':
        e=request.form.get('email')
        if(Professional.query.filter_by(email=e).first()):
            return 'email already exist'
        p=request.form.get('pass')
        n=request.form.get('name')
        exp=request.form.get('exp')
        a=request.form.get('address')
        serv=request.form.get('serv')
        Category.query.filter_by(name=serv).first().proCount+=1
        pin=request.form.get('pin')
        phone=request.form.get('phone')
        u=Professional(id=idGen(n),email=e,name=n,password=p,address=a,pincode=pin,experience=exp,service=serv,phone=phone)
        db.session.add(u)
        db.session.commit()
        pro=Professional.query.filter_by(email=e).first()
        return redirect(f'/{pro.id}/professional/dashboard')
    return render_template('proRegister.html',categories=Category.query.all())


@app.route('/admin/dashboard')
def adminDashboard():

    return render_template('admin_dash.html',requests=Request.query.all(),services=Service.query.all(),categories=Category.query.all(),professionals=Professional.query.all())


@app.route('/<cId>/service/create', methods=['GET','POST'])
def serviceCreate(cId,serv=None):
    if request.method=='POST':
        n=request.form.get('name')
        p=request.form.get('price')
        d=request.form.get('desc')
        t=request.form.get('t_req')
        s=Service(id=idGen(n),name=n,price=p,desc=d,t_req=t,catId=cId)
        db.session.add(s)
        Category.query.get(cId).count+=1
        file=request.files["logo"]
        if(file):
            max_size = 1024 * 1024
    


            if file and allowed_file(file.filename):
                # Process the file (e.g., save it)
                if len(file.read()) > max_size:
                    flash('Image size too large!')
                else:
                    file.seek(0)
                    s.logo=file
                    dp=secure_filename(s.logo.filename)
                    logo=str(uuid.uuid1())+"_"+dp
                    s.logo.save(os.path.join(app.config['UPLOAD_FOLDER'],logo))
                    s.logo=logo
                    db.session.commit()
                    return redirect('/admin/dashboard')
            else:
                flash('Invalid image type')
        else:
            db.session.commit()
            return redirect('/admin/dashboard')
    if(serv):
        return render_template('service-create.html',service=serv)
    return render_template('service-create.html',cId=cId,category=Category.query.get(cId).name)

@app.route('/category/create', methods=['GET','POST'])
def categoryCreate(cat=None):
    if request.method=='POST':
        n=request.form.get('name')
        s=Category(id=idGen(n),name=n)
        file=request.files["logo"]
        db.session.add(s)
   
        
        if(file):
            max_size = 1024 * 1024
            if file and allowed_file(file.filename):
                # Process the file (e.g., save it)
                if len(file.read()) > max_size:
                    flash('Image size too large!')
                else:
                    file.seek(0)
                    s.logo=file
                    dp=secure_filename(s.logo.filename)
                    logo=str(uuid.uuid1())+"_"+dp
                    s.logo.save(os.path.join(app.config['UPLOAD_FOLDER'],logo))
                    s.logo=logo
                    db.session.commit()
            
                    return redirect('/admin/dashboard')
            else:
                flash('Invalid image type')
        else:
            db.session.commit()
        
            return redirect('/admin/dashboard')
    if(cat):
        return render_template('category-create.html',category=cat)
    return render_template('category-create.html')

@app.route('/<catId>/category/remove')
def categoryRemove(catId):
    db.session.delete(Category.query.get(catId))
    db.session.commit()
    return redirect('/admin/dashboard')

@app.route('/<catId>/category/modify',methods=['GET','POST'])
def categoryModify(catId):
    if request.method=='POST':
        n=request.form.get("name")
        l=request.files["logo"]
        s=Category.query.get(catId)
        if(n):
            s.name=n
        if(l):
            file=request.files["logo"]
            max_size = 1024 * 1024
            if file and allowed_file(file.filename):
                # Process the file (e.g., save it)
                if len(file.read()) > max_size:
                    flash('Image size too large!')
                else:
                    file.seek(0)
                    s.logo=file
                    dp=secure_filename(s.logo.filename)
                    logo=str(uuid.uuid1())+"_"+dp
                    s.logo.save(os.path.join(app.config['UPLOAD_FOLDER'],logo))
                    s.logo=logo
                    db.session.commit()
                    return redirect('/admin/dashboard')
            else:
                flash('Invalid image type')
        else:
            db.session.commit()
            return redirect('/admin/dashboard')
    c=Category.query.get(catId)
    return categoryCreate(c)

@app.route('/<sId>/service/modify',methods=['GET','POST'])
def serviceModify(sId):
    if request.method=='POST':
        n=request.form.get("name")
        l=request.files["logo"]
        p=request.form.get('price')
        d=request.form.get('desc')
        t=request.form.get('t_req')
        s=Service.query.get(sId)
        if(n):
            s.name=n
        if(p):
            s.price=p
        if(d):
            s.desc=d
        if(t):
            s.t_req=t
        if(l):
            file=request.files["logo"]
            max_size = 1024 * 1024

            if file and allowed_file(file.filename):
                # Process the file (e.g., save it)
                if len(file.read()) > max_size:
                    flash('Image size too large!')
                else:
                    file.seek(0)
                    s.logo=file
                    dp=secure_filename(s.logo.filename)
                    logo=str(uuid.uuid1())+"_"+dp
                    s.logo.save(os.path.join(app.config['UPLOAD_FOLDER'],logo))
                    s.logo=logo
                    db.session.commit()
                    return redirect('/admin/dashboard')
            else:
                flash('Invalid image type')
        else:
            db.session.commit()
            return redirect('/admin/dashboard')
    serv=Service.query.get(sId)
    return serviceCreate(cId=-1,serv=serv)


@app.route('/<sId>/service/remove')
def serviceRemove(sId):
    s=Service.query.get(sId)
    db.session.delete(s)
    Category.query.get(s.catId).count-=1
    db.session.commit()
    return redirect('/admin/dashboard')


@app.route('/admin/summary')
def adminSummary():
    ratings=[i.rating for i in Request.query.all() if i.rating]
    d={}
    for i in ratings:
        if i in d:
            d[i]+=1
        else:
            d[i]=1
    
    requests=Request.query.all()
    e={"Requested":0,"Accepted":0,"Closed":0,"Total":len(requests)}
    for i in requests:
        if i.status=='Accepted':
            e['Acceptee']+=1
        elif i.status=="Closed":
            e['Closed']+=1
        elif i.status=='Requested':
            e['Requested']+=1

    cat=Category.query.all()
    f={}
    for i in cat:
        f[i.name]=i.proCount
    print(f)
    return render_template('admin_sum.html',d=d,e=e,f=f)

@app.route('/<userId>/dashboard')
def userDashboard(userId):
    user=User.query.get(userId)
    r=user.requests
    s=[]
    for i in r:
        if(i.status!='Requested'):
            s.append((i,Service.query.get(i.sId),Professional.query.get(i.proId)))
        else:
            s.append((i,Service.query.get(i.sId),None))
    all=Category.query.all()
    return render_template('user_dash.html',user=user,requests=s,services=Service.query.all(),categories=all)

@app.route('/<userId>/<sId>/book')
def bookService(userId,sId):
    import datetime
    r=Request(userId=userId,sId=sId,d_req=datetime.datetime.now())
    db.session.add(r)
    db.session.commit()
    return redirect(f'/{userId}/dashboard')

@app.route('/<userId>/<rId>/cancel')
def cancelService(userId,rId):
    Request.query.get(rId).status='Cancelled'
    db.session.commit()
    return redirect(f'/{userId}/dashboard')

@app.route('/<userId>/<rId>/remove')
def removeService(userId,rId):
    db.session.delete(Request.query.get(rId))
    db.session.commit()
    return redirect(f'/{userId}/dashboard')

@app.route('/<userId>/<rId>/close',methods=['GET','POST'])
def closeService(userId,rId):
    if request.method=='POST':
        r=Request.query.get(rId)
        import datetime
        r.d_comp=datetime.datetime.now()
        r.rating=request.form.get('rating')
        r.remarks=request.form.get('remarks')
        r.status='Closed'
        db.session.commit()
        return redirect(f'/{userId}/dashboard')



@app.route('/<string:proId>/professional/dashboard')
def proDashboard(proId):
    pro=Professional.query.get(proId)
    rejectIds=[]
    if(pro.rejectIds):
        rejectIds=list(map(int,pro.rejectIds.split(' ')))
    cat=Category.query.filter_by(name=Professional.query.get(proId).service).first()
    s=cat.services
    sIds=[]
    for i in s:
        sIds.append(i.id)
    rcus=[]
    reqcus=[]
    r=Request.query.all()
    for i in r:
        if(i.sId in sIds and i.id not in rejectIds):
            if(i.status=='Requested'):
                reqcus.append((i,Service.query.get(i.sId),User.query.get(i.userId)))
            elif(i.status!='Cancelled'):
                rcus.append((i,Service.query.get(i.sId),User.query.get(i.userId)))
    return render_template('pro_dash.html',pro=pro,rcus=rcus,rejectIds=rejectIds,reqcus=reqcus)

@app.route('/<proId>/<rId>/accept')
def acceptRequest(proId,rId):
    r=Request.query.get(rId)
    r.proId=proId
    r.status="Accepted"
    db.session.commit()
    return redirect(f'/{proId}/professional/dashboard')

@app.route('/<proId>/<rId>/reject')
def rejectRequest(proId,rId):
    p=Professional.query.get(proId)
    p.rejectIds+=' '+rId;
    db.session.commit()
    return redirect(f'/{proId}/professional/dashboard')









