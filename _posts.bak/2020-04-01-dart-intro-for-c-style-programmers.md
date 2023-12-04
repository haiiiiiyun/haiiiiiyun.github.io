---
title: C 系程序员20分钟学会 Dart 语言
date: 2020-04-09
writing-time: 2020-04-01--2020-04-09
categories: dart
tags: dart
---

# 1. 概述

Dart 是 Google 下一代操作系统 Fuchsia 的御用程序开发语言，而是 App 跨平台框架 Flutter 使用的开发语言。它是一种面向对象的语言，使用 C 风格语法，揉合了 Javascript、Python、Java 等语言的相关特性。

如果之前熟悉这几门语言，可以快速入门。

# 2. 应知就会

## 2.1. 语句结束符

同 C 语言一样，Dart 所有语句都以 `;` 结束。

## 2.2. 注释

同 Javascript，单行用 `//`, 多行用 `/*  */`。

如果要支持文档生成工具，则单行注释用 `///`，多行注释用 `/**  */`, 例如：

```dart
/// This is a documentation comment

/**
  This , too,
  is a
  documentation comment.
*/
```

## 2.3. 变量声明与类型

Dart 是强类型语言，即所有变量都是有类型的。

同 C 语言一样，可以在声明变量时指定类型 `<specific_type> variable;` ，如：

```dart
int a = 3;
```

也可以同 Javascript 中一样，用 `var a = 3;` 声明，此时 Dart 会从赋值语句的右值推导出变量的类型，如本例中将推导出 `a` 变量是 `int` 型。
那么之后该变量的类型就确定了，不能再赋值其它类型的值了，例如本例中再给 a 赋值字符串值编译会通不过： `a = "String Value";`。

如果将变量声明为 `dynamic` 类型，那么当变量赋值为一个类型的值后，可随时再次赋值为其它类型的值，如：

```dart
dynamic x = 42;
x = "Hello World";
```

同 Java 一样， Dart 中的一切都是对象，都最终继承自 `Object` 类，因此将变量声明为 `Object` 类型类似于声明为 `dynamic` 类型，可以赋值任何类型的值，如：

```dart
Object x = 42;
x = "Hello World";
```

两都区别是：  `dynamic` 类型告诉 Dart 不要查检变量的类型，即关闭类型检测功能，因此若引用 dynamic 变量上不存在的方法时，编译是能通过的，但在运行时出错; 而引用
`Object` 类上不存在的方法时，编译就不能通过。


## 2.4. 常量和 final 值

同 Java 类似，常量值用 `const` 修饰，常量值在编译时就被确定，不能修改，如：

```dart
const x = "Hello";
const String y = "world";
```

而 `final` 变量可以在运行时赋值，但只能赋值一次，例如想确定程序启动时间值，可以声明为一个 `final` 变量，如：

```dart
final x = DateTime.now();
```

`const` 不仅能修饰变量，也可以修饰值，如：

```dart
List lst = const [1, 2, 3];
lst[0] = 999; // compile error
```

## 2.5. 类型

基本类似用小写开头，如 `int, double, num, bool`, 其中 `num` 是 `int, double` 的父类。其它类型以大写开头，如 `String, List, Map`。

### 2.5.1. 数字型

同 C 一样，`int, double, num` 都支持 `+, -, *, /, %`。数字型唯一特殊的操作符是 `~/`，表示返回除法结果的整数部分，功能同 Python 中的 `//` 操作符，如：

```dart
int x = 3;
double y = 2.0;
x = x ~/ y;
print(x); // 1
```

同 C 中一样，dart 中 `x = x + y` 也可以缩写为 `x += y`，这种缩写同样适用于 `-, *, /, %` 和 `~/` 操作符，如 `x = x ~/ y` 可写为 `x ~/= y`。

也有 C 中类似的 `v++`, `++v`, `v--`, `--v` 等前后缀操作符及三元条件表达式如： `x = a ? b : c`。

Dart 中还支持一种特有的二元条件表达式，如 `x = a ?? b;`，表示当 a 有值时（即不为 null 值，声明的变量未初始化时值默认为 null)，x 赋值为 a，否则赋值为 b。


### 2.5.2. 字符串型 String

同 Javascript 中类似，字符串即可以用单引号 `'xxx'`，也可以用双引号 `"xxx"` 表示。字符串中若包含 `${val}` 形式的变量引用，则生成的字符串结果中会自动用变量值进行替换，这是一种很方便的功能，如：

```dart
String name = "Haiiiiiyun";
String greeting = "Hello ${name}"; // Hello Haiiiiiyun
String greeting = "Hello $name"; // 也可省略 {}，直接用 $var
```

字符串与数字间可进行相互转换，如：

