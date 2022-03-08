module.exports = function (grunt) {

  grunt.config.set('sass', {
    dist: {
      files: {
        'static/css/styles.css': 'staticassets/sass/styles.scss',
      }
    }
  });

  grunt.loadNpmTasks( "grunt-contrib-sass" );
};
