angular.module('myApp').controller('AngularTreeCtrl', function AngularTreeCtrl($scope, $http, $rootScope, appConfig) {
    $scope.treeOptions = {
        nodeChildren: "children",
        dirSelectable: true,
        injectClasses: {
            ul: "a1",
            li: "a2",
            liSelected: "a7",
            iExpanded: "a3",
            iCollapsed: "a4",
            iLeaf: "a5",
            label: "a6",
            labelSelected: "a8"
        }
    }
    $scope.ArchivalInstitution =
        [
        { "name" : "Archival institution", "children" : [
        ]}
        ];
        $scope.ArchivistOrganization = [
        { "name" : "Archivist organization", "children" : [
            ]}
        ];
        $scope.ArchivalType = [
        { "name" : "Archival type", "children" : [
        ]}
        ];
        $scope.ArchivalLocation = [
        { "name" : "Archival location", "children" : [
        ]}
        ];
        $scope.other = [
        { "name" : "other", "children" : [
        ]}
        ];
        $scope.loadNavigation = function() {
            $http({
                method: 'GET',
                url: appConfig.djangoUrl+"archival-institutions/"
            }).then(function(response) {
                $scope.ArchivalInstitution[0].children = response.data;
            });
            $http({
                method: 'GET',
                url: appConfig.djangoUrl+"archivist-organizations/"
            }).then(function(response) {
                $scope.ArchivistOrganization[0].children = response.data;
            });
            $http({
                method: 'GET',
                url: appConfig.djangoUrl+"archival-types/"
            }).then(function(response) {
                $scope.ArchivalType[0].children = response.data;
            });
            $http({
                method: 'GET',
                url: appConfig.djangoUrl+"archival-locations/"
            }).then(function(response) {
                $scope.ArchivalLocation[0].children = response.data;
            });
        }
        $scope.loadNavigation();

});
