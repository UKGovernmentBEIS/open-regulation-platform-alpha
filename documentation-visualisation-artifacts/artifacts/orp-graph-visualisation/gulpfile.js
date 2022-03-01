// gulpfile.js
const {
    watch,
    series,
    src,
    dest
} = require("gulp");
var browserSync = require("browser-sync").create();
var cleanCss = require('gulp-clean-css');
var concat = require('gulp-concat');
var minify = require('gulp-minify');
var postcss = require("gulp-postcss");
var tailwindcss = require("tailwindcss");

// Task for compiling our CSS files using PostCSS
function cssTask(cb) {
    return src("./src/css/*.css") // read .css files from ./src/ folder
        .pipe(postcss()) // compile using postcss
        .pipe(dest("./assets/css")) // paste them in ./assets/css folder
        .pipe(browserSync.stream());
    cb();
}

function cssBuildTask(cb) {
    return src("./src/css/*.css") // read .css files from ./src/ folder
        .pipe(postcss()) // compile using postcss
        .pipe(cleanCss()) // minify files
        .pipe(dest("./assets/css")) // paste them in ./assets/css folder
        .pipe(browserSync.stream());
    cb();
}

// Task for compiling our Script files
function jsTask(cb) {
    return src(['src/js/vendor/*.js', 'src/js/scripts.js']) // read .js files from ./src/ folder
        .pipe(concat('bundle.js')) // merge files// minify files
        .pipe(dest("./assets/js")) // paste them in ./assets/js folder
        .pipe(browserSync.stream());
    cb();
}

function jsBuildTask(cb) {
    return src(['src/js/vendor/*.js', 'src/js/scripts.js']) // read .js files from ./src/ folder
        .pipe(concat('bundle.js')) // merge files
        .pipe(minify({
            ext: {
                min: '.js'
            },
            noSource: true
        })) // minify files
        .pipe(dest("./assets/js")) // paste them in ./assets/js folder
        .pipe(browserSync.stream());
    cb();
}

// Serve from browserSync server
function browsersyncServe(cb) {
    browserSync.init({
        server: {
            baseDir: "./",
        },
    });
    cb();
}

function browsersyncReload(cb) {
    browserSync.reload();
    cb();
}

// Watch Files & Reload browser after tasks
function watchTask() {
    watch("./**/*.html", browsersyncReload);
    watch("./**/*.json", browsersyncReload);
    watch(["./src/**/*.css"], series(cssTask, browsersyncReload));
    watch(["./src/**/*.js"], series(jsTask, browsersyncReload));
}

// Default Gulp Task
exports.default = series(cssTask, jsTask, browsersyncServe, watchTask);
exports.build = series(cssBuildTask, jsBuildTask);