// var json = require('./data.json');

(function() {


    'use strict';

    angular
        .module('formlyApp')
        .controller('MainController', MainController);

        function MainController($scope, $http) {

            //not hardcoded in future
            $http.get('/template/struct/test').then(function(res){
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

            vm.countAll = {
                name: {count: 1, element: {}}
            };
            // vm.count = 0;

            $scope.showSelected = function(sel, selected) {
                // console.log($scope);
                // if (selected) {
                //     $scope.expandedNodes.push(sel);
                // } else {
                //     var i = $scope.expandedNodes.indexOf(sel);
                //     $scope.expandedNodes.splice(i, 1);
                // }
                // console.log($scope.expandedNodes)
                vm.selectedNode = sel;
                $http.get(('/template/struct/test/'+sel['key'])).then(function(res){
                    // console.log(res.data);
                    var data = JSON.parse(res.data);
                    vm.title = sel['name']; //TODO make first char capitol
                    vm.min = sel.meta['minOccurs'];
                    vm.max = sel.meta['maxOccurs'];
                    if (vm.max == -1) {
                        vm.max = 'infinite';
                    }
                    vm.uuid = sel['key'];
                    vm.schemaName = 'test';
                    vm.fields = data['attributes'];
                    vm.model = [];
                    // console.log(sel);
                    vm.selectedElement = data;
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

                    // console.log(vm.fields);
                });
                // vm.selectedNode = sel;
                // vm.fields = sel.attributes;
                // vm.title = sel.path;
                // vm.min = sel.meta['minOccurs'];
                // vm.max = sel.meta['maxOccurs'];
                // if (vm.max == -1) {
                //     vm.max = 'infinite';
                // }
                // vm.model = [];
                // vm.possibleChildren = [];
                // // vm.possibleChildren = sel.children;
                //
                // load avaliable children
                // for (var i in sel.children) {
                //     var child = sel.children[i];
                    // if (!(child.path in vm.countAll)) {
                    //     vm.countAll[child.path] = child.meta.minOccurs;
                    // }
                //     if (child.meta.maxOccurs == -1 || vm.countAll[child.path] < child.meta.maxOccurs) {
                //         var found = false;
                //         for (i in vm.possibleChildren) {
                //             if (vm.possibleChildren[i].name == child.name) {
                //                 found = true;
                //             }
                //         }
                //         if (!found) {
                //             vm.possibleChildren.push(child);
                //         }
                //     }
                // }

             };

            vm.possibleChildren = [
                    {name: 'Simon'},
                    {name: 'Simo'},
                    {name: 'Sim'},
                    {name: 'Si'},
            ];

            vm.onSubmit = onSubmit;
            vm.addChild = addChild;

            String.prototype.replaceAll = function(str1, str2, ignore) {
                return this.replace(new RegExp(str1.replace(/([\/\,\!\\\^\$\{\}\[\]\(\)\.\*\+\?\|\<\>\-\&])/g,"\\$&"),(ignore?"gi":"g")),(typeof(str2)=="string")?str2.replace(/\$/g,"$$$$"):str2);
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
                $http.get('/template/struct/addChild/test/' + child.element['path'].replaceAll('/', '-')).then(function(res){
                    // $scope.treeInfo = [JSON.parse(res.data)];
                    console.log(res);
                    // $scope.expandedNodes = $scope.treeInfo;
                });
                // $http({
                //     method: 'POST',
                //     url: '/template/struct/addChild/test/', //TODO test to varaible
                //     data: JSON.stringify(child.element)
                // });

                // console.log(child)
                // var copy = JSON.parse(JSON.stringify(child));
                // console.log($scope.selectedNode.path)
                //get selectedNodes template json
                // var path = $scope.selectedNode.path.split('/');
                // var t = $scope.template;
                // for (var i = 0; i < path.length; i++) {
                //     if (path[i].length > 0) {
                //         t = t[path[i]];
                //     }
                // }
                // //get childs template json
                // var path = child.path.split('/');
                // var y = $scope.template;
                // for (var i = 0; i < path.length; i++) {
                //     if (path[i].length > 0) {
                //         y = t[path[i]];
                //     }
                // }
                // var copy = JSON.parse(JSON.stringify(y));
                // // console.log(t);
                // //find position in template
                //
                // if (child.name in t) {
                //     if (Array.isArray(t[child.name])) {
                //         t[child.name].push(copy);
                //     } else {
                //         var temp = t[child.name];
                //         t[child.name] = [];
                //         t[child.name].push(temp);
                //         t[child.name].push(copy);
                //     }
                // } else {
                //     console.log('I dont know where to paste new child');
                // }
                // console.log($scope.selectedNode);
                //
                // //add to data
                // var found = -1;
                // var count = 0;
                // for (var c in $scope.selectedNode.children) {
                //     if ($scope.selectedNode.children[c].name == child.name) {
                //         found = c;
                //         count += 1;
                //     }
                // }
                // copy = JSON.parse(JSON.stringify(child));
                // if (found != -1) {
                //     var f = copy.path.substring(0, copy.path.length-1).lastIndexOf("/");
                //     copy.path = copy.path.substring(0, f) + count;
                //     console.log(copy.path);
                //     copy.key = guid();
                //     $scope.selectedNode.children.splice(c, 0, copy);
                // } else {
                //     console.log('I dont know where to paste new child');
                // }

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
