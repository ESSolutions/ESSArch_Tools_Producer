angular.module('myApp').controller('IpApprovalCtrl', function ($scope, myService, $http, $timeout){
    var vm = this;
    // List view
    $scope.changePath= function(path) {
        myService.changePath(path);
    };

    localStorage.setItem('tableItemSelected', "false");
    $scope.tableItemClick = function() {
        if(localStorage.getItem('tableItemSelected') == "true"){
            localStorage.setItem('tableItemSelected', "false");
        } else {
            localStorage.setItem('tableItemSelected', "true");
        }
    };

    $scope.getListViewData = function() {
        if(localStorage.getItem('tableItemSelected') == "false"){
            $http({
                method: 'GET',
                url: 'http://localhost:8000/steps/'
            })
            .then(function successCallback(response) {
                //alert(JSON.stringify(response.data));
                $scope.rowCollection = response.data;
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
        }, 2000)
    };
    $scope.listViewUpdate();


});
