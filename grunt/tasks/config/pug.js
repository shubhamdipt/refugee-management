module.exports = function (grunt) {

  grunt.config.set('pug', {
    django: {
      options: {
        pretty: true
      },
      files: [{
        expand: true,
        src: ['**/*.pug', '!**/*.mixins.pug'],
        dest: 'templates/',
        cwd: 'templates',
        ext: '.html'
      }]
    },
  });

  grunt.loadNpmTasks( 'grunt-contrib-pug' );
};
