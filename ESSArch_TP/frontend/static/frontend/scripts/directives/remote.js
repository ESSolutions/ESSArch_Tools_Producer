angular.module('essarch.directives').directive('remote', function ($timeout, $parse) {
    var REMOTE_URL_REGEXP = /^[a-z][a-z\d.+-]*:\/*(?:[^:@]+(?::[^@]+)?@)?(?:[^\s:/?#,]+|\[[a-f\d:]+])(?::\d+)?(?:\/[^?#]*)?(?:\?[^#]*)?(?:#.*)?,[^,]+,[^,]+$/;

    return {
        require: '?ngModel',
        link: function(scope, elm, attrs, ctrl) {
            // only apply the validator if ngModel is present
            if (ctrl) {
                // this will overwrite the default AngularJS url validator
                ctrl.$validators.remoteUrl = function(modelValue) {
                    return ctrl.$isEmpty(modelValue) || REMOTE_URL_REGEXP.test(modelValue);
                };
            }
        }
    };
});
