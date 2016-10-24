angular.module('myApp').controller('LanguageCtrl', function($scope, $rootScope, $cookies, $cookieStore, $translate) {
    $scope.changeLanguage = function(lang) {
        $translate.use(lang);
    }
    $scope.getCurrentLanguage = function() {
        var lang = $cookieStore.get('NG_TRANSLATE_LANG_KEY');
        $scope.currentLanguage = lang;
        return lang;
    }
    $scope.getCurrentLanguage();

    $scope.loadLanguages = function() {
        $scope.availableLanguages = $translate.getAvailableLanguageKeys();
    }
    $scope.loadLanguages();
});
