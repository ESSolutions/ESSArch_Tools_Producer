angular.module('myApp').controller('DropdownCtrl', function ($scope, $log, $rootScope) {
  $scope.items = [
    'Shortcut 1',
    'Shortcut 2',
    'Shortcut 3'
  ];
  $scope.editUserOptions = [
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
  $scope.$watch(function() {
      return $rootScope.auth.name;
  }, function() {
      $scope.name = $rootScope.auth.name;
  }, true);


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
