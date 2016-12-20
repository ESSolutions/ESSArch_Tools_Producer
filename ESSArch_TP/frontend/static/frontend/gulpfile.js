var gulp = require('gulp')
var sourcemaps = require('gulp-sourcemaps');
var concat = require('gulp-concat');
var concatCss = require('gulp-concat-css');
var gulpif = require('gulp-if');
var ngAnnotate = require('gulp-ng-annotate');
var plumber = require('gulp-plumber');
var rename = require('gulp-rename');
var uglify = require('gulp-uglify');
var cleanCSS = require('gulp-clean-css');
var gutil = require('gulp-util');
var argv = require('yargs').argv;
var isProduction = (argv.production === undefined) ? false : true;

var jsVendorFiles = [
        'scripts/bower_components/api-check/dist/api-check.js',
        'scripts/bower_components/jquery/dist/jquery.js',
        'scripts/bower_components/jquery-ui/jquery-ui.js',
        'scripts/bower_components/angular/angular.js',
        'scripts/bower_components/angular-animate/angular-animate.js',
        'scripts/bower_components/angular-messages/angular-messages.js',
        'scripts/bower_components/angular-route/angular-route.js',
        'scripts/bower_components/angular-bootstrap/ui-bootstrap-tpls.js',
        'scripts/bower_components/angular-tree-control/angular-tree-control.js',
        'scripts/bower_components/angular-formly/dist/formly.js',
        'scripts/bower_components/angular-formly-templates-bootstrap/dist/angular-formly-templates-bootstrap.js',
        'scripts/bower_components/angular-smart-table/dist/smart-table.js',
        'scripts/bower_components/angular-bootstrap-grid-tree/src/tree-grid-directive.js',
        'scripts/bower_components/angular-ui-router/release/angular-ui-router.js',
        'scripts/bower_components/angular-cookies/angular-cookies.js ',
        'scripts/bower_components/angular-permission/dist/angular-permission.js',
        'scripts/bower_components/angular-translate/angular-translate.js',
        'scripts/bower_components/angular-translate-storage-cookie/angular-translate-storage-cookie.js',
        'scripts/bower_components/angular-translate-loader-static-files/angular-translate-loader-static-files.js',
        'scripts/bower_components/angular-sanitize/angular-sanitize.js',
        'scripts/bower_components/angular-bootstrap-contextmenu/contextMenu.js',
        'scripts/bower_components/angular-ui-select/dist/select.js',
        'scripts/bower_components/bootstrap/dist/js/bootstrap.js',
        'scripts/bower_components/ng-flow/dist/ng-flow-standalone.js',
        'node_modules/moment/min/moment-with-locales.js',
        'node_modules/angular-date-time-input/src/dateTimeInput.js',
        'node_modules/angular-bootstrap-datetimepicker/src/js/datetimepicker.js',
        'node_modules/angular-bootstrap-datetimepicker/src/js/datetimepicker.templates.js',
    ],
    jsFiles = [
        'scripts/myApp.js', 'scripts/controllers/*.js', 'scripts/services/*.js',
        'scripts/directives/*.js', 'scripts/configs/*.js'
    ],
    jsDest = 'scripts',
    cssFiles = [
        'node_modules/angular-bootstrap-datetimepicker/src/css/datetimepicker.css',
        'scripts/bower_components/angular-bootstrap-grid-tree/src/treeGrid.css',
        'scripts/bower_components/angular-tree-control/css/tree-control-attribute.css',
        'scripts/bower_components/angular-ui-select/dist/select.css',
        'scripts/bower_components/font-awesome/css/font-awesome.min.css',
        'scripts/bower_components/select2/dist/css/select2.min.css',
        'styles/index.css',
    ],
    cssDest = 'styles';

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
        .pipe(gulpif(isProduction, uglify()))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest(jsDest));
};

var buildVendors = function() {
    return gulp.src(jsVendorFiles)
        .pipe(plumber(function(error) {
          // output an error message

          gutil.log(gutil.colors.red('error (' + error.plugin + '): ' + error.message));
          // emit the end event, to properly end the task
          this.emit('end');
        }))
        .pipe(sourcemaps.init())
        .pipe(ngAnnotate())
        .pipe(concat('vendors.min.js'))
        .pipe(gulpif(isProduction, uglify()))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest(jsDest));
};

var buildCSS = function() {
    return gulp.src(cssFiles)
        .pipe(plumber(function(error) {
          // output an error message

          gutil.log(gutil.colors.red('error (' + error.plugin + '): ' + error.message));
          // emit the end event, to properly end the task
          this.emit('end');
        }))
        .pipe(sourcemaps.init())
        .pipe(concatCss('styles.min.css'))
        .pipe(gulpif(isProduction, cleanCSS()))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest(cssDest));
};

gulp.task('default', function() {
    buildScripts(),
    buildVendors(),
    buildCSS()
});


gulp.task('scripts', buildScripts);
gulp.task('vendors', buildVendors);
gulp.task('css', buildCSS);

gulp.task('watch', function(){
    gulp.watch(jsFiles, ['scripts']);
    gulp.watch(jsVendorFiles, ['vendors']);
    gulp.watch(cssFiles, ['css']);
})
