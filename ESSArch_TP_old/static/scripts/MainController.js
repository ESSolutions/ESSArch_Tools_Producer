// var json = require('./data.json');

(function() {


    'use strict';

    angular
        .module('formlyApp')
        .controller('MainController', MainController);


    function MainController($scope, $http) {

        //not hardcoded in future
        $http.get('/template/struct/test').then(function(res) {
            $scope.treeInfo = [JSON.parse(res.data)];
            // $scope.expandedNodes = $scope.treeInfo;
        });
        // $http.get('template.json').then(function(res){
        //     $scope.template = res.data;
        //     // console.log($scope.template)
        // });

        var vm = this;

        // $scope.template = {
        //
        // };
        $scope.formTitle = 'TEST';
        vm.title = 'ttt';
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
        };

        $scope.expandedNodes = [
            // {name: 'mets',key: "a5b810a8-7187-45c1-a9e7-f7c02a5fc8fa"}
        ];

        $scope.dataForTheTree = [

        ];

        function parseElements(el, p) {
            //split path to find this and next
            if (p != '') {
                var i = p.indexOf("/");
                var key = p.substring(0, i);
                var rest = p.substring(i + 1);

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

        vm.countAll = {
            name: {
                count: 1,
                element: {}
            }
        };
        vm.anyAttribute = false;
        // vm.count = 0;

        $scope.showSelected = function(sel, selected) {
            vm.selectedNode = sel;
            $http.get(('/template/struct/test/' + sel['key'])).then(function(res) {
                // console.log(res.data);
                var data = JSON.parse(res.data);
                vm.title = sel['name'].charAt(0).toUpperCase() + sel['name'].slice(1); //TODO make first char capitol
                vm.min = sel.meta['minOccurs'];
                vm.max = sel.meta['maxOccurs'];
                if (vm.max == -1) {
                    vm.max = 'infinite';
                }
                vm.uuid = sel['key'];
                vm.schemaName = 'test';
                var arr = [];
                vm.fields = data['attributes'];
                if (data['userAttributes'].length > 0) {
                    vm.fields.push({template: '<hr/><p><b>User defined attributes</b></p>'}); //divider
                    vm.fields = vm.fields.concat(data['userAttributes']);
                }
                vm.model = [];
                vm.selectedElement = data;
                vm.anyAttribute = data['anyAttribute'];
                vm.countAll = {};
                vm.possibleChildren = [];
                for (var i in sel.children) {
                    var child = sel.children[i];
                    if (!(child.name in vm.countAll)) {
                        var d = {};
                        d['count'] = 1;
                        d['element'] = child;
                        d['name'] = child.name;
                        var max = child.meta.maxOccurs;
                        if (max == -1) {
                            max = 100000000; // most unlikly to exceed
                        }
                        d['max'] = max;
                        vm.countAll[child.name] = d;
                    } else {
                        vm.countAll[child.name]['count'] += 1;
                    }
                }
                for (var i in vm.countAll) {
                    var child = vm.countAll[i];
                    if (child.count < child.max) {
                        vm.possibleChildren.push(child);
                    }
                }
            });

        };

        vm.possibleChildren = [{
            name: 'Simon'
        }, {
            name: 'Simo'
        }, {
            name: 'Sim'
        }, {
            name: 'Si'
        }, ];

        vm.onSubmit = onSubmit;
        vm.addChild = addChild;
        vm.addAttribute = addAttribute;
        vm.saveAttribute = saveAttribute;

        function saveAttribute() {
            var attribute = {};
            attribute['key'] = vm.floatingmodel['attribname'];
            attribute['type'] = 'input';
            var to = {};
            to['required'] = vm.floatingmodel['attribrequired'];
            to['label'] = vm.floatingmodel['attribname'];
            to['type'] = 'text';
            attribute['templateOptions'] = to;
            attribute['defaultValue'] = vm.floatingmodel['attribvalue'];
            vm.fields.push(attribute);
            vm.floatingVisable = false;
            $http({
                method: 'POST',
                url: '/template/struct/addAttrib/test/' + vm.uuid + '/',
                data: attribute
            })
        }

        function addAttribute() {
            vm.floatingVisable = !vm.floatingVisable;
            vm.floatingmodel = [];
        }

        String.prototype.replaceAll = function(str1, str2, ignore) {
            return this.replace(new RegExp(str1.replace(/([\/\,\!\\\^\$\{\}\[\]\(\)\.\*\+\?\|\<\>\-\&])/g, "\\$&"), (ignore ? "gi" : "g")), (typeof(str2) == "string") ? str2.replace(/\$/g, "$$$$") : str2);
        }

        function addChild(child) {

            // send child.element to server for processing
            // reload page
            // TODO remember expandedNodes

            console.log(child);
            console.log(vm.selectedNode);
            // $http.get('/template/struct/addChild/test').then(function(res){
            //     // $scope.treeInfo = [JSON.parse(res.data)];
            //     // $scope.expandedNodes = $scope.treeInfo;
            // });
            $http.get('/template/struct/addChild/test/' + child.element['path'].replaceAll('/', '-')).then(function(res) {
                // $scope.treeInfo = [JSON.parse(res.data)];
                console.log(res);
                // $scope.expandedNodes = $scope.treeInfo;
            });

        }

        function guid() {
            function s4() {
                return Math.floor((1 + Math.random()) * 0x10000)
                    .toString(16)
                    .substring(1);
            }
            return s4() + s4() + '-' + s4() + '-' + s4() + '-' +
                s4() + '-' + s4() + s4() + s4();
        }

        // function definition
        function onSubmit() {
            for (var key in vm.model) {
                for (var j = 0; j < vm.selectedNode.attributes.length; j++) {
                    console.log(key);
                    console.log(vm.selectedNode.attributes[j].key);
                    if (key == vm.selectedNode.attributes[j].key) {
                        vm.selectedNode.attributes[j].defaultValue = vm.model[key];
                        break;
                    }
                }
            }
        }

        // TODO python:
        // function analyzeContent(c) {
        //     var res = [];
        //     var i = c.indexOf('{{')
        //     if (i > 0) {
        //         var d = {};
        //         d['text'] = c.substring(0, i);
        //         res.push(d);
        //         var r = analyzeContent(c.substring(i));
        //         for (var j = 0; j < r.length; j++) {
        //             res.push(r[j]);
        //         }
        //     } else if (i == -1) {
        //         if (c.length > 0) {
        //             var d = {};
        //             d['text'] = c;
        //             res.push(d);
        //         }
        //     } else {
        //         var d = {};
        //         var v = c.substring(i+2);
        //         i = v.indexOf('}}');
        //         d['var'] = v.substring(0, i);
        //         res.push(d);
        //         var r = analyzeContent(v.substring(i+2));
        //         for (var j = 0; j < r.length; j++) {
        //             res.push(r[j]);
        //         }
        //     }
        //     return res
        // }

        vm.model = {

        };

        vm.fields = [

            //                 {
            //                     key: 'add',
            //                     type: 'input',
            //                     originalModel: 'test',
            //                     id: 'test',
            //                     data: {value: 'test',
            //                     name: 'test'},
            //                     modelOptions: {
            //                         value: 'test',
            //                         name: 'test'
            //                     },
            //                     elementAttributes: {
            //                         value: 'test',
            //                         name: 'test'
            //                     },
            // // `template`, `templateUrl`, `key`, `model`, `originalModel`, `className`, `id`, `name`, `expressionProperties`, `extras`, `data`, `templateOptions`, `wrapper`, `modelOptions`, `watcher`, `validators`, `asyncValidators`, `parsers`, `formatters`, `noFormControl`, `hide`, `hideExpression`, `ngModelElAttrs`, `ngModelAttrs`, `elementAttributes`, `optionsTypes`, `link`, `controller`, `validation`, `formControl`, `value`, `runExpressions`, `templateManipulators`, `resetModel`, `updateInitialValue`, `initialValue`, `defaultValue`
            //                     // value: 'test',
            //                     templateOptions: {
            //                         type: 'button',
            //                         value: 'test',
            //                         label: 'add',
            //                         name: 'test',
            //                         data: {value: 'test',
            //                         name: 'test'},
            //                         placeholder: 'string',
            //                         required: true
            //                     }
            //                 },
            {
                key: 'name',
                type: 'input',
                templateOptions: {
                    type: 'text',
                    label: 'name',
                    placeholder: 'string',
                    required: true
                }
            }, {
                key: 'note',
                type: 'input',
                templateOptions: {
                    type: 'text',
                    label: 'note',
                    placeholder: 'string',
                    required: true
                }
            }, {
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
            }, {
                key: 'ROLE',
                type: 'input',
                templateOptions: {
                    type: 'text',
                    label: 'ROLE',
                    placeholder: 'string',
                    required: true
                }
            }, {
                key: 'OTHERROLE',
                type: 'select',
                templateOptions: {
                    // type: 'text',
                    label: 'OTHERROLE',
                    // placeholder: 'string',
                    // required: true
                    options: [{
                        name: 'CREATOR',
                        value: 'CREATOR'
                    }, {
                        name: 'EDITOR',
                        value: 'EDITOR'
                    }, {
                        name: 'ARCHIVIST',
                        value: 'ARCHIVIST'
                    }, ]
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
        vm.floatingfields = [{
            key: 'attribname',
            type: 'input',
            templateOptions: {
                type: 'text',
                label: 'Name',
                placeholder: 'string',
                required: true
            }
        }, {
            key: 'attribvalue',
            type: 'input',
            templateOptions: {
                type: 'text',
                label: 'Value',
                placeholder: 'string',
                required: false
            }
        }, {
            key: 'attribrequired',
            type: 'checkbox',
            templateOptions: {
                type: 'checkbox',
                label: 'Required',
                // placeholder: 'string',
                required: false
            }
        }, ];
        vm.floatingVisable = false;

    }


})();
