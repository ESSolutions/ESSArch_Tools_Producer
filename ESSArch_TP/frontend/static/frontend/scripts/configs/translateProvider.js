angular.module('myApp').config(['$translateProvider', function ($translateProvider) {
    $translateProvider.useStaticFilesLoader({
        prefix: 'static/lang/',
        suffix: '.json'
    });
    $translateProvider.useCookieStorage();
    $translateProvider.useSanitizeValueStrategy("escape");
    $translateProvider.registerAvailableLanguageKeys(['en', 'sv', 'sl'], {
        'en*': 'en',
        'sv*': 'sv',
        'sl*': 'sl',
    })
    .fallbackLanguage('en')
    .determinePreferredLanguage().preferredLanguage();
}]);
