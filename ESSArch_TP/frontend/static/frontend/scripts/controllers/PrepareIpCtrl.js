angular.module('myApp').controller('PrepareIpCtrl', function ($timeout, $scope, $window, $location, $sce, $http, myService, appConfig){
    var vm = this;
    $scope.redirectAdmin = function () {
        $window.location.href="/admin/";
    }
    $scope.isCollapsed = true;
    $scope.toggleCollapse = function (step) {
        if(step.isCollapsed) {
            step.isCollapsed = false;
        } else {
            step.isCollapsed = true;
        }
        console.log(step.isCollapsed);
        console.log(step);
    };
    // List view
    $scope.changePath= function(path) {
        myService.changePath(path);
    };
    $scope.stateClicked = function(row){
        if($scope.statusShow && $scope.ip== row){
            $scope.statusShow = false;
        } else {
            $scope.statusShow = true;
            $scope.edit = false;
            $scope.getStatusViewData(row);
        }
        $scope.subSelect = false;
        $scope.eventlog = false;
        $scope.select = false;
        $scope.ip= row;
    };

    $scope.ipTableClick = function(row) {
        console.log("ipobject clicked. row: "+row.Label);
        if($scope.select && $scope.ip== row){
            $scope.select = false;
            $scope.ipSelected = false;
        } else {
            $scope.select = true;
            $scope.ipSelected = true;
            $scope.getSaProfiles(row);
        }
        $scope.statusShow = false;
        $scope.ip= row;
    };

    $scope.eventsClick = function (row) {
      $scope.eventShow = true;
        if($scope.eventShow && $scope.ip== row){
            $scope.eventShow = false;
            $scope.ipSelected = false;
        } else {
            $scope.eventCollection = [];
            $http({
                method: 'GET',
                url: appConfig.djangoUrl+'events/'
            })
            .then(function successCallback(response) {
                // console.log(JSON.stringify(response.data));
                var data = response.data;
                for(i=0; i<data.length; i++){
                    if(data[i].linkingObjectIdentifierValue == row.url)
                    $scope.eventCollection.push(data[i]);
                }
            }), function errorCallback(){
                alert('error');
            };
            $scope.eventShow = true;
            $scope.ipSelected = true;
        }
        $scope.statusShow = false;
        $scope.select = false;



        $scope.ip= row;
    };
    //Getting data for list view
    $scope.getListViewData = function() {
            $http({
                method: 'GET',
                url: appConfig.djangoUrl+'information-packages/'
            })
            .then(function successCallback(response) {
                // console.log(JSON.stringify(response.data));
                var data = response.data;
                $scope.ipRowCollection = data;
            }), function errorCallback(){
                alert('error');
            };
    };
    $scope.getListViewData();
    //updates every 5 seconds
    $scope.listViewUpdate = function(){
        $timeout(function() {
            $scope.getListViewData();
            $scope.listViewUpdate();
        }, 5000)
    };
    $scope.listViewUpdate();
    //Getting data for status view
    $scope.getStatusViewData = function(row) {
        var stepRows = [];
        var childSteps = [];
        for(i=0; i<row.steps.length; i++){
            $http({
                method: 'GET',
                url: row.steps[i]
            })
            .then(function successCallback(response) {
                var data = response.data;
                childSteps = getChildSteps(data.child_steps);
                stepRows.push(data);
                taskRows = getTasks(data);
                //console.log(childSteps);
                stepRows[stepRows.length-1].taskObjects = taskRows;
                stepRows[stepRows.length-1].child_steps = childSteps;
                stepRows[stepRows.length-1].isCollapsed = true;
                stepRows[stepRows.length-1].tasksCollapsed = true;
                console.log("steprows start");
                console.log(stepRows);
                console.log("steprows end");
            }), function errorCallback(){
                alert('error(getting steps)');
            }
        }
        $scope.parentStepsRowCollection = stepRows;

    };

    //Helper functions for getStatusViewData
    function getChildSteps(childSteps) {
        if(childSteps.length == 0) {
            return [];
        }
        var steps = [];
        for(i=0; i<childSteps.length; i++){
            $http({
                method: 'GET',
                url: childSteps[i]
            })
            .then(function successCallback(response) {
                response.data.isCollapsed = false;
                response.data.child_steps = getChildSteps(response.data.child_steps);
                response.data.taskObjects = getTasks(response.data);
                response.data.tasksCollapsed = true;
                steps.push(response.data);
                console.log(steps);
            }), function errorCallback(){
                alert('error(getting child steps)');
            }
        }
        childSteps = steps;
        return childSteps;
    };

    function getTasks(step) {
        var taskRows = [];
        for(i=0; i<step.tasks.length; i++){
            $http({
                method: 'GET',
                url: step.tasks[i]
            })
            .then(function successCallback(response) {
                var data = response.data;
                taskRows.push(data);
            }), function errorCallback(){
                alert('error(getting tasks)');
            }
        }
        return taskRows;
    };

    $scope.treeOptions = {
        nodeChildren: "child_steps",
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

       //$scope.getStatusViewData();

    // Progress bar handler
    $scope.max = 100;
    //funcitons for select view
    vm.profileModel = {};
    vm.profileFields=[];
    $scope.profileClick = function(row){
        console.log(row);
        if ($scope.selectProfile == row && $scope.subSelect){
            $scope.eventlog = false;
            $scope.edit = false;
        } else {
            $scope.eventlog = true;
            $scope.edit = true;
            $scope.selectProfile = row;
            vm.profileFields = row.profile.template;
            $scope.subSelectProfile = "profile";
            $http({
                method: 'OPTIONS',
                url: appConfig.djangoUrl+'tasks/'
            })
            .then(function successCallback(response) {
                // console.log(JSON.stringify(response.data));
                var data = response.data;
                $scope.subSelectOptions = data.actions.POST.name.choices;
            }), function errorCallback(){
                alert('error');
            };
        }
        console.log("selected profile: ");
        console.log($scope.selectProfile);
    };

    //populating select view
    $scope.selectRowCollection = [];
    $scope.selectRowCollapse = [
   /* {
        entity: "PROFILE_TRANSFER_PROJECT",
        profile: {},
        profiles: [
        ],
        state: "unspecified"
    },
    {
        entity: "PROFILE_CONTENT_TYPE",
        profile: {},
        profiles: [
        ],
        state: "unspecified"
    },
    {
        entity: "PROFILE_DATA_SELECTION",
        profile: {},
        profiles: [
        ],
        state: "unspecified"
    },
    {
        entity: "PROFILE_CLASSIFICATION",
        profile: {},
        profiles: [
        ],
        state: "unspecified"
    },
    {
        entity: "PROFILE_IMPORT",
        profile: {},
        profiles: [
        ],
        state: "unspecified"
    },
    {
        entity: "PROFILE_SUBMIT_DESCRIPTION",
        profile: {},
        profiles: [
        ],
        state: "unspecified"
    },
    {
        entity: "PROFILE_SUBMISSION_INFORMATION_PACKAGE",
        profile: {},
        profiles: [
        ],
        state: "unspecified"
    },
    {
        entity: "PROFILE_ARCHIVAL_INFORMATION_PACKAGE",
        profile: {},
        profiles: [
        ],
        state: "unspecified"
    },
    {
        entity: "PROFILE_DISSEMINATION_INFORMATION_PACKAGE",
        profile: {},
        profiles: [
        ],
        state: "unspecified"
    },
    {
        entity: "PROFILE_WORKFLOW",
        profile: {},
        profiles: [
        ],
        state: "unspecified"
    },
    {
        entity: "PROFILE_PRESERVATION_METADATA",
        profile: {},
        profiles: [
        ],
        state: "unspecified"
    }*/
    ];
    $scope.saProfile =
    {
        entity: "PROFILE_SUBMISSION_AGREEMENT",
        profile: {},
        profiles: [

        ],
        state: "unspecified"
    };

    $scope.getSaProfiles = function(ip) {
        var sas = [];
        $http({
            method: 'GET',
            url: appConfig.djangoUrl+'submission-agreements'
        })
        .then(function successCallback(response) {
            // console.log(JSON.stringify(response.data));
            sas = response.data;
            var tempProfiles = [];
            $scope.submissionAgreements = sas;
            $scope.saProfile.profileObjects = sas;
            for(i=0; i<sas.length; i++){
                tempProfiles.push(sas[i]);
                if(sas[i].information_packages.url == ip.url){
                    saProfile.profile = sa[i];
                }
            }
            $scope.saProfile.profiles = tempProfiles;
            console.log("current sa: ");
            console.log($scope.currentSa);
        }), function errorCallback(){
            alert('error');
        };
    };
    $scope.getSelectCollection = function (sa) {
        $scope.currentProfiles = {};
        $scope.selectRowCollapse = [];
        for(i=0;i<sa.profile_transfer_project.length;i++){
            getProfile("profile-transfer-project/", sa.profile_transfer_project[i].id);
        }
        for(i=0;i<sa.profile_content_type.length;i++){
            getProfile("profile-content-type/", sa.profile_content_type[i].id);
        }
        for(i=0;i<sa.profile_data_selection.length;i++){
            getProfile("profile-data-selection/", sa.profile_data_selection[i].id);
        }
        for(i=0;i<sa.profile_classification.length;i++){
            getProfile("profile-classification/", sa.profile_classification[i].id);
        }
        for(i=0;i<sa.profile_import.length;i++){
            getProfile("profile-import/", sa.profile_import[i].id);
        }
        for(i=0;i<sa.profile_submit_description.length;i++){
            getProfile("profile-submit-description/", sa.profile_submit_description[i].id);
        }
        for(i=0;i<sa.profile_sip.length;i++){
            getProfile("profile-sip/", sa.profile_sip[i].id);
        }
        for(i=0;i<sa.profile_aip.length;i++){
            getProfile("profile-aip/", sa.profile_aip[i].id);
        }
        for(i=0;i<sa.profile_dip.length;i++){
            getProfile("profile-dip/", sa.profile_dip[i].id);
        }
        for(i=0;i<sa.profile_workflow.length;i++){
            getProfile("profile-workflow/", sa.profile_workflow[i].id);
        }
        for(i=0;i<sa.profile_preservation_metadata.length;i++){
            getProfile("profile-preservation-metadata/", sa.profile_preservation_metadata[i].id);
        }

    };
    function getProfile(profile_type, profile_id) {
        $http({
            method: 'GET',
            url: appConfig.djangoUrl + "profiles/" + profile_id
        })
        .then(function successCallback(response) {
            var newProfileType = true;
            for(i=0; i<$scope.selectRowCollapse.length;i++){
                if($scope.selectRowCollapse[i].profile_type == response.data.profile_type.toUpperCase()){
                    newProfileType = false;
                    $scope.selectRowCollapse[i].profiles.push(response.data);
                    break;
                } else {
                    newProfileType = true;
                }
            }
            console.log("newProfileType = " + newProfileType);
            if(newProfileType){
                var tempProfileObject = {
                    profile_type: response.data.profile_type.toUpperCase(),
                    profile: response.data,
                    profiles: [
                        response.data
                    ],
                    state: "working on it!"
                };
                $scope.selectRowCollapse.push(tempProfileObject);
            }
            /*
            switch(profile_type){
                case "profile-transfer-project/":
                    $scope.currentProfiles.profile_transfer_project = response.data;
                    $scope.selectRowCollapse[0].profiles.push(response.data);
                    $scope.selectRowCollapse[0].state = response.data.status;
                    $scope.selectRowCollapse[0].entity = response.data.profile_type.toUpperCase();
                    break;
                case "profile-content-type/":
                    $scope.currentProfiles.profile_content_type = response.data;
                    $scope.selectRowCollapse[1].profiles.push(response.data);
                    $scope.selectRowCollapse[1].state = response.data.status;
                    break;
                case "profile-data-selection/":
                    $scope.currentProfiles.profile_data_selection = response.data;
                    $scope.selectRowCollapse[2].profiles.push(response.data);
                    $scope.selectRowCollapse[2].state = response.data.status;
                    break;
                case "profile-classification/":
                    $scope.currentProfiles.profile_classification = response.data;
                    $scope.selectRowCollapse[3].profiles.push(response.data);
                    $scope.selectRowCollapse[3].state = response.data.status;
                    break;
                case "profile-import/":
                    $scope.currentProfiles.profile_import = response.data;
                    $scope.selectRowCollapse[4].profiles.push(response.data);
                    $scope.selectRowCollapse[4].state = response.data.status;
                    break;
                case "profile-submit-description/":
                    $scope.currentProfiles.profile_submit_description = response.data;
                    $scope.selectRowCollapse[5].profiles.push(response.data);
                    $scope.selectRowCollapse[5].state = response.data.status;
                    break;
                case "profile-sip/":
                    $scope.currentProfiles.profile_sip = response.data;
                    $scope.selectRowCollapse[6].profiles.push(response.data);
                    $scope.selectRowCollapse[6].state = response.data.status;
                    break;
                case "profile-aip/":
                    $scope.currentProfiles.profile_aip = response.data;
                    $scope.selectRowCollapse[7].profiles.push(response.data);
                    $scope.selectRowCollapse[7].state = response.data.status;
                    break;
                case "profile-dip/":
                    $scope.currentProfiles.profile_dip = response.data;
                    $scope.selectRowCollapse[8].profiles.push(response.data);
                    $scope.selectRowCollapse[8].state = response.data.status;
                    break;
                case "profile-workflow/":
                    $scope.currentProfiles.profile_workflow = response.data;
                    $scope.selectRowCollapse[9].profiles.push(response.data);
                    $scope.selectRowCollapse[9].state = response.data.status;
                    break;
                case "profile-preservation-metadata/":
                    $scope.currentProfiles.profile_preservation_metadata = response.data;
                    $scope.selectRowCollapse[10].profiles.push(response.data);
                    $scope.selectRowCollapse[10].state = response.data.status;
                    break;
            }
            */
        }), function errorCallback(){
            alert('error');
        };
    };
        $scope.showHideAllProfiles = function() {
            if($scope.selectRowCollection.length == 0){
                for(i = 0; i < $scope.selectRowCollapse.length; i++){
                    $scope.selectRowCollection.push($scope.selectRowCollapse[i]);
                }
            } else {
                $scope.selectRowCollection = [];
            }
            $scope.profilesCollapse = !$scope.profilesCollapse;
        };
        //Populating edit view fields
        $scope.submitDesriptionFields = [
        {
            "type": "input",
            "key": "agentname1",
            "templateOptions": {
                "type": "text",
                "label": "Archivist Organization"
            }
        },
        {
            "type": "input",
            "key": "agentname2",
            "templateOptions": {
                "type": "text",
                "label": "Archivist Software"
            }
        },
        {
            "type": "input",
            "key": "agentname3",
            "templateOptions": {
                "type": "text",
                "label": "Archivist Software"
            }
        },
        {
            "type": "input",
            "key": "agentname4",
            "templateOptions": {
                "type": "text",
                "label": "Archivist Software"
            }
        },
        {
            "type": "input",
            "key": "agentname5",
            "templateOptions": {
                "type": "text",
                "label": "Creator Organization"
            }
        },
        {
            "type": "input",
            "key": "agentname6",
            "templateOptions": {
                "type": "text",
                "label": "Producer Organization"
            }
        },
        {
            "type": "input",
            "key": "agentname7",
            "templateOptions": {
                "type": "text",
                "label": "Producer Individual"
            }
        },
        {
            "type": "input",
            "key": "agentname8",
            "templateOptions": {
                "type": "text",
                "label": "Producer Software"
            }
        },
        {
            "type": "input",
            "key": "agentname9",
            "templateOptions": {
                "type": "text",
                "label": "Submitter Organization"
            }
        },
        {
            "type": "input",
            "key": "agentname10",
            "templateOptions": {
                "type": "text",
                "label": "Submitter Individual"
            }
        },
        {
            "type": "input",
            "key": "agentname11",
            "templateOptions": {
                "type": "text",
                "label": "IPOwner Individual"
            }
        },
        {
            "type": "input",
            "key": "agentname12",
            "templateOptions": {
                "type": "text",
                "label": "Preservation Organization"
            }
        },
        {
            "type": "input",
            "key": "SUBMISSIONAGREEMENT",
            "templateOptions": {
                "type": "text",
                "label": "Submission Agreement"
            }
        },
        {
            "type": "input",
            "key": "STARTDATE",
            "templateOptions": {
                "type": "text",
                "label": "Start data"
            }
        },
        {
            "type": "input",
            "key": "ENDDATE",
            "templateOptions": {
                "type": "text",
                "label": "End date"
            }
        },
        {
            "type": "input",
            "key": "DOCUMENTID",
            "templateOptions": {
                "type": "text",
                "label": "document name"
            }
        },
        {
            "type": "input",
            "key": "INPUTFILE",
            "templateOptions": {
                "type": "text",
                "label": "tar folder"
            }
        },
        {
            "type": "input",
            "key": "MetsLABEL",
            "templateOptions": {
                "type": "text",
                "label": "Mets Label"
            }
        },
        {
            "type": "input",
            "key": "MetsType",
            "templateOptions": {
                "type": "text",
                "label": "Mets Type"
            }
        },
        {
            "type": "input",
            "key": "MetsId",
            "templateOptions": {
                "type": "text",
                "label": "Mets ID"
            }
        },
        {
            "type": "input",
            "key": "MetsOBJID",
            "templateOptions": {
                "type": "text",
                "label": "Mets OBJID"
            }
        },
        {
            "type": "input",
            "key": "MetsHdrCREATEDATE",
            "templateOptions": {
                "type": "text",
                "label": "Created Date"
            }
        },
        {
            "type": "input",
            "key": "MetsHdrRECORDSTATUS",
            "templateOptions": {
                "type": "text",
                "label": "Record Status"
            }
        }];
        // Archivist
        // Organisation
        vm.archivistOrganisationModel = {
            ArchivistOrganisation: "Sigtuna Kommun",
            ArchivistOrganisationIdentity: "",
            ArchivistOrganisationSoftware: "",
            ArchivistOrganisationSoftwareIdentity: ""
        };
        vm.archivistOrganisationFields = [
    {
        key: "ArchivistOrganisation",
        type: "select",
        templateOptions: {
            label: "Archivist organisation",
            placeholder: "ArchivistOrganisation",
            options: [
            {
                name: "Petrus", value: "Petrus"
            },
            {
                name: "oskar", value: "oskar"
            },
            {
                name: "Sigtuna kommun", value: "Sigtuna kommun"
            }
            ]
        }
    },
    {
        key: 'ArchivistOrganisationIdentity',
        type: 'input',
        templateOptions: {
            label: 'Archivist organisation identity',
            placeholder: 'Archivist organisation identity'
        }
    },
    {
        key: 'ArchivistOrganisationSoftware',
        type: 'input',
        templateOptions: {
            label: 'Archivist organisation software',
            placeholder: 'Archivist organisation software'
        }
    },
    {
        key: 'ArchivistOrganisationSoftwareIdentity',
        type: 'input',
        templateOptions: {
            label: 'Archivist organisation software identity',
            placeholder: 'Archivist organisation software identity'
        }
    }
    ];

    // Creator
    // Organisation
    vm.creatorOrganisationModel = {
        CreatorOrganisation: "Riksarkivet",
        CreatorOrganisationIdentity: "",
        CreatorOrganisationSoftware: "",
        CreatorOrganisationSoftwareIdentity: ""
    };

    vm.creatorOrganisationFields = [

    {
        key: 'CreatorOrganisation',
        type: 'input',
        defaultValue: 'Riksarkivet',
        templateOptions: {
            label: 'Creator organisation',
            placeholder: 'Creator organisation'
        }
    },
    {
        key: 'CreatorOrganisationIdentity',
        type: 'input',
        templateOptions: {
            label: 'Creator organisation identity',
            placeholder: 'Creator organisation identity'
        }
    },
    {
        key: 'CreatorOrganisationSoftware',
        type: 'input',
        templateOptions: {
            label: 'Creator organisation software',
            placeholder: 'Creator organisation software'
        }
    },
    {
        key: 'CreatorOrganisationSoftwareIdentity',
        type: 'input',
        templateOptions: {
            label: 'Creator organisation software identity',
            placeholder: 'Creator organisation software identity'
        }
    }
    ];


    // Producer
    // organisation
    vm.producerOrganisationModel = {
        ProducerOrganisation: "",
        ProducerIndividual: "",
        ProducerOrganisationSoftware: "",
        ProducerOrganisationSoftwareIdentity: ""
    };

    vm.producerOrganisationFields = [
    {
        key: 'ProducerOrganisation',
        type: 'input',
        templateOptions: {
            label: 'Producer organisation',
            placeholder: 'Producer organisation'
        }
    },
    {
        key: 'ProducerIndividual',
        type: 'input',
        templateOptions: {
            label: 'Producer individual',
            placeholder: 'Producer individual'
        }
    },
    {
        key: 'ProducerOrganisationSoftware',
        type: 'input',
        templateOptions: {
            label: 'Producer organisation software',
            placeholder: 'Producer organisation software'
        }
    },
    {
        key: 'ProducerOrganisationSoftwareIdentity',
        type: 'input',
        templateOptions: {
            label: 'Producer organisation software identity',
            placeholder: 'Producer organisation software identity'
        }
    }
    ];


    // IP Owner
    // organisation
    vm.ipOwnerOrganisationModel = {
        IpOwnerOrganisation: "",
        IpOwnerIndividual: "",
        IpOwnerOrganisationSoftware: "",
        IpOwnerOrganisationSoftwareIdentity: ""
    };

    vm.ipOwnerOrganisationFields = [
    {
        key: 'ipOwnerOrganisation',
        type: 'input',
        templateOptions: {
            label: 'IP owner organisation',
            placeholder: 'IP owner organisation'
        }
    },
    {
        key: 'IpOwnerIndividual',
        type: 'input',
        templateOptions: {
            label: 'IP owner individual',
            placeholder: 'IP owner individual'
        }
    },
    {
        key: 'IpOwnerOrganisationSoftware',
        type: 'input',
        templateOptions: {
            label: 'IP owner organisation software',
            placeholder: 'IP owner organisation software'
        }
    },
    {
        key: 'IpOwnerOrganisationSoftwareIdentity',
        type: 'input',
        templateOptions: {
            label: 'IP owner organisation software identity',
            placeholder: 'IP owner organisation software identity'
        }
    }
    ];


    // Editor
    // organisation
    vm.editorOrganisationModel = {
        EditorOrganisation: "",
        EditorIndividual: "",
        EditorOrganisationSoftware: "",
        EditorOrganisationSoftwareIdentity: ""
    };

    vm.editorOrganisationFields = [
    {
        key: 'EditorOrganisation',
        type: 'input',
        templateOptions: {
            label: 'Editor organisation',
            placeholder: 'Editor organisation'
        }
    },
    {
        key: 'EditorIndividual',
        type: 'input',
        templateOptions: {
            label: 'Editor individual',
            placeholder: 'Editor indivivual'
        }
    },
    {
        key: 'EditorOrganisationSoftware',
        type: 'input',
        templateOptions: {
            label: 'Editor organisation software',
            placeholder: 'Editor organisation software'
        }
    },
    {
        key: 'EditorOrganisationSoftwareIdentity',
        type: 'input',
        templateOptions: {
            label: 'Editor organisation software identity',
            placeholder: 'Editor organisation software identity'
        }
    }
    ];


    // Preservation
    // organisation
    vm.preservationOrganisationModel = {
        PreservationOrganisation: "",
        PreservationIndividual: "",
        PreservationOrganisationSoftware: "",
        PreservationOrganisationSoftwareIdentity: ""
    };

    vm.preservationOrganisationFields = [
    {
        key: 'PreservationOrganisation',
        type: 'input',
        templateOptions: {
            label: 'Preservation organisation',
            placeholder: 'Preservation organisation'
        }
    },
    {
        key: 'PreservationIndividual',
        type: 'input',
        templateOptions: {
            label: 'Preservation individual',
            placeholder: 'Preservation individual'
        }
    },
    {
        key: 'PreservationOrganisationSoftware',
        type: 'input',
        templateOptions: {
            label: 'Preservation organisation software',
            placeholder: 'Preservation organisation software'
        }
    },
    {
        key: 'PreservationOrganisationSoftwareIdentity',
        type: 'input',
        templateOptions: {
            label: 'Preservation organisation software identity',
            placeholder: 'Preservation organisation software identity'
        }
    }
    ];

    $scope.exampleData = "1";
    $scope.exampleSelectData = [
        "1",
        "2",
        "3"
    ];
    // onSubmit function

    vm.onSubmit = function() {
        var params = {
            info: {
                "ArchivistOrganisation": vm.archivistOrganisationModel,
                "CreatorOrganisation": vm.creatorOrganisationModel,
                "ProducerOrganisation": vm.producerOrganisationModel,
                "IpOwnerOrganisation": vm.ipOwnerOrganisationModel,
                "EditorOrganisation": vm.editorOrganisationModel,
                "PreservationOrganisation": vm.preservationOrganisationModel
            }
        };
        var sendData = {"params": params, "name": "preingest.tasks.First", "processstep_pos": 1, "attempt": 1, "progress": 50, "processstep": appConfig.djangoUrl+"steps/16130473-dbcb-4ea1-b251-e9a1e9cb8185/", "task_id": "123"};
        //{"url": "http://0.0.0.0:8000/steps/f79355fc-bb1e-4bde-958c-8e6b66c91d5b/","id": "f69355fc-bb1e-4bde-958c-8e6b66c91d5b","name": "new stuff","result": null,"type": 100,"user": "petrus","status": 0,"progress": 50,"time_created": "2016-08-05T09:39:26.987468Z","parent_step": null,"ipobject": null,"tasks": [],"task_set": []};
        var uri = appConfig.djangoUrl+'tasks/';
        $http({
            method: 'POST',
            url: uri,
            data: sendData,
        })
        .success(function (response) {
            alert('success');
        })
        .error(function (response) {
            alert('error');
        });
    };

// Page selection
//      &
// ng-show code
    $scope.statusShow = false;
    $scope.eventShow = false;
    $scope.select = false;
    $scope.subSelect = false;
    $scope.edit = false;
    $scope.eventlog = false;
    $scope.htmlPopover = $sce.trustAsHtml('<font size="3" color="red">Currently disabled</font>');
    $scope.pages = ['Info', 'Prepare Ip', 'Selection', 'Extraction', 'Manage Data', 'IP Approval', 'IP Management'];
    $scope.selectedPage = $scope.pages[0];

    $scope.toggleSelectView = function () {
        if($scope.select == false){
            $scope.select = true;
        } else {
            $scope.select = false;
        }
    };
    $scope.toggleSubSelectView = function () {
        if($scope.subSelect == false){
            $scope.subSelect = true;
        } else {
            $scope.subSelect = false;
        }
    };
    $scope.toggleEditView = function () {
        if($scope.edit == false){
            $('.edit-view').show();
            $scope.edit = true;
            $scope.eventlog = true;
        } else {
            $('.edit-view').hide();
            $scope.edit = false;
            $scope.eventlog = false;
        }
    };
    $scope.toggleEventlogView = function() {
        if($scope.eventlog == false){
            $scope.eventlog = true;
        }else {
            $scope.eventlog = false;
        }
    }




});

