angular.module('myApp', ['ngRoute', 'treeControl', 'ui.bootstrap', 'formly', 'formlyBootstrap', 'smart-table']).config(function($routeProvider, formlyConfigProvider) {
    $routeProvider
        .when('/', {
            templateUrl: '/static/frontend/views/my_page.html'
        })
    .when('/create-SIP', {
        templateUrl: '/static/frontend/views/create_sip.html',
        controller: 'PrepareIpCtrl as vm'
    })
    .when('/create-SIP/info', {
        templateUrl: '/static/frontend/views/create_sip_info.html',
        controller: 'InfoCtrl as vm'
    })
    .when('/create-SIP/prepare-IP', {
        templateUrl: '/static/frontend/views/create_sip_prepare_ip.html',
        controller: 'PrepareIpCtrl as vm'
    })
    .when('/create-SIP/IP-approval', {
        templateUrl: '/static/frontend/views/create_sip_ip_approval.html',
        controller: 'IpApprovalCtrl as vm'
    })
    .when('/submit-SIP', {
        templateUrl: '/static/frontend/views/submit_sip.html'
    })
    .when('/recieve-SIP', {
        templateUrl: '/static/frontend/views/recieve_sip.html'
    })
    .otherwise({
        redirectTo: '/404'
    });
})
.config(['$httpProvider', function($httpProvider, $rootScope) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}])
.constant('appConfig', {
    djangoUrl: "http://localhost:8000/api/"
})
.factory('myService', function($location) {
    return {
        changePath: function(path) {
            $location.path(path);
        }
    };

});
