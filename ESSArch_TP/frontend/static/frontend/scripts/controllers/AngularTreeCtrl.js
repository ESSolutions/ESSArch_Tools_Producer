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
    $scope.ArchivalInstitution = [
        {
            "name": "Archival institution",
            "children": []
        }
    ];

    $scope.ArchivistOrganization = [
        {
            "name": "Archivist organization",
            "children": []
        }
    ];

    /*
    $scope.ArchivalType = [
        {
            "name": "Archival type",
            "children": []
        }
    ];

    $scope.ArchivalLocation = [
       {
           "name": "Archival location",
           "children": []
        }
    ];
    */

    $scope.other = [
        {
            "name": "other",
            "children": []
        }
    ];

    $rootScope.loadNavigation = function() {
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
       /* $http({
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
        });*/
    }
    $rootScope.loadNavigation();
    $rootScope.navigationFilter = {
        institution: null,
        organization: null,
        type: null,
        location: null,
        other: null
    };

    $scope.showSelectedInstitution = function(node) {
        $scope.nodeOther = null;
        $rootScope.navigationFilter.other = null;
        if(angular.isUndefined(node.id)){
            $rootScope.navigationFilter.institution = null;
            return;
        }
        if($rootScope.navigationFilter.institution == node.id){
            $rootScope.navigationFilter.institution = null;
        } else {
            $rootScope.navigationFilter.institution = node.id;
        }
    }

    $scope.showSelectedOrganization = function(node) {
        $scope.nodeOther = null;
        $rootScope.navigationFilter.other = null;
        if(angular.isUndefined(node.id)){
            $rootScope.navigationFilter.organization = null;
            return;
        }
        if($rootScope.navigationFilter.organization == node.id) {
            $rootScope.navigationFilter.organization = null;
        } else {
            $rootScope.navigationFilter.organization = node.id;
        }
    }

    $scope.showSelectedType = function(node) {
        $scope.nodeOther = null;
        $rootScope.navigationFilter.other = null;
        if(angular.isUndefined(node.id)){
            $rootScope.navigationFilter.type = null;
            return;
        }
        if($rootScope.navigationFilter.type == node.id) {
            $rootScope.navigationFilter.type = null;
        } else {
            $rootScope.navigationFilter.type = node.id;
        }
    }

    $scope.showSelectedLocation = function(node) {
        $scope.nodeOther = null;
        $rootScope.navigationFilter.other = null;
       if(angular.isUndefined(node.id)){
            $rootScope.navigationFilter.location = null;
            return;
        }
       if($rootScope.navigationFilter.location == node.id) {
            $rootScope.navigationFilter.location = null;
       } else {
            $rootScope.navigationFilter.location = node.id;
       }
    }

    $scope.showSelectedOther = function(node) {
        $scope.nodeInst = null;
        $scope.nodeOrg = null;
        $scope.nodeType = null;
        $scope.nodeLoc = null;
        if($rootScope.navigationFilter.other) {
            $rootScope.navigationFilter = {
                institution: null,
                organization: null,
                type: null,
                location: null,
                other: null
            };
        } else {
            $rootScope.navigationFilter = {
                institution: null,
                organization: null,
                type: null,
                location: null,
                other: true
            };
        }
    }
});
