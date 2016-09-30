---
title: Python 的行话术语大全
date: 2016-09-30
writing-time: 2016-09-30 12:56--2016-10-01 22:15
categories: Python
tags: Python
---


**ABC(计算机语言)**

> 是由 Leo Geurts, Lambert Meertens 和 Steven Pemberton 创建的一种编程语言。开发了 Python 的 Guido van Rossum，在 20 世纪 80 年代曾以程序员的身份实现了 ABC 的环境。块由缩进来组织，内置元组和字典，元组拆分，for 循环语义，以及对所有序列化类型的一致处理等这些 Python 的鲜明特性都借鉴自 ABC。

**Abstract base class(ABC)**

> 一个不能被实例化，只能被子类化的类。Python 中的接口由 ABC 形式化表示。除了可以继承一个 ABC 外，类也可以通过注册成一个 ABC 的虚拟子类来声明实现了某个接口。

**accessor**

> 一个实现了可用于访问单个数据属性的方法。一些开发者将 accessor 作为一个通用术语使用，即包含 getter 和 setter 方法，而另一些开发者使用时只表述 getter，setter 表述为 mutator。

**aliasing**

> 为相同的对象分配两个或多个名字。例如，在 `a = []; b = a` 这个例子中，变量 a 和 b 都是同一个列表对象的别名。在任何一种变量用于存储对象引用的语言中，别名会很自然地发生。为避免混淆，只需忘掉变量是保存对象的盒子这样的想法（一个对象不能同时保存在两个盒子中）。最好将它们理解成是贴在对象上的标签（一个对象可以有多个标签）。

**argument**

> 指调用一个函数时，所传递的一个表达式。在 Python 中，*argument* 和 *parameter* 几乎就是同义词。关于这两个术语的区别和使用方法的更多信息，见术语 parameter。

**attribute**

