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

angular.module('essarch.services').factory('Resource', function ($q, $filter, $timeout, listViewService, $rootScope) {

    //Get data for Events table
	function getEventPage(start, number, pageNumber, params, selected, sort, columnFilters, search) {
        var sortString = sort.predicate;
        if(sort.predicate == "eventDateTime") {
            if(sort.reverse) {
                sortString = sortString + ",-id";
            } else {
                sortString = sortString + ",id";
            }
        }
        if(sort.reverse) {
            sortString = "-"+sortString;
        }
        return listViewService.getEvents($rootScope.ip, pageNumber, number, sortString, columnFilters, search).then(function(value) {
            var eventCollection = value.data;
            eventCollection.forEach(function(event) {
                selected.forEach(function(item) {
                    if(item.id == event.id) {
                        event.class = "selected";
                    }
                });
            });
            return {
                data: eventCollection,
                numberOfPages: Math.ceil(value.count / number)
            };
        });
	}
    //Get data for IP table
    function getIpPage(start, number, pageNumber, params, sort, search, state, columnFilters) {
        var sortString = sort.predicate;
        if(sort.reverse) {
            sortString = "-"+sortString;
        }
        return listViewService.getListViewData(pageNumber, number, sortString, search, state, columnFilters).then(function(value) {
            var ipCollection = value.data;
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
