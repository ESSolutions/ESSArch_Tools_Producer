/*
    ESSArch is an open source archiving and digital preservation system

    ESSArch Tools for Producer (ETP)
    Copyright (C) 2005-2017 ES Solutions AB

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.

    Contact information:
    Web - http://www.essolutions.se
    Email - essarch@essolutions.se
*/

angular.module('myApp').controller('CollectContentCtrl', function(IP, $log, $uibModal, $timeout, $scope, $rootScope, $window, $location, $sce, $http, myService, appConfig, $state, $stateParams, listViewService, $interval, Resource, $q, $translate, $anchorScroll, PermPermissionStore, $cookies, $controller, $compile) {
    var vm = this;
    var ipSortString = "Prepared,Uploading";
    $controller('BaseCtrl', { $scope: $scope, vm: vm, ipSortString: ipSortString });
    vm.flowDestination = null;
    $scope.showFileUpload = true;
    $scope.currentFlowObject = null;
    // File browser interval
    var fileBrowserInterval;
    $scope.$watch(function () { return $scope.select; }, function (newValue, oldValue) {
        if (newValue) {
            $interval.cancel(fileBrowserInterval);
            fileBrowserInterval = $interval(function () { $scope.updateGridArray() }, appConfig.fileBrowserInterval);
        } else {
            $interval.cancel(fileBrowserInterval);
        }
    });
    $rootScope.$on('$stateChangeStart', function() {
        $interval.cancel(fileBrowserInterval);
    });

    //Click function for ip table
    $scope.ipTableClick = function(row) {
        if($scope.select && $scope.ip.id== row.id){
            $scope.select = false;
            $scope.eventlog = false;
            $scope.ip = null;
            $rootScope.ip = null;
            $scope.filebrowser = false;
        } else {
            $scope.ip = row;
            $rootScope.ip = row;
            $scope.deckGridInit($scope.ip);
            if(!$rootScope.flowObjects[row.object_identifier_value]) {
                $scope.createNewFlow(row);
            }
            $scope.currentFlowObject = $rootScope.flowObjects[row.object_identifier_value];
            if($scope.select) {
                $scope.showFileUpload = false;
                $timeout(function() {
                    $scope.showFileUpload = true;
                });
            }
            $scope.select = true;
            $scope.eventlog = true;
        }
        $scope.previousGridArrays = [];
        $scope.uploadDisabled = false;
        $scope.eventShow = false;
        $scope.statusShow = false;
    };

    //UPLOAD
    $scope.uploadDisabled = false;
    $scope.setUploaded = function(ip) {
        $scope.uploadDisabled = true;
        IP.setUploaded({
            id: ip.id
        }).$promise.then(function(response){
            $scope.eventlog = false;
            $scope.select = false;
            $scope.filebrowser = false;
            $timeout(function() {
                $scope.getListViewData();
                vm.updateListViewConditional();
            }, 1000);
            $scope.uploadDisabled = false;
            $anchorScroll();
        }, function(response) {
            $scope.uploadDisabled = false;
        });
    }
    $scope.updateListViewTimeout = function(timeout) {
        $timeout(function(){
            $scope.getListViewData();
        }, timeout);
    };
    //Deckgrid test
    $scope.previousGridArrays = [];
    $scope.previousGridArraysString = function() {
        var retString = "";
        $scope.previousGridArrays.forEach(function(card) {
            retString = retString.concat(card.name, "/");
        });
        return retString;
    }
    $scope.deckGridData = [];
    $scope.deckGridInit = function(ip) {
        listViewService.getDir(ip, null).then(function(dir) {
            $scope.deckGridData = dir;
        });
    };
    $scope.previousGridArray = function() {
        $scope.previousGridArrays.pop();
        listViewService.getDir($scope.ip, $scope.previousGridArraysString()).then(function(dir) {
            $scope.deckGridData = dir;
            $scope.selectedCards = [];
        });
    };
    $scope.gridArrayLoading = false;
    $scope.updateGridArray = function(ip) {
        $scope.gridArrayLoading = true;
        listViewService.getDir($scope.ip, $scope.previousGridArraysString()).then(function(dir) {
            $scope.deckGridData = dir;
            $scope.gridArrayLoading = false;
        });
    };
    $scope.expandFile = function(ip, card) {
        if(card.type == "dir"){
            $scope.previousGridArrays.push(card);
            listViewService.getDir(ip,$scope.previousGridArraysString()).then(function(dir) {
                $scope.deckGridData = dir;
                $scope.selectedCards = [];
            });
        } else {
            $scope.getFile(card);
        }
    };

    $scope.getFile = function (file) {
        file.content = $sce.trustAsResourceUrl($scope.ip.url + "files/?path=" + $scope.previousGridArraysString() + file.name);
        $window.open(file.content, '_blank');
    }
    $scope.selectedCards = [];
    $scope.cardSelect = function (card) {

        if (includesWithProperty($scope.selectedCards, "name", card.name)) {
            $scope.selectedCards.splice($scope.selectedCards.indexOf(card), 1);
        } else {
            $scope.selectedCards.push(card);
        }
    };

    function includesWithProperty(array, property, value) {
        for(i=0; i < array.length; i++) {
            if(array[i][property] === value) {
                return true;
            }
        }
        return false;
    }

    $scope.createFolder = function(folderName) {
        var folder = {
            "type": "dir",
            "name": folderName
        };
        var fileExists = false;
        $scope.deckGridData.forEach(function(chosen, index) {
            if (chosen.name === folder.name) {
                fileExists = true;
                folderNameExistsModal(index, folder, chosen);                    
            }
        });
        if (!fileExists) {
            listViewService.addNewFolder($scope.ip, $scope.previousGridArraysString(), folder)
                .then(function (response) {
                    $scope.updateGridArray();
                });
        }
    }

    function folderNameExistsModal(index, folder, fileToOverwrite) {
        var modalInstance = $uibModal.open({
            animation: true,
            ariaLabelledBy: 'modal-title',
            ariaDescribedBy: 'modal-body',
            templateUrl: 'static/frontend/views/folder-exists-modal.html',
            scope: $scope,
            controller: 'OverwriteModalInstanceCtrl',
            controllerAs: '$ctrl',
            resolve: {
                data: function () {
                    return {
                        file: folder,
                        type: fileToOverwrite.type
                    };
                }
            },
        })
        modalInstance.result.then(function (data) {
            listViewService.deleteFile($scope.ip, $scope.previousGridArraysString(), fileToOverwrite)
                .then(function() {
                    listViewService.addNewFolder($scope.ip, $scope.previousGridArraysString(), folder)
                        .then(function () {
                            $scope.updateGridArray();
                        });
                })
        });
    }
    $scope.newDirModal = function () {
        var modalInstance = $uibModal.open({
            animation: true,
            ariaLabelledBy: 'modal-title',
            ariaDescribedBy: 'modal-body',
            templateUrl: 'static/frontend/views/new-dir-modal.html',
            scope: $scope,
            controller: 'ModalInstanceCtrl',
            controllerAs: '$ctrl'
        })
        modalInstance.result.then(function (data) {
            $scope.createFolder(data.dir_name);
        });
    }

    $scope.openEadEditor = function(ip) {
        // Fixes dual-screen position                         Most browsers      Firefox
        var w = 900;
        var h = 600;
        var dualScreenLeft = $window.screenLeft != undefined ? $window.screenLeft : screen.left;
        var dualScreenTop = $window.screenTop != undefined ? $window.screenTop : screen.top;

        var width = $window.innerWidth ? $window.innerWidth : document.documentElement.clientWidth ? document.documentElement.clientWidth : screen.width;
        var height = $window.innerHeight ? $window.innerHeight : document.documentElement.clientHeight ? document.documentElement.clientHeight : screen.height;

        var left = ((width / 2) - (w / 2)) + dualScreenLeft;
        var top = ((height / 2) - (h / 2)) + dualScreenTop;
        $window.open('/static/edead/filledForm.html?id='+ip.id, 'Levente', 'scrollbars=yes, width=' + w + ', height=' + h + ', top=' + top + ', left=' + left);
    }
        $scope.getFlowTarget = function() {
        return $scope.ip.url + 'upload/';
    };
    $scope.getQuery = function(FlowFile, FlowChunk, isTest) {
        return {destination: $scope.previousGridArraysString()};
    };
    $scope.fileUploadSuccess = function(ip, file, message, flow) {
        $scope.uploadedFiles ++;
        var path = flow.opts.query.destination + file.relativePath;

        IP.mergeChunks({
            id: ip.id,
            path: path
        });
    };
    $scope.fileTransferFilter = function(file)
    {
        return file.isUploading();
    };
    $scope.removeFiles = function() {
        $scope.selectedCards.forEach(function(file) {
            listViewService.deleteFile($scope.ip, $scope.previousGridArraysString(), file)
            .then(function () {
                $scope.updateGridArray();
            });
        });
        $scope.selectedCards = [];
    }
    $scope.isSelected = function (card) {
        var cardClass = "";
        $scope.selectedCards.forEach(function (file) {
            if (card.name == file.name) {
                cardClass = "card-selected";
            }
        });
        return cardClass;
    };
    $scope.resetUploadedFiles = function() {
        $scope.uploadedFiles = 0;
    }
    $scope.uploadedFiles = 0;
    $scope.flowCompleted = false;
    $scope.flowComplete = function(flow, transfers) {
        if(flow.progress() === 1) {
            flow.flowCompleted = true;
            flow.flowSize = flow.getSize();
            flow.flowFiles = transfers.length;
            flow.cancel();
            if(flow == $scope.currentFlowObject){
                $scope.resetUploadedFiles();
            }
        }
        
        $scope.updateGridArray();
    }
    $scope.hideFlowCompleted = function(flow) {
        flow.flowCompleted = false;
    }
    $scope.getUploadedPercentage = function(totalSize, uploadedSize, totalFiles) {
        if(totalSize == 0 || uploadedSize/totalSize == 1) {
            return ($scope.uploadedFiles / totalFiles) * 100;
        } else {
            return (uploadedSize / totalSize) * 100;
        }
    }

    $scope.getFileExtension = function(file) {
        return file.name.split(".").pop().toUpperCase();
    }
    $scope.createNewFlow = function(ip) {
        var flowObj = new Flow({
            target: ip.url + 'upload/',
            simultaneousUploads: 15,
            maxChunkRetries: 5,
            chunkRetryInterval: 1000,
            headers: {'X-CSRFToken' : $cookies.get("csrftoken")},
            complete: $scope.flowComplete
        });
        flowObj.on('complete', function(){
            $scope.flowComplete(flowObj, flowObj.files);
        });
        flowObj.on('fileSuccess', function(file,message){
            $scope.fileUploadSuccess(ip, file, message, flowObj);
        });
        flowObj.on('uploadStart', function(){
            flowObj.opts.query = {destination: $scope.previousGridArraysString()};
        });
        $rootScope.flowObjects[ip.object_identifier_value] = flowObj;
    }
});
