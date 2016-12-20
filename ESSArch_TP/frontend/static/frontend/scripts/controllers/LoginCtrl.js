angular.module('myApp').controller('LoginCtrl', function ($scope, $location, myService, $state, $stateParams, $rootScope, djangoAuth, Validate, $http, PermRoleStore, PermPermissionStore){
    $scope.redirectAdmin = function () {
        $window.location.href="/admin/";
    }
    $scope.model = {'username':'','password':''};
    $scope.complete = false;
    $scope.login = function(formData){
        $scope.errors = [];
        Validate.form_validation(formData,$scope.errors);
        if(!formData.$invalid){
            djangoAuth.login($scope.model.username, $scope.model.password)
                .then(function(data){
                    // success case
                    djangoAuth.profile().then(function(data){
                        $rootScope.auth = data;
                        PermPermissionStore.clearStore();
                        PermRoleStore.clearStore();
                        myService.getPermissions(data.permissions);
                    });
                    $state.go('home.info');
                },function(data){
                    // error case
                    $scope.errors = data;
                    console.log($scope.errors);
                });
        }
    }
});

