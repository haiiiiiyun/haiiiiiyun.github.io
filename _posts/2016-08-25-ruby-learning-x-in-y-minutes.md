---
title: Ruby 基础知识(Learn X in Y minutes)
date: 2016-08-25
writing-time: 2016-08-25 15:34--22:46
categories: programming
tags: Ruby
---

安装 Ruby:

```shell
$ sudo apt-get install ruby

$ ruby -v
ruby 2.3.1p112 (2016-04-26) [i386-linux-gnu]
```

开启 Ruby 交互式终端：

```shell
$ irb
irb(main):001:0> 
```


```ruby
# 这是注释

=begin
这是多行注释的写法，不般都不用这种注释
=end

# Ruby 中最最重要的概念是：一切都是对象。

# 数字是对象

3.class #=> Fixnum

3.to_s #=> "3"


# 一些基本算术符
1 + 1 #=> 2
8 - 1 #=> 7
10 * 2 #=> 20
35 / 5 #=> 7
2**5 #=> 32
5 % 3 #=> 2

# 位操作符
3 & 5 #=> 1
3 | 5 #=> 7
3 ^ 5 #=> 6

# 算术符只是语法糖
# 本质是调用了对象上的方法
1.+(3) #=> 4
10.* 5 #=> 50

# 特殊值也是对象
nil # 等同于其它语言中的 null
true # truth
false # falsehood

nil.class #=> NilClass
true.class #=> TrueClass
false.class #=> FalseClass

# 相等比较
1 == 1 #=> true
2 == 1 #=> false

# 不相等比较
1 != 1 #=> false
2 != 1 #=> true

# 除了 false 本身外，nil 是唯一另外一个会被解析成 false 的值

!nil   #=> true
!false #=> true
!0     #=> false

# 更多比较
1 < 10 #=> true
1 > 10 #=> false
2 <= 2 #=> true
2 >= 2 #=> true

# 组合比较操作符，左边小于右边，返回 -1, 相等返回 0, 大于返回 1
1 <=> 10 #=> -1
10 <=> 1 #=> 1
1 <=> 1 #=> 0

# 逻辑操作符
true && false #=> false
true || false #=> true
!true #=> false

# 另外一种版本的逻辑操作符，它们的优先级更低。
# 它们用于控制流结构中，用来串接语句，直到返回 true 或 false。

# `do_something_else` 只当 `do_something` 返回 true 时才被调用
do_something() and do_something_else()
# `log_error` 只当 `do_something` 返回 false 时才会被调用
do_something() or log_error()


# 字符串也是对象

'I am a string'.class #=> String
"I am a string too".class #=> String

# 双引号的字符串可以自动进行占位符字符替换
placeholder = 'use string interpolation'
"I can #{placeholder} when using double quoted strings"
#=> "I can use string interpolation when using double quoted strings"

# 优先使用单引号的字符串表示
# 因为双引号表示的字符串会进行一些额外的处理

# 字符串可以相互组合，但不能和数字组全
'hello ' + 'world'  #=> "hello world"
'hello ' + 3 #=> TypeError: can't convert Fixnum into String
'hello ' + 3.to_s #=> "hello 3"

# 字符串操作符
'hello ' * 3 #=> "hello hello hello "

# 添加到字符串后面
'hello' << ' world' #=> "hello world"

# 打印输出，并在末尾加回车
puts "I'm printing!"
#=> I'm printing!
#=> nil

# 打印输出，不加回车
print "I'm printing!"
#=> I'm printing! => nil

# 变量
x = 25 #=> 25
x #=> 25

# 赋值操作会返回所赋的值
# 这意味着能进行连续赋值：

x = y = 10 #=> 10
x #=> 10
y #=> 10

# 变量名的一般写法
snake_case = true

# 使用有意义的变量名
path_to_project_root = '/good/name/'
path = '/bad/name/'

# 符号（也是对象）
# 符号是不可修改的可重用的常量，在内部使用一个整数值表示。
# 使用它们即能实现字符串的可描述性，又提高了性能

:pending.class #=> Symbol

status = :pending

status == :pending #=> true

status == 'pending' #=> false

status == :approved #=> false

# 数组

# 这是一个数组
array = [1, 2, 3, 4, 5] #=> [1, 2, 3, 4, 5]

# 数组可以包含不同类型的项

[1, 'hello', false] #=> [1, "hello", false]

# 可以通过索引值进行存取
# 从前往后进行
array[0] #=> 1
array.first #=> 1
array[12] #=> nil

# 和算术符一样，[var] 也是语法糖
# 本质上是调用对象的 [] 方法
array.[] 0 #=> 1
array.[] 12 #=> nil

# 从后往前进行
array[-1] #=> 5
array.last #=> 5

# 使用一个开始索引及长度来获取一个子数组
array[2, 3] #=> [3, 4, 5]

# 将数组反序
a=[1,2,3]
a.reverse! #=> [3,2,1]

# 使用区间表达来获取一个子数组
array[1..3] #=> [2, 3, 4]

# 向数组添加新项
array << 6 #=> [1, 2, 3, 4, 5, 6]
# 也可以这样添加
array.push(6) #=> [1, 2, 3, 4, 5, 6]

# 检查项是否包含在数组中
array.include?(1) #=> true

# 哈希表是 Ruby 的主要键/值对表示法。
# 哈希表用花括号表示：
hash = { 'color' => 'green', 'number' => 5 }

hash.keys #=> ['color', 'number']

# 哈希表能通过键快速查询
hash['color'] #=> 'green'
hash['number'] #=> 5

# 对不存在的键进行查询会返回 nil
hash['nothing here'] #=> nil

# 自 Ruby 1.9 后，当符号用作键时，可以用这样的语法：

new_hash = { defcon: 3, action: true }

new_hash.keys #=> [:defcon, :action]

# 查验键和值是否存在
new_hash.key?(:defcon) #=> true
new_hash.value?(3) #=> true

# 数组和哈希表都是可变的
# 它们都共享一组很有用的方法，如：each, map, count 等

# 控制流

if true
  'if statement'
elsif false
  'else if, optional'
else
  'else, also optional'
end

for counter in 1..5
  puts "iteration #{counter}"
end
#=> iteration 1
#=> iteration 2
#=> iteration 3
#=> iteration 4
#=> iteration 5

# 但是！，没有人会用上面这种方式进行循环。
# 我们应该使用 "each" 方法，然后再传给它一个块
# 所谓块就是可以传给像 "each" 这样的方法的代码段。
# 它类似于其它语言中的 lambdas, 匿名函数或闭包。
#
# 区间的 "each" 方法会对区间中的每个元素运行一次块。
# 我们将 counter 作为一个参数传给了块。
# 调用带有块的 "each" 方法看起来如下：

(1..5).each do |counter|
  puts "iteration #{counter}"
end
#=> iteration 1
#=> iteration 2
#=> iteration 3
#=> iteration 4
#=> iteration 5

# 也可以将块包含在一个花括号中：
(1..5).each { |counter| puts "iteration #{counter}" }

# 数据结构中的内容也可以使用 each 来遍历。
array.each do |element|
  puts "#{element} is part of the array"
end
hash.each do |key, value|
  puts "#{key} is #{value}"
end

# 如果还需要索引值，可以使用 "each_with_index"
# 变量
array.each_with_index do |element, index|
  puts "#{element} is number #{index} in the array"
end

counter = 1
while counter <= 5 do
  puts "iteration #{counter}"
  counter += 1
end
#=> iteration 1
#=> iteration 2
#=> iteration 3
#=> iteration 4
#=> iteration 5

# 还有很多有用的循环遍历函数。
# 如 "map", "reduce", "inject" 等。
# map 举例：
array = [1,2,3,4,5]
doubled = array.map do |element|
  element * 2
end
puts doubled
#=> [2,4,6,8,10]
puts array
#=> [1,2,3,4,5]

grade = 'B'

case grade
when 'A'
  puts 'Way to go kiddo'
when 'B'
  puts 'Better luck next time'
when 'C'
  puts 'You can do better'
when 'D'
  puts 'Scraping through'
when 'F'
  puts 'You failed!'
else
  puts 'Alternative grading system, eh?'
end
#=> "Better luck next time"

# case 也可以用区间
grade = 82
case grade
when 90..100
  puts 'Hooray!'
when 80...90
  puts 'OK job'
else
  puts 'You failed!'
end
#=> "OK job"

# 异常处理
begin
  # code here that might raise an exception
  raise NoMemoryError, 'You ran out of memory.'
rescue NoMemoryError => exception_variable
  puts 'NoMemoryError was raised', exception_variable
rescue RuntimeError => other_exception_variable
  puts 'RuntimeError was raised now'
else
  puts 'This runs if no exceptions were thrown at all'
ensure
  puts 'This code always runs no matter what'
end

# 函数

def double(x)
  x * 2
end

# 函数（及所有的块）都默认返回最后一行语句的值
double(2) #=> 4

# 括号是可选的，只在有岐义时使用
double 3 #=> 6

double double 3 #=> 12

def sum(x, y)
  x + y
end

# 方法的参数用逗号分隔
sum 3, 4 #=> 7

sum sum(3, 4), 5 #=> 12

# yield
# 所有方法都有一个隐含的，可选的块参数
# 可以通过 'yield' 关键字调用

def surround
  puts '{'
  yield
  puts '}'
end

surround { puts 'hello world' }

# {
# hello world
# }


# 可以向函数传递一个块
# "&" 标记传递的块是一个引用
def guests(&block)
  block.call 'some_argument'
end

# 可以传递多个参数，这些参数会组成一个数组：
def guests(*array)
  array.each { |guest| puts guest }
end

# 如果函数返回一个数组，在赋值时可以进行拆分：
def foods
    ['pancake', 'sandwich', 'quesadilla']
end
breakfast, lunch, dinner = foods
breakfast #=> 'pancake'
dinner #=> 'quesadilla'

# Ruby 的传统中，所有返回布尔值的方法都以 ? 结尾
5.even? # false
5.odd? # true

# 如果方法名末尾有 !，表示对调用者本身进行修改。
# 很多方法的 ! 版本会修改数据，非 ! 版本只是返回更新了的结果
company_name = "Dunder Mifflin"
company_name.upcase #=> "DUNDER MIFFLIN"
company_name #=> "Dunder Mifflin"
company_name.upcase! # we're mutating company_name this time!
company_name #=> "DUNDER MIFFLIN"


# 通过 class 进行类定义
class Human

  # 类变量。它能在该类的所有实例中共享。
  @@species = 'H. sapiens'

  # 基本的初始化器
  def initialize(name, age = 0)
    # 将 name 值赋给实例变量 @name
    @name = name
    # 如果没有指定 age 值，会使用参数列表中的默认值
    @age = age
  end

  # 基本的 setter 方法
  def name=(name)
    @name = name
  end

  # 基本的 getter 方法
  def name
    @name
  end

  # 以上的功能也可以用下面的 attr_accessor 来封装
  attr_accessor :name

  # Getter/setter 方法也可以像这样单独创建
  attr_reader :name
  attr_writer :name

  # 类方法通过使用 self 与实例方法区别开来。
  # 类方法只能通过类来调用，不能通过实例调用。
  def self.say(msg)
    puts msg
  end

  def species
    @@species
  end
end


# 初始化类
jim = Human.new('Jim Halpert')

dwight = Human.new('Dwight K. Schrute')

# 调用一些方法
jim.species #=> "H. sapiens"
jim.name #=> "Jim Halpert"
jim.name = "Jim Halpert II" #=> "Jim Halpert II"
jim.name #=> "Jim Halpert II"
dwight.species #=> "H. sapiens"
dwight.name #=> "Dwight K. Schrute"

# 调用类方法
Human.say('Hi') #=> "Hi"

# 变量的作用域由它们的名字格式定义
# 以 $ 开头的具有全局域
$var = "I'm a global var"
defined? $var #=> "global-variable"

# 以 @ 开头的具有实例作用域
@var = "I'm an instance var"
defined? @var #=> "instance-variable"

# 以 @@ 开头的具有类作用域
@@var = "I'm a class var"
defined? @@var #=> "class variable"

# 以大写字母开头的是常数
Var = "I'm a constant"
defined? Var #=> "constant"

# 类也是对象。因此类也有实例变量。
# 类变量在类与其继承者之间共享。

# 基类
class Human
  @@foo = 0

  def self.foo
    @@foo
  end

  def self.foo=(value)
    @@foo = value
  end
end

# 派生类
class Worker < Human
end

Human.foo # 0
Worker.foo # 0

Human.foo = 2 # 2
Worker.foo # 2

# 类实例变量不能在继承类间共享。

class Human
  @bar = 0

  def self.bar
    @bar
  end

  def self.bar=(value)
    @bar = value
  end
end

class Doctor < Human
end

Human.bar # 0
Doctor.bar # nil

module ModuleExample
  def foo
    'foo'
  end
end

# include 模块后，模块的方法会绑定为类的实例方法
# extend 模块后，模块的方法会绑定为类方法

class Person
  include ModuleExample
end

class Book
  extend ModuleExample
end

Person.foo     # => NoMethodError: undefined method `foo' for Person:Class
Person.new.foo # => 'foo'
Book.foo       # => 'foo'
Book.new.foo   # => NoMethodError: undefined method `foo'

# 当对模块进行 include 或 extend 时，相应的回调代码会被执行。

module ConcernExample
  def self.included(base)
    base.extend(ClassMethods)
    base.send(:include, InstanceMethods)
  end

  module ClassMethods
    def bar
      'bar'
    end
  end

  module InstanceMethods
    def qux
      'qux'
    end
  end
end

class Something
  include ConcernExample
end

# 类 Something 包含了 ConcernExample, 因此 ConcernExample 模块
# 上的 included 回调代码会被执行。

Something.bar     # => 'bar'
Something.qux     # => NoMethodError: undefined method `qux'
Something.new.bar # => NoMethodError: undefined method `bar'
Something.new.qux # => 'qux'
```


> 参考文献： 
> [Learn X in Y minutes](https://learnxinyminutes.com/docs/ruby/)
