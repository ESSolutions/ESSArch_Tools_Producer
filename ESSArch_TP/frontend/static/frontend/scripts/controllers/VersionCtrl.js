angular.module('myApp').controller('VersionCtrl', function($scope, myService, $window) {
    myService.getVersionInfo().then(function(result) {
        $scope.sysInfo = result;
    });
    $scope.redirectToEss = function(){
        $window.open('http://www.essolutions.se', '_blank');
    };
});
