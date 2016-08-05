angular.module('myApp').controller('IpApprovalCtrl', function ($scope, myService){
    var vm = this;
    // List view
    $scope.changePath= function(path) {
        myService.changePath(path);
    };
});
