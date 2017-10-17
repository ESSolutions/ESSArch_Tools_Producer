angular.module('myApp').factory('SA', function ($resource, appConfig) {
    return $resource(appConfig.djangoUrl + 'submission-agreements/:id/:action/', {}, {
        get: {
            method: "GET",
            params: { id: "@id" }
        },
        includeType: {
            method: "POST",
            params: { action: "include-type", id: "@id" }
        },
        excludeType: {
            method: "POST",
            params: { action: "exclude-type", id: "@id" }
        },
        save: {
            method: "POST",
            params: { action: "save", id: "@id" }
        },
        update: {
            method: "PUT",
            params: { id: "@id" }
        },
        new: {
            method: "POST",
        },
        lock: {
            method: "POST",
            params: { action: "lock", id: "@id" }
        }
    });
});
