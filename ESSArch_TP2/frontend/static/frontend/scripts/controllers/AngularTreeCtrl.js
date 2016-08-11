angular.module('myApp').controller('AngularTreeCtrl', function AngularTreeCtrl($scope) {
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
    $scope.barnOchUngdom =
        [
        { "name" : "Barn och ungdom", "children" : [
            { "name" : "asd", "children" : [] },
            { "name" : "dsa", "children" : [
                { "name" : "asddfgdfgasd", "children" : [
                    { "name" : "asdasd", "children" : [] },
                    { "name" : "asdasggffd", "children" : [] }
                ]}
            ]}
        ]}
        ];
        $scope.byggnadsnamnd = [
        { "name" : "Byggnadsnämnd", "children" : [
            { "name" : "Bygglov", "children" : [] },
            { "name" : "Personal", "children" : [
                { "name" : "asdasd", "children" : [
                    { "name" : "jjafa", "children" : [] },
                    { "name" : "asdasdfagh", "children" : [] }
                ]}
            ]}
        ]}
        ];
        $scope.miljonamnd = [
        { "name" : "Miljönämnd", "children" : [
            { "name" : "asd", "children" : [] },
            { "name" : "hshsbg", "children" : [
                { "name" : "asdasd", "children" : [
                    { "name" : "dsads", "children" : [] },
                    { "name" : "hfdhdfhd", "children" : [] }
                ]}
            ]}
        ]}
        ];


});
