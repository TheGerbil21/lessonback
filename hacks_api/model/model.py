from sqlalchemy import Column, Integer, String, Text
from .. import db
from sqlalchemy.exc import IntegrityError
import json

# 
# Computer DB class that maps computer SQL table 
#
class Computer(db.Model):
    __tablename__ = "computer"

    # 
    # DB columns for brand, year, and age
    #    
    id = Column(Integer, primary_key=True)
    _name = Column(String(255), unique=True, nullable=False)
    _year = Column(Integer, nullable=False)
    _age = Column(Integer, nullable=False)

    # 
    # DB class constructor 
    #
    def __init__(self, name, year, age):
        self._name = name
        self._year = year
        self._age = age

    # 
    # DB class string representation of an object
    #
    def __repr__(self):
        return "<Student(id='%s', name='%s', year='%s', age='%s'>" % (
            self.id,
            self.name,
            self.year,
            self.age,
        )

    # 
    # Returns computer brand
    #    
    @property
    def name(self):
        return self._name

    # 
    # Sets computer brand
    #        
    @name.setter
    def name(self, value):
        self._name = value

    # 
    # checks computer brand
    #            
    def is_name(self, name):
        return self._name == name

    # 
    # Returns computer year
    #        
    @property
    def year(self):
        return self._year

    # 
    # Sets computer year
    #        
    @year.setter
    def year(self, value):
        self._year = value

    # 
    # Sets computer age
    #            
    @property
    def age(self):
        return self._age

    # 
    # Sets computer age
    #        
    @age.setter
    def age(self, value):
        self._age = value

  

    # 
    # Converts data to dictionary
    #            
    def to_dict(self):
        return {"id": self.id, "name": self.name, "year": self.year, "age": self._age}

    # 
    # Converts Leaderboard to string values
    #                
    def __str__(self):
        return json.dumps(self.read())

    # 
    # Creates database
    #                
    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.remove()
            return None
    # 
    # Returns brand value pairs
    #            
    def read(self):
        return {
            "id": self.id,
            "name": self.name,
            "year": self.year,
            "age": self.age,
        }

    # 
    # Updates DB rows for computer data
    #                
    def update(self, name="", year="", age=""):
        """only updates values with length"""
        if len(name) > 0:
            self.name = name
        if len(year) > 0:
            self.year = year
        if len(age) > 0:
            self.age = age
        db.session.add(self)
        db.session.commit()
        return self

    # 
    # Deletes row from the DB
    #                
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None

    # 
    # Initializes DB with test data
    #            
def init_computers():
    """Create database and tables"""
    # db.create_all()
    """Tester data for table"""
    c1 = Computer(name="Apple", year=2004,
                     age=19)
    c2 = Computer(name="DELL", year=2008,
                     age=15)
    c3 = Computer(name="Lenovo", year=2016,
                     age=7)
    c4 = Computer(name="Samsung", year=2000,
                     age=23)
    computers = [c1, c2, c3, c4]

    """Builds sample user/note(s) data"""
    for c in computers:
        try:
            '''add user to table'''
            object = c.create()
            print(f"Created new uid {object.name}")
            db.session.add(c)
            db.session.commit()
        except:
            '''fails with bad or duplicate data'''
            print(f"Records exist uid {c.name}, or error.")

# place your model code here
# you can use the code we showed in our lesson as an example

# make sure you put initial data here as well
# EXTRA CREDIT: make the placing of data more efficient than our method shown in the lesson