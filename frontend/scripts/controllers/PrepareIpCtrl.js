angular.module('myApp').controller('PrepareIpCtrl', function ($timeout, $scope, $location, $sce, $http, myService, appConfig){
    var vm = this;
    // List view
    $scope.changePath= function(path) {
        myService.changePath(path);
    };
    localStorage.setItem('tableItemSelected', "false");
    $scope.tableItemClick = function() {
        if(localStorage.getItem('tableItemSelected') == "true"){
            localStorage.setItem('tableItemSelected', "false");
        } else {
            localStorage.setItem('tableItemSelected', "true");
        }
    };
    //Getting data for list view
    $scope.getListViewData = function() {
        if(localStorage.getItem('tableItemSelected') == "false"){
            $http({
                method: 'GET',
                url: appConfig.djangoUrl+'steps/'
            })
            .then(function successCallback(response) {
                // console.log(JSON.stringify(response.data));
                var data = response.data;
                var parentRows = [];
                for (i = 0; i < data.length; i++) {
                    if(data[i].parent_step == null){
                        parentRows.push(data[i]);
                    }
                    $scope.parentRowCollection = parentRows;
                }
            }), function errorCallback(){
                alert('error');
            };
        }
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
    // Progress bar handler
    $scope.max = 100;


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

    // onSubmit function
    // prints stringified JSON representation of entered fields
    // will probably save the data later on
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
        var sendData = {"params": params, "name": "preingest.tasks.First", "processstep_pos": 1, "attempt": 1, "progress": 50, "processstep": "http://0.0.0.0:8000/steps/16130473-dbcb-4ea1-b251-e9a1e9cb8185/", "task_id": "123"};
        //{"url": "http://0.0.0.0:8000/steps/f79355fc-bb1e-4bde-958c-8e6b66c91d5b/","id": "f69355fc-bb1e-4bde-958c-8e6b66c91d5b","name": "new stuff","result": null,"type": 100,"user": "petrus","status": 0,"progress": 50,"time_created": "2016-08-05T09:39:26.987468Z","parent_step": null,"archiveobject": null,"tasks": [],"task_set": []};
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

    $scope.select = false;
    $scope.subSelect = false;
    $scope.edit = true;
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
        } else {
            $('.edit-view').hide();
            $scope.edit = false;
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
