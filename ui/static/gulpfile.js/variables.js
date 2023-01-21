var args = require('yargs').argv;

/**
 * ---------------------------------------------------------------------------------------------
 * Global settings
 * ---------------------------------------------------------------------------------------------
*/

var FOLDER_PATHS = {
    baseSrc: "src/", // source files
    baseDist: "dist/", // build files
    baseAssets: "src/", // base assets
};

function getSrcFolderPath() {
    return FOLDER_PATHS.baseSrc + "/";
}

function getDistFolderPath() {
    return FOLDER_PATHS.baseDist + "/";
}


module.exports = {
    getBaseSrcPath: function () { return FOLDER_PATHS.baseSrc },
    getBaseDistPath: function () { return FOLDER_PATHS.baseDist },
    getBaseAssetsPath: function () { return FOLDER_PATHS.baseAssets },
    getSrcPath: getSrcFolderPath,
    getDistPath: getDistFolderPath,
    getDistAssetsPath: getDistFolderPath
}
