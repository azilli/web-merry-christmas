import webapp2
import jinja2
import os
import models

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


class MainHandler(webapp2.RequestHandler):
    def get(self):
        return


class ClassRoosterHandler(webapp2.RequestHandler):
    def get(self):
        return


class GradebookHandler(webapp2.RequestHandler):
    def get(self):
        return


# Handlers for updating students data:
class RemoveStudent(webapp2.RequestHandler):
    def post(self):
        return


class EditStudent(webapp2.RequestHandler):
    def post(self):
        return


class AddStudent(webapp2.RequestHandler):
    def post(self):
        return

# Handlers for updating grades
class EditGrade(webapp2.RequestHandler):
    def post(self):
        return


app = webapp2.WSGIApplication([('/', MainHandler), ('/gradebook', GradebookHandler), ('/class-rooster', MainHandler),
                               ('/edit-student', EditStudent), ('/remove-student', RemoveStudent),
                               ('/add-student', AddStudent), ('/edit-grade', EditGrade)],
    debug=True)

