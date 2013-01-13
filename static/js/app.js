/*global ko, crossroads */
(function () {
    'use strict';



    // represent a single todo item
    var Stud = function (firstName, secondName, grades) {
        var self = this;
        this.firstName = ko.observable(firstName);
        this.secondName = ko.observable(secondName);
        this.grades = ko.observableArray(grades || [{ value: ko.observable(5) }, { value: ko.observable(4) }/*, { value: ko.observable(5)}*/]);
        this.average = ko.computed(function () {
            var avr = 0;
            var len = 0;
            ko.utils.arrayForEach(self.grades(), function (item) {
                avr += 1 * item.value();
                len++;
            });
            return avr / len;
            // return 666;
        });
        this.lesson = "lesson";
        //this.editing = false;
    };

    // our main view model
    var ViewModel = function (studs) {
        var self = this;
        var count = 3;
        // map array of passed in todos to an observableArray of Todo objects
        self.studs = ko.observableArray(ko.utils.arrayMap(studs, function (stud) {
            return new Stud(stud.firstName, stud.secondName);
        }));

        self.add = function () {
            var grades = [];

            for (var i = 0; i < count; i++) {
                grades.push({ value: ko.observable(0) });
            }
            self.studs.push(new Stud("", "", grades));
        }

        self.remove = function (stud) {
            self.studs.remove(stud);
        }

        self.addgrade = function () {
            count++;
            ko.utils.arrayForEach(self.studs(), function (stud) {
                stud.grades.push({ value: ko.observable(0) });
            });
        }
    };

    // check local storage for todos
    var studs = ko.utils.parseJson(localStorage.getItem('studs'));

    // bind a new instance of our view model to the page
    var viewModel = new ViewModel(studs || [new Stud("A", "B"), new Stud("C", "D")]);
    ko.applyBindings(viewModel);

    // set up filter routing
} ());
