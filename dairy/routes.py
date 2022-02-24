
from datetime import date
import re

from socket import fromshare
from subprocess import CREATE_NO_WINDOW
from turtle import title
from wsgiref.util import request_uri

from flask import redirect, render_template, request, url_for,flash
import flask
from dairy import app, db, bcrypt
from dairy.cow.forms import BreedForm, CowForm, searchForm, show
from dairy.login.forms import AccountForm, LoginForm, RegisterForm
from dairy.models import  HBreed, User,Cow,Breeder,Medicine,Remedy
from flask_login import login_user,logout_user,current_user,login_required
import secrets, os

@app.route("/", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
       
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Login Unsuccessfull. Please check email and password!", 'danger')
        
        
    return render_template("loginAndRegister/login.html", title = "Login Page", form = form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/rigister",methods=["POST", "GET"])
def rigister():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        re = User(username= form.username.data, email=form.email.data, password=hashed_pwd
                      , user_type=form.user_type.data, firstname=form.firstname.data, lastname= form.lastname.data
                      , farmname= form.farmname.data, address = form.address.data, mobilenum = form.mobilenum.data)
        
        db.session.add(re)
        db.session.commit()
        return redirect(url_for("login"))
    
    return render_template("loginAndRegister/rigister.html", title = "Rigister Page", form = form)


@app.route("/dashboard")
@login_required
def home():
    return render_template("index.html", title = "Home Page")



def save_picture(img):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(img.filename)
    image_name = random_hex + f_ext
    image_path = os.path.join(app.root_path, 'static/img',image_name)
    img.save(image_path)
    return image_name

def remove_picture(img):
    os.remove(os.path.join(app.root_path, 'static/img', img))
    

@app.route("/profile", methods=["POST", "GET"])
def profile():
    form  = AccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            if current_user.user_img != 'default.png':
                remove_picture(current_user.user_img)
            picture_file = save_picture(form.picture.data)
            current_user.user_img = picture_file
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.password = hashed_pwd
        current_user.user_type = form.user_type.data
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.farmname = form.farmname.data
        current_user.address = form.address.data
        current_user.mobilenum = form.mobilenum.data
        db.session.commit()
        flash("Update is successfully!!!", "success")
        return redirect(url_for("profile"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.password.data  = current_user.password
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.farmname.data = current_user.farmname
        form.user_type.data  = current_user.user_type
        form.address.data = current_user.address
        form.mobilenum.data = current_user.mobilenum
    return render_template("loginAndRegister/profile.html", form = form, title = "Account Information")


@app.route("/add_cow", methods=["POST", "GET"])
def add_cow():
    form = CowForm()
    user = User.query.get(current_user.id)
    breeds = Breeder.query.filter(Breeder.user_id == user.id)
    if request.method == "POST":
        hb_breed = request.form['hb_breed']
        
    if form.validate_on_submit():
      
        cow = Cow(cow_number=form.cow_number.data, cow_name=form.cow_name.data
                  ,cow_birthday=form.cow_birthday.data, cow_gender= form.cow_gender.data
                  ,cow_status = form.cow_status.data,cow_picture=form.cow_picture.data,cow_remark= form.cow_remark.data
                  , user_id=current_user.id, mother_id = form.cow_mother.data, breeder_id = hb_breed)
        db.session.add(cow)
        db.session.commit()
        flash("Add cow successfully!!!", "success")
        return redirect(url_for("cow_milk"))
    return render_template("manageCow/add_cow.html", title="Add Cow", form = form,breeds = breeds)

@app.route("/cow_milk",methods = ["POST", "GET"])
@login_required
def cow_milk():
    form = show()
    formsearch = searchForm()
    print(form.show.data)
    if formsearch.search.data:
        page = request.args.get('page', 1, type=int)
        user = User.query.get(current_user.id)
        cows = Cow.query.filter(Cow.user_id == user.id)
        if formsearch.search.data != "":
            cows = cows.filter(Cow.cow_name.like('%'+formsearch.search.data+'%'))
        cows = cows.paginate(page = page, per_page = form.show.data)
        
        
    else:
        if form.show.data != 5:
            page = request.args.get('page', 1, type=int)
            user = User.query.get(current_user.id)
            print(user.id)
            if user:
                cow = Cow.query.filter(Cow.user_id == user.id)
                cows = cow.paginate(page = page, per_page = form.show.data)
            else:
                cows = None
        else:
            page = request.args.get('page', 1, type=int)
            user = User.query.get(current_user.id)
            print(user.id)
            if user:
                cow = Cow.query.filter(Cow.user_id == user.id)
                cows = cow.paginate(page = page, per_page = 5)
            else:
                cows = None
               
    return render_template("manageCow/cow_milk.html", title = "Cow Milk Page", cows = cows,date = date, form = form,formsearch = formsearch)


@app.route("/manageCow/delete:<int:id>")
def deleteCow(id):
    user = User.query.get(current_user.id)
    cow = Cow.query.filter(Cow.user_id == user.id)
    c = cow.filter_by(id =id).first()
    db.session.delete(c)
    db.session.commit()
    return redirect(url_for("cow_milk"))

@app.route("/manageCow/detail:<int:id>")
def detailCow(id):
    user = User.query.get(current_user.id)
    cow = Cow.query.filter(Cow.user_id == user.id)
    c = cow.filter_by(id =id).first()
   
    return render_template("manageCow/cow_detail.html", title = "Detail Cow", cow = c)

@app.route("/manageCow/updateCow:<int:id>",methods=["POST", "GET"])
def updateCow(id):
    user = User.query.get(current_user.id)
    cow = Cow.query.filter(Cow.user_id == user.id)
    c = cow.filter_by(id =id).first()
    user = User.query.get(current_user.id)
    breeds = Breeder.query.filter(Breeder.user_id == user.id)
    form = CowForm()
    if request.method == "POST":
        cb_name = request.form["cb_name"]
    if form.validate_on_submit():
        if form.cow_picture.data:
            if c.cow_picture != "default.png":
                remove_picture(c.cow_picture)
                picture_file = save_picture(form.cow_picture.data)
                c.cow_picture = picture_file
        print(form.cow_picture.data)
        c.cow_number = form.cow_number.data
        c.cow_name = form.cow_name.data
        c.cow_birthday = form.cow_birthday.data
        c.cow_gender = form.cow_gender.data
        c.cow_status = form.cow_status.data
        c.breeder_id = cb_name    
        c.cow_remark = form.cow_remark.data
        c.user.id = current_user.id 
        c.mother_id = form.cow_mother.data
       
        db.session.commit()
        flash("Update is successfully!!!", "success")
        return redirect(url_for("cow_milk"))
    elif request.method == "GET":
        form.cow_number.data = c.cow_number
        form.cow_name.data = c.cow_name
        form.cow_birthday.data = c.cow_birthday
        form.cow_gender.data = c.cow_gender
        form.cow_status.data = c.cow_status
        form.cow_remark.data = c.cow_remark
        
    return render_template("manageCow/updateCow.html", title= "Update Cow", cow = c, form = form , breeds = breeds)

@app.route("/cow_breeder",methods = ["POST", "GET"])
def cow_breeder():
    formsearch = searchForm()
    formshow = show()
    
    if formsearch.search.data:
        page = request.args.get('page', 1, type=int)
        user = User.query.get(current_user.id)
        breeds = Breeder.query.filter(Breeder.user_id == user.id)
        if formsearch.search.data != "":
             breed = breeds.filter(Breeder.cb_name.like('%' + formsearch.search.data + '%'))
        
        breed = breed.paginate(page = page, per_page = 5)
        
    else:
        if formshow.show.data != 5:
            page = request.args.get('page', 1, type=int)
            user = User.query.get(current_user.id)
            breeds = Breeder.query.filter(Breeder.user_id == user.id)
            if user:
                breed = breeds.paginate(page = page, per_page = formshow.show.data)
            else:
                None
        else:
            page = request.args.get('page', 1, type=int)
            user = User.query.get(current_user.id)
            breeds = Breeder.query.filter(Breeder.user_id == user.id)
            if user:
                #breads = Breeder.query.filter(Breeder.id == cow.breeder_id)
                breed = breeds.paginate(page = page, per_page = 5)
            else:
                None
    
    return render_template("manageCow/breeder/cow_breeder.html",title="Cow Breeder",
                           formsearch = formsearch,formshow = formshow,breeds = breed)
@app.route("/add_breed",methods=["POST", "GET"])
def add_breed():
    form = BreedForm()
    if form.validate_on_submit():
        breed = Breeder(cb_number=form.cb_number.data, cb_name = form.cb_name.data, cb_breed = form.cb_breed.data, user_id = current_user.id)
        db.session.add(breed)
        db.session.commit()
        return redirect(url_for("cow_breeder"))    
    return render_template("manageCow/breeder/add_breed.html", title= "Add Breed", form = form)

@app.route("/breeder/deleteBreed:<int:id>")
def deleteBreed(id):
    user = User.query.get(current_user.id)
    breeds = Breeder.query.filter(Breeder.user_id == user.id)
    breed = breeds.filter_by(id=id).first()
    db.session.delete(breed)
    db.session.commit()
    return redirect(url_for("cow_breeder"))

@app.route("/breeder/updateBreed:<int:id>", methods=["POST", "GET"])
def updateBreed(id):
    user = User.query.get(current_user.id)
    breeds = Breeder.query.filter(Breeder.user_id == user.id)
    breed = breeds.filter_by(id=id).first()
    form = BreedForm()
    if form.validate_on_submit():
        breed.cb_number = form.cb_number.data
        breed.cb_name = form.cb_name.data
        breed.cb_breed = form.cb_breed.data
        db.session.commit()
        flash("Update breed information already", "success")
        
        return redirect(url_for("cow_breeder"))
    
    elif request.method == "GET":
        form.cb_number.data = breed.cb_number
        form.cb_name.data = breed.cb_name
        form.cb_breed.data = breed.cb_breed
        
    return render_template("manageCow/breeder/updateBreed.html", title = "Update Breed", breed = breed, form = form)



@app.route("/manageCow/Heritage/cow_heritage",methods = ["POST", "GET"])
def cow_heritage():
    formsearch = searchForm()
    formshow = show()
    user = User.query.get(current_user.id)
    page = request.args.get('page', 1, type=int)
    hers = HBreed.query.filter(HBreed.user_id == user.id)
    cows = Cow.query.filter(Cow.user_id == user.id)
    
    if formsearch.search.data:
        if formsearch.search.data != "":
            her = hers.filter(HBreed.hb_date.like('%' + formsearch.search.data + '%'))
        hers = her.paginate(page = page, per_page = 4)
    else:
        
        if formshow.show.data != 5:
            hers = hers.paginate(page = page, per_page =formshow.show.data)
        else:
            hers = hers.paginate(page = page, per_page =4)
           
    
        
    return render_template("manageCow/Heritage/cow_heritage.html",cows = cows, hers = hers,title = "Cow Heritage", formshow = formshow, formsearch  = formsearch)


@app.route("/Cow heritage/add_heritage", methods=["POST", "GET"])
def add_heritage():
    user = User.query.get(current_user.id)
    breeds = Breeder.query.filter(Breeder.user_id == user.id)
    cows = Cow.query.filter(Cow.user_id == user.id)
    if request.method == "POST":
        hb_date = request.form["hb_date"]
        hb_cow = request.form["hb_cow"]
        hb_breed = request.form["hb_breed"]
        hb_status = request.form["hb_status"]
        hb_remark = request.form["hb_remark"]
        her = HBreed(hb_date = hb_date,cow_id = hb_cow,cb_id= hb_breed, hb_status = hb_status, hb_remark= hb_remark,user_id = current_user.id)
        print(hb_date)
        
        db.session.add(her)
        db.session.commit()
        flash("Add heritage is successfull!!", "success")
        return redirect(url_for("cow_heritage"))
    return render_template("manageCow/Heritage/add_heritage.html", title = "Add Heritage",breeds = breeds, cows = cows)

@app.route("/Cow heritage/deleteHeritage:<int:id>")
def deleteHerigtage(id):
    user = User.query.get(current_user.id)
    hers = HBreed.query.filter(HBreed.user_id == user.id)
    her = hers.filter_by(id=id).first()
    db.session.delete(her)
    db.session.commit()
    return redirect(url_for("cow_heritage"))



@app.route("/Cow heritage/updateHeritage:<int:id>", methods=["POST", "GET"])
def updateHerigtage(id):
    user = User.query.get(current_user.id)
    hers = HBreed.query.filter(HBreed.user_id == user.id)
    her = hers.filter_by(id=id).first()
    breeds = Breeder.query.filter(Breeder.user_id == user.id)
    cows = Cow.query.filter(Cow.user_id == user.id)
    if request.method == "POST":
        her.hb_date = request.form["hb_date"]
        her.ch_id = request.form["cb_name"]
        her.hb_id = request.form["hb_cow"]
        her.hb_status =request.form["hb_status"]
        
        db.session.commit()
        flash("Update Heritage already!!!", "success")
        return redirect(url_for("cow_heritage"))
    return render_template("manageCow/Heritage/updateHerigtage.html", title ="Update Heritage",her = her, breeds = breeds, cows = cows)

@app.route("/Medicine/medicine", methods=["POST","GET"])
def medicine():
    formsearch = searchForm()
    formshow = show()
    user = User.query.get(current_user.id)
    page = request.args.get('page',1, type=int)
    meds = Medicine.query.filter(Medicine.user_id == user.id)
    if formsearch.search.data:
        
        if formsearch.search.data != "":
            med = meds.filter(Medicine.m_name.like('%' + formsearch.search.data + '%'))
        meds = med.paginate(page = page, per_page = 5)
    else:
        if formshow.show.data != 5:
            meds = meds.paginate(page = page, per_page =formshow.show.data)
        else:
            meds = meds.paginate(page = page, per_page =5)
            
    return render_template("manageCow/medicine/medicine.html", title = "Medicine Page",meds = meds, formsearch = formsearch, formshow = formshow)
@app.route("/medicine/add_medicine",methods =["POST","GET"])
def add_medicine():
    if request.method == "POST":
        m_name = request.form["m_name"]
        m_use = request.form["m_use"]
        m_detail = request.form["m_detail"]
        med = Medicine(m_name= m_name, m_use= m_use, m_detail=m_detail,user_id = current_user.id)
        db.session.add(med)
        db.session.commit()
        flash("Add Medicine successfully!!", "success")
        return redirect(url_for("medicine"))
    return render_template("manageCow/medicine/add_medicine.html", title = "Add Medicine")
@app.route("/medicine/deleteMedicine:<int:id>")
def deleteMedicine(id):
    user = User.query.get(current_user.id)
    meds = Medicine.query.filter(Medicine.user_id == user.id)
    med = meds.filter_by(id=id).first()
    db.session.delete(med)
    db.session.commit()
    return redirect(url_for("medicine"))

@app.route("/medicine/updateMedicine:<int:id>",methods=["POST", "GET"])
def updateMedicine(id):
    
    user = User.query.get(current_user.id)
    meds = Medicine.query.filter(Medicine.user_id == user.id)
    med = meds.filter_by(id=id).first()
    if request.method == "POST":
        med.m_name = request.form['m_name']
        med.m_use = request.form['m_use']
        med.m_detail = request.form['m_detail']
        
        db.session.commit()
        flash("Update is successfully!!!", 'success')
        return redirect(url_for("medicine"))
    return render_template("manageCow/medicine/update_medicine.html", title = "Update Medicine", med = med )

@app.route("/remedy", methods =["POST", "GET"])
def remedy():
    
    formsearch = searchForm()
    formshow = show()
    page = request.args.get('page', 1, type=int)
    user = User.query.get(current_user.id)
    rems = Remedy.query.filter(Remedy.user_id == user.id)
    
    if formsearch.search.data:
        if formsearch.search.data != "":
            rem = rems.filter(Remedy.r_date.like('%' + formsearch.search.data + '%'))
        rems = rem.paginate(page = page, per_page = 5)
    
    else:
    
        if formshow.show.data != 5:
            rems = rems.paginate(page = page, per_page =formshow.show.data)
        else:
            rems = rems.paginate(page = page, per_page =5)
    return render_template("manageCow/Remedy/remedy.html", title = "Remedy Page",
                           formsearch = formsearch, formshow = formshow, remedys = rems)
        
        
        
@app.route("/remedy/add_remedy", methods =["POST", "GET"])
def add_remedy():
    user = User.query.get(current_user.id)
    cows = Cow.query.filter(Cow.user_id == user.id)
    medicines = Medicine.query.filter(Medicine.user_id == user.id)
    if request.method == "POST":
        r_date = request.form["r_date"]
        cow_id = request.form["cow_id"]
        m_id = request.form["m_id"]
        r_description = request.form['r_description']
        remedy = Remedy(r_date = r_date, r_description = r_description, cow_id = cow_id, m_id = m_id, user_id = current_user.id)
        db.session.add(remedy)
        db.session.commit()
        flash("Add remedy is successfully!!!", "success")
        return redirect(url_for("remedy"))
    return render_template("manageCow/Remedy/add_remedy.html", title = "Add Remedy",cows = cows, medicines = medicines)

@app.route("/remedy/deleteRemedy:<int:id>")
def deleteRemedy(id):
    page = request.args.get('page', 1, type=int)
    user = User.query.get(current_user.id)
    rems = Remedy.query.filter(Remedy.user_id == user.id)
    rem = rems.filter(id==id).first()
    db.session.delete(rem)
    db.session.commit()
    return redirect(url_for("remedy"))
@app.route("/remedy/updateRemedy:<int:id>", methods =["POST", "GET"])
def updateRemedy(id):
    page = request.args.get('page', 1, type=int)
    user = User.query.get(current_user.id)
    rems = Remedy.query.filter(Remedy.user_id == user.id)
    cows = Cow.query.filter(Cow.user_id == user.id)
    medicines = Medicine.query.filter(Medicine.user_id == user.id)
    rem = rems.filter(id==id).first()
    if request.method == "POST":
        rem.r_date= request.form["r_date"]
        rem.cow_id = request.form['cow_id']
        rem.m_id  = request.form["m_id"]
        rem.r_description = request.form["r_description"]
        db.session.commit()
        flash("Update is successfully!!!", "success")
        return redirect(url_for("remedy"))
    
    return render_template("manageCow/Remedy/update_remedy.html",title = "Update Remedy", rem = rem, cows = cows, medicines = medicines)

@app.route("/milk")
def milk():
    form = show()
    formsearch = searchForm()
    
    return render_template("manageCow/milk/milk.html", title = "Milk Page", form = form, formsearch = formsearch)