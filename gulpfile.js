var gulp             = require('gulp'),
    compass          = require('gulp-compass'),
    notify           = require('gulp-notify'),
    plumber          = require('gulp-plumber'),
    browserify       = require('browserify'),
    watchify         = require('watchify'),
    babelify         = require('babelify'),
    path             = require('path'),
    source           = require('vinyl-source-stream'),
    buffer           = require('vinyl-buffer'),
    rename           = require('gulp-rename'),
    uglify           = require('gulp-uglify');


//the title and icon that will be used for the notifications
var notifyInfo = {
    title: 'Gulp',
    icon: path.join(__dirname, 'gulp.png')
};

//error notification settings for plumber
var plumberErrorHandler = { errorHandler: notify.onError({
        title: notifyInfo.title,
        icon: notifyInfo.icon,
        message: "Error: <%= error.message %>"
    })
};

var config = {
     sassPath: './app_source/sass',
     bootstrapDir: './node_modules/bootstrap' ,
}

var deps = [
    'jquery',
    'lodash',
    'react',
    'react-dom'
];

var app_bundler = function() {
    return browserify({
        entries: ['./app_source/js/lj.js'],
        external: deps,
        bundleExternal: false,
        transform: [[babelify, {presets: ["es2015", "react"]}]],
        debug: true, // adds sourcemap
        cache: {}, packageCache: {}, fullPaths: true // needed for watchify
    });
};

var app_bundle_pipeline = function(bundler) {
    return bundler
        .bundle()  // create new bundle using the cache
        .pipe(source('lj.js'))
        // .pipe(buffer())
        // .pipe(sourcemaps.init({loadMaps: true}))
        // .pipe(uglify())
        // .pipe(sourcemaps.write('./'))
        .pipe(gulp.dest('./learning_journal/static/js/'))
        .pipe(notify({title: 'Gulp', icon: notifyInfo.icon, message: 'Built JS'}));
};

//vendor script bundle
gulp.task('vendor', function() {
    return browserify({
        require: deps,
        debug: false,  // no sourcemap for vendor libs
    })
    .bundle()
    .pipe(source('vendor.js'))
    .pipe(buffer())
    .pipe(uglify())
    .pipe(rename('vendor.min.js'))
    .pipe(gulp.dest('./learning_journal/static/js/'))
    .pipe(notify({title: 'Gulp', icon: notifyInfo.icon, message: 'Built vendor JS'}));
});

//scripts
gulp.task('scripts', function() {
    return app_bundle_pipeline(app_bundler());
});

gulp.task('bstrapcss', function() {
    return gulp.src(config.bootstrapDir + '/dist/css/bootstrap*.min.css')
        .pipe(gulp.dest('./learning_journal/static/css/'))
        .pipe(notify({title: 'Gulp', icon: notifyInfo.icon, message: 'Copied boostrap css'}));
});

gulp.task('bstrapfonts', function() {
    return gulp.src(config.bootstrapDir + '/dist/fonts/*.*')
        .pipe(gulp.dest('./learning_journal/static/fonts/'))
        .pipe(notify({title: 'Gulp', icon: notifyInfo.icon, message: 'Copied boostrap fonts'}));
});

gulp.task('bootstrap', ['bstrapcss', 'bstrapfonts']);

//styles
gulp.task('styles', function() {
    return gulp.src(['./app_source/sass/*.scss'])
        .pipe(plumber(plumberErrorHandler))
        .pipe(compass({
            sass: './app_source/sass'
        }))
        .pipe(gulp.dest('learning_journal/static/css'))
        .pipe(notify({title: 'Gulp', icon: notifyInfo.icon, message: 'Built CSS'}));
});

//watch and rebuild
gulp.task('watch', ['vendor', 'bootstrap', 'styles'], function() {
    gulp.watch('./app_source/static/scss/**/*.scss', ['styles']);

    var watcher = watchify(app_bundler());
    watcher.on('update', function() { app_bundle_pipeline(watcher); }); // when any file updates
    return app_bundle_pipeline(watcher); // do initial bundle when the task starts
});

gulp.task('default', ['vendor', 'bootstrap', 'scripts', 'styles']);