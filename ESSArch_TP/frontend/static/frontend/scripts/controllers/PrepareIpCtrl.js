angular.module('myApp').controller('PrepareIpCtrl', function ($log, $uibModal, $timeout, $scope, $window, $location, $sce, $http, myService, appConfig){
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
            cellTemplate: "<uib-progressbar class=\"progress-striped active\" animate=\"true\" value=\"row.branch[col.field]\" type=\"success\"><b>{{row.branch[col.field]+\"%\"}}</b></uib-progressbar>"
        }
    ];

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
            $scope.tree_data = [];
            $scope.getStatusViewData(row).then(function(steps) {
                $scope.tree_data = steps;
                console.log(steps);
            });

            //$scope.tree_data = $scope.parentStepsRowCollection;
        }
        $scope.subSelect = false;
        $scope.eventlog = false;
        $scope.select = false;
        $scope.ip= row;
    };

    $scope.ipTableClick = function(row) {
        console.log("ipobject clicked. row: "+row.Label);
        if($scope.select && $scope.ip== row){
            $scope.select = false;
        } else {
            $scope.select = true;
            $scope.eventShow = false;
            $scope.statusShow = false;
            $scope.getSaProfiles(row);
        }
        $scope.statusShow = false;
        $scope.ip= row;
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
        var promises = [];

        row.steps.forEach(function(step){
            promises.push(
                $http({
                    method: 'GET',
                    url: step
                })
                .then(function (response) {
                    return getChildSteps(response.data.child_steps).then(function(children) {
                        return $scope.getTasks(response.data).then(function(tasks){
                            tasks.forEach(function(task){
                                task.label = task.name;
                            });

                            response.data.children = children.concat(tasks);
                            response.data.isCollapsed = false;
                            response.data.tasksCollapsed = true;
                            return response.data;
                        });
                    });
                })
            );
        });

        return Promise.all(promises);
    };

    //Helper functions for getStatusViewData
    function getChildSteps(childSteps) {
        if (childSteps.length == 0) {
            return Promise.resolve([]);
        }
        promises = [];

        childSteps.forEach(function(child){
            promises.push(
                $http({
                    method: 'GET',
                    url: child
                })
                .then(function(response) {
                    return getChildSteps(response.data.child_steps).then(function(child_steps){
                        return $scope.getTasks(response.data).then(function(tasks){
                            tasks.forEach(function(task){
                                task.user = response.data.user;
                                task.time_created = task.time_started;
                            });

                            response.data.children = child_steps.concat(tasks);
                            response.data.isCollapsed = false;
                            response.data.tasksCollapsed = true;
                            return response.data;
                        });
                    });
                })
            );
        });

        return Promise.all(promises);
    };

    $scope.getTasks = function(step) {
        if (step.tasks.length == 0) {
            return Promise.resolve([]);
        }

        var promises = [];

        step.tasks.forEach(function(task){
            promises.push(
                $http({
                    method: 'GET',
                    url: task
                })
                .then(function(response) {
                    return response.data;
                })
            );
        });

        return Promise.all(promises);
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
    vm.profileModel = {};
    vm.profileFields=[];
    $scope.profileClick = function(row){
        $scope.profileToSave = row.profile;
        console.log(row);
        if ($scope.selectProfile == row && $scope.subSelect){
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
            for(i=0; i<sas.length; i++){
                tempProfiles.push(sas[i]);
                if(sas[i].information_packages.url == ip.url){
                    saProfile.profile = sa[i];
                }
            }
            $scope.saProfile.profiles = tempProfiles;
            console.log("current sa: ");
            console.log($scope.currentSa);
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
            url: appConfig.djangoUrl+"profiles-by-type",
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
            console.log("newProfileType = " + newProfileType);
            if(newProfileType){
                var tempProfileObject = {
                    profile_label: response.data.profile_type.toUpperCase(),
                    profile_type: response.data.profile_type,
                    profile: {},
                    profiles: [
                       response.data
                    ],
                };
                if(defaultProfile){
                    response.data.defaultProfile = true;
                    tempProfileObject.profile = response.data;
                }
                $scope.selectRowCollapse.push(tempProfileObject);
            }
        }), function errorCallback(response){
            alert(response.status);
        };
    };
    $scope.changeProfile = function(profile){
        var sendData = {"new_profile": profile.id};
        var uri = $scope.currentSa.url+"change-profile/";
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
        if($scope.approvedToCreate){
        var uri = $scope.ip.url+"prepare/";
        var sendData = {
            "status_note": $scope.statusNote.id,
            "signature": $scope.signature
        };

        $http({
            method: 'POST',
            url: uri,
            data: sendData
        })
        .success(function (response) {
            alert(response.status);
        })
        .error(function (response) {
            alert(response.status);
        });
        } else {
            var uri = $scope.profileToSave.url+"save/";
            var sendData = {"specification_data": vm.profileModel, "status_note": $scope.statusNote.id, "signature": $scope.signature, "submission_agreement": $scope.currentSa.id, "new_name": new_name};
            console.log(sendData);
            $http({
                method: 'POST',
                url: uri,
                data: sendData
            })
            .success(function (response) {
                alert(response.status);
                //????????????
                $scope.getSelectCollection($scope.currentSa);
                $scope.showHideAllProfiles();
                $scope.showHideAllProfiles();
                //????????????
            })
            .error(function(response) {
                alert(response.status);
            });
        }
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
    $scope.openModalOrRun = function(){
        if($scope.approvedToCreate){
            vm.onSubmit("");
         } else {
            $scope.openModal();
         }
    }
    $scope.openModal = function() {
        var modalInstance = $uibModal.open({
            animation: true,
            ariaLabelledBy: 'modal-title',
            ariaDescribedBy: 'modal-body',
            templateUrl: 'enter-profile-name.html',
            controller: 'ModalInstanceCtrl',
            controllerAs: '$ctrl'
        })
        modalInstance.result.then(function (data) {
            vm.onSubmit(data.name);
        }, function () {
            $log.info('modal-component dismissed at: ' + new Date());
        });
    };


});
angular.module('myApp').controller('ModalInstanceCtrl', function ($uibModalInstance) {
  var $ctrl = this;

  $ctrl.ok = function () {
      $ctrl.data = {
        name: $ctrl.profileName
      };
        $uibModalInstance.close($ctrl.data);
  };

  $ctrl.cancel = function () {
    $uibModalInstance.dismiss('cancel');
  };
});
