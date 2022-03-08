module.exports = function (grunt) {

  grunt.registerTask('assets', [
    'pug',
    'sass',
    'uglify',
    'cssmin'
  ]);

};
