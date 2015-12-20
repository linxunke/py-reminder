from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property

import flask_admin as admin
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla.filters import IntGreaterFilter

# Create application
app = Flask(__name__)

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'

# Create in-memory database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sample_db_2.sqlite'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


# Flask views
@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'


class Screen(db.Model):
    __tablename__ = 'screen'
    id = db.Column(db.Integer, primary_key=True)
    width = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)

    @hybrid_property
    def number_of_pixels(self):
        return self.width * self.height

# Create reminder table
class Reminder(db.Model):
    __tablename__ = 'reminder'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    expiredate = db.Column(db.DATE, nullable=False)

# Create shoppinglist table
class Shoplist(db.Model):
    __tablename__ = 'shoplist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

class ScreenAdmin(sqla.ModelView):
    ''' Flask-admin can not automatically find a hybrid_property yet. You will
        need to manually define the column in list_view/filters/sorting/etc.'''
    list_columns = ['id', 'width', 'height', 'number_of_pixels']
    column_sortable_list = ['id', 'width', 'height', 'number_of_pixels']

    # make sure the type of your filter matches your hybrid_property
    column_filters = [IntGreaterFilter(Screen.number_of_pixels,
                                       'Number of Pixels')]

class ReminderAdmin(sqla.ModelView):
    list_columns = ['id', 'name', 'expiredate']
    column_searchable_list = ('name',)

class ShoplistAdmin(sqla.ModelView):
    list_columns = ['id', 'name', 'quantity']
    column_searchable_list = ('name',)

# Create admin
admin = admin.Admin(app, name='ISC: FoodReminder', template_mode='bootstrap3')
# admin.add_view(ScreenAdmin(Screen, db.session))
admin.add_view(ReminderAdmin(Reminder, db.session))
admin.add_view(ShoplistAdmin(Shoplist, db.session))

if __name__ == '__main__':

    # Create DB
    db.create_all()

    # Start app
    app.run(debug=True)
