module.exports = function (grunt) {
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-exec');

    grunt.initConfig({
        exec: {
            dockerStart: "docker-compose up -d",
            dockerStop: "docker-compose stop",
            deploy: "npm run deploy"
        }
    });

    grunt.registerTask("default", () => {
        grunt.task.run(["exec:dockerStart", "watch"]);
    });

    // grunt.registerTask("default", ["exec:dockerStart", "watch"]);
    grunt.registerTask("stop", ["exec:dockerStop"]);
};