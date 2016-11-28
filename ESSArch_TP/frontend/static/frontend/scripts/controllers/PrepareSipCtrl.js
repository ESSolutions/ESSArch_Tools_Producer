angular.module('myApp').controller('PrepareSipCtrl', function ($log, $uibModal, $timeout, $scope, $rootScope, $window, $location, $sce, $http, myService, appConfig, $state, $stateParams, listViewService, $interval, Resource, $q, $translate){
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
             stateInterval = $interval(function(){$scope.statusViewUpdate($scope.ip)}, appConfig.stateInterval);
         } else {
             $interval.cancel(stateInterval);
         }
     });
     $rootScope.$on('$stateChangeStart', function() {
         $interval.cancel(stateInterval);
         $interval.cancel(listViewInterval);
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
         $scope.statusLoading = true;
         var expandedNodes = [];
         if($scope.tree_data != []) {
             expandedNodes = checkExpanded($scope.tree_data);
         }
         listViewService.getTreeData(row, expandedNodes).then(function(value) {
             $scope.tree_data = value;
             $scope.statusLoading = false;
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
         $scope.ipLoading = true;
         if(!angular.isUndefined(tableState)) {
             $scope.tableState = tableState;
             var search = "";
             if(tableState.search.predicateObject) {
                 var search = tableState.search.predicateObject["$"];
             }
             var sorting = tableState.sort;
             var pagination = tableState.pagination;
             var start = pagination.start || 0;     // This is NOT the page number, but the index of item in the list that you want to use to display the table.
             var number = pagination.number;  // Number of entries showed per page.
             var pageNumber = start/number+1;

             Resource.getIpPage(start, number, pageNumber, tableState, $scope.selectedIp, sorting, search, "Created,Submitting,Submitted").then(function (result) {
                 ctrl.displayedIps = result.data;
                 tableState.pagination.numberOfPages = result.numberOfPages;//set the number of pages so the pagination can update
                 $scope.ipLoading = false;
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
    $scope.$watch(function(){return $rootScope.navigationFilter;}, function(newValue, oldValue) {
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
        $scope.fileListCollection = listViewService.getFileList(ip);
    };
    //Get package dependencies for ip(transfer_project profile)
    $scope.getPackageDependencies = function(ip) {
        if(ip.profile_transfer_project) {
            $http({
                method: 'GET',
                url: ip.profile_transfer_project.profile
            }).then(function(response) {
                vm.dependencyModel= response.data.specification_data;
                vm.dependencyFields = response.data.template;
                vm.dependencyFields.forEach(function(field) {
                    field.templateOptions.disabled = true;
                });
            });
        }
    }
    vm.profileFields = [];
    vm.profileModel = {
    };
    //Get lock-status from profiles
    $scope.getPackageProfiles = function(ip) {
        vm.profileFields = [];
        vm.profileModel = {};
        if(ip.profile_transfer_project){
            vm.profileModel.transfer_project = ip.profile_transfer_project.LockedBy != null;
            var field = {
                templateOptions: {
                    label: "transfer_project",
                    disabled: true
                },
                type: "checkbox",
                key: "transfer_project"
            };
            vm.profileFields.push(field);
        }
        if(ip.profile_submit_description){
            vm.profileModel.submit_description = ip.profile_submit_description.LockedBy != null;
            var field = {
                templateOptions: {
                    label: "submit_description",
                    disabled: true
                },
                type: "checkbox",
                key: "submit_description"
            };
            vm.profileFields.push(field);
        }
        if(ip.profile_sip){
            vm.profileModel.sip = ip.profile_sip.LockedBy != null;
            var field = {
                templateOptions: {
                    label: "sip",
                    disabled: true
                },
                type: "checkbox",
                key: "sip"
            };
            vm.profileFields.push(field);
        }
        if(ip.profile_aip){
            vm.profileModel.aip = ip.profile_aip.LockedBy != null;
            var field = {
                templateOptions: {
                    label: "aip",
                    disabled: true
                },
                type: "checkbox",
                key: "aip"
            };
            vm.profileFields.push(field);
        }
        if(ip.profile_dip){
            vm.profileModel.dip = ip.profile_dip.LockedBy != null;
            var field = {
                templateOptions: {
                    label: "dip",
                    disabled: true
                },
                type: "checkbox",
                key: "dip"
            };
            vm.profileFields.push(field);
        }
        if(ip.profile_content_type){
            vm.profileModel.content_type = ip.profile_content_type.LockedBy != null;
            var field = {
                templateOptions: {
                    label: "content_type",
                    disabled: true
                },
                type: "checkbox",
                key: "content_type"
            }
            vm.profileFields.push(field);
        };

        if(ip.profile_authority_information){
            vm.profileModel.authority_information = ip.profile_authority_information.LockedBy != null;
            var field = {
                templateOptions: {
                    label: "authority_information",
                    disabled: true
                },
                type: "checkbox",
                key: "authority_information"
            };
            vm.profileFields.push(field);
        }
        if(ip.profile_archival_description){
            vm.profileModel.archival_description = ip.profile_archival_description.LockedBy != null;
            var field = {
                templateOptions: {
                    label: "archival_description",
                    disabled: true
                },
                type: "checkbox",
                key: "archival_description"
            };
            vm.profileFields.push(field);
        }
        if(ip.profile_preservation_metadata){
            vm.profileModel.preservation_metadata = ip.profile_preservation_metadata.LockedBy != null;
            var field = {
                templateOptions: {
                    label: "preservation_metadata",
                    disabled: true
                },
                type: "checkbox",
                key: "preservation_metadata"
            };
            vm.profileFields.push(field);
        }
        if(ip.profile_event){
            vm.profileModel.event = ip.profile_event.LockedBy != null;
            var field = {
                templateOptions: {
                    label: "event",
                    disabled: true
                },
                type: "checkbox",
                key: "event"
            };
            vm.profileFields.push(field);
        }
        if(ip.profile_data_selection){
            vm.profileModel.data_selection = ip.profile_data_selection.LockedBy != null;
            var field = {
                templateOptions: {
                    label: "data_selection",
                    disabled: true
                },
                type: "checkbox",
                key: "data_selection"
            };
            vm.profileFields.push(field);
        }
        if(ip.profile_import){
            vm.profileModel.import = ip.profile_import.LockedBy != null;
            var field = {
                templateOptions: {
                    label: "import",
                    disabled: true
                },
                type: "checkbox",
                key: "import"
            };
            vm.profileFields.push(field);
        }
        if(ip.profile_workflow){
            vm.profileModel.workflow = ip.profile_workflow.LockedBy != null;
            var field = {
                templateOptions: {
                    label: "workflow",
                    disabled: true
                },
                type: "checkbox",
                key: "workflow"
            };
            vm.profileFields.push(field);
        }
    }
    //Get package information(submit-description)
    $scope.getPackageInformation = function(ip) {
        if (ip.profile_submit_description) {
            $http({
                method: 'GET',
                url: ip.profile_submit_description.profile
            }).then(function(response) {
                vm.informationModel= response.data.specification_data;
                vm.informationFields = response.data.template;
                vm.informationFields.forEach(function(field) {
                    field.templateOptions.disabled = true;
                });
            }, function(response) {
                console.log(response.status);
            });
        }
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
            $timeout(function() {
                $scope.getListViewData();
                updateListViewConditional();
            }, 1000);
        }, function(response) {
            console.log(response.status);
        });
    }
    var listViewInterval;
    function updateListViewConditional() {
        $interval.cancel(listViewInterval);
        listViewInterval = $interval(function() {
            var updateVar = false;
            vm.displayedIps.forEach(function(ip, idx) {
                if(ip.status < 100) {
                    if(ip.step_state != "FAILURE") {
                        updateVar = true;
                    }
                }
            });
            if(updateVar) {
                $scope.getListViewData();
            } else {
                $interval.cancel(listViewInterval);
                listViewInterval = $interval(function() {
                    var updateVar = false;
                    vm.displayedIps.forEach(function(ip, idx) {
                        if(ip.status < 100) {
                            if(ip.step_state != "FAILURE") {
                                updateVar = true;
                            }
                        }
                    });
                    if(!updateVar) {
                        $scope.getListViewData();
                    } else {
                        updateListViewConditional();
                    }

                }, appConfig.ipIdleInterval);
            }
        }, appConfig.ipInterval);
    };
    updateListViewConditional();

    $scope.colspan = 7;
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
    $scope.yes = $translate.instant('YES');
    $scope.no = $translate.instant('NO');
    vm.validatorModel = {

    };
    vm.validatorFields = [
    {
        "templateOptions": {
            "type": "text",
            "label": $translate.instant('VALIDATEFILEFORMAT'),
            "options": [{name: $scope.yes, value: true},{name: $scope.no, value: false}],
        },
        "defaultValue": false,
        "type": "select",
        "key": "validate_file_format",
    },
    {
        "templateOptions": {
            "type": "text",
            "label": $translate.instant('VALIDATEXMLFILE'),
            "options": [{name: $scope.yes, value: true},{name: $scope.no, value: false}],
        },
        "defaultValue": false,
        "type": "select",
        "key": "validate_xml_file",
    },
    {
        "templateOptions": {
            "type": "text",
            "label": $translate.instant('VALIDATELOGICALPHYSICALREPRESENTATION'),
            "options": [{name: $scope.yes, value: true},{name: $scope.no, value: false}],
        },
        "defaultValue": false,
        "type": "select",
        "key": "validate_logical_physical_representation",
    },
    {
        "templateOptions": {
            "type": "text",
            "label": $translate.instant('VALIDATEINTEGRITY'),
            "options": [{name: $scope.yes, value: true},{name: $scope.no, value: false}],
        },
        "defaultValue": false,
        "type": "select",
        "key": "validate_integrity",
    }
    ];
    //Create and show modal for remove ip
    $scope.removeIpModal = function (ipObject) {
        var modalInstance = $uibModal.open({
            animation: true,
            ariaLabelledBy: 'modal-title',
            ariaDescribedBy: 'modal-body',
            templateUrl: 'static/frontend/views/remove-ip-modal.html',
            controller: 'ModalInstanceCtrl',
            controllerAs: '$ctrl'
        })
        modalInstance.result.then(function (data) {
            $scope.removeIp(ipObject);
        }, function () {
            $log.info('modal-component dismissed at: ' + new Date());
        });
    }
    //Remove and ip
    $scope.removeIp = function (ipObject) {
        $http({
            method: 'DELETE',
            url: ipObject.url
        }).then(function() {
            console.log("ip removed");
            vm.displayedIps.splice(vm.displayedIps.indexOf(ipObject), 1);
            $scope.edit = false;
            $scope.select = false;
            $scope.eventlog = false;
            $scope.eventShow = false;
            $scope.statusShow = false;

        });
    }
});
