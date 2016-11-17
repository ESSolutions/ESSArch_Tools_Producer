angular.module('myApp').factory('myService', function($location, PermPermissionStore) {
   function changePath(state) {
        $state.go(state);
    };
   function getPermissions(group){
            var permissions = group.permissions.map(function(currentValue){return currentValue.codename});
            PermPermissionStore.defineManyPermissions(permissions, function(permissionName) {
                return_.contains(permissions, permissionName);
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
    return {
        changePath: changePath,
        getPermissions: getPermissions,
        hasChild: hasChild
    }
});
