---
title: 用人话描述的设计模式--创建型设计模式
date: 2017-02-25
writing-time: 2017-02-25 15:21
categories: Programming
tags: Programming design&nbsp;pattern simple&nbsp;factory factory&nbsp;method abstract&nbsp;factory builder prototype singleton
---

> 注意下面的代码示例都是用 PHP-7 写的。

创建型设计模式
==========================

简单来说
> 创建型模式关注于如何实例化一个或一组相关对象。

Wikipedia 上描述为
> 在软件工程中，创建型设计模式是处理对象创建机制，设法以适合当前情况的方式来创建对象的设计模式。对象创建时若使用一般形式可能会导致设计难题或增加设计的复杂度。创建型设计模式通过对对象创建过程的控制以解决此问题。
 
 * [简单工厂(Simple Factory)](#-简单工厂simple-factory)
 * [工厂方法(Factory Method)](#-工厂方法factory-method)
 * [抽象工厂(Abstract Factory)](#-抽象工厂abstract-factory)
 * [建造者(Builder)](#-建造者builder)
 * [原型(Prototype)](#-原型prototype)
 * [单例(Singleton)](#-单例singleton)
 
🏠 简单工厂(Simple Factory)
--------------
现实案例
> 假设你正在建房，需要用到门。如果每次需要门时，你都穿上木匠服在房子里亲自制作，肯定会导致一团糟。这种情况下你需要将门放在工厂里制作。

简单来说
> 简单工厂模式对客户隐藏了所有的实例化逻辑，只简单地为客户创建实例。

Wikipedia 上描述为
> 在面向对象编程 (OOP) 中，工厂就是一个用于创建其它对象的对象,  – 形式上它可以是一个函数或方法，它在被方法调用时（假设通过 "new"）会返回不同原型或类的对象。

**编程示例**

首先定义门的接口及其实现

```php
interface Door {
    public function getWidth() : float;
    public function getHeight() : float;
}

class WoodenDoor implements Door {
    protected $width;
    protected $height;

    public function __construct(float $width, float $height) {
        $this->width = $width;
        $this->height = $height;
    }
    
    public function getWidth() : float {
        return $this->width;
    }
    
    public function getHeight() : float {
        return $this->height;
    }
}
```

然后定义门的工厂，它创建并返回门实例

```php
class DoorFactory {
   public static function makeDoor($width, $height) : Door {
       return new WoodenDoor($width, $height);
   }
}
```

再这样使用

```php
$door = DoorFactory::makeDoor(100, 200);
echo 'Width: ' . $door->getWidth();
echo 'Height: ' . $door->getHeight();
```

**何时用？**

当创建对象不仅只是一些赋值操作，还涉及一些逻辑操作时，就适合将这些逻辑放到一个专门的工厂中，从而能避免代码重复。

🏭 工厂方法(Factory Method)
--------------

现实案例
> 考虑人事招聘经理的情况。一个人不可能参与对每个职位的面试。根据职位空缺，她必须决定将面试工作委派给不同的人来完成。

简单来说
> 它提供了一种能将实例化逻辑委派到子类中完成的方式。

Wikipedia 上描述为
> 在基于类的编程中，工厂方法模式是一种创建型模式，它无需指定将要创造的对象的具体类，只使用工厂中的各种方法就能处理对象创建的问题。对象的创建是通过调用工厂方法而非构造器来完成的，工厂方法—要么在接口中定义然后由子类实现，要么是在基类中实现然后被继承类重载。
 
 **编程示例**
 
继续上面的人事招聘经理的例子。首先定义面试接口并给出了几个实现

```php
interface Interviewer {
    public function askQuestions();
}

class Developer implements Interviewer {
    public function askQuestions() {
        echo 'Asking about design patterns!';
    }
}

class CommunityExecutive implements Interviewer {
    public function askQuestions() {
        echo 'Asking about community building';
    }
}
```

现在让我们创建 `HiringManager`

```php
abstract class HiringManager {
    
    // Factory method
    abstract public function makeInterviewer() : Interviewer;
    
    public function takeInterview() {
        $interviewer = $this->makeInterviewer();
        $interviewer->askQuestions();
    }
}
```

现在任何子类都可以扩展并提供所需的面试接口

```php
class DevelopmentManager extends HiringManager {
    public function makeInterviewer() : Interviewer {
        return new Developer();
    }
}

class MarketingManager extends HiringManager {
    public function makeInterviewer() : Interviewer {
        return new CommunityExecutive();
    }
}
```

然后可以这样使用

```php
$devManager = new DevelopmentManager();
$devManager->takeInterview(); // Output: Asking about design patterns

$marketingManager = new MarketingManager();
$marketingManager->takeInterview(); // Output: Asking about community building.
```

**何时使用？**

适合时当类中存在一些通用操作，但是所需的子类是在运行时才动态决定的情况。换句话说，即当客户无法知道所需的确切子类时。

🔨 抽象工厂(Abstract Factory)
----------------

现实案例
> 继续简单工厂模式中门的例子。基于你的需求，你可能要从木门店获取木门，从铁门店获取铁门，或者从 PVC 相关店获取 PVC 门。另外你可能还要找不同专长的人来安装门，例如找木匠来安装木门，找电焊工来安装铁门等等。可以看到现在门已经有了依赖性，比如木门依赖于木匠，铁门依赖于电焊工等。

简单来说
> 就是工厂的工厂; 该工厂将各个相关/相依赖的工厂组合起来，而无需指定他们具体的类。

Wikipedia 上描述为
> 抽象工厂模式提供了一种将具有相同风格的一组工厂封闭起来的方法，而无需指定各工厂具体的类。

**编程示例**

修改上面门的例子。首先定义 `Door` 接口并做出几个实现

```php
interface Door {
    public function getDescription();
}

class WoodenDoor implements Door {
    public function getDescription() {
        echo 'I am a wooden door';
    }
}

class IronDoor implements Door {
    public function getDescription() {
        echo 'I am an iron door';
    }
}
```

然后为每种门都定义相应的安装人员

```php
interface DoorFittingExpert {
    public function getDescription();
}

class Welder implements DoorFittingExpert {
    public function getDescription() {
        echo 'I can only fit iron doors';
    }
}

class Carpenter implements DoorFittingExpert {
    public function getDescription() {
        echo 'I can only fit wooden doors';
    }
}
```

现在定义我们的抽象工厂，它能为我们创建相关的一组对象，例如木门工厂将会创建木门及木门安装人员对象，而铁门工厂将会创建铁门及铁门安装人员对象。

```php
interface DoorFactory {
    public function makeDoor() : Door;
    public function makeFittingExpert() : DoorFittingExpert;
}

// 木门工厂将返回木匠及木门对象
class WoodenDoorFactory implements DoorFactory {
    public function makeDoor() : Door {
        return new WoodenDoor();
    }

    public function makeFittingExpert() : DoorFittingExpert{
        return new Carpenter();
    }
}

// 铁门工厂将返回铁门及相应的安装人员
class IronDoorFactory implements DoorFactory {
    public function makeDoor() : Door {
        return new IronDoor();
    }

    public function makeFittingExpert() : DoorFittingExpert{
        return new Welder();
    }
}
```

然后可以这样使用

```php
$woodenFactory = new WoodenDoorFactory();

$door = $woodenFactory->makeDoor();
$expert = $woodenFactory->makeFittingExpert();

$door->getDescription();  // Output: I am a wooden door
$expert->getDescription(); // Output: I can only fit wooden doors

// Same for Iron Factory
$ironFactory = new IronDoorFactory();

$door = $ironFactory->makeDoor();
$expert = $ironFactory->makeFittingExpert();

$door->getDescription();  // Output: I am an iron door
$expert->getDescription(); // Output: I can only fit iron doors
```

可以看到木门工厂已经封装了 `木匠` 和 `木门` 而铁门工厂已经封闭了 `铁门` 和 `电焊工`。这样它就能确保，每次创建了一个门对象后，我们也可以得到其相应的安装人员对象。

**何时使用？**

当创建逻辑有点复杂但内部又相互关联时使用。

👷 创造者(Builder)
--------------------------------------------

现实案例
> 假设你在 Harees(美国连锁快餐店)，你下了单，假定说要来份 "大份装"，然后店员 *无需再多问* 就直接为你送上 "大份装"; 像这样的就是简单工厂模式的例子。但是有些情况下创建逻辑可能要涉及多个步骤。例如你想要一份定制餐，你给出了如何做汉堡的具体要求，例如使用什么面包，使用何种酱汁，何种奶酪等。那么这种情况下就需要使用建造者模式。

简单来说
> 它允许你创建 ”不同口味" 的对象，同时又能避免 “污染” 构造函数的参数。适合当某对象可能会有多种 “口味"，或者对象的创建过程涉及多个步骤时使用。
 
Wikipedia 上描述为
> 建造者模式是一种对象创建的软件设计模式，它意在为重叠构造器这种反模式(telescoping constructor anti-pattern)找到一种解决方案。

既然说到了，那让我多说几句什么是重叠构造器反模式(telescoping constructor anti-pattern)。我们或多或少有看到过像这样的构造函数：
 
```php
public function __construct($size, $cheese = true, $pepperoni = true, $tomato = false, $lettuce = true) {
}
```

可以看到; 构造函数的参数个数很快会变得一发不可收拾，从而要理解参数布局会变得困难。另外假如以后还要添加更多功能的话，该参数列表还会继续增长。这就是所谓的重叠构造器反模式(telescoping constructor anti-pattern)。

**编程示例**

理智地选择是使用建造者模式。首先定义我们需要制作的汉堡类

```php
class Burger {
    protected $size;

    protected $cheese = false;
    protected $pepperoni = false;
    protected $lettuce = false;
    protected $tomato = false;
    
    public function __construct(BurgerBuilder $builder) {
        $this->size = $builder->size;
        $this->cheese = $builder->cheese;
        $this->pepperoni = $builder->pepperoni;
        $this->lettuce = $builder->lettuce;
        $this->tomato = $builder->tomato;
    }
}
```

然后定义建造者类

```php
class BurgerBuilder {
    public $size;

    public $cheese = false;
    public $pepperoni = false;
    public $lettuce = false;
    public $tomato = false;

    public function __construct(int $size) {
        $this->size = $size;
    }
    
    public function addPepperoni() {
        $this->pepperoni = true;
        return $this;
    }
    
    public function addLettuce() {
        $this->lettuce = true;
        return $this;
    }
    
    public function addCheese() {
        $this->cheese = true;
        return $this;
    }
    
    public function addTomato() {
        $this->tomato = true;
        return $this;
    }
    
    public function build() : Burger {
        return new Burger($this);
    }
}
```

然后可以这样使用:

```php
$burger = (new BurgerBuilder(14))
                    ->addPepperoni()
                    ->addLettuce()
                    ->addTomato()
                    ->build();
```

**何时使用？**

当某个对象可能会有多种 "口味"，或者想避免重叠构造器反模式(telescoping constructor anti-pattern) 时使用。它与工厂模式的主要区别在于：工厂模式适用于创建过程只有一个步骤的情况，而建造者模式适用于创建过程涉及多个步骤的情况。

🐑 原型(Prototype)
------------

现实案例
> 还记得多莉吗？那只克隆羊！我们先不要关注细节，但是这里的重点是克隆。

简单来说
> 根据某个现存的对象，通过克隆来创建对象。

Wikipedia 上描述为
> 原型模式是软件开发中的创建型设计模式。它用于当所需创建的对象的类型是由某个原型实例决定的情况，并通过克隆该原型实例来产生新的对象。

简单来说，它能让你创建某个现有对象的克隆版本，然后你可按需对其进行修改，从而避免了从新创建一个对象并对其进行设置的所有麻烦。

**编程示例**

在 PHP 中, 可以非常容易地使用 `clone` 实现
 
```php
class Sheep {
    protected $name;
    protected $category;

    public function __construct(string $name, string $category = 'Mountain Sheep') {
        $this->name = $name;
        $this->category = $category;
    }
    
    public function setName(string $name) {
        $this->name = $name;
    }

    public function getName() {
        return $this->name;
    }

    public function setCategory(string $category) {
        $this->category = $category;
    }

    public function getCategory() {
        return $this->category;
    }
}
```

然后像下面这样进行克隆

```php
$original = new Sheep('Jolly');
echo $original->getName(); // Jolly
echo $original->getCategory(); // Mountain Sheep

// Clone and modify what is required
$cloned = clone $original;
$cloned->setName('Dolly');
echo $cloned->getName(); // Dolly
echo $cloned->getCategory(); // Mountain sheep
```

另外你也可以通过特殊方法 `__clone` 来定制克隆行为。

**何时使用？**

当所需对象和某个现存对象非常相似时，或者当创建操作相比克隆花销更大时。

💍 单例(Singleton)
------------

现实案例
> 一个国家在同一时期只能有一位总统。当需要担起责任时，都是这位总统实施行动的。这里总统就是单例。

简单来说
> 它能确保某个类永远只能够创建一个对象。

Wikipedia 上描述为
> 在软件工程中，单例模式是一种软件设计模式，它限制某个类只能实例化成一个对象。当系统中需要确切一个对象来协调行为时，单例是很适合的。

单例模式实际上被认为是一种反模式，因此需避免过度使用。它不一定就是不好的，它有它的适用情况，但是使用时应当当心，因为它在你的程序中引用了一个全局状态，因此在某处对它的修改可能会影响其它地方，从而对它进行调试会变得相当困难。

**编程示例**

创建一个单例，将构造器设为私有，禁用克隆功能，禁止扩展，并创建一个静态变量来保存实例

```php
final class President {
    private static $instance;

    private function __construct() {
        // Hide the constructor
    }
    
    public static function getInstance() : President {
        if (!self::$instance) {
            self::$instance = new self();
        }
        
        return self::$instance;
    }
    
    private function __clone() {
        // Disable cloning
    }
    
    private function __wakeup() {
        // Disable unserialize
    }
}
```

然后这样使用

```php
$president1 = President::getInstance();
$president2 = President::getInstance();

var_dump($president1 === $president2); // true
```


# 参考 

+ [Design patterns for humans, CN](https://github.com/haiiiiiyun/design-patterns-for-humans-cn)
