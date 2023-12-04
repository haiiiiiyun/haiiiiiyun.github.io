---
title: Sass 基础知识
date: 2016-09-06
writing-time: 2016-09-06 08:02--10:31
categories: programming
tags: Sass Utility LearnXinYminutes
---

## 概述

Sass 是一种 CSS 扩展语言，它增加了如变量、嵌套、mixin 等功能。
Sass (及其它预处理器，如 [Less](http://lesscss.org/)) 能帮助开发人员编写易维护和 DRY (Don't Repeat Yourself) 的代码。

Sass 有两种不同的语法可选用。SCSS 的语法和 CSS 的一样，但增加了一些其它功能。或者 Sass （原来的语法），它使用缩进而非大括号和分号。

本教程使用 SCSS 编写。

如果你已熟悉 CSS3，你可能相对能较快掌握 Sass。它并没有提供任何新的类型属性，它只是提供了一些工具使你能编写更高效的 CSS 并使维护更加容易。

## 实践 Sass

如果想在浏览器中测试 Sass，访问 [SassMeister](http://sassmeister.com/)。
可以选用任一种语法，只需到设置页中选择 Sass 或者 SCSS。


```scss
//单行注释在编译成 CSS 后会被删除。

/* 多行注释将保留. */

/* 变量
============================== */

/* 你可以将一个 CSS 值（如一个颜色值）保存到变量中。
使用 '$' 符号来创建一个变量。*/

$primary-color: #A3A4FF;
$secondary-color: #51527F;
$body-font: 'Roboto', sans-serif;

/* 你可以在你的样式文件中全局引用变量。
现在假如要修改颜色，只需修改一次即可。*/

body {
	background-color: $primary-color;
	color: $secondary-color;
	font-family: $body-font;
}

/* 以上将编译成： */
body {
	background-color: #A3A4FF;
	color: #51527F;
	font-family: 'Roboto', sans-serif;
}

/* 相比在全文中逐个修改，这种方式维护性更好。 */


/* 控制指令
============================== */

/* Sass 中可以使用 @if, @else, @for, @while, 和 @each 来控制
   代码如何编译成 CSS */

/* @if/@else 块的行为和你预想的完全相同 */

$debug: true !default;

@mixin debugmode {
	@if $debug {
		@debug "Debug mode enabled";

		display: inline-block;
	}
	@else {
		display: none;
	}
}

.info {
	@include debugmode;
}

/* 如果 $debug 设置为 true, .info 将显示; 如果设置为 false 那么
.info 将不显示。

注意： @debug 是在命令行中输出调试信息。
在调试 SCSS 时对于检查变量很有用。*/

.info {
	display: inline-block;
}

/* @for 是控制循环，它能遍历区间值。
它对于设置一组元素的类型特别有用。
有两种形式，"through" 和 "to"。 前者包括最后一个值，
而后者不包括。 
定义的变量一般都为属性值，
如果作为属性值使用， 可以直接用 $var 形式，
而在其它特殊情况下使用时, 必须用 #{$var} 的形式。
*/

@for $c from 1 to 4 {
	div:nth-of-type(#{$c}) {
		left: ($c - 1) * 900 / 3;
	}
}

@for $c from 1 through 3 {
	.myclass-#{$c} {
		color: rgb($c * 255 / 3, $c * 255 / 3, $c * 255 / 3);
	}
}

/* 将编译成: */

div:nth-of-type(1) {
	left: 0;
}

div:nth-of-type(2) {
	left: 300;
}

div:nth-of-type(3) {
	left: 600;
}

.myclass-1 {
	color: #555555;
}

.myclass-2 {
	color: #aaaaaa;
}

.myclass-3 {
	color: white;
// Sass 自动将 #FFFFFF 转换成 white
}

/* @while 也非常直白： */

$columns: 4;
$column-width: 80px;

@while $columns > 0 {
	.col-#{$columns} {
		width: $column-width;
		left: $column-width * ($columns - 1);
	}

	$columns: $columns - 1;
}

/* 将输出以下 CSS: */

.col-4 {
	width: 80px;
	left: 240px;
}

.col-3 {
	width: 80px;
	left: 160px;
}

.col-2 {
	width: 80px;
	left: 80px;
}

.col-1 {
	width: 80px;
	left: 0px;
}

/* @each 函数类似 @for, 除了它使用列表而不是普通的值
注意: 指定列表的方式和指定其它变量一样，
但用空格作为分隔符。 */

$social-links: facebook twitter linkedin reddit;

.social-links {
	@each $sm in $social-links {
		.icon-#{$sm} {
			background-image: url("images/#{$sm}.png");
		}
	}
}

/* 将输出: */

.social-links .icon-facebook {
	background-image: url("images/facebook.png");
}

.social-links .icon-twitter {
	background-image: url("images/twitter.png");
}

.social-links .icon-linkedin {
	background-image: url("images/linkedin.png");
}

.social-links .icon-reddit {
	background-image: url("images/reddit.png");
}


/*Mixin
==============================*/

/* 如果你要为多个元素编写相同的代码，
应该将相同的代码抽取到一个 mixin 中。

使用 '@mixin' 指令，再加一个 mixin 名。*/

@mixin center {
	display: block;
	margin-left: auto;
	margin-right: auto;
	left: 0;
	right: 0;
}

/* 可以通过 '@include' 和  mixin 名来调用。 */

div {
	@include center;
	background-color: $primary-color;
}

/* 将编译成: */
div {
	display: block;
	margin-left: auto;
	margin-right: auto;
	left: 0;
	right: 0;
	background-color: #A3A4FF;
}

/* 可以使用 mixin 来创建一个快捷属性。*/

@mixin size($width, $height) {
	width: $width;
	height: $height;
}

/* 通过传入 width 和 height 参数来调用。*/

.rectangle {
	@include size(100px, 60px);
}

.square {
	@include size(40px, 40px);
}

/* 编译成: */
.rectangle {
  width: 100px;
  height: 60px;
}

.square {
  width: 40px;
  height: 40px;
}


/* 函数
============================== */


/* Sass 提供的函数可以用来完成各种不同任务。
   考虑以下情况 */

/* 函数通过其名称及传入的必要参数来调用 */
body {
  width: round(10.25px);
}

.footer {
  background-color: fade_out(#000000, 0.25);
}

/* 编译成: */

body {
  width: 10px;
}

.footer {
  background-color: rgba(0, 0, 0, 0.75);
}

/* 也可以定义自己的函数。函数非常类似于 mixin。
   当你纠结于选用哪个时，记住 mixin 最适于创建 CSS 而函数更适于处理逻辑。
   '数学操作符' 节中的例子是转成可重用函数的最理想候选。 */

/* 该函数将接收一个 target-size 和 parent-size 参数，然后计算并
    返回百分数 */

@function calculate-percentage($target-size, $parent-size) {
  @return $target-size / $parent-size * 100%;
}

$main-content: calculate-percentage(600px, 960px);

.main-content {
  width: $main-content;
}

.sidebar {
  width: calculate-percentage(300px, 960px);
}

/* 编译成: */

.main-content {
  width: 62.5%;
}

.sidebar {
  width: 31.25%;
}


/* 扩展 (继承)
============================== */


/* 扩展是在选择子间共享属性的一种方法。 */

.display {
	@include size(5em, 5em);
	border: 5px solid $secondary-color;
}

.display-success {
	@extend .display;
	border-color: #22df56;
}

/* 编译成: */
.display, .display-success {
  width: 5em;
  height: 5em;
  border: 5px solid #51527F;
}

.display-success {
  border-color: #22df56;
}

/* 扩展 CSS 语句时，相比创建一个 mixin，
   优先使用扩展，由于 Sass 整理类的方式，这些
   类将共享相同的基样式。如果使用 mixin 完成，width,
   height, border 将会在调用该 mixin 的语句中重复。
   虽然它不影响你的工作流，但它会在编译后的文件中添加不必要的
   代码。*/


/* 嵌套
============================== */


/* Sass 允许在选择子中嵌套选择子 */

ul {
	list-style-type: none;
	margin-top: 2em;

	li {
		background-color: #FF0000;
	}
}

/* '&' 将以父选择子替换。*/
/* 也可以嵌套伪类。 */
/* 注意过度嵌套将会使代码难以维护。
   最佳实践是不超过 3 层嵌套。
   例如： */

ul {
	list-style-type: none;
	margin-top: 2em;

	li {
		background-color: red;

		&:hover {
		  background-color: blue;
		}

		a {
		  color: white;
		}
	}
}

/* 编译成： */

ul {
  list-style-type: none;
  margin-top: 2em;
}

ul li {
  background-color: red;
}

ul li:hover {
  background-color: blue;
}

ul li a {
  color: white;
}


/* 片段与导入
============================== */

/* Sass 允许创建片段文件。它能使你的 Sass 代码更具模块化。
   片段文件应该以 '_' 开头，例如 _reset.css。
   片段文件不会包含在产生的 CSS 文件列表中。*/

/* 考虑将下面的 CSS 放入 _reset.css */

html,
body,
ul,
ol {
  margin: 0;
  padding: 0;
}

/* Sass 的 @import 能用来将片段导入文件中。
   它与传统的 CSS @import 语句不同，不需要通过
   HTTP 请求来获取导入的文件。
   Sass 会将导入文件与编译后的代码结合起来。 */

@import 'reset';

body {
  font-size: 16px;
  font-family: Helvetica, Arial, Sans-serif;
}

/* 编译成: */

html, body, ul, ol {
  margin: 0;
  padding: 0;
}

body {
  font-size: 16px;
  font-family: Helvetica, Arial, Sans-serif;
}



/* 占位符选择子
============================== */


/* 占位符在创建用于扩展的 CSS 语句时非常有用。
   如果你创建的 CSS 语句只为 @extend 使用，可以利用占位符来实现。
   占位符以 '%' 而非 '.' 或 '#' 开头。占位符不会出现在编译后的 CSS 中 */

%content-window {
  font-size: 14px;
  padding: 10px;
  color: #000;
  border-radius: 4px;
}

.message-window {
  @extend %content-window;
  background-color: #0000ff;
}

/* 编译成: */

.message-window {
  font-size: 14px;
  padding: 10px;
  color: #000;
  border-radius: 4px;
}

.message-window {
  background-color: #0000ff;
}


/* 数学操作
============================== */


/* Sass 提供以下的操作符: +, -, *, /, 和 %。它们
   对于直接在你的 Sass 文件中计算值很有用，而无需自己手工先计算。
   以下是设置一个两列设计的例子。*/

$content-area: 960px;
$main-content: 600px;
$sidebar-content: 300px;

$main-size: $main-content / $content-area * 100%;
$sidebar-size: $sidebar-content / $content-area * 100%;
$gutter: 100% - ($main-size + $sidebar-size);

body {
  width: 100%;
}

.main-content {
  width: $main-size;
}

.sidebar {
  width: $sidebar-size;
}

.gutter {
  width: $gutter;
}

/* 编译成： */

body {
  width: 100%;
}

.main-content {
  width: 62.5%;
}

.sidebar {
  width: 31.25%;
}

.gutter {
  width: 6.25%;
}

```

## SASS 还是 Sass?
该语言的名字，“Sass”，是一个词，不是一个缩写。


## 兼容性
只要你有将它编译成 CSS 的程序，Sass 可以用于任何项目中。
你还需要验证你所使用的 CSS 是否与你的目标浏览器兼容。

[QuirksMode CSS](http://www.quirksmode.org/css/) 和 [CanIUse](http://caniuse.com) 是检查兼容性的有好的资源。


## 更多资源
* [Official Documentation](http://sass-lang.com/documentation/file.SASS_REFERENCE.html)
* [The Sass Way](http://thesassway.com/) provides tutorials (beginner-advanced) and articles.
```

> 参考文献： [Learn Sass in Y minutes](https://learnxinyminutes.com/docs/sass/)
