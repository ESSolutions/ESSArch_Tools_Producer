angular.module('myApp').config(['$translateProvider', function ($translateProvider) {
    $translateProvider.translations('English', {
        'TITLE': 'Hello',
        'FOO': 'This is a paragraph'
    });

    $translateProvider.translations('Svenska', {
        'TITLE': 'Hallå',
        'FOO': 'Detta är en paragraf'
    });
    $translateProvider.useCookieStorage();
    $translateProvider.preferredLanguage('English');
    $translateProvider.registerAvailableLanguageKeys(['English', 'Swedish']);
}]);
