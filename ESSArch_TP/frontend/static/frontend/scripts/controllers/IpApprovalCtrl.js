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


});
