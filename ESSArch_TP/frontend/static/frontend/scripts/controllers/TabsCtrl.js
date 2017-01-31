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

angular.module('myApp').controller('TabsCtrl', function TabsCtrl($state, $scope, $location, $window, myService, $translate, $rootScope){
    $rootScope.$on('$translateChangeSuccess', function () {
        $state.reload()
    });
    $rootScope.$on('$stateChangeStart', function(event, toState, toParams, fromState) {
        if(toState.name == "home.info" || toState.name == "home.versionInfo") {
            $scope.activeTab = null;
        }
    });
    $scope.activeTab = null;
    $scope.myPage = $translate.instant('MYPAGE');
    $scope.prepareIp = $translate.instant('PREPAREIP');
    $scope.createSip = $translate.instant('CREATESIP');
    $scope.submitSip = $translate.instant('SUBMITSIP');
    $scope.collectContent = $translate.instant('COLLECTCONTENT');
    $scope.tabs = [
    //{ link: 'home.myPage', label: $scope.myPage },
    { link: 'home.createSip.prepareIp', label: $scope.prepareIp },
    { link: 'home.createSip.collectContent', label: $scope.collectContent },
    { link: 'home.createSip.ipApproval', label: $scope.createSip },
    { link: 'home.submitSip.prepareSip', label: $scope.submitSip },
    ];
    $scope.is_active = function(tab) {
        var isAncestorOfCurrentRoute = $state.includes(tab.link);
        return isAncestorOfCurrentRoute;
    };
    $scope.update_tabs = function() {

        // sets which tab is active (used for highlighting)
        angular.forEach($scope.tabs, function(tab, index) {
            tab.params = tab.params || {};
            tab.options = tab.options || {};
            tab.class = tab.class || '';

            tab.active = $scope.is_active(tab);
            if (tab.active) {
                $scope.activeTab = index;
            }
        });
    };

    $scope.update_tabs();
    // Get active tab from localStorage
    $scope.go = function(tab) {
        $state.go(tab.link);
    }
});

