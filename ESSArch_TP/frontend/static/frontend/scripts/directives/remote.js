angular.module('myApp').directive('remote', function ($timeout, $parse) {
    var URL_REGEXP = /^[a-z][a-z\d.+-]*:\/*(?:[^:@]+(?::[^@]+)?@)?(?:[^\s:/?#]+|\[[a-f\d:]+])(?::\d+)?(?:\/[^?#]*)?(?:\?[^#]*)?(?:#.*)?,[^,]+,[^,]+$/;

    return {
        require: '?ngModel',
        link: function(scope, elm, attrs, ctrl) {
            // only apply the validator if ngModel is present and AngularJS has added the url validator
            if (ctrl && ctrl.$validators.url) {
                // this will overwrite the default AngularJS url validator
                ctrl.$validators.url = function(modelValue) {
                    return ctrl.$isEmpty(modelValue) || URL_REGEXP.test(modelValue);
                };
            }
        }
    };
});
