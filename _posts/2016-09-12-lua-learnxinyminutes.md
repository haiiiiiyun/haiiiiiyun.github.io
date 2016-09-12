---
title: Lua 基础知识
date: 2016-09-12
writing-time: 2016-09-12 15:24--18:48
categories: programming
tags: Lua Utility LearnXinYminutes
---

# 在 Ubuntu 中安装使用

当前版本是 Lua5.3：

```bash
$ sudo apt-get install lua5.3
```

开启 Lua REPL：

```bash
$ lua5.3
Lua 5.3.1  Copyright (C) 1994-2015 Lua.org, PUC-Rio
>
```

```lua
-- 两个破折号开始一个单行注释。

--[[
     添加两个 [ 和 ] 
     成为一个多行注释。
--]]
--------------------------------------------------------------------------------
-- 1. 变量和流控制。
--------------------------------------------------------------------------------

num = 42  -- 所有数字都是 double 型。
-- 不要担心，64 位的 double 有 52 位用于保存整数值;
-- 对于需要 < 52 位表示的整数，机器精度都不是问题。

s = 'walternate'  -- 不可变字符串与 Python 的类似。
t = "double-quotes are also fine"
u = [[ Double brackets
       start and end
       multi-line strings.]]
t = nil  -- 未定义 t; Lua 有垃圾回收机制。

-- 块用 do/end 等关键字表示：
while num < 50 do
  num = num + 1  -- 不能用 ++ 或 += 形式的操作符。
end

-- If 语句：
if num > 40 then
  print('over 40')
elseif s ~= 'walternate' then  -- ~= 指不相等。
  -- 相等判断和 Python 类似用 ==; 这也适用于字符串。
  io.write('not over 40\n')  -- 默认输出到 stdout。
else
  -- 变量默认都是全局域的。
  thisIsGlobal = 5  -- 变量名一般用骆驼写法。

  -- 如何定义一个局部变量：
  local line = io.read()  -- 从 stdin 上读取下一行内容。

  -- 字符串连接使用 .. 操作符：
  print('Winter is coming, ' .. line)
end

-- 未定义变量返回 nil。
-- 这里不会出错：
foo = anUnknownVariable  -- 现在 foo = nil。

aBoolValue = false

-- 只有 nil 和 false 会解释成假值; 0 和 '' 都是真值！
if not aBoolValue then print('was false') end

-- 'or' 和 'and' 都使用短路机制。这和 C/js 中的 a?b:c 操作符类似：
ans = aBoolValue and 'yes' or 'no'  --> 'no'

karlSum = 0
for i = 1, 100 do  -- 这个区间包含了两端点。
  karlSum = karlSum + i
end

-- 使用 "100, 1, -1" 创建一个降序区间：
fredSum = 0
for j = 100, 1, -1 do fredSum = fredSum + j end

-- 通常，区间表述为 begin, end[, step]。

-- 另一种循环结构：
repeat
  print('the way of the future')
  num = num - 1
until num == 0

--------------------------------------------------------------------------------
-- 2. 函数。
--------------------------------------------------------------------------------

function fib(n)
  if n < 2 then return n end
  return fib(n - 2) + fib(n - 1)
end

-- 也支持封闭和匿名函数：
function adder(x)
  -- 当 adder 调用时会创建返回的函数，并且该函数
  -- 会保存 x 的值：
  return function (y) return x + y end
end
a1 = adder(9)
a2 = adder(36)
print(a1(16))  --> 25
print(a2(64))  --> 100

-- 返回值，函数调用，和赋值都可以用列表，并且列表长度允许不匹配。
-- 未匹配的接收方将设为 nil; 未匹配的发送方会被丢弃。

x, y, z = 1, 2, 3, 4
-- 现在 x = 1, y = 2, z = 3, 并且 4 被丢弃。

function bar(a, b, c)
  print(a, b, c)
  return 4, 8, 15, 16, 23, 42
end

x, y = bar('zaphod')  --> 输出 "zaphod  nil nil"
-- 现在 x = 4, y = 8, 15..42 的值被丢弃。

-- 函数是一级概念，可以是局部/全局的。以下的定义是等同的：
function f(x) return x * x end
f = function (x) return x * x end

-- 下面的也是等同的：
local function g(x) return math.sin(x) end
local g = function(x) return math.sin(x) end
-- 等同于 local function g(x)..., 除了不能在函数体中引用 g
local g; g  = function (x) return math.sin(x) end
-- 'local g' 声明使得 g 可以被引用

-- 只有一个字符串参数的调用无需括号：
print 'hello'  -- 正常运行。

-- 只有一个表 table 参数的调用也不需要括号（下面有更多关于表的信息）：
print {} -- 也能运行。

--------------------------------------------------------------------------------
-- 3. 表 Table。
--------------------------------------------------------------------------------

-- 表 = Lua 中唯一的复合数据结构：它们是关联数组。
-- 类似于 php 中的数组或 js 的对象，它们都是哈希查询的字典，
-- 并且可以作为列表使用。

-- 将表作为字典 / 映射：

-- 字典默认使用字符串键：
t = {key1 = 'value1', key2 = false}

-- 字符串键可以使用类似 js 中的点表示法：
print(t.key1)  -- 输出 'value1'。
t.newKey = {}  -- 增加一个新的 键/值对。
t.key2 = nil   -- 将 key2 从表中删除。

-- 任意 （非 nil）值作为键的文本表示法：
u = {['@!#'] = 'qbert', [{}] = 1729, [6.28] = 'tau'}
print(u[6.28])  -- 输出 "tau"

-- 键的匹配对于数字和字符串基本上是根据值进行，但对于表是根据其 ID 进行。
a = u['@!#']  -- 现在 a = 'qbert'。
b = u[{}]     -- 我们可能预想是 1729, 但它的值却是 nil：
-- 因查询失败故 b = nil。查询失败是因为我们使用的键和用于存储原来值的键不是同一个对象。
-- 因此字符串 & 数字是更具移植性的键。

-- 只有一个表参数的函数调用无需括号：
function h(x) print(x.key1) end
h {key1 = 'Sonmi~451'}  -- 输出 'Sonmi~451'。

for key, val in pairs(u) do  -- 表的遍历。
  print(key, val)
end

-- _G 是用于保存所有全局变量的一个特殊表。
print(_G['_G'] == _G)  -- 输出 'true'。

-- 表用作 列表 / 数组：

-- 列表文本表示隐含使用整数键：
v = {'value1', 'value2', 1.21, 'gigawatts'}
for i = 1, #v do  -- #v 是列表 v 的长度。
  print(v[i])  -- 索引尽然从 1 开始！疯了！
end
-- 'list' 不是一个真实的类型。v 只是一个具有连续整数键的表，
-- 它被用作一个列表。

--------------------------------------------------------------------------------
-- 3.1 Metatables 和 metamethods。
--------------------------------------------------------------------------------

-- 表可以通过 metatable 实现表的操作符重载。
-- 稍后我们将看到 metatables 如何实现 js-prototype 行为。

f1 = {a = 1, b = 2}  -- 表示分数 a/b。
f2 = {a = 2, b = 3}

-- 这会出错：
-- s = f1 + f2

metafraction = {}
function metafraction.__add(f1, f2)
  local sum = {}
  sum.b = f1.b * f2.b
  sum.a = f1.a * f2.b + f2.a * f1.b
  return sum
end

setmetatable(f1, metafraction)
setmetatable(f2, metafraction)

s = f1 + f2  -- 调用 f1 的 metatalbe 上 的 __add(f1, f2)

-- f1, f2 中没有与其 metatable 相关的键，这和 js 中的 prototype 不同，因此你必需
-- 通过 gemetatable(f1) 获取。metatable 是一个具有特殊键的普通表，
-- 它的键如 __add 等可以被 Lua 理解。

-- 但是下行会失败，这是因为 s 没有 metatable：
-- t = s + s
-- 下面给出的类似 Class 的模式可以修复这个问题：

-- metatable 上的__index 重载点查询操作：
defaultFavs = {animal = 'gru', food = 'donuts'}
myFavs = {food = 'pizza'}
setmetatable(myFavs, {__index = defaultFavs})
eatenBy = myFavs.animal  -- 正常！多亏了 metatable

--------------------------------------------------------------------------------
-- 直接表查询一旦失败后将使用 metatable 中的 __index 值进行重试。

-- __index 值针对更多个性化的查询，也可以是一个 function(tbl, key)

-- __index, __add 等的值, .. 称作 metamethods。
-- 完整列表。这是一份关于 metamethod 的列表。

-- __add(a, b)                     for a + b
-- __sub(a, b)                     for a - b
-- __mul(a, b)                     for a * b
-- __div(a, b)                     for a / b
-- __mod(a, b)                     for a % b
-- __pow(a, b)                     for a ^ b
-- __unm(a)                        for -a
-- __concat(a, b)                  for a .. b
-- __len(a)                        for #a
-- __eq(a, b)                      for a == b
-- __lt(a, b)                      for a < b
-- __le(a, b)                      for a <= b
-- __index(a, b)  <函数或一个表>  for a.b
-- __newindex(a, b, c)             for a.b = c
-- __call(a, ...)                  for a(...)

--------------------------------------------------------------------------------
-- 3.2 Class 形式的表和继承。
--------------------------------------------------------------------------------

-- 类不是内置的;通过表和 metatable 可以用不同的方法实现类。

-- 对这个例子的讲解都在下面。

Dog = {}                                   -- 1.

function Dog:new()                         -- 2.
  local newObj = {sound = 'woof'}          -- 3.
  self.__index = self                      -- 4.
  return setmetatable(newObj, self)        -- 5.
end

function Dog:makeSound()                   -- 6.
  print('I say ' .. self.sound)
end

mrDog = Dog:new()                          -- 7.
mrDog:makeSound()  -- 'I say woof'         -- 8.

-- 1. Dog 像一个类：它实际是一个表。
-- 2. "function tablename:fn(...)" 等同于
--    "function tablename.fn(self, ...)", : 只是增加了一个叫 self 的首个参数。
--    阅读下面的第 7 & 8 条了解 self 如何获取值。
-- 3. newObj 将会是 Dog 类的一个实例。
-- 4. "self" 指正在初始化的类。通常 self = Dog, 但是继承后会有变动。
--    当我们将 newObj 的 metatable 和 self 的 __index 都设置为 self 后，
--    newObj 将取得 self 的函数。
-- 5. 记住：setmetatable 返回它的首个参数。
-- 6. : 和第 2 行中的一样，但是这次我们期望 self 是一个实例而不是一个类。
-- 7. 与 Dog.new(Dog) 等同，因此在 new() 中 self = Dog。
-- 8. 与 mrDog.makeSound(mrDog) 等同; self = mrDog。

--------------------------------------------------------------------------------

-- 继承的例子：

LoudDog = Dog:new()                           -- 1.

function LoudDog:makeSound()
  local s = self.sound .. ' '                 -- 2.
  print(s .. s .. s)
end

seymour = LoudDog:new()                       -- 3.
seymour:makeSound()  -- 'woof woof woof'      -- 4.

--------------------------------------------------------------------------------
-- 1. LoudDog 获取 Dog 的方法和变量。
-- 2. self 从 new() 中获取了 'sound' 键。
-- 3. 等同于 "LoudDog.new(LoudDog)", 并且因为 LougDog 没有 'new' 键，
--    会转换成 "Dog.new(LoudDog)"，但是在其 metatable 中又是 "__index = Dog"。
--    结果： seymour 的 metatable 是 LoudDog, 同时 "LoudDog.__index = Dog"。因此
--    seymour.key 将等同于 seymour.key, LoudDog.key, Dog.key, 无论哪个具有给定
--    键的首个表。
-- 4. 'makeSound' 键在 LoudDog 中找到; 它等同于
--    "LoudDog.makeSound(seymour)".

-- 如果需要，子类的 new() 可以与基类的类似：
function LoudDog:new()
  local newObj = {}
  -- 设置 newObj
  self.__index = self
  return setmetatable(newObj, self)
end

--------------------------------------------------------------------------------
-- 4. 模块。
--------------------------------------------------------------------------------


--[[ 我将本节注释掉了，因而本脚本的余下部分也是可运行的。
```

