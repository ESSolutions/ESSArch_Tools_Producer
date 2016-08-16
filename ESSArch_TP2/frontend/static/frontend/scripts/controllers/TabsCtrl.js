angular.module('myApp').controller('TabsCtrl', function TabsCtrl($scope, $location){
  $scope.tabs = [
      { link : '#/', label : 'My page' },
      { link : '#/create-SIP/info', label : 'Create SIP' },
      { link : '#/submit-SIP/prepare-SIP', label : 'Submit SIP' },
     // { link : '#/recieve-SIP', label : 'Recieve SIP' }
    ];

  $scope.selectedTab = $scope.tabs[0];
  $scope.setSelectedTab = function(tab) {
    $scope.selectedTab = tab;
  }

  $scope.tabClass = function(tab) {
    if ($scope.selectedTab == tab) {
      return "active";
    } else {
      return "";
    }
  }
  });

