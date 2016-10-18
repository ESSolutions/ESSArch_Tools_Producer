angular.module('myApp').controller('TabsCtrl', function TabsCtrl($state, $scope, $location, $window, myService){
    $scope.tabs = [
    { link: 'home.myPage', label: 'My page' },
    { link: 'home.createSip.info', label: 'Create SIP' },
    { link: 'home.submitSip', label: 'Submit SIP' },
    // { link : '#/recieve-SIP', label : 'Recieve SIP' }
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

