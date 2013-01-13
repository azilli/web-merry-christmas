/*global ko, crossroads */
(function () {
    'use strict';

    var ENTER_KEY = 13;

    // a custom binding to handle the enter key (could go in a separate library)
    ko.bindingHandlers.enterKey = {
        init: function (element, valueAccessor, allBindingsAccessor, data) {
            var wrappedHandler, newValueAccessor;

            // wrap the handler with a check for the enter key
            wrappedHandler = function (data, event) {
                if (event.keyCode === ENTER_KEY) {
                    valueAccessor().call(this, data, event);
                }
            };

            // create a valueAccessor with the options that we would want to pass to the event binding
            newValueAccessor = function () {
                return {
                    keyup: wrappedHandler
                };
            };

            // call the real event binding's init function
            ko.bindingHandlers.event.init(element, newValueAccessor, allBindingsAccessor, data);
        }
    };

    var GradeWrapper = function (student_id, assignment_id, grade) {
        var self = this;
        this.grade = ko.observable(grade);
        // Non changeable
        this.student_id = student_id;
        this.assignment_id = assignment_id;
    }

    // represent a single todo item
    var Student = function (id, firstName, secondName, grades) {
        var self = this;
        this.id = ko.observable(id);
        this.firstName = ko.observable(firstName);
        this.secondName = ko.observable(secondName);
        this.grades = ko.observableArray(
            ko.utils.arrayMap(
                grades,
                function (grade) {
                    return ko.observable(new GradeWrapper(id, grade.assignment_id, grade.grade));
                }
            )
        );

        this.average = ko.computed(function () {
            var sum = 0;
            ko.utils.arrayForEach(
                self.grades(),
                function (item) {
                    sum += parseInt(item().grade());
                }
            );
            console.log(sum);
            console.log(ko.utils.arrayMap(
                self.grades(),
                function (grade) {
                    return grade().grade();
                }
            ));
            return sum / self.grades().length;
        });
    };

    var Assignment = function (id, name, maxGrade) {
        var self = this;
        this.id = ko.observable(id);
        this.name = ko.observable(name);
        this.maxGrade = ko.observable(maxGrade);
    };

    // our main view model
    var ViewModel = function (inputStudents, inputAssignments) {
        var self = this;

        // map array of passed in todos to an observableArray of Todo objects
        self.students = ko.observableArray(
            ko.utils.arrayMap(
                inputStudents,
                function (student) {
                    var grades = [];
                    for (var i=0; i < student.grades.length; i++) {
                        grades.push({assignment_id: inputAssignments[i].id, grade:student.grades[i]});
                    };
                    console.log(grades);
                    return new Student(
                        student.id,
                        student.firstName,
                        student.secondName,
                        grades
                    );
                }
            )
        );

        self.assignments = ko.observableArray(
            ko.utils.arrayMap(
                inputAssignments,
                function (assignment) {
                    return new Assignment(
                        assignment.id,
                        assignment.name,
                        assignment.maxGrade
                    );
                }
            )
        );

        self.editGrade = function(grade) {
            console.log(grade);

            var params = {
                assignment_id: grade.assignment_id,
                student_id: grade.student_id,
                data: JSON.stringify(grade)
            }

            $.ajax({
                url: "/grades/edit",
                type: "POST",
                data: params,
                success: function (data) {
                },
                error: function (data) {

                }
            });
        }

        self.addAssignment = function () {
            var assignment = new Assignment(
                null,
                "Lesson #" + (self.assignments().length + 1),
                5
            );

            self.assignments.push(assignment);

            ko.utils.arrayForEach(
                self.students(),
                function (student) {
                    student.grades.push(ko.observable(new GradeWrapper(student.id(), assignment.id(), 0)));
                }
            );

            data: ko.toJSON(assignment)

            var params = {
                id: null,
                data: JSON.stringify(assignment)
            }

            $.ajax({
                url: "/assignments/edit",
                type: "POST",
                data: params,
                success: function (data) {
                    if (!data.id === undefined){
                        assignment.id(data.id);
                    }
                },
                error: function (data) {

                }
            });
        }
    };

    // check local storage for todos
//    var studs = ko.utils.parseJson(localStorage.getItem('studs'));

    // bind a new instance of our view model to the page
    var viewModel = new ViewModel(inputStudents, inputAssignments);
    ko.applyBindings(viewModel);

    // set up filter routing
} ());
