angular.module('myApp')
.controller('LogoutCtrl', function ($scope, $location, djangoAuth, $rootScope) {
    $rootScope.auth = null;
    djangoAuth.logout();
});
