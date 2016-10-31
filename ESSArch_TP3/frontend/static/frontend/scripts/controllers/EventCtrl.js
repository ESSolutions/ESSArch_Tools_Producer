angular.module('myApp').controller('EventCtrl', ['Resource', '$scope', '$rootScope', 'listViewService', function (service, $scope, $rootScope, listViewService) {
    $scope.selected = [];
    $scope.displayed = [];
    //Event click funciton
    $scope.eventClick = function(row) {
        if(row.class == "selected"){
            row.class = "";
            for(i=0; i<$scope.selected.length; i++){
                if($scope.selected[i].id === row.id){
                    $scope.selected.splice(i,1);
                }
            }
            console.log($scope.selected);
        } else {
            row.class = "selected";
            $scope.selected.push(row);
            console.log($scope.selected);
        }
    };
    $scope.addEvent = function(ip, eventType, eventDetail) {
        listViewService.addEvent(ip, eventType, eventDetail).then(function(value) {
            $rootScope.stCtrl.pipe();
            console.log(value);
        });
    }
    //Get data from rest api for event table
    $scope.eventPipe = function(tableState, ctrl) {
        $rootScope.stCtrl = ctrl;
        var pagination = tableState.pagination;
        var start = pagination.start || 0;     // This is NOT the page number, but the index of item in the list that you want to use to display the table.
        var number = pagination.number || 10;  // Number of entries showed per page.
        var pageNumber = start/number+1;

        service.getEventPage(start, number, pageNumber, tableState, $scope.selected).then(function (result) {
            $scope.displayed = result.data;
            tableState.pagination.numberOfPages = result.numberOfPages;//set the number of pages so the pagination can update
            $scope.tableState = tableState;
        });
    };

}]);
