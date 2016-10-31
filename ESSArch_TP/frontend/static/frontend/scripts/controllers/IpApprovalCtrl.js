angular.module('myApp').controller('IpApprovalCtrl', function ($log, $scope, myService, appConfig, $http, $timeout, $state, $stateParams, $rootScope, listViewService, $interval, Resource, $uibModal, $translate){
    var vm = this;
    $scope.tree_data = [];
    $scope.expanding_property = {
        field: "name",
        displayName: "Label",
    };
    $scope.col_defs = [
    {
        field: "user",
        displayName: "Responsible",
    },
    {
        field: "time_created",
        displayName: "Date"
    },
    {
        field: "status",
        displayName: "State",
    },
    {
        field: "progress",
        displayName: "Status",
        cellTemplate: "<uib-progressbar ng-click=\"taskStepUndo(row.branch)\" class=\"progress\" value=\"row.branch[col.field]\" type=\"success\"><b>{{row.branch[col.field]+\"%\"}}</b></uib-progressbar>"
    },
    {
        cellTemplate: "<a ng-click=\"treeControl.scope.taskStepUndo(row.branch)\" ng-if=\"(row.branch.status == 'SUCCESS' || row.branch.status == 'FAILURE') && !row.branch.undone && !row.branch.undo_type\" style=\"color: #a00\">{{'UNDO' | translate}}</a></br ><a ng-click=\"treeControl.scope.taskStepRedo(row.branch)\" ng-if=\"row.branch.undone\"style=\"color: #0a0\">{{'REDO' | translate}}</a>"
    }
    ];
    $scope.myTreeControl = {};
    $scope.myTreeControl.scope = this;
    //Undo step/task
    $scope.myTreeControl.scope.taskStepUndo = function(branch) {
        $http({
            method: 'POST',
            url: branch.url+"undo/"
        }).then(function(response) {
            console.log("UNDO");
        }, function() {
            console.log("error");
        });
    };
    //Redo step/task
    $scope.myTreeControl.scope.taskStepRedo = function(branch){
        $http({
            method: 'POST',
            url: branch.url+"retry/"
        }).then(function(response) {
            console.log("REDO");
        }, function() {
            console.log("error");
        });
    };
    $scope.currentStepTask = {id: ""}
    //Click funciton for steps and tasks
    $scope.stepTaskClick = function(branch) {
        if(branch.isTask){
            if($scope.stepTaskInfoShow && $scope.currentStepTask.id == branch.id){
                $scope.stepTaskInfoShow = false;
            }else {
                $scope.stepTaskInfoShow = true;
                $http({
                    method: 'GET',
                    url: branch.url
                }).then(function(response){
                    $scope.currentStepTask = response.data;
                    $scope.taskInfoModal();
                }, function(response) {
                    response.status;
                });
            }
        }
    };
    //Change state
    $scope.changePath= function(path) {
        myService.changePath(path);
    };
     // Click funtion columns that does not have a relevant click function
     $scope.ipRowClick = function(row) {
         $scope.selectIp(row);
         if($scope.ip == row){
             row.class = "";
             $scope.selectedIp = {id: "", class: ""};
         }
         if($scope.eventShow) {
             $scope.eventsClick(row);
         }
         if($scope.statusShow) {
             $scope.stateClicked(row);
         }
         if ($scope.select || $scope.edit || $scope.eventlog) {
             $scope.ipTableClick(row);
         }
     }
    $scope.ipSelected = false;
    $scope.stateClicked = function(row){
        if($scope.statusShow && $scope.ip == row){
            $scope.statusShow = false;
        } else {
            $scope.statusShow = true;
            $scope.edit = false;

            $scope.statusViewUpdate(row);
        }
        $scope.subSelect = false;
        $scope.eventlog = false;
        $scope.select = false;
        $scope.eventShow = false;
        $scope.ip = row;
    };
    //Get data for status view
    $scope.getTreeData = function(row) {
        listViewService.getTreeData(row).then(function(value) {
            $scope.tree_data = value;
        });
    }
    //Update status view data
    //currently not updating every n'th second
    $scope.statusViewUpdate = function(row){
        $scope.getTreeData(row);
        if($scope.statusShow && false){
            $timeout(function() {
                $scope.getTreeData(row);
                $scope.statusViewUpdate(row);
            }, 5000)}
    };

    /*******************************************/
    /*Piping and Pagination for List-view table*/
    /*******************************************/

    var ctrl = this;
    this.itemsPerPage = 10;
    $scope.selectedIp = {id: "", class: ""};
    this.displayedIps = [];

    //Update ip table with configuration from table paginetion etc
    this.callServer = function callServer(tableState) {
        $scope.tableState = tableState;
        ctrl.isLoading = true;

        var pagination = tableState.pagination;
        var start = pagination.start || 0;     // This is NOT the page number, but the index of item in the list that you want to use to display the table.
        var number = pagination.number;  // Number of entries showed per page.
        var pageNumber = start/number+1;

        Resource.getIpPage(start, number, pageNumber, tableState, $scope.selectedIp).then(function (result) {
            ctrl.displayedIps = result.data;
            tableState.pagination.numberOfPages = result.numberOfPages;//set the number of pages so the pagination can update
            ctrl.isLoading = false;
        });
    };
    //Make ip selected and add class to visualize
    $scope.selectIp = function(row) {
        vm.displayedIps.forEach(function(ip) {
            if(ip.id == $scope.selectedIp.id){
                ip.class = "";
            }
        });
        if(row.id == $scope.selectedIp.id && !$scope.select && !$scope.statusShow && !$scope.eventShow){
            $scope.selectedIp = {id: "", class: ""};
        } else {
            row.class = "selected";
            $scope.selectedIp = row;
        }
    };
    //Click function for ip table objects
    $scope.ipTableClick = function(row) {
        if($scope.select && $scope.ip.id== row.id){
            $scope.select = false;
            $scope.eventlog = false;
            $scope.edit = false;
        } else {
            $http({
                method: 'GET',
                url: row.url
            }).then(function (response) {
                $scope.getSaProfiles(response.data);
            });
            $scope.select = true;
            $scope.eventlog = true;
            $scope.ip = row;
            $rootScope.ip = row;

        }
        $scope.eventShow = false;
        $scope.statusShow = false;
    };
    //Click funciton for event table objects
    $scope.eventsClick = function (row) {
        if($scope.eventShow && $scope.ip == row){
            $scope.eventShow = false;
            $rootScope.stCtrl = null;
        } else {
            if($rootScope.stCtrl) {
                $rootScope.stCtrl.pipe();
            }
            $scope.eventShow = true;
            getEventlogData();
            $scope.eventShow = true;
            $scope.statusShow = false;
        }
        $scope.select = false;
        $scope.edit = false;
        $scope.eventlog = false;
        $scope.ip = row;
        $rootScope.ip = row;
    };
    $scope.addEvent = function(ip, eventType, eventDetail) {
        listViewService.addEvent(ip, eventType, eventDetail).then(function(value) {
        });
    }

    //funcitons for select view
    vm.profileModel = {};
    vm.profileFields=[];
    //Click function for profile pbject
    $scope.profileClick = function(row){
        $scope.profileToSave = row.profile;
        if ($scope.selectProfile == row && $scope.subSelect){
            $scope.eventlog = false;
            $scope.edit = false;
        } else {
            $scope.eventlog = true;
            getEventlogData();
            $scope.edit = true;
            $scope.selectProfile = row;
            vm.profileModel = row.profile.specification_data;
            vm.profileFields = row.profile.template;
            vm.profileFields.forEach(function(field) {
                if(field.fieldGroup != null){
                    field.fieldGroup.forEach(function(subGroup) {
                        subGroup.fieldGroup.forEach(function(item) {
                            item.templateOptions.disabled = true;
                        });
                    });
                } else {
                    field.templateOptions.disabled = true;
                }
            });
        }
    };
    //Get eventlog data
    function getEventlogData() {
        listViewService.getEventlogData().then(function(value){
            $scope.statusNoteCollection = value;
        });
    };

    //populating select view
    $scope.selectRowCollection = [];
    $scope.selectRowCollapse = [];
    //Get All sa profiles and set default according to ip
    $scope.getSaProfiles = function(ip) {
        listViewService.getSaProfiles(ip).then(function(value) {
            $scope.saProfile = value;
            $scope.getSelectCollection(value.profile, ip);
        });
    };
    //Get all profiles and populate select view array
    $scope.getSelectCollection = function (sa, ip) {
        $scope.selectRowCollapse = [];

        listViewService.getSelectCollection(sa, ip).then( function(value){
            $scope.selectRowCollapse = value;
        });
    };
    //Getting data for list view
    $scope.getListViewData = function() {
        vm.callServer($scope.tableState);
    };
    //$scope.getListViewData();
    //$interval(function(){$scope.getListViewData();}, 5000, false);

    //toggle visibility on profiles in select view
    $scope.showHideAllProfiles = function() {
        if($scope.selectRowCollection.length == 0){
            for(i = 0; i < $scope.selectRowCollapse.length; i++){
                $scope.selectRowCollection.push($scope.selectRowCollapse[i]);
            }
        } else {
            $scope.selectRowCollection = [];
        }
        $scope.profilesCollapse = !$scope.profilesCollapse;
    };
    //Creates and shows modal with task information
    $scope.taskInfoModal = function () {
        var modalInstance = $uibModal.open({
            animation: true,
            ariaLabelledBy: 'modal-title',
            ariaDescribedBy: 'modal-body',
            templateUrl: 'static/frontend/views/task_info_modal.html',
            scope: $scope,
            controller: 'ModalInstanceCtrl',
            controllerAs: '$ctrl'
        });
        modalInstance.result.then(function (data, $ctrl) {
        }, function () {
            $log.info('modal-component dismissed at: ' + new Date());
        });
    }

    //Executes Create sip on an ip
    $scope.createSip = function (ip) {
        $http({
            method: 'POST',
            url: ip.url+"create/",
            data: {validators: vm.validatorModel}
        })
        .then(function successCallback(response) {
            $state.reload();
        }), function errorCallback(response){
            alert(response.status);
        };
    };
    //Visibility of status view
    $scope.statusShow = false;
    //Visibility of select view
    $scope.select = false;
    //Visibility of sub-select view
    $scope.subSelect = false;
    //Visibility of edit view
    $scope.edit = false;
    //Visibility of status view
    $scope.eventlog = false;
    //Visibility of status view
    $scope.eventShow = false;
    //Toggle visibility of select view
    $scope.toggleSelectView = function () {
        if($scope.select == false){
            $scope.select = true;
        } else {
            $scope.select = false;
        }
    };
    //Toggle visibility of sub select view
    $scope.toggleSubSelectView = function () {
        if($scope.subSelect == false){
            $scope.subSelect = true;
        } else {
            $scope.subSelect = false;
        }
    };
    //toggle visibility of edit view
    $scope.toggleEditView = function () {
        if($scope.edit == false){
            $('.edit-view').show();
            $scope.edit = true;
            $scope.eventlog = true;
        } else {
            $('.edit-view').hide();
            $scope.edit = false;
            $scope.eventlog = false;
        }
    };
    //Toggle visibility of eventlog view
    $scope.toggleEventlogView = function() {
        if($scope.eventlog == false){
            $scope.eventlog = true;
        }else {
            $scope.eventlog = false;
        }
    }
    //Unlock profile and redirect to Prepare-ip
    $scope.unlockAndRedirect = function() {
            $http({
                method: 'GET',
                url: $scope.ip.url
            }).then(function(response) {
                response.data.locks.forEach(function(lock) {
                    if(lock.information_package == $scope.ip.url && lock.submission_agreement == $scope.saProfile.profile.url && lock.profile == $scope.profileToSave.url){
                        $http({
                            method: 'DELETE',
                            url: lock.url
                        }).then(function() {
                            $scope.goToPrepareIp();
                        });
                    }
                });
            });
    }
    //Change state to prepare-ip
    $scope.goToPrepareIp = function() {
        $state.go('home.createSip.prepareIp');
    }
    vm.validatorModel = {

    };
    vm.validatorFields = [
    {
        "templateOptions": {
            "type": "text",
            "label": $translate.instant('VALIDATEFILES'),
            "options": [{name: "Yes", value: 1},{name: "No", value: 0}],
        },
        "defaultValue": 1,
        "type": "select",
        "key": "validate_files",
    },
    {
        "templateOptions": {
            "type": "text",
            "label": $translate.instant('VALIDATEFILEFORMAT'),
            "options": [{name: "Yes", value: 1},{name: "No", value: 0}],
        },
        "defaultValue": 1,
        "type": "select",
        "key": "validate_file_format",
    },
    {
        "templateOptions": {
            "type": "text",
            "label": $translate.instant('VALIDATEXMLFILE'),
            "options": [{name: "Yes", value: 1},{name: "No", value: 0}],
        },
        "defaultValue": 1,
        "type": "select",
        "key": "validate_xml_file",
    },
    {
        "templateOptions": {
            "type": "text",
            "label": $translate.instant('VALIDATELOGICALPHYSICALREPRESENTATION'),
            "options": [{name: "Yes", value: 1},{name: "No", value: 0}],
        },
        "defaultValue": 1,
        "type": "select",
        "key": "validate_logical_physical_representation",
    },
    {
        "templateOptions": {
            "type": "text",
            "label": $translate.instant('VALIDATEINTEGRITY'),
            "options": [{name: "Yes", value: 1},{name: "No", value: 0}],
        },
        "defaultValue": 1,
        "type": "select",
        "key": "validate_integrity",
    }
    ];
});

