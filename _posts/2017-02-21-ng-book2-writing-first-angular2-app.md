---
title: 编写首个 Angular2 应用
date: 2017-02-21
writing-time: 2017-02-21 22:29--2017-03-13:15:49
categories: Programming
tags: Programming 《ng-book2-r49》 Angular2 Google JavaScript TypeScript Node ng2
---

# 环境设置

TypeScript 是 JavaScript ES6 的超集，它添加了对类型的支持。

Angular 2(简称 ng2) 虽然提供了 ES5 (普通 JavaScript) API，但由于其本身是用 TypeScript 编写的，因此 ng2 应用最好也应该用 TypeScript 编写。

TypeScript 依赖 Node，故要先 [安装 Node](https://nodejs.org/en/download/package-manager/#debian-and-ubuntu-based-linux-distributions)。

## 安装 angular-cli

这个命令行可以用来管理 ng 项目，如创建项目，创建控制器等常用任务。 安装 angular-cli:

```bash
$ sudo npm install -g @angular/cli
```

由于开发 ng 项目时有时会构建一些 Node 的本地 addon，一般还要安装 [node-gyp](https://www.npmjs.com/package/node-gyp) ：

```bash
$ sudo npm install -g node-gyp
```

安装好后会有 ng 命令，运行该命令后会有一大串输出：

```bash
$ ng # 安装好后会有该命令
Could not start watchman; falling back to NodeWatcher for file system events.
3 Visit http://ember-cli.com/user-guide/#watchman for more info.
4 Usage: ng <command (Default: help)>
...
```

在 OSX 或 Linux 上运行一般会有 'Could not start watchman ...' 的输出，这是因为我们还没有安装 [watchman](https://ember-cli.com/user-guide/#watchman)，该程序能帮助 angular-cli 监测项目中的文件修改情况。如果在 OSX 上，最好通过 Homebrew 安装它：

```bash
$ brew install watchman
```

# 一个示例项目

创建项目：

```bash
$ ng new angular2-hello-world #@angular/cli: 1.0.0-beta.32.3 创建的项目名似乎不支持 _, 如 angular2-hello-world 为有效项目名，而 angualr2_hello_world 无效

1 installing ng2
2 create .editorconfig
3 create README.md
4 create src/app/app.component.css
5 create src/app/app.component.html
...
33 Successfully initialized git.
34  Installing packages for tooling via npm
...
Project 'angular2-hello-world' successfully created.
```

等待一段时间后，会出现 "Project 'angular2-hello-world' successfully created."，说明已经创建项目成功。 ng 为该项目创建了很多的默认文件。

通过 tree 命令可以看到项目的文件目录结构：

```bash
$ tree -F -L 1
.
├── e2e/
├── karma.conf.js
├── node_modules/
├── package.json
├── protractor.conf.js
├── README.md
├── src/
└── tslint.json

3 directories, 5 files
```

项目根目录下的文件和目录用途说明如下：

+ `src/*`: 源代码目录
+ `e2e/*`: End-to-End 测试文件。 e2e 测试是一个独立的应用，用于测试我们的主应用，因此它们不放在 `src/` 下，并且有自己的 `tsconfig.json` 文件
+ `node_modules/...`: Node 将列于 package.json 中的依赖包安装在该目录下
+ `.editorconfig`: 编辑器的通用配置文件，大多数编辑器都支持加载 .editorconfig 中的配置项，见 http://editorconfig.org
+ `angular-cli.json`: Angular-CLI 的配置信息。可以设置一些默认值，也可配置当构建项目时要包含的文件
+ `karma.conf.js`: [Karma test runner](https://karma-runner.github.io/) 单元测试的配置文件，当运行 `ng test` 时会用到
+ `package.json`: npm 将项目的依赖包记录在该文件中。也可以在文件内添加 [自定义的脚本](https://docs.npmjs.com/misc/scripts)
+ `protractor.conf.js`: [Protractor](http://www.protractortest.org/) 的 e2e 测试配置文件，当运行 `ng e2e` 时使用
+ `tslint.json`: 有关 [TSLint](https://palantir.github.io/tslint/) 和 [Codelyzer](http://codelyzer.com/) 的配置文件，当运行 `ng lint` 时使用


而源代码目录里包含了 Angular 的所有组件，模板，样式，图片，及项目所需的其它所有内容。目录结构如下：

```bash
$ cd src
$ tree -F
.
├── app/
│   ├── app.component.css
│   ├── app.component.html
│   ├── app.component.spec.ts
│   ├── app.component.ts
│   └── app.module.ts
├── assets/
├── environments/
│   ├── environment.prod.ts
│   └── environment.ts
├── favicon.ico
├── index.html
├── main.ts
├── polyfills.ts
├── styles.css
├── test.ts
└── tsconfig.json

3 directories, 14 files
```

各文件和目录的用途：

+ `app/app.component.{ts,html,css,spec.ts}`: 定义 `AppComponent` 及其 HTML 模板，CSS 样式和单元测试。这是 ng 项目组件树的根组件。
+ `app/app.module.ts`: 定义 `AppModule`, 该模块能告诉 Angular 如何组装应用。新建项目后，该文件中只有一个 `AppComponent`，但是之后自定义的组件也要加到该文件中。
+ `assets/*`: 保存图片等文件，该目录中的内容在应用构建时会原样复制。
+ `environments/*`: 每个目标环境都对应一个配置文件，如开发环境、生产环境等。
+ `indext.html`: 主 HTML 页。通常无需对它手动编辑，CLI 在应用构建过程中会自动将所需的 js 和 css 文件链接进去。
+ `main.ts`: 这是应用的主入口点。[JIT 编译器](https://angular.io/docs/ts/latest/glossary.html#jit) 对它编译后，再在浏览器中启动应用的根模块 (AppModule) 运行。也可以用 [AoT 编译器](https://angular.io/docs/ts/latest/glossary.html#ahead-of-time-aot-compilation) 进行编译，只需在运行 `ng build` 或 `ng serve` 时传入 `--aot` 参数即可。
+ `polyfills.ts`: 不同的浏览器对标准的支持不同，而该文件就是用来磨平这些区别的。在使用 `core-js` 和 `zone.js` 时需当心，更多信息见 [Browser Support guide](https://angular.io/docs/ts/latest/guide/browser-support.html)。
+ `styles.css`: 全局的样式放这里。通常为便于维护，自定义组件的样式都放在其定义目录中。
+ `test.ts`: 单元测试的主入口。
+ `tsconfig.json`: TypeScript 编译器的配置文件。


## 源代码文件

先看 `src/index.html`:

```html
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Angular2HelloWorld</title>
  <base href="/">

  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" type="image/x-icon" href="favicon.ico">
</head>
<body>
  <app-root>Loading...</app-root>
</body>
</html>
```

里面定义了 charset, base href 等，`app-root` 标签是我们的 ng 应用呈现的位置。


## 运行

在项目根目录下：

```bash
$ ng serve
** NG Live Development Server is running on http://localhost:4200. **
// a bunch of debug messages

Build successful - 1342ms.
```

现可以在浏览器里使用 `http://localhost:4200` 访问应用了。

## 制作一个组件 (Component)

Angular 中最大的思想就是组件化。

浏览器通常只理解标准化的标签，如 select, form, video 等。如何让浏览器理解新的标签，如显示天气信息的 weather 标签，或显示登录页的 login 标签，这是 Angular 组件化要完成的任务。

创建一个 `hello-world` 组件：

```bash
$ ng generate component hello-world
installing component
  create src/app/hello-world/hello-world.component.css
  create src/app/hello-world/hello-world.component.html
  create src/app/hello-world/hello-world.component.spec.ts
  create src/app/hello-world/hello-world.component.ts
  update src/app/app.module.ts
```

创建组件要完成：

1. 完成 `Component` 注解
2. 实现组件的类定义


### 导入依赖模块

`src/app/hello-world/hello-world.component.ts` 的内容如下：

```typescript
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-hello-world',
  templateUrl: './hello-world.component.html',
  styleUrls: ['./hello-world.component.css']
})
export class HelloWorldComponent implements OnInit {

  constructor() { }

  ngOnInit() {
  }

}
```

`import { things } from wherever` 是模块导入，这里的 `{ things }` 称为解构 (destructing)。

### 组件注解 (Annotation)

代码如下：

```typescript
@Component({
  selector: 'app-hello-world',
  templateUrl: './hello-world.component.html',
  styleUrls: ['./hello-world.component.css']
})
export class HelloWorldComponent implements OnInit {
}
```


组件注解和 Python 里的装饰器类似，也是用 `@`。注解将 meta 数据加入到我们的代码中。本例中，当将 `@Component` 使用在 `HelloWorldComponent` 类上时，即将 `HelloWorldComponent` “装饰”为了一个组件。

在注解中，定义了组件的一些属性：

**selector**

`selector: 'app-hello-world'`: 定义该组件的标签，之后在 ng 应用中即可使用 `app-hello-world` 标签来引用该组件。它类似 CSS 选择子， XPath 或 JQuery 选择子。该属性指定了组件将使用哪个 DOM 元素。

**templateUrl**

 `templateUrl`: 指定该组件的模板文件，也可以用 `template` 属性代替，此时是将模板内容直接写出来，如：

 ```typescript
 @Component({
    selector: 'app-hello-world',
    template: `
        <p>
        hello-world works inline!
        </p>
    `
 })
 ```

 ES6 中能使用 '\`' 来包围多行字符串。

**styleUrls**

指定该组件的样式文件，ng2 采用一种称为 **style encapsulation** 的理念，从而使特定样式只应用于特定组件。

### 使用组件

要使用组件，需要将组件标签添加到已经呈现的模板中，即 `src/app/app.component.html` 中，修改如下：

```html
{% raw %}
<h1>
  {{title}}

  <app-hello-world></app-hello-world>
</h1>
{% endraw %}
```

现在刷新浏览器即可看到更新。


## 将数据添加到组件中

假设有一组用户，需要显示他们的名字。在显示整个列表前，先显示单个用户。故先创建一个新组件来显示用户名字：

```bash
$ ng generate component user-item

  create src/app/user-item/user-item.component.css
  create src/app/user-item/user-item.component.html
  create src/app/user-item/user-item.component.spec.ts
  create src/app/user-item/user-item.component.ts
  update src/app/app.module.ts
```

要使 `UserItemComponent` 组件显示用户名字，需为该组件引入一个新的属性 `name`，引入属性（变量）后，该组件即可被用于其他用户。

要引入 name 属性，需在 `UserItemComponent` 类中定义一个 name 局部变量：

```typescript
export class UserItemComponent implements OnInit {
    name: string; // added name property

    constructor(){
        this.name = 'Felipe';
    }

    ngOnInit(){
    }
}
```

定义含类型的类属性是 ES6 中的特性，这里属性 name 被定义为 string 类型。而 `constructor` 函数是该类的构造函数，它在类初始化时调用。

### 呈现模板

模板内容修改如下：

```html
{% raw %}
<p>
  Hello {{ name }}
</p>
{% endraw %}
```

这里的 `{%raw%}{{ name }}{%endraw%}` 的语法和 Django 模板内的语法类似，也是用于显示变量值，这里的称为 **template tags** 或 **mustache tags**，中间的 name 部分也可以是一个表达式。由于模板绑定到组件，因此本例中将显示组件的变量 name, 即值为 'Felipe'。


### 使用 UserItemComponent 组件

将组件添加入 `src/app/app.component.html`，刷新浏览器即可看到效果：

```html
{% raw %}
<h1>
  {{title}}

  <app-hello-world></app-hello-world>
  <app-user-item></app-user-item>

</h1>
{% endraw %}
```

## 使用数组来显示用户组

ng2 中的 `*ngFor` 指令可以循环重复创建多个标签。

先创建一个新组件：

```bash
$ ng generate component user-list
```

将 `app.component.html` 中的 app-user-item 替换成 app-user-list：

```html
{% raw %}
<h1>
  {{title}}

  <app-hello-world></app-hello-world>
  <app-user-list></app-user-list>

</h1>
{% endraw %}
```

在 `app/user-list/user-list.component.ts` 中为 UserListComponent 添加 names 属性，该属性类型是字符串数组：

```typescript
export class UserListComponent implements OnInit {
  names: string[];

  constructor() { 
    this.names = ['Ari', 'Carlos', 'Felip', 'Nate'];
  }

  ngOnInit() {
  }

}
```

修改模板 `src/app/user-list/user-list.component.html`，循环遍历组件的 names 属性：

```html
{% raw %}
<ul>
  <li *ngFor="let name of names">Hello {{ name }}</li>
</ul>
{% endraw %}
```

`*ngFor*` 语法中的 ngFor 指令，它类似 Python 中的 `for name in names`，遍历 names 变量，然后将每个值赋给一个新的临时变量 name。ngFor 是在整个标签上循环的，即在本例中，将生成多个 li 标签。

现在刷新浏览器即可看到修改效果。

## 利用 User Item 组件

User List 组件通过 User Item 组件来显示每个用户的信息。

User List 的模板 `src/app/user-list/user-list.component.html`:

```html
<ul>
  <app-user-item 
    *ngFor="let name of names">
  </app-user-item>
</ul>
```

但是现在 User Item 组件还不能接收 User List 中的每个用户名，故显示的用户名字都是 "Felip"。我们需要有将数据传入子组件的机制，而这是通过 `@Input` 注释（装饰器）来实现的。

## 接收输入

在组件的类定义中，任何加有 `@Input` 注释的属性都为可接收输入的属性。将 User Item 组件的 name 属性设置为可接收输入：

`src/app/user-item/user-item.component.ts`: 

```typescript
import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-user-item',
  templateUrl: './user-item.component.html',
  styleUrls: ['./user-item.component.css']
})
export class UserItemComponent implements OnInit {
  @Input() name: string;

  constructor() {
  }

  ngOnInit() {
  }

}
```

### 向子组件传入数据

在模板中使用 `[]` 语法来向子组件传入数据。

`src/app/user-list/user-list.component.html`: 

```html
<ul>
  <app-user-item 
    *ngFor="let name of names"
    [name]="name">
  </app-user-item>
</ul>
```

用 `[name]` 来表示将值赋给子组件的该属性，用 `[]` 表示法和 Python、JavaScript 的属性访问符类似。语法右边字符串中的是要传入的变量。

现在，示例程序可以显示用户列表的信息了。

# ng2 应用的启动过程

所有应用都有一个主入口。应用的构建由 `angular-cli` 完成，而 `angular-cli` 基于 webpack实现。

当运行 `ng serve` 时，ng 会在 `angular-cli.json` 中查找应用的主入口，例如在本例中：

+ angular-cli.json 中指定了一个 "main" 文件，即 main.ts
+ main.ts 即是该应用的主入口，由它启动应用
+ 启动过程会启动一个 Angular 模块（Angular module）
+ 本例中，该启动模块为 AppModule，它在 `src/app/app.module.ts` 中指定
+ AppModule 指定了哪个组件用作顶层组件，本例中是 AppComponent
+ 本例中 AppComponent 模板中加入了 app-user-list 标签，因而可显示用户列表信息


Angular 也有模块的概念。当启动一个应用时，我们不是直接启动一个组件，而是创建一个 `NgModule`，由该 NgModule 指向我们要加载的组件。

`src/app/app.module.ts` 代码如下：

```typescript
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';

import { AppComponent } from './app.component';
import { HelloWorldComponent } from './hello-world/hello-world.component';
import { UserItemComponent } from './user-item/user-item.component';
import { UserListComponent } from './user-list/user-list.component';

@NgModule({
  declarations: [ // 指定了本模块中定义了的组件，它们在 "ng generate component" 时自动添加到此，只有在 NgModule 中声明了的组件才能在模板中使用
    AppComponent,
    HelloWorldComponent,
    UserItemComponent,
    UserListComponent
  ],
  imports: [ // 指定本模板的依赖模块
    BrowserModule,
    FormsModule,
    HttpModule
  ],
  providers: [],
  bootstrap: [AppComponent] //启动组件，即将 AppComponent 作为顶层组件
})
export class AppModule { }
```

可见，`@NgModule` 也是一个注释，它将 meta 数据添加到紧跟它的类(AppModule) 中。

# 扩展我们的应用

实现一个 Simple Reddit 应用。

```bash
$ ng new angular2-reddit  # 创建新应用
```

## 添加 CSS

从 https://github.com/haiiiiiyun/ng-book2-r51-code 的 first_app/angular2_reddit 目录下复制以下文件到相应目录下。

本例的样式使用了 [Semantic-UI](http://semantic-ui.com/)，这也是一个 CSS 框架，和 [Zurb foundation](http://foundation.zurb.com/) 及 [Twitter Bootstrap](http://getbootstrap.com/) 类似。


## Application 组件

现创建一个新的组件来完成：

+ 存储当前的章列表
+ 包含一个能提交文章的表单


```html
<!--file: src/app/app.component.html
这是提交文档的表单，样式大都来自 semantic-ui 包
-->
<form class="ui large form segment">
  <h3 class="ui header">Add a Link</h3>

  <div class="field">
    <label for="title">Title:</label>
    <!--
    input 标签中，通过 #varname 使该标签对象 (HTMLInputElement 类型) 绑定到
    varname 局部变量， 而 input 的值可用 varname.value 获取
    -->
    <input name="title" #newtitle>
  </div>
  <div class="field">
    <label for="link">Link:</label>
    <input name="link" #newlink>
  </div>
  <!--
  将事件名用 () 括起来，来绑定事件响应。这里 button 的 click
  事件响应函数是本组件中的 addArticle 方法， addArticle 定义在当前组件的  ArticleComponet 类中 。
    回调函数中的 newtitle, newlink 等是从上面的输入域标签 resolve 过来的，如 resolve(#newtitle)。
  -->
  <button (click)="addArticle(newtitle, newlink)"
           class="ui positive right floated button">
    Submit link
  </button>
</form>
```

## 添加交互功能

```typescript
// file: src/app/app.component.ts
import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
    // 方法声明的格式为：
    // functionName(propertyName1: typeName, propertyName2: typeName): returnTypeName
    // 这些参数需要在响应事件时传入
    addArticle(title: HTMLInputElement, link: HTMLInputElement): boolean {
        console.log(`Adding article title: ${title.value} and link: ${link.value}`);
        return false;
    }
}
```

## 添加 Article 组件

```bash
$ ng generate component article # 创建一个新组件来表示每个提交的 Article

组件模板 src/app/article/article.component.html 定义如下，其效果为：

![单个 Article](/assets/images/ng-book2/reddit-article.png)

```html
{% raw %}
<!--
  CSS 类 four wide column 和 twelve wide column 都来自 Semantics UI。
  该模板中的 {{ votes }}, {{ link }} 等变量绑定到组件类 ArticleComponent 中的相应属性 votes 和 link
-->
<div class="four wide column center aligned votes">
  <div class="ui statistic">
    <div class="value">
      {{ votes }}
    </div>
    <div class="label">
      Points
    </div>
  </div>
</div>

<div class="twelve wide column">
  <a class="ui large heaer" href="{{ link }}">
    {{ title }}
  </a>
  <!--
    绑定的回调函数 voteUp, voteDown 也是在组件类 ArticleComponent 中定义
  -->
  <ul class="ui big horizontal list voters">
    <li class="item">
      <a href (click)="voteUp()">
        <i class="arrow up icon"></i>
        upvote
      </a>
    </li>
    <li class="item">
      <a href (click)="voteDown()">
        <i class="arrow down icon"></i>
        downvote
      </a>
    </li>
  </ul>
</div>
{% endraw %}
```

组件类定义 src/app/article/article.component.ts:

```typescript
/*
 * host 就是代表当前组件关联到的元素。这里设置在
 * 每个 app-article 标签上都加个 'row' 类。通过 host，
 * 我们可以在组件内对元素标签进行配置
 */
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-article',
  templateUrl: './article.component.html',
  styleUrls: ['./article.component.css']
  host: {
      class: 'row'
  }
})
export class ArticleComponent implements OnInit {
  // 这些属性可以在组件模板中引用
  votes: number;
  title: string;
  link: string;


  constructor() {
      this.title = 'Angular 2';
      this.link = 'http://angular.io';
      this.votes = 10;
  }

  // 这些函数可以在组件模板中引用
  voteUp() {
      this.votes += 1;
  }

  voteDown() {
      this.votes -= 1;
  }

  ngOnInit() {
  }

}
```

这里每个 Article 自成一行，使用了 [Semantic UI 的 row 类](https://semantic-ui.com/collections/grid.html)。


## 使用 app-article 组件

在 AppComponent 模板的 form 下添加 app-article 标签：

```html
<!-- file: src/app/app.component.html -->
<!-- form ... -->

<div class="ui grid posts">
  <app-article>
  </app-article>
</div>
```

现在可以正常显示 Article 了，但是当点击 upvote, downvote 时浏览器会进行刷新加载。这是因为 Javascript 默认会将 click 事件向上传递给所有的父元素，因此当该空链接传递到父链接后，浏览器会进行加载。要改正这种行为，只需使 click 回调函数返回 false 即可，它使 JavaScript 不再向上传递 click 事件。

修改后的回调函数为：

```typeScript
  voteUp(): boolean {
      this.votes += 1;
      return false;
  }

  voteDown(): boolean {
      this.votes -= 1;
      return false;
  }
```


## 显示多行 Article

### 创建 Article 数据结构类

Angular 代码的最佳实践是将数据结构与组件代码进行分离。因此现创建一个代表单个 Article 的数据结构类：

```typeScript
// file src/app/article/article.model.ts
export class Article {
    title: string;
    link: string;
    votes: number;

    // 参数 votes? 表示是可选的
    constructor(title: string, link: string, votes?: number){
        this.title = title;
        this.link = link;
        this.votes = votes || 0;
    }

    voteUp(): void {
        this.votes += 1;
    }

    voteDown(): void {
        this.votes -= 1;
    }

    domain(): string {
        try {
            const link: string = this.link.split('//')[1];
            return link.split('/')[0];
        } catch(err){
            return null;
        }
    }
}
```

这是一个普通的类，非 Angular 组件，在 MVC 模式中，这是一个 Model。

更新 ArticleComponent 代码，使用 Article 类来存储属性：

```typeScript
// file: src/article/article.component.ts
/*
 * host 就是代表当前组件关联到的元素。这里设置将
 * 每个 app-article 标签上都加个 'row' 类。通过 host，
 * 我们可以在组件内对元素标签进行配置
 */
import { Component, OnInit } from '@angular/core';
import { Article } from './article.model.ts';

@Component({
  selector: 'app-article',
  templateUrl: './article.component.html',
  styleUrls: ['./article.component.css']
  host: {
      class: 'row'
  }
})
export class ArticleComponent implements OnInit {
  // 这些属性可以在组件模板中引用
  article: Article;

  constructor() {
      this.article = new Article(
          'Angular 2',
          'http://angular.io',
          10
      );
  }

  // 这些函数可以在组件模板中引用
  voteUp(): boolean {
      this.article.voteUp();
      return false;
  }

  voteDown(): boolean {
      this.article.voteDown();
      return false;
  }

  ngOnInit() {
  }

}
```

同时，更新 Article 组件模板中的引用绑定，如从 `votes` 更新为 `article.votes` 等。


## 显示多个 Article

```typescript
// file: src/app/app.component.ts
import { Component } from '@angular/core';
import { Article } from './article/article.model.ts';
//...
export class AppComponent {
    // 将 articles 定义为 Article 的数组，
    // 也可以写成 articles: Array<Article>
    articles: Article[];

    constructor(){
        this.articles = [
            new Article('Angular 2', 'http://angular.io', 3),
            new Article('Fullstack', 'http://fullstack.io', 2),
            new Article('Angular Homepage', 'http://angular.io', 1)
        ];
    }

    // 方法声明的格式为：
    // functionName(propertyName1: typeName, propertyName2: typeName): returnTypeName
    // 这些参数需要在响应事件时传入
    addArticle(title: HTMLInputElement, link: HTMLInputElement): boolean {
        // 这里又用 ` 来包围字符串，在 ES6 中，这种字符串能扩展里面的变量值
        console.log(`Adding article title: ${title.value} and link: ${link.value}`);
        return false;
    }
}
```

将 AppComponent 中的 article 数据模型传入 ArticleComponent，需要定义 @Input 参数。如：

```typescript
// file: src/article/article.component.ts
/*
 * host 就是代表当前组件关联到的元素。这里设置将
 * 每个 app-article 标签上都加个 'row' 类。通过 host，
 * 我们可以在组件内对元素标签进行配置
 */
import { Component, OnInit, Input } from '@angular/core';
import { Article } from './article.model.ts';

@Component({
  selector: 'app-article',
  templateUrl: './article.component.html',
  styleUrls: ['./article.component.css']
  host: {
      class: 'row'
  }
})
export class ArticleComponent implements OnInit {
  // 这些属性可以在组件模板中引用
  @Input() article: Article;

  // 这些函数可以在组件模板中引用
  voteUp(): boolean {
      this.article.voteUp();
      return false;
  }

  voteDown(): boolean {
      this.article.voteDown();
      return false;
  }

  ngOnInit() {
  }

}
```

然后在模板中：

```html
<app-article [article]="article1"></app-article>
<app-article [article]="article2"></app-article>
```

更新 AppComponent 模板：

```html
<!-- file: src/app/app.component.html-->
<!--
  articles 是定义在 AppComponent 中的 Article 数组，
  anarticle 是由 NgFor 创建的局部变量，
  [article] 是 ArticleComponent 中的 Input 参数
-->
<div class="ui grid posts">
  <app-article
    *ngFor="let anarticle of articles"
    [article]="anarticle">
  </app-article>
</div>
```

刷新浏览器后，可看到可以显示多个 Article 了。

## 添加新的 Article

更新 AppComponent 中的 addArticle:

```typescript
// file: src/app/app.component.ts
//...
    addArticle(title: HTMLInputElement, link: HTMLInputElement): boolean {
        // 这里又用 ` 来包围字符串，在 ES6 中，这种字符串能扩展里面的变量值
        console.log(`Adding article title: ${title.value} and link: ${link.value}`);
        this.articles.push(new Article(title.value, link.value, 0));

        // 值清空后，其绑定的 Input 标签上的值也会清空
        title.value = '';
        link.value = '';
        return false;
    }
```

## 显示链接的域名

在 Article Model 中定义链接域名提取函数：

```typescript
// file: src/article/article.model.ts
//...

    domain(): string {
        try {
            const link: string = this.link.split('//')[1];
            return link.split('/')[0];
        } catch(err){
            return null;
        }
    }
```

然后在 ArticleComponent 模板中调用：

```html
  <div class="meta">({{ article.domain() }})</div>
  <ul class="ui big horizontal list voters">
```

## 基于分数排序 Article

在 AppComponent 中定义排序函数：

```typescript
// file: src/app/app.component.ts
    sortedArticles(): Article[] {
        return this.articles.sort((a: Article, b: Article) => b.votes - a.votes);
    }
```

并在 AppComponent 模板中调用 sortedArticles():

```html
<!--file: src/app/app.component.html -->
<div class="ui grid posts">
  <app-article
    *ngFor="let anarticle of sortedArticles()"
    [article]="anarticle">
  </app-article>
</div>
```


# 总结

大部分 Angular 应用开发步骤为：

+ 将应用分解为组件
+ 创建视图
+ 定义数据模型
+ 显示数据模型
+ 添加交互


# 参考 

+ [Writing your first Angular 2 Web Application](https://www.ng-book.com/2/)
+ [Step 1. Set up the Development Environment](https://angular.io/docs/ts/latest/cli-quickstart.html#!#devenv)
