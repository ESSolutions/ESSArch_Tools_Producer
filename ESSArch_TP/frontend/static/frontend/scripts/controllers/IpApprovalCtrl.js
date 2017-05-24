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

angular.module('myApp').controller('IpApprovalCtrl', function ($log, $scope, myService, appConfig, $http, $timeout, $state, $stateParams, $rootScope, listViewService, $interval, Resource, $uibModal, $translate, $filter, $anchorScroll, PermPermissionStore, $cookies, $controller){
    $controller('BaseCtrl', { $scope: $scope });
    var vm = this;
    var ipSortString = "Uploaded,Creating,Created";
    vm.itemsPerPage = $cookies.get('etp-ips-per-page') || 10;
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
    //Update status view data
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
            if(ip.ObjectIdentifierValue == $scope.selectedIp.ObjectIdentifierValue){
                ip.class = "";
            }
        });
        if(row.ObjectIdentifierValue == $scope.selectedIp.ObjectIdentifierValue){
            $scope.selectedIp = {ObjectIdentifierValue: "", class: ""};
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
    $scope.createDisabled = false;
    //Executes Create sip on an ip
    $scope.createSip = function (ip) {
        $scope.createDisabled = true;
        $http({
            method: 'POST',
            url: ip.url+"create/",
            data: {
                validators: vm.validatorModel,
                file_conversion: vm.fileConversionModel.file_conversion,
            }
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
            $scope.unlockProfileModal(profile);
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
            $scope.getListViewData();
            $scope.edit = false;
            $scope.select = false;
            $scope.eventlog = false;
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
            },
            "defaultValue": true,
            "type": "checkbox",
            "key": "validate_file_format",
        },
        {
            "templateOptions": {
                "type": "text",
                "label": $translate.instant('VALIDATEXMLFILE'),
            },
            "defaultValue": true,
            "type": "checkbox",
            "key": "validate_xml_file",
        },
        {
            "templateOptions": {
                "type": "text",
                "label": $translate.instant('VALIDATELOGICALPHYSICALREPRESENTATION'),
            },
            "defaultValue": true,
            "type": "checkbox",
            "key": "validate_logical_physical_representation",
        },
        {
            "templateOptions": {
                "type": "text",
                "label": $translate.instant('VALIDATEINTEGRITY'),
            },
            "defaultValue": true,
            "type": "checkbox",
            "key": "validate_integrity",
        }
    ];
    vm.fileConversionModel = {};
    vm.fileConversionFields = [
        {
            "templateOptions": {
                "type": "text",
                "label": $translate.instant('CONVERTFILES'),
                "options": [{name: $scope.yes, value: true},{name: $scope.no, value: false}],
            },
            "defaultValue": false,
            "type": "select",
            "key": "file_conversion",
        },
    ];
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
            $scope.getListViewData();
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
        $scope.unlockProfileModal = function (profile) {
        $scope.profileToSave = profile;
        var modalInstance = $uibModal.open({
            animation: true,
            ariaLabelledBy: 'modal-title',
            ariaDescribedBy: 'modal-body',
            templateUrl: 'static/frontend/views/unlock_profile_modal.html',
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
});

