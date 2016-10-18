angular.module('myApp').controller('TabsCtrl', function TabsCtrl($state, $scope, $location, $window, myService, $translate, $rootScope){
    $translate(['MYPAGE', 'CREATESIP', 'SUBMITSIP', 'RECIEVESIP']).then(function(translations) {
        $scope.tabs = [
        { link: 'home.myPage', label: translations.MYPAGE },
        { link: 'home.createSip.info', label: translations.CREATESIP },
        { link: 'home.submitSip', label: translations.SUBMITSIP },
        // { link : 'home.recieveSip', label : translations.RECIEVESIP }
        ];
    });
    $rootScope.$on('$translateChangeSuccess', function () {
        $translate(['MYPAGE', 'CREATESIP', 'SUBMITSIP', 'RECIEVESIP']).then(function(translations) {
            $scope.tabs = [
            { link: 'home.myPage', label: translations.MYPAGE },
            { link: 'home.createSip.info', label: translations.CREATESIP },
            { link: 'home.submitSip', label: translations.SUBMITSIP },
            // { link : 'home.recieveSip', label : translations.RECIEVESIP }
            ];
        });
    });

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
                $scope.tabs.active = index;
            }
        });
    };

    $scope.update_tabs();
    // Get active tab from localStorage
    $scope.getActiveTab = function () {
        return sessionStorage.getItem("activeTab");
    };
    $scope.go = function(tab) {
        $state.go(tab.link);
    }
});

