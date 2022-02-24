from email.policy import default
from datetime import date, datetime
from dairy import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(11), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)
    firstname = db.Column(db.String(30),nullable=False)
    lastname = db.Column(db.String(30), nullable=False)
    farmname = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(20),nullable=False)
    mobilenum = db.Column(db.String(20), nullable=False)
    user_img = db.Column(db.String(20), default="default.png")
    cows = db.relationship('Cow', backref="user", lazy='dynamic')
    breeds = db.relationship("Breeder", backref = "user", lazy = 'dynamic')
    hbreeds = db.relationship("HBreed", backref = "user", lazy = 'dynamic')
    reds = db.relationship("Remedy", backref="user", lazy= 'dynamic')
    milks = db.relationship("Milk", backref="user", lazy='dynamic')
    
    def __repr__(self):
        return f"<Username: {self.username}>"
    
    
class Mother(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    mother_name = db.Column(db.String(100), nullable=False)
    cows = db.relationship('Cow', backref="mother", lazy='dynamic')
    def __repr__(self) -> str:
        return f"<Mother name: {self.mother_name}>"
class Breeder(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    cb_number = db.Column(db.String(20), nullable=False)
    cb_name = db.Column(db.String(100), nullable=False)
    cb_breed = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    cows = db.relationship('Cow', backref="breeder", lazy='dynamic')
    hbreeds = db.relationship("HBreed", backref="breeder", lazy="dynamic")
    def __repr__(self):
        return f"<Father Name: {self.cb_name}>"
        
    
class Cow(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    cow_number = db.Column(db.String(10), nullable=False, unique=False)
    cow_name = db.Column(db.String(50), nullable=False)
    cow_birthday = db.Column(db.Date(),default=date.today())
    cow_gender = db.Column(db.String(50), nullable=False)
    cow_status = db.Column(db.String(50), nullable=False)
    cow_picture = db.Column(db.String(50), default="default.png")
    cow_remark = db.Column(db.String(100), nullable=False, default="None")
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    mother_id = db.Column(db.Integer(), db.ForeignKey('mother.id'))
    breeder_id = db.Column(db.Integer(), db.ForeignKey('breeder.id'))
    hbreeds = db.relationship("HBreed", backref="cow", lazy="dynamic")
    rems = db.relationship("Remedy", backref="cow", lazy="dynamic")
    
    def __repr__(self):
        return f"<Cow Name: {self.cow_name}>"
    
class HBreed(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    hb_date = db.Column(db.String(30), default = date.today())
    hb_status = db.Column(db.String(), nullable=False)
    hb_remark = db.Column(db.String(), nullable=False)
    cow_id = db.Column(db.Integer(), db.ForeignKey('cow.id'))
    cb_id = db.Column(db.Integer(), db.ForeignKey('breeder.id'))
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    

class Medicine(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    m_name = db.Column(db.String(20), nullable=False)
    m_use = db.Column(db.String(50), nullable=False)
    m_detail = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    meds = db.relationship("Remedy", backref="medicine", lazy="dynamic")
    
class Remedy(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    r_date = db.Column(db.String(20), nullable=False)
    r_description = db.Column(db.String(100), nullable=False)
    cow_id = db.Column(db.Integer(), db.ForeignKey("cow.id"))
    m_id = db.Column(db.Integer(), db.ForeignKey("medicine.id"))
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    
class Milk(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    mi_date = db.Column(db.String(20), nullable=False)
    mi_num = db.Column(db.Integer(), nullable=False)
    mi_morning = db.Column(db.Integer(), nullable=False)
    mi_afternoon = db.Column(db.Integer(), nullable=False)
    mi_quantity = db.Column(db.Integer(), nullable=False)
    mi_avg = db.Column(db.Integer(), nullable=False)
   
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    
    