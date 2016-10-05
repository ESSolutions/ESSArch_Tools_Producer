angular.module('myApp').factory('Resource', function ($q, $filter, $timeout, listViewService, $rootScope) {

	//this would be the service to call your server, a standard bridge between your model an $http

	// the database (normally on your server)
    function getEvents(ip){
        return listViewService.getEvents($rootScope.ip).then(function(value) {
            return value;
        });
    }


	//fake call to the server, normally this service would serialize table state to send it to the server (with query parameters for example) and parse the response
	//in our case, it actually performs the logic which would happened in the server
	function getPage(start, number, pageNumber, params) {
        console.log("--getPage input variables--");
        console.log("start: ");
        console.log(start);
        console.log("number: ");
        console.log(number);
        console.log("params: ");
        console.log(params);
        console.log("$rootScope.ip: ");
        console.log($rootScope.ip);
        return listViewService.getEvents($rootScope.ip, pageNumber, number).then(function(value) {
            var eventCollection = value.data;
            /*
            console.log("eventCollection: ");
            console.log(eventCollection);

            var filtered = params.search.predicateObject ? $filter('filter')(eventCollection, params.search.predicateObject) : eventCollection;

            if (params.sort.predicate) {
                filtered = $filter('orderBy')(filtered, params.sort.predicate, params.sort.reverse);
            }

            var result = filtered.slice(start, start + number);
            */

            return {
                data: eventCollection,
                numberOfPages: Math.ceil(value.count / number)
            };
        });
	}

	return {
		getPage: getPage
	};

});
