angular.module('myApp').controller('CreateSipCtrl', function ($scope, $location, $sce){
    var vm = this;
    // List view
    $scope.rowCollection = [
        {label: 'Bygglov 2012', content: 'ERMS', responsible: 'Kalle Karlsson', date: '2013-01-14', state: 'Submitted', status: 100},
        {label: 'Bygglov 2013', content: 'ERMS', responsible: 'Eva Rööse', date: '2013-12-30', state: 'Created', status: 75},
        {label: 'Bygglov 2014', content: 'ERMS', responsible: 'Ove Jansson', date: '2014-12-19', state: 'Preparing', status: 40}
    ];
    // Progress bar handler
    $scope.max = 100;

// Archivist
// Organisation
vm.archivistOrganisationModel = {
    ArchivistOrganisation: "Sigtuna Kommun"
};
vm.archivistOrganisationFields = [
{
    key: 'ArchivistOrganisation',
    type: 'select',
    defaultValue: 'Sigtuna Kommun',
    templateOptions: {
            label: 'Archivist organisation',
            placeholder: 'ArchivistOrganisation',
            options: [
            {
                name: "Petrus", value: "Petrus"
            },
            {
                name: 'oskar', value: "oskar"
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
        CreatorOrganisation: "Riksarkivet"
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
        alert(JSON.stringify(vm.archivistOrganisationModel) + " "
                + JSON.stringify(vm.creatorOrganisationModel) + " "
                + JSON.stringify(vm.producerOrganisationModel) + " "
                + JSON.stringify(vm.ipOwnerOrganisationModel) + " "
                + JSON.stringify(vm.editorOrganisationModel) + " "
                + JSON.stringify(vm.preservationOrganisationModel));
    }

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
