angular.module('myApp').controller('EventCtrl', ['Resource', '$scope', function (service, $scope) {

    var ctrl = this;
    this.itemsPerPage = 10;
    $scope.selected = [];
    this.displayed = [];
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
    //Get data from rest api for event table
    this.callServer = function callServer(tableState) {

        ctrl.isLoading = true;

        var pagination = tableState.pagination;
        var start = pagination.start || 0;     // This is NOT the page number, but the index of item in the list that you want to use to display the table.
        var number = pagination.number;  // Number of entries showed per page.
        var pageNumber = start/number+1;

        service.getEventPage(start, number, pageNumber, tableState, $scope.selected).then(function (result) {
            ctrl.displayed = result.data;
            tableState.pagination.numberOfPages = result.numberOfPages;//set the number of pages so the pagination can update
            ctrl.isLoading = false;
            $scope.tableState = tableState;
        });
    };

}]);
