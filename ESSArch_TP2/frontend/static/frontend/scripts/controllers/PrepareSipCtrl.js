angular.module('myApp').controller('PrepareSipCtrl', function ($log, $uibModal, $timeout, $scope, $window, $location, $sce, $http, myService, appConfig, $state, $stateParams){
    var vm = this;
    // List view
    $scope.changePath= function(path) {
        myService.changePath(path);
    };
    $scope.redirectAdmin = function () {
        $window.location.href="/admin/";
    }
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
            $scope.edit = false;
            $scope.eventlog = false;
        } else {
            $http({
                method: 'GET',
                url: row.url
            }).then(function (response) {
                $scope.ip = response.data;
                getEventlogData();
                $scope.getPackageInformation(response.data);
                $scope.getPackageDependencies(response.data);
                $scope.getPackageProfiles(response.data);
                $scope.getFileList(response.data);
            });
            $scope.edit = true;
            $scope.eventlog = true;
            $scope.eventShow = false;
            $scope.statusShow = false;
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

    // Populate file list view
    vm.options = {
        formState: {
        }
    };
    $scope.getFileList = function(ip) {
        var tempElement = {
            filename: ip.ObjectPath,
            created: ip.CreateDate,
            size: ip.ObjectSize
        };
        $scope.fileListCollection = [tempElement];
    };
    $scope.getPackageDependencies = function(ip) {
        $http({
            method: 'GET',
            url: ip.SubmissionAgreement
        }).then(function(response) {
            var sa = response.data;
            $http({
                method: 'GET',
                url: sa.profile_transfer_project[0].url
            }).then(function(response) {
                vm.dependencyModel= response.data.specification_data;
                vm.dependencyFields = response.data.template;
            }, function(response) {
                console.log(response.status);
            });
        }, function(response){
            console.log(response.status);
        });
    }
    vm.profileFields = [{
        templateOptions: {
            label: "transfer_project",
            options: [{name: "OK", value: true},{name: "", value: false}]

        },
        type: "select",
        key: "transfer_project"
    },
    {
        templateOptions: {
            label: "content_type",
            options: [{name: "OK", value: true},{name: "", value: false}]

        },
        type: "select",
        key: "content_type"
    },
    {
        templateOptions: {
            label: "data_selection",
            options: [{name: "OK", value: true},{name: "", value: false}]

        },
        type: "select",
        key: "data_selection"
    },
    {
        templateOptions: {
            label: "classification",

            options: [{name: "OK", value: true},{name: "", value: false}]


        },
        type: "select",
        key: "classification"
    },
    {
        templateOptions: {
            label: "import",

            options: [{name: "OK", value: true},{name: "", value: false}]


        },
        type: "select",
        key: "import"
    },
    {
        templateOptions: {
            label: "submit_description",

            options: [{name: "OK", value: true},{name: "", value: false}]


        },
        type: "select",
        key: "submit_description"
    },
    {
        templateOptions: {
            label: "sip",

            options: [{name: "OK", value: true},{name: "", value: false}]


        },
        type: "select",
        key: "sip"
    },
    {
        templateOptions: {
            label: "aip",

            options: [{name: "OK", value: true},{name: "", value: false}]


        },
        type: "select",
        key: "aip"
    },
    {
        templateOptions: {
            label: "dip",

            options: [{name: "OK", value: true},{name: "", value: false}]


        },
        type: "select",
        key: "dip"
    },
    {
        templateOptions: {
            label: "workflow",

            options: [{name: "OK", value: true},{name: "", value: false}]


        },
        type: "select",
        key: "workflow"
    },
    {
        templateOptions: {
            label: "preservation_metadata",

            options: [{name: "OK", value: true},{name: "", value: false}]


        },
        type: "select",
        key: "preservation_metadata"
    },
    {
        templateOptions: {
            label: "event",
            options: [{name: "OK", value: true},{name: "", value: false}]

        },
        type: "select",
        key: "event"
    }
    ];
    vm.profileModel = {
    };

    $scope.getPackageProfiles = function(ip) {
        $http({
            method: 'GET',
            url: ip.SubmissionAgreement
        }).then(function(response) {
            vm.profileModel = {
            };

            var sa = response.data;
            getProfiles(sa.profile_transfer_project).then(function(profileValue){vm.profileModel.transfer_project = profileValue});
            getProfiles(sa.profile_content_type).then(function(profileValue){vm.profileModel.content_type = profileValue});
            getProfiles(sa.profile_data_selection).then(function(profileValue){vm.profileModel.data_selection = profileValue});
            getProfiles(sa.profile_classification).then(function(profileValue){vm.profileModel.classification = profileValue});
            getProfiles(sa.profile_import).then(function(profileValue){vm.profileModel.import = profileValue});
            getProfiles(sa.profile_submit_description).then(function(profileValue){vm.profileModel.submit_description = profileValue});
            getProfiles(sa.profile_sip).then(function(profileValue){vm.profileModel.sip = profileValue});
            getProfiles(sa.profile_aip).then(function(profileValue){vm.profileModel.aip = profileValue});
            getProfiles(sa.profile_dip).then(function(profileValue){vm.profileModel.dip = profileValue});
            getProfiles(sa.profile_workflow).then(function(profileValue){vm.profileModel.workflow = profileValue});
            getProfiles(sa.profile_preservation_metadata).then(function(profileValue){vm.profileModel.preservation_metadata = profileValue});
            getProfiles(sa.profile_event).then(function(profileValue){vm.profileModel.event = profileValue});
            console.log("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx");
            console.log(vm.profileModel);
            console.log("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx");
        }, function(response){
            console.log(response.status);
        });
    }
    function getProfiles(profiles){
        var promise = $http({
            method: 'GET',
            url: getActiveProfile(profiles).url
        }).then(function(response) {
            var returnVal = false;
            $scope.ip.locks.forEach(function(lock) {
                if(lock.profile == response.data.url){
                    returnVal = true;
                    console.log("true");
                }
            });
            return returnVal;
        }, function(response) {
            console.log(response.status);
        });
        return promise;
    }

    $scope.getPackageInformation = function(ip) {
        $http({
            method: 'GET',
            url: ip.SubmissionAgreement
        }).then(function(response) {
            var sa = response.data;
            $http({
                method: 'GET',
                url: getActiveProfile(sa.profile_submit_description).url
            }).then(function(response) {
                vm.informationModel= response.data.specification_data;
                vm.informationFields = response.data.template;
            }, function(response) {
              console.log(response.status);
            });
        }, function(response){
            console.log(response.status);
        });
    };
    function getActiveProfile(profiles) {
        /*if(profiles.length < 2) {
            return profiles[0];
        }*/
        var activeProfile = profiles[0];
        var bestStatus = 0;
        profiles.forEach(function(profile) {
            if(profile.status == 1){
                activeProfile = profile;
                bestStatus = 1;
            }
            else if(profile.status == 2 && bestStatus != 1){
                activeProfile = profile;
                bestStatus = 2;
            }
        });
        return activeProfile;
    }

    $scope.statusShow = false;
    $scope.eventShow = false;
    $scope.select = false;
    $scope.subSelect = false;
    $scope.edit = false;
    $scope.eventlog = false;


});
