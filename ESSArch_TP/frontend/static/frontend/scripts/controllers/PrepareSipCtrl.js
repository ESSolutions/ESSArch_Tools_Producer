angular.module('myApp').controller('PrepareSipCtrl', function ($log, $uibModal, $timeout, $scope, $rootScope, $window, $location, $sce, $http, myService, appConfig, $state, $stateParams, listViewService, $interval, Resource){
    var vm = this;
    // List view
    //Go to give state
    $scope.changePath= function(path) {
        myService.changePath(path);
    };
    //Redirect to django admin page
    $scope.redirectAdmin = function () {
        $window.location.href="/admin/";
    }
    $scope.tree_data = [];
    $scope.expanding_property = {
        field: "name",
        displayName: "Label",
    };
    $scope.col_defs = [
    {
        field: "user",
        displayName: "Responsible",
    },
    {
        field: "time_created",
        displayName: "Date"
    },
    {
        field: "status",
        displayName: "State",
    },
    {
        field: "progress",
        displayName: "Status",
        cellTemplate: "<uib-progressbar ng-click=\"taskStepUndo(row.branch)\" class=\"progress\" value=\"row.branch[col.field]\" type=\"success\"><b>{{row.branch[col.field]+\"%\"}}</b></uib-progressbar>"
    },
    {
        cellTemplate: "<a ng-click=\"treeControl.scope.taskStepUndo(row.branch)\" ng-if=\"(row.branch.status == 'SUCCESS' || row.branch.status == 'FAILURE') && !row.branch.undone && !row.branch.undo_type\" style=\"color: #a00\">{{'UNDO' | translate}}</a></br ><a ng-click=\"treeControl.scope.taskStepRedo(row.branch)\" ng-if=\"row.branch.undone\"style=\"color: #0a0\">{{'REDO' | translate}}</a>"
    }
    ];
    $scope.myTreeControl = {};
    $scope.myTreeControl.scope = this;
    //Undo steps/tasks
    $scope.myTreeControl.scope.taskStepUndo = function(branch) {
        $http({
            method: 'POST',
            url: branch.url+"undo/"
        }).then(function(response) {
            console.log("UNDO");
        }, function() {
            console.log("error");
        });
    };
    //Redo steps/tasks
    $scope.myTreeControl.scope.taskStepRedo = function(branch){
        $http({
            method: 'POST',
            url: branch.url+"retry/"
        }).then(function(response) {
            console.log("REDO");
        }, function() {
            console.log("error");
        });
    };
     $scope.currentStepTask = {id: ""}
    //Click funciton for steps and tasks
     $scope.stepTaskClick = function(branch) {
        if(branch.isTask){
            if($scope.stepTaskInfoShow && $scope.currentStepTask.id == branch.id){
                $scope.stepTaskInfoShow = false;
            }else {
                $scope.stepTaskInfoShow = true;
                $http({
                    method: 'GET',
                    url: branch.url
                }).then(function(response){
                    $scope.currentStepTask = response.data;
                    $scope.taskInfoModal();
                }, function(response) {
                    response.status;
                });
            }
        }
     };
     // Click funtion columns that does not have a relevant click function
     $scope.ipRowClick = function(row) {
         $scope.selectIp(row);
         if($scope.ip == row){
             row.class = "";
             $scope.selectedIp = {id: "", class: ""};
         }
         if($scope.eventShow) {
             $scope.eventsClick(row);
         }
         if($scope.statusShow) {
             $scope.stateClicked(row);
         }
         if ($scope.select || $scope.edit || $scope.eventlog) {
             $scope.ipTableClick(row);
         }
     }
    //click function forstatus view
     var stateInterval;
     $scope.stateClicked = function(row){
         if($scope.statusShow && $scope.ip == row){
             $scope.statusShow = false;
         } else {
             $scope.statusShow = true;
             $scope.edit = false;
             $scope.statusViewUpdate(row);
         }
         $scope.subSelect = false;
         $scope.eventlog = false;
         $scope.eventShow = false;
         $scope.select = false;
         $scope.ip = row;
         $rootScope.ip = row;
     };
     $scope.$watch(function(){return $scope.statusShow;}, function(newValue, oldValue) {
         if(newValue) {
             $interval.cancel(stateInterval);
             stateInterval = $interval(function(){$scope.statusViewUpdate($scope.ip)}, 4000);
         } else {
             $interval.cancel(stateInterval);
         }
     });
     $rootScope.$on('$stateChangeStart', function() {
         $interval.cancel(stateInterval);
     });
     //Get data for status view
     function checkExpanded(nodes) {
         var ret = [];
         nodes.forEach(function(node) {
             if(node.expanded == true) {
                 ret.push({id: node.id, name: node.name});
             }
             if(node.children && node.children.length > 0) {
                 ret = ret.concat(checkExpanded(node.children));
             }
         });
         return ret;
     }
     //Update status view data
     $scope.statusViewUpdate = function(row){
        var expandedNodes = [];
        if($scope.tree_data != []) {
            expandedNodes = checkExpanded($scope.tree_data);
        }
        listViewService.getTreeData(row, expandedNodes).then(function(value) {
            $scope.tree_data = value;
        });
    };

     /*******************************************/
     /*Piping and Pagination for List-view table*/
     /*******************************************/

     var ctrl = this;
     this.itemsPerPage = 10;
     $scope.selectedIp = {id: "", class: ""};
     this.displayedIps = [];
     //Get data for ip table from rest api
     this.callServer = function callServer(tableState) {
         if(!angular.isUndefined(tableState)) {
             $scope.tableState = tableState;
             var sorting = tableState.sort;
             var pagination = tableState.pagination;
             var start = pagination.start || 0;     // This is NOT the page number, but the index of item in the list that you want to use to display the table.
             var number = pagination.number;  // Number of entries showed per page.
             var pageNumber = start/number+1;

             Resource.getIpPage(start, number, pageNumber, tableState, $scope.selectedIp, sorting, "CREATED").then(function (result) {
                 ctrl.displayedIps = result.data;
                 tableState.pagination.numberOfPages = result.numberOfPages;//set the number of pages so the pagination can update
             });
         }
     };    //Add ip to selected
    $scope.selectIp = function(row) {
        vm.displayedIps.forEach(function(ip) {
            if(ip.id == $scope.selectedIp.id){
                ip.class = "";
            }
        });
        if(row.id == $scope.selectedIp.id && !$scope.select && !$scope.edit && !$scope.eventlog && !$scope.eventShow){
            $scope.selectedIp = {id: "", class: ""};
        } else {
            row.class = "selected";
            $scope.selectedIp = row;
        }
    };
    //Click function for ip table
    $scope.ipTableClick = function(row) {
        if($scope.edit && $scope.ip.id== row.id){
            $scope.edit = false;
            $scope.eventlog = false;
        } else {
            $scope.ip = row;
            $rootScope.ip = row;
            $http({
                method: 'GET',
                url: row.url
            }).then(function (response) {
                getEventlogData();
                $scope.getPackageInformation(response.data);
                $scope.getPackageDependencies(response.data);
                $scope.getPackageProfiles(response.data);
                $scope.getFileList(response.data);
            });
            $scope.edit = true;
            $scope.eventlog = true;

        }
        $scope.eventShow = false;
        $scope.statusShow = false;
    };
    $rootScope.$watch(function(){return $rootScope.navigationFilter;}, function(newValue, oldValue) {
        $scope.getListViewData();
    }, true);

    //click funtion or event
    $scope.eventsClick = function (row) {
        if($scope.eventShow && $scope.ip == row){
            $scope.eventShow = false;
            $rootScope.stCtrl = null;
        } else {
            if($rootScope.stCtrl) {
                $rootScope.stCtrl.pipe();
            }
            getEventlogData();
            $scope.eventShow = true;
            $scope.statusShow = false;
        }
        $scope.select = false;
        $scope.edit = false;
        $scope.eventlog = false;
        $scope.ip = row;
        $rootScope.ip = row;
    };
    //Add event to database
    $scope.addEvent = function(ip, eventType, eventDetail) {
        listViewService.addEvent(ip, eventType, eventDetail).then(function(value) {
        });
    }
    //Get data for list view
    $scope.getListViewData = function() {
        vm.callServer($scope.tableState);
    };
    //$scope.getListViewData();
    //$interval(function(){$scope.getListViewData();}, 5000, false);

    //Creates and shows modal with task information
    $scope.taskInfoModal = function () {
        var modalInstance = $uibModal.open({
            animation: true,
            ariaLabelledBy: 'modal-title',
            ariaDescribedBy: 'modal-body',
            templateUrl: 'static/frontend/views/task_info_modal.html',
            scope: $scope,
            controller: 'ModalInstanceCtrl',
            controllerAs: '$ctrl'
        })
        modalInstance.result.then(function (data, $ctrl) {
        }, function () {
            $log.info('modal-component dismissed at: ' + new Date());
        });
    }
    $scope.max = 100;
    //Get data for eventlog view
    function getEventlogData() {
        listViewService.getEventlogData().then(function(value){
            $scope.statusNoteCollection = value;
        });
    };

    // Populate file list view
    vm.options = {
        formState: {
        }
    };
    //Get list of files in ip
    $scope.getFileList = function(ip) {
        $scope.fileListCollection = listViewService.getFileList(ip);;
    };
    //Get package dependencies for ip(transfer_project profile)
    $scope.getPackageDependencies = function(ip) {
        $http({
            method: 'GET',
            url: ip.SubmissionAgreement
        }).then(function(response) {
            var sa = response.data;
            $http({
                method: 'GET',
                url: sa.profile_transfer_project.active.url
            }).then(function(response) {
                vm.dependencyModel= response.data.specification_data;
                vm.dependencyFields = response.data.template;
            }, function(response) {
            });
        }, function(response){
            console.log(response.status);
        });
    }
    vm.profileFields = [];
    vm.profileModel = {
    };
    //Get lock-status from profiles
    $scope.getPackageProfiles = function(ip) {
        listViewService.getIp(ip.url).then(function(value) {
            ip = value;
        $http({
            method: 'GET',
            url: ip.SubmissionAgreement
        }).then(function(response) {
            vm.profileModel = {
            };

            var sa = response.data;
            getProfiles(sa.profile_transfer_project, ip).then(function(profileValue){
                if(profileValue != null){
                    vm.profileModel.transfer_project = profileValue;
                    var field = {
                        templateOptions: {
                            label: "transfer_project",
                            options: [{name: "OK", value: true},{name: "", value: false}]

                        },
                        type: "select",
                        key: "transfer_project"
                    };
                    vm.profileFields.push(field);
                }
            });
            getProfiles(sa.profile_content_type, ip).then(function(profileValue){
                if(profileValue != null){
                    vm.profileModel.content_type = profileValue;
                    var field = {
                        templateOptions: {
                            label: "content_type",
                            options: [{name: "OK", value: true},{name: "", value: false}]

                        },
                        type: "select",
                        key: "content_type"
                    }
                    vm.profileFields.push(field);
                };
            });
            getProfiles(sa.profile_data_selection, ip).then(function(profileValue){
                if(profileValue != null){
                    vm.profileModel.data_selection = profileValue;
                    var field = {
                        templateOptions: {
                            label: "data_selection",
                            options: [{name: "OK", value: true},{name: "", value: false}]

                        },
                        type: "select",
                        key: "data_selection"
                    };
                    vm.profileFields.push(field);
                }
            });
            getProfiles(sa.profile_classification, ip).then(function(profileValue){
                if(profileValue != null){
                    vm.profileModel.classification = profileValue;
                    var field = {
                        templateOptions: {
                            label: "classification",

                            options: [{name: "OK", value: true},{name: "", value: false}]


                        },
                        type: "select",
                        key: "classification"
                    };
                    vm.profileFields.push(field);
                }
            });
            getProfiles(sa.profile_import, ip).then(function(profileValue){
                if(profileValue != null){
                    vm.profileModel.import = profileValue;
                    var field = {
                        templateOptions: {
                            label: "import",

                            options: [{name: "OK", value: true},{name: "", value: false}]


                        },
                        type: "select",
                        key: "import"
                    };
                    vm.profileFields.push(field);
                }
            });
            getProfiles(sa.profile_submit_description, ip).then(function(profileValue){
                if(profileValue != null){
                    vm.profileModel.submit_description = profileValue;
                    var field = {
                        templateOptions: {
                            label: "submit_description",
                            options: [{name: "OK", value: true},{name: "", value: false}]


                        },
                        type: "select",
                        key: "submit_description"
                    };
                    vm.profileFields.push(field);
                }
            });
            getProfiles(sa.profile_sip, ip).then(function(profileValue){
                if(profileValue != null){
                    vm.profileModel.sip = profileValue;
                    var field = {
                        templateOptions: {
                            label: "sip",

                            options: [{name: "OK", value: true},{name: "", value: false}]


                        },
                        type: "select",
                        key: "sip"
                    };
                    vm.profileFields.push(field);
                }
            });
            getProfiles(sa.profile_aip, ip).then(function(profileValue){
                if(profileValue != null){
                    vm.profileModel.aip = profileValue;
                    var field = {
                        templateOptions: {
                            label: "aip",

                            options: [{name: "OK", value: true},{name: "", value: false}]


                        },
                        type: "select",
                        key: "aip"
                    };
                    vm.profileFields.push(field);
                }
            });
            getProfiles(sa.profile_dip, ip).then(function(profileValue){
                if(profileValue != null){
                    vm.profileModel.dip = profileValue;
                    var field = {
                        templateOptions: {
                            label: "dip",

                            options: [{name: "OK", value: true},{name: "", value: false}]


                        },
                        type: "select",
                        key: "dip"
                    };
                    vm.profileFields.push(field);
                }
            });
            getProfiles(sa.profile_workflow, ip).then(function(profileValue){
                if(profileValue != null){
                    vm.profileModel.workflow = profileValue;
                    var field = {
                        templateOptions: {
                            label: "workflow",

                            options: [{name: "OK", value: true},{name: "", value: false}]


                        },
                        type: "select",
                        key: "workflow"
                    };
                    vm.profileFields.push(field);
                }
            });
            getProfiles(sa.profile_preservation_metadata, ip).then(function(profileValue){
                if(profileValue != null){
                    vm.profileModel.preservation_metadata = profileValue
                        var field = {
                            templateOptions: {
                                label: "preservation_metadata",

                                options: [{name: "OK", value: true},{name: "", value: false}]


                            },
                            type: "select",
                            key: "preservation_metadata"
                        };
                    vm.profileFields.push(field);
                }
            });
            getProfiles(sa.profile_event, ip).then(function(profileValue){
                if(profileValue != null){
                    vm.profileModel.event = profileValue;
                    var field = {
                        templateOptions: {
                            label: "event",
                            options: [{name: "OK", value: true},{name: "", value: false}]

                        },
                        type: "select",
                        key: "event"
                    };
                    vm.profileFields.push(field);
                }
            });
        }, function(response){
            console.log(response.status);
        });
        });
    }
    //Get profiles in given profile type
    function getProfiles(profiles, ip){
        if(profiles.active == null || angular.isUndefined(profiles)){
            var deferred = $q.defer();
            deferred.resolve(null);
            return deferred.promise;
        }
        var promise = $http({
            method: 'GET',
            url: getActiveProfile(profiles).url
        }).then(function(response) {
            var returnVal = false;
            ip.locks.forEach(function(lock) {
                if(lock.profile == response.data.url){
                    returnVal = true;
                }
            });
            return returnVal;
        }, function(response) {
            console.log(response.status);
        });
        return promise;
    }
    //Get package information(submit-description)
    $scope.getPackageInformation = function(ip) {
        $http({
            method: 'GET',
            url: ip.SubmissionAgreement
        }).then(function(response) {
            var sa = response.data;
            $http({
                method: 'GET',
                url: getActiveProfile(sa.profile_submit_description).url
            }).then(function(response) {
                vm.informationModel= response.data.specification_data;
                vm.informationFields = response.data.template;
            }, function(response) {
              console.log(response.status);
            });
        }, function(response){
            console.log(response.status);
        });
    };
    //Get active profile
    function getActiveProfile(profiles) {

        return profiles.active;
    }
    $scope.submitSip = function(ip) {
        $http({
            method: 'POST',
            url: ip.url+'submit/'
        }).then(function(response) {
            $scope.eventlog = false;
            $scope.edit = false;
            $scope.getListViewData();
            updateListViewConditional();
        }, function(response) {
            console.log(response.status);
        });
    }
    function updateListViewConditional() {
        console.log("Running updateListViewConditional");
        listViewInterval = $interval(function() {
            var updateVar = false;
            vm.displayedIps.forEach(function(ip, idx) {
                if(ip.status < 100) {
                    if(ip.step_state != "FAILURE") {
                        updateVar = true;
                    }
                }
                if(updateVar) {
                    $scope.getListViewData();
                }
            });
        }, 4000);
    };

    $scope.colspan = 6;
    //visibility of status view
    $scope.statusShow = false;
    //visibility of event view
    $scope.eventShow = false;
    //visibility of select view
    $scope.select = false;
    //visibility of sub-select view
    $scope.subSelect = false;
    //visibility of edit view
    $scope.edit = false;
    //visibility of eventlog view
    $scope.eventlog = false;
});
