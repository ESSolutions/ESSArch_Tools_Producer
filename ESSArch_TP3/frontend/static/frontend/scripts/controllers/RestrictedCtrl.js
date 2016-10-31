angular.module('myApp')
.controller('RestrictedCtrl', function ($scope, $location) {
    $scope.$on('djangoAuth.logged_in', function() {
        $state.go('home');
    });
});
