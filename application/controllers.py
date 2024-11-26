def idGen(n):
    import uuid
    return n+str(uuid.uuid4())[:5]
 

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'pdf','doc'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#methods imported from flask module
from flask import Flask,render_template, redirect, request,url_for, flash
from werkzeug.utils import secure_filename
from flask import current_app as app
import uuid as uuid
import os

#models content imported in this file
from .models import *


#home page
@app.route('/')
def index():
    return render_template('index.html',categories=Category.query.all(),services=Service.query.all())

#login page
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
            flash('invalid email or password')
    return render_template('login.html')

#register page
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
        u=User(id=idGen('US'),email=e,name=n,password=p,address=a,pincode=pin,phone=phone)
        db.session.add(u)
        db.session.commit()
        user=User.query.filter_by(email=e).first()
        return redirect(f'/{user.id}/dashboard')
    return render_template('register.html')

#professional register page
@app.route('/proRegister',methods=['GET','POST'])
def proRegister():
    if request.method=='POST':
        e=request.form.get('email')
        if(Professional.query.filter_by(email=e).first()):
            flash('email already exist')
        p=request.form.get('pass')
        n=request.form.get('name')
        exp=request.form.get('exp')
        a=request.form.get('address')
        catId=request.form.get('catId')
        print(catId)
        
        pin=request.form.get('pin')
        phone=request.form.get('phone')
        u=Professional(id=idGen('PR'),email=e,name=n,password=p,address=a,pincode=pin,experience=exp,catId=catId,phone=phone)
        db.session.add(u)
        file=request.files["file"]
        
        max_size = 10*1024 * 1024
    

        if allowed_file(file.filename):
                # Process the file (e.g., save it)
            if len(file.read()) > max_size:
                flash('File size too large!')
            else:
                file.seek(0)
                u.doc=file
                dp=secure_filename(u.doc.filename)
                doc=str(uuid.uuid1())+"_"+dp
                u.doc.save(os.path.join(app.config['UPLOAD_FOLDER'],doc))
                u.doc=doc
                db.session.commit()
                return redirect(f'/{u.id}/professional/dashboard')
        else:
            flash('Invalid file type')
    return render_template('proRegister.html',categories=Category.query.all())

"""ADMIN FUNCTIONALITIES"""
#admin dashboard
@app.route('/admin/dashboard')
def adminDashboard():
    pros=Professional.query.all()
    professionals=[]
    newpros=[]
    for i in pros:
        if( i.approval==0 ):
            newpros.append(i)
            
        else:
            professionals.append(i)
    return render_template('admin_dash.html' ,newpros=newpros,customers=User.query.all(),requests=Request.query.all(),services=Service.query.all(),categories=Category.query.all(),professionals=professionals)

#admin approves professional
@app.route('/<proId>/professional/approve')
def proApprove(proId):
    pro=Professional.query.get(proId)
    pro.approval=1
    cat=Category.query.get(pro.catId)
    cat.proCount+=1
    db.session.commit()
    return redirect('/admin/dashboard')

#admin rejects professional
@app.route('/<proId>/professional/reject')
def proReject(proId):
    Professional.query.get(proId).approval=-1
    db.session.commit()
    return redirect('/admin/dashboard')

#admin looks professional's details
@app.route('/<proId>/professional/details')
def proDetails(proId):
    pro=Professional.query.get(proId)
    return render_template('pro_details.html',professional=pro,category=Category.query.get(pro.catId))

#admin removes professional
@app.route('/<proId>/professional/remove')
def proRemove(proId):
    pro=Professional.query.get(proId)
    for i in pro.requests:
        i.proId=None
    Category.query.get(pro.catId).proCount-=1
    db.session.delete(pro)
    db.session.commit()
    return redirect('/admin/dashboard')

#admin bans professional
@app.route('/<proId>/professional/ban')
def proBan(proId):
    Professional.query.get(proId).approval=-1
    db.session.commit()
    return redirect('/admin/dashboard')

#admin bans customer
@app.route('/<userId>/customer/ban')
def userBan(userId):
    user=User.query.get(userId)
    user.status=-1
    for i in user.requests:
        if i.status=='Requested':
            db.session.delete(i)
    db.session.commit()
    return redirect('/admin/dashboard')

#admin removes customer
@app.route('/<userId>/customer/remove')
def userRemove(userId):
    user=User.query.get(userId)
    db.session.delete(user)
    db.session.commit()
    return redirect('/admin/dashboard')

