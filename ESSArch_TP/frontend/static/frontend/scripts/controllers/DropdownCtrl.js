angular.module('myApp').controller('DropdownCtrl', function ($scope, $log, $rootScope, $state, $stateParams, djangoAuth) {
    $scope.items = [
        'Shortcut 1',
        'Shortcut 2',
        'Shortcut 3'
    ];

    var options = [
    {
        label: 'Edit profile',
        link: ''
    },
    {
        label: 'Settings',
        link: ''
    },
    {
        label: 'Log in',
        link: 'login'
    }
    ];
    var optionsAuth = [
    {
        label: 'Edit profile',
        link: ''
    },
    {
        label: 'Settings',
        link: ''
    },
    {
        label: 'Log out',
        link: 'logout'
    }
    ];

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
        $state.go(choice.link)
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
