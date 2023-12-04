---
title: Gulp 入门知识
date: 2016-12-08
writing-time: 2016-12-08 17:23--17:50
categories: programming Javascript Node
tags: Programming Javascript Gulp Node
---

# 概述

Gulp 是一个自动化构建工具。它依赖 NodeJS。

# 准备项目目录

在项目目录下，运行：

```bash
$ npm init
```

该命令会在当前目录下创建一个 `package.json` 文件，用来保存本项目及其依赖包的相关信息。

# 安装 Gulp

全局安装：

```bash
$ npm install -g gulp
```

非全局安装：

```bash
$ npm install --save-dev gulp
```

上面的 `--save-dev` 选项指示 npm 将相关的依赖信息都一并保存到之前创建的 `package.json` 中。

# 设置 gulpfile 并运行 Gulp

假设要完成下面的任务：

+ 检验 JavaScript
+ 编译 Sass 文件
+ 合并 JavaScript 文件
+ 混淆合并后的文件


## 安装所需的插件

```bash
$ npm install gulp-jshint gulp-sass gulp-contact gulp-uglify gulp-rename --save-dev
```

这将安装所有的依赖包并将依赖信息(devDependencies) 保存到 `package.json` 中。

## 创建 gulpfile 文件

Gulp 只有 5 个方法： task, run, watch, src, dest。

先在当前目录下创建 `gulpfile.js` 文件，文件内容如下：

```javascript
// Include gulp
var gulp = require('gulp');

// Include Our Plugins
var jshint = require('gulp-jshint')
var sass = require('gulp-sass')
var contact = require('gulp-contact')
var uglify = require('gulp-uglify')
var rename = require('gulp-rename')

// Lint Task
glup.task('lint', function() {
    return gulp.src('js/*.js')
        .pipe(jshint())
        .pipe(jshint.reporter('default'));
});

// Compile Our Sass
gulp.task('sass', function() {
    return gulp.src('scss/*.scss')
        .pipe(sass())
        .pipe(gulp.dest('dist/css'));
});

// Concatenate & Minify JS
gulp.task('scripts', function() {
    return gulp.src('js/*.js')
        .pipe(contact('all.js'))
        .pipe(glup.dest('dist'))
        .pipe(rename('all.min.js'))
        .pipe(uglify())
        .pipe(glup.dest('dist/js'));
});

// Watch Files For Changes
gulp.task('watch', function() {
    gulp.watch('js/*.js', ['lint', 'scripts']);
    gulp.watch('scss/*.scss', ['sass']);
});

// Default Task
gulp.task('default', ['lint', 'sass', 'scripts', 'watch']);
```

**watch** 任务会监视对文件的修改，一旦有变化就自动运行相应的任务。

定义的 **default** 任务实际就是对其它任务的一个组引用。当直接运行 `$ gulp` 时，会默认运行 default 任务。

当然，也可以指定运行某个任务，如 `$ gulp sass`

参考： [Getting Started with Gulp](https://travismaynard.com/writing/getting-started-with-gulp)
