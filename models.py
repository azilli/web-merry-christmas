__author__ = 'mkislinska'

from google.appengine.ext import db

class Student(db.Model):
    first_name = db.StringProperty()
    last_name = db.StringProperty()
    email = db.EmailProperty()
    phone = db.PhoneNumberProperty()

    def get_roster_json(self):
        return {
            'id': self.key().id(),
            'firstName': self.first_name,
            'secondName': self.last_name,
            'email': self.email,
            'phone': self.phone,
            }

    def get_gradebook_json(self):
        return {
            'id': self.key().id(),
            'firstName': self.first_name,
            'secondName': self.last_name,
            'grades': [int(grade) for grade in Grade.all().filter("student = ", self)],
            }


class Assignment(db.Model):

    name = db.StringProperty()
    max_grade = db.IntegerProperty()

    def get_json(self):
        return {
            'id': self.key().id(),
            'name': self.name,
            'maxGrade': self.max_grade,
            }


class Grade(db.Model):
    mark = db.IntegerProperty()
    student = db.ReferenceProperty(reference_class=Student, verbose_name="FK Student")
    assignment = db.ReferenceProperty(reference_class=Assignment, verbose_name="FK Assignment")