> 方法和数据属性(如 Java 术语中的 "fields" 等）在 Python 中都被称作属性。方法也是一个属性，只不过这个属性恰好是一个可调用对象（通常是一个函数，但不是必需的）。

**BDFL**

> Benevolent Dictator For Life，是 Python 语言的创造者 Guido van Rossum 的别称。

**binary sequence**

> 一个用于表述含有字节元素的序列化类型的通用术语。内置的二进制序列类型有 byte，bytearray 和 memoryview。

**BOM**

> Byte Order Mark（字节序标识符），该字节串可能会出现在以 UTF-16 编码的文件的开头处。一个 BOM 就是字符 U+FEFF(ZERO WIDTH NO-BREAK SPACE)，它编码后在大数端的 CPU 上生成 b'\xfe\xff'，在小数端的 CPU 上生成 b'\xff\xfe'。因为 Unicode 中没有 U+FFFE 这个字符，因此一旦出现该字节串就能明确判断出该编码使用的字节序。可能有点多余，但在 UTF-8 文件中可能会找到编码成 b'\xef\xbb\xbf' 的 BOM。

**bound method**

> 一个需要通过实例访问的方法，因为它被绑定到了那个实例。任何一个方法实际上都是一个描述子 descriptor(实现了 __get__)，当被访问时，它将自身封装到一个对象中，该对象将方法绑定到实例。该对象就是一个绑定方法。调用它可以不用传递 self 值。例如，通过以下赋值 `my_method = my_obj.method`，该绑定函数以后可以通过 `my_method()` 调用。

**build-in function(BIF)**

> 一个与 Python 解析器捆绑的函数，它使用低层实现语言编写（例如，CPython 用的 C; Jython 用的 Java 等等）。该术语通常只表述那些无需导入就能使用的函数。但是内置模块如 sys, math, re 等也含有内置函数。

**byte string**

> 很不幸 Python 3 中仍然还用这个名字表示 bytes 和 bytearray。在 Python 2 中， str 类型实际上是一个字节字符串，因此使用该术语将 str 字符串和 unicode字符串进行区分是说得通的。而在 Python 3 中还坚持使用这个术语就没有意义了，Python 3 中最好用 byte sequence 表述。

**bytes-like object**

> 一个通用的字节序列。最常见的 bytes-like 类型是 bytes, bytearray 和 memoryview。但是其它支持低层 CPython buffer 协议的对象，如果它们的元素都是单字节的话，也有符合条件的。

**callable object**

> 一个可以通过调用操作符 () 进行调用的对象，它能返回一个结果或者执行某些操作。在 Python 中有七种可调用对象: 用户定义的函数，内置函数，内置方法，实例方法，生成器函数，类，实现了 `__call__` 特殊方法的类实例。

**CamelCase**

> 标识的一种写法约定：相连的每个词首字母都大写（如 ConnectionRefusedError）。PEP-8 建议类名应该以 CamelCase 约定命名，但是 Python 的标准库并没有遵循这个建议。见 snake_case 术语。

**CheeseShop**

> [Python Package Index(PyPi)](https://pypi.python.org/pypi) 的原名，以 Monty Python 剧中的奶酪店命名。目前 https://cheeseshop.python.org 仍然可访问。 见 PyPI 术语。

**class**

> 一种用于定义新类型的程序结构，它具有数据属性和可在其上进行某些操作的方法。见 type 术语。

**code point**

> 0 到 0x10FFFF 区间内的一个整数，用于标识 Unicode 字符数据库中的一个记录。在 Unicode 7.0 中，只有不到 3% 的代码点被分配了字符。在 Python 文档中，该术语可能有两种表述。例如， `chr` 函数说需要一个整数 "code point"，而其相应的 ord 函数，描述为返回一个 "Unicode code point"。

**code smell**

> 表明该程序设计可能会有问题的一种代码编写模式。例如，过度使用 `isinstance` 来检查具体类就是一种 code smell，因为它使程序在将来难以扩展以应对新的类型。

**codec**

> (encoder/decoder)，一个具有编码和解析函数的模块，通常用于进行 str 和 bytes 间的相互转换，虽然 Python 也有几个 codecs 可以用于执行 bytes 到 bytes，以及 str 到 str 的转换。

**collection**

> 一种通用术语，用于表述这类数据结构：它由多个项组成，并且项能被单独存取。 一些 collection (集合) 可以包含任意类型的对象（见 container 术语），而另一些只能包含一种简单原子类型的对象（见 flat sequence 术语）。list 和 bytes 都是集合， 但是 list 是一个 container，而 bytes 是一个 flat sequence。

**considered harmful**

> Edsger Dijkstra 的一封名叫 “Go To Statement Considered Harmful” 的信为那些批评某种计算机科学技术的论文标题建立了一种范式。Wikipedia 上的 ["Considered harmful" 文章](http://en.wikipedia.org/wiki/Considered_harmful) 举了一些例子，包括由 Eric A. Meyer 写的 ["Considered Harmful Essays Considered Harmful"](http://meyerweb.com/eric/comment/chech.html)。


**constructor**

> 非正式地，类中的 `__init__` 实例方法被称为构造器，因为它的语义和 Java 的构造器非常相似。但是，`__init__` 更恰当的名字应该叫初始化器，因为它实际上并没有构造该实例，它只是接收这个实例为自己的 self 参数。*constructor* 这个术语用于描述类中的 `__new__` 方法会更好，Python 在调用 `__init__` 前调用该方法，它实际上负责创建并返回实例对象。见 initializer 术语。

**container**

> 一个能保存其它对象的引用的对象。Python 中的大多数 collection 类型都是容器，但有些不是。例如 *flat sequence*，它是 collection，但不是 container。

**context manager**

> 一个实现了 `__enter__` 和 `__exit__` 这两个特殊方法的对象，用于 `with` 块中。

**coroutine**

> 一个用于并行程序开发的 generator(生成器)，该生成器通过 `coro.send(value)` 从一个 schedulere (调度器) 或 event loop (事件循环器) 中获取数值。该术语可用于描述 generator function (生成器函数)，也可以描述通过调用生成器函数所获得的 generator object (生成器对象)。见 generator 术语。

**CPython**

> 标准 Python 解析器，用 C 实现。该术语只在以下情况下使用：讨论特定于某种实现的特性时，或讨论 PyPy 等有多种可用 Python 解析器时。

**CURD**

> 即 Create, Read, Update 和 Delete 的字母缩写，它们是任何数据存储型应用系统的四个基本功能。

**decorator**

> 一个可调用对象 A，调用能返回另一个可调用对象 B，对 A 的调用要在一个可调用对象 C 的定义体前使用语法 `@A` 进行。当碰到这种代码时，Python 解析器调用 `A(C)` 并将结果 B 绑定到之前分配给 C 的变量，从而事实上将 C 的定义替换成了 B。如果该目标可调用对象 C 是一个函数，那么 A 就是一个函数装饰器;如果 C 是一个类，那么 A 就是一个类装饰器。

**deep copy**

> 拷贝一个对象时，对象中的所有属性自身也被拷贝。对比 shallow copy。

**descriptor**

> 一个实现了 `__get__`, `__set__`, `__delete__` 这三个特殊方法中的一个或多个方法的类，当它的一个实例成为了另一个类（即 managed class， 受管理类) 的类属性时，即成为一个 descriptor (描述子)。描述子对受管理类中的受管理属性的存取和删除操作进行管理，并通常将数据保存到 managed instance (受管理实例）中。

**docstring**

> 即 documentation string 的简写。当一个模块、类或函数中的首行语句是一个字符串时，Python 会将该字符串作为该对象的 *docstring*，并保存到该对象的 `__doc__` 属性上。见 doctest 术语。

**doctest**

> 是一个模块，它包含一些函数用于解析和运行嵌在 Python 模块的 docstring 中或纯文本文件中的示例代码。也可以在命令行中这样使用:

```bash
python -m doctest module_with_tests.py
```

**DRY**

> Don't Repeat Yourself--一种软件工程原则，它表述为 "Every piece of knowledge must have a single, unambiguous, authoritative representation within a system"。它最先出现在 Andy Hunt 和 Dava Thomas 写的 《The Pragmatic Programmer》(Addison-Wesley, 1999) 中。

**duck typing**

> 多态的一种形式: 函数可作用于任何实现了特定方法的对象上，而不需要考虑它们的类或者显式接口声明。

**dunder**

> double underscores 的简写，用于简化那些前后带有双下划线的特殊方法和属性名的发音（如 __len__ 读作 "dunder len")。

**dunder method**

> 见术语 dunder 和 special methods 。

**EAFP**

> 是 "It's easier to ask forgiveness than permission" 的缩写，它源于计算机先驱 Grace Hopper，Python 开发人员引用它来阐述这样的动态编程实践: 对属性的存取都可假定属性是存在的，因而不必进行事先测试，如果不存在的话，只需捕获相关异常即可。`hasattr` 函数的 docstring 实际上这样描述它的工作原理: “通过调用 getattr(object, name) 并捕猎 AttributeError。"

**eager**

> 一个 iterable object (可迭代对象），它会立马构建出其所有的元素。在 Python 中，一个 list comprehension (列表推导器) 是一个 eager。相较于 lazy。

**fail-fast**

> 一种系统设计原则，它建议错误应该尽早汇报。相比于大部分动态语言，Python 更加遵循该原则。例如，它没有 "undefined" 值: 变量没有初始化前一旦P被引用就会产生错误，并且 `my_dict[k]` 时当 k 不存在时会抛出异常 (相较于 JavaScript)。另一个例子，Python 中通过元组拆分进行的并行赋值只有当元组中的每个元素都匹配时才能进行，而 Ruby 却是不声不响地处理了元素个数不匹配的情况: 忽略 = 右边没有使用的元素，或者将 nil 值赋给左边多余的变量。

**falsy**

> 表示任何一个值 x, 该值 x 当调用 `bool(x)` 时会返回 False; 在布尔上下文中，例如控制 if 或 while 循环的表达式中，Python 默认使用 `bool` 来计算对象值。它的相反的值是 truthy。

**file-like object**

> 在官方文档中非正式地用于表述实现了文件协议的对象，这些对象都有像 `read`, `write`, `close` 等方法。常见的变体有: 包含已编码字符串以便于面向行读写的文本文件，`StringIO` 实例--内存中的文本文件和包含未编码字节数据的二进制文件。后者可能有缓冲，也可能没有。标准文件类型自 Python 2.6 开始都定义在 `io` 模块中。

**first-class function**

> 编程语言中能作为 first-class object (一类对象) 的任何函数 (即可以在运行时创建，能赋值给变量，能作为参数传递，能作为另一个函数的返回值返回)。Python 函数都是一类函数。

**flat sequence**

> 一种序列类型: 它实际存储其元素的值，而不是存储到其它对象的引用。内置的类型如 `str`, `bytes`, `bytearray`, `memoryview` 和 `array.array` 等都是 flat sequence (简单序列)。而 `list`, `tuple` 和 `collections.deque` 都是 container sequence (容器序列)。见术语 container。

**function**

>严格来说，是一个从 `def` 块或 `lambda` 表达式运行而来的对象。非正式地，`function` 这个词用于描述任何可调用对象，如方法、甚至有时也可以是类。官方的 [内置函数](http://docs.python.org/library/functions.html) 列表中也含有一些内置类，像 `dict`, `range` 和 `str` 等。见 callable object。

**genexp**

> *generator expression* 的缩写。

**generator**

> 一个由 generator function (生成器函数) 或 generator expression (生成器表达式) 构建的迭代器，它在产生值时无需遍历整个集合; 典型的例子是一个产生 Fibonacci 序列的生成器，由于该序列是无限的，因而不适合在存于一个集合中。该术语除了表述从生成器函数调用中返回的对象外，有时也用于表述该生成器函数本身。

**generator function**

> 一个在函数体中使用了 `yeild` 关键字的函数。当被调用时，generator function (生成器函数) 会返回一个 generator (生成器)。

**generator expression**

> 一种由括号包围的表达式，它使用和 *list comprehension (列表推导式)* 相同的语法，只不过它返回的不是列表，而是一个生成器。一个 *generator expression (生成器表达式)* 可以被理解成列表推导式的 *lazy* 版本。见术语 lazy。

**generic function**

> 指一组函数：它们意在以可定制的方式为不同的对象类型实现相同的操作。在 Python 3.4 中，`functools.singledispatch` 装饰器是创建 generic function (通用函数) 的标准方法。在其它语言中也叫做 multimethods。

**GoF book**

> 《Design Patterns: Elements of Resuable Object-Oriented Software》(Addison Wesley, 1995) 的别称。它的作者即所谓的四人帮: Erich Gamma, Richard Helm, Ralph Johnson 和 John Vlissides。

**hashable**

> 一个对象为 `hashable` 即指它同时含有 `__hash__` 和 `__eq__` 方法，并且有以下限制: 它的哈希值永远不会变且当 `a == b` 成立时 `hash(a) == hash(b)` 也必须为 True。大多数内置的不可修改类型都是 hashable 的，但是元组只有当其每个元素都 hashable 时才是 hashable 的。

**higher-order function**

> 指一个能接受另一个函数作为参数的函数，如 `sorted`, `map` 和 `filter` 等，或者指一个将函数作为返回值的函数，如 Python 装饰器。

**idion**

> "A manner of speaking that it natural to native speakers of a language"，摘自 Princeton WordNet。

**import time**

> 指一个模块初始化运行的时刻，此时模块代码被 Python 解析器加载，并从上到下进行运算，然后被编译成字节码。这是类和函数执行定义并变成活跃对象的时刻，也是执行装假器的时刻。

**initializer**

> 更适合 `__init__` 方法的名字(相较于 constructor 构造器)。`__init__` 的任务是初始化作为 self 参数接收来的实例。而实际的实例构建过程是由 `__new__` 函数完成的。见术语 constructor。

**iteralbe**

> 任何一个只要通过 `iter` 这个内置函数能获取一个 iterator (迭代器) 的对象。iterable object (可迭代对象) 可作为 for 循环、推导式和元组拆分时的元素源。那些实现了 `__iter__` 方法并返回一个迭代器的对象都是 iterable 的; 而其它实现了 `__getitem__` 方法的对象可能也是 iterable 的。

**iterable unpacking**

> *tuple unpacking* 的一个现代的，更加准确的同义词。见 parallel assignment。

**iterator**

> 任何一个实现了 `__next__` 方法的的对象，`__next__` 不接收参数，调用它时会返回序列中的下一个元素，或者当序列中已无元素时会抛出 `StopIteration` 异常。Python 的 iterator (迭代器) 也会实现 `__iter__` 方法，因而它们也是 iterable 的。经典的迭代器，根据原来的设计模式，是从集合中返回元素。generator (生成器) 也是一个迭代器，但是它更加灵活。见术语 generator。

**KISS principle**

> 即 "Keep It Simple, Stupid"。提倡寻求尽可能简单，稳定的解决方案。这句话是由 Kelly Johnson 提出的，Johnson 是一个天才的航空航天工程师，他在真正的 51 区工作，20 世纪的很多高级飞行器都是由他设计出来的。

**lazy**

> 一个按需产生元素的可迭代对象。在 Python 中，相较于 eager，生成器是 lazy 的。

**listcomp**

> *list comprehension* 的简写。

**list comprehension**

> 一种由方括号包围的表达式: 它使用 for 和 in 关键字，并对来自一个或多个可迭代对象中的元素进行处理和过滤，从而创建出一个列表。list comprehension (列表推导式) 是即时计算的，见术语 eager。

**liveness**

> 一个异步的、多线程的或者分布式的系统，当 "某些好事终会发生” (即虽然一些期望的计算现在还没有发生，但它最终会完成的) 时，即展现了它的 liveness (活性)。如果系统死锁了，那它就失去了它的活性。

**magic method**

> 同 *special method*。

**managed attribute**

> 一个由描述子对象管理的公共属性。虽然 *managed attribute (受管理属性)* 是在 *managed class (受管理类)* 中定义的，但是它操作起来像一个实例属性 (即它通常在每个实例中都有一个值，并保存在 storage attribute 中)。见术语 descriptor。

**managed class**

> 一个使用描述子对象来管理其至少一个属性的类。见术语 descriptor。

**managed instance**

> managed class 的一个实例。见 managed attribute 和 descriptor。

**metaclass**

> 一种其实例也是类的类。默认地，Python 的类是 `type` 的实例，例如，`type(int)` 返回类 `type`，因此 `type` 是一个 `metaclass`。用户自定义的 metaclass 可以通过继承 type 来创建。

**metaprogramming**

> 一种使用有关其自身的运行时信息来修改其行为的程序编写实践。例如，*ORM* 可能会检查数据模型类的声明来确定如何去验证数据库记录中的数据域，以及如何将数据库类型转换成 Python 中的类型。

**monkey patching**

> 在运行时动态地修改一个模块、类，或者函数，通常是为了添加功能和修正 Bug。因为它是在内存中实现的，并没有修改源代码，因此一个 monkey patch 只在当前运行的进程中有效。Monkey patch 破坏了封装性并且趋于和修复部分的实现细节紧密藕合，因此它们只被认为是临时的解决方法，不是代码集成的一种推荐技术。

**mixin class**

> 一种意在与一个或更多个类一起使用在多重类继承树的类。一个 mixin 类不能被初始化，mixin class 的具体子类也应该继承其它的非 mixin class。

**mixin method**

> 一个具体的方法实现: 该方法由一个 ABC 或 mixin class 提供。

**mutator**

> 见术语 accessor。

**name mangling**

> 自动将私有属性从 `__x` 重命名为 `_MyClass__x` 的过程，它由 Python 解析器在运行时执行。

**nonoverriding descriptor**

> 一种未实现 `__set__` 的描述子，因而不会干涉受管理实例上的受管理属性的设置过程。其结果是，如果受管理实例上设置了一个同名属性，将隐藏该实例上的描述子。也称作 nondata descriptor 或者 shadowable descriptor。相较于 overriding descriptor。

**ORM**

> Object-Relation Mapper--一种 API: 它以 Python 类和对象的形式提供访问数据库和记录的方式，提供方法调用来执行数据库操作。SQLAlchemy 是一个流行地独立 Python ORM; Django 和 Web2py 框架都有它们自己捆绑的 ORM。

**overriding descriptor**

> 一种实现了 `__set__` 的描述子，因而它会干预并覆盖在受管理实例上设置受管理属性的企图。也称为 data descriptor 或者 enforced descriptor。相较于 nonoverriding descriptor。

**parallel assignment**

> 用来将一个可迭代对象中的多个元素赋值给多个变量，使用像 `a, b = [c, d]` 这样的语法--也称为 destructing assignment (解构赋值)。这是 tuple unpacking (元组拆分) 的常见用法。

**parameter**

> 函数会声明成具有 0 到多个 “形式参数”，它们都是未绑定的本地变量。当函数被调用时，传递的参数或 “实参” 会绑定到这些变量。通常，arguemnt 指实参，而 parameter 指形参，但是 Python 文档和 API 中这两者都是混用的。见术语 argument。

**prime (动词)**

> prime 动词的含义是 “填充、事先准备好”，它在一个协程上调用 `next(coro)`，使其运行到首个 `yeild` 表达式处，从而使其能准备好接收由接下来的 `coro.send(value)` 调用发送的数值。

**PyPI**

> 即 [Python Package Index](https://pypi.python.org)，上面有超过 60,000 个包，也称作 Cheese shop (见术语 Cheese shop)。PyPI 发音为 "pie-P-eye"，以避免与 PyPy 混淆。

**PyPy**

> Python 编程语言的另一种实现，它所使用的工具链将 Python 的一个子集编译成了机器码，因此解析器的源代码实际上是用 Python 编写的。PyPy 还包含一个 JIT，用于将用户程序实时转换成机器码--像 Java VM 做的一样。截止 2014 年 12 月，根据 [公布的评测数据](http://speed.pypy.org)，PyPy 平均比 CPython 快 6.8 倍。PyPy 发音为 "pie-pie"，以避免与 PyPI 混淆。

**Pythonic**

> 用于称赞符合语言习惯的 Python 代码，这些代码很好地利用了语言特性，从而显得简洁、易读，通常也更快。也用于表述 API，这些 API 使得熟练的 Python 程序员使用它们进行编程时显得很自然。

**refcount**

> 每个 CPython 对象在内部保存的引用计算器，以便决定它自身何时能被垃圾回收器回收。

**REPL**

> Read-Eval-Print Loop，一个交互式的控制台，例如标准的 python 或者其它的像 ipython, bpython 和 Python Anywhere 等。

**sequence**

> 某些可迭代数据结构的通用名字: 这些数据结构有已知的大小 (如 len(s)) 并且允许使用基于 0 的整数索引进行访问 (如 s[0])。*sequence* 一开始就是一个 Python 术语，但是直到 Python 2.6 它才正式地作为一个抽象类在 `collections.abc.Sequence` 中定义。

**serialization**

> 将一个对象从其内存结构转换成一个二进制或面向文本的结构，以便于存储或传输，它能使用的方式能便于以后在相同或不同的系统上重建该对象的一个克隆版本。`pickle` 模块支持将任意的 Python 对象序列化成一个二进制格式。

**shallow copy**

> 对象的拷贝版本与原对象共享属性对象的引用。相较于 deep copy。也见 aliasing。

**singleton**

> 一个对象是某个类的唯一存在的实例--通常不是偶尔引起的，而是有意设计该类以避免其能创建多个实例。有一个设计模式也叫 Singleton，是编写这种类的指南。Python 中的 None 对象就是一个 singleton (独子)。

**slicing**

> 通过使用切片表示法来生产某个序列的子集，比如 `my_sequence[2:6]`。Slicing (切片) 通常是通过复制数据来创建一个新的对象; 特别如 `my_sequence[:]` 会创建整个序列的一个 shallow copy (浅复制版本)。而一个 memoryview 对象通过切片生成的新 memoryview 对象能与源对象共享数据。

**snake_case**

> 标识的一种写法约定：用下划线 (_) 连接单词，例如 `run_until_complete`。PEP-8 称这种风格为 “单词都小写，并以下划线分隔” 并且推荐以它来命名函数，方法，参数和变量。而对于包，PEP-8 建议名字中的各名词直接相连接，不使用分隔符。Python 标准库中有很多 `snake_case` 型的标识例子，但是也有很多标识中的单词没有用分隔符 (例如 `getattr`, `classmethod`, `isinstance`, `str.endswith` 等)。见术语 CamelCase。

**special method**

> 具有特殊名字的方法，如 `__getitem__`，它的开头和结尾都有双下划线。

**storage attribute**

> managed instance (受管理实例) 中的一个属性，用于保存某个受描述子管理的属性值。

**strong reference**

> 该引用使被引用的对象在 Python 中一直保持活跃。相较于 weak reference。

**tuple unpacking**

> 将来自一个可迭代对象中的元素赋值给一组变量 (例如: `first, second, third = my_list`)。Python 开发人员一般都使用该术语，但是 `iterable unpacking` 也越来越受到青睐。

**truthy**

> 表示任何一个值 x, 该值 x 当调用 `bool(x)` 时会返回 True; 在布尔上下文中，例如控制 if 或 while 循环的表达式中，Python 默认使用 `bool` 来计算对象值。它的相反的值是 falsy。

**type**

> 它表述有关程序数据的每个特定类别，它通过一组可能值及可运用于其上的操作来定义。有些 Python type (类型) 与机器数据类型很接近 (如 `float` 和 `bytes`)，而其它的会有相应的扩展 (如 `int` 不受限于 CPU 的字大小，`str` 能保存多字节的 Unicode 数据点)，同时还有很高级的抽象类型 (如 `dict`, `deque` 等)。类型可以是用户自定义的，也可以是内置于解析器中的 ( 一个 “内置” 类型)。在 Python 2.2 之前，type/class 还没有统一起来，那时 type 和 class 是不同的实体，用户自定义的类无法对内置的类型进行扩展。而自 Python 2.2 后，内置类型和新型的类开始变得相互兼容，class (类) 成为了 type (类型) 的一个实例。而在 Python 3 中，所有类都是新型类。见 class 和 metaclass。

**unbound method**

> 一个实例方法如果直接通过类来访问就没有绑定到该实例上; 从而被称为是一个 "unbound method (未绑定的方法)"。要想顺利进行，对一个未绑定方法的调用必须显式地传递一个类的实例作为首个参数。那个实例将赋给该方法的 self 参数。见术语 bound method。

**uniform access principle**

> Bertrand Meyer, Eiffel 语言的创建者，写道: "All services offered by a module should be available through a uniform notation, which does not betray whether they are implemented through storage or through computation." 属性和描述子使得在 Python 中能实现 uniform access principle (统一访问原则)。由于没有 `new` 操作符，调用函数和初始化对象看起来是一样的，这也是该原则的另一种形式: 调用者无需知道被调用对象是一个类、一个函数、或者是任何其它的可调用对象。

**user-defined**

> 在 Python 文档中 *user* 这个单词几乎总是指你和我--使用 Python 语言的程序员--相较于那些实现 Python 解析器的开发人员。因此术语 "user-defined class" 意指一个用 Python 编写的类，相较于内置的用 C 编写的类，比如说 `str`。

**view**

> Python 3 中的 view (视图) 指的是通过 `dict` 的 `.keys()`, `.values()` 和 `.items()` 方法返回的特殊数据结构，它无需进行数据复制，就能为我们提供一个关于 dict 键和值的一个动态视图，而在 Python 2 中，由于这些方法返回列表，因而有数据复制的过程。所有 dict 视图都是可迭代的，并且都支持 `in` 操作符。另外，如果被视图引用的元素都是 hashable 的，那么该视图也会实现 `collections.abc.Set` 接口。所有由 `.keys()` 方法返回的视图都属于这种情况，而当 dict 的值是 hashable 时，由 `.items()` 方法返回的视图也是 hashable 的。

**vitual subclass**

> 一个没有继承 superclass，但又使用 `TheSuperClass.register(TheSubClass)` 注册过的类。参见 [abc.ABCMeta.register](http://bit.ly/1DeDbKf) 的文档。

**wart**

> 该语言的不好的特性。Andrew Kuchling 的那篇很有名的文章 "Python warts" 已经被 BDFL 认可了，并在他设计 Python 3 时做出打破向后兼容性这样的决定中起来了很大作用，因为如果不这样，提到的大部分缺陷都将无法修复。Kuchling 提到的很多问题都已在 Python 3 中修复了。

**weak reference**

> 一种特殊种类的对象引用，它不增加 *referent* 对象引用计数值。弱引用由 `weakref` 模块中的某个函数和数据结构创建。

**YAGNI**

> "You Ain't Gonna Need It", 该标语用来避免实现那些现在不需要，而基于未来假定会需要的那些功能。

**Zen of Python**

> 在 Python 2.2 版本之后的任何 Python 终端中输入 `import this` 即可显示。


参考： 《Fluent Python》中 Python Jargon 章。
