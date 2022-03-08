module.exports = function (grunt) {

  var watchFilesAssets= [
    "**/*.pug",
    "**/*.scss",
    "**/*.js",
    "!node_modules/**",
    "!bower_components/**",
    "!static/js/**",
    "!static/vendor/**"
  ];

  var watchOptions = {
    interrupt: true,
    debounceDelay: 250
  };

  grunt.config.set('watch', {
    assets: {
      options: watchOptions,
      files: watchFilesAssets,
      tasks: [ "assets" ]
    }
  });

  grunt.loadNpmTasks( "grunt-contrib-watch" );
};