```lua
-- 假设 mod.lua 文件看起来像这样：
local M = {}

local function sayMyName()
  print('Hrunkner')
end

function M.sayHello()
  print('Why hello there')
  sayMyName()
end

return M

-- 另一个文件可以使用 mod.lua 中的功能：
local mod = require('mod')  -- 运行 mod.lua 文件。

-- require 是包含模块的标准方式。
-- require 的行为类似：     （如果没有缓存：见下面）
local mod = (function ()
  <contents of mod.lua>
end)()
-- mod.lua 就像是一个函数体，
-- 因此 mod.lua 内的局部变量在外部都是不可见的。

-- 下面可以运行，因为这里的 mod = mod.lua 中的 M：
mod.sayHello()  -- Says hello to Hrunkner.

-- 这个不行：sayMyName 只存在于 mod.lua 中：
mod.sayMyName()  -- 错误

-- require 的返回值会被缓存，因此一个文件即使 require 了多次，
-- 也最多只能被执行一次。

-- 假设 mod2.lua 中包含 "print('Hi!')"。
local a = require('mod2')  -- 输出 Hi!
local b = require('mod2')  -- 没有输出; a=b。

-- dofile 就像不进行缓存的 require：
dofile('mod2')  --> Hi!
dofile('mod2')  --> Hi! (再次运行，不像 require)

-- loadfile 加载一个 lua 文件但不运行。
f = loadfile('mod2')  -- 调用 f() 将运行 mod2.lua。

-- loadstring 是 loadfile 的字符串版本。
g = loadstring('print(343)')  -- 返回一个函数。
g()  -- 输出 343; 在这之前没有输出。

--]]

```
## 参考资料

+ <a href="http://love2d.org/">Love 2D game engine</a>。
+ <a href="http://nova-fusion.com/2012/08/27/lua-for-programmers-part-1/">BlackBulletIV's Lua for programmers</a>。
+ The official <a href="http://www.lua.org/pil/contents.html">Programming in Lua</a> book。
+ <a href="http://lua-users.org/files/wiki_insecure/users/thomasl/luarefv51.pdf">Lua short reference</a> on lua-users.org。


未覆盖的主要主题是标准库：
* <a href="http://lua-users.org/wiki/StringLibraryTutorial">string library</a>
* <a href="http://lua-users.org/wiki/TableLibraryTutorial">table library</a>
* <a href="http://lua-users.org/wiki/MathLibraryTutorial">math library</a>
* <a href="http://lua-users.org/wiki/IoLibraryTutorial">io library</a>
* <a href="http://lua-users.org/wiki/OsLibraryTutorial">os library</a>

> 参考文献： [Learn Lua in Y minutes](https://learnxinyminutes.com/docs/lua/)
