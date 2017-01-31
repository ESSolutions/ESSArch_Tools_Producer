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

angular.module('myApp').controller('IpApprovalCtrl', function ($log, $scope, myService, appConfig, $http, $timeout, $state, $stateParams, $rootScope, listViewService, $interval, Resource, $uibModal, $translate, $filter, $anchorScroll, PermPermissionStore, $cookies){
    var vm = this;
    var ipSortString = "Uploaded,Creating,Created";
    vm.itemsPerPage = $cookies.get('etp-ips-per-page') || 10;
    $scope.updateIpsPerPage = function(items) {
        $cookies.put('etp-ips-per-page', items);
    };

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
            displayName: $scope.responsible
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
    //Undo step/task
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
    //Redo step/task
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
    //Change state
    $scope.changePath= function(path) {
        myService.changePath(path);
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
     $scope.ipSelected = false;
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
         $scope.select = false;
         $scope.eventShow = false;
         $scope.ip = row;
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

    //Update ip table with configuration from table paginetion etc
    this.callServer = function callServer(tableState) {
        $scope.ipLoading = true;
        if(vm.displayedIps.length == 0) {
            $scope.initLoad = true;
        }
        if(!angular.isUndefined(tableState)){
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
    //Make ip selected and add class to visualize
    $scope.selectIp = function(row) {
        vm.displayedIps.forEach(function(ip) {
            if(ip.id == $scope.selectedIp.id){
                ip.class = "";
            }
        });
        if(row.id == $scope.selectedIp.id && !$scope.select && !$scope.statusShow && !$scope.eventShow){
            $scope.selectedIp = {id: "", class: ""};
        } else {
            row.class = "selected";
            $scope.selectedIp = row;
        }
    };
    //Click function for ip table objects
    $scope.ipTableClick = function(row) {
        if($scope.select && $scope.ip.id== row.id){
            $scope.select = false;
            $scope.eventlog = false;
        } else {
            $scope.getSaProfiles(row);
            $scope.select = true;
            $scope.eventlog = true;
            $scope.ip = row;
            $rootScope.ip = row;
            $timeout(function() {
                $anchorScroll("select-wrap");
            }, 0);
        }
        $scope.createDisabled = false;
        $scope.edit = false;
        $scope.eventShow = false;
        $scope.statusShow = false;
    };
     $scope.$watch(function(){return $rootScope.navigationFilter;}, function(newValue, oldValue) {
         $scope.getListViewData();
     }, true);
    //Click funciton for event table objects
    $scope.eventsClick = function (row) {
        if($scope.eventShow && $scope.ip == row){
            $scope.eventShow = false;
            $rootScope.stCtrl = null;
        } else {
            if($rootScope.stCtrl) {
                $rootScope.stCtrl.pipe();
            }
            $scope.eventShow = true;
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
    $scope.addEvent = function(ip, eventType, eventDetail) {
        listViewService.addEvent(ip, eventType, eventDetail).then(function(value) {
        });
    }

    //funcitons for select view
    vm.profileModel = {};
    vm.profileFields=[];
    //Click function for profile pbject
    $scope.profileClick = function(row){
        if ($scope.selectProfile == row && $scope.edit){
            $scope.edit = false;
        } else {
            if(row.active) {
                $http({
                    method: 'GET',
                    url: row.active.profile,
                    params: {
                        "ip": $scope.ip.id
                    }
                }).then(function(response) {
                    $scope.profileToSave = row.active;
                    $scope.selectProfile = row;
                    vm.profileModel = response.data.specification_data;
                    vm.profileFields = response.data.template;
                    vm.profileFields.forEach(function(field) {
                        if(field.fieldGroup != null){
                            field.fieldGroup.forEach(function(subGroup) {
                                subGroup.fieldGroup.forEach(function(item) {
                                    item.type = 'input';
                                    item.templateOptions.disabled = true;
                                });
                            });
                        } else {
                            field.type = 'input';
                            field.templateOptions.disabled = true;
                        }
                    });
                    $scope.edit = true;
                    $scope.eventlog = true;
                    getEventlogData();
                    $timeout(function() {
                        $anchorScroll('edit-view');
                    }, 0);
                });
            }
        }
    };
    //Get eventlog data
    function getEventlogData() {
        listViewService.getEventlogData().then(function(value){
            $scope.eventTypeCollection = value;
        });
    };

    //populating select view
    $scope.selectRowCollection = [];
    $scope.selectRowCollapse = [];
    //Get All sa profiles and set default according to ip
    $scope.getSaProfiles = function(ip) {
        listViewService.getSaProfiles(ip).then(function(value) {
            $scope.saProfile = value;
            $scope.getSelectCollection(value.profile, ip);
            $scope.selectRowCollection = $scope.selectRowCollapse;
        });
    };
    //Get all profiles and populate select view array
    $scope.getSelectCollection = function (sa, ip) {
        $scope.selectRowCollapse = listViewService.getProfilesFromIp(sa, ip)
    };
    //Getting data for list view
    $scope.getListViewData = function() {
        vm.callServer($scope.tableState);
        $rootScope.loadNavigation(ipSortString);
    };
    //$scope.getListViewData();
    //$interval(function(){$scope.getListViewData();}, 5000, false);

    //toggle visibility on profiles in select view
    $scope.showHideAllProfiles = function() {
        if($scope.selectRowCollection == {} || $scope.profilesCollapse){
            $scope.profilesCollapse = false;
        } else{
            $scope.profilesCollapse = true;
        }
    };
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
        });
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
    $scope.createDisabled = false;
    //Executes Create sip on an ip
    $scope.createSip = function (ip) {
        $scope.createDisabled = true;
        $http({
            method: 'POST',
            url: ip.url+"create/",
            data: {validators: vm.validatorModel}
        })
        .then(function successCallback(response) {
            $scope.select = false;
            $scope.edit = false;
            $scope.eventlog = false;
            $timeout(function(){
                $scope.getListViewData();
                updateListViewConditional();
            }, 1000);
            $anchorScroll();
        }).finally(function(){
            $scope.createDisabled = false;
        });
    };
    var listViewInterval;
    function updateListViewConditional() {
        $interval.cancel(listViewInterval);
        listViewInterval = $interval(function() {
            var updateVar = false;
            vm.displayedIps.forEach(function(ip, idx) {
                if(ip.status < 100 || (ip.State == "Creating" && ip.status == 100)) {
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
                        if(ip.status < 100 || (ip.State == "Creating" && ip.status == 100)) {
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
    //Visibility of status view
    $scope.statusShow = false;
    //Visibility of select view
    $scope.select = false;
    //Visibility of sub-select view
    $scope.subSelect = false;
    //Visibility of edit view
    $scope.edit = false;
    //Visibility of status view
    $scope.eventlog = false;
    //Visibility of status view
    $scope.eventShow = false;
    //Toggle visibility of select view
    $scope.toggleSelectView = function () {
        if($scope.select == false){
            $scope.select = true;
        } else {
            $scope.select = false;
        }
    };
    //Toggle visibility of sub select view
    $scope.toggleSubSelectView = function () {
        if($scope.subSelect == false){
            $scope.subSelect = true;
        } else {
            $scope.subSelect = false;
        }
    };
    //toggle visibility of edit view
    $scope.toggleEditView = function () {
        if($scope.edit == false){
            $('.edit-view').show();
            $scope.edit = true;
            $scope.eventlog = true;
        } else {
            $('.edit-view').hide();
            $scope.edit = false;
            $scope.eventlog = false;
        }
    };
    //Toggle visibility of eventlog view
    $scope.toggleEventlogView = function() {
        if($scope.eventlog == false){
            $scope.eventlog = true;
        }else {
            $scope.eventlog = false;
        }
    }
    $scope.unlockConditional = function(profile) {
        if(profile.profile_type == "sip") {
            $scope.unlockSipModal(profile);
        } else {
            $scope.unlock(profile);
        }
    }

    //Unlock profile from current IP
    $scope.unlock = function(profile) {
        $http({
            method: 'POST',
            url: $scope.ip.url + "unlock-profile/",
            data: {
                type: profile.active.profile_type
            }
        }).then(function(response){
            profile.locked = false;
        });
    }
    //Change state to prepare-ip
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
        "defaultValue": true,
        "type": "select",
        "key": "validate_file_format",
    },
    {
        "templateOptions": {
            "type": "text",
            "label": $translate.instant('VALIDATEXMLFILE'),
            "options": [{name: $scope.yes, value: true},{name: $scope.no, value: false}],
        },
        "defaultValue": true,
        "type": "select",
        "key": "validate_xml_file",
    },
    {
        "templateOptions": {
            "type": "text",
            "label": $translate.instant('VALIDATELOGICALPHYSICALREPRESENTATION'),
            "options": [{name: $scope.yes, value: true},{name: $scope.no, value: false}],
        },
        "defaultValue": true,
        "type": "select",
        "key": "validate_logical_physical_representation",
    },
    {
        "templateOptions": {
            "type": "text",
            "label": $translate.instant('VALIDATEINTEGRITY'),
            "options": [{name: $scope.yes, value: true},{name: $scope.no, value: false}],
        },
        "defaultValue": true,
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
    $scope.unlockSipModal = function (profile) {
        $scope.profileToSave = profile;
        var modalInstance = $uibModal.open({
            animation: true,
            ariaLabelledBy: 'modal-title',
            ariaDescribedBy: 'modal-body',
            templateUrl: 'static/frontend/views/unlock_sip_modal.html',
            scope: $scope,
            controller: 'ModalInstanceCtrl',
            controllerAs: '$ctrl'
        })
        modalInstance.result.then(function (data) {
            $scope.unlock($scope.profileToSave);
        }, function () {
            $log.info('modal-component dismissed at: ' + new Date());
        });
    }
    $scope.checkPermission = function(permissionName) {
        return !angular.isUndefined(PermPermissionStore.getPermissionDefinition(permissionName));
    };
});

