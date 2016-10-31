angular.module('myApp').controller('TabsCtrl', function TabsCtrl($state, $scope, $location, $window, myService, $translate, $rootScope){
    $rootScope.$on('$translateChangeSuccess', function () {
        $state.reload()
    });
    $scope.myPage = $translate.instant('MYPAGE');
    $scope.createSip = $translate.instant('CREATESIP');
    $scope.submitSip = $translate.instant('SUBMITSIP');
    $scope.recieveSip = $translate.instant('RECEIVESIP');
    $scope.tabs = [
    { link: 'home.myPage', label: $scope.myPage },
    { link: 'home.createSip', label: $scope.createSip },
    { link: 'home.submitSip', label: $scope.submitSip },
    { link: 'home.receiveSip', label : $scope.recieveSip },
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

