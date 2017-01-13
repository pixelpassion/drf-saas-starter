
////////////////////////////////
		//Setup//
////////////////////////////////

// Plugins
var gulp = require('gulp'),
    pjson = require('./package.json'),
    gutil = require('gulp-util'),
    sass = require('gulp-sass'),
    autoprefixer = require('gulp-autoprefixer'),
    cssnano = require('gulp-cssnano'),
    rename = require('gulp-rename'),
    concat = require('gulp-concat'),
    del = require('del'),
    plumber = require('gulp-plumber'),
    pixrem = require('gulp-pixrem'),
    uglify = require('gulp-uglify'),
    imagemin = require('gulp-imagemin'),
    exec = require('gulp-exec'),
    runSequence = require('run-sequence'),
    browserSync = require('browser-sync'),
    pagespeed = require('psi');


// Relative paths function
var pathsConfig = function (appName) {
  this.app = "./" + (appName || pjson.name);

  return {
    app: this.app,
    templates: 'templates',
    css: 'static/css',
    sass: 'static/sass',
    fonts: 'static/fonts',
    images: 'static/images',
    js: 'static/js',
  }
};

var paths = pathsConfig();

////////////////////////////////
		//Tasks//
////////////////////////////////

var sassConfig = {
  precision: 6,
  indentedSyntax: false,
  sourceComments: false
}

// Styles autoprefixing and minification
gulp.task('styles', function() {
  return gulp.src(paths.sass + '/project.scss')
    .pipe(sass(sassConfig).on('error', sass.logError))
    .pipe(plumber()) // Checks for errors
    .pipe(autoprefixer({browsers: ['last 2 version']})) // Adds vendor prefixes
    .pipe(pixrem())  // add fallbacks for rem units
    .pipe(gulp.dest(paths.css))
    .pipe(rename({ suffix: '.min' }))
    .pipe(cssnano()) // Minifies the result
    .pipe(gulp.dest(paths.css));
});

// Javascript Concatenate + minification
gulp.task('scripts', function() {
  return gulp.src(['./node_modules/jquery/dist/jquery.min.js', './node_modules/tether/dist/js/tether.min.js', './node_modules/bootstrap/dist/js/bootstrap.min.js', '/raven.min.js', '/project.js'])
    .pipe(concat('project.js'))
    .pipe(plumber()) // Checks for errors
    .pipe(uglify()) // Minifies the js
    .pipe(rename({ suffix: '.min' }))
    .pipe(gulp.dest(paths.js));
});

// Image compression
gulp.task('imgCompression', function(){
  return gulp.src(paths.images + '/*')
    .pipe(imagemin()) // Compresses PNG, JPEG, GIF and SVG images
    .pipe(gulp.dest(paths.images))
});

// Run django server
gulp.task('runServer', function() {
  exec('python manage.py runserver', function (err, stdout, stderr) {
    console.log(stdout);
    console.log(stderr);
  });
});

// Browser sync server for live reload
gulp.task('browserSync', function() {
    browserSync.init(
      [paths.css + "/*.css", paths.js + "*.js", paths.templates + '*.html'], {
        proxy:  "localhost:8000"
    });
});

// Default task
gulp.task('default', function() {
    runSequence(['styles', 'scripts', 'imgCompression'], 'runServer', 'browserSync');
});


// Run PageSpeed Insights
gulp.task('pagespeed', function (cb) {
  // Update the below URL to the public URL of your site
  pagespeed.output('https://einhorn-starter.herokuapp.com', {
    strategy: 'desktop',
    // By default we use the PageSpeed Insights free (no API key) tier.
    // Use a Google Developer API key if you have one: http://goo.gl/RkN0vE
    // key: 'YOUR_API_KEY'
  }, cb);
});


////////////////////////////////
		//Watch//
////////////////////////////////

// Watch
gulp.task('watch', ['default'], function() {

  gulp.watch(paths.sass + '/*.scss', ['styles']);
  gulp.watch(paths.js + '/*.js', ['scripts']);
  gulp.watch(paths.images + '/*', ['imgCompression']);
  gulp.watch('templates/*.html');

});
