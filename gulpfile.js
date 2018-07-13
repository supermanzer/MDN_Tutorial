var gulp = require('gulp');
var sass = require('gulp-sass');
var concat = require('gulp-concat');
var rename = require('gulp-rename');
var uglify = require('gulp-uglify');

// Defining SASS and CSS variables
var sassFiles = 'assets/scss/*.scss',
      cssDest = 'static/css/';

//Processing any SASS into CSS
gulp.task('sass', function () {
    return gulp.src(sassFiles)
        .pipe(sass())
        .pipe(gulp.dest(cssDest))
})

// JS script paths
var jsFiles = 'assets/js/*.js',
      jsDest = 'static/js/';

gulp.task('scripts', function(){
    return gulp.src(jsFiles)
                .pipe(concat('scripts.js'))
                .pipe(gulp.dest(jsDest))
                .pipe(rename('scripts.min.js'))
                .pipe(uglify())
                .pipe(gulp.dest(jsDest));
});

// Change watching task to leave running while we develo
gulp.task('watch', function(){
    gulp.watch(sassFiles, ['sass']);
    gulp.watch(jsFiles,['scripts']);
});

gulp.task('default', ['sass', 'scripts', 'watch']);
