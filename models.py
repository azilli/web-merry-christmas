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


class Assignment(db.Model):
    pass


class Grade(db.Model):
    mark = db.FloatProperty()
    student = db.ReferenceProperty(reference_class=Student, verbose_name="FK Student")
    assignment = db.ReferenceProperty(reference_class=Assignment, verbose_name="FK Assignment")