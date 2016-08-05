angular.module('myApp').controller('InfoCtrl', function ($scope, myService){
    var vm = this;
    // List view
    $scope.changePath= function(path) {
        myService.changePath(path);
    };
});
