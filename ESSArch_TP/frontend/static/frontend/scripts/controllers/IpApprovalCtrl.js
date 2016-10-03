angular.module('myApp').controller('IpApprovalCtrl', function ($scope, myService, appConfig, $http, $timeout, $state, $stateParams, $rootScope, listViewService, $interval){
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
     // List view
     $scope.changePath= function(path) {
         myService.changePath(path);
     };
     $scope.ipSelected = false;
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

     //Getting data for status view
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
            vm.profileFields.forEach(function (field) {
                field.templateOptions.disabled = true;
            });
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
        $scope.selectRowCollapse = listViewService.getSelectCollection(sa, $scope.ip);
        console.log($scope.selectRowCollapse);
    };
    //Getting data for list view
    $scope.getListViewData = function() {
        listViewService.getListViewData().then(function(value){
            $scope.ipRowCollection = value;
        });
    };
    $scope.getListViewData();
    $interval(function(){$scope.getListViewData();}, 5000, false);


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
    $scope.createSip = function (ip) {
        $http({
            method: 'POST',
            url: ip.url+"create/"
        })
            .then(function successCallback(response) {
            }), function errorCallback(response){
                alert(response.status);
            };
    };
    $scope.statusShow = false;
    $scope.select = false;
    $scope.subSelect = false;
    $scope.edit = false;
    $scope.eventlog = false;
    $scope.eventShow = false;
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
    $scope.unlockAndRedirect = function() {
        console.log($scope.ip)
        $http({
            method: 'GET',
            url: $scope.ip.url
        }).then(function(response) {
        response.data.locks.forEach(function(lock) {
            if(lock.information_package == $scope.ip.url && lock.submission_agreement == $scope.saProfile.profile.url && lock.profile == $scope.profileToSave.url){
                $http({
                    method: 'DELETE',
                    url: lock.url
                }).then(function() {
                    $scope.goToPrepareIp();
                });
            }
        });
        });
    }
    $scope.goToPrepareIp = function() {
        $state.go('home.createSip.prepareIp');
    }
});

