/*
    ESSArch is an open source archiving and digital preservation system

    ESSArch Tools for Producer (ETP)
    Copyright (C) 2005-2017 ES Solutions AB

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.

    Contact information:
    Web - http://www.essolutions.se
    Email - essarch@essolutions.se
*/

angular
  .module('essarch.controllers')
  .controller('OrganizationCtrl', function($scope, $rootScope, $cookies, Organization) {
    $scope.changeOrganization = function() {
      var org = $scope.currentOrganization;
      Organization.setOrganization(org);
    };
    $scope.getCurrentOrganization = function() {
      $scope.currentOrganization = Organization.getOrganization();
    };

    $scope.loadOrganizations = function() {
      $scope.availableOrganizations = Organization.availableOrganizations();
    };

    $scope.loadOrganizations();
    $scope.getCurrentOrganization();
  })
  .factory('Organization', function($rootScope, $cookies, $http, $state, appConfig, myService) {
    var service = {
      availableOrganizations: function() {
        return $rootScope.auth.organizations;
      },
      setOrganization: function(org) {
        $http.patch(appConfig.djangoUrl + 'me/', {current_organization: org.id}).then(function(response) {
          $rootScope.auth = response.data;
          $rootScope.auth.current_organization = org;
          myService.getPermissions(response.data.permissions);
          $state.reload();
        });
      },
      getOrganization: function() {
        return $rootScope.auth.current_organization;
      },
    };
    return service;
  });
