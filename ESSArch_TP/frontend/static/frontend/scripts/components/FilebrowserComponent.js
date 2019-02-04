angular.module('essarch.components').component('filebrowser', {
  templateUrl: 'static/frontend/views/filebrowser.html',
  controller: 'FilebrowserController',
  controllerAs: 'vm',
  bindings: {
    ip: '<',
    browserstate: '=',
  },
});
