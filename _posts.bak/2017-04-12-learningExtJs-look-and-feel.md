---
title: ExtJS 的外观定制--Learning ExtJS(4th)
date: 2017-04-12
writing-time: 2017-04-12 09:02--14:27
categories: Programming
tags: Programming 《Learning&nbsp;ExtJS&nbsp;4th&nbsp;Edition》 Sencha ExtJS Javascript
---

自 Ext JS 4 开始，可以针对全局或单个组件修改颜色、渐变、字体等主题元素。

Ext JS 使用 [SASS](http://sass-lang.com/) (一个 CSS 扩展) 和 [COMPASS](http://compass-style.org) ( 一个 SASS 框架，基于 Ruby) 来处理样式。

先安装：

```bash
$ sudo apt-get install ruby-dev
$ sudo gem install compass
$ ruby -v
ruby 2.3.1p112 (2016-04-26) [i386-linux-gnu]

$ compass -v
Compass 1.0.3 (Polaris)
Copyright (c) 2008-2017 Chris Eppstein
Released under the MIT License.
Compass is charityware.
Please make a tax deductable donation for a worthy cause: http://umdf.org/compass

$ sass -v
Sass 3.4.23 (Selective Steve)
```

# 主题文件目录

主题风格和类相似，具有层级（继承）结构。

![主题风格层级结构](/assets/images/learningextjs4th/theme_hierarchy.png)

Neptune 扩展至 Neutral，而自定义风格通常扩展至 Neptune 和 Classic。

## 创建自定义主题

```bash
# 命令为:
# sencha –sdk [path to SDK] generate theme –extend ext-theme-neptune mycustom-theme

$ cd myapp

# sdk 指向项目目录中的 ext 目录，
# 命令完成后会在 ext/packages/ 下创建了一个 my-custome-theme
$ sencha –sdk ext generate theme –extend ext-theme-neptune my-custom-theme
```

修改项目目录下的 `app.json` 文件，更新为使用自定义主题：

```json
"theme": "my-custome-theme",
```

## 修改主题变量值

自定义主题中定义的变量值会覆盖父主题上的相应变量。有 2 种变量：

+ 全局变量，作为于整个主题。
+ 针对某类组件的变量：如 Ext.panel.Panel 上的变量。


创建全局变量：

```bash
#先切换到 `ext/packages/my-custome-theme/sass/var/` 目录
$ cd ext/packages/my-custome-theme/sass/var/

#创建文件 Component.scss
$ touch Component.scss
```

加入内容：

```scss
/* file: ext/packages/my-custome-theme/sass/var/Component.scss */
/* My Custom Theme SCSS Component file */
$color: #6d6d6d !default; /*theme font/text color */
$base-color: #0d7179 !default; /*all component color base */
```

构建新的主题：

```bash
# 回到自定义主题的根目录
$ cd ext/packages/my-custome-theme/
$ sencha package build # 会在自定义主题根目录下创建一个 build 目录
```

现在可以看到自定义主题已经生效了。


# 主题高级定制

## 修改组件风格

例如要修改 Ext.toolbar.Toolbar 的风格。注意文件的层级结构，Ext 对应 ext/packages/sass/var，toolbar 对应 toolbar 目录，而 Toolbar 对应最终文件 Toolbar.scss：

```bash
$ mkdir scss/var/toolbar
$ touch scss/var/toolbar/Toolbar.scss
```

内容为：

```scss
$toolbar-background-color: rgba(188,188,188,1);
$toolbar-background-gradient: recessed;
```

## 添加新的渐变效果

Ext 已经内置有 matte, glossy, bevel, recessed 等效果。

添加新的渐变：

1. 在文件 `ext/packages/my-custom-theme/sass/etc/all.scss` 中加入：

```scss
@import 'mixins'; /* 导入 mixins.scss 文件 */
```

2. 创建文件 `ext/packages/my-custom-theme/sass/etc/mixins.scss` 文件，内容为：

```scss
/* 导入 mixins/background-gradient.scss 文件 */
@import 'mixins/background-gradient'; 
```

3. 创建文件 `ext/packages/my-custom-theme/sass/etc/mixins/background-gradient.scss` 文件，内容为：

```scss
@function linear-gradient-recessed ($direction, $bg-color) {
    @return linear-gradient(left, color_stops(#fbb040, #cccccc));
}
```

3. 将 `ext/packages/my-custom-theme/sass/var/toolbar/Toolbar.scss` 内容改为：

```scss
/*$toolbar-background-color: rgba(188,188,188,1); */
$toolbar-background-gradient: recessed;
```

重新编译主题后可看到工具栏中的 recessed 的渐变已经被我们定义的覆盖了。


## 修改 Tab 的风格

`Ext.tab.Tab` 对应的主题文件是 `ext/packages/my-custom-theme/sass/var/tab/Tab.scss`。

内容为：

```sass
/* Tab Custom style for my-custom-theme */
$tab-base-color: #65a9e0; /* Tab 普通情况下的基本色(背景色) */
$tab-base-color-active: #c5c5c5; /* 激活情况下的背景色 */
$tab-base-color-disabled: #597179; /* 禁用情况下的背景色 */
$tab-color-active: #333333; /* 激活情况下的文本色 */
```

## 添加自定义字体

获取字体的常用网站有 [Google Fonts] 和 [FONT Squirrel](https://www.fontsquirrel.com/fonts/open-sans)。

在 FONT Squirrel 的 OPEN SANS 页上下载 @FONT-FACE KIT，里面包含字体文件及相关的 CSS 文件。在 `ext/packages/my-custom-theme/resources/` 下创建目录 `fonts/open-sans`，并将下载下来的压缩包中的 web fonts/opensans_regular_macroman 目录下的文件复制到 open-sans 目录。

将复制来的文件 stylesheet.css 中的内容复制到 `ext/packages/my-custom-theme/sass/var/Component.scss`，修改相对路径并添加 `$font-family: open_sansregular;`，如下：

```scss
/* file: ext/packages/my-custome-theme/sass/var/Component.scss */
/* My Custom Theme SCSS Component file */

@font-face {
    font-family: 'open_sansregular';
    src: url('../resources/fonts/open-sans/OpenSans-Regular-webfont.eot');
    src: url('../resources/fonts/open-sans/OpenSans-Regular-webfont.eot?#iefix') format('embedded-opentype'),
         url('../resources/fonts/open-sans/OpenSans-Regular-webfont.woff') format('woff'),
         url('../resources/fonts/open-sans/OpenSans-Regular-webfont.ttf') format('truetype'),
         url('../resources/fonts/open-sans/OpenSans-Regular-webfont.svg#open_sansregular') format('svg');
    font-weight: normal;
    font-style: normal;

}

$font-family: 'open_sansregular';
$color: #6d6d6d !default; /*theme font/text color */
$base-color: #0d7179 !default; /*all component color base */
```

## 相同组件呈现不同风格

Ext 的每个组件都有 'ui' 属性，用来为 CSS 类添加前缀。

假设定义了一个 Panel 如下：

```javascript
{
    xtype: 'panel',
    ui: 'featuredpanel',
    frame: true,
    height: 200,
    margin: '0px 5px 0px 5px',
    title: 'Featured',
    bodyPadding: 4,
    html: 'Place contents for FEATURED zone',
    tools: [
        {
            xtype: 'tool',
            type: 'prev'
        },{
            xtype: 'tool',
            type: 'next'
        }
    ]
}
```

为 `Ext.panel.Panel` 创建自定义 ui 风格，先在 `ext/packages/my-custom-theme/sass/src` 目录下创建 `panel` 目录，并创建文件 `Panel.scss`，内容如下：

```scss
/* 应用于 ui: 'featuredpanel' 的 panel */
@include extjs-panel-ui(
    $ui:'featuredpanel',
    $ui-header-background-color: #5e1b5e,
    $ui-border-color: #5e1b5e,
    $ui-header-border-color: #5e1b5e,
    $ui-body-border-color: #5e1b5e
);

/* 应用于 ui: 'featuredpanel' 及 frame: true 的 panel */
@include extjs-panel-ui(
    $ui:'featuredpanel-framed',
    $ui-header-background-color: #5e1b5e,
    $ui-border-color: #5e1b5e,
    $ui-header-border-color: #5e1b5e,
    $ui-body-border-color: #5e1b5e,
    $ui-border-width: 5px,
    $ui-border-radius: 4px
);
```

重新构建主题后，可看到由于例子中的 Panel 设置了 `ui: 'featuredpanel', frame: true,`，应用了 'featuredpanel-framed' 中的风格。


## 支持 IE8 等老浏览器

由于 IE8 等老浏览器不支持 CSS 3，Ext 可以为这些浏览器生成效果图片，从而实现 CSS 3 类似的效果。

打开文件 `ext/packages/my-custom-theme/sass/example/custom.js`，加入以下内容：

```javascript
Ext.theme.addManifest(
    {
        xtype: 'widget.panel',
        ui: 'featuredpanel'
    },
    {
        xtype: 'widget.panel',
        ui: 'newspanel'
    },
    {
        xtype: 'widget.panel',
        ui: 'tipspanel'
    }
);
```

以告诉 Ext 为哪些自定义风格生成效果图片，运行 `sencha package build` 后，会在 `ext/packages/my-custom-theme/build/resoures/images/panel/` 下生成多个效果图片。

要将加载这些资源文件，需重构应用：

```bash
$ sencha app build development # or
$ sencha app build production
```

之后在 IE8 中可以看到，圆角等 CSS 3 的特性都能实现了。



# 参考 

+ [Chapter11: The Look and Feel](https://www.amazon.com/Learning-ExtJS-Fourth-Carlos-Mendez/dp/1784394386/)
