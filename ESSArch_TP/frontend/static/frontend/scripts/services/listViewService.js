angular.module('myApp').service('listViewService', function($q, $http, $state, $log, appConfig) {
        this.changePath = function(state) {
            $state.go(state);
        }
        this.getListViewData = function() {
            var promise = $http({
                method: 'GET',
                url: appConfig.djangoUrl+'information-packages/'
            })
            .then(function successCallback(response) {
                return response.data;
            }, function errorCallback(response){
            });
            return promise;
        }
    this.getTreeData = function(row) {
        var promise = $http({
            method: 'GET',
            url: row.url,
        }).then(function(response){
            ip = response.data;
            $scope.getStatusViewData(ip).then(function(steps){
                $scope.tree_data = steps;
            });
        });
        return promise;
    }
    this.addEvent = function(ip, eventType, eventDetail) {
        var promise = $http({
            method: 'POST',
            url: appConfig.djangoUrl+"events/",
            data: {
                "eventType": eventType.id,
                "eventDetail": eventDetail,
                "information_package": ip.id
            }

        }).then(function(response) {
            return response.data;
        }, function(){

        });
        return promise;
    }
});

