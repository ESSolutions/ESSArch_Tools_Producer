angular.module('myApp').controller('PrepareIpCtrl', function ($log, $uibModal, $timeout, $scope, $window, $location, $sce, $http, myService, appConfig, $state, $stateParams, $rootScope, listViewService, $interval, Resource, $translate, $cookies, $cookieStore){
    var vm = this;
    $scope.tree_data = [];
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
            field: "time_created",
            displayName: $scope.date,
        },
        {
            field: "status",
            displayName: $scope.state,
        },
        {
            field: "progress",
            displayName: $scope.status,
            cellTemplate: "<uib-progressbar ng-click=\"taskStepUndo(row.branch)\" class=\"progress active\" value=\"row.branch[col.field]\" type=\"success\"><b>{{row.branch[col.field]+\"%\"}}</b></uib-progressbar>"
        },
        {
            cellTemplate: "<a ng-click=\"treeControl.scope.taskStepUndo(row.branch)\" ng-if=\"(row.branch.status == 'SUCCESS' || row.branch.status == 'FAILURE') && !row.branch.undone && !row.branch.undo_type\" style=\"color: #a00\">{{'UNDO' | translate}}</a></br ><a ng-click=\"treeControl.scope.taskStepRedo(row.branch)\" ng-if=\"row.branch.undone\"style=\"color: #0a0\">{{'REDO' | translate}}</a>"
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
            console.log("UNDO");
            console.log(branch);
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
            console.log("REDO");
            console.log(branch);
        }, function() {
            console.log("error");
        });
    };
     $scope.currentStepTask = {id: ""}
    //Click funciton for steps and tasks
     $scope.stepTaskClick = function(branch) {
         if(branch.isTask){
             $http({
                 method: 'GET',
                 url: branch.url
             }).then(function(response){
                 console.log(response.data);
                 $scope.currentStepTask = response.data;
                 $scope.taskInfoModal();
             }, function(response) {
                 response.status;
             });
         }
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
         if ($scope.select || $scope.edit || $scope.eventlog) {
             $scope.ipTableClick(row);
         }
     }
     //Click function for status view
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
    //Get data for status view
    $scope.getTreeData = function(row) {
        listViewService.getTreeData(row).then(function(value) {
            $scope.tree_data = value;
        });
    }
    //Update status view data
    //Currently not up updating the value every n'th second.
    $scope.statusViewUpdate = function(row){
            $scope.getTreeData(row);
        if($scope.statusShow && false){
        $timeout(function() {
            $scope.getTreeData(row);
            $scope.statusViewUpdate(row);
        }, 5000)}
    };

     /*******************************************/
     /*Piping and Pagination for List-view table*/
     /*******************************************/

    var ctrl = this;
    this.itemsPerPage = 10;
    $scope.selectedIp = {id: "", class: ""};
    this.displayedIps = [];

    //Get data according to ip table settings and populates ip table
    this.callServer = function callServer(tableState) {
    $scope.tableState = tableState;
        ctrl.isLoading = true;

        var pagination = tableState.pagination;
        var start = pagination.start || 0;     // This is NOT the page number, but the index of item in the list that you want to use to display the table.
        var number = pagination.number;  // Number of entries showed per page.
        var pageNumber = start/number+1;

        Resource.getIpPage(start, number, pageNumber, tableState, $scope.selectedIp).then(function (result) {
            console.log(tableState);
            ctrl.displayedIps = result.data;
            tableState.pagination.numberOfPages = result.numberOfPages;//set the number of pages so the pagination can update
            ctrl.isLoading = false;
        });
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
             $scope.eventlog = false;
            $scope.edit = false;
        } else {
            $http({
                method: 'GET',
                url: row.url
            }).then(function (response) {
                $scope.getSaProfiles(response.data);
            });
            $scope.select = true;
            $scope.ip = row;
            $rootScope.ip = row;
        }
        $scope.eventShow = false;
        $scope.statusShow = false;
    };
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
            console.log(value);
        });
    }
    //Get data for list view
    $scope.getListViewData = function() {
        vm.callServer($scope.tableState);
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
        if(!row.locked){
            $scope.profileClick(row);
        }
    }
    vm.profileModel = {};
    vm.profileFields=[];
    //Click funciton for profile view
    $scope.profileClick = function(row){
        $scope.profileToSave = row;
        console.log(row);
        if ($scope.selectProfile == row && $scope.edit){
            $scope.eventlog = false;
            $scope.edit = false;
        } else {
            $scope.eventlog = true;
            getEventlogData();
            $scope.edit = true;
            $scope.selectProfile = row;
            vm.profileModel = row.profile.specification_data;
            vm.profileFields = row.profile.template;
            $scope.subSelectProfile = "profile";
        }
        console.log("selected profile: ");
        console.log($scope.selectProfile);
    };
    //GET data for eventlog view
    function getEventlogData() {
        listViewService.getEventlogData().then(function(value){
            $scope.statusNoteCollection = value;
        });
    };
    //populating select view
    $scope.selectRowCollection = [];
    $scope.selectRowCollapse = [];
    //Gets all submission agreement profiles
    $scope.getSaProfiles = function(ip) {
        console.log("current sa: ");
        console.log($scope.saProfile);
        listViewService.getSaProfiles(ip).then(function(value) {
            $scope.saProfile = value;
            $scope.getSelectCollection(value.profile, ip);
        });
    };
    //Get All profiles and populates the select view table array
    $scope.getSelectCollection = function (sa, ip) {
        $scope.selectRowCollapse = [];
            $scope.selectRowCollapse = listViewService.getSelectCollection(sa, ip);
            console.log($scope.selectRowCollapse);
    };
    //Updates the included profiles for an ip
    //Currently has no back end support
    $scope.updateIncludedProfiles = function(profile){
        if(profile.checked){
            $scope.saProfile.profile.includedProfiles.push(profile.profile_type);
        } else {
            for(i=0;i<$scope.saProfile.profile.includedProfiles.length;i++) {
                if($scope.saProfile.profile.includedProfiles[i] == profile.profile_type){
                    $scope.saProfile.profile.includedProfiles.splice(i,1);
                }
            }
        }
    }
    //Change the standard profile of the same type as given profile for an sa
    $scope.changeProfile = function(profile){
        var sendData = {"new_profile": profile.id};
        var uri = $scope.saProfile.profile.url+"change-profile/";
         $http({
            method: 'PUT',
            url: uri,
            data: sendData
        })
        .success(function (response) {
            console.log("sa updated with"+profile.id);
        })
        .error(function (response) {
            alert(response.status);
        });

    };
    //Changes SA profile for selected ip
    $scope.changeSaProfile = function (sa) {
        $http({
            method: 'PATCH',
            url: $scope.ip.url,
            data: {
                'SubmissionAgreement': sa.url
            }
        }).then(function(response){
            console.log(response);
        });
    }
    //Toggle visibility of profiles in select view
    $scope.showHideAllProfiles = function() {
        if($scope.selectRowCollection.length == 0){
            for(i = 0; i < $scope.selectRowCollapse.length; i++){
                $scope.selectRowCollection.push($scope.selectRowCollapse[i]);
            }
        } else {
            $scope.selectRowCollection = [];
        }
        $scope.profilesCollapse = !$scope.profilesCollapse;
    };
    //Populating edit view fields

    //Saves edited profile and creates a new profile instance with given name
    vm.onSubmit = function(new_name) {
        var uri = $scope.profileToSave.profile.url+"save/";
        var sendData = {"specification_data": vm.profileModel, "submission_agreement": $scope.saProfile.profile.id, "new_name": new_name};
        console.log(sendData);
        $http({
            method: 'POST',
            url: uri,
            data: sendData
        })
        .success(function (response) {
            alert(response.status);
            $scope.getSelectCollection($scope.saProfile.profile);
            $scope.getListViewData();
            $scope.edit = false;
            $scope.eventlog = false;
        })
        .error(function(response) {
            alert(response.status);
        });
    };
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
    $scope.saveModal = function(){
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
    //Creates and shows modal for profile lock.
    $scope.lockProfileModal = function () {
        var modalInstance = $uibModal.open({
            animation: true,
            ariaLabelledBy: 'modal-title',
            ariaDescribedBy: 'modal-body',
            templateUrl: 'static/frontend/views/lock-profile-modal.html',
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
    $scope.lockProfile = function (profileObject) {
        console.log(profileObject);
        $http({
            method: 'POST',
            url: profileObject.profile.url+"lock/",
            data: {
                information_package: $scope.ip.id,
                submission_agreement: $scope.saProfile.profile.id
            }
        }).then(function (response) {
            console.log("locked");
            $scope.profileToSave.locked = true;
            profileObject.locked = true;
            $scope.edit = false;
            $scope.eventlog = false;
            $scope.getListViewData();
            });
    }
    //Create and initialize new ip
    $scope.prepareIp = function (label) {
        listViewService.prepareIp(label).then(function() {
            $scope.getListViewData();
        });
    }
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
});
