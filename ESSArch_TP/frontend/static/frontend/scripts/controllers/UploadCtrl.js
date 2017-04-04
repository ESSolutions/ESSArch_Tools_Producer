angular.module('myApp').controller('UploadCtrl', function($log, $uibModal, $timeout, $scope, $rootScope, $window, $location, $sce, $http, myService, appConfig, $state, $stateParams, listViewService, $interval, Resource, $q, $translate, $anchorScroll, PermPermissionStore, $cookies, $controller) {
    var vm = this;
    $scope.ip = $stateParams.ip;
    $scope.getFlowTarget = function() {
        return appConfig.djangoUrl+'information-packages/'+$scope.ip + '/upload/';
    };
    $scope.getQuery = function(FlowFile, FlowChunk, isTest) {
        return {destination: $stateParams.destination};
    };
    $scope.fileUploadSuccess = function(ip, file, message, flow) {
        $scope.uploadedFiles ++;
        var url = appConfig.djangoUrl+'information-packages/'+$scope.ip + '/merge-uploaded-chunks/';
        var path = $scope.getQuery().destination + file.relativePath;

        $http({
            method: 'POST',
            url: url,
            data: {'path': path}
        });
    };
    $scope.fileTransferFilter = function(file)
    {
        return file.isUploading();
    };
    $scope.resetUploadedFiles = function() {
        $scope.uploadedFiles = 0;
    }
    $scope.uploadedFiles = 0;
    $scope.flowCompleted = false;
    $scope.flowComplete = function(flow, transfers, ip) {
        if(flow.progress() === 1) {
            $scope.flowCompleted = true;
            $scope.flowSize = flow.getSize();
            $scope.flowFiles = transfers.length;
            flow.cancel();
            $scope.resetUploadedFiles();
        }
    }
    $scope.hideFlowCompleted = function() {
        $scope.flowCompleted = false;
    }
    $scope.getUploadedPercentage = function(totalSize, uploadedSize, totalFiles) {
        if(totalSize == 0 || uploadedSize/totalSize == 1) {
            return ($scope.uploadedFiles / totalFiles) * 100;
        } else {
            return (uploadedSize / totalSize) * 100;
        }
    }
});