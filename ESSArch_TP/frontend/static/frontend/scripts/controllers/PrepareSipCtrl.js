/*
    ESSArch is an open source archiving and digital preservation system

    ESSArch Tools for Producer (ETP)
    Copyright (C) 2005-2017 ES Solutions AB

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.

    Contact information:
    Web - http://www.essolutions.se
    Email - essarch@essolutions.se
*/

angular.module('myApp').controller('PrepareSipCtrl', function ($log, $uibModal, $timeout, $scope, $rootScope, $window, $location, $sce, $http, myService, appConfig, $state, $stateParams, listViewService, $interval, Resource, $q, $translate, $anchorScroll, PermPermissionStore, $cookies){
    var vm = this;
    var ipSortString = "Created,Submitting,Submitted";
    vm.itemsPerPage = $cookies.get('etp-ips-per-page') || 10;
    $scope.updateIpsPerPage = function(items) {
        $cookies.put('etp-ips-per-page', items);
    };

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
    $scope.angular = angular;
    $translate(['LABEL', 'RESPONSIBLE', 'DATE', 'STATE', 'STATUS']).then(function(translations) {
        $scope.responsible = translations.RESPONSIBLE;
        $scope.label = translations.LABEL;
        $scope.date = translations.DATE;
        $scope.state = translations.STATE;
        $scope.status = translations.STATUS;
        $scope.expanding_property = {
            field: "name",
            displayName: $scope.label,
        };
        $scope.col_defs = [
        {
            field: "user",
            displayName: $scope.responsible,
        },
        {
            cellTemplate: "<div ng-include src=\"'static/frontend/views/task_pagination.html'\"></div>"
        },
        {
            field: "time_started",
            displayName: $scope.date
        },
        {
            field: "status",
            displayName: $scope.state,
            cellTemplate: "<div ng-if=\"row.branch[col.field] == 'SUCCESS'\" class=\"step-state-success\"><b>{{'SUCCESS' | translate}}</b></div><div ng-if=\"row.branch[col.field] == 'FAILURE'\" class=\"step-state-failure\"><b>{{'FAILURE' | translate}}</b></div><div ng-if=\"row.branch[col.field] != 'SUCCESS' && row.branch[col.field] !='FAILURE'\" class=\"step-state-in-progress\"><b>{{'INPROGRESS' | translate}}</b></div>"

        },
        {
            field: "progress",
            displayName: $scope.status,
            cellTemplate: "<uib-progressbar class=\"progress\" value=\"row.branch[col.field]\" type=\"success\"><b>{{row.branch[col.field]+\"%\"}}</b></uib-progressbar>"
        },
        {
            cellTemplate: "<div ng-include src=\"'static/frontend/views/undo_redo.html'\"></div>"
        }
        ];
    });

    $scope.myTreeControl = {};
    $scope.myTreeControl.scope = this;
    //Undo steps/tasks
    $scope.myTreeControl.scope.taskStepUndo = function(branch) {
        $http({
            method: 'POST',
            url: branch.url+"undo/"
        }).then(function(response) {
            $timeout(function(){
                $scope.statusViewUpdate($scope.ip);
            }, 1000);
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
            $timeout(function(){
                $scope.statusViewUpdate($scope.ip);
            }, 1000);
        }, function() {
            console.log("error");
        });
    };
    $scope.currentStepTask = {id: ""}
    $scope.myTreeControl.scope.updatePageNumber = function(branch, page) {
        if(page > branch.page_number && branch.next){
            branch.page_number = parseInt(branch.next.page);
            listViewService.getChildrenForStep(branch, branch.page_number);
        } else if(page < branch.page_number && branch.prev && page > 0) {
            branch.page_number = parseInt(branch.prev.page);
            listViewService.getChildrenForStep(branch, branch.page_number);
        }
    };
    //Click on +/- on step
    $scope.stepClick = function(step) {
        listViewService.getChildrenForStep(step);
    };

    //Click funciton for steps and tasks
    $scope.stepTaskClick = function(branch) {
        if($scope.stepTaskInfoShow && $scope.currentStepTask.id == branch.id){
            $scope.stepTaskInfoShow = false;
        }else {
            $scope.stepTaskInfoShow = true;
            $http({
                method: 'GET',
                url: branch.url
            }).then(function(response){
                $scope.currentStepTask = response.data;
                if(branch.flow_type == "task"){
                    $scope.taskInfoModal();
                } else {
                    $scope.stepInfoModal();
                }

            }, function(response) {
                response.status;
            });
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
                 ret.push(node);
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
         }, function(response){
             if(response.status == 404) {
                 $scope.statusShow = false;
                 $timeout(function(){
                     $scope.getListViewData();
                     updateListViewConditional();
                 }, 1000);
             }
         });
     };

     /*******************************************/
     /*Piping and Pagination for List-view table*/
     /*******************************************/

     var ctrl = this;
     $scope.selectedIp = {id: "", class: ""};
     this.displayedIps = [];
     //Get data for ip table from rest api
     this.callServer = function callServer(tableState) {
         $scope.ipLoading = true;
         if(vm.displayedIps.length == 0) {
             $scope.initLoad = true;
         }
         if(!angular.isUndefined(tableState)) {
             $scope.tableState = tableState;
             var search = "";
             if(tableState.search.predicateObject) {
                 var search = tableState.search.predicateObject["$"];
             }
             var sorting = tableState.sort;
             var pagination = tableState.pagination;
             var start = pagination.start || 0;     // This is NOT the page number, but the index of item in the list that you want to use to display the table.
             var number = pagination.number || vm.itemsPerPage;  // Number of entries showed per page.
             var pageNumber = start/number+1;

             Resource.getIpPage(start, number, pageNumber, tableState, $scope.selectedIp, sorting, search, ipSortString).then(function (result) {
                 ctrl.displayedIps = result.data;
                 tableState.pagination.numberOfPages = result.numberOfPages;//set the number of pages so the pagination can update
                 $scope.ipLoading = false;
                 $scope.initLoad = false;
             });
         }
     };
     //Add ip to selected
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
            var ip = row;
            if (ip.profile_submit_description) {
                $http({
                    method: 'GET',
                    url: ip.profile_submit_description.profile,
                    params: {
                        'ip': ip.id
                    }
                }).then(function(response) {
                    vm.informationModel= response.data.specification_data;
                    vm.informationFields = response.data.template;
                    vm.informationFields.forEach(function(field) {
                        field.type = 'input';
                        field.templateOptions.disabled = true;
                    });
                    if(ip.profile_transfer_project) {
                        $http({
                            method: 'GET',
                            url: ip.profile_transfer_project.profile,
                            params: {
                                'ip': ip.id
                            }
                        }).then(function(response) {
                            vm.dependencyModel= response.data.specification_data;
                            vm.dependencyFields = response.data.template;
                            vm.dependencyFields.forEach(function(field) {
                                field.type = 'input';
                                field.templateOptions.disabled = true;
                            });
                            listViewService.getFileList(ip).then(function(result) {
                                $scope.fileListCollection = result;
                                $scope.getPackageProfiles(row);
                                $scope.edit = true;
                                $scope.eventlog = true;
                                $timeout(function() {
                                    $anchorScroll("select-wrap");
                                }, 0);
                            });
                        });
                    }

                }, function(response) {
                    console.log(response.status);
                });
            }
        }
        $scope.submitDisabled = false;
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
        $rootScope.loadNavigation(ipSortString);
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
    //Creates and shows modal with step information
    $scope.stepInfoModal = function () {
        var modalInstance = $uibModal.open({
            animation: true,
            ariaLabelledBy: 'modal-title',
            ariaDescribedBy: 'modal-body',
            templateUrl: 'static/frontend/views/step_info_modal.html',
            scope: $scope,
            controller: 'ModalInstanceCtrl',
            controllerAs: '$ctrl'
        });
        modalInstance.result.then(function (data, $ctrl) {
        }, function () {
            $log.info('modal-component dismissed at: ' + new Date());
        });
    }
    $scope.max = 100;
    //Get data for eventlog view
    function getEventlogData() {
        listViewService.getEventlogData().then(function(value){
            $scope.eventTypeCollection = value;
        });
    };

    // Populate file list view
    vm.options = {
        formState: {
        }
    };
    //Get list of files in ip
    $scope.getFileList = function(ip) {
        listViewService.getFileList(ip).then(function(result) {
            $scope.fileListCollection = result;
        });
    };
    //Get package dependencies for ip(transfer_project profile)
    $scope.getPackageDependencies = function(ip) {
        if(ip.profile_transfer_project) {
            $http({
                method: 'GET',
                url: ip.profile_transfer_project.profile,
                params: {
                    'ip': ip.id
                }
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
                url: ip.profile_submit_description.profile,
                params: {
                    'ip': ip.id
                }
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
    $scope.submitDisabled = false;
    $scope.submitSip = function(ip, email) {
        if(!email) {
            var sendData = {validators: vm.validatorModel}
        } else {
            var sendData = {validators: vm.validatorModel, subject: email.subject, body: email.body}
        }
        $scope.submitDisabled = true;
        $http({
            method: 'POST',
            url: ip.url+'submit/',
            data: sendData
        }).then(function(response) {
            $scope.eventlog = false;
            $scope.edit = false;
            $timeout(function() {
                $scope.getListViewData();
                updateListViewConditional();
            }, 1000);
            $scope.submitDisabled = false;
            $anchorScroll();
        }, function(response) {
            $scope.submitDisabled = false;
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

    $scope.colspan = 9;
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
            vm.displayedIps.splice(vm.displayedIps.indexOf(ipObject), 1);
            $scope.edit = false;
            $scope.select = false;
            $scope.eventlog = false;
            $scope.eventShow = false;
            $scope.statusShow = false;
            $rootScope.loadNavigation(ipSortString);
        });
    }
    $scope.tracebackModal = function (profiles) {
        $scope.profileToSave = profiles;
        var modalInstance = $uibModal.open({
            animation: true,
            ariaLabelledBy: 'modal-title',
            ariaDescribedBy: 'modal-body',
            templateUrl: 'static/frontend/views/task_traceback_modal.html',
            scope: $scope,
            size: 'lg',
            controller: 'ModalInstanceCtrl',
            controllerAs: '$ctrl'
        })
        modalInstance.result.then(function (data) {
        }, function () {
            $log.info('modal-component dismissed at: ' + new Date());
        });
    }
    $scope.emailModal = function (profiles) {
        if(vm.dependencyModel.preservation_organization_receiver_email) {
            var modalInstance = $uibModal.open({
                animation: true,
                ariaLabelledBy: 'modal-title',
                ariaDescribedBy: 'modal-body',
                templateUrl: 'static/frontend/views/email_modal.html',
                scope: $scope,
                size: 'lg',
                controller: 'ModalInstanceCtrl',
                controllerAs: '$ctrl'
            })
            modalInstance.result.then(function (data) {
                $scope.submitSip($scope.ip, data.email);
            }, function () {
                $log.info('modal-component dismissed at: ' + new Date());
            });
        } else {
            $scope.submitSip($scope.ip);
        }
    }

    $scope.checkPermission = function(permissionName) {
        return !angular.isUndefined(PermPermissionStore.getPermissionDefinition(permissionName));
    };
});
