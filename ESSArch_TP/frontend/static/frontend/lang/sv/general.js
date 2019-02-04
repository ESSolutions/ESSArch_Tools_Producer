angular.module('essarch.language').config(function($translateProvider) {
  $translateProvider.translations('sv', {
    AGENTS: 'Agenter',
    COLLECTCONTENT: 'Samla innehåll',
    COMPLETED_UPLOAD_DESC: 'Vill du slutföra uppladdning för IP(n)?',
    CONVERTFILES: 'Konvertera filer',
    CREATESIP: 'Skapa SIP',
    CREATE_SIP_DESC: 'Vill du skapa SIP(ar) av IP(n)?',
    DIR_EXISTS_IN_IP: 'Det existerar redan en mapp med samma namn!',
    DIR_EXISTS_IN_IP_DESC:
      'Det existerar redan en mapp med detta namn i IPt. Vill du skriva över den nuvarande mappen?',
    ENABLEDDESC: 'Profilen är aktiverad om den är checkad',
    ENTERSAPROFILENAME: 'Välj nytt SA-profilnamn',
    FILECONVERSION: 'Filkonvertering',
    FILE_EXISTS_IN_IP: 'Det existerar redan en fil med samma namn!',
    FILE_EXISTS_IN_IP_DESC:
      'Det existerar redan en fil med detta namn i IPt. Vill du skriva över den nuvarande filen?',
    INCLUDEDPROFILES: 'Inkluderade profiler',
    IPAPPROVAL: 'Skapa SIP',
    IP_EXISTS: 'IP med object identifer value "{{ip}}" finns redan',
    LOCK: 'Lås',
    LOCK_ERROR: 'kunde inte låsas',
    NO_SUBMISSION_AGREEMENT_AVAILABLE: 'Inga leveransöverenskommelser tillgängliga',
    PACKAGEDEPENDENCIES: 'Paketberoenden',
    PACKAGEINFORMATION: 'Paketinformation',
    PREPAREIP: 'Förbered IP',
    PREPAREIPDESC: 'Gör ett nytt IP',
    PREPARESIP: 'Skicka SIP',
    PREPARE_IP: 'Förbered IP',
    PREPARE_IP_DESC: 'Vill du förbereda IP(n) för uppladdning?',
    PREPARE_NEW_IP: 'Förbered nytt IP',
    SAVESAPROFILE: 'Spara SA-profil',
    SUBMIT_SIP_DESC: 'Vill du skicka SIP(ar)?',
    UNLOCKPROFILE: 'Lås upp profil',
    UNLOCKPROFILEINFO:
      'Om du låser upp denna profil kommer IPt att flyttas till "Förbered IP"-vyn. Fortsätt genom att klicka OK.',
  });
});
