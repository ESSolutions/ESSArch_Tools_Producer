angular.module('myApp').controller('PrepareSipCtrl', function ($log, $uibModal, $timeout, $scope, $rootScope, $window, $location, $sce, $http, myService, appConfig, $state, $stateParams, listViewService, $interval){
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
        if($scope.statusShow && $scope.ip == row){
            $scope.statusShow = false;
        } else {
            $scope.statusShow = true;
            $scope.edit = false;

            $scope.statusViewUpdate(row);
            //$scope.tree_data = $scope.parentStepsRowCollection;
        }
        $scope.subSelect = false;
        $scope.eventlog = false;
        $scope.eventShow = false;
        $scope.select = false;
        $scope.ip = row;
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
            $scope.edit = false;
            $scope.eventlog = false;
        } else {
            $http({
                method: 'GET',
                url: row.url
            }).then(function (response) {
                $scope.ip = response.data;
                $rootScope.ip = response.data;
                getEventlogData();
                $scope.getPackageInformation(response.data);
                $scope.getPackageDependencies(response.data);
                $scope.getPackageProfiles(response.data);
                $scope.getFileList(response.data);
            });
            $scope.edit = true;
            $scope.eventlog = true;
        }
        $scope.eventShow = false;
        $scope.statusShow = false;
    };

    $scope.eventsClick = function (row) {
        if($scope.eventShow && $scope.ip == row){
            $scope.eventShow = false;
        } else {
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
            console.log(value);
        });
    }
    //Getting data for list view
    $scope.getListViewData = function() {
        listViewService.getListViewData().then(function(value){
            $scope.ipRowCollection = value;
        });
    };
    $scope.getListViewData();
    $interval(function(){$scope.getListViewData();}, 5000, false);

    $scope.max = 100;
    //Getting data for status view
    function getEventlogData() {
        listViewService.getEventlogData().then(function(value){
            $scope.statusNoteCollection = value;
        });
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
                url: sa.profile_transfer_project.active.url
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

        return profiles.active;
    }

    $scope.statusShow = false;
    $scope.eventShow = false;
    $scope.select = false;
    $scope.subSelect = false;
    $scope.edit = false;
    $scope.eventlog = false;


});
