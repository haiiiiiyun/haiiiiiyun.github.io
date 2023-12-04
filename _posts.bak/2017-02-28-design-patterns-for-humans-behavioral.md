---
title: 用人话描述的设计模式--行为型设计模式
date: 2017-02-28
writing-time: 2017-02-28 09:52
categories: Programming
tags: Programming design&nbsp;pattern chain&nbsp;of&nbsp;responsibility command iterator mediator memento observer visitor strategy state template&nbsp;method
---

> 注意下面的代码示例都是用 PHP-7 写的。

行为型设计模式
==========================

简单来说
> 它关注于对象间的职责分配。它们与结构型模式的区别在于：它们不只指定结构，还勾画出了相互间的消息传送/通信模式。或者也可以说，它们有助于回答 "如何在软件组件中实现行为？"

Wikipedia 上描述为
> 在软件工程中，行为型设计模式标识了对象间的常见通信模式及其实现模式。通过这样，这些模式增加了实施此种通信的灵活性。

* [责任链(Chain of Responsibility)](#-责任链chain-of-responsibility)
* [命令(Command)](#-命令command)
* [迭代器(Iterator)](#-迭代器iterator)
* [中介者(Mediator)](#-中介者mediator)
* [备忘录(Memento)](#-备忘录memento)
* [观察者(Observer)](#-观察者observer)
* [访问者(Visitor)](#-访问者visitor)
* [策略(Strategy)](#-策略strategy)
* [状态(State)](#-状态state)
* [模板方法(Template Method)](#-模板方法template-method)

🔗 责任链(Chain of Responsibility)
-----------------------

现实案例
> 例如，你在你的账户中设置了三种支付方式 (`A`, `B` 和 `C`); 每个里面都存有不同的金额。`A` 里面有 100 元，`B` 里面有 300 元以及 `C` 里面有 1000 元，并且你的支付偏好选择为先 `A` 再 `B` 最后 `C`。你想要购买价格为 210 元的商品。如何使用责任链，那么首先会检查帐户 `A`，看它是否足够支付，如何可以那么完成支付并且链条到此结束。如果不能，那么请求将传向检查帐户 `B` 中的金额，如果足够那么链条到此结构否则请求将继续传递直到找到合适的处理帐户。这里 `A`, `B` 和 `C` 都是链条中的链接点，而这整个现象就是责任链。

简单来说
> 它用于创建一个对象链。请求从一端进入，并从一个对象传递到另一个，直至找到适合的处理对象。

Wikipedia 上描述为
> 在面向对象设计中，责任链设计模式由命令对象源和一系列的处理对象组成。每个处理对象中都包含有逻辑，用来定义它能处置的命令对象类型; 那些不能处置的其它命令对象都将传递给链条中的下一个处理对象。

**编程示例**

实现上面的帐户的例子。首先定义一个基本的帐户类，其中包含有将各帐户关联起来的逻辑功能，然后再实现几种帐户。

```php
abstract class Account {
    protected $successor;
    protected $balance;

    public function setNext(Account $account) {
        $this->successor = $account;
    }
    
    public function pay(float $amountToPay) {
        if ($this->canPay($amountToPay)) {
            echo sprintf('Paid %s using %s' . PHP_EOL, $amountToPay, get_called_class());
        } else if ($this->successor) {
            echo sprintf('Cannot pay using %s. Proceeding ..' . PHP_EOL, get_called_class());
            $this->successor->pay($amountToPay);
        } else {
            throw Exception('None of the accounts have enough balance');
        }
    }
    
    public function canPay($amount) : bool {
        return $this->balance >= $amount;
    }
}

class Bank extends Account {
    protected $balance;

    public function __construct(float $balance) {
        $this->balance = $balance;
    }
}

class Paypal extends Account {
    protected $balance;

    public function __construct(float $balance) {
        $this->balance = $balance;
    }
}

class Bitcoin extends Account {
    protected $balance;

    public function __construct(float $balance) {
        $this->balance = $balance;
    }
}
```

现在用上面定义的帐户（如 Bank, Paypal, Bitcoin) 准备一个链条

```php
// 创建如下的一个链接
//      $bank->$paypal->$bitcoin
//
// 优先使用银行帐户
//      如果银行帐户无法支付再用 paypal
//      如果 paypal 不能支持再用比特币

$bank = new Bank(100);          // Bank with balance 100
$paypal = new Paypal(200);      // Paypal with balance 200
$bitcoin = new Bitcoin(300);    // Bitcoin with balance 300

$bank->setNext($paypal);
$paypal->setNext($bitcoin);

// Let's try to pay using the first priority i.e. bank
$bank->pay(259);

// 输出会是
// ==============
// Cannot pay using bank. Proceeding ..
// Cannot pay using paypal. Proceeding ..: 
// Paid 259 using Bitcoin!
```

👮 命令(Command)
-------

现实案例
> 一个常见的例子就是在餐厅吃饭。你（即 `客户 Client`）要求服务员（即 `调用者 Invoker`）上菜（即 `命令 Command`），而服务员只是简单地将你的请求传达给厨师（即 `接收者 Receiver`），厨师知道做哪道菜及如何做。
> 另一个例子是你（即 `客户 Client`）使用遥控器（即 `调用者 Invoker`）打开（即 `命令 Command`）电视机（即 `接收者 Receiver`）。

简单来说
> 它允许你在对象中封装行为。该模式背后的主要思想是：提供将客户与接收者解耦的方法。

Wikipedia 上描述为
> 在面向对象编程中，命令模式是一种行为型设计模式，它用对象来封装执行动作或稍后触发事件所需的所有信息。这些信息包括方法名，拥有该方法的对象以及方法参数值等。

**编程示例**

首先定义接收者，并实现它支持的每个行为

```php
// Receiver
class Bulb {
    public function turnOn() {
        echo "Bulb has been lit";
    }
    
    public function turnOff() {
        echo "Darkness!";
    }
}
```

然后定义每个命令都需要实现的接口，并实现一组命令

```php
interface Command {
    public function execute();
    public function undo();
    public function redo();
}

// Command
class TurnOn implements Command {
    protected $bulb;
    
    public function __construct(Bulb $bulb) {
        $this->bulb = $bulb;
    }
    
    public function execute() {
        $this->bulb->turnOn();
    }
    
    public function undo() {
        $this->bulb->turnOff();
    }
    
    public function redo() {
        $this->execute();
    }
}

class TurnOff implements Command {
    protected $bulb;
    
    public function __construct(Bulb $bulb) {
        $this->bulb = $bulb;
    }
    
    public function execute() {
        $this->bulb->turnOff();
    }
    
    public function undo() {
        $this->bulb->turnOn();
    }
    
    public function redo() {
        $this->execute();
    }
}
```

再定义一个 `调用者 Invoker`，客户与它交互来处理任何命令

```php
// Invoker
class RemoteControl {
    
    public function submit(Command $command) {
        $command->execute();
    }
}
```

最后看下客户如何使用

```php
$bulb = new Bulb();

$turnOn = new TurnOn($bulb);
$turnOff = new TurnOff($bulb);

$remote = new RemoteControl();
$remote->submit($turnOn); // Bulb has been lit!
$remote->submit($turnOff); // Darkness!
```

命令模式也可用以实现事务型系统。当一旦执行命令后就保存其执行记录。如果最后一个命令也执行成功了，那样很好，否则只需遍历历史记录，并在所有完成了的命令上执行 `undo` 即可。

➿ 迭代器(Iterator)
--------

现实案例
> 老式收音机是迭代器的很好的例子，用户可以先从某个频道开始，然后使用前后按键来遍历各个频道。或者以 MP3 播放器或电视机为例，它们也可以使用前后按键来遍历歌曲或频道。换句话说，它们都提供了一个接口，来遍历频道，歌曲或广播电台。

简单来说
> 它提供了一种访问对象内所有元素的方法，而避免暴露低层的表示法。

Wikipedia 上描述为
> 在面向对象编程中，迭代器模式是一个设计模式，它使用迭代器来遍历容器并访问容器内的元素。迭代器模式将算法和容器进行了解耦; 但在某些情况下，算法必需是特定于容器的，因而无法解耦。

**编程示例**

在 PHP 中很容易使用 SPL (标准 PHP 库) 来实现。实现上面的广播电台的例子。首先我们定义 `RadioStation`

```php
class RadioStation {
    protected $frequency;

    public function __construct(float $frequency) {
        $this->frequency = $frequency;    
    }
    
    public function getFrequency() : float {
        return $this->frequency;
    }
}
```

然后定义迭代器

```php
use Countable;
use Iterator;

class StationList implements Countable, Iterator {
    /** @var RadioStation[] $stations */
    protected $stations = [];
    
    /** @var int $counter */
    protected $counter;
    
    public function addStation(RadioStation $station) {
        $this->stations[] = $station;
    }
    
    public function removeStation(RadioStation $toRemove) {
        $toRemoveFrequency = $toRemove->getFrequency();
        $this->stations = array_filter($this->stations, function (RadioStation $station) use ($toRemoveFrequency) {
            return $station->getFrequency() !== $toRemoveFrequency;
        });
    }
    
    public function count() : int {
        return count($this->stations);
    }
    
    public function current() : RadioStation {
        return $this->stations[$this->counter];
    }
    
    public function key() {
        return $this->counter;
    }
    
    public function next() {
        $this->counter++;
    }
    
    public function rewind() {
        $this->counter = 0;
    }
    
    public function valid(): bool
    {
        return isset($this->stations[$this->counter]);
    }
}
```

然后可以这样使用

```php
$stationList = new StationList();

$stationList->addStation(new RadioStation(89));
$stationList->addStation(new RadioStation(101));
$stationList->addStation(new RadioStation(102));
$stationList->addStation(new RadioStation(103.2));

foreach($stationList as $station) {
    echo $station->getFrequency() . PHP_EOL;
}

$stationList->removeStation(new RadioStation(89)); // Will remove station 89
```

👽 中介者(Mediator)
========

现实案例
> 一个常见的例子就是当你用手机与别人通话时，你们之间隔有一个网络服务提供商，你们的通话是要通过它，而不是直接传送的。在这种情况下网络服务提供商就是一个中介者。

简单来说
> 中介者模式引入了一个第三方对象（叫中介者 mediator) 来控制两个对象（叫同事 colleagues) 间的交互。它有助于减少彼此通信的类间的耦合性。因为现在它们无需了解对方的实现细节。

Wikipedia 上描述为
> 在软件工程中，中介者模式定义了一个对象，它对一组对象如何交互进行了封装。这种模式被认为是一种行为型模式，因为它能改变程序运行时的行为。

**编程示例**

这里是一个聊天室（即中介者）的最简单的例子，其中的用户（即同事）之间会相互发送消息。

首先，我们定义中介者（即聊天室）

```php
// Mediator
class ChatRoom implements ChatRoomMediator {
    public function showMessage(User $user, string $message) {
        $time = date('M d, y H:i');
        $sender = $user->getName();

        echo $time . '[' . $sender . ']:' . $message;
    }
}
```

然后定义用户（即同事）

```php
class User {
    protected $name;
    protected $chatMediator;

    public function __construct(string $name, ChatRoomMediator $chatMediator) {
        $this->name = $name;
        $this->chatMediator = $chatMediator;
    }
    
    public function getName() {
        return $this->name;
    }
    
    public function send($message) {
        $this->chatMediator->showMessage($this, $message);
    }
}
```

使用

```php
$mediator = new ChatRoom();

$john = new User('John Doe', $mediator);
$jane = new User('Jane Doe', $mediator);

$john->send('Hi there!');
$jane->send('Hey!');

// Output will be
// Feb 14, 10:58 [John]: Hi there!
// Feb 14, 10:58 [Jane]: Hey!
```

💾 备忘录(Memento)
-------

现实案例
> 以计算器（即发起人 originator）为例，当你完成计算后，最后的结果会被保存在内存（即备忘录 memento）中，那样你就能取回它，或许也可以通过一些功能按键（即管理者 caretaker）来恢复它。

简单来说
> 备忘录模式就是关于用某种方式获取或保存对象当前状态的模式，从而使对象能在稍后顺利恢复。

Wikipedia 上描述为
> 备忘录模式是一种软件设计模式，它提供了将对象恢复到先前状态的能力（使用回滚来撤销操作）。

通常当你需要提供一些撤销功能时非常有用。

**编程示例**

以文本编辑器为例，它会不时地保存当前状态，从而当你需要时可以恢复。

首先定义我们的备忘录对象，它能用于保存编辑器的状态

```php
class EditorMemento {
    protected $content;
    
    public function __construct(string $content) {
        $this->content = $content;
    }
    
    public function getContent() {
        return $this->content;
    }
}
```

然后定义编辑器（即发起人 originator），它会用到备忘录对象

```php
class Editor {
    protected $content = '';
    
    public function type(string $words) {
        $this->content = $this->content . ' ' . $words;
    }
    
    public function getContent() {
        return $this->content;
    }
    
    public function save() {
        return new EditorMemento($this->content);
    }
    
    public function restore(EditorMemento $memento) {
        $this->content = $memento->getContent();
    }
}
```

然后可以这样使用

```php
$editor = new Editor();

// Type some stuff
$editor->type('This is the first sentence.');
$editor->type('This is second.');

// Save the state to restore to : This is the first sentence. This is second.
$saved = $editor->save();

// Type some more
$editor->type('And this is third.');

// Output: Content before Saving
echo $editor->getContent(); // This is the first sentence. This is second. And this is third.

// Restoring to last saved state
$editor->restore($saved);

$editor->getContent(); // This is the first sentence. This is second.
```

😎 观察者(Observer)
--------

现实案例
> 一个不错的案例是求职者，他们订阅到一些职位发布网站，然后当出现匹配的工作机会时，他们就会得到通知。

简单来说
> 它在对象间定义了一种依赖关系，从而当某个对象的状态改变后，它的所有依赖对象都将得到通知。

Wikipedia 上描述为
> 观察者模式是一种软件设计模式，其内的一个对象（称为主题），会维护一组依赖对象（称为观察者），当对象的状态改变后，它通常通过调用依赖对象的某个函数来自动通知它们。

**编程示例**

实现以上的例子。首先定义求职者，他需要得到工作职位的发布通知

```php
class JobPost {
    protected $title;
    
    public function __construct(string $title) {
        $this->title = $title;
    }
    
    public function getTitle() {
        return $this->title;
    }
}

class JobSeeker implements Observer {
    protected $name;

    public function __construct(string $name) {
        $this->name = $name;
    }

    public function onJobPosted(JobPost $job) {
        // Do something with the job posting
        echo 'Hi ' . $this->name . '! New job posted: '. $job->getTitle();
    }
}
```

再定义工作职位发布网站，求职者将会订阅

```php
class JobPostings implements Observable {
    protected $observers = [];
    
    protected function notify(JobPost $jobPosting) {
        foreach ($this->observers as $observer) {
            $observer->onJobPosted($jobPosting);
        }
    }
    
    public function attach(Observer $observer) {
        $this->observers[] = $observer;
    }
    
    public function addJob(JobPost $jobPosting) {
        $this->notify($jobPosting);
    }
}
```

然后这样使用

```php
// Create subscribers
$johnDoe = new JobSeeker('John Doe');
$janeDoe = new JobSeeker('Jane Doe');

// Create publisher and attach subscribers
$jobPostings = new JobPostings();
$jobPostings->attach($johnDoe);
$jobPostings->attach($janeDoe);

// Add a new job and see if subscribers get notified
$jobPostings->addJob(new JobPost('Software Engineer'));

// Output
// Hi John Doe! New job posted: Software Engineer
// Hi Jane Doe! New job posted: Software Engineer
```

🏃 访问者(Visitor)
-------

现实案例
> 考虑到迪拜旅游的例子。游客只需通过某种途径（例如签证）进入迪拜。抵达后，他们就可以自己去参观迪拜的任何地方，要参观这里的任何一个地方，都无需再获得许可或做一些跑腿的工作; 只需告诉他们地址，他们就能去参观。访问者模式也允许你那样做，它能帮你添加要访问的地点，从而使你能参观尽可能多的地方，而无需另做额外的工作。

简单来说
> 访问者模式允许你无需进行修改就能将进一步的操作添加到对象中。
 
Wikipedia 上描述为
> 在面向对象编程和软件工程中，访问者设计模式是将算法与其所操作的对象结构进行分离的一种方法。这种分离的实际结果是：具有在不修改现有对象结构的情况下，将新操作加入到对象结构中的能力。

**编程示例**

以一个模拟动物园为例，里面有多种动物，并且我们需要它们发出声音。我们将用访问者模式实现这个例子

```php
// 被访问者
interface Animal {
    public function accept(AnimalOperation $operation);
}

// 访问者
interface AnimalOperation {
    public function visitMonkey(Monkey $monkey);
    public function visitLion(Lion $lion);
    public function visitDolphin(Dolphin $dolphin);
}
```

再实现一些动物类

```php
class Monkey implements Animal {
    
    public function shout() {
        echo 'Ooh oo aa aa!';
    }

    public function accept(AnimalOperation $operation) {
        $operation->visitMonkey($this);
    }
}

class Lion implements Animal {
    public function roar() {
        echo 'Roaaar!';
    }
    
    public function accept(AnimalOperation $operation) {
        $operation->visitLion($this);
    }
}

class Dolphin implements Animal {
    public function speak() {
        echo 'Tuut tuttu tuutt!';
    }
    
    public function accept(AnimalOperation $operation) {
        $operation->visitDolphin($this);
    }
}
```

实现访问者

```php
class Speak implements AnimalOperation {
    public function visitMonkey(Monkey $monkey) {
        $monkey->shout();
    }
    
    public function visitLion(Lion $lion) {
        $lion->roar();
    }
    
    public function visitDolphin(Dolphin $dolphin) {
        $dolphin->speak();
    }
}
```

然后可以这样使用

```php
$monkey = new Monkey();
$lion = new Lion();
$dolphin = new Dolphin();

$speak = new Speak();

$monkey->accept($speak);    // Ooh oo aa aa!    
$lion->accept($speak);      // Roaaar!
$dolphin->accept($speak);   // Tuut tutt tuutt!
```

我们本可以只通过动物类的继承结构实现上面的功能，但是那么的话，当我们需要将新动作添加到动物类时，就必须修改动物类。而现在我们无需修改它们。例如，当要求将跳的行为加入动物类时，我们只需简单地创建一个新访问者即可。

```php
class Jump implements AnimalOperation {
    public function visitMonkey(Monkey $monkey) {
        echo 'Jumped 20 feet high! on to the tree!';
    }
    
    public function visitLion(Lion $lion) {
        echo 'Jumped 7 feet! Back on the ground!';
    }
    
    public function visitDolphin(Dolphin $dolphin) {
        echo 'Walked on water a little and disappeared';
    }
}
```

再这样使用

```php
$jump = new Jump();

$monkey->accept($speak);   // Ooh oo aa aa!
$monkey->accept($jump);    // Jumped 20 feet high! on to the tree!

$lion->accept($speak);     // Roaaar!
$lion->accept($jump);      // Jumped 7 feet! Back on the ground! 

$dolphin->accept($speak);  // Tuut tutt tuutt! 
$dolphin->accept($jump);   // Walked on water a little and disappeared
```

💡 策略(Strategy)
--------

现实案例
> 考虑排序的例子，我们实现了冒泡排序，但是随着数据增多，冒泡排序变得越来越慢。为了解决这个问题，我们又实现了快速排序。但是现在虽然快速排序算法在大数据集中运行很好，在小数据集上却很慢。为了处理这种情况，我们实现了一种策略：小数据集时用冒泡排序，大数据集时用快速排序。

简单来说
> 策略模式允许你根据情况切换算法或策略。

Wikipedia 上描述为
> 在计算机编程中，策略模式（也称为政策模式）是一种行为型软件设计模式，它使得能在运行时选择算法的行为。
 
**编程示例**

实现上面的例子。首先定义策略接口，并实现不同的策略

```php
interface SortStrategy {
    public function sort(array $dataset) : array; 
}

class BubbleSortStrategy implements SortStrategy {
    public function sort(array $dataset) : array {
        echo "Sorting using bubble sort";
         
        // Do sorting
        return $dataset;
    }
} 

class QuickSortStrategy implements SortStrategy {
    public function sort(array $dataset) : array {
        echo "Sorting using quick sort";
        
        // Do sorting
        return $dataset;
    }
}
```
 
然后定义客户，它能使用任何一个策略

```php
class Sorter {
    protected $sorter;
    
    public function __construct(SortStrategy $sorter) {
        $this->sorter = $sorter;
    }
    
    public function sort(array $dataset) : array {
        return $this->sorter->sort($dataset);
    }
}
```

然后这样使用

```php
$dataset = [1, 5, 4, 3, 2, 8];

$sorter = new Sorter(new BubbleSortStrategy());
$sorter->sort($dataset); // Output : Sorting using bubble sort

$sorter = new Sorter(new QuickSortStrategy());
$sorter->sort($dataset); // Output : Sorting using quick sort
```

💢 状态(State)
-----

现实案例
> 假设你正在使用绘画程序，你选择画笔绘画。现在画笔会根据所选的颜色改变其行为，比如当你选择红色后它将画出红色，选择蓝色后将画出蓝色等。

简单来说
> 它能使你在状态改变后修改类的行为。

Wikipedia 上描述为
> 状态模式是一种行为型软件设计模式，它用面向对象的方式实现了一个状态机。在状态模式中，通过将每个单独状态实现为状态模式接口的一个继承类，而状态间的转变通过调用在模式的父类中定义的函数来实现，从而实现一个状态机。
> 状态模式可以解释为是一种策略模式，它能通过调用在模式接口中定义的方法来切换当前策略。

**编程示例**

以文本编辑器为例，它能让我们修改输入文本的状态，比如选择粗体后，它就会用粗体书写，选择斜体就会用斜体等。

首先定义状态接口，并实现一些状态类

```php
interface WritingState {
    public function write(string $words);
}

class UpperCase implements WritingState {
    public function write(string $words) {
        echo strtoupper($words); 
    }
} 

class LowerCase implements WritingState {
    public function write(string $words) {
        echo strtolower($words); 
    }
}

class Default implements WritingState {
    public function write(string $words) {
        echo $words;
    }
}
```

再定义编辑器

```php
class TextEditor {
    protected $state;
    
    public function __construct(WritingState $state) {
        $this->state = $state;
    }
    
    public function setState(WritingState $state) {
        $this->state = $state;
    }
    
    public function type(string $words) {
        $this->state->write($words);
    }
}
```

然后这样使用

```php
$editor = new TextEditor(new Default());

$editor->type('First line');

$editor->setState(new UpperCaseState());

$editor->type('Second line');
$editor->type('Third line');

$editor->setState(new LowerCaseState());

$editor->type('Fourth line');
$editor->type('Fifth line');

// Output:
// First line
// SECOND LINE
// THIRD LINE
// fourth line
// fifth line
```

📒 模板方法(Template Method)
---------------

现实案例
> 假设我们要造房子，造房子的步骤看起来像这样:
> - 打地基
> - 砌墙
> - 盖屋顶
> - 加盖其它层
> 
> 这些步骤的顺序永远都不会变，即你不可能先盖屋顶再砌墙等。但是每一步的具体操作都是可以修改的，比如说，你可以砌木墙，聚酯纤维墙或者石头墙。
 
简单来说
> 模板方法定义了某特定算法如何执行的框架，但执行步骤的具体实现则推迟到子类中去完成。
 
Wikipedia 上描述为
> 在软件工程中，模板方法是行为型设计模式的一种，它定义了操作中的某个算法的程序框架，并将一些步骤推迟到子类中去实现。它能在不修改算法结构的情况下，重新定义算法中的某些步骤。

**编程示例**

假设我们有一个构建工具，它能帮助我们进行测试，代码检查，构建，生成构建报告（比如代码覆盖率报告，代码检查报告等）以及部署应用至测试服务器。

首先我们定义一个基类用来指定构建算法的框架

```php
abstract class Builder {
    
    // Template method 
    public final function build() {
        $this->test();
        $this->lint();
        $this->assemble();
        $this->deploy();
    }
    
    public abstract function test();
    public abstract function lint();
    public abstract function assemble();
    public abstract function deploy();
}
```

然后进行各种实现

```php
class AndroidBuilder extends Builder {
    public function test() {
        echo 'Running android tests';
    }
    
    public function lint() {
        echo 'Linting the android code';
    }
    
    public function assemble() {
        echo 'Assembling the android build';
    }
    
    public function deploy() {
        echo 'Deploying android build to server';
    }
}

class IosBuilder extends Builder {
    public function test() {
        echo 'Running ios tests';
    }
    
    public function lint() {
        echo 'Linting the ios code';
    }
    
    public function assemble() {
        echo 'Assembling the ios build';
    }
    
    public function deploy() {
        echo 'Deploying ios build to server';
    }
}
```

接着，可以这样使用

```php
$androidBuilder = new AndroidBuilder();
$androidBuilder->build();

// Output:
// Running android tests
// Linting the android code
// Assembling the android build
// Deploying android build to server

$iosBuilder = new IosBuilder();
$iosBuilder->build();

// Output:
// Running ios tests
// Linting the ios code
// Assembling the ios build
// Deploying ios build to server
```


# 参考 

+ [Design patterns for humans, CN](https://github.com/haiiiiiyun/design-patterns-for-humans-cn)
