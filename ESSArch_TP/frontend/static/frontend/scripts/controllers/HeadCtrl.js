angular.module('myApp').controller('HeadCtrl', function($scope, $rootScope, $timeout, $translate, $state) {
    var vm = this;
    var appName = " | ESSArch Tools for Producer";
    vm.pageTitle = "ESSArch Tools for Producer";
    $rootScope.$on('$stateChangeSuccess', function (event, toState, toParams, fromState, fromParams) {
        vm.pageTitle = $translate.instant(toState.name.split(".").pop().toUpperCase())+appName;
    });
    $rootScope.$on('$translateChangeSuccess', function () {
        vm.pageTitle = $translate.instant($state.current.name.split(".").pop().toUpperCase())+appName;
    });
});
