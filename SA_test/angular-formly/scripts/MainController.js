// var json = require('./data.json');

(function() {


    'use strict';

    angular
        .module('formlyApp')
        .controller('MainController', MainController);

        function MainController($scope, $http) {

            $http.get('data.json').then(function(res){
                $scope.dataForTheTree = [res.data];
            });
            $http.get('template.json').then(function(res){
                $scope.template = res.data;
                // console.log($scope.template)
            });

            var vm = this;

            $scope.template = {

            };
            // The model object that we reference
            // on the  element in index.html
            vm.rental = {

            };
            $scope.formTitle = 'TEST';
            // An array of our form fields with configuration
            // and options set. We make reference to this in
            // the 'fields' attribute on the  element

            $scope.treeOptions = {
                nodeChildren: "children",
                dirSelectable: true,
                injectClasses: {
                    ul: "a1",
                    li: "a2",
                    liSelected: "a7",
                    iExpanded: "a3",
                    iCollapsed: "a4",
                    iLeaf: "a5",
                    label: "a6",
                    labelSelected: "a8"
                }
            }
            $scope.dataForTheTree =
            [

            ];

            function parseElements(el, p) {
                //split path to find this and next
                if (p != '') {
                    var i = p.indexOf("/");
                    var key = p.substring(0, i);
                    var rest = p.substring(i+1);

                    for (var k in el) {
                        if (k == key) {
                            return parseElements(el[k], rest)
                        }
                    }
                    return null;
                } else {
                    return el
                }
            }

            $scope.parseElements = parseElements

            $scope.showSelected = function(sel) {
                 $scope.selectedNode = sel;
                 console.log(sel)
                 vm.rentalFields = sel.attributes
                 $scope.formTitle = sel.path
                 console.log(parseElements($scope.template, sel.path))
             };

            vm.rentalFields = [
                {
                    key: 'name',
                    type: 'input',
                    templateOptions: {
                        type: 'text',
                        label: 'name',
                        placeholder: 'string',
                        required: true
                    }
                },
                {
                    key: 'note',
                    type: 'input',
                    templateOptions: {
                        type: 'text',
                        label: 'note',
                        placeholder: 'string',
                        required: true
                    }
                },
                {
                    template: '<hr/><p><b>Attributes</b></p>'
                },
                //attributes:
                {
                    key: 'ID',
                    type: 'input',
                    templateOptions: {
                        type: 'text',
                        label: 'ID',
                        placeholder: 'string',
                        required: true
                    }
                },
                {
                    key: 'ROLE',
                    type: 'input',
                    templateOptions: {
                        type: 'text',
                        label: 'ROLE',
                        placeholder: 'string',
                        required: true
                    }
                },
                {
                    key: 'OTHERROLE',
                    type: 'select',
                    templateOptions: {
                        // type: 'text',
                        label: 'OTHERROLE',
                        // placeholder: 'string',
                        // required: true
                        options: [
                            {name: 'CREATOR', value: 'CREATOR'},
                            {name: 'EDITOR', value: 'EDITOR'},
                            {name: 'ARCHIVIST', value: 'ARCHIVIST'},
                        ]
                    }
                },
                // {
                //     key: 'first_name',
                //     type: 'input',
                //     templateOptions: {
                //         type: 'text',
                //         label: 'First Name',
                //         placeholder: 'Enter your first name',
                //         required: true
                //     }
                // },
                // {
                //     key: 'last_name',
                //     type: 'input',
                //     templateOptions: {
                //         type: 'text',
                //         label: 'Last Name',
                //         placeholder: 'Enter your last name',
                //         required: true
                //     }
                // },
                // {
                //     key: 'email',
                //     type: 'input',
                //     templateOptions: {
                //         type: 'email',
                //         label: 'Email address',
                //         placeholder: 'Enter email',
                //         required: true
                //     }
                // },
                // {
                //     key: 'under25',
                //     type: 'checkbox',
                //     templateOptions: {
                //         label: 'Are you under 25?',
                //     },
                //     // Hide this field if we don't have
                //     // any valid input in the email field
                //     hideExpression: '!model.email'
                // },
                // {
                //     key: 'province',
                //     type: 'select',
                //     templateOptions: {
                //         label: 'Province/Territory',
                //         // Call our province service to get a list
                //         // of provinces and territories
                //         options: province.getProvinces()
                //     },
                //     hideExpression: '!model.email'
                // },
                // {
                //     key: 'insurance',
                //     type: 'input',
                //     templateOptions: {
                //         label: 'Insurance Policy Number',
                //         placeholder: 'Enter your insurance policy number'
                //     },
                //     hideExpression: '!model.under25 || !model.province',
                // }
            ];

        }


})();
