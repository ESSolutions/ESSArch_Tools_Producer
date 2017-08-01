angular.module('myApp').factory('ArchivistOrganization', function ($resource, appConfig) {
    return $resource(appConfig.djangoUrl + 'archivist-organizations/:id/:action/', { id: "@id" }, {
    });
});