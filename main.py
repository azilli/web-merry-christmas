import sys
import webapp2
import jinja2
import os
from json import dumps, loads

import models


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))

ROSTER_STUDENTS_STUB = [
    {
        'id': 1,
        'firstName': 'Hello',
        'secondName': 'World',
        'email': 'world@hello.com',
        'phone': '+380981617916',
    },
    {
        'id': 2,
        'firstName': 'I',
        'secondName': 'am',
        'email': 'ro@b.ot',
        'phone': '+380678156371',
    },
]


class MainHandler(webapp2.RequestHandler):
    def get(self):
        return


class ClassRosterHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('roster.jinja2')
        self.response.out.write(template.render({'inputStudents': dumps(ROSTER_STUDENTS_STUB)}))


class GradebookHandler(webapp2.RequestHandler):
    def get(self):
        return


# Handlers for updating students data:
class RemoveStudent(webapp2.RequestHandler):
    def post(self):
        id = self.request.get('id')
        sys.stderr.write("\nremoving student with id=%s\n" % id)

class EditStudent(webapp2.RequestHandler):
    def post(self):
        id = self.request.get('id')
        data = loads(self.request.get('data'))
        sys.stderr.write("\nediting student with id=%s, data=%s\n" % (id, data))


# Handlers for updating grades
class EditGrade(webapp2.RequestHandler):
    def post(self):
        pass

app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/gradebook', GradebookHandler),
                               ('/class-roster', ClassRosterHandler),
                               ('/students/edit', EditStudent),
                               ('/students/remove', RemoveStudent),
                               ('/edit-grade', EditGrade)],
    debug=True)

