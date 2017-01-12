angular.module('myApp').factory('listViewService', function ($q, $http, $state, $log, appConfig, $rootScope, $filter) {
    //Go to Given state
    function changePath(state) {
        $state.go(state);
    }
    //Gets data for list view i.e information packages
    function getListViewData(pageNumber, pageSize, filters, sortString, searchString, state) {
        var promise = $http({
            method: 'GET',
            url: appConfig.djangoUrl+'information-packages/',
            params: {
                page: pageNumber,
                page_size: pageSize,
                archival_institution: filters.institution,
                archivist_organization: filters.organization,
                archival_type: filters.type,
                archival_location: filters.location,
                other: filters.other,
                ordering: sortString,
                state: state,
                search: searchString
            }
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
    function getStatusViewData(ip, expandedNodes){
        var promise = $http({
            method: 'GET',
            url: ip.url + 'steps/',
        }).then(function(response){
            steps = response.data;
            steps.forEach(function(step){
                step.children = getChildSteps(step.child_steps);
                step.time_created = $filter('date')(step.time_created, "yyyy-MM-dd HH:mm:ss");

                var preserved_tasks = [];
                step.tasks.forEach(function(task){
                    if (!task.hidden) {
                        task.label = task.name;
                        task.user = task.responsible;
                        task.time_created = task.time_started;
                        task.isTask = true;
                        preserved_tasks.push(task);
                    }
                });

                step.tasks = preserved_tasks;

                step.children = step.children.concat(step.tasks);
                step.children.sort(function(a, b){
                    if(a.time_created != null && b.time_created == null) return -1;
                    if(a.time_created == null && b.time_created != null) return 1;
                    var a = new Date(a.time_created),
                        b = new Date(b.time_created);

                    if(a < b) return -1;
                    if(a > b) return 1;
                    return 0;
                });
                step.children = step.children.map(function(c){
                    c.time_created = $filter('date')(c.time_created, "yyyy-MM-dd HH:mm:ss");
                    return c
                });
            });
            steps = setExpanded(steps, expandedNodes);
            return steps;
        });
        return promise;
    }
    //Prepare the data for tree view in status view
    function getTreeData(row, expandedNodes) {
        return getStatusViewData(row, expandedNodes);
    }
    //Add a new event
    function addEvent(ip, eventType, eventDetail, outcome) {
        var promise = $http({
            method: 'POST',
            url: appConfig.djangoUrl+"events/",
            data: {
                "eventType": eventType.id,
                "eventOutcomeDetailNote": eventDetail,
                "eventOutcome": outcome.value,
                "information_package": ip.id
            }

        }).then(function(response) {
            return response.data;
        }, function(){

        });
        return promise;
    }
    //Returns all events for one ip
    function getEvents(ip, pageNumber, pageSize, sortString) {
        var promise = $http({
            method: 'GET',
            url: ip.url+'events/',
            params: {page: pageNumber, page_size: pageSize, ordering: sortString}
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
    //Gets event type for dropdown selection
    function getEventlogData() {
        var promise = $http({
            method: 'GET',
            url: appConfig.djangoUrl+'event-types/'
        })
        .then(function successCallback(response) {
            return response.data;
        }, function errorCallback(response){
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
            saProfile.profiles = [];
            saProfile.profileObjects = sas;
            sas.forEach(function (sa) {
                saProfile.profiles.push(sa);
                if (ip.SubmissionAgreement == sa.url){
                    saProfile.profile = sa;
                    saProfile.locked = ip.SubmissionAgreementLocked;
                }
            });
            return saProfile;
        }, function errorCallback(response){
        });
        return promise;
    }

    function getProfileByTypeFromSA(sa, type){
        return sa['profile_' + type];
    }

    function getProfileByTypeFromIP(ip, type){
        return ip['profile_' + type];
    }

    function findProfileByUrl(url, profiles){
        var p = null;

        profiles.forEach(function(profile){
            if (profile.url == url){
                p = profile;
            }
        });

        return p;
    }

    //Ligher fetching of profiles start
    function createProfileObjMinified(type, profiles, ip, sa){
        var required = false;
        var locked = false;
        var checked = false;
        var profile = null;

        p = getProfileByTypeFromIP(ip, type);
        if (p) {
            profile_from_ip = p;
            profile = profile_from_ip;
            locked = p.LockedBy ? true : false;
            checked = p.included
        }
        p = getProfileByTypeFromSA(sa, type);
        if (p){
            checked = true;
            required = true;
            if (profile == null) {
                profile = p;
            }
        }
        active = profile;
        if(profile) {
            profiles = [profile];
        }
        return {
            type_label: getProfileTypeLabel(type),
            profile_type: type,
            active: active,
            checked: checked,
            required: required,
            profiles: profiles,
            locked: locked
        };
    }

    function getProfilesFromIp(sa, ip) {
        var selectCollapse = [];
        if(sa == null) {
            return [];
        }
        if(sa.id != null){
            if(ip.profile_transfer_project) {
                selectCollapse.push(createProfileObjMinified("transfer_project", [ip.profile_transfer_project], ip, sa));
            } else {
                selectCollapse.push(createProfileObjMinified("transfer_project", [], ip, sa));
            }
            if(ip.profile_submit_description) {
                selectCollapse.push(createProfileObjMinified("submit_description", [ip.profile_submit_description], ip, sa));
            } else {
                selectCollapse.push(createProfileObjMinified("submit_description", [], ip, sa));
            }
            if(ip.profile_sip) {
                selectCollapse.push(createProfileObjMinified("sip", [ip.profile_sip], ip, sa));
            } else {
                selectCollapse.push(createProfileObjMinified("sip", [], ip, sa));
            }
            /*
            if(ip.profile_aip) {
                selectCollapse.push(createProfileObjMinified("aip", [ip.profile_aip], ip, sa));
            } else {
                selectCollapse.push(createProfileObjMinified("aip", [], ip, sa));
            }
            if(ip.profile_dip) {
                selectCollapse.push(createProfileObjMinified("dip", [ip.profile_dip], ip, sa));
            } else {
                selectCollapse.push(createProfileObjMinified("dip", [], ip, sa));
            }
            if(ip.profile_content_type) {
                selectCollapse.push(createProfileObjMinified("content_type", [ip.profile_content_type], ip, sa));
            } else {
                selectCollapse.push(createProfileObjMinified("content_type", [], ip, sa));
            }
            if(ip.profile_authority_information) {
                selectCollapse.push(createProfileObjMinified("authority_information", [ip.profile_authority_information], ip, sa));
            } else {
                selectCollapse.push(createProfileObjMinified("authority_information", [], ip, sa));
            }
            if(ip.profile_archival_description) {
                selectCollapse.push(createProfileObjMinified("archival_description", [ip.profile_archival_description], ip, sa));
            } else {
                selectCollapse.push(createProfileObjMinified("archival_description", [], ip, sa));
            }
            if(ip.profile_preservation_metadata) {
                selectCollapse.push(createProfileObjMinified("preservation_metadata", [ip.profile_preservation_metadata], ip, sa));
            } else {
                selectCollapse.push(createProfileObjMinified("preservation_metadata", [], ip, sa));
            }
            if(ip.profile_data_selection) {
                selectCollapse.push(createProfileObjMinified("data_selection", [ip.profile_data_selection], ip, sa));
            } else {
                selectCollapse.push(createProfileObjMinified("data_selection", [], ip, sa));
            }
            if(ip.profile_import) {
                selectCollapse.push(createProfileObjMinified("import", [ip.profile_import], ip, sa));
            } else {
                selectCollapse.push(createProfileObjMinified("import", [], ip, sa));
            }
            if(ip.profile_workflow) {
                selectCollapse.push(createProfileObjMinified("workflow", [ip.profile_workflow], ip, sa));
            } else {
                selectCollapse.push(createProfileObjMinified("workflow", [], ip, sa));
            }*/
            return selectCollapse;
        }
    }
    //Lighter fetching of profiles end
    function getProfileTypeLabel(type) {
        var typeMap = {
            "transfer_project": "Transfer project",
            "submit_description": "Submit description",
            "sip": "SIP",
            "aip": "AIP",
            "dip": "DIP",
            "content_type": "Content type",
            "authority_information": "Authority information",
            "archival_description": "Archival description",
            "preservation_metadata": "Preservation metadata",
            "data_selection": "Data selection",
            "import": "Import",
            "workflow": "Workflow"
        };
        return typeMap[type];
    }

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
        return getIp(ip.url).then(function(result) {
            var array = [];
            var tempElement = {
                filename: result.ObjectPath,
                created: result.CreateDate,
                size: result.ObjectSize
            };
            array.push(tempElement);
            return array;
        });
    }

    function getDir(ip, pathStr) {
        if(pathStr == "") {
            sendData = {};
        } else {
            sendData = {path: pathStr};
        }
        return $http({
            method: 'GET',
            url: ip.url + "files/",
            params: sendData
        }).then(function(response) {
            return response.data;
        });
    }
    /*******************/
    /*HELPER FUNCTIONS*/
    /*****************/

    //Set expanded nodes in array of steps
    function setExpanded(steps, expandedNodes) {
        expandedNodes.forEach(function(node) {
            steps.forEach(function(step) {
                if(step.id == node.id) {
                    step.expanded = true;
                }
                if(step.children != null){
                    if(step.children.length > 0){
                        setExpanded(step.children, expandedNodes);
                    }
                }
            });
        });
        return steps;

    }
    //Gets all profiles of a specific profile type for an IP
    function getProfiles(type){
        var promise = $http({
            method: 'GET',
            url: appConfig.djangoUrl+"profiles/",
            params: {type: type}
        })
        .then(function successCallback(response) {
            return response.data;
        }, function errorCallback(response){
            console.log(response.status);
        });
        return promise;
    };
    function getProfilesMin(type){
        var promise = $http({
            method: 'GET',
            url: appConfig.djangoUrl+"profiles/",
            params: {type: type}
        })
        .then(function successCallback(response) {
            response.data.forEach(function(profileObj) {
                profileObj.profile_name = profileObj.name;
            });
            return response.data;
        }, function errorCallback(response){
            console.log(response.status);
        });
        return promise;
    };

    //Checks if a given sa is locked to a given ip
    function saLocked(sa, ip) {
        locked = false;
        ip.locks.forEach(function (lock) {
            if(lock.submission_agreement == sa.url){
                locked = true;
            }
        });
        return locked;
    }

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
        var stepsToRemove = [];
        childSteps.forEach(function(child, idx){
            child.child_steps = getChildSteps(child.child_steps);
            var preserved_tasks = [];
            child.tasks.forEach(function(task){
                if (!task.hidden) {
                    task.user = task.responsible;
                    task.time_created = task.time_started;
                    task.isTask = true;
                    preserved_tasks.push(task);
                }
            });
            child.tasks = preserved_tasks;

            child.children = child.child_steps.concat(child.tasks);
            if(child.children.length == 0){
                stepsToRemove.push(idx);
            }
            child.isCollapsed = false;
            child.tasksCollapsed = true;

            child.children.sort(function(a, b){
                if(a.time_created != null && b.time_created == null) return -1;
                if(a.time_created == null && b.time_created != null) return 1;
                var a = new Date(a.time_created),
                    b = new Date(b.time_created);
                if(a < b) return -1;
                if(a > b) return 1;
                return 0;
            });

            child.children = child.children.map(function(c){
                c.time_created = $filter('date')(c.time_created, "yyyy-MM-dd HH:mm:ss");
                return c
            });
        });
        stepsToRemove.forEach(function(idx){
            childSteps.splice(idx, 1);
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
        prepareIp: prepareIp,
        getIp: getIp,
        getSa: getSa,
        getFileList: getFileList,
        getStructure: getStructure,
        getProfilesFromIp: getProfilesFromIp,
        getProfiles: getProfiles,
        getProfilesMin: getProfilesMin,
        getDir: getDir,
    };

});

