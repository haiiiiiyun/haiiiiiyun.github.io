---
title: 编写首个 Angular2 应用
date: 2017-02-21
writing-time: 2017-02-21 22:29
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

由于开发 ng 项目时有时会构建一些 Node 的本地 add，一般还要安装 [node-gyp](https://www.npmjs.com/package/node-gyp) ：

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

在 OSX 或 Linux 运行一般会有 'Could not start watchman ...' 的输出，这是因为我们还没有安装 [watchman](https://ember-cli.com/user-guide/#watchman)，该程序能帮助 angular-cli 监测项目中的文件修改情况。如果在 OSX 上，最好通过 Homebrew 安装它：

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
+ `.editorconfig`: 编辑器的通用配置文件，大多数编辑都支持加载 .editorconfig 中的配置项，见 http://editorconfig.org
+ `angular-cli.json`: Angular-CLI 的配置信息。可以设置一些默认值，也可配置当构建项目时要包含的文件
+ `karma.conf.js`: [Karma test runner](https://karma-runner.github.io/) 单元测试的配置文件，当运行 `ng test` 时会用到
+ `package.json`: npm 将项目的依赖包记录在该文件中。也可以在文件内添加 [自定义的脚本](https://docs.npmjs.com/misc/scripts)
+ `protractor.conf.js`: [Protractor](http://www.protractortest.org/) 的 e2e 测试配置文件，当运行 `ng e2e` 时使用
+ `tslint.json`: 有关 [TSLint](https://palantir.github.io/tslint/) 和 [Codelyzer](http://codelyzer.com/) 的配置文件，当运行 `ng lint` 时使用


而源代码目录里包含了 Angular 的所有组件，模板，样式，图片，及项目所需的其它所有内容。项目结构如下：

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

+ `app/app.component.{ts,html,css,spec.ts}`: 定义 `AppComponent` 及其 HTML 模板，CSS 样式和单元测试。这是 ng 项目中的组件树中的根组件。
+ `app/app.module.ts`: 定义 `AppModule`, 该根模块能告诉 Angular 如何组装应用。新建项目后，该文件中只有一个 `AppComponent`，但是之后自定义的组件也要加到该文件中。
+ `assets/*`: 保存图片等文件，该目录中的内容在应用构建时会原样复制。
+ `environments/*`: 每个目标环境都对应一个配置文件，如开发环境、和生产环境等。
+ `indext.html`: 主 HTML 页。通常无需对它手动编辑，CLI 在应用构建过程中会自动将所需的 js 和 css 文件链接添加进去。
+ `main.ts`: 这是应用的主入口点。[JIT 编译器](https://angular.io/docs/ts/latest/glossary.html#jit) 对它编译后，再在浏览器中启动应用的根模块 (AppModule) 运行。也可以用 [AoT 编译器](https://angular.io/docs/ts/latest/glossary.html#ahead-of-time-aot-compilation) 进行编译，只需在运行 `ng build` 或 `ng serve` 时传入 `--aot` 参数即可。
+ `polyfills.ts`: 不同的浏览器对标准的支持不同，而该文件就是用来磨平这些区别的。在使用 `core-js` 和 `zone.js` 需当时，更多信息见 [Browser Support guide](https://angular.io/docs/ts/latest/guide/browser-support.html)。
+ `styles.css`: 全局的样式放这里。通常为便于维护，自定义的组件的样式都放在其定义目录中。
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

瑞可以在浏览器里通过 `http://localhost:4200` 访问应用了。

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
...
```

组件注解和 Python 里的装饰器类似，也是用 `@`。注解将 meta 数据加入到我们的代码中。本例中，当将 `@Component` 使用在 `HelloWorldComponent` 类上时，即将 `HelloWorldComponent` “装饰”为了一个组件。

在注解中，定义了组件的一些属性：

**selector**

`selector: 'app-hello-world'`: 定义该组件的标签，之后在 ng 应用中即可使用 `app-hello-world` 标签来引用该组件。类似 CSS 选择子， XPath 或 JQuery 选择子。该属性指定了组件将使用哪个 DOM 元素。

**templateUrl**

 `templateUrl`: 指定该组件的模板文件，也可以用 `template` 属性将代替，此时是将模板内容直接写出来，如：

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

指定该组件的样式文件，ng2 采用一种称为 **style=encapsulation** 的理念，从而使特定的样式只应用于特定的组件。

### 使用组件

要使用组件，需要将组件标签添加到已经呈现的模板中，即 `src/app/app.component.html` 中，修改如下：

```html
<h1>
  {{title}}

  <app-hello-world></app-hello-world>
</h1>
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

要实现 `UserItemComponent` 组件显示用户名字，则需为该组件引入一个新的属性 `name`，引入属性（变量）后，该组件即可被用于其他用户。

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

定义含类型的类属性是 ES5 中的特性，这里属性 name 被定义为 string 类型。而 `constructor` 函数是该类的构建函数，在类初始化时调用。

### 呈现模板

模板内容修改如下：

```html
<p>
  Hello {{ name }}
</p>
```

这里的 `{{ name }}` 的语法和 Django 模板内的语法类似，也是用于显示变量值，这里的称为 **template tags** 或 **mustache tags**，中间的 name 部分也可以是一个表达式。由于模板绑定到组件，因此本例中将显示组件的变量 name, 即值为 'Felipe'。


### 使用 UserItemComponent 组件

将组件添加入 `src/app/app.component.html`，刷新浏览器即可看到效果：

```html
<h1>
  {{title}}

  <app-hello-world></app-hello-world>

  <app-user-item></app-user-item>

</h1>
```

## 使用数组来显示用户组

ng2 中的 `*ngFor` 指令可以循环重复创建多个标签。

先创建一个新组件：

```bash
$ ng generate component user-list
```

将 `app.component.html` 中的 app-user-item 替换成 app-user-list：

```html
<h1>
  {{title}}

  <app-hello-world></app-hello-world>

  <app-user-list></app-user-list>

</h1>
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
<ul>
  <li *ngFor="let name of names">Hello {{ name }}</li>
</ul>
```

`*ngFor*` 语法开始使用 ngFor 指令，它类似 Python 中的 `for name in names`，遍历 names 变量，然后将每个值赋给一个新的临时变量 name。ngFor 是在整个标签上循环的，即要本例中，将生成多个 li 标签。

现在刷新浏览器即可看到修改效果。

## 利用 User Item 组件

在 User List 组件通过 User Item 组件来显示每个用户的信息。

先在 UserListComponent 

续..












# 参考 

+ [Writing your first Angular 2 Web Application](https://www.ng-book.com/2/)
+ [Step 1. Set up the Development Environment](https://angular.io/docs/ts/latest/cli-quickstart.html#!#devenv)
