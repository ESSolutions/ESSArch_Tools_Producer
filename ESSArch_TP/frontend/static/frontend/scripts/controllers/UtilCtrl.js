angular.module('myApp').controller('UtilCtrl', function($scope, $state, $location, $window) {
    $scope.reloadPage = function (){
        $state.reload();
    }
    $scope.redirectAdmin = function () {
        $window.location.href="/admin/";
    }
});
