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

angular.module('myApp').controller('PrepareIpCtrl', function ($log, $uibModal, $timeout, $scope, $window, $location, $sce, $http, myService, appConfig, $state, $stateParams, $rootScope, listViewService, $interval, Resource, $translate, $cookies, $cookieStore, $filter, $anchorScroll, PermPermissionStore, $q){
    var vm = this;
    var ipSortString = "Preparing,Prepared";
    vm.itemsPerPage = $cookies.get('etp-ips-per-page') || 10;
    $scope.updateIpsPerPage = function(items) {
        $cookies.put('etp-ips-per-page', items);
    };
    //Status tree view structure
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
     };
     //Redirect to admin page
     $scope.redirectAdmin = function () {
         $window.location.href="/admin/";
     }

     //Go to another state
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
         if ($scope.select) {
             $scope.ipTableClick(row);
         }
     }
     //Click function for status view
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
         $rootScope.ip = row;
     };
     //If status view is visible, start update interval
     $scope.$watch(function(){return $scope.statusShow;}, function(newValue, oldValue) {
         if(newValue) {
             $interval.cancel(stateInterval);
             stateInterval = $interval(function(){$scope.statusViewUpdate($scope.ip)}, appConfig.stateInterval);
        } else {
            $interval.cancel(stateInterval);
        }
     });
     //Cancel update intervals on state change
     $rootScope.$on('$stateChangeStart', function() {
         $interval.cancel(stateInterval);
         $interval.cancel(listViewInterval);
     });
     //Get data for status view

     //checks expanded rows in tree structure
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
    //Get data according to ip table settings and populates ip table
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

    //Click function for Ip table
    $scope.ipTableClick = function(row) {
        if($scope.select && $scope.ip.id== row.id){
            $scope.select = false;
        } else {
            $scope.ip = row;
            $rootScope.ip = $scope.ip;
            $scope.getSaProfiles($scope.ip);
            $scope.select = true;
            $timeout(function() {
                $anchorScroll("select-wrap");
            }, 0);
        }
        $scope.eventlog = false;
        $scope.edit = false;
        $scope.eventShow = false;
        $scope.statusShow = false;
    };
     $scope.$watch(function(){return $rootScope.navigationFilter;}, function(newValue, oldValue) {
         $scope.getListViewData();
     }, true);
    //Click funciton for event view
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

    //Adds a new event to the database
    $scope.addEvent = function(ip, eventType, eventDetail) {
        listViewService.addEvent(ip, eventType, eventDetail).then(function(value) {
        });
    }
    //Get data for list view
    $scope.getListViewData = function() {
        vm.callServer($scope.tableState);
        $rootScope.loadNavigation(ipSortString);
    };
    //updates every 5 seconds
    //$scope.getListViewData();
    //$interval(function(){$scope.getListViewData();}, 5000, false);
       //Getting data for status view
       //$scope.getStatusViewData();

    // Progress bar max value
    $scope.max = 100;
    //funcitons for select view
    //Condition for profile click. it the profile is locked it is not shown in the edit view
    $scope.profileClickCondition = function(row){
        if(!row.locked && row.active != null){
            $scope.profileClick(row);
        }
    }
    vm.profileModel = {};
    vm.profileFields=[];
    vm.options = {};
    //Click funciton for profile view
    $scope.profileClick = function(row){
        if ($scope.selectProfile == row && $scope.edit){
            $scope.eventlog = false;
            $scope.edit = false;
        } else {
            if (row.active.name){
                var profileUrl = row.active.url;
            } else {
                var profileUrl = row.active.profile;
            }


            $http({
                method: 'GET',
                url: profileUrl,
                params: {
                    'sa': $scope.saProfile.profile.id,
                    'ip': $scope.ip.id
                }
            }).then(function(response) {
                response.data.profile_name = response.data.name;
                row.active = response.data;
                row.profiles = [response.data];
                $scope.selectProfile = row;
                vm.profileModel = angular.copy(row.active.specification_data);
                vm.profileFields = row.active.template;
                $scope.treeElements =[{name: $translate.instant('ROOT'), type: "folder", children: angular.copy(row.active.structure)}];
                $scope.expandedNodes = [$scope.treeElements[0]].concat($scope.treeElements[0].children);
                $scope.profileToSave = row.active;
                $scope.subSelectProfile = "profile";
                if(row.locked) {
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

                }
                $scope.edit = true;
                $scope.eventlog = true;
                $timeout(function() {
                    $anchorScroll('edit-view');
                }, 0);
            });
        }
    };
    //Get data for eventlog view
    function getEventlogData() {
        listViewService.getEventlogData().then(function(value){
            $scope.eventTypeCollection = value;
        });
    };
    //populating select view
    $scope.selectRowCollection = [];
    $scope.selectRowCollapse = [];
    //Gets all submission agreement profiles
    $scope.getSaProfiles = function(ip) {
        listViewService.getSaProfiles(ip).then(function(value) {
            $scope.saProfile = value;
            $scope.getSelectCollection(value.profile, ip)
            $scope.selectRowCollection = $scope.selectRowCollapse;
        });
    };
    //Get All profiles and populates the select view table array
    $scope.getSelectCollection = function (sa, ip) {
        $scope.selectRowCollapse = listViewService.getProfilesFromIp(sa, ip)
    };

    //Include the given profile type in the SA
    $scope.includeProfileType = function(type){
        var sendData = {
            "type": type
        };

        var uri = $scope.saProfile.profile.url+"include-type/";
         $http({
            method: 'POST',
            url: uri,
            data: sendData
        })
        .success(function (response) {
        })
        .error(function (response) {
            alert(response.status);
        });
    };

    //Exclude the given profile type in the SA
    $scope.excludeProfileType = function(type){
        var sendData = {
            "type": type
        };

        var uri = $scope.saProfile.profile.url+"exclude-type/";
         $http({
            method: 'POST',
            url: uri,
            data: sendData
        })
        .success(function (response) {
        })
        .error(function (response) {
            alert(response.status);
        });
    };
    //Make a profile "Checked"
    $scope.setCheckedProfile = function(type, checked){
        var uri = $scope.ip.url+"check-profile/";
         $http({
            method: 'PUT',
            url: uri,
            data: {
                type: type,
                checked: checked
            }
        })
        .success(function (response) {
        })
    };

    //Change the standard profile of the same type as given profile for an sa
    $scope.changeProfile = function(profile, row){
        var sendData = {"new_profile": profile.id};
        var uri = $scope.ip.url+"change-profile/";
         $http({
            method: 'PUT',
            url: uri,
            data: sendData
         })
         .success(function (response) {
             if($scope.edit) {
                 $scope.profileClick(row);
             }
        })
        .error(function (response) {
            alert(response.status);
        });

    };
    //Changes SA profile for selected ip
    $scope.changeSaProfile = function (sa, ip, oldSa_idx) {
        $http({
            method: 'PATCH',
            url: ip.url,
            data: {
                'SubmissionAgreement': sa.url
            }
        }).then(function(response){
            $scope.getSelectCollection(sa, ip);
            $scope.selectRowCollection = $scope.selectRowCollapse;
        }, function(response) {
            $scope.saProfile.profile = $scope.saProfile.profiles[oldSa_idx];
        });
    }
    //Toggle visibility of profiles in select view
    $scope.showHideAllProfiles = function() {
        if($scope.selectRowCollection == {} || $scope.profilesCollapse){
            $scope.profilesCollapse = false;
            $scope.edit = false;
            $scope.eventlog = false
        } else{
            $scope.profilesCollapse = true;
        }
    };

    //Saves edited profile and creates a new profile instance with given name
    vm.onSubmit = function(new_name) {
        profileUrl = $scope.profileToSave.profile || $scope.profileToSave.url
        var sendData = {
            "specification_data": vm.profileModel,
            "information_package": $scope.ip.id,
            "new_name": new_name,
            "structure": $scope.treeElements[0].children
        };
        $http({
            method: 'POST',
            url: profileUrl+"save/",
            data: sendData
        })
        .then(function(response) {
            var profileType = 'profile_' + $scope.profileToSave.profile_type;
            var newProfile = response.data;
            newProfile.profile_name = newProfile.name;
            listViewService.getIp($scope.ip.url).then(function(result) {
                $scope.getSelectCollection($scope.saProfile.profile, result);
                $scope.selectRowCollection = $scope.selectRowCollapse;
            });
            $scope.edit = false;
            $scope.eventlog = false;
            $anchorScroll('select-view');
        }, function(response) {
            alert(response.status);
        });
    };
    $scope.colspan = 9;
    //Decides visibility of stepTask info page
    $scope.stepTaskInfoShow = false;
    //Decides visibility of status view
    $scope.statusShow = false;
    //Decides visibility of events view
    $scope.eventShow = false;
    //Decides visibility of select view
    $scope.select = false;
    //Decides visibility of sub-select view
    $scope.subSelect = false;
    //Decides visibility of edit view
    $scope.edit = false;
    //Decides visibility of eventlog view
    $scope.eventlog = false;
    //Html popover template for currently disabled
    $scope.htmlPopover = $sce.trustAsHtml('<font size="3" color="red">Currently disabled</font>');

    //Toggle visibility of select view
    $scope.toggleSelectView = function () {
        if($scope.select == false){
            $scope.select = true;
        } else {
            $scope.select = false;
        }
    };
    //Toggle visibility of sub-select view
    $scope.toggleSubSelectView = function () {
        if($scope.subSelect == false){
            $scope.subSelect = true;
        } else {
            $scope.subSelect = false;
        }
    };
    //Toggle visibility of edit view
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
    //Create and show modal when saving a profile
    vm.saveModal = function(){
        if (vm.editForm.$valid) {
            vm.options.updateInitialValue();
            var modalInstance = $uibModal.open({
                animation: true,
                ariaLabelledBy: 'modal-title',
                ariaDescribedBy: 'modal-body',
                templateUrl: 'static/frontend/views/enter-profile-name-modal.html',
                controller: 'ModalInstanceCtrl',
                controllerAs: '$ctrl'
            })
            modalInstance.result.then(function (data) {
                vm.onSubmit(data.name);
            }, function () {
                $log.info('modal-component dismissed at: ' + new Date());
            });
        }
    }
    //Create and show modal for creating new ip
    $scope.newIpModal = function () {
        var modalInstance = $uibModal.open({
            animation: true,
            ariaLabelledBy: 'modal-title',
            ariaDescribedBy: 'modal-body',
            templateUrl: 'static/frontend/views/new-ip-modal.html',
            controller: 'ModalInstanceCtrl',
            controllerAs: '$ctrl'
        })
        modalInstance.result.then(function (data) {
            $scope.prepareIp(data.label);
        }, function () {
            $log.info('modal-component dismissed at: ' + new Date());
        });
    }
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
    //Remove ip
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
    //Creates and shows modal for profile lock.
    $scope.lockProfileModal = function (profiles) {
        $scope.profileToSave = profiles;
        var modalInstance = $uibModal.open({
            animation: true,
            ariaLabelledBy: 'modal-title',
            ariaDescribedBy: 'modal-body',
            templateUrl: 'static/frontend/views/lock-profile-modal.html',
            scope: $scope,
            controller: 'ModalInstanceCtrl',
            controllerAs: '$ctrl'
        })
        modalInstance.result.then(function (data) {
            $scope.lockProfile($scope.profileToSave);
        }, function () {
            $log.info('modal-component dismissed at: ' + new Date());
        });
    }
    //Lock a profile
    $scope.lockProfile = function (profiles) {
        var profileUrl;
        if(profiles.active.profile) {
            profileUrl = profiles.active.profile;
        } else {
            profileUrl = profiles.active.url;
        }
        return $http({
            method: 'POST',
            url: profileUrl+"lock/",
            data: {
                information_package: $scope.ip.id,
            }
        }).then(function (response) {
            profiles.locked = true;
            $scope.edit = false;
            $scope.eventlog = false;
            $scope.getListViewData();
            updateListViewConditional();
            return {status: response.status, profile: profiles};
        }, function(error) {
            if(error.status == 400) {
                showRequiredProfileFields(profiles);
            }
            return {status: error.status, profile: profiles};
        });
    }
    function showRequiredProfileFields(row) {
        if (row.active.name){
            var profileUrl = row.active.url;
        } else {
            var profileUrl = row.active.profile;
        }
        $http({
            method: 'GET',
            url: profileUrl,
            params: {
                'sa': $scope.saProfile.profile.id,
                'ip': $scope.ip.id
            }
        }).then(function(response) {
            response.data.profile_name = response.data.name;
            row.active = response.data;
            row.profiles = [response.data];
            $scope.selectProfile = row;
            vm.profileModel = angular.copy(row.active.specification_data);
            vm.profileFields = row.active.template;
            $scope.treeElements =[{name: $translate.instant('ROOT'), type: "folder", children: angular.copy(row.active.structure)}];
            $scope.expandedNodes = [$scope.treeElements[0]].concat($scope.treeElements[0].children);
            $scope.profileToSave = row.active;
            $scope.subSelectProfile = "profile";
            if(row.locked) {
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

            }
            $scope.edit = true;
            $scope.eventlog = true;
            $timeout(function() {
                $anchorScroll('edit-view');
                vm.editForm.$setSubmitted();
            }, 0);
        });
    }
    //Creates modal for lock SA
    $scope.lockSaModal = function(sa) {
        $scope.saProfile = sa;
        var modalInstance = $uibModal.open({
            animation: true,
            ariaLabelledBy: 'modal-title',
            ariaDescribedBy: 'modal-body',
            templateUrl: 'static/frontend/views/lock-sa-profile-modal.html',
            scope: $scope,
            controller: 'ModalInstanceCtrl',
            controllerAs: '$ctrl'
        })
        modalInstance.result.then(function (data) {
            $scope.lockSa($scope.saProfile);
        }, function () {
            $log.info('modal-component dismissed at: ' + new Date());
        });
    }
    //Lock a SA
    $scope.lockSa = function(sa) {
        ip = $scope.ip;

        $http({
            method: 'POST',
            url: sa.profile.url+"lock/",
            data: {
                ip: ip.id
            }
        }).then(function (response) {
            sa.locked = true;
            $scope.edit = false;
            $scope.eventlog = false;
            $scope.getListViewData();
        });
    }
    //Create and initialize new ip
    $scope.prepareIp = function (label) {
        listViewService.prepareIp(label).then(function() {
            $timeout(function(){
                $scope.getListViewData();
                updateListViewConditional();
            }, 1000);
        });
    }
    //Update ip list view with an interval
    //Update only if status < 100 and no step has failed in any IP
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

    //Opens a new instance of a modal window
    $scope.openModal = function(modalTemplate) {
        var modalInstance = $uibModal.open({
            animation: true,
            ariaLabelledBy: 'modal-title',
            ariaDescribedBy: 'modal-body',
            templateUrl: 'enter-profile-name-modal.html',
            controller: 'ModalInstanceCtrl',
            controllerAs: '$ctrl'
        })
        modalInstance.result.then(function (data) {
            vm.onSubmit(data.name);
        }, function () {
            $log.info('modal-component dismissed at: ' + new Date());
        });
    };
    //Reload current view
    $scope.reloadPage = function (){
        $state.reload();
    }
    /*
     * Edit view map structure tree
     */

    /*
     * Formly form  structure
     */
    vm.treeEditModel = {
    };
    vm.treeEditFields = [
    {
        "templateOptions": {
            "type": "text",
            "label": $translate.instant('NAME'),
            "required": true
        },
        "type": "input",
        "key": "name"
    },
    {
        "templateOptions": {
            "type": "text",
            "label": $translate.instant('TYPE'),
            "options": [{name: "folder", value: "folder"},{name: "file", value: "file"}],
            "required": true
        },
        "type": "select",
        "key": "type",
    },
    {
        "templateOptions": {
            "type": "text",
            "label": $translate.instant('USE'),
            "options": [
			    {name: "content", value: "content"},
                {name: "preservation_description_file", value: "preservation_description_file"},
                {name: "mets_file", value: "mets_file"},
                {name: "archival_description_file", value: "archival_description_file"},
                {name: "authoritive_information_file", value: "authoritive_information_file"},
                {name: "xsd_files", value: "xsd_files"}

            ],
        },
        "hideExpression": function($viewValue, $modelValue, scope){
            return scope.model.type != "file";
        },
        "expressionProperties": {
            "templateOptions.required": function($viewValue, $modelValue, scope) {
                return scope.model.type == "file";
            }
        },
        "type": "select-tree-edit",
        "key": "use",
        "defaultValue": "Pick one",
    }

    ];

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
        },
        isLeaf: function(node) {
            return node.type == "file";
        },
        equality: function(node1, node2) {
            return node1 === node2;
        },
        isSelectable: function(node) {
            return !$scope.updateMode.active && !$scope.addMode.active;
        }
    };
    //Generates test data for map structure tree
    function createSubTreeExampleData(level, width, prefix) {
        if (level > 0) {
            var res = [];
            // if (!parent) parent = res;
            for (var i = 1; i <= width; i++) {
                res.push({
                    "name": "Node " + prefix + i,
                    "type": "folder",
                    "children": createSubTreeExampleData(level - 1, width, prefix + i + ".")
                });
            }

            return res;
        }
        else return [];
    }
    //Populate map structure tree view given tree width and amount of levels
    function getStructure(profileUrl) {
        listViewService.getStructure(profileUrl).then(function(value) {
           $scope.treeElements =[{name: $translate.instant('ROOT'), type: "folder", children: value}];
           $scope.expandedNodes = [$scope.treeElements[0]].concat($scope.treeElements[0].children);
        });
    }
    $scope.treeElements = [];//[{name: "Root", type: "Folder", children: createSubTree(3, 4, "")}];
    $scope.currentNode = null;
    $scope.selectedNode = null;
    //Add node to map structure tree view
    $scope.addNode = function(node) {
        var dir = {
            "name": vm.treeEditModel.name,
            "type": vm.treeEditModel.type,
        };
        if(vm.treeEditModel.type == "folder") {
            dir.children = [];
        }
        if(vm.treeEditModel.type == "file"){
            dir.use = vm.treeEditModel.use;
        }
        if(node == null){
            $scope.treeElements[0].children.push(dir);
        } else {
            node.node.children.push(dir);
        }
        $scope.exitAddMode();
        $anchorScroll('edit-tree');
    };
    //Remove node from map structure tree view
    $scope.removeNode = function(node) {
        if(node.parentNode == null){
            //$scope.treeElements.splice($scope.treeElements.indexOf(node.node), 1);
            return;
        }
        node.parentNode.children.forEach(function(element) {
            if(element.name == node.node.name) {
                node.parentNode.children.splice(node.parentNode.children.indexOf(element), 1);
            }
        });
    };
    $scope.treeItemClass = "";
    $scope.addMode = {
        active: false
    };
    //Enter "Add-mode" which shows a form
    //for adding a node to the map structure
    $scope.enterAddMode = function(node) {
        $scope.addMode.active = true;
        $('.tree-edit-item').draggable('disable');
    };
    //Exit add mode and return to default
    //map structure edit view
    $scope.exitAddMode = function() {
        $scope.addMode.active = false;
        $scope.treeItemClass = "";
        resetFormVariables();
        $('.tree-edit-item').draggable('enable');
    };
    $scope.updateMode = {
        node: null,
        active: false
    };

    //Enter update mode which shows form for updating a node
    $scope.enterUpdateMode = function(node, parentNode) {
        if(parentNode == null) {
            alert("Root directory can not be updated");
            return;
        }
        if($scope.updateMode.active && $scope.updateMode.node === node) {
            $scope.exitUpdateMode();
        } else {
            $scope.updateMode.active = true;
            vm.treeEditModel.name = node.name;
            vm.treeEditModel.type = node.type;
            vm.treeEditModel.use = node.use;
            $scope.updateMode.node = node;
            $('.tree-edit-item').draggable('disable');
        }
    };

    //Exit update mode and return to default map-structure editor
    $scope.exitUpdateMode = function() {
        $scope.updateMode.active = false;
        $scope.updateMode.node = null;
        $scope.selectedNode = null;
        $scope.currentNode = null;
        resetFormVariables();
        $('.tree-edit-item').draggable('enable');
    };
    //Resets add/update form fields
    function resetFormVariables() {
                vm.treeEditModel = {};
    };
    //Update current node variable with selected node in map structure tree view
    $scope.updateCurrentNode = function(node, selected, parentNode) {
        if(selected) {
            $scope.currentNode = {"node": node, "parentNode": parentNode};
        } else {
            $scope.currentNode = null;
        }
    };
    //Update node values
    $scope.updateNode = function(node) {
        if(vm.treeEditModel.name != ""){
            node.node.name = vm.treeEditModel.name;
        }
        if(vm.treeEditModel.type != ""){
            node.node.type = vm.treeEditModel.type;
        }
        if(vm.treeEditModel.use != ""){
            node.node.use = vm.treeEditModel.use;
        }
        $scope.exitUpdateMode();
    };
    //Select function for clicking a node
    $scope.showSelected = function(node, parentNode) {
        $scope.selectedNode = node;
        $scope.updateCurrentNode(node, $scope.selectedNode, parentNode);
        if($scope.updateMode.active){
            $scope.enterUpdateMode(node, parentNode);
        }
    };
    //Submit function for either Add or update
    $scope.treeEditSubmit = function(node) {
        if($scope.addMode.active) {
            $scope.addNode(node);
        } else if($scope.updateMode.active) {
            $scope.updateNode(node);
        } else {
            return;
        }
    }
    //context menu data
    $scope.menuOptions = function(item) {
        if($scope.addMode.active || $scope.updateMode.active){
            return [];
        }
        return [
            [$translate.instant('ADD'), function ($itemScope, $event, modelValue, text, $li) {
                $scope.showSelected($itemScope.node, $itemScope.$parentNode);
                $scope.enterAddMode($itemScope.node);
            }],

            [$translate.instant('REMOVE'), function ($itemScope, $event, modelValue, text, $li) {
                $scope.updateCurrentNode($itemScope.node, true, $itemScope.$parentNode);
                $scope.removeNode($scope.currentNode);
                $scope.selectedNode = null;
            }],
            [$translate.instant('UPDATE'), function ($itemScope, $event, modelValue, text, $li) {
                $scope.showSelected($itemScope.node, $itemScope.$parentNode);
                $scope.enterUpdateMode($itemScope.node, $itemScope.$parentNode);
            }]
        ];
    };
    $scope.getProfilesFromIp = function(ip, sa) {
        listViewService.getProfilesFromIp(ip, sa).then(function(result) {
            //$scope.selectCollapse = result;
        });
    }
    $scope.getProfiles = function(profile) {
        listViewService.getProfilesMin(profile.profile_type).then(function(result) {
            if(profile.active != null) {
            result.forEach(function(prof) {
                if(angular.isUndefined(profile.active.profile)) {
                    if(prof.url == profile.active.url) {
                        profile.active = prof;
                }
                }
                if(prof.url == profile.active.profile) {
                    profile.active = prof;
                }
            });
        }
            profile.profiles = result;
        })
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
    $scope.showLockAllButton = function(profiles){
        return profiles.some(function(elem){
            return elem.checked && !elem.locked;
        });
    };
    $scope.lockAllIncludedModal = function (profiles) {
        $scope.profileToSave = profiles;
        var modalInstance = $uibModal.open({
            animation: true,
            ariaLabelledBy: 'modal-title',
            ariaDescribedBy: 'modal-body',
            templateUrl: 'static/frontend/views/lock_all_included_modal.html',
            scope: $scope,
            controller: 'ModalInstanceCtrl',
            controllerAs: '$ctrl'
        })
        modalInstance.result.then(function (data) {
            $scope.lockAllIncluded();
        }, function () {
            $log.info('modal-component dismissed at: ' + new Date());
        });
    }
    $scope.lockAllIncluded = function() {
        var failure = false;
        var prom = [];
        $scope.selectRowCollection.forEach(function(profile) {
            if(profile.checked && !profile.locked) {
                prom.push($scope.lockProfile(profile));
            }
        });
        $q.all(prom).then(function (results) {
            var failure = false;
            var failedProfile = null;
            results.forEach(function(result) {
                if(result.status == 400) {
                    failure = true;
                    failedProfile = result.profile;
                }
            });
            if(failure && failedProfile != null) {
                showRequiredProfileFields(failedProfile);
            } else {
                $scope.select = false;
                $scope.edit = false;
                $scope.eventLog = false;
                $anchorScroll();
            }
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
    $scope.extendedEqual = function(specification_data, model) {
        var returnValue = true;
        for(var prop in model) {
            if(model[prop] == "" && angular.isUndefined(specification_data[prop])){
                returnValue = false;
            }
        }
        if(returnValue) {
            return angular.equals(specification_data, model);
        } else {
            return true;
        }
    };
});
