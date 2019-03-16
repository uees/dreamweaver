const {src, dest, series, parallel} = require('gulp');
const cleanCss = require('gulp-clean-css'); // 压缩CSS
const rename = require('gulp-rename');  // 设置压缩后的文件名
const autoprefixer = require('gulp-autoprefixer');  // 给 CSS 增加前缀。解决某些CSS属性不是标准属性，有各种浏览器前缀的情况
const rev = require('gulp-rev');
const jeditor = require("gulp-json-editor");
const sass = require("gulp-sass");
const babel = require('gulp-babel');
const uglify = require('gulp-uglify');
const browserify = require('browserify');
const babelify = require('babelify');
const standalonify = require('standalonify');
const source = require('vinyl-source-stream');
const buffer = require('vinyl-buffer');

function bundleCss() {
    return src('src/scss/index.scss')
        .pipe(sass())
        .pipe(cleanCss()) // 压缩css
        .pipe(autoprefixer({
            browsers: ['last 2 versions', 'Safari >0', 'Explorer >0', 'Edge >0', 'Opera >0', 'Firefox >=20'], //last 2 versions- 主流浏览器的最新两个版本
            cascade: true, // 是否美化属性值 默认：true 像这样：
            // -webkit-transform: rotate(45deg);
            //        transform: rotate(45deg);
            remove: true // 是否去掉不必要的前缀 默认：true
        }))
        .pipe(rename('style.min.css')) // 设置压缩文件名
        .pipe(dest('public/static/css/')) // 输出文件的存放地址
}

function bundleJs() {
    // 创建 Browserify 实例
    return browserify({
        entries: 'src/js/index.js',  //指定打包入口文件
    })
        .plugin(standalonify, {
            name: 'Sar888'
        }) // 使打包后的js文件符合UMD规范
        .transform(babelify)  // babel 转化 es6 (配合.babelrc)
        .bundle() //合并打包
        .pipe(source('app.min.js')) // 将常规流转换为包含Stream的vinyl对象，并且重命名
        .pipe(buffer()) // 将vinyl对象内容中的Stream转换为Buffer
        .pipe(uglify())
        .pipe(dest('public/static/js/'))
}

function manifest() {
    return src(['public/static/js/app.min.js', 'public/static/css/style.min.css'])
        .pipe(rev())  // 添加 hash
        .pipe(rev.manifest()) // 生成 manifest
        .pipe(dest('public/static/'))  // manifest 的存放地址
}

function modifyManifest() {
    return src('public/static/rev-manifest.json')
        .pipe(jeditor(function (json) {
            for (let key of Object.keys(json)) {
                json[key] = json[key].replace(/[^-]+-(.+)\.min.(?:js|css)/, "$1");
            }
            return json;
        }))
        .pipe(dest('public/static/')) // manifest 的存放地址
}

exports.default = series(
    parallel(bundleCss, bundleJs),
    manifest,
    modifyManifest
);
