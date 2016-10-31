angular.module('myApp').controller('LoginCtrl', function ($scope, $location, myService, $state, $stateParams, $rootScope, djangoAuth, Validate){
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
                        console.log($rootScope.auth);
                    });
                    $state.go('home');
                },function(data){
                    // error case
                    $scope.errors = data;
                    console.log($scope.errors);
                });
        }
    }
});

