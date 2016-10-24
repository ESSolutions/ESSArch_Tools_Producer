angular.module('myApp').controller('QualityControlCtrl', function($http, $scope, $rootScope, $state, $log, listViewService, Resource, $translate) {
    /*******************************************/
    /*Piping and Pagination for List-view table*/
    /*******************************************/
    var vm = this;
    var ctrl = this;
    this.itemsPerPage = 10;
    $scope.selectedIp = {id: "", class: ""};
    this.displayedIps = [];

    //Get data according to ip table settings and populates ip table
    this.callServer = function callServer(tableState) {
    $scope.tableState = tableState;

        var pagination = tableState.pagination;
        var start = pagination.start || 0;     // This is NOT the page number, but the index of item in the list that you want to use to display the table.
        var number = pagination.number;  // Number of entries showed per page.
        var pageNumber = start/number+1;

        Resource.getIpPage(start, number, pageNumber, tableState, $scope.selectedIp).then(function (result) {
            ctrl.displayedIps = result.data;
            tableState.pagination.numberOfPages = result.numberOfPages;//set the number of pages so the pagination can update
        });
    };
    //Make ip selected and add class to visualize
    vm.displayedIps=[];
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

    $scope.ipTableClick = function(row) {
        $scope.ip = row;
        listViewService.getSa(row.SubmissionAgreement).then(function(sa) {
            $scope.currentSa = sa;
        });
    }

            $scope.packageDescription = $translate.instant('PACKAGEDESCRIPTION');
            $scope.contentDescription = $translate.instant('CONTENTDESCRIPTION');
            $scope.authorityInformation = $translate.instant('AUTHORITYINFORMATION');
            $scope.archivalDescription = $translate.instant('ARCHIVALDESCRIPTION');
            $scope.manageContent = $translate.instant('MANAGECONTENT');

    $scope.tabsEditView = [
        {
            label: $scope.packageDescription,
            templateUrl: 'static/frontend/views/reception_delivery_description.html'
        },
        {
            label: $scope.contentDescription,
            templateUrl: "static/frontend/views/reception_package.html"
        },
        {
            label: $scope.authorityInformation,
            templateUrl: "static/frontend/views/reception_package.html"
        },
        {
            label: $scope.archivalDescription,
            templateUrl: "static/frontend/views/reception_package.html"
        },
        {
            label: $scope.managecontent,
            templateUrl: "static/frontend/views/reception_package.html"
        }
    ];
});
