angular.module('myApp').factory('Profile', function ($resource, appConfig) {
    return $resource(appConfig.djangoUrl + 'profiles/:id/:action/', { id: "@id" }, {
        get: {
            method: "GET",
            params: { id: "@id" }
        },
        save: {
            method: "POST",
            params: { action: "save", id: "@id" }
        },
        lock: {
            method: "POST",
            params: { action: "lock", id: "@id" }
        }
    });
});