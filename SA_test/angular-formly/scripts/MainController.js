(function() {

    'use strict';

    angular
        .module('formlyApp')
        .controller('MainController', MainController);

        function MainController($scope) {

            var vm = this;

            // The model object that we reference
            // on the  element in index.html
            vm.rental = {};

            // An array of our form fields with configuration
            // and options set. We make reference to this in
            // the 'fields' attribute on the  element

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
            $scope.dataForTheTree =
            [
                {"attributes": [{"templateOptions": {"type": "text", "label": "ID"}, "type": "input", "key": "ID"}, {"templateOptions": {"type": "text", "label": "OBJID"}, "type": "input", "key": "OBJID"}, {"templateOptions": {"type": "text", "label": "LABEL"}, "type": "input", "key": "LABEL"}, {"templateOptions": {"options": [{"name": "ERMS", "value": "ERMS"}, {"name": "Personnel", "value": "Personnel"}, {"name": "Medical record", "value": "Medical record"}, {"name": "Economics", "value": "Economics"}, {"name": "Databases", "value": "Databases"}, {"name": "Webpages", "value": "Webpages"}, {"name": "GIS", "value": "GIS"}, {"name": "No specification", "value": "No specification"}, {"name": "AIC", "value": "AIC"}, {"name": "Publication", "value": "Publication"}, {"name": "Archival information", "value": "Archival information"}, {"name": "Unstructured", "value": "Unstructured"}, {"name": "Single records", "value": "Single records"}], "label": "TYPE"}, "type": "select", "key": "TYPE"}, {"templateOptions": {"type": "text", "label": "PROFILE"}, "type": "input", "key": "PROFILE"}], "name": "mets", "children": [{"attributes": [{"templateOptions": {"type": "text", "label": "ID"}, "type": "input", "key": "ID"}, {"templateOptions": {"type": "text", "label": "ADMID"}, "type": "input", "key": "ADMID"}, {"templateOptions": {"type": "text", "label": "CREATEDATE"}, "type": "input", "key": "CREATEDATE"}, {"templateOptions": {"type": "text", "label": "LASTMODDATE"}, "type": "input", "key": "LASTMODDATE"}, {"templateOptions": {"options": [{"name": "SUPPLEMENT", "value": "SUPPLEMENT"}, {"name": "REPLACEMENT", "value": "REPLACEMENT"}, {"name": "NEW", "value": "NEW"}, {"name": "TEST", "value": "TEST"}, {"name": "VERSION", "value": "VERSION"}, {"name": "DEPOSIT", "value": "DEPOSIT"}, {"name": "AGREEMENT", "value": "AGREEMENT"}, {"name": "OTHER", "value": "OTHER"}], "label": "RECORDSTATUS"}, "type": "select", "key": "RECORDSTATUS"}], "name": "metsHdr", "children": [{"attributes": [{"templateOptions": {"type": "text", "label": "ID"}, "type": "input", "key": "ID"}, {"templateOptions": {"options": [{"name": "CREATOR", "value": "CREATOR"}, {"name": "EDITOR", "value": "EDITOR"}, {"name": "ARCHIVIST", "value": "ARCHIVIST"}, {"name": "PRESERVATION", "value": "PRESERVATION"}, {"name": "DISSEMINATOR", "value": "DISSEMINATOR"}, {"name": "CUSTODIAN", "value": "CUSTODIAN"}, {"name": "IPOWNER", "value": "IPOWNER"}, {"name": "OTHER", "value": "OTHER"}], "label": "ROLE"}, "type": "select", "key": "ROLE"}, {"templateOptions": {"options": [{"name": "SUBMITTER", "value": "SUBMITTER"}, {"name": "PRODUCER", "value": "PRODUCER"}], "label": "OTHERROLE"}, "type": "select", "key": "OTHERROLE"}, {"templateOptions": {"options": [{"name": "INDIVIDUAL", "value": "INDIVIDUAL"}, {"name": "ORGANIZATION", "value": "ORGANIZATION"}, {"name": "OTHER", "value": "OTHER"}], "label": "TYPE"}, "type": "select", "key": "TYPE"}, {"templateOptions": {"options": [{"name": "SOFTWARE", "value": "SOFTWARE"}], "label": "OTHERTYPE"}, "type": "select", "key": "OTHERTYPE"}], "name": "agent", "children": [{"attributes": [], "name": "name", "children": []}, {"attributes": [], "name": "note", "children": []}]}, {"attributes": [], "name": "altRecordID", "children": []}, {"attributes": [], "name": "metsDocumentID", "children": []}]}, {"attributes": [{"templateOptions": {"type": "text", "label": "ID"}, "type": "input", "key": "ID"}, {"templateOptions": {"type": "text", "label": "GROUPID"}, "type": "input", "key": "GROUPID"}, {"templateOptions": {"type": "text", "label": "ADMID"}, "type": "input", "key": "ADMID"}, {"templateOptions": {"type": "text", "label": "CREATED"}, "type": "input", "key": "CREATED"}, {"templateOptions": {"type": "text", "label": "STATUS"}, "type": "input", "key": "STATUS"}], "name": "dmdSec", "children": []}, {"attributes": [{"templateOptions": {"type": "text", "label": "ID"}, "type": "input", "key": "ID"}], "name": "amdSec", "children": [{"attributes": [], "name": "techMD", "children": []}, {"attributes": [], "name": "rightsMD", "children": []}, {"attributes": [], "name": "sourceMD", "children": []}, {"attributes": [], "name": "digiprovMD", "children": []}]}, {"attributes": [{"templateOptions": {"type": "text", "label": "ID"}, "type": "input", "key": "ID"}], "name": "fileSec", "children": [{"attributes": [{"templateOptions": {"type": "text", "label": "ID"}, "type": "input", "key": "ID"}, {"templateOptions": {"type": "text", "label": "VERSDATE"}, "type": "input", "key": "VERSDATE"}, {"templateOptions": {"type": "text", "label": "ADMID"}, "type": "input", "key": "ADMID"}, {"templateOptions": {"type": "text", "label": "USE"}, "type": "input", "key": "USE"}], "name": "fileGrp", "children": [{"attributes": [], "name": "fileGrp", "children": []}, {"attributes": [{"templateOptions": {"type": "text", "label": "ID"}, "type": "input", "key": "ID"}, {"templateOptions": {"type": "text", "label": "SEQ"}, "type": "input", "key": "SEQ"}, {"templateOptions": {"type": "text", "label": "MIMETYPE"}, "type": "input", "key": "MIMETYPE"}, {"templateOptions": {"type": "text", "label": "SIZE"}, "type": "input", "key": "SIZE"}, {"templateOptions": {"type": "text", "label": "CREATED"}, "type": "input", "key": "CREATED"}, {"templateOptions": {"type": "text", "label": "CHECKSUM"}, "type": "input", "key": "CHECKSUM"}, {"templateOptions": {"options": [{"name": "MD5", "value": "MD5"}, {"name": "SHA-1", "value": "SHA-1"}, {"name": "SHA-256", "value": "SHA-256"}, {"name": "SHA-384", "value": "SHA-384"}, {"name": "SHA-512", "value": "SHA-512"}], "label": "CHECKSUMTYPE"}, "type": "select", "key": "CHECKSUMTYPE"}, {"templateOptions": {"type": "text", "label": "OWNERID"}, "type": "input", "key": "OWNERID"}, {"templateOptions": {"type": "text", "label": "ADMID"}, "type": "input", "key": "ADMID"}, {"templateOptions": {"type": "text", "label": "DMDID"}, "type": "input", "key": "DMDID"}, {"templateOptions": {"type": "text", "label": "GROUPID"}, "type": "input", "key": "GROUPID"}, {"templateOptions": {"type": "text", "label": "USE"}, "type": "input", "key": "USE"}, {"templateOptions": {"type": "text", "label": "BEGIN"}, "type": "input", "key": "BEGIN"}, {"templateOptions": {"type": "text", "label": "END"}, "type": "input", "key": "END"}, {"templateOptions": {"options": [{"name": "BYTE", "value": "BYTE"}], "label": "BETYPE"}, "type": "select", "key": "BETYPE"}], "name": "file", "children": [{"attributes": [{"templateOptions": {"type": "text", "label": "ID"}, "type": "input", "key": "ID"}, {"templateOptions": {"options": [{"name": "URN", "value": "URN"}, {"name": "URL", "value": "URL"}, {"name": "HANDLE", "value": "HANDLE"}, {"name": "OTHER", "value": "OTHER"}], "label": "LOCTYPE"}, "type": "select", "key": "LOCTYPE"}, {"templateOptions": {"type": "text", "label": "OTHERLOCTYPE"}, "type": "input", "key": "OTHERLOCTYPE"}, {"templateOptions": {"type": "text", "label": "USE"}, "type": "input", "key": "USE"}], "name": "FLocat", "children": []}, {"attributes": [{"templateOptions": {"type": "text", "label": "ID"}, "type": "input", "key": "ID"}, {"templateOptions": {"type": "text", "label": "USE"}, "type": "input", "key": "USE"}], "name": "FContent", "children": [{"attributes": [], "name": "binData", "children": []}, {"attributes": [], "name": "xmlData", "children": []}]}, {"attributes": [], "name": "stream", "children": []}, {"attributes": [], "name": "transformFile", "children": []}, {"attributes": [], "name": "file", "children": []}]}]}]}, {"attributes": [{"templateOptions": {"type": "text", "label": "ID"}, "type": "input", "key": "ID"}, {"templateOptions": {"type": "text", "label": "TYPE"}, "type": "input", "key": "TYPE"}, {"templateOptions": {"type": "text", "label": "LABEL"}, "type": "input", "key": "LABEL"}], "name": "structMap", "children": [{"attributes": [{"templateOptions": {"type": "text", "label": "ID"}, "type": "input", "key": "ID"}, {"templateOptions": {"type": "text", "label": "ORDER"}, "type": "input", "key": "ORDER"}, {"templateOptions": {"type": "text", "label": "ORDERLABEL"}, "type": "input", "key": "ORDERLABEL"}, {"templateOptions": {"type": "text", "label": "LABEL"}, "type": "input", "key": "LABEL"}, {"templateOptions": {"type": "text", "label": "DMDID"}, "type": "input", "key": "DMDID"}, {"templateOptions": {"type": "text", "label": "ADMID"}, "type": "input", "key": "ADMID"}, {"templateOptions": {"type": "text", "label": "TYPE"}, "type": "input", "key": "TYPE"}, {"templateOptions": {"type": "text", "label": "CONTENTIDS"}, "type": "input", "key": "CONTENTIDS"}], "name": "div", "children": [{"attributes": [{"templateOptions": {"type": "text", "label": "ID"}, "type": "input", "key": "ID"}, {"templateOptions": {"options": [{"name": "URN", "value": "URN"}, {"name": "URL", "value": "URL"}, {"name": "HANDLE", "value": "HANDLE"}, {"name": "OTHER", "value": "OTHER"}], "label": "LOCTYPE"}, "type": "select", "key": "LOCTYPE"}, {"templateOptions": {"type": "text", "label": "OTHERLOCTYPE"}, "type": "input", "key": "OTHERLOCTYPE"}, {"templateOptions": {"type": "text", "label": "CONTENTIDS"}, "type": "input", "key": "CONTENTIDS"}], "name": "mptr", "children": []}, {"attributes": [{"templateOptions": {"type": "text", "label": "ID"}, "type": "input", "key": "ID"}, {"templateOptions": {"type": "text", "label": "FILEID"}, "type": "input", "key": "FILEID"}, {"templateOptions": {"type": "text", "label": "CONTENTIDS"}, "type": "input", "key": "CONTENTIDS"}], "name": "fptr", "children": [{"attributes": [{"templateOptions": {"type": "text", "label": "ID"}, "type": "input", "key": "ID"}, {"templateOptions": {"type": "text", "label": "ORDER"}, "type": "input", "key": "ORDER"}, {"templateOptions": {"type": "text", "label": "ORDERLABEL"}, "type": "input", "key": "ORDERLABEL"}, {"templateOptions": {"type": "text", "label": "LABEL"}, "type": "input", "key": "LABEL"}], "name": "par", "children": [{"attributes": [{"templateOptions": {"type": "text", "label": "ID"}, "type": "input", "key": "ID"}, {"templateOptions": {"type": "text", "label": "FILEID"}, "type": "input", "key": "FILEID"}, {"templateOptions": {"options": [{"name": "RECT", "value": "RECT"}, {"name": "CIRCLE", "value": "CIRCLE"}, {"name": "POLY", "value": "POLY"}], "label": "SHAPE"}, "type": "select", "key": "SHAPE"}, {"templateOptions": {"type": "text", "label": "COORDS"}, "type": "input", "key": "COORDS"}, {"templateOptions": {"type": "text", "label": "BEGIN"}, "type": "input", "key": "BEGIN"}, {"templateOptions": {"type": "text", "label": "END"}, "type": "input", "key": "END"}, {"templateOptions": {"options": [{"name": "BYTE", "value": "BYTE"}, {"name": "IDREF", "value": "IDREF"}, {"name": "SMIL", "value": "SMIL"}, {"name": "MIDI", "value": "MIDI"}, {"name": "SMPTE-25", "value": "SMPTE-25"}, {"name": "SMPTE-24", "value": "SMPTE-24"}, {"name": "SMPTE-DF30", "value": "SMPTE-DF30"}, {"name": "SMPTE-NDF30", "value": "SMPTE-NDF30"}, {"name": "SMPTE-DF29.97", "value": "SMPTE-DF29.97"}, {"name": "SMPTE-NDF29.97", "value": "SMPTE-NDF29.97"}, {"name": "TIME", "value": "TIME"}, {"name": "TCF", "value": "TCF"}, {"name": "XPTR", "value": "XPTR"}], "label": "BETYPE"}, "type": "select", "key": "BETYPE"}, {"templateOptions": {"type": "text", "label": "EXTENT"}, "type": "input", "key": "EXTENT"}, {"templateOptions": {"options": [{"name": "BYTE", "value": "BYTE"}, {"name": "SMIL", "value": "SMIL"}, {"name": "MIDI", "value": "MIDI"}, {"name": "SMPTE-25", "value": "SMPTE-25"}, {"name": "SMPTE-24", "value": "SMPTE-24"}, {"name": "SMPTE-DF30", "value": "SMPTE-DF30"}, {"name": "SMPTE-NDF30", "value": "SMPTE-NDF30"}, {"name": "SMPTE-DF29.97", "value": "SMPTE-DF29.97"}, {"name": "SMPTE-NDF29.97", "value": "SMPTE-NDF29.97"}, {"name": "TIME", "value": "TIME"}, {"name": "TCF", "value": "TCF"}], "label": "EXTTYPE"}, "type": "select", "key": "EXTTYPE"}, {"templateOptions": {"type": "text", "label": "ADMID"}, "type": "input", "key": "ADMID"}, {"templateOptions": {"type": "text", "label": "CONTENTIDS"}, "type": "input", "key": "CONTENTIDS"}, {"templateOptions": {"type": "text", "label": "ORDER"}, "type": "input", "key": "ORDER"}, {"templateOptions": {"type": "text", "label": "ORDERLABEL"}, "type": "input", "key": "ORDERLABEL"}, {"templateOptions": {"type": "text", "label": "LABEL"}, "type": "input", "key": "LABEL"}], "name": "area", "children": []}, {"attributes": [{"templateOptions": {"type": "text", "label": "ID"}, "type": "input", "key": "ID"}, {"templateOptions": {"type": "text", "label": "ORDER"}, "type": "input", "key": "ORDER"}, {"templateOptions": {"type": "text", "label": "ORDERLABEL"}, "type": "input", "key": "ORDERLABEL"}, {"templateOptions": {"type": "text", "label": "LABEL"}, "type": "input", "key": "LABEL"}], "name": "seq", "children": [{"attributes": [], "name": "area", "children": []}, {"attributes": [], "name": "par", "children": []}]}]}, {"attributes": [], "name": "seq", "children": []}, {"attributes": [], "name": "area", "children": []}]}, {"attributes": [], "name": "div", "children": []}]}]}, {"attributes": [{"templateOptions": {"type": "text", "label": "ID"}, "type": "input", "key": "ID"}], "name": "structLink", "children": [{"attributes": [{"templateOptions": {"type": "text", "label": "ID"}, "type": "input", "key": "ID"}], "name": "smLink", "children": []}, {"attributes": [{"templateOptions": {"type": "text", "label": "ID"}, "type": "input", "key": "ID"}, {"templateOptions": {"options": [{"name": "ordered", "value": "ordered"}, {"name": "unordered", "value": "unordered"}], "label": "ARCLINKORDER"}, "type": "select", "key": "ARCLINKORDER"}], "name": "smLinkGrp", "children": [{"attributes": [{"templateOptions": {"type": "text", "label": "ID"}, "type": "input", "key": "ID"}], "name": "smLocatorLink", "children": []}, {"attributes": [{"templateOptions": {"type": "text", "label": "ID"}, "type": "input", "key": "ID"}, {"templateOptions": {"type": "text", "label": "ARCTYPE"}, "type": "input", "key": "ARCTYPE"}, {"templateOptions": {"type": "text", "label": "ADMID"}, "type": "input", "key": "ADMID"}], "name": "smArcLink", "children": []}]}]}, {"attributes": [{"templateOptions": {"type": "text", "label": "ID"}, "type": "input", "key": "ID"}, {"templateOptions": {"type": "text", "label": "CREATED"}, "type": "input", "key": "CREATED"}, {"templateOptions": {"type": "text", "label": "LABEL"}, "type": "input", "key": "LABEL"}], "name": "behaviorSec", "children": [{"attributes": [], "name": "behaviorSec", "children": []}, {"attributes": [{"templateOptions": {"type": "text", "label": "ID"}, "type": "input", "key": "ID"}, {"templateOptions": {"type": "text", "label": "STRUCTID"}, "type": "input", "key": "STRUCTID"}, {"templateOptions": {"type": "text", "label": "BTYPE"}, "type": "input", "key": "BTYPE"}, {"templateOptions": {"type": "text", "label": "CREATED"}, "type": "input", "key": "CREATED"}, {"templateOptions": {"type": "text", "label": "LABEL"}, "type": "input", "key": "LABEL"}, {"templateOptions": {"type": "text", "label": "GROUPID"}, "type": "input", "key": "GROUPID"}, {"templateOptions": {"type": "text", "label": "ADMID"}, "type": "input", "key": "ADMID"}], "name": "behavior", "children": [{"attributes": [{"templateOptions": {"type": "text", "label": "ID"}, "type": "input", "key": "ID"}, {"templateOptions": {"type": "text", "label": "LABEL"}, "type": "input", "key": "LABEL"}, {"templateOptions": {"options": [{"name": "URN", "value": "URN"}, {"name": "URL", "value": "URL"}, {"name": "HANDLE", "value": "HANDLE"}, {"name": "OTHER", "value": "OTHER"}], "label": "LOCTYPE"}, "type": "select", "key": "LOCTYPE"}, {"templateOptions": {"type": "text", "label": "OTHERLOCTYPE"}, "type": "input", "key": "OTHERLOCTYPE"}], "name": "interfaceDef", "children": []}, {"attributes": [], "name": "mechanism", "children": []}]}]}]}
            ];

            $scope.showSelected = function(sel) {
                 $scope.selectedNode = sel;
                 console.log(sel)
                 vm.rentalFields = sel.attributes
             };

            vm.rentalFields = [
                {
                    key: 'name',
                    type: 'input',
                    templateOptions: {
                        type: 'text',
                        label: 'name',
                        placeholder: 'string',
                        required: true
                    }
                },
                {
                    key: 'note',
                    type: 'input',
                    templateOptions: {
                        type: 'text',
                        label: 'note',
                        placeholder: 'string',
                        required: true
                    }
                },
                {
                    template: '<hr/><p><b>Attributes</b></p>'
                },
                //attributes:
                {
                    key: 'ID',
                    type: 'input',
                    templateOptions: {
                        type: 'text',
                        label: 'ID',
                        placeholder: 'string',
                        required: true
                    }
                },
                {
                    key: 'ROLE',
                    type: 'input',
                    templateOptions: {
                        type: 'text',
                        label: 'ROLE',
                        placeholder: 'string',
                        required: true
                    }
                },
                {
                    key: 'OTHERROLE',
                    type: 'select',
                    templateOptions: {
                        // type: 'text',
                        label: 'OTHERROLE',
                        // placeholder: 'string',
                        // required: true
                        options: [
                            {name: 'CREATOR', value: 'CREATOR'},
                            {name: 'EDITOR', value: 'EDITOR'},
                            {name: 'ARCHIVIST', value: 'ARCHIVIST'},
                        ]
                    }
                },
                // {
                //     key: 'first_name',
                //     type: 'input',
                //     templateOptions: {
                //         type: 'text',
                //         label: 'First Name',
                //         placeholder: 'Enter your first name',
                //         required: true
                //     }
                // },
                // {
                //     key: 'last_name',
                //     type: 'input',
                //     templateOptions: {
                //         type: 'text',
                //         label: 'Last Name',
                //         placeholder: 'Enter your last name',
                //         required: true
                //     }
                // },
                // {
                //     key: 'email',
                //     type: 'input',
                //     templateOptions: {
                //         type: 'email',
                //         label: 'Email address',
                //         placeholder: 'Enter email',
                //         required: true
                //     }
                // },
                // {
                //     key: 'under25',
                //     type: 'checkbox',
                //     templateOptions: {
                //         label: 'Are you under 25?',
                //     },
                //     // Hide this field if we don't have
                //     // any valid input in the email field
                //     hideExpression: '!model.email'
                // },
                // {
                //     key: 'province',
                //     type: 'select',
                //     templateOptions: {
                //         label: 'Province/Territory',
                //         // Call our province service to get a list
                //         // of provinces and territories
                //         options: province.getProvinces()
                //     },
                //     hideExpression: '!model.email'
                // },
                // {
                //     key: 'insurance',
                //     type: 'input',
                //     templateOptions: {
                //         label: 'Insurance Policy Number',
                //         placeholder: 'Enter your insurance policy number'
                //     },
                //     hideExpression: '!model.under25 || !model.province',
                // }
            ];

        }


})();
