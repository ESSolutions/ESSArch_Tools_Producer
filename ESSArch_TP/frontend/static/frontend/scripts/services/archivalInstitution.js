angular.module('myApp').factory('ArchivalInstitution', function ($resource, appConfig) {
    return $resource(appConfig.djangoUrl + 'archival-institutions/:id/:action/', { id: "@id" }, {
    });
});