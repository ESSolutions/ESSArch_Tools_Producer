angular.module('myApp').controller('DropdownCtrl', function ($scope, $log) {
  $scope.items = [
    'Shortcut 1',
    'Shortcut 2',
    'Shortcut 3'
  ];
  $scope.editUserOptions = [
    'Edit profile',
    'Settings',
    'Log off'
  ];
  $scope.name = "Björn Skog";

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
