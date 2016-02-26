var gulp             = require('gulp'),
    sass             = require('gulp-sass'),
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

var deps = [
    'jquery',
    'bootstrap',
    'lodash',
    'react',
    'react-dom',
    'react-lorem-component'
];

var app_bundler = function() {
    return browserify({
        entries: ['./app_source/js/lj.js'],
        external: deps,
        bundleExternal: true,
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

var app_minify_pipeline = function(bundler) {
    return bundler
        .bundle()  // create new bundle using the cache
        .pipe(source('lj.js'))
        .pipe(buffer())
        .pipe(uglify())
        .pipe(rename('lj.min.js'))
        .pipe(gulp.dest('./learning_journal/static/js/'))
        .pipe(notify({title: 'Gulp', icon: notifyInfo.icon, message: 'Built Minified JS'}));
};

//scripts
gulp.task('scripts', function() {
    return app_bundle_pipeline(app_bundler());
});

gulp.task('minify', function() {
    return app_minify_pipeline(app_bundler());
})

//styles
gulp.task('styles', function() {
    return gulp.src(['./app_source/sass/*.scss'])
        .pipe(plumber(plumberErrorHandler))
        .pipe(sass({outputStyle: 'compact'}))
        .pipe(gulp.dest('learning_journal/static/css'))
        .pipe(notify({title: 'Gulp', icon: notifyInfo.icon, message: 'Built CSS'}));
});

//watch and rebuild
gulp.task('watch', ['minify', 'scripts', 'styles'], function() {
    gulp.watch('./app_source/sass/*.scss', ['styles']);

    var watcher = watchify(app_bundler());
    watcher.on('update', function() {
        app_bundle_pipeline(watcher);
        app_minify_pipeline(watcher);
    }); // when any file updates
});

gulp.task('default', ['minify', 'scripts', 'styles']);