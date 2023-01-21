"use strict";

var gulp = require("gulp"),
    HubRegistry = require('gulp-hub'),
    browsersync = require("browser-sync"),
    vars = require('./variables');


/**
 * Register all the tasks
 */
// load some files into the registry
var hub = new HubRegistry(['tasks/*.js']);

// tell gulp to use the tasks just loaded
gulp.registry(hub);

/**
 * Watches the changes
 */
function watchFiles() {
    const srcPath = vars.getSrcPath();
    const baseAssets = vars.getBaseAssetsPath();

    gulp.watch(baseAssets + "images/**/*", gulp.series('copyImages'));
    gulp.watch(baseAssets + "fonts/**/*", gulp.series('copyFonts'));
    gulp.watch(baseAssets + "scss/**/*", gulp.series('compileSaas'));
    gulp.watch(baseAssets + "js/**/*", gulp.series("compileJs"));
}

/**
 * Default tasks
 */

// watch all changes
gulp.task("watch", gulp.parallel(watchFiles));

// default
gulp.task('default', gulp.series('copyAssets', 'copyImages', 'copyFonts', 'compileSaas', 'compileJs', 'watch'), function (done) { done(); });


// build
gulp.task("build", gulp.series('copyAssets', 'copyImages', 'copyFonts', 'compileSaas', 'compileJs'));
gulp.task("build-js", gulp.series('compileJs'));

// doc
gulp.task("docs", function () {
    browsersync.init({
        server: {
            baseDir: "docs"
        }
    });
});
