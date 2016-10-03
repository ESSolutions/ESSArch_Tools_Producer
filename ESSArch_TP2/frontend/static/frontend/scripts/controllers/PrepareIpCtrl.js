angular.module('myApp').controller('PrepareIpCtrl', function ($log, $uibModal, $timeout, $scope, $window, $location, $sce, $http, myService, appConfig, $state, $stateParams, $rootScope, listViewService, $interval){
    var vm = this;
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
            cellTemplate: "<uib-progressbar ng-click=\"taskStepUndo(row.branch)\" class=\"progress active\" value=\"row.branch[col.field]\" type=\"success\"><b>{{row.branch[col.field]+\"%\"}}</b></uib-progressbar>"
        },
        {
            cellTemplate: "<a ng-click=\"treeControl.scope.taskStepUndo(row.branch)\" style=\"color: #a00\">Undo</a></br ><a ng-click=\"treeControl.scope.taskStepRedo(row.branch)\"style=\"color: #0a0\">Redo</a>"
        }
    ];
    $scope.myTreeControl = {};
    $scope.myTreeControl.scope = this;
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

    $scope.redirectAdmin = function () {
        $window.location.href="/admin/";
    }
    $scope.isCollapsed = true;
    $scope.toggleCollapse = function (step) {
        if(step.isCollapsed) {
            step.isCollapsed = false;
        } else {
            step.isCollapsed = true;
        }
        console.log(step.isCollapsed);
        console.log(step);
    };
    // List view
    $scope.changePath= function(path) {
        myService.changePath(path);
    };
    $scope.stateClicked = function(row){
        if($scope.statusShow && $scope.ip== row){
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
        $scope.ip= row;
    };
    $scope.getTreeData = function(row) {
        listViewService.getTreeData(row).then(function(value) {
            $scope.tree_data = value;
        });
    }
    $scope.statusViewUpdate = function(row){
            $scope.getTreeData(row);
        if($scope.statusShow && false){
        $timeout(function() {
            $scope.getTreeData(row);
            $scope.statusViewUpdate(row);
        }, 5000)}
    };
    $scope.ipTableClick = function(row) {
        console.log("ipobject clicked. row: "+row.Label);
        if($scope.select && $scope.ip.id== row.id){
            $scope.select = false;
             $scope.eventlog = false;
            $scope.edit = false;
        } else {
            $http({
                method: 'GET',
                url: row.url
            }).then(function (response) {
                $scope.ip = response.data;
                $rootScope.ip = response.data;
                $scope.getSaProfiles(response.data);
            });
            $scope.select = true;
        }
        $scope.eventShow = false;
        $scope.statusShow = false;
    };

    $scope.eventsClick = function (row) {
        if($scope.eventShow && $scope.ip== row){
            $scope.eventShow = false;
        } else {
            $scope.eventShow = true;
            listViewService.getEvents(row).then(function(value) {
                $scope.eventCollection = value;
                getEventlogData();
            });
            $scope.eventShow = true;
            $scope.statusShow = false;
        }
        $scope.select = false;
        $scope.edit = false;
        $scope.eventlog = false;
        $scope.ip= row;
    };
    $scope.addEvent = function(ip, eventType, eventDetail) {
        listViewService.addEvent(ip, eventType, eventDetail).then(function(value) {
            console.log(value);
        });
    }
    //Getting data for list view
    $scope.getListViewData = function() {
        listViewService.getListViewData().then(function(value){
            $scope.ipRowCollection = value;
        });
    };
    //updates every 5 seconds
    $scope.getListViewData();
    $interval(function(){$scope.getListViewData();}, 5000, false);
       //Getting data for status view
       //$scope.getStatusViewData();

    // Progress bar handler
    $scope.max = 100;
    //funcitons for select view
    $scope.profileClickCondition = function(row){
        if(!row.locked){
            $scope.profileClick(row);
        }
    }
    vm.profileModel = {};
    vm.profileFields=[];
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
    function getEventlogData() {
        listViewService.getEventlogData().then(function(value){
            $scope.statusNoteCollection = value;
        });
    };
    //populating select view
    $scope.selectRowCollection = [];
    $scope.selectRowCollapse = [];
    $scope.getSaProfiles = function(ip) {
        console.log("current sa: ");
        console.log($scope.saProfile);
        listViewService.getSaProfiles(ip).then(function(value) {
            $scope.saProfile = value;
            $scope.getSelectCollection(value.profile);
        });
    };

    $scope.getSelectCollection = function (sa) {
        $scope.selectRowCollapse = [];
        $scope.selectRowCollapse = listViewService.getSelectCollection(sa, $scope.ip);
        console.log($scope.selectRowCollapse);
    };
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
    // onSubmit function

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
            $scope.edit = false;
            $scope.eventlog = false;
        })
        .error(function(response) {
            alert(response.status);
        });
    };
    $scope.saveProfileEnabled = false;
    $scope.statusShow = false;
    $scope.eventShow = false;
    $scope.select = false;
    $scope.subSelect = false;
    $scope.edit = false;
    $scope.eventlog = false;
    $scope.htmlPopover = $sce.trustAsHtml('<font size="3" color="red">Currently disabled</font>');
    $scope.pages = ['Info', 'Prepare Ip', 'Selection', 'Extraction', 'Manage Data', 'IP Approval', 'IP Management'];
    $scope.selectedPage = $scope.pages[0];

    $scope.toggleSelectView = function () {
        if($scope.select == false){
            $scope.select = true;
        } else {
            $scope.select = false;
        }
    };
    $scope.toggleSubSelectView = function () {
        if($scope.subSelect == false){
            $scope.subSelect = true;
        } else {
            $scope.subSelect = false;
        }
    };
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
    $scope.toggleEventlogView = function() {
        if($scope.eventlog == false){
            $scope.eventlog = true;
        }else {
            $scope.eventlog = false;
        }
    }
    // Handle modal
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
    $scope.removeIp = function (ipObject) {
        $http({
            method: 'DELETE',
            url: ipObject.url
        }).then(function() {
            console.log("ip removed");
            $scope.ipRowCollection.splice($scope.ipRowCollection.indexOf(ipObject), 1);

        });
    }
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
            });
    }
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
    $scope.reloadPage = function (){
        $state.reload();
    }
});
angular.module('myApp').controller('ModalInstanceCtrl', function ($uibModalInstance) {
  var $ctrl = this;

  $ctrl.save = function () {
      $ctrl.data = {
        name: $ctrl.profileName
      };
        $uibModalInstance.close($ctrl.data);
  };
  $ctrl.prepare = function () {
      $ctrl.data = {
        label: $ctrl.label
      };
        $uibModalInstance.close($ctrl.data);
  };
  $ctrl.lock = function () {
      $ctrl.data = {
          status: "locked"
      }
      $uibModalInstance.close($ctrl.data);
  };
  $ctrl.remove = function () {
    $ctrl.data = {
        status: "removed"
    }
    $uibModalInstance.close($ctrl.data);
  };

  $ctrl.cancel = function () {
    $uibModalInstance.dismiss('cancel');
  };
});