```dart
int i = 42;
double d = 4.2;
String si = i.toString(); // "42"
String sd = d.toString(); // "4.2";

int i2 = int.parse(si); // 42
double d2 = double.parse(sd); // 4.2
```

### 2.5.3. 布尔型  bool

只有 `true` 和 `false` 两个值，注意，在 if while 等条件判断表达式的值不能隐匿转换成 `bool` 类型值，这和一般的语言都不同，例如：

```dart
if (1) { // 
    print("true");
}
```

不能编译通过，因为 `1` 不能转换成 `bool` 型值 `true`。

### 2.5.4. 枚举型 Enum

类型 C，可用 `enum` 定义枚举类型，如： `enum Week{ Mon, Tue, Wed, Thu, Fri, Sat, Sun };`。

其每个值都有一个 index 值，如 `Week.Mon.index` 的值为 `0`，`Week.Tue.index` 值为 1，以此类推。枚举值适用于 `switch` 语句。


### 2.5.5. List

List 类似 Javascript 中的数组，它是有序的，因此有 `indexOf` 方法，操作有：

```dart
List lst = ['a', 'b', 'c'];
lst.add('d'); // ['a', 'b', 'c', 'd']
lst.removeLast(); // ['a', 'b', 'c']
print(lst.indexOf('a')); // 0
```

Set 和 Python 中的 Set 类似，是无序数组，且其中的元素不会重复：

```dart
Set chars = Set();
chars.addAll([ "a", "b", "c" ]);
chars.add("a"); // 还是 ["a", "b", "c"]
chars.remove("b"); // ["a", "c"]
chars.contains("a")); // true
chars.containsAll([ "a", "b" ])); // false
```

### 2.5.6. Map

类似 Javascript 中的 dict，操作有：

```dart
Map<String, String> countries = Map();
countries['India'] = "Asia";
countries["Germany"] = "Asia"; // wrong
countries["France"] = "Europe";
countries["Brazil"] = "South America";

if (countries.containsKey("Germany")) {
    countries["Germany"] = "Europe"; // update
    print(countries); // {India: Asia, Germany: Europe, France: Europe, Brazil: South America}
}

countries.remove("Germany");
print(countries); // {India: Asia, France: Europe, Brazil: South America}
```

## 2.6. 类型测试和类型转换

用 `is` 关键字进行类型测试，用 `as` 关键字进行类型转换，如

```dart
// Pig 是 Animal 的子类

if(animal is Pig) {
    (animal as Pig).oink(); //叫声
}
```

## 2.7. 流程控制

`if`, `else` 和 C 中完全一样。条件表达式也可用 `||`, `&&` 和 `!` 进行组合。

`switch` 也和 C 中一样。


## 2.8. 循环

`while` 和 `do while` 循环和 C 中完全一样。同时 `continue` 和 `break` 语句也一样使用。

### 2.8.1 for 循环

第一个 for 循环形式和 C 类型，如：

```dart
for (var i=0; i<10; i++){
    print(i);
}
```

第二个 `for-in` 形式适用于可迭代对象，如 List, Iterator 等：

```dart
List lst = ['a', 'b', 'c'];
for (var char in lst) {
    print(char);
}
```

## 2.9 异常处理

异常处理和 Java 类似。基类是 `Error` 和 `Exception`，若要捕获某种类型的异常，用 `on <SpecificException> catch(e)`，
若不关心捕获的异常类型，直接用 `catch(e)`，而 `finally` 段中的代码不管有没有异常捕获到最会最后执行，如：

```dart
try {
    somethingThatMightThrowAnException();
} on FormatException catch (fe) {
    print(fe);
} on Exception catch (e) {
    Print("Some other Exception: " + e);
} catch (u) {
    print("Unknown exception");
} finally {
    print("All done!");
}
```

# 3. 函数与对象

Dart 中所有变量都是对象，因此函数也是对象，其类型是 `Function`。

函数定义同 C 中类似，如：

```dart
int add(int a, int b)
{
    return a + b;
}

```

即定义函数时要指定函数返回值类型，及参数的类型。如果没有指定返回值类型，默认为 void。

类似 C， `main(List<String> args)` 函数是程序的入口函数。


## 3.1 命名函数参数

普通函数调用时，其参数值由其位置确定，如上面的函数调用：

```dart
int x = add(1, 2); // 3
```

命名函数参数在 `{}` 中指定，如：

```dart
int add2(int init, {int a, int b}){
    return init + a + b;
}

print(add2(1, b:2, a:1)); // 4
```

其中的命名参数值在调用时用形如 `x:y` 形式指定，并且参数位置与定义时的位置无关，但必须在普通位置函数值之后。


## 3.2. 参数默认值

可以指定命名参数的默认值，如：


```dart
int add3({int init=0, int a, int b}){
    return init+a+b;
}

print(add3(a:1, b:2)); // 3
print(add3(init:10, a:1, b:2)); // 13
```


