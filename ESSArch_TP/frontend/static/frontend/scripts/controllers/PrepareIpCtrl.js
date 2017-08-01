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

angular.module('myApp').controller('PrepareIpCtrl', function (IP, SA, Profile, $log, $uibModal, $timeout, $scope, $window, $location, $sce, $http, myService, appConfig, $state, $stateParams, $rootScope, listViewService, $interval, Resource, $translate, $cookies, $cookieStore, $filter, $anchorScroll, PermPermissionStore, $q, $controller){
    var vm = this;
    var ipSortString = "Preparing,Prepared";
    $controller('BaseCtrl', { $scope: $scope, vm: vm, ipSortString: ipSortString });

    $scope.selectedProfileRow = {profile_type: "", class: ""};

    $scope.setSelectedProfile = function(row) {
        $scope.selectRowCollection.forEach(function(profileRow) {
            if(profileRow.profile_type == $scope.selectedProfileRow.profile_type){
                profileRow.class = "";
            }
        });
        if(row.profile_type == $scope.selectedProfileRow.profile_type && $scope.edit){
            $scope.selectedProfileRow = {profile_type: "", class: ""};
        } else {
            row.class = "selected";
            $scope.selectedProfileRow = row;
        }
    };
    //Click function for Ip table
    $scope.ipTableClick = function(row) {
        if($scope.select && $scope.ip.id== row.id){
            $scope.select = false;
            $scope.ip = null;
            $rootScope.ip = null;
            $scope.filebrowser = false;
        } else {
            $scope.ip = row;
            $rootScope.ip = $scope.ip;
            $scope.getSaProfiles($scope.ip);
            $scope.select = true;
        }
        $scope.eventlog = false;
        $scope.edit = false;
        $scope.eventShow = false;
        $scope.statusShow = false;
    };

    // Progress bar max value
    //funcitons for select view
    vm.profileModel = {};
    vm.profileFields=[];
    vm.options = {};
    //Click funciton for sa view
    $scope.saClick = function(row){
        if ($scope.selectProfile == row && $scope.editSA){
            $scope.editSA = false;
        } else {
            $scope.eventlog = false;
            $scope.edit = false;

            var chosen = row.profile
            $scope.selectProfile = row;

            vm.profileFields = chosen.template;
            vm.profileOldModel = {};
            vm.profileModel = {};

            // only keep fields defined in template
            vm.profileFields.forEach(function(field){
                vm.profileOldModel[field.key] = chosen[field.key];
                vm.profileModel[field.key] = chosen[field.key];
            })


            $scope.profileToSave = chosen;
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
            $scope.editSA = true;
        }
    };
    //Click funciton for profile view
    $scope.profileClick = function(row){
        if ($scope.selectProfile == row && $scope.edit){
            $scope.eventlog = false;
            $scope.edit = false;
        } else {
            $scope.editSA = false;
            $scope.closeAlert();
            var profileId;
            if (row.active.name){
                profileId = row.active.id;
            } else {
                profileId = row.active.profile;
            }
            getAndShowProfile(profileId, row);
        }
    };

    function getAndShowProfile(profileId, row) {
        Profile.get({
            id: profileId,
            sa: $scope.saProfile.profile.id,
            ip: $scope.ip.id
        }).$promise.then(function (resource) {
            resource.profile_name = resource.name;
            row.active = resource;
            row.profiles = [resource];
            $scope.selectProfile = row;
            vm.profileOldModel = row.active.specification_data;
            vm.profileModel = angular.copy(row.active.specification_data);
            vm.profileFields = row.active.template;
            $scope.treeElements = [{ name: 'root', type: "folder", children: angular.copy(row.active.structure) }];
            $scope.expandedNodes = [$scope.treeElements[0]].concat($scope.treeElements[0].children);
            $scope.profileToSave = row.active;
            if (row.locked) {
                vm.profileFields.forEach(function (field) {
                    if (field.fieldGroup != null) {
                        field.fieldGroup.forEach(function (subGroup) {
                            subGroup.fieldGroup.forEach(function (item) {
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
        });
    }

    //Include the given profile type in the SA
    $scope.includeProfileType = function(type){
        var sendData = {
            "type": type
        };
        SA.includeType(
            angular.extend({ id: $scope.saProfile.profile.id} , sendData)
        ).$promise.then(function success(response){
        }, function error(response){
            alert(response.status);
        });
    };

    //Exclude the given profile type in the SA
    $scope.excludeProfileType = function(type){
        var sendData = {
            "type": type
        };
        SA.excludeType(
            angular.extend({ id: $scope.saProfile.profile.id }, sendData)
        ).$promise.then(function success(response){
        }, function error(response){
            alert(response.status);
        });
    };
    //Make a profile "Checked"
    $scope.setCheckedProfile = function(type, checked){
        IP.checkProfile({
            id: $scope.ip.id,
            type: type,
            checked: checked
        }).$promise.then(function success(response){
        }, function error(response){
        });
    };

    //Change the standard profile of the same type as given profile for an sa
    $scope.changeProfile = function(profile, row){
        var sendData = {"new_profile": profile.id};
        var uri = $scope.ip.url+"change-profile/";
        IP.changeProfile(
            angular.extend({id: $scope.ip.id}, sendData)
        ).$promise.then(function success(response){
            row.active = profile;
            if($scope.edit && row == $scope.selectedProfileRow) {
                $scope.edit = false;
                $scope.profileClick(row);
            }
        }, function error(response){
            alert(response.status);
        });
    };
    //Changes SA profile for selected ip
    $scope.changeSaProfile = function (sa, ip, oldSa_idx) {
        IP.changeSa({
            id: ip.id,
            submission_agreement: sa.url
        }).$promise.then(function(response){
            $scope.getSelectCollection(sa, ip);
            $scope.selectRowCollection = $scope.selectRowCollapse;
            if($scope.editSA) {
                $scope.saClick({profile: sa});
            }
            $scope.saProfile.profile = sa;
        }, function(response) {
            $scope.saProfile.profile = $scope.saProfile.profiles[oldSa_idx];
        });
    }

    //Saves edited SA and creates a new SA instance with given name
    vm.onSASubmit = function(new_name) {
        SA.save({
            id: $scope.profileToSave.id,
            data: vm.profileModel,
            information_package: $scope.ip.id,
            new_name: new_name,
        }).$promise.then(function(resource) {
            $scope.editSA = false;
            var old = $scope.saProfile.profiles.indexOf($scope.saProfile.profile);
            $scope.saProfile.profiles.push(resource);
            $scope.changeSaProfile(resource, $scope.ip, old);
        }, function(resource) {
            console.log(resource.status);
        });
    };
    //Saves edited profile and creates a new profile instance with given name
    vm.onSubmit = function(new_name) {
        profileUrl = $scope.profileToSave.profile || $scope.profileToSave.url
        var sendData = {

        };
        Profile.save({
            id: $scope.profileToSave.profile || $scope.profileToSave.id,
            specification_data: vm.profileModel,
            new_name: new_name,
            structure: $scope.treeElements[0].children
        }).$promise.then(function(resource) {
                var profileType = 'profile_' + $scope.profileToSave.profile_type;
                var newProfile = resource;
                $scope.selectedProfileRow.profiles.push(newProfile);
                newProfile.profile_name = newProfile.name;
                $scope.changeProfile(newProfile, $scope.selectedProfileRow);
                $scope.edit = false;
                $scope.eventlog = false;
            }, function(resource) {
                alert(resource.status);
            });
    };
    $scope.optionalOptions = true;

    //Create and show modal when saving an SA
    vm.saveSAModal = function(){
        if (vm.editForm.$valid) {
            vm.options.updateInitialValue();
            var modalInstance = $uibModal.open({
                animation: true,
                ariaLabelledBy: 'modal-title',
                ariaDescribedBy: 'modal-body',
                templateUrl: 'static/frontend/views/save_sa_modal.html',
                controller: 'ModalInstanceCtrl',
                controllerAs: '$ctrl'
            })
            modalInstance.result.then(function (data) {
                vm.onSASubmit(data.name);
            }, function () {
                $log.info('modal-component dismissed at: ' + new Date());
            });
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
        modalInstance.closed.then(function (data) {
            $scope.getListViewData();
            vm.updateListViewConditional();
        });
    }

    $scope.profileToLock = null;
    //Creates and shows modal for profile lock.
    $scope.lockProfileModal = function (profiles) {
        $scope.profileToLock = profiles;
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
            $scope.lockProfile($scope.profileToLock);
        }, function () {
            $log.info('modal-component dismissed at: ' + new Date());
        });
    }
    //Lock a profile
    $scope.lockProfile = function (profiles) {
        $scope.closeAlert();
        var profileId;
        if(profiles.active.profile) {
            profileId = profiles.active.profile;
        } else {
            profileId = profiles.active.id;
        }
        return Profile.lock({
            id: profileId,
            information_package: $scope.ip.id,
        }).$promise.then(function (response) {
            profiles.locked = true;
            $scope.edit = false;
            $scope.eventlog = false;
            $scope.getListViewData();
            vm.updateListViewConditional();
            return {status: response.status, profile: profiles};
        }, function(error) {
            if(error.status == 400) {
                showRequiredProfileFields(profiles);
            }
            return {status: error.status, profile: profiles};
        });
    }

    $scope.lockAlert = null;
    $scope.alerts = {
        lockError: { type: 'danger', msg: 'LOCK_ERROR', name: '', profile_type: '' },
    };
    $scope.closeAlert = function() {
        $scope.lockAlert = null;
    }
    function showRequiredProfileFields(row) {
        if($scope.edit) {
            $scope.lockAlert = $scope.alerts.lockError;
            $scope.lockAlert.name = row.active.profile_name;
            $scope.lockAlert.profile_type = row.active.profile_type;
            vm.editForm.$setSubmitted();
            return;
        }
        if (row.active.name){
            var profileId = row.active.id;
        } else {
            var profileId = row.active.profile;
        }
        Profile.get({
            id: profileId,
            sa: $scope.saProfile.profile.id,
            ip: $scope.ip.id
        }).$promise.then(function(resource) {
            resource.profile_name = resource.name;
            row.active = resource;
            row.profiles = [resource];
            $scope.selectProfile = row;
            vm.profileModel = angular.copy(row.active.specification_data);
            vm.profileFields = row.active.template;
            $scope.treeElements =[{name: 'root', type: "folder", children: angular.copy(row.active.structure)}];
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
        SA.lock({
            id: sa.profile.id,
            ip: $scope.ip.id
        }).$promise.then(function (response) {
            sa.locked = true;
            $scope.edit = false;
            $scope.eventlog = false;
            $scope.getListViewData();
        });
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
            // File uses
            "templateOptions": {
                "type": "text",
                "label": $translate.instant('USE'),
                "options": [
                    {name: "Premis file", value: "preservation_description_file"},
                    {name: "Mets file", value: "mets_file"},
                    {name: "Archival Description File", value: "archival_description_file"},
                    {name: "Authoritive Information File", value: "authoritive_information_file"},
                    {name: "XSD Files", value: "xsd_files"}

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
    function getStructure(profileId) {
        listViewService.getStructure(profileId).then(function(value) {
            $scope.treeElements =[{name: 'root', type: "folder", children: value}];
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
    $scope.treeEditOptions = function(item) {
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

    $scope.getProfiles = function(profile) {
        listViewService.getProfilesMin(profile.profile_type).then(function(result) {
            if(profile.active != null) {
                result.forEach(function(prof) {
                    if(angular.isUndefined(profile.active.profile)) {
                        if(prof.id == profile.active.id) {
                            profile.active = prof;
                        }
                    }
                    if(prof.id == profile.active.profile) {
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
        IP.unlockProfile({
            id: $scope.ip.id,
            type: profile.active.profile_type
        }).$promise.then(function(response){
            profile.locked = false;
            if($scope.edit && profile.active.id === $scope.selectedProfileRow.active.id) {
                getAndShowProfile(profile.active.id, profile);
            }
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
});
