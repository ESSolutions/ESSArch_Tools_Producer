angular.module('myApp').factory('listViewService', function ($q, $http, $state, $log, appConfig) {
    //Go to Given state
    function changePath(state) {
        $state.go(state);
    }
    //Gets data for list view i.e information packages
    function getListViewData(pageNumber, pageSize) {
        var promise = $http({
            method: 'GET',
            url: appConfig.djangoUrl+'information-packages/',
            params: {page: pageNumber, page_size: pageSize}
        })
        .then(function successCallback(response) {
            count = response.headers('Count');
            if (count == null) {
                count = response.data.length;
            }
            return {
                count: count,
                data: response.data
            };
        }, function errorCallback(response){
        });
        return promise;
    }
    //Get data for status view. child steps and tasks
    function getStatusViewData(ip){
        var promise = $http({
            method: 'GET',
            url: ip.url + 'steps',
        }).then(function(response){
            steps = response.data;
            steps.forEach(function(step){
                step.children = getChildSteps(step.child_steps);
                step.tasks.forEach(function(task){
                    task.label = task.name;
                    task.time_created = task.time_started;
                    task.isTask = true;
                });
                step.children = step.children.concat(step.tasks);
            });
            return steps;
        });
        return promise;
    }
    //Prepare the data for tree view in status view
    function getTreeData(row) {
        var promise = $http({
            method: 'GET',
            url: row.url,
        }).then(function(response){
            ip = response.data;
            return getStatusViewData(ip);
        });
        return promise;
    }
    //Add a new event
    function addEvent(ip, eventType, eventDetail) {
        var promise = $http({
            method: 'POST',
            url: appConfig.djangoUrl+"events/",
            data: {
                "eventType": eventType.id,
                "eventDetail": eventDetail,
                "information_package": ip.id
            }

        }).then(function(response) {
            return response.data;
        }, function(){

        });
        return promise;
    }
    //Returns all events for one ip
    function getEvents(ip, pageNumber, pageSize) {
        var promise = $http({
            method: 'GET',
            url: ip.url+'events/',
            params: {page: pageNumber, page_size: pageSize}
        })
        .then(function successCallback(response) {
            count = response.headers('Count');
            if (count == null) {
                count = response.data.length;
            }
            return {
                count: count,
                data: response.data
            };
        }, function errorCallback(response){
            alert(response.status);
        });
        return promise;
    }
    //Gets event type for dropdown selection
    function getEventlogData() {
        var promise = $http({
            method: 'GET',
            url: appConfig.djangoUrl+'event-types/'
        })
        .then(function successCallback(response) {
            return response.data;
        }, function errorCallback(response){
            alert(response.status);
        });
        return promise;

    }
    //Returns map structure for a profile
    function getStructure(profileUrl) {
        console.log(profileUrl)
        return $http({
            method: 'GET',
            url: profileUrl
        }).then(function(response) {
            console.log(response.data.structure);
            return response.data.structure;
        }, function(response) {
        });
    }
    //returns all SA-profiles and current as an object
    function getSaProfiles(ip) {
        var sas = [];
        var saProfile =
        {
            entity: "PROFILE_SUBMISSION_AGREEMENT",
            profile: null,
            profiles: [

            ],
        };
        var promise = $http({
            method: 'GET',
            url: appConfig.djangoUrl+'submission-agreements/'
        })
        .then(function successCallback(response) {
            sas = response.data;
            var tempProfiles = [];
            saProfile.profileObjects = sas;
            sas.forEach(function (sa) {
                tempProfiles.push(sa);
                sa.information_packages.forEach(function (informationPackage) {
                    if(informationPackage == ip.url){
                        saProfile.profile = sa;
                        saProfile.profile.includedProfiles = [];
                    }
                });
            });
            saProfile.profiles = tempProfiles;
            return saProfile;
        }, function errorCallback(response){
            alert(response.status);
        });
        return promise;
    }
    //Returns an array consisting of profile objects for an SA
    function getSelectCollection(sa, ip) {
        if(sa == null) {
            var deferred = $q.defer();
            deferred.resolve([]);
            return deferred.promise;
        }
        return getIp(ip.url).then(function(value) {
            ip = value;
            if(sa.id != null) {
                var selectRowCollapse = [];
                getProfiles("transfer_project", sa.profile_transfer_project, selectRowCollapse, sa, ip).then(function(value) {
                    selectRowCollapse = value;
                });
                getProfiles("content_type", sa.profile_content_type, selectRowCollapse, sa, ip).then(function(value) {
                    selectRowCollapse = value;
                });
                getProfiles("data_selection", sa.profile_data_selection, selectRowCollapse ,sa, ip).then(function(value) {
                    selectRowCollapse = value;
                });
                getProfiles("classification", sa.profile_classification, selectRowCollapse, sa, ip).then(function(value) {
                    selectRowCollapse = value;
                });
                getProfiles("import", sa.profile_import, selectRowCollapse, sa, ip).then(function(value) {
                    selectRowCollapse = value;
                });
                getProfiles("submit_description", sa.profile_submit_description, selectRowCollapse, sa, ip).then(function(value) {
                    selectRowCollapse = value;
                });
                getProfiles("sip", sa.profile_sip, selectRowCollapse, sa, ip).then(function(value) {
                    selectRowCollapse = value;
                });
                getProfiles("aip", sa.profile_aip, selectRowCollapse, sa, ip).then(function(value) {
                    selectRowCollapse = value;
                });
                getProfiles("dip", sa.profile_dip, selectRowCollapse, sa, ip).then(function(value) {
                    selectRowCollapse = value;
                });
                getProfiles("workflow", sa.profile_workflow, selectRowCollapse, sa, ip).then(function(value) {
                    selectRowCollapse = value;
                });
                getProfiles("preservation_metadata", sa.profile_preservation_metadata, selectRowCollapse, sa, ip).then(function(value) {
                    selectRowCollapse = value;
                });
                getProfiles("event", sa.profile_event, selectRowCollapse, sa, ip).then(function(value) {
                    selectRowCollapse = value;
                });
                return selectRowCollapse;
            }
        })
    };
    //Execute prepare ip, which creates a new IP
    function prepareIp(label){
        return $http({
            method: 'POST',
            url: appConfig.djangoUrl+"information-packages/",
            data: {label: label}
        }).then(function (response){
            return "created";
        });

    }
    //Returns IP
    function getIp(url) {
        return $http({
            method: 'GET',
            url: url
        }).then(function(response) {
            return response.data;
        }, function(response) {
        });
    }
    //Returns SA
    function getSa(url) {
        return $http({
            method: 'GET',
            url: url
        }).then(function(response) {
            return response.data;
        }, function(response) {
        });
    }
    //Get list of files in Ip
    function getFileList(ip) {
        var array = [];
        var tempElement = {
            filename: ip.ObjectPath,
            created: ip.CreateDate,
            size: ip.ObjectSize
        };
         array.push(tempElement);
         return array;
    }
    /*******************/
    /*HELPER FUNCTIONS*/
    /*****************/
    //Gets all profiles of a specific profile type for an IP
    function getProfiles(type, profileArray, selectRowCollapse, sa, ip){
        if(profileArray.active == null || angular.isUndefined(profileArray)){
            var deferred = $q.defer();
            deferred.resolve([]);
            return deferred.promise;
        }
        getProfile(profileArray.active.id, true, selectRowCollapse, sa, ip).then(function(value) {
            selectRowcollapse = value;
        });
        profileArray.profiles.forEach(function(profile) {
            if(profile.id != profileArray.active.id){
                getProfile(profile.id, false, selectRowCollapse, sa, ip).then(function(value) {
                    selectRowcollapse = value;
                });
            }

        });
        var promise = $http({
            method: 'GET',
            url: appConfig.djangoUrl+"profiles",
            params: {type: type}
        })
        .then(function successCallback(response) {
            var tempProfileArray = response.data;
            for(i=0;i<profileArray.profiles.length;i++){
                for(j=0;j<tempProfileArray.length;j++){
                    if(tempProfileArray[j].id == profileArray.profiles[i].id){
                        tempProfileArray.splice(j,1);
                    }
                }
            }
            for(i=0;i<tempProfileArray.length;i++){
                getProfile(response.data[i].id, false, selectRowCollapse, sa, ip).then(function(value) {
                    selectRowCollection = value;
                });
            }
            return selectRowCollapse;
        }, function errorCallback(response){
            alert(response.status);
        });
        return promise;
    };
    //Returns profile given profile id
    function getProfile(profile_id, defaultProfile, selectRowCollapse, saProfile, ip) {
        var promise = $http({
            method: 'GET',
            url: appConfig.djangoUrl + "profiles/" + profile_id
        })
        .then(function successCallback(response) {
            var newProfileType = true;
            for(i=0; i<selectRowCollapse.length;i++){
                if(selectRowCollapse[i].profile_type == response.data.profile_type){
                    newProfileType = false;
                    selectRowCollapse[i].profiles.push(response.data);
                    if(defaultProfile){
                        response.data.defaultProfile = true;
                        selectRowCollapse[i].profile = response.data;
                    }
                    break;
                } else {
                    newProfileType = true;
                }
            }
            if(newProfileType){
                var tempProfileObject = {
                    profile_label: response.data.profile_type.toUpperCase(),
                    profile_type: response.data.profile_type,
                    profile: {},
                    profiles: [
                        response.data
                    ],
                    checked: true,
                };
                if(defaultProfile){
                        response.data.defaultProfile = true;
                    tempProfileObject.profile = response.data;
                }
                tempProfileObject = profileLocked(tempProfileObject, saProfile.url, ip.locks);
                selectRowCollapse.push(tempProfileObject);
                return selectRowCollapse;;
            }
        }, function errorCallback(response){
            alert(response.status);
        });
        return promise;
    };
    //Checks if a profile is locked
    function profileLocked(profileObject, sa, locks) {
        profileObject.locked = false;
        locks.forEach(function (lock) {
            if(lock.submission_agreement == sa && lock.profile == profileObject.profile.url){
                profileObject.locked = true;
            }
        });
        return profileObject;
    }
    //Return child steps list and corresponding tasks on all levels of child steps
    function getChildSteps(childSteps) {
        childSteps.forEach(function(child){
            child.child_steps = getChildSteps(child.child_steps);
            child.tasks.forEach(function(task){
                task.user = child.user;
                task.time_created = task.time_started;
                task.isTask = true;
            });

            child.children = child.child_steps.concat(child.tasks);
            if(child.children.length == 0){
                child.icons = {
                    iconLeaf: "glyphicon glyphicon-alert"
                };
            }
            child.isCollapsed = false;
            child.tasksCollapsed = true;
        });
        return childSteps;
    }
    return {
        getListViewData: getListViewData,
        addEvent: addEvent,
        getEvents: getEvents,
        getTreeData: getTreeData,
        getStatusViewData: getStatusViewData,
        changePath: changePath,
        getEventlogData: getEventlogData,
        getSaProfiles: getSaProfiles,
        getSelectCollection: getSelectCollection,
        prepareIp: prepareIp,
        getIp: getIp,
        getSa: getSa,
        getFileList, getFileList,
        getStructure: getStructure,
    };

});