## 3.3. 可选参数

将参数放在 `[]` 指定其为可选参数，在调用时可不用提供参数值，如：

```dart
String add4(int a, int b, [String c]){
    return "$c: ${a+b}";
}

main(){
    print(add(1,2));
    print(add2(1, a:1,b:2));
    print(add3(a:1, b:2));
    print(add3(init:10, a:1, b:2));

    print(add4(1,2)); // null: 3
    print(add4(1,2, "Sum")); // Sum: 3
}
```

## 3.4. 匿名函数

类似 Javascript 和 Java 中的匿名函数，创建的匿名函数可以赋值给 Function 的变量，之后该变量和普通的函数一样调用，如：

```dart
Function add5 = (int a, int b) {
    return a+b;
};

print(add5(1,2)); // 3
```

如果函数体如本例一样，只是一条 return 语句，则可以简写为 `fat arrow` 形式（和 Python lambda 函数类似)：

```dart
Function add6 = (int a, int b) => a+b;
print(add6(1,2)); // 3
```

## 3.5. 高阶函数

函数是对象，可以作为函数参数值传递。而能接受函数值作为参数的函数即为高阶函数。

例如：

```dart
Function add6 = (int a, int b) => a+b;

int operator(Function op_fun, int a, int b)
{
    return op_fun(a, b);
}

print(operator(add6, 1, 2)); //3
```

这里的 `operator` 函数即为高阶函数。

## 3.6. 闭包 Closure

闭包是一个特殊的函数，也叫闭包函数。其特点时：当定义闭包函数时，闭包函数将定义函数时其父作用域中的变量值都固定下来，从而当调用闭包函数时，使用的也是定义时的变量值。

这在函数里定义闭包函数时特别明显（函数体中可以定义函数），如：

```dart

Function adder(int step)
{
    return (a) => a + step;
}

var adder1 = adder(1);
print(adder1(1)); // 2

var adder10 = adder(10);
print(adder10(1)); //11
```

闭包函数 `adder1` 将 step 值固定为定义时的 `1`，而 `adder10` 将 step 值固定为 `10`。

# 4. 类与面向对象

同 Java 类似，类用 `class` 定义，如：

```dart
class Animal {
    int numLegs = 0;
    int numEyes = 0;

    Animal(int numLegs, int numEyes){
        this.numLegs = numLegs;
        this.numEyes = numEyes;
    }

    void eat() {
        print("Animals eat everything depending on what type it is.");
    }
}

var a1 = new Animal(4, 2);
var a2 = Animal(4, 2); // new 关键字可省略
```

创建类实例也用 `new ClassName(arg)`，其中的 `new` 关键字可省略，这样创建类实例和调用函数在形式上就一样了。

## 4.1 属性和方法

其中的 `numLegs` 和 `numEyes` 是属性，可以直接访问实例中的属性值，如：

```dart
var a1 = new Animal(4, 2);
a1.numLegs = 2;
print(a1.numLegs); //2
```

其中的 `eat()` 是方法，可以和函数调用一样调用类实例上的方法。


访问属性和方法时，如果对象为空，会抛出异常，类似 Typescript, Dart 中的 `?.` 操作符用来访问对象属性时，如果对象为 null，则不访问，
从而避免了抛出异常：

```dart
var a1 = Animal(4, 2);
a1 = null;
print(a1?.numLegs); //不会抛出异常。
```

静态属性和静态方法都用 `static` 修改，它们是类级别的属性和方法，可以直接在类上访问：

```dart
class Circle {
    static const pi = 3.14;
    static void drawCicle() {
        //...
    }
}

print(Circle.pi); // 3.14
Circle.drawCicle();
```

## 4.2. 构造方法

类中和类名相同的方法是构造方法，构造方法可以有参数，例如本例中的构造方法，其功能只是设置类的各属性值，像这种构造方法在 Dart 中可以简写为：

```dart
class Animal {
    int numLegs;
    int numEyes;

    Animal(int this.numLegs, int this.numEyes);

    void eat() {
        print("Animals eat everything depending on what type it is.");
    }
}
```

可定义多个构造方法，方法名要么和类名 `<ClassName>` 相同，要么以 `<ClassName>.` 为前缀，例如：

```dart
class Animal {
    int numLegs = 0;
    int numEyes = 0;

    Animal(int this.numLegs, int this.numEyes); //构造方法

    Animal.namedConstructor(int this.numLegs, int this.numEyes) { //另一个构造方法
    }

    void eat() {
        print("Animals eat everything depending on what type it is.");
    }
}
```

### 4.2.1. 默认构造方法

和 C++ 类似，如果没有声明构造方法，编译器会自动生成一个无参数的默认构造方法，该默认构造方法也会调用父类的无参构造方法。

### 4.2.2. 构造方法不能继承

