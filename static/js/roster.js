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
    // represent a single todo item
  
    var Student = function (id, firstName, secondName, email, phone) {
        var self = this;
        this.id = ko.observable(id);
        this.firstName = ko.observable(firstName);
        this.secondName = ko.observable(secondName);
        this.email = ko.observable(email);
        this.phone = ko.observable(phone);
    };

    // our main view model
    var ViewModel = function (inputStudents) {
        var self = this;

        // map array of passed in todos to an observableArray of Todo objects
        self.students = ko.observableArray(
            ko.utils.arrayMap(
                inputStudents,
                function (student) {
                    return new Student(
                        student.id,
                        student.firstName,
                        student.secondName,
                        student.email,
                        student.phone
                    );
                }
            )
        );

        self.add = function () {
//            console.log("add");
//            console.log(self.students)
            self.students.push(
                new Student(
                    ko.observable(null),
                    ko.observable(""),
                    ko.observable(""),
                    ko.observable(""),
                    ko.observable("")
                )
            );
            console.log(self.students)
        }

        // Remove function
        self.remove = function (student) {
            var obj = ko.toJS(student);
            if (obj.id === null) {
                self.students.remove(student);
            }
            else {
//                console.log(ko.toJSON(student));
                var params = { id: obj.id };

                $.ajax({
                    url: "/students/remove",
                    type: "POST",
                    data: params,
                    success: function () {
                        self.students.remove(student);
                    },
                    error: function () {

                    }
                });
            }

//            console.log(obj);

        }

        // Editing function
        self.edit = function (student) {
            var obj = ko.toJS(student);
//            console.log(obj);
//            console.log(student);

            var params = {
                'id':obj.id,
                'data':JSON.stringify(obj)
            };

            $.ajax({
                url: "/students/edit",
                type: "POST",
                data: params,
                dataType : 'json',
                success: function (data) {
//                    console.log(data);
                    if (data.id){
                        student.id(data.id);
                    }
                },
                error: function () {
                }
            });
        }


    };

    // check local storage for todos
    // var student = ko.utils.parseJson(localStorage.getItem('student'));

//    console.log(inputStudents);

    var StudsModel = [];

    for (var i = 0; i < inputStudents.length; i++) {
        StudsModel.push(
            new Student(
                inputStudents[i].id,
                inputStudents[i].firstName,
                inputStudents[i].secondName,
                inputStudents[i].email,
                inputStudents[i].phone
            )
        );
    }

    var viewModel = new ViewModel(StudsModel);
    ko.applyBindings(viewModel);

    // set up filter routing
}());
