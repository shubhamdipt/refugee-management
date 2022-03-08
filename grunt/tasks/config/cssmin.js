// Project configuration.
module.exports = function (grunt) {

  grunt.config.set('cssmin', {
    styles: {
        files: {
            'static/css/styles.min.css': [
                'static/css/styles.css'
            ]
        }
    },
  });

  grunt.loadNpmTasks( "grunt-contrib-cssmin" );
};
