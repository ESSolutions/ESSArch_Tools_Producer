angular.module('myApp').controller('LoginCtrl', function ($scope, $location, myService, $state, $stateParams, $rootScope){
    $scope.redirectAdmin = function () {
        $window.location.href="/admin/";
    }
   $scope.login = function(username, password) {
        $rootScope.auth.name = username;
        $rootScope.auth.password = password;
        $state.go('home.myPage');
   }
});

