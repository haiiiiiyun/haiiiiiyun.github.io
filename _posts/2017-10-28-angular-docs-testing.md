---
title: Angular docs-测试
date: 2017-10-28
writing-time: 2017-10-25:2017-10-28
categories: programming
tags: angular node Angular&nbsp;docs
---

# 测试

## 工具和技术

技术 | 目的
Jasmine | [Jasmine 框架](http://jasmine.github.io/2.4/introduction.html) 可用来写基本测试，提供了在浏览器中运行测试的工具。
Angular 测试工作 | 可为测试创建 Angular 环境。
Karma | [karma test runner](https://karma-runner.github.io/1.0/index.html) 适于在开发时编写和测试。可集成到开发过程和持续集成过程中。
Protractor | 用来编写和运行 end-to-end(e2e) 测试。在 e2e 测试时，一个进程开启应用，另一个进行模块用户进行操作。


### 隔离的单元测试与 Angular 测试工具

适用于对管道和服务进行测试。而组件类通常与环境交互，通常要通过 `TestBed` 创建 Angular 测试环境。

## 首个 karma 测试

用 Jasmine 写的测试叫 *specs*，文件扩展名为 `.spec.ts`，例如：

```typescript
//src/app/1st.spec.ts
describe('1st tests', () => {
  it('true is true', () => expect(true).toBe(true));
});
```

在项目目录下运行：

```bash
npm test
```

## 测试内联模板的组件

测试文件和组件文件一般放在相同的目录下，例如 `src/app/banner-inline.component.ts` 对应 `src/app/banner-inline.component.spec.ts`

```typescript
//src/app/banner-inline.component.ts
import { Component } from '@angular/core';

@Component({
  selector: 'app-banner',
  template: '<h1>{{title}}</h1>'
})
export class BannerComponent {
  title = 'Test Tour of Heroes';
}
```

```typescript
//src/app/banner-inline.component.spec.ts
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { By }              from '@angular/platform-browser';
import { DebugElement }    from '@angular/core';

import { BannerComponent } from './banner-inline.component';

describe('BannerComponent (inline template)', () => {

  let comp:    BannerComponent;
  let fixture: ComponentFixture<BannerComponent>;
  let de:      DebugElement;
  let el:      HTMLElement;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ BannerComponent ], // declare the test component
    });

    fixture = TestBed.createComponent(BannerComponent);

    comp = fixture.componentInstance; // BannerComponent test instance

    // query for the title <h1> by CSS element selector
    de = fixture.debugElement.query(By.css('h1'));
    el = de.nativeElement;
  });
});
```

通过 `TestBed` 创建一个测试的 `@NgModule` 类，其 metadata 可以通过 `configureTestingModule` 方法来设置。从而创建一个与生产环境隔离的 Angular 测试环境。

`beforeEach` 方法用来定义每个测试运行前都要运行的任务。

`TestBed.createComponent()` 用来创建组件实例，并返回一个 `component test fixture`。`createComponent()` 方法调用后，`TestBed` 实例就不能再进行配置了。返回的 `component test fixture` 对象 `ComponentFixture` 实际上是一个被测试环境包围的组件实例，可从中抽取组件实例(`fixture.componentInstance` 和组件的 DOM 元素对象 (`fixture.DebugElement`)。

`DebugElement` 上使用 `query` 和 `queryAll` 方法来过滤获取相关元素。


```typescript
//src/app/banner-inline.component.spec.ts (tests)
it('should display original title', () => {
  fixture.detectChanges();
  expect(el.textContent).toContain(comp.title);
});

it('should display a different test title', () => {
  comp.title = 'Test Title';
  fixture.detectChanges();
  expect(el.textContent).toContain('Test Title');
});
```

`fixture.detectChanges()` 用来执行修改检测，即完成数据绑定等工作。生产环境下修改检测是自动触发的，而测试环境下一般需要手动触发。

### 自动触发

```typescript
//src/app/banner.component.detect-changes.spec.ts (import)
import { ComponentFixtureAutoDetect } from '@angular/core/testing';


//src/app/banner.component.detect-changes.spec.ts (AutoDetect)
TestBed.configureTestingModule({
  declarations: [ BannerComponent ],
  providers: [
    { provide: ComponentFixtureAutoDetect, useValue: true }
  ]
})

//src/app/banner.component.detect-changes.spec.ts (AutoDetect Tests)
it('should display original title', () => {
  // Hooray! No `fixture.detectChanges()` needed
  expect(el.textContent).toContain(comp.title);
});

it('should still see original title after comp.title change', () => {
  const oldTitle = comp.title;
  comp.title = 'Test Title';
  // Displayed title is old because Angular didn't hear the change :(
  expect(el.textContent).toContain(oldTitle);
});

it('should display updated title after detectChanges', () => {
  comp.title = 'Test Title';
  fixture.detectChanges(); // detect changes explicitly
  expect(el.textContent).toContain(comp.title);
});
```

这种自动触发也只由异步事件（如 promise resolution, timers, DOM events) 等触发，而同步的属性修改不能触发，还是要通过 `detectChagnes()` 手动触发。


## 测试有外部模板文件的组件

### 首个异步 beforeEach

需要 2 个 beforeEach，第 1 个使用异步方式，使 Angular 模板编译器有时间读取文件：

```typescript
//src/app/banner.component.spec.ts (first beforeEach)
import { async } from '@angular/core/testing';

// async beforeEach
beforeEach(async(() => {
  TestBed.configureTestingModule({
    declarations: [ BannerComponent ], // declare the test component
  })
  .compileComponents();  // compile template and css
}));
```

`async()` 将作为其参数的任务安排到一个特殊的 `async test zone` 中执行。TestBed 调用异步操作 `compileComponents()` 后就不能再进行配置了。


## 测试有依赖的组件

为依赖的服务创建替身，注入时不直接注入原来的服务，通过 `useValue` 注入该替身：

```typescript
//src/app/welcome.component.spec.ts
userServiceStub = {
  isLoggedIn: true,
  user: { name: 'Test User'}
};

//src/app/welcome.component.spec.ts
TestBed.configureTestingModule({
   declarations: [ WelcomeComponent ],
// providers:    [ UserService ]  // NO! Don't provide the real service!
                                  // Provide a test-double instead
   providers:    [ {provide: UserService, useValue: userServiceStub } ]
});
```

获取注入服务对象的最安全方式是通过组件上的注入器获取：

```typescript
//WelcomeComponent's injector
// UserService actually injected into the component
userService = fixture.debugElement.injector.get(UserService);
```

而 `Test.get(userService)` 是通过根注入器获取的。


## 测试依赖异步服务的组件


### 通过 Jasmine spy 来替换真实服务上的方法

注入的是真实的服务，但是调用的服务方法被替换：

```typescript
// src/app/shared/twain.component.ts
@Component({
  selector: 'twain-quote',
  template: '<p class="twain"><i>{{quote}}</i></p>'
})
export class TwainComponent  implements OnInit {
  intervalId: number;
  quote = '...';
  constructor(private twainService: TwainService) { }

  ngOnInit(): void {
    this.twainService.getQuote().then(quote => this.quote = quote);
  }
}


//src/app/shared/twain.component.spec.ts (setup)
beforeEach(() => {
  TestBed.configureTestingModule({
     declarations: [ TwainComponent ],
     providers:    [ TwainService ],
  });

  fixture = TestBed.createComponent(TwainComponent);
  comp    = fixture.componentInstance;

  // TwainService actually injected into the component
  twainService = fixture.debugElement.injector.get(TwainService);

  // Setup spy on the `getQuote` method
  spy = spyOn(twainService, 'getQuote')
        .and.returnValue(Promise.resolve(testQuote));

  // Get the Twain quote element by CSS selector (e.g., by class name)
  de = fixture.debugElement.query(By.css('.twain'));
  el = de.nativeElement;
});

//src/app/shared/twain.component.spec.ts (tests)
it('should not show quote before OnInit', () => {
  expect(el.textContent).toBe('', 'nothing displayed');
  // 在 OnInit 之前没有对 spy 上的 getQuote 进行调用
  expect(spy.calls.any()).toBe(false, 'getQuote not yet called');
});

it('should still not show quote after component initialized', () => {
  fixture.detectChanges();
  // getQuote service is async => still has not returned with quote
  expect(el.textContent).toBe('...', 'no quote yet');
  // 在 OnInit 之后对 spy 上的 getQuote 进行了调用，
  // 但由于是异步操作，只返回一个 resolved Promise,
  // 需要等待一个 tick 后才能使用返回值
  // 因此测试也必须使用异步方式
  expect(spy.calls.any()).toBe(true, 'getQuote called');
});

//异步方式的测试，async() 将包裹的测试任务安排到一个特殊的 async test zone 中执行。
it('should show quote after getQuote promise (async)', async(() => {
  fixture.detectChanges();

  // `ComponentFixture.whenStable` 方法也返回一个自己的 Promise，
  // 当 `getQuote` 的 Promise 结束时会 resolve，也就是当该测试中的
  // 所有异步活动都结束时。  
  fixture.whenStable().then(() => { // wait for async getQuote
    fixture.detectChanges();        // update view with quote
    expect(el.textContent).toBe(testQuote);
  });
}));

//另一种异步方式的测试，fakeAsync() 也将包裹的测试任务安排到一个特殊的 fakeAsync test zone 中执行。
//使用 fakeAsync() 能使其中的测试代码以同步的方式编写。
// 而其中的 `tick()`(只能在 `fackAsync` 异步体中调用）功能等同于 `fixture.whenStable`
it('should show quote after getQuote promise (fakeAsync)', fakeAsync(() => {
  fixture.detectChanges();
  tick();                  // wait for async getQuote
  fixture.detectChanges(); // update view with quote
  expect(el.textContent).toBe(testQuote);
}));
```

也可以通过 jasmine.done 回调函数来手动编写异步测试：

```typescript
//src/app/shared/twain.component.spec.ts (done test)
it('should show quote after getQuote promise (done)', (done: any) => {
  fixture.detectChanges();

  // get the spy promise and wait for it to resolve
  spy.calls.mostRecent().returnValue.then(() => {
    fixture.detectChanges(); // update view with quote
    expect(el.textContent).toBe(testQuote);
    done();
  });
});
```

## 测试有输入和输出属性的组件

在 `beforeEach` 中直接设置输入属性，在测试用例中通过 `triggerEventHandler` 来触发组件的发出属性：

```typescript
//src/app/dashboard/dashboard-hero.component.spec.ts (setup)
// async beforeEach
beforeEach( async(() => {
  TestBed.configureTestingModule({
    declarations: [ DashboardHeroComponent ],
  })
  .compileComponents(); // compile template and css
}));

// synchronous beforeEach
beforeEach(() => {
  fixture = TestBed.createComponent(DashboardHeroComponent);
  comp    = fixture.componentInstance;
  heroEl  = fixture.debugElement.query(By.css('.hero')); // find hero element

  // pretend that it was wired to something that supplied a hero
  expectedHero = new Hero(42, 'Test Name');
  comp.hero = expectedHero;
  fixture.detectChanges(); // trigger initial data binding
});


//src/app/dashboard/dashboard-hero.component.spec.ts (name test)
it('should display hero name', () => {
  const expectedPipedName = expectedHero.name.toUpperCase();
  expect(heroEl.nativeElement.textContent).toContain(expectedPipedName);
});

//src/app/dashboard/dashboard-hero.component.spec.ts (click test)
it('should raise selected event when clicked', () => {
  let selectedHero: Hero;
  //组件的输出属性是一个 `EventEmitter`，像它注册就相当于对组件事件的绑定
  comp.selected.subscribe((hero: Hero) => selectedHero = hero);

  //DebugElement.triggerEventHandler() 触发事件，第 2 个参数是传给
  //事件处理函数的参数对象
  heroEl.triggerEventHandler('click', null);
  expect(selectedHero).toBe(expectedHero);
});
```

### 触发事件

`RouterLink` 指令的点击事件处理函数需要传入一个含 `button` 属性的参数对象，用来表示鼠标哪个按键按下。可将触发所有元素上的点击封装成一个通用函数如下：

```typescript
//testing/index.ts (click helper)
/** Button events to pass to `DebugElement.triggerEventHandler` for RouterLink event handler */
export const ButtonClickEvents = {
   left:  { button: 0 },
   right: { button: 2 }
};

/** Simulate element click. Defaults to mouse left-button click event. */
export function click(el: DebugElement | HTMLElement, eventObj: any = ButtonClickEvents.left): void {
  if (el instanceof HTMLElement) {
    el.click();
  } else {
    el.triggerEventHandler('click', eventObj);
  }
}
```

## 对在一个托管组件中的组件进行测试

先定义一个测试用的托管组件，进来简化实际的托管组件。

```typescript
//src/app/dashboard/dashboard-hero.component.spec.ts (test host)
@Component({
  template: `
    <dashboard-hero  [hero]="hero"  (selected)="onSelected($event)"></dashboard-hero>`
})
class TestHostComponent {
  hero = new Hero(42, 'Test Name');
  selectedHero: Hero;
  onSelected(hero: Hero) { this.selectedHero = hero; }
}


//rc/app/dashboard/dashboard-hero.component.spec.ts (test host setup)
beforeEach( async(() => {
  TestBed.configureTestingModule({
    declarations: [ DashboardHeroComponent, TestHostComponent ], // declare both
  }).compileComponents();
}));

beforeEach(() => {
  // create TestHostComponent instead of DashboardHeroComponent
  fixture  = TestBed.createComponent(TestHostComponent);
  testHost = fixture.componentInstance;
  heroEl   = fixture.debugElement.query(By.css('.hero')); // find hero
  fixture.detectChanges(); // trigger initial data binding
});


//src/app/dashboard/dashboard-hero.component.spec.ts (test-host)
it('should display hero name', () => {
  const expectedPipedName = testHost.hero.name.toUpperCase();
  expect(heroEl.nativeElement.textContent).toContain(expectedPipedName);
});

it('should raise selected event when clicked', () => {
  click(heroEl);
  // selected hero should be the same data bound hero
  expect(testHost.selectedHero).toBe(testHost.hero);
});
```

## 测试一个带路由的组件

这些组件通常会注入 `Router`，必须只使用 `Router` 中的某些方法，因此可以为 `Router` 创建一个 `RouterStub` 来注入：

```typescript
//src/app/dashboard/dashboard.component.ts (constructor)
constructor(
  private router: Router,
  private heroService: HeroService) {
}

//src/app/dashboard/dashboard.component.ts (goToDetail)
//该组件只使用了 `Router` 的 `navigateByUrl` 功能
gotoDetail(hero: Hero) {
  let url = `/heroes/${hero.id}`;
  this.router.navigateByUrl(url);
}


//src/app/dashboard/dashboard.component.spec.ts (Router Stub)
//创建一个 RouterStub
class RouterStub {
  navigateByUrl(url: string) { return url; }
}


//src/app/dashboard/dashboard.component.spec.ts (compile and create)
beforeEach( async(() => {
  TestBed.configureTestingModule({
    providers: [
      { provide: HeroService, useClass: FakeHeroService },
      { provide: Router,      useClass: RouterStub }
    ]
  })
  .compileComponents().then(() => {
    fixture = TestBed.createComponent(DashboardComponent);
    comp = fixture.componentInstance;
  });
  

//src/app/dashboard/dashboard.component.spec.ts (navigate test)
it('should tell ROUTER to navigate when hero clicked',
  inject([Router], (router: Router) => { // ...

  const spy = spyOn(router, 'navigateByUrl');

  heroClick(); // trigger click on first inner <div class="hero">

  // args passed to router.navigateByUrl()
  const navArgs = spy.calls.first().args[0];

  // expecting to navigate to id of the component's first hero
  const id = comp.heroes[0].id;
  expect(navArgs).toBe('/heroes/' + id,
    'should nav to HeroDetail for first hero');
}));
```

`inject()` 函数来自 Angular 测试工具集，通过它注入的服务，在测试中可进行修改、spy on 和处理。而通过 `inject()` 获取的服务都来自 `TestBed` 注入器，不能调整为来自组件的注入器。

## 对带参数路由的组件进行测试

路由器会将参数推到 `ActivatedRoute.params` Observable 属性上，组件通过注入 `ActivatedRoute`，在 `ngOnInit` 中获取并处理参数：

```typescript
//src/app/hero/hero-detail.component.ts (ngOnInit)
ngOnInit(): void {
  // get hero when `id` param changes
  this.route.paramMap.subscribe(p => this.getHero(p.has('id') && p.get('id')));
}
```

测试时创建一个 ActivatedRouteStub，为测试提供参数值。下面是一个通用的 `ActivatedRouteStub`:

```typescript
//testing/router-stubs.ts (ActivatedRouteStub)
import { BehaviorSubject } from 'rxjs/BehaviorSubject';
import { convertToParamMap, ParamMap } from '@angular/router';

@Injectable()
export class ActivatedRouteStub {

  // ActivatedRoute.paramMap is Observable
  private subject = new BehaviorSubject(convertToParamMap(this.testParamMap));
  paramMap = this.subject.asObservable();

  // Test parameters
  private _testParamMap: ParamMap;
  get testParamMap() { return this._testParamMap; }
  set testParamMap(params: {}) {
    this._testParamMap = convertToParamMap(params);
    this.subject.next(this._testParamMap);
  }

  // ActivatedRoute.snapshot.paramMap
  get snapshot() {
    return { paramMap: this.testParamMap };
  }
}
```

通过对 testParamMap 赋值，模拟 URL 参数：

```typescript
//src/app/hero/hero-detail.component.spec.ts
//对 id 参数有效的情况进行测试
describe('when navigate to existing hero', () => {
  let expectedHero: Hero;

  beforeEach( async(() => {
    expectedHero = firstHero;
    activatedRoute.testParamMap = { id: expectedHero.id };
    createComponent();
  }));

  it('should display that hero\'s name', () => {
    expect(page.nameDisplay.textContent).toBe(expectedHero.name);
  });
});


//对 id 参数无效的情况进行测试，此时会重定向到 List 页面
describe('when navigate to non-existent hero id', () => {
  beforeEach( async(() => {
    activatedRoute.testParamMap = { id: 99999 };
    createComponent();
  }));

  it('should try to navigate back to hero list', () => {
    expect(page.gotoSpy.calls.any()).toBe(true, 'comp.gotoList called');
    expect(page.navSpy.calls.any()).toBe(true, 'router.navigate called');
  });
});

// 对无 id 值的情况进行测试
describe('when navigate with no hero id', () => {
  beforeEach( async( createComponent ));

  it('should have hero.id === 0', () => {
    expect(comp.hero.id).toBe(0);
  });

  it('should display empty hero name', () => {
    expect(page.nameDisplay.textContent).toBe('');
  });
});
```

### 使用一个 page 对象来简化设置

组件是一个视图，将视图中包含的所有测试时要用到的元素全部抽取到一个 `Page` 中，方便对各元素的存取，例如上例中测试的组件视图可组织为：

```typescript
//src/app/hero/hero-detail.component.spec.ts (Page)
class Page {
  gotoSpy:      jasmine.Spy;
  navSpy:       jasmine.Spy;

  saveBtn:      DebugElement;
  cancelBtn:    DebugElement;
  nameDisplay:  HTMLElement;
  nameInput:    HTMLInputElement;

  constructor() {
    const router = TestBed.get(Router); // get router from root injector
    this.gotoSpy = spyOn(comp, 'gotoList').and.callThrough();
    this.navSpy  = spyOn(router, 'navigate');
  }

  /** Add page elements after hero arrives */
  addPageElements() {
    if (comp.hero) {
      // have a hero so these elements are now in the DOM
      const buttons    = fixture.debugElement.queryAll(By.css('button'));
      this.saveBtn     = buttons[0];
      this.cancelBtn   = buttons[1];
      this.nameDisplay = fixture.debugElement.query(By.css('span')).nativeElement;
      this.nameInput   = fixture.debugElement.query(By.css('input')).nativeElement;
    }
  }
}
```

再创建一个 `createComponent()` 方法来创建一个组件及其 `page` 对象，并当组件所需的异步数据返回时填入 `page` 中：

```typescript
//src/app/hero/hero-detail.component.spec.ts (createComponent)
/** Create the HeroDetailComponent, initialize it, set test variables  */
function createComponent() {
  fixture = TestBed.createComponent(HeroDetailComponent);
  comp    = fixture.componentInstance;
  page    = new Page();

  // 1st change detection triggers ngOnInit which gets a hero
  fixture.detectChanges();
  return fixture.whenStable().then(() => {
    // 2nd change detection displays the async-fetched hero
    fixture.detectChanges();
    page.addPageElements();
  });
}
```

下面是一些测试举例：

```typescript
//src/app/hero/hero-detail.component.spec.ts (selected tests)
it('should display that hero\'s name', () => {
  expect(page.nameDisplay.textContent).toBe(expectedHero.name);
});

it('should navigate when click cancel', () => {
  click(page.cancelBtn);
  expect(page.navSpy.calls.any()).toBe(true, 'router.navigate called');
});

it('should save when click save but not navigate immediately', () => {
  // Get service injected into component and spy on its`saveHero` method.
  // It delegates to fake `HeroService.updateHero` which delivers a safe test result.
  const hds = fixture.debugElement.injector.get(HeroDetailService);
  const saveSpy = spyOn(hds, 'saveHero').and.callThrough();

  click(page.saveBtn);
  expect(saveSpy.calls.any()).toBe(true, 'HeroDetailService.save called');
  expect(page.navSpy.calls.any()).toBe(false, 'router.navigate not called');
});

it('should navigate when click save and save resolves', fakeAsync(() => {
  click(page.saveBtn);
  tick(); // wait for async save to complete
  expect(page.navSpy.calls.any()).toBe(true, 'router.navigate called');
}));

it('should convert hero name to Title Case', () => {
  const inputName = 'quick BROWN  fox';
  const titleCaseName = 'Quick Brown  Fox';

  // simulate user entering new name into the input box
  page.nameInput.value = inputName;

  // dispatch a DOM event so that Angular learns of input value change.
  page.nameInput.dispatchEvent(newEvent('input'));

  // Tell Angular to update the output span through the title pipe
  fixture.detectChanges();

  expect(page.nameDisplay.textContent).toBe(titleCaseName);
});
```

## 重载组件的提供者

通过 `TestBed.overrideComponent()` 来重载：

```typescript
//src/app/hero/hero-detail.component.spec.ts (Override setup)
beforeEach( async(() => {
  TestBed.configureTestingModule({
    imports:   [ HeroModule ],
    providers: [
      { provide: ActivatedRoute, useValue: activatedRoute },
      { provide: Router,         useClass: RouterStub},
    ]
  })

  // Override component's own provider
  .overrideComponent(HeroDetailComponent, {
    set: {
      providers: [
        { provide: HeroDetailService, useClass: HeroDetailServiceSpy }
      ]
    }
  })

  .compileComponents();
}));
```

重载时组件的 metadata 可以添加，删除和重设置，参数类型为：

```typescript
type MetadataOverride = {
    add?: T;
    remove?: T;
    set?: T;
  };
```

替换服务实现为：

```typescript
//src/app/hero/hero-detail.component.spec.ts (HeroDetailServiceSpy)
class HeroDetailServiceSpy {
  testHero = new Hero(42, 'Test Hero');

  getHero = jasmine.createSpy('getHero').and.callFake(
    () => Promise
      .resolve(true)
      .then(() => Object.assign({}, this.testHero))
  );

  saveHero = jasmine.createSpy('saveHero').and.callFake(
    (hero: Hero) => Promise
      .resolve(true)
      .then(() => Object.assign(this.testHero, hero))
  );
}
```

测试为：

```typescript
//src/app/hero/hero-detail.component.spec.ts (override tests)
let hdsSpy: HeroDetailServiceSpy;

beforeEach( async(() => {
  createComponent();
  // get the component's injected HeroDetailServiceSpy
  hdsSpy = fixture.debugElement.injector.get(HeroDetailService) as any;
}));

it('should have called `getHero`', () => {
  expect(hdsSpy.getHero.calls.count()).toBe(1, 'getHero called once');
});

it('should display stub hero\'s name', () => {
  expect(page.nameDisplay.textContent).toBe(hdsSpy.testHero.name);
});

it('should save stub hero change', fakeAsync(() => {
  const origName = hdsSpy.testHero.name;
  const newName = 'New Name';

  page.nameInput.value = newName;
  page.nameInput.dispatchEvent(newEvent('input')); // tell Angular

  expect(comp.hero.name).toBe(newName, 'component hero has new name');
  expect(hdsSpy.testHero.name).toBe(origName, 'service hero unchanged before save');

  click(page.saveBtn);
  expect(hdsSpy.saveHero.calls.count()).toBe(1, 'saveHero called once');

  tick(); // wait for async save to complete
  expect(hdsSpy.testHero.name).toBe(newName, 'service hero has new name after save');
  expect(page.navSpy.calls.any()).toBe(true, 'router.navigate called');
}));
```

`TestBed` 中也提供了 `overrideDirective`, `overrideModule`, `overridePipe` 方法。

## 测试 RouterOutlet 组件

这种组件一般有一组导航及一个 `<router-outlet>` 元素。要为 `RouterLink` 指令创建 `RouterLinkStubDirective`，以测试链接是否正确。

```typescript
//src/app/app.component.spec.ts (Stub Setup)
beforeEach( async(() => {
  TestBed.configureTestingModule({
    declarations: [
      AppComponent,
      BannerComponent, WelcomeStubComponent,
      RouterLinkStubDirective, RouterOutletStubComponent
    ]
  })

  .compileComponents()
  .then(() => {
    fixture = TestBed.createComponent(AppComponent);
    comp    = fixture.componentInstance;
  });
}));


//testing/router-stubs.ts (RouterLinkStubDirective)
@Directive({
  selector: '[routerLink]',
  host: {
    '(click)': 'onClick()'
  }
})
export class RouterLinkStubDirective {
  @Input('routerLink') linkParams: any;
  navigatedTo: any = null;

  onClick() {
    this.navigatedTo = this.linkParams;
  }
}

//src/app/app.component.spec.ts (test setup)
beforeEach(() => {
  // trigger initial data binding
  fixture.detectChanges();

  // find DebugElements with an attached RouterLinkStubDirective
  linkDes = fixture.debugElement
    .queryAll(By.directive(RouterLinkStubDirective));

  // get the attached link directive instances using the DebugElement injectors
  links = linkDes
    .map(de => de.injector.get(RouterLinkStubDirective) as RouterLinkStubDirective);
});
```

`RouterLinkStubDirective` 指令 metadata 中的 `host` 属性将指令托管元素（如 `<a>`) 上的点击与 `onClick()` 关联。

元素即可通过 CSS 选择子查询，也可用 `By.directive` 即指令查询到。因为 Angular 会将组件中的关联指令对象都放入到组件的注入器上，因此可通过注入到获致指令对象。

```typescript
//src/app/app.component.spec.ts (selected tests)
it('can get RouterLinks from template', () => {
  expect(links.length).toBe(3, 'should have 3 links');
  expect(links[0].linkParams).toBe('/dashboard', '1st link should go to Dashboard');
  expect(links[1].linkParams).toBe('/heroes', '1st link should go to Heroes');
});

it('can click Heroes link in template', () => {
  const heroesLinkDe = linkDes[1];
  const heroesLink = links[1];

  expect(heroesLink.navigatedTo).toBeNull('link should not have navigated yet');

  heroesLinkDe.triggerEventHandler('click', null);
  fixture.detectChanges();

  expect(heroesLink.navigatedTo).toBe('/heroes');
});
```

## 测试环境配置文件

+ `karma.conf.js`: 指定了使用哪些插件，加载哪个应用及测试文件，使用哪个浏览器，及如何报道结果。它还会加载另外 3 个设置文件：`systemjs.config.js`, `systemjs.config.extras.js`, `karma-test-shim.js`
+ `karma-test.shim.js`: 用于为 Angular 测试环境作准备，同时加载 karma 本身，同时加载 `systemjs.config.js`。
+ `systemjs.config.js`: SystemJS 加载应用和测试文件。该脚本告诉 SystemJS 到哪里及如何加载。
+ `system.config.extras.js`: 可选的额外配置。

## 参考

+ https://angular.io/guide/testing
+ [对应的 jupyter notebook](https://github.com/haiiiiiyun/angular-docs-notebook/blob/master/testing.ipynb)
