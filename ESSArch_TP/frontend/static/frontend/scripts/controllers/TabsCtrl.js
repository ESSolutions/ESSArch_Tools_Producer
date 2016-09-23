angular.module('myApp').controller('TabsCtrl', function TabsCtrl($scope, $location, $window){
    $scope.tabs = [
    { link: 'home.myPage', label: 'My page' },
    { link: 'home.createSip.info', label: 'Create SIP' },
    { link: 'home.submitSip', label: 'Submit SIP' },
    // { link : '#/recieve-SIP', label : 'Recieve SIP' }
    ];
    $scope.setActiveTab = function(index){
        $window.localStorage.setItem("activeTab", index);
    };

    $scope.getActiveTab = function(){
        return $window.localStorage.getItem("activeTab");
    };

    $scope.isActiveTab = function(tabName,index){
        var activeTab = $scope.getActiveTab();
        return (index === activeTab)
    };
});

