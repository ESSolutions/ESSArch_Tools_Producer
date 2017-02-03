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

angular.module('myApp').controller('CollectContentCtrl', function($log, $uibModal, $timeout, $scope, $rootScope, $window, $location, $sce, $http, myService, appConfig, $state, $stateParams, listViewService, $interval, Resource, $q, $translate, $anchorScroll, PermPermissionStore, $cookies, $controller) {
    $controller('BaseCtrl', { $scope: $scope });
    var vm = this;
    var ipSortString = "Prepared,Uploading";
    vm.itemsPerPage = $cookies.get('etp-ips-per-page') || 10;
    vm.flowDestination = null;
    // List view
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
});
