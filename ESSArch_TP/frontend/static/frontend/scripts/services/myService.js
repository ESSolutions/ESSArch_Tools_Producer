angular.module('myApp').factory('myService', function($location, PermPermissionStore, $anchorScroll, $http, appConfig) {
    function changePath(state) {
        $state.go(state);
    };
    function getPermissions(permissions){
        PermPermissionStore.defineManyPermissions(permissions, /*@ngInject*/ function (permissionName) {
            return permissions.includes(permissionName);
        });
        return permissions;
    }
    function hasChild(node1, node2){
        var temp1 = false;
        if (node2.children) {
            node2.children.forEach(function(child) {
                if(node1.name == child.name) {
                    temp1 = true;
                }
                if(temp1 == false) {
                    temp1 = hasChild(node1, child);
                }
            });
        }
        return temp1;
    }
    function getVersionInfo() {
        return $http({
            method: 'GET',
            url: appConfig.djangoUrl+"sysinfo/"
        }).then(function(response){
            return response.data;
        }, function() {
            console.log('error');
        })
    }
    return {
        changePath: changePath,
        getPermissions: getPermissions,
        hasChild: hasChild,
        getVersionInfo: getVersionInfo
    }
});
