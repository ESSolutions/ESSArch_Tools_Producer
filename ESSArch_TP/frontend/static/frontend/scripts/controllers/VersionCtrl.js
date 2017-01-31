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

angular.module('myApp').controller('VersionCtrl', function($scope, myService, $window, $state, marked, $anchorScroll, $location, $translate) {
    myService.getVersionInfo().then(function(result) {
        $scope.sysInfo = result;
    });
    $scope.redirectToEss = function(){
        $window.open('http://www.essolutions.se', '_blank');
    };
    $scope.scrollToLink = function(link) {
        if(!isURL(link)) {
            $location.hash(link);
            $anchorScroll();
        } else {
            $window.open(link, '_blank');
            return true;
        }
    }
    function isURL(str) {
        var urlRegex = '^(?!mailto:)(?:(?:http|https|ftp)://)(?:\\S+(?::\\S*)?@)?(?:(?:(?:[1-9]\\d?|1\\d\\d|2[01]\\d|22[0-3])(?:\\.(?:1?\\d{1,2}|2[0-4]\\d|25[0-5])){2}(?:\\.(?:[0-9]\\d?|1\\d\\d|2[0-4]\\d|25[0-4]))|(?:(?:[a-z\\u00a1-\\uffff0-9]+-?)*[a-z\\u00a1-\\uffff0-9]+)(?:\\.(?:[a-z\\u00a1-\\uffff0-9]+-?)*[a-z\\u00a1-\\uffff0-9]+)*(?:\\.(?:[a-z\\u00a1-\\uffff]{2,})))|localhost)(?::\\d{2,5})?(?:(/|\\?|#)[^\\s]*)?$';
        var url = new RegExp(urlRegex, 'i');
        return str.length < 2083 && url.test(str);
    }
    $scope.docs = $translate.instant('DOCS');
    $scope.sysInfo = $translate.instant('SYSTEMINFORMATION');
    $scope.tabs = [
        {
            label: $scope.docs,
            templateUrl: 'static/frontend/views/docs.html'
        },
        {
            label: $scope.sysInfo,
            templateUrl: "static/frontend/views/sysinfo.html"
        }
    ];
});