#admin creates service
@app.route('/<cId>/service/create', methods=['GET','POST'])
def serviceCreate(cId,serv=None):
    if request.method=='POST':
        n=request.form.get('name')
        p=request.form.get('price')
        d=request.form.get('desc')
        t=request.form.get('t_req')
        s=Service(id=idGen('SE'),name=n,price=p,desc=d,t_req=t,catId=cId)
        db.session.add(s)
        Category.query.get(cId).count+=1
        db.session.commit()
        return redirect('/admin/dashboard')
    if(serv):
        return render_template('service-create.html',service=serv)
    return render_template('service-create.html',cId=cId,category=Category.query.get(cId).name)

#admin looks service details
@app.route('/<sid>/service/details')
def serviceDetails(sid):
    serv=Service.query.get(sid)
    return render_template('service_details.html',category=Category.query.get(serv.catId),service=serv)

#admin modifies service
@app.route('/<sId>/service/modify',methods=['GET','POST'])
def serviceModify(sId):
    if request.method=='POST':
        n=request.form.get("name")
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
       
        db.session.commit()
        return redirect('/admin/dashboard')
    serv=Service.query.get(sId)
    return serviceCreate(cId=-1,serv=serv)

#admin removes service
@app.route('/<sId>/service/remove')
def serviceRemove(sId):
    s=Service.query.get(sId)
    for i in Request.query.filter_by(sId=sId).all():
        db.session.delete(i)
    db.session.delete(s)
    Category.query.get(s.catId).count-=1
    db.session.commit()
    return redirect('/admin/dashboard')


#admin looks category details
@app.route('/<catId>/category/details')
def categoryDetails(catId):
    return render_template('category_details.html',category=Category.query.get(catId))

#admin creates category
@app.route('/category/create', methods=['GET','POST'])
def categoryCreate(cat=None):
    if request.method=='POST':
        n=request.form.get('name')
        s=Category(id=idGen('CA'),name=n)
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


#admin removes category
@app.route('/<catId>/category/remove')
def categoryRemove(catId):
    for j in Professional.query.filter_by(catId=catId).all():
        for k in j.requests:
            k.proId=None
        db.session.delete(j)
    for i in Service.query.filter_by(catId=catId).all():
        for j in Request.query.filter_by(sId=i.id).all():
            db.session.delete(j)
        db.session.delete(i)
    db.session.delete(Category.query.get(catId))
    db.session.commit()
    return redirect('/admin/dashboard')

#admin modifies category
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


#admin looks request details
@app.route('/<rid>/request/details')
def requestDetails(rid):
    req=Request.query.get(rid)
    serv=Service.query.get(req.sId)
    cust=User.query.get(req.userId)
    pro=None
    if(req.proId):
        pro=Professional.query.get(req.proId)
    return render_template('req_details.html',service=serv,request=req,professional=pro,customer=cust)

#admin summary page
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
            e['Accepted']+=1
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

#admin search page
@app.route('/admin/search',methods=['GET','POST'])
def adminSearch():
    return render_template("admin_search.html",categories=Category.query.all(),services=Service.query.all(),requests=Request.query.all(),customers=User.query.all(),professionals=Professional.query.all())




'''USER FUNCTIONALITIES'''
#user dashboard
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

#user books service
@app.route('/<userId>/<sId>/book')
def bookService(userId,sId):
    import datetime
    r=Request(id=idGen('RE'),userId=userId,sId=sId,d_req=datetime.datetime.now())
    db.session.add(r)
    db.session.commit()
    return redirect(f'/{userId}/dashboard')

#user cancels booking
@app.route('/<userId>/<rId>/cancel')
def cancelService(userId,rId):
    Request.query.get(rId).status='Cancelled'
    db.session.commit()
    return redirect(f'/{userId}/dashboard')

#user removes request
@app.route('/<userId>/<rId>/remove')
def removeRequest(userId,rId):
    db.session.delete(Request.query.get(rId))
    db.session.commit()
    return redirect(f'/{userId}/dashboard')

