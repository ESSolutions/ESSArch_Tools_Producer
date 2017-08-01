angular.module('myApp').factory('IP', function ($resource, appConfig, Event, Step) {
    return $resource(appConfig.djangoUrl + 'information-packages/:id/:action/', {}, {
        get: {
            method: "GET",
            params: { id: "@id" }
        },
        query: {
            method: 'GET',
            isArray: true,
            interceptor: {
                response: function (response) {
                    response.resource.$httpHeaders = response.headers;
                    return response.resource;
                }
            },
        },
        events: {
            method: 'GET',
            params: {action: "events", id: "@id"},
            isArray: true,
            interceptor: {
                response: function (response) {
                    response.resource.forEach(function(res, idx, array) {
                        array[idx] = new Event(res);
                    });
                    response.resource.$httpHeaders = response.headers;
                    return response.resource;
                }
            },
        },
        prepare: {
            method: "POST",
        },
        create: {
            method: "POST",
            params: { action: "create", id: "@id" }
        },
        files: {
            method: "GET",
            params: { action: "files", id: "@id" },
            isArray: true
        },
        steps: {
            method: "GET",
            params: { action: "steps", id: "@id" },
            isArray: true,
            interceptor: {
                response: function (response) {
                    response.resource.forEach(function(res, idx, array) {
                        array[idx] = new Step(res);
                    });
                    response.resource.$httpHeaders = response.headers;
                    return response.resource;
                }
            },
        },
        unlockProfile: {
            method: "POST",
            params: { action: "unlock-profile", id: "@id" }
        },
        checkProfile: {
            method: "PUT",
            params: { method: "check-profile", id: "@id"}
        },
        unlockProfile: {
            method: "POST",
            params: { action: "unlock-profile", id: "@id" }
        },
        changeProfile: {
            method: "PUT",
            params: { action: "change-profile", id: "@id" }
        },
        changeSa: {
            method: "PATCH",
            params: { id: "@id" }
        },
        addFile: {
            method: "POST",
            params: { action: "files" , id: "@id" }
        },
        removeFile: {
            method: "DELETE",
            hasBody: true,
            params: { action: "files", id: "@id" },
            headers: { "Content-type": 'application/json;charset=utf-8' },
        },
        changeSa: {
            method: "PATCH",
            params: { id: "@id" },
        },
        submit: {
            method: 'POST',
            params: { action: "submit", id: "@id" }
        },
        setUploaded: {
            method: "POST",
            params: { action: "set-uploaded", id: "@id" }
        },
        mergeChunks: {
            method: "POST",
            params: { action: "merge-uploaded-chunks", id: "@id" }
        }
    });
});