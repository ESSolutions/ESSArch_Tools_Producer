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

angular.module('myApp').controller('AngularTreeCtrl', function AngularTreeCtrl(Agent, $scope, $http, $rootScope, appConfig) {
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
    };

    $scope.Agent = [];
    $rootScope.loadNavigation = function(ipState) {
        Agent.query({
            ip_state: ipState
        }).$promise.then(function(data) {
            $scope.Agent = [];
            data.forEach(function(agent) {
                var agentName = agent.role + " " + agent.type;
                agentName = agentName.charAt(0).toUpperCase() + agentName.slice(1).toLowerCase();
                var agent_role_type = $scope.Agent.find(function(element) {
                    return element.name === agentName;
                });

                if (agent_role_type === undefined){
                    agent_role_type = {
                        "name": agentName,
                        "children": []
                    };
                    $scope.Agent.push(agent_role_type);
                }
                var existing_agent = agent_role_type.children.find(function(element) {
                    return element.id === agent.id;
                });
                if (existing_agent === undefined) {
                    agent_role_type.children.push(agent);
                }
            });
            $scope.Agent.sort(function(a,b){
                return a.name > b.name;
            });
        });
    }
    $rootScope.navigationFilter = {
        agents: null,
    };

    $scope.showSelectedAgent = function(node) {
        $scope.nodeOther = null;
        $rootScope.navigationFilter.other = null;
        if(angular.isUndefined(node.id)){
            $rootScope.navigationFilter.agents = null;
            return;
        }
        if($rootScope.navigationFilter.agents == node.id) {
            $rootScope.navigationFilter.agents = null;
        } else {
            $rootScope.navigationFilter.agents = node.id;
        }
    }
});
