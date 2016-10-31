angular.module('myApp').factory('Resource', function ($q, $filter, $timeout, listViewService, $rootScope) {

    //Get data for Events table
	function getEventPage(start, number, pageNumber, params, selected) {
        return listViewService.getEvents($rootScope.ip, pageNumber, number).then(function(value) {
            var eventCollection = value.data;
            eventCollection.forEach(function(event) {
                selected.forEach(function(item) {
                    if(item.id == event.id) {
                        event.class = "selected";
                    }
                });
            });
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
    //Get data for IP table
    function getIpPage(start, number, pageNumber, params, selected) {
        return listViewService.getListViewData(pageNumber, number).then(function(value) {
            var ipCollection = value.data;
            ipCollection.forEach(function(ip) {
                if(selected.id == ip.id) {
                    ip.class = "selected";
                }
            });
            /*
            console.log("ipCollection: ");
            console.log(ipCollection);

            var filtered = params.search.predicateObject ? $filter('filter')(ipCollection, params.search.predicateObject) : ipCollection;

            if (params.sort.predicate) {
                filtered = $filter('orderBy')(filtered, params.sort.predicate, params.sort.reverse);
            }

            var result = filtered.slice(start, start + number);
            */

            return {
                data: ipCollection,
                numberOfPages: Math.ceil(value.count / number)
            };
        });
	}

	return {
		getEventPage: getEventPage,
        getIpPage: getIpPage,
	};

});
