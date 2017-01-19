/*
    ESSArch is an open source archiving and digital preservation system

    ESSArch Tools for Producer (ETP)
    Copyright (C) 2005-2017 ES Solutions AB

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.

    Contact information:
    Web - http://www.essolutions.se
    Email - essarch@essolutions.se
*/

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
