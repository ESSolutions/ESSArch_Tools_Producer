angular.module('myApp').controller('EventCtrl', ['Resource', function (service) {

    var ctrl = this;
    this.itemsPerPage = 10;

    this.displayed = [];

    this.callServer = function callServer(tableState) {

        ctrl.isLoading = true;

        var pagination = tableState.pagination;
        console.log(pagination);
        var start = pagination.start || 0;     // This is NOT the page number, but the index of item in the list that you want to use to display the table.
        var number = pagination.number;  // Number of entries showed per page.
        var pageNumber = start/number+1;

        service.getPage(start, number, pageNumber, tableState).then(function (result) {
            ctrl.displayed = result.data;
            tableState.pagination.numberOfPages = result.numberOfPages;//set the number of pages so the pagination can update
            ctrl.isLoading = false;
        });
    };

}]);
