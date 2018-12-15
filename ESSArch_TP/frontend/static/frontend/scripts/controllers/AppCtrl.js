angular.module('essarch.controllers').controller('AppCtrl', function($rootScope, $scope, $uibModal, $log) {
    var vm = this;
    var questionMark = 187;
    vm.questionMarkListener = function(e) {
        if(e.shiftKey) {
            $('#list-view *').attr('UNSELECTABLE', 'on');
            $("#list-view").css(
                {
                    '-moz-user-select': 'none',
                    '-o-user-select': 'none',
                    '-khtml-user-select': 'none',
                    '-webkit-user-select': 'none',
                    '-ms-user-select': 'none',
                    'user-select': 'none'
                }
            );
            if(e.keyCode == questionMark) {
                $scope.keyboardShortcutModal();
            }
        }
    }

    //Create and show modal for keyboard shortcuts
    $scope.keyboardShortcutModal = function () {
        var modalInstance = $uibModal.open({
            animation: true,
            ariaLabelledBy: 'modal-title',
            ariaDescribedBy: 'modal-body',
            templateUrl: 'static/frontend/views/keyboard_shortcuts_modal.html',
            controller: 'ModalInstanceCtrl',
            controllerAs: '$ctrl'
        })
        modalInstance.result.then(function (data) {
        }, function () {
            $log.info('modal-component dismissed at: ' + new Date());
        });
    }

    $rootScope.mapStepStateProgress = function(row) {
        var property = angular.isUndefined(row.step_state) ? 'status' : 'step_state';
        switch (row[property]) {
            case 'SUCCESS':
                return 'success';
            case 'FAILURE':
                return 'danger';
            case 'STARTED':
                return 'warning';
            default:
                return 'warning';
        }
    }
});
