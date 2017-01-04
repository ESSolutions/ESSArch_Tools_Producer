var gulp = require('gulp')
var sass = require('gulp-sass');
var ngConstant = require('gulp-ng-constant');
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
        'styles/modules/create_sip_ip_approval.scss',
        'styles/modules/create_sip_prepare_ip.scss',
        'styles/modules/submit_sip_prepare_sip.scss',
        'styles/modules/index.scss',
        'styles/modules/login.scss',
        'styles/modules/my_page.scss',
        'styles/modules/submit_sip.scss'
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

var compileSass = function() {
 return gulp.src('styles/styles.scss')
    .pipe(sass().on('error', sass.logError))
    .pipe(gulp.dest('styles'));
};
var copyIcons = function() {
    return gulp.src('scripts/bower_components/font-awesome/fonts/**.*') 
        .pipe(gulp.dest('fonts')); 
};
var copyImages = function() {
    return gulp.src('scripts/bower_components/angular-tree-control/images/**.*') 
        .pipe(gulp.dest('images')); 
};

var configConstants = function() {
    var myConfig = require('./scripts/configs/config.json');
    if(isProduction) {
        var envConfig = myConfig["production"];
    } else {
        var envConfig = myConfig["development"];
    }
    return ngConstant({
        name: 'myApp.config',
        constants: envConfig,
        stream: true
    })
    .pipe(rename('myApp.config.js'))
    .pipe(gulp.dest('./scripts/configs'));
};

gulp.task('default', function() {
    configConstants(),
    buildScripts(),
    buildVendors(),
    compileSass(),
    copyIcons(),
    copyImages()
});

gulp.task('icons', copyIcons);
gulp.task('scripts', buildScripts);
gulp.task('vendors', buildVendors);
gulp.task('sass', compileSass);
gulp.task('config', configConstants);

gulp.task('watch', function(){
    gulp.watch(jsFiles, ['scripts']);
    gulp.watch(jsVendorFiles, ['vendors']);
    gulp.watch(cssFiles, ['sass']);
})
