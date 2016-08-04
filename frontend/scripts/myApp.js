angular.module('myApp', ['ngRoute', 'treeControl', 'ui.bootstrap', 'formly', 'formlyBootstrap', 'smart-table']).config(function($routeProvider, formlyConfigProvider) {
    $routeProvider
        .when('/', {
            templateUrl: '/views/my_page.html'
        })
    .when('/create-SIP', {
        templateUrl: '/views/create_sip.html',
        controller: 'CreateSipCtrl as vm'
    })
    .when('/submit-SIP', {
        templateUrl: '/views/submit_sip.html'
    })
    .when('/recieve-SIP', {
        templateUrl: '/views/recieve_sip.html'
    })
    .otherwise({
        redirectTo: '/404'
    });
});

angular.module('myApp').config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);
