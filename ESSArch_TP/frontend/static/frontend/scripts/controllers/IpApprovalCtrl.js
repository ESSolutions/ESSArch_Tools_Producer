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

angular.module('myApp').controller('IpApprovalCtrl', function (IP, Profile, $log, $scope, myService, appConfig, $http, $timeout, $state, $stateParams, $rootScope, listViewService, $interval, Resource, $uibModal, $translate, $filter, $anchorScroll, PermPermissionStore, $cookies, $controller){
    var vm = this;
    var ipSortString = "Uploaded,Creating";
    $controller('BaseCtrl', { $scope: $scope, vm: vm, ipSortString: ipSortString });
    $scope.ipSelected = false;

    //Click function for ip table objects
    $scope.ipTableClick = function(row) {
        if($scope.select && $scope.ip.id== row.id){
            $scope.select = false;
            $scope.eventlog = false;
            $scope.ip = null;
            $rootScope.ip = null;
            $scope.filebrowser = false;
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


    //funcitons for select view
    vm.profileModel = {};
    vm.profileFields=[];
    //Click function for profile pbject
    $scope.profileClick = function(row){
        if ($scope.selectProfile == row && $scope.edit){
            $scope.edit = false;
        } else {
            if(row.active) {
                console.log(row)
                Profile.get({
                    id: row.active.profile,
                    ip: $scope.ip.id
                }).$promise.then(function(resource) {
                    $scope.profileToSave = row.active;
                    $scope.selectProfile = row;
                    vm.profileModel = resource.specification_data;
                    vm.profileFields = resource.template;
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
                    vm.getEventlogData();
                });
            }
        }
    };

    //Creates and shows modal with task information
    $scope.createDisabled = false;
    //Executes Create sip on an ip
    $scope.createSip = function (ip) {
        $scope.createDisabled = true;
        IP.create({
            id: ip.id,
            validators: vm.validatorModel,
            file_conversion: vm.fileConversionModel.file_conversion,
        }).$promise.then(function (response) {
            $scope.select = false;
            $scope.edit = false;
            $scope.eventlog = false;
            $scope.filebrowser = false;
            $timeout(function () {
                $scope.getListViewData();
                vm.updateListViewConditional();
            }, 1000);
            $anchorScroll();
        }).finally(function () {
            $scope.createDisabled = false;
        });
    };

    $scope.unlockConditional = function(profile) {
        if(profile.profile_type == "sip") {
            $scope.unlockSipModal(profile);
        } else {
            $scope.unlockProfileModal(profile);
        }
    }

    //Unlock profile from current IP
    $scope.unlock = function(profile) {
        IP.unlockProfile({
                id: $scope.ip.id,
                type: profile.active.profile_type
        }).$promise.then(function(response){
            profile.locked = false;
            $scope.getListViewData();
            $scope.edit = false;
            $scope.select = false;
            $scope.eventlog = false;
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
