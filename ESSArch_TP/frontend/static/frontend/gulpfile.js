var gulp = require('gulp')
var sourcemaps = require('gulp-sourcemaps');
var concat = require('gulp-concat');
var gulpif = require('gulp-if');
var ngAnnotate = require('gulp-ng-annotate');
var plumber = require('gulp-plumber');
var rename = require('gulp-rename');
var uglify = require('gulp-uglify');
var gutil = require('gulp-util');

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
        'scripts/bower_components/bootstrap/dist/js/bootstrap.min.js',
        'scripts/bower_components/ng-flow/dist/ng-flow-standalone.min.js',
        'node_modules/moment/min/moment-with-locales.min.js',
        'node_modules/angular-date-time-input/src/dateTimeInput.js',
        'node_modules/angular-bootstrap-datetimepicker/src/js/datetimepicker.js',
        'node_modules/angular-bootstrap-datetimepicker/src/js/datetimepicker.templates.js',
    ],
    jsFiles = [
        'scripts/myApp.js', 'scripts/controllers/*.js', 'scripts/services/*.js',
        'scripts/directives/*.js', 'scripts/configs/*.js'
    ],
    jsDest = 'scripts';

var buildScripts = function() {
    return gulp.src(jsFiles)
        .pipe(plumber(function(error) {
          // output an error message

          gutil.log(gutil.colors.red('error (' + error.plugin + '): ' + error.message));
          // emit the end event, to properly end the task
          this.emit('end');
        }))
        .pipe(sourcemaps.init())
        .pipe(ngAnnotate())
        .pipe(concat('scripts.min.js'))
        .pipe(uglify())
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest(jsDest));
};

var buildVendors = function() {
    return gulp.src(vendorFiles)
        .pipe(plumber(function(error) {
          // output an error message

          gutil.log(gutil.colors.red('error (' + error.plugin + '): ' + error.message));
          // emit the end event, to properly end the task
          this.emit('end');
        }))
        .pipe(sourcemaps.init())
        .pipe(ngAnnotate())
        .pipe(concat('vendors.min.js'))
        .pipe(uglify())
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest(jsDest));
};

gulp.task('default', function() {
    buildScripts(),
    buildVendors()
});


gulp.task('scripts', buildScripts);
gulp.task('vendors', buildVendors);

gulp.task('watch', function(){
    gulp.watch(jsFiles, ['scripts']);
    gulp.watch(vendorFiles, ['vendors']);
})
