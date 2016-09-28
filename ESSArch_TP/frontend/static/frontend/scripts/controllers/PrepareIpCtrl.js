angular.module('myApp').controller('PrepareIpCtrl', function ($log, $uibModal, $timeout, $scope, $window, $location, $sce, $http, myService, appConfig, $state, $stateParams){
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
            cellTemplate: "<uib-progressbar ng-click=\"taskStepUndo(row.branch)\" class=\"progress-striped active\" animate=\"true\" value=\"row.branch[col.field]\" type=\"success\"><b>{{row.branch[col.field]+\"%\"}}</b></uib-progressbar>"
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
            //$scope.tree_data = $scope.parentStepsRowCollection;
        }
        $scope.subSelect = false;
        $scope.eventlog = false;
        $scope.select = false;
        $scope.ip= row;
    };
    $scope.getTreeData = function(row) {
     $http({
                method: 'GET',
                url: row.url,
            }).then(function(response){
                ip = response.data
                $scope.tree_data = $scope.getStatusViewData(ip).steps;
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
        } else {
            $http({
                method: 'GET',
                url: row.url
            }).then(function (response) {
                $scope.ip = response.data;
            });
            $scope.select = true;
            $scope.eventShow = false;
            $scope.statusShow = false;
            $scope.getSaProfiles(row);
        }
        $scope.statusShow = false;
    };

    $scope.eventsClick = function (row) {
        if($scope.eventShow && $scope.ip== row){
            $scope.eventShow = false;
        } else {
            $scope.eventShow = true;
            $scope.eventCollection = [];
            $http({
                method: 'GET',
                url: appConfig.djangoUrl+'events/'
            })
            .then(function successCallback(response) {
                // console.log(JSON.stringify(response.data));
                var data = response.data;
                for(i=0; i<data.length; i++){
                    if(data[i].linkingObjectIdentifierValue == row.url)
                    $scope.eventCollection.push(data[i]);
                }
            }), function errorCallback(response){
                alert(response.status);
            };
            $scope.eventShow = true;
        }
        $scope.select = false;



        $scope.ip= row;
    };
    //Getting data for list view
    $scope.getListViewData = function() {
            $http({
                method: 'GET',
                url: appConfig.djangoUrl+'information-packages/'
            })
            .then(function successCallback(response) {
                //console.log(JSON.stringify(response.data));
                var data = response.data;
                $scope.ipRowCollection = data;
            }), function errorCallback(response){
                alert(response.status);
            };
    };
    $scope.getListViewData();
    //updates every 5 seconds
    $scope.listViewUpdate = function(){
        $timeout(function() {
            $scope.getListViewData();
            $scope.listViewUpdate();
        }, 5000)
    };
    $scope.listViewUpdate();
    //Getting data for status view
    $scope.getStatusViewData = function(row) {

        row.steps.forEach(function(step){
            step.children = getChildSteps(step.child_steps);
            step.tasks.forEach(function(task){
                task.label = task.name;
            });
            step.children = step.children.concat(step.tasks);
            step.isCollapsed = false;
            step.tasksCollapsed = true;
        });

        return row;

    };

    //Helper functions for getStatusViewData
    function getChildSteps(childSteps) {
        childSteps.forEach(function(child){
            child.child_steps = getChildSteps(child.child_steps);
            child.tasks.forEach(function(task){
                task.user = child.user;
                task.time_created = task.time_started;
            });

            child.children = child.child_steps.concat(child.tasks);
            if(child.children.length == 0){
                child.icons = {
                    iconLeaf: "glyphicon glyphicon-alert"
                };
            }
            child.isCollapsed = false;
            child.tasksCollapsed = true;
        });
        return childSteps;
    };

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
        }
    }

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
            $http({
                method: 'OPTIONS',
                url: appConfig.djangoUrl+'tasks/'
            })
            .then(function successCallback(response) {
                // console.log(JSON.stringify(response.data));
                var data = response.data;
                $scope.subSelectOptions = data.actions.POST.name.choices;
            }), function errorCallback(response){
                alert(response.status);
            };
        }
        console.log("selected profile: ");
        console.log($scope.selectProfile);
    };
    function getEventlogData() {
        $http({
            method: 'GET',
            url: appConfig.djangoUrl+'event-types/'
        })
        .then(function successCallback(response) {
            $scope.statusNoteCollection = response.data;
        }), function errorCallback(response){
            alert(response.status);
        };
    };
    //populating select view
    $scope.selectRowCollection = [];
    $scope.selectRowCollapse = [];
    $scope.saProfile =
    {
        entity: "PROFILE_SUBMISSION_AGREEMENT",
        profile: {},
        profiles: [

        ],
    };

    $scope.getSaProfiles = function(ip) {
        var sas = [];
        $http({
            method: 'GET',
            url: appConfig.djangoUrl+'submission-agreements/'
        })
        .then(function successCallback(response) {
            // console.log(JSON.stringify(response.data));
            sas = response.data;
            var tempProfiles = [];
            $scope.submissionAgreements = sas;
            $scope.saProfile.profileObjects = sas;
            sas.forEach(function (sa) {
                tempProfiles.push(sa);
                sa.information_packages.forEach(function (informationPackage) {
                    if(informationPackage == ip.url){
                        $scope.saProfile.profile = sa;
                        $scope.saProfile.profile.includedProfiles = [];
                    }
                });
            });
            $scope.saProfile.profiles = tempProfiles;
            $scope.getSelectCollection($scope.saProfile.profile);
            console.log("current sa: ");
            console.log($scope.saProfile.profile);
        }), function errorCallback(response){
            alert(response.status);
        };
    };
    $scope.getSelectCollection = function (sa) {



        $scope.currentProfiles = {};
        $scope.selectRowCollapse = [];
        getProfiles("transfer_project", sa.profile_transfer_project);
        getProfiles("content_type", sa.profile_content_type);
        getProfiles("data_selection", sa.profile_data_selection);
        getProfiles("classification", sa.profile_classification);
        getProfiles("import", sa.profile_import);
        getProfiles("submit_description", sa.profile_submit_description);
        getProfiles("sip", sa.profile_sip);
        getProfiles("aip", sa.profile_aip);
        getProfiles("dip", sa.profile_dip);
        getProfiles("workflow", sa.profile_workflow);
        getProfiles("preservation_metadata", sa.profile_preservation_metadata);
        getProfiles("event", sa.profile_event);
        console.log($scope.selectRowCollapse);

    };
    function getProfiles(type, profileArray){
        var bestStatus = 0;
        for(i=0;i<profileArray.length;i++){
            if(profileArray[i].status == 0 ){
                getProfile(profileArray[i].id, false);
            }
            if(profileArray[i].status == 2 && bestStatus != 1){
                bestStatus = 2;
                getProfile(profileArray[i].id, true);
            }
            if(profileArray[i].status == 2 && bestStatus == 1){
                getProfile(profileArray[i].id, false);
            }
            if(profileArray[i].status == 1){
                bestStatus = 1;
                getProfile(profileArray[i].id, true);
            }
        }
        $http({
            method: 'GET',
            url: appConfig.djangoUrl+"profiles",
            params: {type: type}
        })
        .then(function successCallback(response) {
            var tempProfileArray = response.data;
            for(i=0;i<profileArray.length;i++){
                for(j=0;j<tempProfileArray.length;j++){
                    if(tempProfileArray[j].id == profileArray[i].id){
                        tempProfileArray.splice(j,1);
                    }
                }
            }
            for(i=0;i<tempProfileArray.length;i++){
                getProfile(response.data[i].id, false);
            }
        }), function errorCallback(response){
            alert(response.status);
        };
    };
    function getProfile(profile_id, defaultProfile) {
        $http({
            method: 'GET',
            url: appConfig.djangoUrl + "profiles/" + profile_id
        })
        .then(function successCallback(response) {
            var newProfileType = true;
            for(i=0; i<$scope.selectRowCollapse.length;i++){
                if($scope.selectRowCollapse[i].profile_type == response.data.profile_type){
                    newProfileType = false;
                    $scope.selectRowCollapse[i].profiles.push(response.data);
                    if(defaultProfile){
                        response.data.defaultProfile = true;
                        $scope.selectRowCollapse[i].profile = response.data;
                    }
                    break;
                } else {
                    newProfileType = true;
                }
            }
            // console.log("newProfileType = " + newProfileType);
            if(newProfileType){
                var tempProfileObject = {
                    profile_label: response.data.profile_type.toUpperCase(),
                    profile_type: response.data.profile_type,
                    profile: {},
                    profiles: [
                       response.data
                    ],
                    checked: true,
                };
                if(defaultProfile){
                    response.data.defaultProfile = true;
                    tempProfileObject.profile = response.data;
                }
                if (tempProfileObject.profile_label.toUpperCase() == "SUBMIT_DESCRIPTION"){
                }
                $http({
                    method: 'GET',
                    url: $scope.ip.url
                }).then(function(response){
                    tempProfileObject = $scope.profileLocked(tempProfileObject, $scope.saProfile.profile.url, response.data.locks);
                });
                $scope.selectRowCollapse.push(tempProfileObject);
                $scope.updateIncludedProfiles(tempProfileObject);
                // console.log("finished profile object");
                // console.log(tempProfileObject);
            }
        }), function errorCallback(response){
            alert(response.status);
        };
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
    $scope.profileLocked = function(profileObject, sa, locks) {
        profileObject.locked = "";
              locks.forEach(function (lock) {
                     if(lock.submission_agreement == sa) {
            }
            if(lock.profile == profileObject.profile.url) {
            }
            if(lock.submission_agreement == sa && lock.profile == profileObject.profile.url){
                profileObject.locked = "Locked";
            }
        });
        return profileObject;
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

// Page selection
//      &
// ng-show code
    $scope.ipSubmitText = "Save profile";
    $scope.toggleIpText = function() {
        if($scope.approvedToCreate){
            $scope.ipSubmitText = "Prepare ip";
        }else {
            $scope.ipSubmitText = "Save profile";
        }
    }
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
        console.log($scope.profileToSave);
        $http({
            method: 'POST',
            url: profileObject.profile.url+"lock/",
            data: {
                information_package: $scope.ip.id,
                submission_agreement: $scope.saProfile.profile.id
            }
        }).then(function (response) {
            console.log("locked");
            $scope.profileToSave.locked = "Locked";
            profileObject.locked = "Locked";
            $scope.edit = false;
            $scope.eventlog = false;
            });
    }
    $scope.prepareIp = function (label) {
        $http({
            method: 'POST',
            url: appConfig.djangoUrl+"information-packages/",
            data: {label: label}
        }).then(function (response){
            console.log("new ip created, with label: " + label);
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
