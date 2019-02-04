angular.module('essarch.services').factory('Agent', function($resource, appConfig) {
  return $resource(appConfig.djangoUrl + 'agents/:id/:action/', {id: '@id'}, {});
});
