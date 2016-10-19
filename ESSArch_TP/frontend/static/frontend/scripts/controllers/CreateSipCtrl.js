angular.module('myApp').controller('CreateSipCtrl', function CreateSipCtrl($scope, $location, $state, $stateParams){
    $state.go('home.createSip.info');
});
;
