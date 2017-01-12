angular.module('myApp').controller('UtilCtrl', function($scope, $state, $location, $window, $rootScope, $timeout, $http, appConfig) {
    $scope.reloadPage = function (){
        $state.reload();
    }
    $scope.redirectAdmin = function () {
        $window.location.href="/admin/";
    }
    $scope.infoPage = function() {
        $state.go('home.info');
    }
});
