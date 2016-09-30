---
title: Python 的行话术语大全
date: 2016-09-30
writing-time: 2016-09-30 12:56
categories: Python
tags: Python
---


**ABC(计算机语言)**

> 是由 Leo Geurts, Lambert Meertens 和 Steven Pemberton 创建的一种编程语言。开发了 Python 的 Guido van Rossum，在 20 世纪 80 年代曾以程序员的身份实现了 ABC 的环境。块由缩进来组织，内置元组和字典，元组拆分，for 循环的语义，以及对所有序列化类型的一致处理等这些 Python 的鲜明特性都是借鉴自 ABC。

**Abstract base class(ABC)**

> 一个不能被实例化，只能被子类化的类。Python 中的接口由 ABC 形式化表示。除了可以继承一个 ABC 外，类也可以通过注册成一个 ABC 的虚拟子类来声明实现了某个接口。

**accessor**

> 一个实现用于访问单个数据属性的方法。一些开发者将 accessor 作为一个通用术语使用，包括 getter 和 setter 方法，而另一些开发者使用时只表述 getter，setter 表述为 mutator。

**aliasing**

> 为相同的对象分配两个或多个名字。例如，在 `a = []; b = a` 这个例子中，变量 a 和 b 是同一个列表对象的别名。在任何一种为避免混淆，只需忘掉变量是保存对象的盒子这样的想法（一个对象不能同时在两个盒子中）。最好将它们想成是贴在对象上的标签（一个对象可以有多个标签）。在任何一种变量用于存储对象引用的语言中，别名会很自然地发生。为避免混淆，只需忘掉变量是保存对象的盒子这样的想法（一个对象不同同时在两个盒子中）。最好将它们理解成是贴在对象上的标签（一个对象可以有多个标签）。

**argument**

> 当调用一个函数时，传递的一个表达式。在 Python 中，*argument* 和 *parameter* 几乎就是同义词。关于这两个术语的区别和使用方法的更多信息，见 **parameter** 节。

**attribute**

> 方法和数据属性(如 Java 术语中的 "fields" 等）在 Python 中都被称作属性。方法是一个属性，而这个属性恰好是一个可调用对象（通常是一个函数，但不是必需的）。

**BDFL**

> Benevolent Dictator For Life，是 Python 语言的创造者 Guido van Rossum 的别称。

**binary sequence**

> 含有字节元素的序列化类型的通用术语。内置的二进制序列类型有 byte，bytearray 和 memoryview。

**BOM**

> Byte Order Mark（字节序标识符），该字节串可能会出现在以 UTF-16 编码的文件的开头处。一个 BOM 就是字符 U+FEFF(ZERO WIDTH NO-BREAK SPACE)，它编码后在大数端的 CPU 上生成 b'\xfe\xff'，在小数端的 CPU 上生成 b'\xff\xfe'。因为 Unicode 中没有 U+FFFE 这个字符，因此一旦出现该字节串就能明确揭示出该编码使用的字节序。可能有点多余，但在 UTF-8 文件中可以会找到编码成 b'\xef\xbb\xbf' 的 BOM。

**bound method**

> 一个需要通过实例访问的方法，因为它被绑定到了那个实例。任何一个方法实际上都是一个描述子 descriptor(实现了 __get__)，当被访问时，它将自身封装到一个对象中，该对象将方法绑定到实例。该对象就是一个绑定方法。调用它可以不用传递 self 值。例如，通过以下赋值 `my_method = my_obj.method`，该绑定函数以后可以通过 `my_method()` 调用。

**build-in function(BIF)**

> 一个与 Python 解析器捆绑的函数，它使用低层实现语言编写（例如，CPython 用的 C; Jython 用的 Java 等等）。该术语通过只表示那些无需导入就能用的函数。但是内置的模块像 sys, math, re 等也包含有内置函数。

**byte string**

> 很不幸 Python 3 中仍然是用这个名字来表示 bytes 和 bytearray。在 Python 2 中， str 类型实际上是一个字节字符串，因此这个术语用来将 str 字符串和 unicode字符串进行区分是说得通的。而在 Python 3 中还坚持使用这个术语就没有意义了，Python 3 中最好用 byte sequence 表述。

**bytes-like object**

> 一个通用的字节序列。最常见的 bytes-like 类型是 bytes, bytearray 和 memoryview。但是其它支持低层 CPython buffer 协议的对象，如果它们的元素都是单字节的话，也有符合条件的。

**callable object**

> 一个可以通过调用操作符 () 进行调用的对象，它能返回一个结果或者执行某些操作。在 Python 中有七种可调用对象: 用户定义的函数，内置函数，内置方法，实例方法，生成器函数，类，实现了 `__call__` 特殊方法的类实例。

**CamelCase**

> 标识的一种写法约定：相连的每个词首字母都大写（如 ConnectionRefusedError）。PEP-8 建议类名应该以 CamelCase 约定命名，但是 Python 的标准库并没有遵循这个建议。见 snake_case 术语。

**CheeseShop**

> [Python Package Index(PyPi)](https://pypi.python.org/pypi) 的原名，以 Monty Python 剧中的奶酪店命名。目前 https://cheeseshop.python.org 仍然可访问。 见 PyPI 术语。

**class**

> 一种用于定义新类型的程序结构，它具有数据属性和可指定在其上进行某些操作的方法。见 type 术语。

**code point**

> 0 到 0x10FFFF 区间内的一个整数，用于标识 Unicode 字符数据库中的一个记录。在 Unicode 7.0 中，只有不到 3% 的代码点被分配了字符。在 Python 文档中，该术语可能有两点表述。例如， `chr` 函数说需要一个整数 "code point"，而其相应的 ord 函数，描述为返回一个 "Unicode code point"。

**code smell**

> 表明该程序设计可能会有问题的一种代码编写模式。例如，过度使用 `ininstance` 来检查具有类是一个 code smell，因为它使程序在将来难以扩展处理新的类型。

**codec**

> (encoder/decoder)，一个具有编码和解析函数的模块，通常用于进行 str 和 bytes 间的相互转换，虽然 Python 也有几个 codecs 可以用于执行 bytes 到 bytes，以及 str 到 str 的转换。

**collection**

> 一种通用术语，用于表述这类数据结构：该数据结构由多个项组成，并且项能被单独存取。 一些 collections 可以包含任意类型的对象（见 container 术语），而另一些只能包含一种简单原子类型的对象（见 flat sequence 术语）.list 和 bytes 都是 collection， 但是 list 是一个 container，而 bytes 是一个 flat sequence。


参考： 《Fluent Python》中 Python Jargon 章。
