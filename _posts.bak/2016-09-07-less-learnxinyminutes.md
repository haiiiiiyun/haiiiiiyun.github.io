---
title: Less 基础知识
date: 2016-09-07
writing-time: 2016-09-07 09:50--10:17
categories: programming
tags: Less Utility LearnXinYminutes
---

## 概述

Less 是一种 CSS 扩展语言，它增加了如变量、嵌套、mixin 等功能。
Less (及其它预处理器，如 [Sass](http://sass-lang.com/)) 能帮助开发人员编写易维护和 DRY (Don't Repeat Yourself) 的代码。

## 实践 Less

如果想在浏览器中测试 Less，尝试下：
* [Codepen](http://codepen.io/)
* [LESS2CSS](http://lesscss.org/less-preview/)


```less
//单行注释在编译成 CSS 后会被删除。

/* 多行注释将保留. */

/* 变量
============================== */

/* 你可以将一个 CSS 值（如一个颜色值）保存到变量中。
使用 '@' 符号来创建一个变量。*/

@primary-color: #A3A4FF;
@secondary-color: #51527F;
@body-font: 'Roboto', sans-serif;

/* 你可以在你的样式文件中全局引用变量。
现在假如要修改颜色，只需修改一次即可。*/

body {
	background-color: @primary-color;
	color: @secondary-color;
	font-family: @body-font;
}

/* 以上将编译成： */
body {
	background-color: #A3A4FF;
	color: #51527F;
	font-family: 'Roboto', sans-serif;
}

/* 相比在全文中逐个修改，这种方式维护性更好。 */


/*Mixin
==============================*/


/* 如果你要为多个元素编写相同的代码，
你可以想实现更容易的重用。*/

.center {
	display: block;
	margin-left: auto;
	margin-right: auto;
	left: 0;
	right: 0;
}

/* 只需简单地将选择子作为样式添加进来就能使用 mixin 了 */

div {
	.center;
	background-color: @primary-color;
}

/* 将编译成: */
.center {
	display: block;
	margin-left: auto;
	margin-right: auto;
	left: 0;
	right: 0;
}
div {
	display: block;
	margin-left: auto;
	margin-right: auto;
	left: 0;
	right: 0;
	background-color: #A3A4FF;
}

/* 如果在选择子后面添加括号，那么这些 mixin
代码将被忽略编译进最终文件中*/

.center() {
  display: block;
  margin-left: auto;
  margin-right: auto;
  left: 0;
  right: 0;
}

div {
  .center;
  background-color: @primary-color;
}

/* 它将编译成： */
div {
  display: block;
  margin-left: auto;
  margin-right: auto;
  left: 0;
  right: 0;
  background-color: #a3a4ff;
}


/* 嵌套
============================== */


/* Less 允许在选择子中嵌套选择子 */

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


/* 函数
============================== */


/* Less 提供的函数可以用来完成各种不同任务。
   考虑以下情况 */

/* 函数通过其名称及传入的必要参数来调用 */
body {
  width: round(10.25px);
}

.header {
	background-color: lighten(#000, 0.5);
}

.footer {
  background-color: fade_out(#000, 0.25);
}

/* 编译成: */

body {
  width: 10px;
}

.header {
  background-color: #010101;
}

.footer {
  background-color: rgba(0, 0, 0, 0.75);
}

/* 也可以定义自己的函数。函数非常类似于 mixin。
   当你纠结于选用哪个时，记住 mixin 最适于创建 CSS 而函数更适于处理逻辑。
   '数学操作符' 节中的例子是转成可重用函数的最理想候选。 */

/* 该函数将接收一个 target-size 和 parent-size 参数，然后计算并
    返回百分数 */

.average(@x, @y) {
  @average-result: ((@x + @y) / 2);
}

div {
  .average(16px, 50px); // 有参数的 mixin 就是函数？
  padding: @average-result;    // 使用返回值
}

/* 编译成：*/

div {
  padding: 33px;
}


/* 扩展 (继承)
============================== */


/* 扩展是在选择子间共享属性的一种方法。 */

.display {
    height: 50px;	
}

.display-success {
	&:extend(.display);
	border-color: #22df56;
}

/* 编译成: */
.display, .display-success {
    height: 50px;
}

.display-success {
  border-color: #22df56;
}

/* 扩展 CSS 语句时，相比创建一个 mixin，
   优先使用扩展，由于 Less 整理类的方式，这些
   类将共享相同的基样式。如果使用 mixin 完成，width,
   height, border 将会在调用该 mixin 的语句中重复。
   虽然它不影响你的工作流，但它会在编译后的文件中添加不必要的
   代码。*/


/* 片段与导入
============================== */

/* Less 允许创建片段文件。它能使你的 Less 代码更具模块化。
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

/* Less 的 @import 能用来将片段导入文件中。
   它与传统的 CSS @import 语句不同，不需要通过
   HTTP 请求来获取导入的文件。
   Less 会将导入文件与编译后的代码结合起来。 */

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


/* 数学操作
============================== */


/* Less 提供以下的操作符: +, -, *, /, 和 %。它们
   对于直接在你的 Less 文件中计算值很有用，而无需自己手工先计算。
   以下是设置一个两列设计的例子。*/

@content-area: 960px;
@main-content: 600px;
@sidebar-content: 300px;

@main-size: @main-content / @content-area * 100%;
@sidebar-size: @sidebar-content / @content-area * 100%;
@gutter: 100% - (@main-size + @sidebar-size);

body {
  width: 100%;
}

.main-content {
  width: @main-size;
}

.sidebar {
  width: @sidebar-size;
}

.gutter {
  width: @gutter;
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

## 兼容性
只要你有将它编译成 CSS 的程序，Less 可以用于任何项目中。
你还需要验证你所使用的 CSS 是否与你的目标浏览器兼容。

[QuirksMode CSS](http://www.quirksmode.org/css/) 和 [CanIUse](http://caniuse.com) 是检查兼容性的有好的资源。


## 更多资源
* [Official Documentation](http://lesscss.org/features/)
* [Less CSS - Beginner's Guide](http://www.hongkiat.com/blog/less-basic/)
```

> 参考文献： [Learn Less in Y minutes](https://learnxinyminutes.com/docs/less/)
