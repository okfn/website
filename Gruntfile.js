module.exports = function(grunt) {

  const sass = require('node-sass');

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

    sass: {
      options: {
        implementation: sass,
        sourceMap: true
      },
      dist: {
        files: [{
          expand: true,
          cwd: 'src/scss',
          src: ['*.scss'],
          dest: 'static/css',
          ext: '.css'
        }]
      }
    },

    postcss: {
      options: {
        map: true,
        processors: [
          require('autoprefixer'),
          require('cssnano')
        ]
      },
      dist: {
        src: 'static/css/*.css'
      }
    },

    shell: {
      tokens: {
        command: 'npx style-dictionary build',
          options: {
          execOptions: {
            cwd: 'design-tokens'
          }
        }
      }
    },

    uglify: {
      scripts: {
        files: {
          'static/js/scripts.js': [
            'node_modules/jquery/dist/jquery.js',
            'node_modules/bootstrap/dist/js/bootstrap.bundle.js',
            'node_modules/jquery.mmenu/dist/jquery.mmenu.all.js',
            'src/js/dom.js'
          ]
        }
      }
    },

    watch: {
      css: {
        files: '**/*.scss',
        tasks: ['sass', 'postcss:dist']
      },

      tokens: {
        files: 'design-tokens/properties/**/*.json',
        tasks: ['shell:tokens']
      },

      js: {
        files: 'src/js/*.js',
        tasks: ['uglify']
      }
    }
  });

  // Load the plugins
  grunt.loadNpmTasks('grunt-sass');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-postcss');
  grunt.loadNpmTasks('grunt-shell');
  grunt.loadNpmTasks('grunt-contrib-uglify');

  grunt.registerTask('default',['watch']);
};
