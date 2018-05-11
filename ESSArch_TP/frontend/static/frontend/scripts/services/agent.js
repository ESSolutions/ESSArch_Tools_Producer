angular.module('myApp').factory('Agent', function ($resource, appConfig) {
    return $resource(appConfig.djangoUrl + 'agents/:id/:action/', { id: "@id" }, {
    });
});
