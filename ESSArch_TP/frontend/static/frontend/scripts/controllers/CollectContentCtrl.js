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

angular.module('myApp').controller('CollectContentCtrl', function($log, $uibModal, $timeout, $scope, $rootScope, $window, $location, $sce, $http, myService, appConfig, $state, $stateParams, listViewService, $interval, Resource, $q, $translate, $anchorScroll, PermPermissionStore, $cookies) {
    var vm = this;
    var ipSortString = "Prepared,Uploading";
    vm.itemsPerPage = $cookies.get('etp-ips-per-page') || 10;
    $scope.updateIpsPerPage = function(items) {
        $cookies.put('etp-ips-per-page', items);
    };
    vm.flowDestination = null;
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
        if($scope.select && $scope.ip.id== row.id){
            $scope.select = false;
            $scope.eventlog = false;
        } else {
            $scope.ip = row;
            $rootScope.ip = row;
            $scope.deckGridInit($scope.ip);
            $scope.select = true;
            $scope.eventlog = true;
            $timeout(function() {
                $anchorScroll("select-wrap");
            }, 0);

        }
        $scope.uploadDisabled = false;
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
    //UPLOAD
    $scope.getFlowTarget = function() {
        return $scope.ip.url + 'upload/';
    };
    $scope.getQuery = function(FlowFile, FlowChunk, isTest) {
        return {destination: vm.flowDestination};
    };
    $scope.uploadDisabled = false;
    $scope.setUploaded = function(ip) {
        $scope.uploadDisabled = true;
        $http({
            method: 'POST',
            url: ip.url + "set-uploaded/"
        }).then(function(response){
            $scope.eventlog = false;
            $scope.select = false;
            $timeout(function() {
                $scope.getListViewData();
                updateListViewConditional();
            }, 1000);
            $scope.uploadDisabled = false;
            $anchorScroll();
        }, function(response) {
            $scope.uploadDisabled = false;
        });
    }
    $scope.updateListViewTimeout = function(timeout) {
        $timeout(function(){
            $scope.getListViewData();
        }, timeout);
    };
    //Deckgrid test
    $scope.previousGridArrays = [];
    $scope.previousGridArraysString = function() {
        var retString = "";
        $scope.previousGridArrays.forEach(function(card) {
            retString = retString.concat(card.name, "/");
        });
        return retString;
    }
    $scope.deckGridData = [];
    $scope.deckGridInit = function(ip) {
        listViewService.getDir(ip, null).then(function(dir) {
            $scope.deckGridData = dir;
        });
    };
    $scope.previousGridArray = function() {
        $scope.previousGridArrays.pop();
        listViewService.getDir($scope.ip, $scope.previousGridArraysString()).then(function(dir) {
            $scope.deckGridData = dir;
            $scope.selectedCard = null;
        });
    };
    $scope.updateGridArray = function(ip) {
        listViewService.getDir($scope.ip, $scope.previousGridArraysString()).then(function(dir) {
            $scope.deckGridData = dir;
        });
    };
    $scope.expandFile = function(ip, card) {
        if(card.type == "dir"){
            $scope.previousGridArrays.push(card);
            listViewService.getDir(ip,$scope.previousGridArraysString()).then(function(dir) {
                $scope.deckGridData = dir;
                $scope.selectedCard = null;
            });
        }
    };
    $scope.selectedCard = null;
    $scope.toggleCardSelect = function(card)  {
        if(card == $scope.selectedCard) {
            $scope.selectedCard = null;;
        } else {
            $scope.selectedCard = card;
        }
    };
    $scope.fileTransferFilter = function(file)
    {
        return file.isUploading();
    };
    $scope.checkPermission = function(permissionName) {
        return !angular.isUndefined(PermPermissionStore.getPermissionDefinition(permissionName));
    };
});
