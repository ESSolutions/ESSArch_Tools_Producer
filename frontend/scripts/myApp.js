angular.module('myApp', ['ngRoute', 'treeControl', 'ui.bootstrap', 'formly', 'formlyBootstrap', 'smart-table']).config(function($routeProvider, formlyConfigProvider) {
    $routeProvider
        .when('/', {
            templateUrl: '/views/my_page.html'
        })
    .when('/create-SIP', {
        templateUrl: '/views/create_sip.html',
        controller: 'PrepareIpCtrl as vm'
    })
    .when('/create-SIP/info', {
        templateUrl: '/views/create_sip_info.html',
        controller: 'InfoCtrl as vm'
    })
    .when('/create-SIP/prepare-IP', {
        templateUrl: '/views/create_sip_prepare_ip.html',
        controller: 'PrepareIpCtrl as vm'
    })
    .when('/create-SIP/IP-approval', {
        templateUrl: '/views/create_sip_ip_approval.html',
        controller: 'IpApprovalCtrl as vm'
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
angular.module('myApp').factory('myService', function($location) {
    return {
        changePath: function(path) {
            $location.path(path);
        }
    };
});
