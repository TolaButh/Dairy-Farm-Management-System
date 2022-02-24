
from ast import Sub
from email.policy import default
from os import curdir
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField ,SelectField, SubmitField, BooleanField, RadioField,DateField,FileField,TextAreaField
from wtforms.validators import DataRequired, InputRequired,Length
from flask_login import current_user
from flask_wtf.file import FileAllowed
from datetime import datetime
from dairy.models import User, Cow, Mother, Breeder



    
def selectMother():
    try:
        mother = Mother.query.all()
        moth = []
        for m in mother:
            ms = m.mother_name
            moth.append(ms)
        return moth
    except:
        return None
    
    
def selectBreeder():
    try:
        user = User.query.get(current_user.id)
        breeds = Breeder.query.filter(Breeder.user_id == user.id)
        breeds = Breeder.query.all()
        fath = []
        for f in breeds:
            fs = f.cb_name
            fath.append(fs)
        return fath
    except:
        return None


class CowForm(FlaskForm):
    cow_number = StringField("Cow ID", validators=[DataRequired(),Length(max=5, min=4)])
    cow_name = StringField("Cow Name", validators=[DataRequired(),Length(max=20, min=4)])
    cow_birthday =  DateField('Cow Birthday',format='%Y-%m-%d', validators=[DataRequired()],default=datetime.now())
    cow_gender = RadioField("Cow Gender" 
                            , choices=[('เพศเมีย', 'เพศเพีย'),
                                       ('เพศผู้', 'เพศผู้')])
    cow_status = RadioField("Cow Status"
                            ,choices=[('วัววัยรุ่น', 'วัววัยรุ่น'),
                                      ('ตั้งครรน์', 'ตั้งครรน์'),
                                      ('ให้นม', 'ให้นม')])
    cow_picture = FileField("Cow Picture", validators=[FileAllowed(['jpeg', 'png', 'jpg'])])
    cow_remark =   TextAreaField("Remark", validators=[DataRequired()],)
    cow_mother = SelectField("Cow Mother",  validators=[DataRequired()],choices=[('สาราวาร', 'สาราวาร'),
                                                                                 ('จารยาร', 'จารายาร'),
                                                                                 ('บารายา', 'บารายา')])
   
    submit = SubmitField("Add Cow")
    
class show(FlaskForm):
    show = IntegerField("Show" ,validators=[DataRequired()],default="5")
    submit = SubmitField('Item')
class searchForm(FlaskForm):
    search = StringField("Search")
    submit = SubmitField("Search")
    
    
class BreedForm(FlaskForm):
    cb_number = StringField("หมายพ่อพันธุ์", validators=[DataRequired(), Length(max=8, min=4)])
    cb_name = StringField("ชื่อพ่อพันธุ์",validators=[DataRequired()])
    cb_breed = StringField("สายพันธุ์", validators=[DataRequired()])
    submit = SubmitField("เพื่อพ่อพันธุ์")
    update = SubmitField("แก้ไขข้อมูลพ่อพันธุ์")
    