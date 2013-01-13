import sys
import webapp2
import jinja2
import os
from json import dumps, loads

import models


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))

GRADEBOOK_STUDENTS_STUB = [
    {
        'id': 1,
        'firstName': 'Hello',
        'secondName': 'World',
        'grades': [3, 4],
    },
    {
        'id': 2,
        'firstName': 'I',
        'secondName': 'am',
        'grades': [5, 5],
    },
]

GRADEBOOK_ASSIGNMENTS_STUB = [
    {
        'id': 1,
        'name': "Trolling",
        'maxGrade': 5,
    },
    {
        'id': 1,
        'name': "Olololing",
        'maxGrade': 5,
    },
]

ROSTER_STUDENTS_STUB = GRADEBOOK_STUDENTS_STUB

class MainHandler(webapp2.RequestHandler):
    def get(self):
        return


class ClassRosterHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('roster.jinja2')
        self.response.out.write(template.render({'inputStudents': dumps(ROSTER_STUDENTS_STUB)}))


class GradebookHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('gradebook.jinja2')
        self.response.out.write(
            template.render({
                'inputStudents': GRADEBOOK_STUDENTS_STUB,
                'inputAssignments': GRADEBOOK_ASSIGNMENTS_STUB,
                }
            )
        )

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

