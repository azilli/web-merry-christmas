import sys
import webapp2
import jinja2
import os
from json import dumps, loads

from models import *


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

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.redirect("/class-roster")


class ClassRosterHandler(webapp2.RequestHandler):
    def get(self):
        students = [student.get_roster_json() for student in Student.all()]

        template = jinja_environment.get_template('roster.jinja2')
        self.response.out.write(template.render({'inputStudents': dumps(students), "url" : "/class-roster"}))


class GradebookHandler(webapp2.RequestHandler):
    def get(self):
        students = [student.get_gradebook_json() for student in Student.all()]
        assignments = [assignment.get_json() for assignment in Assignment.all()]

        template = jinja_environment.get_template('gradebook.jinja2')

        self.response.out.write(
            template.render({
                'inputStudents': dumps(students),
                'inputAssignments': dumps(assignments),
                "url" : "/gradebook",
                }
            )
        )

# Handlers for updating students data:
class RemoveStudent(webapp2.RequestHandler):
    def post(self):
        id = int(self.request.get('id'))
        student = Student.get_by_id(id)

        for grade in Grade.all().filter("student = ", student):
            grade.delete()
        student.delete()
        sys.stderr.write("\nremoving student with id=%s\n" % id)

class EditStudent(webapp2.RequestHandler):
    def post(self):
        id_str = self.request.get('id')
        data = loads(self.request.get('data'))

        if id_str == "null":
            student = Student()
        else:
            student = Student.get_by_id(int(id_str))

        student.email = data["email"]
        student.first_name = data["firstName"]
        student.last_name = data["secondName"]
        student.phone = data["phone"]
        student.put()

        if id_str == "null":
            for assignment in Assignment.all():
                grade = Grade()
                grade.student = student
                grade.assignment = assignment
                grade.mark = 0.0
                grade.put()
        id_str = str(student.key().id())
        sys.stderr.write("\nediting student with id=%s, data=%s\n" % (id_str, data))
        self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
        self.response.out.write(dumps({"id": id_str}))


# Handlers for updating grades and assignments
class EditGrade(webapp2.RequestHandler):
    def post(self):
        assignment = Assignment.get_by_id(int(self.request.get('assignment_id')))
        student = Student.get_by_id(int(self.request.get('student_id')))

        grade = Grade.all().filter("assignment = ", assignment).filter("student = ", student)

        grade.mark = int(self.request.get('grade'))
        grade.put()

        sys.stderr.write("\nediting grade with student_id=%s, assignment_id=%s, data=%s\n" % (student, assignment, data))


class EditAssignment(webapp2.RequestHandler):
    def post(self):
        id_str = self.request.get('id')
        data = loads(self.request.get('data'))

        if id_str == "null":
            assignment = Assignment()
        else:
            assignment = Assignment.get_by_id(int(id_str))

        assignment.name = data["name"]
        assignment.max_grade = data["maxGrade"]
        assignment.put()

        if id_str == "null":
            for student in Student.all():
                grade = Grade()
                grade.mark = 0
                grade.assignment = assignment
                grade.student = student
                grade.put()

        id_str = str(assignment.key().id())
        sys.stderr.write("\nediting grade with id=%s, data=%s\n" % (id_str, data))
        self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
        self.response.out.write(dumps({"id" : id_str}))


class RemoveAssignment(webapp2.RequestHandler):
    def post(self):
        id = int(self.request.get('id'))
        assignment = Assignment.get_by_id(int(id))

        for grade in Grade.all().filter("assignment = ", assignment):
            grade.delete()

        assignment.delete()
        sys.stderr.write("\nremoving assignment with id=%s\n" % id)


app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/gradebook', GradebookHandler),
                               ('/class-roster', ClassRosterHandler),
                               ('/students/edit', EditStudent),
                               ('/students/remove', RemoveStudent),
                               ('/grades/edit', EditGrade),
                               ('/assignments/edit', EditAssignment),
                               ('/assignments/remove', RemoveAssignment)],
    debug=True)