子类不能继承父类的构造方法。子类的构造方法通过 `super` 调用父类的构造方法，并且和 C++ 中类似，将这种父类调用放在初始化列表中，如：

```dart
class Cat extends Animal {
    Cat(): super(4,2) {
    }
}
```

初始化列表中的代码是最先执行的。


### 4.2.3. 重定向构造方法

一个构造方法通过初始化列表，只调用另一个构造方法，没有方法体，如：

```dart
class Animal {
    int numLegs = 0;
    int numEyes = 0;

    Animal(int this.numLegs, int this.numEyes); //构造方法

    Animal.cat(): this(4, 2); // 重定向构造方法

    void eat() {
        print("Animals eat everything depending on what type it is.");
    }
}
```


### 4.2.4. getter 和 setter

```dart
import 'dart:math';

class Square {
    double width;

    
    Square(this.width);

    double get area => width * width;

    set area(inArea) => width = sqrt(inArea);
}

var s = Square(5);
print(s.area); // 25.0

s.area = 16;
print(s.width); // 4.0
```

用 `get` 关键字设置 getter, 用 `set` 关键字设置 setter。

## 4.3. 子类

和 Java 一样，生成子类的语法是 `class SubClass extends SuperClass {}`。
Dart 不支持多重继承，只能 extends 自一个父类。

## 4.4. 抽象类

类似 Java, 抽象类用 `abstract` 修饰，抽象类中可以只声明方法，也可以有默认的实现：

```dart
abstract class Shape {
    double area(); //只有声明

    void draw(){ //有默认实现体
        print("draw here");
    }
}
```

抽象类不能实例化。


## 4.4. 接口 interface

Dart 中类与接口不分，普通类和抽象类都是接口。类不能多重继承，但可以实现多个接口，用 `implements` 关键字，多个接口用 `,` 分隔，如：

```dart
abstract class Shape {
    double area(); //只有声明

    void draw(){ //有默认实现体
        print("draw here");
    }
}

class Circle implements Shape {

    @override
    double area(){
    }

    @override
    void draw(){ //有默认实现体
        print("draw here");
    }
}
```

如果用 `implements` 实现接口，则必须实现(重写)接口中的全部方法和属性，不管接口中有没有默认实现。

## 4.6. mixin

mixin 是实现代码复用的一种方式。

Dart 中类与mixin不分，普通类和抽象类都是mixin。类不能多重继承，但可以引入多个mixin，用 `with` 关键字，多个mixin用 `,` 分隔，如：

```dart
class Shape {
    double area() {
    }

    void draw(){
        print("draw here");
    }
}

class Circle with Shape {
}

var c = Circle();
c.draw();
```

同接口不同，子类无需实现 mixin 中已实现了的方法。

## 4.7. 特殊方法

### 4.7.1 call()

如果类中实现了 call 方法，则类实例可以像函数一样调用，而实际上执行的就是实例中的 `call(...)` 方法，如：

```dart
class CallableClassWithoutArgument {
    String output = "Callable class";

    void call() {
        print(output);
    }
}

class CallableClassWithArgument {
    call(String name) => print("$name");
}

var withoutArgument = CallableClassWithoutArgument();
withoutArgument(); // Callable class

var withArgument = CallableClassWithArgument();
print(withArgument("John Smith")); //  John Smith
```

### 4.7.2 操作符重载方法

Dart 类中可以重载以下操作符：`<, >, <=, >=, -, +, /, ~/, *, %, |, ^, &, <<, >>, [], []=, ~, ==`。

重载方法是在类中实现 `operator `及操作符号为名的方法，例如：


```dart
class MyNumber {
    num val;
    num operator + (num n) => val * n;
    MyNumber(this.val);
}

MyNumber mn = MyNumber(5);
print(mn+2); // 10
```

这里，将 + 功能重载为乘法功能。



# 5. 包

每个 dart 文件都是一个包 package。

用 `import 'URL'` 的形式导入其它包，其中的 `URL` 的形式为 `schema:path`， schema 的值有：

+ `dart`: Dart 内置的包，如 `import 'dart:math'`
+ `package`: 第三方包，如 `import 'package:flutter/material.dart'`
+ 没有 schame部分：表示只导入当前项目中的相关包，如 `import 'NotesModel.dart'`
 
可以用 `show` 关键字限定只导入包中相关属性，如 `import "NotesModel.dart" show NotesModel, notesModel;`。
也可以用 `hide` 关键字限定只排除包中相关属性，其它属性都导入，如 `import "NotesModel.dart" show NotesModel, notesModel;`。

如果包中的属性名有冲突，可以用 `as` 关键字将导入的包重命名，如 `import 'dart:math' as math;`。



# 资源

+ [flutter 官网](https://flutter.dev/)
+ [flutter 社区中文资源](https://flutter.cn/)
