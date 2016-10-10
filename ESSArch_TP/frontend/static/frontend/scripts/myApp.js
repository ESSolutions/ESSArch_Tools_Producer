angular.module('myApp', ['ngRoute', 'treeControl', 'ui.bootstrap', 'formly', 'formlyBootstrap', 'smart-table', 'treeGrid', 'ui.router', 'ngCookies', 'permission'])
    .config(function($routeProvider, formlyConfigProvider, $stateProvider, $urlRouterProvider, $rootScopeProvider, $uibTooltipProvider) {
    $stateProvider
        .state('home', {
            url: '/',
            templateUrl: '/static/frontend/views/home.html',
        })
    .state('login', {
        url: '/login',
        templateUrl: '/static/frontend/views/login.html',
        controller: 'LoginCtrl as vm',
        resolve: {
          authenticated: ['djangoAuth', function(djangoAuth){
            return djangoAuth.authenticationStatus();
          }],
        }
    })
    .state('logout', {
        url: '/logout',
        templateUrl: '/static/frontend/views/logout.html',
        controller: 'LogoutCtrl as vm',
        resolve: {
          authenticated: ['djangoAuth', function(djangoAuth){
            return djangoAuth.authenticationStatus();
          }],
        }
    })
    .state('home.myPage', {
        url: 'my-page',
        templateUrl: '/static/frontend/views/my_page.html',
        resolve: {
          authenticated: ['djangoAuth', function(djangoAuth){
            return djangoAuth.authenticationStatus();
          }],
        }
    })
    .state('home.createSip', {
        url: 'create-SIP',
        templateUrl: '/static/frontend/views/create_sip.html',
        redirectTo: 'createSip.info',
        controller: 'CreateSipCtrl as vm',
        resolve: {
          authenticated: ['djangoAuth', function(djangoAuth){
            return djangoAuth.authenticationStatus();
          }],
        }
    })
    .state('home.createSip.info', {
        url: '/info',
        templateUrl: '/static/frontend/views/create_sip_info.html',
        controller: 'InfoCtrl as vm',
        resolve: {
          authenticated: ['djangoAuth', function(djangoAuth){
            return djangoAuth.authenticationStatus();
          }],
        }
    })
    .state('home.createSip.prepareIp', {
        url: '/prepare-IP',
        templateUrl: '/static/frontend/views/create_sip_prepare_ip.html',
        controller: 'PrepareIpCtrl as vm',
        resolve: {
          authenticated: ['djangoAuth', function(djangoAuth){
            return djangoAuth.authenticationStatus();
          }],
        }
    })
    .state('home.createSip.dataSelection', {
        url: '/data-selection',
        templateUrl: '/static/frontend/views/create_sip_data_selection.html',
        controller: 'PrepareIpCtrl as vm',
        resolve: {
          authenticated: ['djangoAuth', function(djangoAuth){
            return djangoAuth.authenticationStatus();
          }],
        }
    })
    .state('home.createSip.dataExtraction', {
        url: '/data-extraction',
        templateUrl: '/static/frontend/views/create_sip_data_extraction.html',
        controller: 'PrepareIpCtrl as vm',
        resolve: {
          authenticated: ['djangoAuth', function(djangoAuth){
            return djangoAuth.authenticationStatus();
          }],
        }
    })
    .state('home.createSip.manageData', {
        url: '/manage-data',
        templateUrl: '/static/frontend/views/create_sip_manage_data.html',
        controller: 'PrepareIpCtrl as vm',
        resolve: {
          authenticated: ['djangoAuth', function(djangoAuth){
            return djangoAuth.authenticationStatus();
          }],
        }
    })
    .state('home.createSip.ipApproval', {
        url: '/create-SIP',
        templateUrl: '/static/frontend/views/create_sip_ip_approval.html',
        controller: 'IpApprovalCtrl as vm',
        resolve: {
          authenticated: ['djangoAuth', function(djangoAuth){
            return djangoAuth.authenticationStatus();
          }],
        }
    })
    .state('home.submitSip', {
        url: 'submit-SIP',
        templateUrl: '/static/frontend/views/submit_sip.html',
        controller: 'IpApprovalCtrl as vm',
        resolve: {
          authenticated: ['djangoAuth', function(djangoAuth){
            return djangoAuth.authenticationStatus();
          }],
        }
    })
    .state('home.submitSip.prepareSip', {
        url: '/prepare-SIP',
        templateUrl: '/static/frontend/views/submit_sip_prepare_sip.html',
        controller: 'PrepareSipCtrl as vm',
        resolve: {
          authenticated: ['djangoAuth', function(djangoAuth){
            return djangoAuth.authenticationStatus();
          }],
        }
    })
    .state('home.submitSip.reuseSip', {
        url: '/reuse-SIP',
        templateUrl: '/static/frontend/views/submit_sip_reuse_sip.html',
        controller: 'IpApprovalCtrl as vm',
        resolve: {
          authenticated: ['djangoAuth', function(djangoAuth){
            return djangoAuth.authenticationStatus();
          }],
        }
    })
    .state('home.submitSip.removeSip', {
        url: '/remove-SIP',
        templateUrl: '/static/frontend/views/submit_sip_remove_sip.html',
        controller: 'IpApprovalCtrl as vm',
        resolve: {
          authenticated: ['djangoAuth', function(djangoAuth){
            return djangoAuth.authenticationStatus();
          }],
        }
    })
    .state('home.recieveSip', {
        url: '/recieve-SIP',
        templateUrl: '/static/frontend/views/recieve_sip.html',
        controller: 'IpApprovalCtrl as vm',
        resolve: {
          authenticated: ['djangoAuth', function(djangoAuth){
            return djangoAuth.authenticationStatus();
          }],
        }
    })
    .state('restricted', {
        url: '/restricted',
        templateUrl: '/static/frontend/views/restricted.html',
        controller: 'RestrictedCtrl as vm',
        resolve: {
          authenticated: ['djangoAuth', function(djangoAuth){
            return djangoAuth.authenticationStatus();
          }],
        }
    })
    .state('authRequired', {
        url: '/auth-required',
        templateUrl: '/static/frontend/views/auth_required.html',
        controller: 'authRequiredCtrl as vm',
        resolve: {
          authenticated: ['djangoAuth', function(djangoAuth){
            return djangoAuth.authenticationStatus();
          }],
        }
    });
    $urlRouterProvider.otherwise('/');
})
.config(['$httpProvider', function($httpProvider, $rootScope) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}])
.constant('appConfig', {
    djangoUrl: "/api/"
})
.service('myService', function($location, PermPermissionStore) {
        this.changePath = function(state) {
            $state.go(state);
        };
        this.getPermissions = function(group){
            var permissions = group.permissions.map(function(currentValue){return currentValue.codename});
            PermPermissionStore.defineManyPermissions(permissions, function(permissionName) {
                return_.contains(permissions, permissionName);
            });
            return permissions;
        }
})
.run(function(djangoAuth, $rootScope, $state, $location, $cookies, PermPermissionStore, PermRoleStore, $http, myService){
    djangoAuth.initialize('/rest-auth', false).then(function() {

        djangoAuth.profile().then(function(data) {
            $rootScope.auth = data;
            console.log($rootScope.auth);
            data.groups.forEach(function(group){
                $http({
                    method: 'GET',
                    url: group
                }).then(function(response) {
                    PermRoleStore.defineRole(response.data.name, myService.getPermissions(response.data));
                }, function() {
                    console.log("error");
                });
            });
            console.log(PermRoleStore.getStore());
            console.log(PermPermissionStore.getStore());
        }, function() {
            $state.go('login');
        });

        $rootScope.$on('$stateChangeStart', function (event, toState, toParams, fromState) {
            if (toState.name === 'login' ){
                return;
            }
            if(djangoAuth.authenticated !== true){
                event.preventDefault();
                $state.go('login'); // go to login
            }

            // now, redirect only not authenticated


        });
    }, function(status) {
        console.log("when not logged in");
        console.log(status);
    });

});
