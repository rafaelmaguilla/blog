module.exports = function (grunt) {
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        banner: '/*!\n' +
                '* <%= pkg.name %> - v<%= pkg.version %>\n' +
                '* @author <%= pkg.author %>\n' +
                '* Copyright <%= grunt.template.today("yyyy") %>' + 
                '*/',
        devDir: 'src',
        buildDir: 'dist',
        assetsDir: 'assets',
        watch: {
            styles: {
                files: ['<%= devDir %>/<%= assetsDir %>/less/*.less'],
                tasks: ['less:compilestyles'],
                options: {
                    nospawn: true
                }
            },
            copyhtml: {
            	files: ['<%= devDir %>/*.html'],
                tasks: ['copy:develop'],
                options: {
                    nospawn: true
                }  
            }
        },
        clean: {
            build: {
                src: ['<%= buildDir %>/']
            }
        },
        less: {
            compilestyles: {
                options: {
                    banner: '<%= banner %>'
                },
                files: {
                    '<%= buildDir %>/<%= assetsDir %>/css/moltran.min.css': '<%= devDir %>/<%= assetsDir %>/less/moltran.less'
                }
            },
            build: {
                options: {
                    compress: true,
                    yuicompress: true,
                    optimization: 2,
                    banner: '<%= banner %>'
                },
                files: {
                    '<%= buildDir %>/<%= assetsDir %>/css/moltran.min.css': '<%= devDir %>/<%= assetsDir %>/less/moltran.less'
                }
            }
        },
        htmlmin: {
			dist: {
		    	options: {
		        	removeComments: true,
		        	collapseWhitespace: true
		  		},
		    	files: [
                	{
                        expand: true,
                        cwd: '<%= devDir %>/',
                        src: '*.html',
                        dest: '<%= buildDir %>/'
                    },
                ]
			}
		},
        concat: {
            options: {
                separator: ';'
            },
            build: {
                src: [
                    '<%= devDir %>/<%= assetsDir %>/vendor/jquery/dist/jquery.js',
                    '<%= devDir %>/<%= assetsDir %>/vendor/bootstrap/dist/js/bootstrap.js',
                    '<%= devDir %>/<%= assetsDir %>/js/detect.js',
                    '<%= devDir %>/<%= assetsDir %>/vendor/fastclick/lib/fastclick.js',
                    '<%= devDir %>/<%= assetsDir %>/js/jquery.slimscroll.js',                       
                    '<%= devDir %>/<%= assetsDir %>/vendor/blockUI/jquery.blockUI.js',
                    '<%= devDir %>/<%= assetsDir %>/js/waves.js',
                    '<%= devDir %>/<%= assetsDir %>/js/wow.min.js',
                    '<%= devDir %>/<%= assetsDir %>/js/jquery.nicescroll.js',
                    '<%= devDir %>/<%= assetsDir %>/js/jquery.scrollTo.js',
                    '<%= devDir %>/<%= assetsDir %>/js/jquery.app.js'
                ],
                dest: '<%= buildDir %>/<%= assetsDir %>/js/moltran.min.js'
            }
        },
        uglify: {
            options: {
                banner: '<%= banner %>'
            },
            build: {
                files: {
                    '<%= buildDir %>/<%= assetsDir %>/js/moltran.min.js': ['<%= buildDir %>/<%= assetsDir %>/js/moltran.min.js']
                }
            }
        },
        copy: {
        	develop: {
                files: [
                	{
                        expand: true,
                        cwd: '<%= devDir %>/',
                        src: '*.html',
                        dest: '<%= buildDir %>/'
                    },
                ]
            },
            build: {
                files: [
                    {
                        expand: true,
                        cwd: '<%= devDir %>/<%= assetsDir %>/fonts/',
                        src: '**',
                        dest: '<%= buildDir %>/<%= assetsDir %>/fonts/'
                    },
                    {
                        expand: true,
                        cwd: '<%= devDir %>/<%= assetsDir %>/images/',
                        src: '**',
                        dest: '<%= buildDir %>/<%= assetsDir %>/images/'
                    },
                    {
                        expand: true,
                        cwd: '<%= devDir %>/<%= assetsDir %>/vendor/',
                        src: '**',
                        dest: '<%= buildDir %>/<%= assetsDir %>/vendor/'
                    },
                    {
                        expand: true,
                        cwd: '<%= devDir %>/<%= assetsDir %>/plugins/',
                        src: '**',
                        dest: '<%= buildDir %>/<%= assetsDir %>/plugins/'
                    },
                    {
                        expand: true,
                        cwd: '<%= devDir %>/<%= assetsDir %>/pages/',
                        src: '**',
                        dest: '<%= buildDir %>/<%= assetsDir %>/pages/'
                    },
                    /*{
                        expand: true,
                        cwd: '<%= devDir %>/',
                        src: '*.html',
                        dest: '<%= buildDir %>/'
                    },*/
                ],
            }
        }
    });

    // Load tasks
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-contrib-clean');
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-contrib-htmlmin');

    // Register Tasks
    grunt.registerTask('default', ['watch']);
    grunt.registerTask('build', ['clean:build', 'less:build', 'htmlmin:dist', 'concat:build', 'uglify:build', 'copy:build']);
};