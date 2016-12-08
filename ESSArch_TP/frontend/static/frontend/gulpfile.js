var gulp = require('gulp')
var sourcemaps = require('gulp-sourcemaps');
var concat = require('gulp-concat');
var ngAnnotate = require('gulp-ng-annotate');
var rename = require('gulp-rename');
var uglify = require('gulp-uglify');

var vendorFiles = [
        'scripts/bower_components/api-check/dist/api-check.js',
        'scripts/bower_components/jquery/dist/jquery.min.js',
        'scripts/bower_components/jquery-ui/jquery-ui.min.js',
        'scripts/bower_components/angular/angular.min.js',
        'scripts/bower_components/angular-route/angular-route.min.js',
        'scripts/vendor/ui-bootstrap-tpls-1.3.3.min.js',
        'scripts/bower_components/angular-tree-control/angular-tree-control.js',
        'scripts/bower_components/angular-formly/dist/formly.js',
        'scripts/bower_components/angular-formly-templates-bootstrap/dist/angular-formly-templates-bootstrap.js',
        'scripts/bower_components/angular-smart-table/dist/smart-table.min.js',
        'scripts/bower_components/angular-bootstrap-grid-tree/src/tree-grid-directive.js',
        'scripts/bower_components/angular-ui-router/release/angular-ui-router.min.js',
        'scripts/bower_components/angular-cookies/angular-cookies.js ',
        'scripts/bower_components/angular-permission/dist/angular-permission.js',
        'scripts/bower_components/angular-translate/angular-translate.min.js',
        'scripts/bower_components/angular-translate-storage-cookie/angular-translate-storage-cookie.min.js',
        'scripts/bower_components/angular-translate-loader-static-files/angular-translate-loader-static-files.min.js',
        'scripts/bower_components/angular-sanitize/angular-sanitize.min.js',
        'scripts/bower_components/angular-bootstrap-contextmenu/contextMenu.js',
        'scripts/bower_components/angular-ui-select/dist/select.min.js',
        'scripts/bower_components/ng-flow/dist/ng-flow-standalone.min.js',
        'node_modules/moment/min/moment-with-locales.min.js',
        'scripts/bower_components/angular-moment-picker/dist/angular-moment-picker.min.js',
        'scripts/bower_components/angular-deckgrid/angular-deckgrid.js'
    ],
    jsFiles = [
        'scripts/myApp.js', 'scripts/controllers/*.js', 'scripts/services/*.js',
        'scripts/directives/*.js', 'scripts/configs/*.js'
    ],
    jsDest = 'scripts';

gulp.task('default', function() {
    gulp.src(jsFiles)
        .pipe(sourcemaps.init())
        .pipe(ngAnnotate())
        .pipe(concat('scripts.js'))
        .pipe(gulp.dest(jsDest))
        .pipe(rename('scripts.min.js'))
        .pipe(uglify().on('error', function(e){
            console.log(e);
         }))
        .pipe(sourcemaps.write())
        .pipe(gulp.dest(jsDest));

    gulp.src(vendorFiles)
        .pipe(sourcemaps.init())
        .pipe(ngAnnotate())
        .pipe(concat('vendors.js'))
        .pipe(gulp.dest(jsDest))
        .pipe(rename('vendors.min.js'))
        .pipe(uglify().on('error', function(e){
            console.log(e);
         }))
        .pipe(sourcemaps.write())
        .pipe(gulp.dest(jsDest));
});

gulp.task('scripts', function() {
    return gulp.src(jsFiles)
        .pipe(sourcemaps.init())
        .pipe(ngAnnotate())
        .pipe(concat('scripts.js'))
        .pipe(gulp.dest(jsDest))
        .pipe(rename('scripts.min.js'))
        .pipe(uglify().on('error', function(e){
            console.log(e);
         }))
        .pipe(sourcemaps.write())
        .pipe(gulp.dest(jsDest));
});

gulp.task('vendors', function() {
    return gulp.src(vendorFiles)
        .pipe(sourcemaps.init())
        .pipe(ngAnnotate())
        .pipe(concat('vendors.js'))
        .pipe(gulp.dest(jsDest))
        .pipe(rename('vendors.min.js'))
        .pipe(uglify().on('error', function(e){
            console.log(e);
         }))
        .pipe(sourcemaps.write())
        .pipe(gulp.dest(jsDest));
});

gulp.task('watch', function(){
    gulp.watch(jsFiles, ['scripts']);
    gulp.watch(vendorFiles, ['scripts']);
})
