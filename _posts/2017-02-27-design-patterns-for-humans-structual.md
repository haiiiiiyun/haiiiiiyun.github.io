---
title: 用人话描述的设计模式--结构型设计模式
date: 2017-02-27
writing-time: 2017-02-27 10:10
categories: Programming
tags: Programming design&nbsp;pattern adapter bridge composite decorator facade flyweight proxy
---

> 注意下面的代码示例都是用 PHP-7 写的。

结构型设计模式
==========================

简单来说
> 结构型模式主要关注对象的组合或者换句话说是实体间如何能够相互使用。或者也可以另外解释为，它们有助于回答 "如何构建一个软件组件?“。

Wikipedia 上描述为
> 在软件工程中，结构型设计模式是这样的一些设计模式，它们通过某种简明的方式来实现实体间的关系，从而减少设计的难度。
 
 * [适配器(Adapter)](#-适配器adapter)
 * [桥接(Bridge)](#-桥接bridge)
 * [组合(Composite)](#-组合composite)
 * [装饰器(Decorator)](#-装饰器decorator)
 * [外观(Facade)](#-外观facade)
 * [享元(Flyweight)](#-享元flyweight)
 * [代理(Proxy)](#-代理proxy)

🔌 适配器(Adapter)
-------

现实案例
> 假设你的内存卡里有一些照片，你需要将它们传到电脑上。要完成传输，你需要有与你的电脑接口兼容的适配器，这样你才能将内存卡与你的电脑连接。在这种情况下读卡器就是一个适配器。
> 另一个例子就是大家都知道的电源适配器; 一个三脚插头无法插到两口的插座上，需要使用一个电源适配器才能将它与两口插座连接。
> 还有一个例子就是翻译，他能将一个人说的话翻译给另一个听。

简单来说
> 适配器模式允许你在适配器中封装其它不兼容的对象，从而使它们与某些类兼容。

Wikipedia 上描述为
> 在软件工程中，适配器这种软件设计模式允许将现有类的接口转成另一种接口来使用。它通常用于使现有类在无需修改其源码的情况下，与其它类实现协作。

**编程示例**

假设现有一款关于猎人猎狮的游戏。

首先定义 `Lion` 接口并实现所有种类的狮子类

```php
interface Lion {
    public function roar();
}

class AfricanLion implements Lion {
    public function roar() {}
}

class AsianLion implements Lion {
    public function roar() {}
}
```

猎人只有当看到实现了 `Lion` 接口的猎物后才能狩猎。

```php
class Hunter {
    public function hunt(Lion $lion) {
    }
}
```

现假设我们需要在游戏中加入 `WildDog`，使猎人对它们也能进行狩猎。但是我们无法直接实现，因为狗具有不同的接口。要使它与我们的猎人兼容，我们需要创建一个兼容的适配器。
 
```php
// This needs to be added to the game
class WildDog {
    public function bark() {}
}

// Adapter around wild dog to make it compatible with our game
class WildDogAdapter implements Lion {
    protected $dog;

    public function __construct(WildDog $dog) {
        $this->dog = $dog;
    }
    
    public function roar() {
        $this->dog->bark();
    }
}
```

现在 `WildDog` 可能通过 `WildDogAdapter` 使用到我们的游戏中了。

```php
$wildDog = new WildDog();
$wildDogAdapter = new WildDogAdapter($wildDog);

$hunter = new Hunter();
$hunter->hunt($wildDogAdapter);
```

🚡 桥接(Bridge)
------

现实案例
> 假设你有一个由多个不同的页面组成的网站，然后你想让用户可以修改页面主题风格。那么你会怎么做？是为每一个页面针对每一个主题风格都创建一个复本，还是只创建分离的主题风格，然后根据用户的喜好加载主题风格？如果你想用第二种办法，那么桥接模式就是你的解决之道。

![With and without the bridge pattern](https://cloud.githubusercontent.com/assets/11269635/23065293/33b7aea0-f515-11e6-983f-98823c9845ee.png)

简单来说
> 桥接模式认为组合优于继承。它能将一个层级结构中的实现细节转到位于另一个分离的层级结构的对象中。

Wikipedia 上描述为
> 桥接模式是软件设计模式之一，它意在 ”将抽象与真实现分离，从而使它们可以各自独立的变化“。

**编程实例**

实现上面的网站的例子，这里定义了 `WebPage` 的层级结构

```php
interface WebPage {
    public function __construct(Theme $theme);
    public function getContent();
}

class About implements WebPage {
    protected $theme;
    
    public function __construct(Theme $theme) {
        $this->theme = $theme;
    }
    
    public function getContent() {
        return "About page in " . $this->theme->getColor();
    }
}

class Careers implements WebPage {
   protected $theme;
   
   public function __construct(Theme $theme) {
       $this->theme = $theme;
   }
   
   public function getContent() {
       return "Careers page in " . $this->theme->getColor();
   } 
}
```

然后是另外分离的主题风格层级结构

```php
interface Theme {
    public function getColor();
}

class DarkTheme implements Theme {
    public function getColor() {
        return 'Dark Black';
    }
}
class LightTheme implements Theme {
    public function getColor() {
        return 'Off white';
    }
}
class AquaTheme implements Theme {
    public function getColor() {
        return 'Light blue';
    }
}
```

最后将两个层级结构组合起来

```php
$darkTheme = new DarkTheme();

$about = new About($darkTheme);
$careers = new Careers($darkTheme);

echo $about->getContent(); // "About page in Dark Black";
echo $careers->getContent(); // "Careers page in Dark Black";
```

🌿 组合(Composite)
-----------------

现实案例
> 每个组织都由员工组成。每个员工都有相似的特征，如都有工资，都担负一些职责，需要（或者不需要）向某人汇报，有（或者没有）一些下属等。

简单来说
> 组合模式使得客户能以统一的方式对待每个对象。

Wikipedia 上描述为
> 在软件工程中，组合模式是一种分割式的设计模式。组合模式描述为：能以和对待单个对象实例相同的方式对待对象的组合。组合为的是将对象组织成树状结构，以表达 *部分-整体* 的层级关系。使用组合模式后，客户就能一致地对待单独对象和组合体了。

**编程示例**

使用上面的员工的例子。这里定义了不同类型的员工

```php
interface Employee {
    public function __construct(string $name, float $salary);
    public function getName() : string;
    public function setSalary(float $salary);
    public function getSalary() : float;
    public function getRoles()  : array;
}

class Developer implements Employee {

    protected $salary;
    protected $name;

    public function __construct(string $name, float $salary) {
        $this->name = $name;
        $this->salary = $salary;
    }

    public function getName() : string {
        return $this->name;
    }

    public function setSalary(float $salary) {
        $this->salary = $salary;
    }

    public function getSalary() : float {
        return $this->salary;
    }

    public function getRoles() : array {
        return $this->roles;
    }
}

class Designer implements Employee {

    protected $salary;
    protected $name;

    public function __construct(string $name, float $salary) {
        $this->name = $name;
        $this->salary = $salary;
    }

    public function getName() : string {
        return $this->name;
    }

    public function setSalary(float $salary) {
        $this->salary = $salary;
    }

    public function getSalary() : float {
        return $this->salary;
    }

    public function getRoles() : array {
        return $this->roles;
    }
}
```

再定义一个组织，它由不同类型的员工组成

```php
class Organization {
    
    protected $employees;

    public function addEmployee(Employee $employee) {
        $this->employees[] = $employee;
    }

    public function getNetSalaries() : float {
        $netSalary = 0;

        foreach ($this->employees as $employee) {
            $netSalary += $employee->getSalary();
        }

        return $netSalary;
    }
}
```

然后可以这样使用

```php
// Prepare the employees
$john = new Developer('John Doe', 12000);
$jane = new Designer('Jane', 10000);

// Add them to organization
$organization = new Organization();
$organization->addEmployee($john);
$organization->addEmployee($jane);

echo "Net salaries: " . $organization->getNetSalaries(); // Net Salaries: 22000
```

☕ 装饰器(Decorator)
-------------

现实案例

> 假设你运营一家能提供多种服务的汽车服务店。现在你怎样计算要收的费用？你会根据提供了的所有服务，将每项服务费用都动态叠加进去，直到算出总额。这里每种服务都是一种装饰器。

简单来说
> 装饰器模式通过将对象封装在装饰器类的对象中，从而使你能在运行时动态地修改原对象的行为。

Wikipedia 上描述为
> 在面向对象编程中，装饰器这种设计模式允许以静态或者动态的方式，将行为添加到某个对象中，而这种修改不会影响相同类中的其它实例对象的行为。装饰器模式通常对于遵循单一职责原则(Single Responsibility Principle)很有用, 因为它允许功能在类间进行划分，使得各个类只专注各自的功能领域。

**编程示例**

以咖啡为例。首先为简单咖啡实现咖啡接口

```php
interface Coffee {
    public function getCost();
    public function getDescription();
}

class SimpleCoffee implements Coffee {

    public function getCost() {
        return 10;
    }

    public function getDescription() {
        return 'Simple coffee';
    }
}
```

我们想使代码可扩展，允许在需要的时候能够修改选项。让我们增加一些添加物（装饰器）

```php
class MilkCoffee implements Coffee {
    
    protected $coffee;

    public function __construct(Coffee $coffee) {
        $this->coffee = $coffee;
    }

    public function getCost() {
        return $this->coffee->getCost() + 2;
    }

    public function getDescription() {
        return $this->coffee->getDescription() . ', milk';
    }
}

class WhipCoffee implements Coffee {

    protected $coffee;

    public function __construct(Coffee $coffee) {
        $this->coffee = $coffee;
    }

    public function getCost() {
        return $this->coffee->getCost() + 5;
    }

    public function getDescription() {
        return $this->coffee->getDescription() . ', whip';
    }
}

class VanillaCoffee implements Coffee {

    protected $coffee;

    public function __construct(Coffee $coffee) {
        $this->coffee = $coffee;
    }

    public function getCost() {
        return $this->coffee->getCost() + 3;
    }

    public function getDescription() {
        return $this->coffee->getDescription() . ', vanilla';
    }
}
```

现在可以制作咖啡了

```php
$someCoffee = new SimpleCoffee();
echo $someCoffee->getCost(); // 10
echo $someCoffee->getDescription(); // Simple Coffee

$someCoffee = new MilkCoffee($someCoffee);
echo $someCoffee->getCost(); // 12
echo $someCoffee->getDescription(); // Simple Coffee, milk

$someCoffee = new WhipCoffee($someCoffee);
echo $someCoffee->getCost(); // 17
echo $someCoffee->getDescription(); // Simple Coffee, milk, whip

$someCoffee = new VanillaCoffee($someCoffee);
echo $someCoffee->getCost(); // 20
echo $someCoffee->getDescription(); // Simple Coffee, milk, whip, vanilla
```

📦 外观(Facade)
----------------

现实案例
> 你是怎样开电脑的？ "按电源键" 你说！你相信那样一定可以，这是由于你正在使用电脑外部的一个简单接口，而其内部则需要完成大量工作才能实现开机。这个针对复杂子系统而设计的简单接口就是外观。

简单来说
> 外观模式为复杂子系统提供一个简化接口。

Wikipedia 上描述为
> 外观就是一个对象，它为更大规模的代码，如类库等提供简化的接口。

**编程示例**

使用上面的电脑的例子。现在先定义电脑类

```php
class Computer {

    public function getElectricShock() {
        echo "Ouch!";
    }

    public function makeSound() {
        echo "Beep beep!";
    }

    public function showLoadingScreen() {
        echo "Loading..";
    }

    public function bam() {
        echo "Ready to be used!";
    }

    public function closeEverything() {
        echo "Bup bup bup buzzzz!";
    }

    public function sooth() {
        echo "Zzzzz";
    }

    public function pullCurrent() {
        echo "Haaah!";
    }
}
```

这样定义外观

```php
class ComputerFacade
{
    protected $computer;

    public function __construct(Computer $computer) {
        $this->computer = $computer;
    }

    public function turnOn() {
        $this->computer->getElectricShock();
        $this->computer->makeSound();
        $this->computer->showLoadingScreen();
        $this->computer->bam();
    }

    public function turnOff() {
        $this->computer->closeEverything();
        $this->computer->pullCurrent();
        $this->computer->sooth();
    }
}
```

现在这样使用外观

```php
$computer = new ComputerFacade(new Computer());
$computer->turnOn(); // Ouch! Beep beep! Loading.. Ready to be used!
$computer->turnOff(); // Bup bup buzzz! Haah! Zzzzz
```

🍃 享元(Flyweight)
---------

现实案例
> 你有过在摊位上品尝过新茶吗？他们通常沏出比你所要的还要多的杯数，然后将多余的荼留给其他客人，从而起到节约资源（如燃气）的目的。享元模式的全部即共享。

简单来说
> 它能使相似对象间通过尽可能多地共享，以减少内存使用和计算花销。

Wikipedia 上描述为
> 在计算机编程中，享元是一种软件设计模式。一个享元就是一个对象，它通过与其它相似对象共享尽可能多的数据，以达到对内存的最少化使用;它适用于对象数量庞大的情况，此时简单地重复表示将需要过量的内存量。

**编程示例**

实现以上的茶的例子。首先定义各种茶和茶艺师

```php
// Anything that will be cached is flyweight. 
// Types of tea here will be flyweights.
class KarakTea {
}

// Acts as a factory and saves the tea
class TeaMaker {
    protected $availableTea = [];

    public function make($preference) {
        if (empty($this->availableTea[$preference])) {
            $this->availableTea[$preference] = new KarakTea();
        }

        return $this->availableTea[$preference];
    }
}
```

然后定义 `TeaShop`，提供饮茶服务

```php
class TeaShop {
    
    protected $orders;
    protected $teaMaker;

    public function __construct(TeaMaker $teaMaker) {
        $this->teaMaker = $teaMaker;
    }

    public function takeOrder(string $teaType, int $table) {
        $this->orders[$table] = $this->teaMaker->make($teaType);
    }

    public function serve() {
        foreach($this->orders as $table => $tea) {
            echo "Serving tea to table# " . $table;
        }
    }
}
```

可以如下使用

```php
$teaMaker = new TeaMaker();
$shop = new TeaShop($teaMaker);

$shop->takeOrder('less sugar', 1);
$shop->takeOrder('more milk', 2);
$shop->takeOrder('without sugar', 5);

$shop->serve();
// Serving tea to table# 1
// Serving tea to table# 2
// Serving tea to table# 5
```

🎱 代理(Proxy)
-------------------

现实案例
> 你有用过门禁卡开过门吗？打开门有多种方式，比如使用门禁门或者使用密码锁等。门的主要功能是打门，但在此之上还加了个代理，它增加了额外的一些功能。让我们使用以下的代码示例来更好地解释。

简单来说
> 使用代理模式，一个类可以代表其它类的功能。

Wikipedia 上描述为
> 一个代理，其最一般的形式，就是作为其它类的接口的一个类。代理就是一个包装或中介对象，客户通过调用它来访问幕后真正提供服务的对象。使用代理可以简单地转发到真实对象，也可以提供额外的逻辑。代理可以提供这些额外的功能，例如当在真实对象上的操作需要大量资源时进行缓存，或者对真实对象调用操作时先检查先决条件等。

**编程示例**

使用以上的安全门的例子。首先定义门的接口并实现门的类

```php
interface Door {
    public function open();
    public function close();
}

class LabDoor implements Door {
    public function open() {
        echo "Opening lab door";
    }

    public function close() {
        echo "Closing the lab door";
    }
}
```

然后定义代理，为门提供安全措施

```php
class Security {
    protected $door;

    public function __construct(Door $door) {
        $this->door = $door;
    }

    public function open($password) {
        if ($this->authenticate($password)) {
            $this->door->open();
        } else {
        	echo "Big no! It ain't possible.";
        }
    }

    public function authenticate($password) {
        return $password === '$ecr@t';
    }

    public function close() {
        $this->door->close();
    }
}
```

这里是如何使用

```php
$door = new Security(new LabDoor());
$door->open('invalid'); // Big no! It ain't possible.

$door->open('$ecr@t'); // Opening lab door
$door->close(); // Closing lab door
```

另一个例子是一些数据映射(data-mapper)的实现。例如，我（原作者）使用该模式为 MongoDB 做了一个对象数据映射器(ODM, Object Data Mapper)，我通过在 mongo 类外编写一个代理来调用特殊函数 `__call()`。对代理的所有方法函数都转到原 mongo 类上，并且取得的结果也都原样返回，除了 `find` 或 `findOne` 的数据会映射成所需的类对象并返回，而不以 `Cursor` 返回。


# 参考 

+ [Design patterns for humans, CN](https://github.com/haiiiiiyun/design-patterns-for-humans-cn)