#user closes request
@app.route('/<userId>/<rId>/close',methods=['GET','POST'])
def closeService(userId,rId):
    if request.method=='POST':
        r=Request.query.get(rId)
        import datetime
        r.d_comp=datetime.datetime.now()
        r.rating=request.form.get('rating')
        r.remarks=request.form.get('remarks')
        r.status='Closed'
        pro=Professional.query.get(r.proId)
        pro.nCustomers+=1
        pro.rating=(pro.rating*(pro.nCustomers-1)+r.rating)/pro.nCustomers
        db.session.commit()
        return redirect(f'/{userId}/dashboard')

# user search page   
@app.route('/<userId>/customer/search')
def userSearch(userId):
    user=User.query.get(userId)
    requests=user.requests
    services=Service.query.all()
    return render_template('user_search.html',user=user,requests=requests,services=services)

# user summary page
@app.route('/<userId>/summary')
def userSummary(userId):
    requests=[i for i in Request.query.all() if i.userId==userId]
    e={"Requested":0,"Accepted":0,"Closed":0,"Total":0}
    for i in requests:
        if i.status=='Accepted':
            e['Accepted']+=1
        elif i.status=="Closed":
            e['Closed']+=1
        elif i.status=='Requested':
            e['Requested']+=1
        e['Total']+=1
    print(e)
    return render_template('user_sum.html',user=User.query.get(userId),e=e)

# user deletes account
@app.route('/<userId>/user/delete')
def userDelete(userId):
    user=User.query.get(userId)
    db.session.delete(user)

    db.session.commit()
    return redirect('/')

'''PROFESSIONAL FUNCTIONALITIES'''
# professional dashboard
@app.route('/<proId>/professional/dashboard')
def proDashboard(proId):
    pro=Professional.query.get(proId)
    cat=Category.query.get(pro.catId)
    s=cat.services
    sIds=[]
    for i in s:
        sIds.append(i.id)
    rcus=[]
    reqcus=[]
    r=Request.query.all()
    for i in r:
        if(i.sId in sIds and i.status!='Cancelled'):
            if(i.status=='Requested' and proId not in i.rejectIds):
                reqcus.append((i,Service.query.get(i.sId),User.query.get(i.userId)))
            else:
                rcus.append((i,Service.query.get(i.sId),User.query.get(i.userId)))
    return render_template('pro_dash.html',pro=pro,rcus=rcus,reqcus=reqcus)

#professional accepts request
@app.route('/<proId>/<rId>/accept')
def acceptRequest(proId,rId):
    r=Request.query.get(rId)
    r.proId=proId
    r.status="Accepted"
    db.session.commit()
    return redirect(f'/{proId}/professional/dashboard')

#professional rejects request
@app.route('/<proId>/<rId>/reject')
def rejectRequest(proId,rId):
    r=Request.query.get(rId)
    r.rejectIds+=' '+proId;
    db.session.commit()
    return redirect(f'/{proId}/professional/dashboard')

#professional search page
@app.route('/<proId>/professional/search')
def proSearch(proId):
    pro=Professional.query.get(proId)
    requests=[]
    for i in pro.requests:
        requests.append((User.query.get(i.userId),i))
    rejrequests=[(User.query.get(i.userId),i) for i in Request.query.all() if proId in i.rejectIds]
    return render_template('pro_search.html',pro=pro,requests=requests,rejrequests=rejrequests)

#professional summary page
@app.route('/<proId>/professional/summary')
def proSummary(proId):
    ratings=[i.rating for i in Request.query.all() if i.rating and i.proId==proId]
    d={}
    for i in ratings:
        if i in d:
            d[i]+=1
        else:
            d[i]=1
    
    requests=Request.query.all()
    catId=Professional.query.get(proId).catId
    services=Service.query.filter_by(catId=catId).all()
    
    e={"Requested":0,"Rejected":0,"Accepted":0,"Closed":0,"Total":0}
    for i in requests:
        if(Service.query.get(i.sId) in services and i.status!='Cancelled'):
            if i.status=='Accepted' and i.proId==proId:
                e['Accepted']+=1
            elif i.status=="Closed" and i.proId==proId:
                e['Closed']+=1
            elif proId in i.rejectIds:
                e['Rejected']+=1
            elif i.status=='Requested':
                e['Requested']+=1
            
            e['Total']+=1
    return render_template('pro_sum.html',pro=Professional.query.get(proId),d=d,e=e)

# professional deletes account
@app.route('/<proId>/pro/delete')
def proDelete(proId):
    pro=Professional.query.get(proId)
    Category.query.get(pro.catId).proCount-=1
    db.session.delete(pro)
    db.session.commit()
    return redirect('/')








