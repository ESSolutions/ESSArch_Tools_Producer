angular.module('myApp').controller('DropdownCtrl', function ($scope, $log, $rootScope, $state, $stateParams, djangoAuth, $window, $translate) {
    $scope.items = [
        'Shortcut 1',
        'Shortcut 2',
        'Shortcut 3'
    ];
    var options, optionsAuth;
    $translate(['LOGIN', 'CHANGEPASSWORD', 'LOGOUT']).then(function(translations) {
        $scope.logIn = translations.LOGIN;
        $scope.changePassword = translations.CHANGEPASSWORD;
        $scope.logOut = translations.LOGOUT;
        options = [
        {
            label: $scope.logIn,
            link: 'login'
        }
        ];
        optionsAuth = [
        {
            label: $scope.changePassword,
            link: '/accounts/changepassword/'
        },
        {
            label: $scope.logOut,
            link: 'logout'
        }
        ];
    });
    $scope.$watch(function() {
        return djangoAuth.authenticated;
    }, function() {
        if(!djangoAuth.authenticated){
            $scope.editUserOptions = options;
        } else {
            $scope.editUserOptions = optionsAuth;
        }
    }, true);
    $scope.name = "";
    $scope.gotoLink = function(choice) {
        if(choice.link != 'logout') {
            $window.location.href = choice.link;
        } else {
            $state.go(choice.link);
        }
    };
    $scope.status = {
        isopen: false
    };

    $scope.toggled = function(open) {
        $log.log('Dropdown is now: ', open);
    };

    $scope.toggleDropdown = function($event) {
        $event.preventDefault();
        $event.stopPropagation();
        $scope.status.isopen = !$scope.status.isopen;
    };

    $scope.appendToEl = angular.element(document.querySelector('#dropdown-long-content'));
});
