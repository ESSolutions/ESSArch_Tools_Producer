'use strict';

describe('PrepareIpCtrl', function() {
    beforeEach(module('myApp'));

    var $controller, $scope;

    beforeEach(inject(function(_$controller_){
        $controller = _$controller_;
    }));

    describe('toggling', function() {
        var $scope, controller;

        beforeEach(inject(function($rootScope){
            $scope = $rootScope.$new();
            controller = $controller('PrepareIpCtrl', { $scope: $scope });
        }));

        describe('$scope.select', function() {
            it('when true sets false', function() {
                $scope.select = true;
                $scope.toggleSelectView();

                expect($scope.select).toBe(false);
            });

            it('when false sets true', function() {
                $scope.select = false;
                $scope.toggleSelectView();

                expect($scope.select).toBe(true);
            });
        });

        describe('$scope.subSelect', function() {
            it('when true sets false', function() {
                $scope.subSelect = true;
                $scope.toggleSubSelectView();

                expect($scope.subSelect).toBe(false);
            });

            it('when false sets true', function() {
                $scope.subSelect = false;
                $scope.toggleSubSelectView();

                expect($scope.subSelect).toBe(true);
            });
        });

        describe('$scope.toggleEditView', function() {
            it('when true sets false', function() {
                $scope.edit = true;
                $scope.toggleEditView();

                expect($scope.edit).toBe(false);
                expect($scope.eventlog).toBe(false);
            });

            it('when false sets true', function() {
                $scope.edit = false;
                $scope.toggleEditView();

                expect($scope.edit).toBe(true);
                expect($scope.eventlog).toBe(true);
            });
        });

        describe('$scope.toggleEventLogView', function() {
            it('when true sets false', function() {
                $scope.eventlog = true;
                $scope.toggleEventlogView();

                expect($scope.eventlog).toBe(false);
            });

            it('when false sets true', function() {
                $scope.eventlog = false;
                $scope.toggleEventlogView();

                expect($scope.eventlog).toBe(true);
            });
        });
    });
});
