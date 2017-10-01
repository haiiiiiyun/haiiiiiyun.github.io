---
title: Angular docs-模板与数据绑定-动态组件加载器
date: 2017-10-01
writing-time: 2017-10-01
categories: programming
tags: angular node Angular&nbsp;docs
---


使用 `ComponentFactoryResolver` 来动态加入组件。


## 定位指令

实现一个辅助定位指令，来标记动态组件的插入位置。

```typescript
//src/app/ad.directive.ts
import { Directive, ViewContainerRef } from '@angular/core';

@Directive({
  selector: '[ad-host]',
})
export class AdDirective {
  constructor(public viewContainerRef: ViewContainerRef) { }
}
```

`AdDirective` 注入 `ViewContainerRef` 来获取元素的视图容器，即放置动态加载组件的元素。


## 加载组件

```typescript
//src/app/ad-banner.component.ts (template)
template: `
            <div class="ad-banner">
              <h3>Advertisements</h3>
              <ng-template ad-host></ng-template>
            </div>
          `
```

将 AdDirective 指令应用到 `<ng-template>` 元素，从而动态加载的组件都会在该元素内。`<ng-template>` 元素最适合作为容器，因它不呈现额外内容。

## 解析组件

```typescript
//src/app/ad-banner.component.ts (excerpt)
export class AdBannerComponent implements AfterViewInit, OnDestroy {
  @Input() ads: AdItem[];
  currentAddIndex: number = -1;
  @ViewChild(AdDirective) adHost: AdDirective;
  subscription: any;
  interval: any;

  constructor(private componentFactoryResolver: ComponentFactoryResolver) { }

  ngAfterViewInit() {
    this.loadComponent();
    this.getAds();
  }

  ngOnDestroy() {
    clearInterval(this.interval);
  }

  loadComponent() {
    this.currentAddIndex = (this.currentAddIndex + 1) % this.ads.length;
    let adItem = this.ads[this.currentAddIndex];

    let componentFactory = this.componentFactoryResolver.resolveComponentFactory(adItem.component);

    let viewContainerRef = this.adHost.viewContainerRef;
    viewContainerRef.clear();

    let componentRef = viewContainerRef.createComponent(componentFactory);
    (<AdComponent>componentRef.instance).data = adItem.data;
  }

  getAds() {
    this.interval = setInterval(() => {
      this.loadComponent();
    }, 3000);
  }
}
```

## 参考

+ https://angular.io/guide/dynamic-component-loader
+ [对应的 jupyter notebook](https://github.com/haiiiiiyun/angular-docs-notebook/blob/master/template_data_binding_dynamic_component_loader.ipynb)
