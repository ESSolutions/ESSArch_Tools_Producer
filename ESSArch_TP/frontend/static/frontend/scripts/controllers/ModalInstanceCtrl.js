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

angular.module('myApp').controller('ModalInstanceCtrl', function (IP, $scope, $uibModalInstance, $http, appConfig, djangoAuth, $translate, Notifications) {
    var $ctrl = this;
    $ctrl.preparing = false;
    $ctrl.error_messages_old = [];
    $ctrl.error_messages_pw1 = [];
    $ctrl.error_messages_pw2 = [];
    $ctrl.dir_name = "";
    $ctrl.email = {
        subject: "",
        body: ""
    };
    $ctrl.tracebackCopied = false;
    $ctrl.copied = function() {
        $ctrl.tracebackCopied = true;
    }
    $ctrl.idCopied = false;
    $ctrl.idCopyDone = function() {
        $ctrl.idCopied = true;
    }
    $ctrl.save = function () {
        $ctrl.data = {
            name: $ctrl.profileName
        };
        $uibModalInstance.close($ctrl.data);
    };
    $ctrl.saveDir = function () {
        $ctrl.data = {
            dir_name: $ctrl.dir_name
        };
        $uibModalInstance.close($ctrl.data);
    };
    $ctrl.prepare = function () {
        $ctrl.data = {
            label: $ctrl.label,
            objectIdentifierValue: $ctrl.objectIdentifierValue
        }
        $ctrl.preparing = true;
        return IP.prepare({
                label: $ctrl.data.label,
                object_identifier_value: $ctrl.data.objectIdentifierValue
        }).$promise.then(function (resource){
            $ctrl.preparing = false;
            return $uibModalInstance.close($ctrl.data);
        }).catch(function(response) {
            if (response.status == 409) {
                var msg = $translate.instant("IP_EXISTS", {'ip': $ctrl.data.objectIdentifierValue});
                Notifications.add(msg, "error", 5000);
            } else if (response.status != 500) {
                Notifications.add(response.data.detail, "error", 5000);
            }
            $ctrl.preparing = false;
        });
    };
    $ctrl.prepareForUpload = function() {
        $ctrl.data = {
            ip: $scope.ip
        }
        $ctrl.preparing = true;
        IP.prepareForUpload({ id: ip.id }).$promise.then(function(resource) {
            $ctrl.preparing = false;
            $uibModalInstance.close($ctrl.data);
        }).catch(function(response) {
            Notifications.add($translate.instant(response.data.detail), 'error');
            $ctrl.preparing = false;
        })
    }
    $ctrl.submitSip = function() {
        $ctrl.data = {
            ip: $scope.ip
        }
        $uibModalInstance.close($ctrl.data);
    }
    $ctrl.lock = function () {
        $ctrl.data = {
            status: "locked"
        }
        $uibModalInstance.close($ctrl.data);
    };
    $ctrl.lockSa = function() {
        $ctrl.data = {
            status: "locked"
        }
        $uibModalInstance.close($ctrl.data);
    };
    $ctrl.changePassword = function () {
        djangoAuth.changePassword($ctrl.pw1, $ctrl.pw2, $ctrl.oldPw).then(function(response) {
            $uibModalInstance.close($ctrl.data);
        }, function(error) {
            $ctrl.error_messages_old = error.old_password || [];
            $ctrl.error_messages_pw1 = error.new_password1 || [];
            $ctrl.error_messages_pw2 = error.new_password2 || [];
        });
    };
    $ctrl.cancel = function () {
        $uibModalInstance.dismiss('cancel');
    };
})
.controller('DataModalInstanceCtrl', function (IP, $scope, $uibModalInstance, $http, appConfig, djangoAuth, $translate, Notifications, data) {
    var $ctrl = this;
    if(data.vm) {
        var vm = data.vm;
    }
    $ctrl.email = {
        subject: "",
        body: ""
    };
    $scope.prepareAlert = null;
    $ctrl.data = data;

    // Close prepare alert
    $scope.closePrepareAlert = function() {
        $scope.prepareAlert = null;
    }

    // Prepare IP for upload
    $ctrl.prepareForUpload = function(ip) {
        $ctrl.preparing = true;
        IP.prepareForUpload({ id: ip.id }).$promise.then(function(resource) {
            $ctrl.preparing = false;
            $uibModalInstance.close();
        }).catch(function(response) {
            $scope.prepareAlert = { msg: response.data.detail };
            $ctrl.preparing = false;
        })
    }

    // Set IP as uploaded
    $ctrl.setUploaded = function (ip) {
        $ctrl.settingUploaded = true;
        IP.setUploaded({
            id: ip.id
        }).$promise.then(function (response) {
            $ctrl.settingUploaded = false;
            $uibModalInstance.close();
        }).catch(function (response) {
            $ctrl.settingUploaded = false;
            if(response.status) {
                Notifications.add('IP could not be found', 'error');
            } else {
                Notifications.add(response.data.detail, 'error');
            }
        });
    }

    // Create SIP from IP
    $ctrl.createSip = function(ip) {
        $ctrl.creating = true;
        IP.create({
            id: ip.id,
            validators: vm.validatorModel,
            file_conversion: vm.fileConversionModel.file_conversion,
        }).$promise.then(function (response) {
            $ctrl.creating = false;
            $uibModalInstance.close();
        }).catch(function (response) {
            if(response.status) {
                Notifications.add('IP could not be found', 'error');
            } else {
                Notifications.add(response.data.detail, 'error');
            }
        });
    }

    // Submit SIP
    $ctrl.submit = function (ip, email) {
        if(!email) {
            var sendData = {validators: vm.validatorModel}
        } else {
            var sendData = {validators: vm.validatorModel, subject: email.subject, body: email.body}
        }
        $ctrl.submitting = true;
        IP.submit(
            angular.extend({ id: ip.id }, sendData)
        ).$promise.then(function(response) {
            $ctrl.submitting = false;
            $uibModalInstance.close();
        }).catch(function(response) {
            $ctrl.submitting = false;
            if(response.status) {
                Notifications.add('IP could not be found', 'error');
            } else {
                Notifications.add(response.data.detail, 'error');
            }
        });
    };

    // Remove IP
    $ctrl.remove = function (ipObject) {
        $ctrl.removing = true;
        IP.delete({
			id: ipObject.id
		}).$promise.then(function() {
            $ctrl.removing = false;
            $uibModalInstance.close($ctrl.data);
        }).catch(function(response) {
            if(response.status) {
                Notifications.add('IP could not be found', 'error');
            } else {
                Notifications.add(response.data.detail, 'error');
            }
            $ctrl.removing = false;
        });
    };

    $ctrl.cancel = function () {
        $uibModalInstance.dismiss('cancel');
    };
})
.controller('OverwriteModalInstanceCtrl', function ($uibModalInstance, djangoAuth, data, SA, Profile, Notifications) {
    var $ctrl = this;
    if(data.file) {
        $ctrl.file = data.file;
    }
    if(data.type) {
        $ctrl.type = data.type;
    }
    if(data.profile) {
        $ctrl.profile = data.profile;
    }
    $ctrl.overwriteProfile = function() {
        return Profile.update($ctrl.profile).$promise.then(function(resource) {
            Notifications.add("Profile: \"" + resource.name + "\" has been imported. <br/>ID: " + resource.id , "success", 5000, {isHtml: true});
            $ctrl.data = {
                status: "overwritten"
            }
            $uibModalInstance.close($ctrl.data);
            return resource;
        }).catch(function(repsonse) {
            Notifications.add(response.detail, "error");
        })
    }
    $ctrl.overwriteSa = function() {
        $ctrl.profile.published = false;
        return SA.update($ctrl.profile).$promise.then(function(resource) {
            Notifications.add("Submission agreement: \"" + resource.name + "\" has been imported. <br/>ID: " + resource.id , "success", 5000, {isHtml: true});
            $ctrl.data = {
                status: "overwritten"
            }
            $uibModalInstance.close($ctrl.data);
            return resource;
        }).catch(function(response) {
            Notifications.add("Submission Agreement " + $ctrl.profile.name + " is Published and can not be overwritten", "error");
        })
    }
    $ctrl.overwrite = function () {
        $ctrl.data = {
            status: "overwritten"
        }
        $uibModalInstance.close($ctrl.data);
    };
    $ctrl.cancel = function () {
        $uibModalInstance.dismiss('cancel');
    };
});
