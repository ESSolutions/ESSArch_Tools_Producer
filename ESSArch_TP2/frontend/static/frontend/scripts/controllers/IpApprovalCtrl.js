angular.module('myApp').controller('IpApprovalCtrl', function ($scope, myService, appConfig, $http, $timeout){
    var vm = this;
    // List view
    $scope.changePath= function(path) {
        myService.changePath(path);
    };
$scope.archiveSelected = false;
    $scope.stateClicked = function(row){
        console.log(row);
        if($scope.statusShow && $scope.archive == row){
            $scope.statusShow = false;
            $scope.archiveSelected = false;
        } else {
            $scope.statusShow = true;
            $scope.edit = false;
            $scope.archiveSelected = true;
        }
        $scope.select = false;
        $scope.archive = row;
    };

    $scope.archiveTableClick = function(row) {
        console.log("archive object clicked. row: "+row.label);
        if($scope.select && $scope.archive == row){
            $scope.select = false;
            $scope.archiveSelected = false;
        } else {
            $scope.select = true;
            $scope.archiveSelected = true;
        }
        $scope.statusShow = false;
        $scope.archive = row;
    };
    //Getting data for list view
    $scope.getListViewData = function() {
        if(!$scope.archiveSelected){
            $http({
                method: 'GET',
                url: appConfig.djangoUrl+'archive-objects/'
            })
            .then(function successCallback(response) {
                // console.log(JSON.stringify(response.data));
                var data = response.data;
                $scope.archiveObjectsRowCollection = data;
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
    $scope.selectProfile = {
        entity: "dummyValue"
    };
    $scope.subSelect = true;
    $scope.subSelectProfile = "";
    $scope.subSelectOptions = [
        "test1",
        "test2",
        "test3"
    ];
    $scope.selectRowCollection = [
    {
        entity: "PROFILE_SUBMISSION_AGREEMENT",
        profile: "standard profil",
        profiles: [
            "default SA"
        ],
        state: "unspecified"
    },
    {
        entity: "PROFILE_TRANSFER_PROJECT",
        profile: "standard profile",
        profiles: [
            "default PTP"
        ],
        state: "unspecified"
    },
    {
        entity: "PROFILE_CONTENT_TYPE",
        profile: "standard profile",
        profiles: [
            "default PCT"
        ],
        state: "unspecified"
    },
    {
        entity: "PROFILE_DATA_SELECTION",
        profile: "standard profile",
        profiles: [
            "default PDS"
        ],
        state: "unspecified"
    },
    {
        entity: "PROFILE_CLASSIFICATION",
        profile: "standard profile",
        profiles: [
            "default PC"
        ],
        state: "unspecified"
    },
    {
        entity: "PROFILE_IMPORT",
        profile: "standard profile",
        profiles: [
            "default PCT"
        ],
        state: "unspecified"
    },
    {
        entity: "PROFILE_SUBMIT_DESCRIPTION",
        profile: "standard profile",
        profiles: [
            "default PSD"
        ],
        state: "unspecified"
    },
    {
        entity: "PROFILE_SUBMISSION INFORMATION PACKAGE",
        profile: "standard profile",
        profiles: [
            "default PSIP"
        ],
        state: "unspecified"
    },
    {
        entity: "PROFILE_ARCHIVAL INFORMATION PACKAGE",
        profile: "standard profile",
        profiles: [
            "default PAIP"
        ],
        state: "unspecified"
    },
    {
        entity: "PROFILE_DISSEMINATION INFORMATION PACKAGE",
        profile: "standard profile",
        profiles: [
            "default PDIP"
        ],
        state: "unspecified"
    },
    {
        entity: "PROFILE_WORKFLOW",
        profile: "standard profile",
        profiles: [
            "default PWF"
        ],
        state: "unspecified"
    }
    ];
    $scope.profileClick = function(row){
        $scope.toggleSubSelectView();
        $scope.toggleEditView();
        $scope.selectProfile = row;
        $scope.subSelectProfile = "profile";
        $scope.subSelectOptions = [
            "option1",
            "option2",
            "option3"
        ];
        console.log($scope.selectProfile);
    };
});
