angular.module('myApp').controller('IpApprovalCtrl', function ($scope, myService, appConfig, $http, $timeout, $state, $stateParams){
    var vm = this;
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
            $scope.getStatusViewData(row);
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
            $scope.eventlog = false;
            $scope.ipSelected = false;
        } else {
            $scope.select = true;
            $scope.ipSelected = true;
            $scope.getSaProfiles(row);
        }
        $scope.statusShow = false;
        $scope.ip= row;
    };
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
                if(sas[i].information_packages.indexOf(ip.url, 0)!= -1){
                    $scope.saProfile.profile = sas[i];
                }
            }
            $scope.saProfile.profiles = tempProfiles;
            $scope.currentSa = $scope.saProfile.profile;
            $scope.getSelectCollection($scope.currentSa);
            $scope.showHideAllProfiles();
            getEventlogData();
            $scope.eventlog = true;
            console.log("current sa: ");
            console.log($scope.currentSa);
        }), function errorCallback(response){
            alert(response.status);
        };
    };
    $scope.getSelectCollection = function (sa) {
        $scope.currentProfiles = {};
        $scope.selectRowCollapse = [];
        getProfiles(sa.profile_transfer_project);
        getProfiles(sa.profile_content_type);
        getProfiles(sa.profile_data_selection);
        getProfiles(sa.profile_classification);
        getProfiles(sa.profile_import);
        getProfiles(sa.profile_submit_description);
        getProfiles(sa.profile_sip);
        getProfiles(sa.profile_aip);
        getProfiles(sa.profile_dip);
        getProfiles(sa.profile_workflow);
        getProfiles(sa.profile_preservation_metadata);
        getProfiles(sa.profile_event);
        console.log($scope.selectRowCollapse);

    };
    function getProfiles(profileArray){
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
     };
    function getProfile(profile_id, defaultProfile) {
        $http({
            method: 'GET',
            url: appConfig.djangoUrl + "profiles/" + profile_id+ "/"
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

    //Getting data for list view
    $scope.getListViewData = function() {
        if(!$scope.ipSelected){
            $http({
                method: 'GET',
                url: appConfig.djangoUrl+'information-packages/'
            })
            .then(function successCallback(response) {
                // console.log(JSON.stringify(response.data));
                var data = response.data;
                $scope.ipRowCollection = data;
            }), function errorCallback(){
                alert('error');
            };
        }
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

    //Dummy values for Sub select view

    $scope.subSelect = true;
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
    $scope.createIp = function (ip) {
            $http({
                method: 'POST',
                url: ip.url+"create/"
            })
            .then(function successCallback(response) {
                // console.log(JSON.stringify(response.data));
                alert(response.status);
            }), function errorCallback(response){
                alert(response.status);
            };
    };

    $scope.exampleData = "1";
    $scope.exampleSelectData = [
        "1",
        "2",
        "3"
    ];
    $scope.statusShow = false;
    $scope.select = false;
    $scope.subSelect = false;
    $scope.edit = false;
    $scope.eventlog = false;
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
});

