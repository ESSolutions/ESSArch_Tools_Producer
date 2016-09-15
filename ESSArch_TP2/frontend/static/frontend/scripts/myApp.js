angular.module('myApp', ['ngRoute', 'treeControl', 'ui.bootstrap', 'formly', 'formlyBootstrap', 'smart-table', 'treeGrid', 'ui.router']).config(function($routeProvider, formlyConfigProvider, $stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise('/404');
    $stateProvider
        .state('myPage', {
            url: '/',
            templateUrl: '/static/frontend/views/my_page.html'
        })
    .state('createSip', {
        url: '/create-SIP',
        templateUrl: '/static/frontend/views/create_sip.html',
        redirectTo: 'createSip.info',
        controller: 'CreateSipCtrl as vm',
    })
    .state('createSip.info', {
        url: '/info',
        templateUrl: '/static/frontend/views/create_sip_info.html',
        controller: 'InfoCtrl as vm'
    })
    .state('createSip.prepareIp', {
        url: '/prepare-IP',
        templateUrl: '/static/frontend/views/create_sip_prepare_ip.html',
        controller: 'PrepareIpCtrl as vm'
    })
    .state('createSip.ipApproval', {
        url: '/IP-approval',
        templateUrl: '/static/frontend/views/create_sip_ip_approval.html',
        controller: 'IpApprovalCtrl as vm'
    })
    .state('submitSip', {
        url: '/submit-SIP',
        templateUrl: '/static/frontend/views/submit_sip.html',
        controller: 'IpApprovalCtrl as vm'
    })
    .state('submitSip.prepareSip', {
        url: '/prepare-SIP',
        templateUrl: '/static/frontend/views/submit_sip_prepare_sip.html',
        controller: 'IpApprovalCtrl as vm'
    })
    .state('submitSip.reuseSip', {
        url: '/reuse-SIP',
        templateUrl: '/static/frontend/views/submit_sip_reuse_sip.html',
        controller: 'IpApprovalCtrl as vm'
    })
    .state('submitSip.removeSip', {
        url: '/remove-SIP',
        templateUrl: '/static/frontend/views/submit_sip_remove_sip.html',
        controller: 'IpApprovalCtrl as vm'
    })
    .state('recieveSip', {
        url: '/recieve-SIP',
        templateUrl: '/static/frontend/views/recieve_sip.html',
        controller: 'IpApprovalCtrl as vm'
    })
   /* .state('login', {
        url: '/login',
        templateUrl: '/static/frontend/views/login.html',
        controller: 'LoginCtrl as vm'
    })*/;
})
.config(['$httpProvider', function($httpProvider, $rootScope) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}])
.constant('appConfig', {
    djangoUrl: "/api/"
})
.service('myService', function($location) {
        this.changePath = function(state) {
            $state.go(state);
        };
})
.run(function($rootScope) {
    $rootScope.auth = {
        name: null,
        password: null
    };
});
