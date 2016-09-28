angular.module('myApp').controller('TabsCtrl', function TabsCtrl($scope, $location, $window){
    $scope.tabs = [
    { link: 'home.myPage', label: 'My page' },
    { link: 'home.createSip.info', label: 'Create SIP' },
    { link: 'home.submitSip', label: 'Submit SIP' },
    // { link : '#/recieve-SIP', label : 'Recieve SIP' }
    ];

    $scope.setActiveTab = function (activeTab) {
        sessionStorage.setItem("activeTab", activeTab);
    };

    // Get active tab from localStorage
    $scope.getActiveTab = function () {
        return sessionStorage.getItem("activeTab");
    };

    // Check if current tab is active
    $scope.isActiveTab = function (tabName, index) {
        var activeTab = $scope.getActiveTab();
        return (activeTab === tabName || (activeTab === null && index === 0));
    };
});

