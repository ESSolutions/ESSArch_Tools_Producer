angular.module('myApp').controller('FilebrowserController', function ($scope, $rootScope, appConfig, listViewService, $uibModal) {
    $scope.previousGridArrays = [];
    $scope.ip = $rootScope.ip;
    $scope.previousGridArraysString = function () {
        var retString = "";
        $scope.previousGridArrays.forEach(function (card) {
            retString = retString.concat(card.name, "/");
        });
        return retString;
    }
    $scope.deckGridData = [];
    $scope.deckGridInit = function (ip) {
        listViewService.getDir(ip, null).then(function (dir) {
            $scope.deckGridData = dir;
        });
    };
    if($rootScope.ip) {
        $scope.deckGridInit($rootScope.ip);
    }
    $scope.$watch(function () { return $rootScope.ip; }, function (newValue, oldValue) {
        $scope.ip = $rootScope.ip;
        $scope.deckGridInit($rootScope.ip);
        $scope.previousGridArrays = [];
    }, true);
    $scope.previousGridArray = function () {
        $scope.previousGridArrays.pop();
        listViewService.getDir($scope.ip, $scope.previousGridArraysString()).then(function (dir) {
            $scope.deckGridData = dir;
            $scope.selectedCards = [];
        });
    };
    $scope.gridArrayLoading = false;
    $scope.updateGridArray = function (ip) {
        $scope.gridArrayLoading = true;
        listViewService.getDir($scope.ip, $scope.previousGridArraysString()).then(function (dir) {
            $scope.deckGridData = dir;
            $scope.gridArrayLoading = false;
        });
    };
    $scope.expandFile = function (ip, card) {
        if (card.type == "dir") {
            $scope.previousGridArrays.push(card);
            listViewService.getDir(ip, $scope.previousGridArraysString()).then(function (dir) {
                $scope.deckGridData = dir;
                $scope.selectedCards = [];
            });
        } else {
            $scope.getFile(card);
        }
    };
    $scope.selectedCards = [];
    $scope.cardSelect = function (card) {

        if (includesWithProperty($scope.selectedCards, "name", card.name)) {
            $scope.selectedCards.splice($scope.selectedCards.indexOf(card), 1);
        } else {
            $scope.selectedCards.push(card);
        }
    };

    function includesWithProperty(array, property, value) {
        for (i = 0; i < array.length; i++) {
            if (array[i][property] === value) {
                return true;
            }
        }
        return false;
    }

    $scope.createFolder = function (folderName) {
        var folder = {
            "type": "dir",
            "name": folderName
        };
        var fileExists = false;
        $scope.deckGridData.forEach(function (chosen, index) {
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

    $scope.getFile = function(file) {
        listViewService.getFile($scope.ip, $scope.previousGridArraysString(), file).then(function(response) {
            file.content = response.data;
            $scope.textfileModal(file);
        });
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
                .then(function () {
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
            controllerAs: '$ctrl',
        })
        modalInstance.result.then(function (data) {
            $scope.createFolder(data.dir_name);
        });
    }
    $scope.textfileModal = function (file) {
        var modalInstance = $uibModal.open({
            animation: true,
            ariaLabelledBy: 'modal-title',
            ariaDescribedBy: 'modal-body',
            templateUrl: 'static/frontend/views/textfile_modal.html',
            scope: $scope,
            size: 'lg',
            controller: 'FileModalInstanceCtrl',
            controllerAs: '$ctrl',
                        resolve: {
                data: function () {
                    return {
                        file: file,
                    };
                }
            },
        })
        modalInstance.result.then(function (data) {
        });
    }
    $scope.removeFiles = function () {
        $scope.selectedCards.forEach(function (file) {
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
    $scope.getFileExtension = function (file) {
        return file.name.split(".").pop().toUpperCase();
    }
});