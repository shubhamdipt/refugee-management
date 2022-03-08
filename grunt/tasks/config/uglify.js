module.exports = function (grunt) {

  grunt.config.set('uglify', {
    options: {
      beautify: false,
      mangle: true
    },
    my_target: {
      files: [{
        expand: true,
        cwd: 'staticassets/js',
        src: '**/*.js',
        dest: 'static/js'
      }]
    }
  });

  grunt.loadNpmTasks( "grunt-contrib-uglify" );
};
