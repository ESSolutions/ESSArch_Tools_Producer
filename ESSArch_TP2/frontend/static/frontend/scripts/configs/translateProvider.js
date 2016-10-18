angular.module('myApp').config(['$translateProvider', function ($translateProvider) {
    $translateProvider.useStaticFilesLoader({
        prefix: 'static/lang/',
        suffix: '.json'
    });
    $translateProvider.useCookieStorage();
    $translateProvider.useSanitizeValueStrategy("escape");
    $translateProvider.registerAvailableLanguageKeys(['English', 'Svenska', 'Slovenski'], {
        'en*': 'English',
        'sv*': 'Svenska',
        'sl*': 'Slovenski',
    })
    .fallbackLanguage('English')
    .determinePreferredLanguage().preferredLanguage();
}]);
