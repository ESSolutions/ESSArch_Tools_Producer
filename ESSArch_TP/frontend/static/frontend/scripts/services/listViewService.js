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
  .module('essarch.services')
  .factory('listViewService', function(
    IP,
    SA,
    Event,
    EventType,
    Profile,
    $http,
    appConfig
  ) {
    /**
     * Map given table type with an url
     * @param {String} table - Type of table, example: "ip", "events", "workspace"
     * @param {string} [id] - Optional id for url
     */
    function tableMap(table, id) {
      var map = {
        ip: 'information-packages/',
        events: 'information-packages/' + id + '/events/',
        reception: 'ip-reception/',
        workspace: 'workareas/',
      };
      return map[table];
    }

    /**
     * Check number of items and how many pages a table has.
     * Used to update tables correctly when amount of pages is reduced.
     * @param {String} table - Type of table, example: "ip", "events", "workspace"
     * @param {Integer} pageSize - Page size
     * @param {Object} filters - All filters and relevant sort string etc
     * @param {String} [id] - ID used in table url, for example IP ID
     */
    function checkPages(table, pageSize, filters, id) {
      var data = angular.extend(
        {
          page: 1,
          page_size: pageSize,
        },
        filters
      );
      var url;
      if (id) {
        url = tableMap(table, id);
      } else {
        url = tableMap(table);
      }
      return $http.head(appConfig.djangoUrl + url, {params: data}).then(function(response) {
        count = response.headers('Count');
        if (count == null) {
          count = response.length;
        }
        if (count == 0) {
          count = 1;
        }
        return {
          count: count,
          numberOfPages: Math.ceil(count / pageSize),
        };
      });
    }
    //Gets data for list view i.e information packages
    function getListViewData(pageNumber, pageSize, sortString, searchString, state, columnFilters) {
      return IP.query(
        angular.extend(
          {
            page: pageNumber,
            page_size: pageSize,
            ordering: sortString,
            state: state,
            search: searchString,
          },
          columnFilters
        )
      ).$promise.then(function successCallback(resource) {
        count = resource.$httpHeaders('Count');
        if (count == null) {
          count = resource.length;
        }
        return {
          count: count,
          data: resource,
        };
      });
    }

    //Add a new event
    function addEvent(ip, eventType, eventDetail, outcome) {
      return Event.save({
        eventType: eventType.eventType,
        eventOutcomeDetailNote: eventDetail,
        eventOutcome: outcome.value,
        information_package: ip.id,
      }).$promise.then(function(response) {
        return response;
      });
    }

    //Returns all events for one ip
    function getEvents(ip, pageNumber, pageSize, sortString, columnFilters, searchString) {
      return IP.events(
        angular.extend(
          {
            id: ip.id,
            page: pageNumber,
            page_size: pageSize,
            search: searchString,
            ordering: sortString,
          },
          columnFilters
        )
      ).$promise.then(function(resource) {
        count = resource.$httpHeaders('Count');
        if (count == null) {
          count = resource.length;
        }
        return {
          count: count,
          data: resource,
        };
      });
    }
    //Gets event type for dropdown selection
    function getEventlogData() {
      return EventType.query().$promise.then(function(data) {
        return data;
      });
    }

    //Returns map structure for a profile
    function getStructure(profileId) {
      return Profile.get({
        id: profileId,
      }).then(function(data) {
        return data.structure;
      });
    }
    //returns all SA-profiles and current as an object
    function getSaProfiles(ip) {
      var sas = [];
      var saProfile = {
        entity: 'PROFILE_SUBMISSION_AGREEMENT',
        profile: null,
        profiles: [],
      };
      var promise = SA.query({
        pager: 'none',
      }).$promise.then(function(resource) {
        sas = resource;
        saProfile.profiles = [];
        sas.forEach(function(sa) {
          saProfile.profiles.push(sa);
          if (ip.submission_agreement == sa.id) {
            saProfile.profile = sa;
            saProfile.locked = ip.submission_agreement_locked;
          }
        });
        return saProfile;
      });
      return promise;
    }

    //Returns IP
    function getIp(id) {
      return IP.get({
        id: id,
      }).$promise.then(function(data) {
        return data;
      });
    }
    //Returns SA
    function getSa(id) {
      return SA.get({
        id: id,
      }).$promise.then(function(data) {
        return data;
      });
    }

    //Get list of files in Ip
    function getFileList(ip) {
      return getIp(ip.id).then(function(result) {
        var array = [];
        var tempElement = {
          filename: result.object_path,
          created: result.create_date,
          size: result.object_size,
        };
        array.push(tempElement);
        return array;
      });
    }

    function getDir(ip, pathStr, pageNumber, pageSize) {
      if (pathStr == '') {
        sendData = {};
      } else {
        sendData = {path: pathStr};
      }
      return IP.files(
        angular.extend(
          {
            id: ip.id,
            page: pageNumber,
            page_size: pageSize,
          },
          sendData
        )
      )
        .$promise.then(function(data) {
          count = data.$httpHeaders('Count');
          if (count == null) {
            count = data.length;
          }
          return {
            numberOfPages: Math.ceil(count / pageSize),
            data: data,
          };
        })
        .catch(function(response) {
          return response;
        });
    }

    function deleteFile(ip, path, file) {
      return IP.removeFile({
        id: ip.id,
        path: path + file.name,
      }).$promise.then(function(response) {
        return response;
      });
    }

    function addNewFolder(ip, path, file) {
      return IP.addFile({
        id: ip.id,
        path: path + file.name,
        type: file.type,
      }).$promise.then(function(response) {
        return response;
      });
    }

    function getFile(ip, path, file) {
      return IP.files({
        id: ip.id,
        path: path + file.name,
      }).then(function(response) {
        return response;
      });
    }

    return {
      getListViewData: getListViewData,
      addEvent: addEvent,
      getEvents: getEvents,
      getEventlogData: getEventlogData,
      getSaProfiles: getSaProfiles,
      getIp: getIp,
      getSa: getSa,
      getFileList: getFileList,
      getStructure: getStructure,
      getDir: getDir,
      deleteFile: deleteFile,
      addNewFolder: addNewFolder,
      getFile: getFile,
      checkPages: checkPages,
    };
  });
