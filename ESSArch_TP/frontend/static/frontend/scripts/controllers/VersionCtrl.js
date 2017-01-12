angular.module('myApp').controller('VersionCtrl', function($scope, myService) {
    myService.getVersionInfo().then(function(result) {
        $scope.sysInfo = result;
    });
});
