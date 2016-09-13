---
title: Per5 基础知识
date: 2016-09-13
writing-time: 2016-09-13 09:39--14:20
categories: programming
tags: Perl5 Utility LearnXinYminutes
---

# 安装使用

Ubuntu 16.04 已经默认安装了 perl5：

```bash
$ perl -v

This is perl 5, version 22, subversion 1 (v5.22.1) built for i686-linux-gnu-thread-multi-64int
(with 58 registered patches, see perl -V for more detail)

Copyright 1987-2015, Larry Wall
```

perl5 的脚本后缀为 `.pl`，并通过 perl 执行：


```bash
$ perl myscript.pl
```


Perl 5 是一门功能强大、特性丰富的编程功能，具有超过 25 年的发展历史。

Perl 5 可运行于超过 100 种平台上，从可移动设备到大型主机，它即适用于快速原型的开发，也适用于大型开发项目。

```perl
# 单行注释开始于一个井号。

#### Strict 和 warnings

use strict;
use warnings;

# 所有的 perl 脚本和模块都应该包含这两行。Strict 使得
# 在拼错变量名等情况下编译会出错，而
# warnings 会在联接一个未定义值等常见陷进时
# 输出警告信息。

#### Perl 变量类型

#  变量开始于一个标记，它是一个标识类型的符号。
#  一个有效的变量名以一个字母或下划线开始，
#  后根任意个字母，数字或下划线。

### Perl 主要有三种变量类型： $scalar, @array, 和 %hash。

## 标量
#  一个标量表示一个单值：
my $animal = "camel";
my $answer = 42;

# 变量名前的 my 用于变量范围声明，
# 类似的关键字还有 local, our。

# my 将变量声明为 “词法范围”，即该变量名及值只能在本层模块
# 或者函数中可以看到，高一层或者低一层的都不可看到。

# local 声明将变量的值局限于 “动态词法范围”，只有本层和
# 本层内的函数可以看到，上层不能看到。

## our 相当于全局声明。

# 标量值可以是字符串，整数或浮点数，
# Perl 会在需要时进行自动转换。

## 数组
#  一个数组表示一组值：
my @animals = ("camel", "llama", "owl");
my @numbers = (23, 42, 69);
my @mixed   = ("camel", 42, 1.23);

# 数组元素通过方括号访问，并使用 $
# 来表示只会返回一个单值。
# 索引从 0 开始计数。
my $second = $animals[1];

## Hashes
#  哈希表示一组 键/值 对：

my %fruit_color = ("apple", "red", "banana", "yellow");

#  你也可以用空格和 "=>" 操作符将它排列地更好看：

my %fruit_color = (
  apple  => "red",
  banana => "yellow",
);

# 哈希元素通过花括号访问，并再次使用了 $。
my $color = $fruit_color{apple};

# 标量，数组和哈希的更多文档见 perldata (perldoc perldata)。

#### 引用，类似于 C 中的指针

# 更加复杂的数据类型可以通过引用来构建，
# 它使你能在数组和哈希中构建数组和哈希。

my $array_ref = \@array;
my $hash_ref = \%hash;
my @array_of_arrays = (\@array1, \@array2, \@array3);

# 你也可以创建匿名的数组或哈希，并返回它的引用：

my $fruits = ["apple", "banana"];
my $colors = {apple => "red", banana => "yellow"};

# 引用值通过加上适合的前缀符可以解引用 (dereference)。

my @fruits_array = @$fruits;
my %colors_hash = %$colors;

# 作为一种简写法，箭头操作符可以用来解引用并存取一个单值。

my $first = $array_ref->[0];
my $value = $hash_ref->{banana};

# 要获取关于引用的更加深入的文档，请查阅 perlreftut 和 perlref。

#### 条件和循环结构

# Perl 中有大部分常用的条件和循环结构。

if ($var) {
  ...
} elsif ($var eq 'bar') {
  ...
} else {
  ...
}

unless (condition) {
  ...
}
# 提供的这个是 "if (!condition)" 的更加易读的版本

# Perl 风格的倒装
print "Yow!" if $zippy;
print "We have no bananas" unless $bananas;

#  while
while (condition) {
  ...
}


# for 循环和遍历
for (my $i = 0; $i < $max; $i++) {
  print "index is $i";
}

for (my $i = 0; $i < @elements; $i++) {
  print "Current element is " . $elements[$i];
}

for my $element (@elements) {
  print $element;
}

# 隐含

for (@elements) {
  print;
}

# 再次 Perl 风格的倒装
print for @elements;

# 遍历一个哈希引用中的键和值，$_ 指默认参数值
print $hash_ref->{$_} for keys %$hash_ref;

#### 正则表达式

# Perl 对正则表达式支持即广又深，
# 这是一个在 perlrequick, perlretut 及其它地方
# 都有冗长文档的主题。但是，简而言之：

# 简单匹配
if (/foo/)       { ... }  # true 如果 $_ 包含 "foo"
if ($x =~ /foo/) { ... }  # true 如果 $x 包含 "foo"

# 简单替换

$x =~ s/foo/bar/;         # 将 $x 中的 foo 替换成 bar
$x =~ s/foo/bar/g;        # 将 $x 中的全部 foo 都 替换成 bar

# 这里的 =~ 指执行正则表达式操作


#### 文件和 I/O

# 通过 "open()" 函数你可以打开一个文件用于输入和输出。
# $! 是根据上下文内容返回的错误号或错误描述

open(my $in,  "<",  "input.txt")  or die "Can't open input.txt: $!";
open(my $out, ">",  "output.txt") or die "Can't open output.txt: $!";
open(my $log, ">>", "my.log")     or die "Can't open my.log: $!";

# 通过 "<>" 操作符，你可以从一个已打开的文件句柄中读取数据。
# 在标量上下文中读取单行，而在
# 列表上下文中读取所有行，并将每行依次赋给列表中的一个元素。

my $line  = <$in>;
my @lines = <$in>;

#### 编写子过程

# 编写子过程很容易：

sub logger {
  my $logmessage = shift;

  open my $logfile, ">>", "my.log" or die "Could not open my.log: $!";

  print $logfile $logmessage;
}

# 这里的 shift 用来获取子过程参数列表中的首个参数值

# 现在我们就能像使用任何其它内置函数一样使用子过程了：

logger("We have a logger subroutine!");

#### 模块

# 一个模块就是一组 Perl 代码，通常是子过程，
# 它们可以用于其它 Perl 代码中。模块通常保存在
# 后缀为 .pm 的文件中，从而便于 Perl 查找。

package MyModule;
use strict;
use warnings;

sub trim {
  my $string = shift;
  $string =~ s/^\s+//;
  $string =~ s/\s+$//;
  return $string;
}

1;

# 最后的 1; 表示该模块返回为 1，这是一种标准写法。

# 在其它地方：

use MyModule;
MyModule::trim($string);

# Exporter 模块能使子过程更加易于导出，从而
# 它们可以这样使用：

use MyModule 'trim';
trim($string);

# 许多 Perl 模块可以从 CPAN (http://www.cpan.org/) 下载，
# 它们提供了大量的功能特性来帮助你避免重造轮子。
# 像 Exporter 等很多流行的模块都已经包含在了 Perl 自己的发布包内了。
# 更多关于模块的信息可查看 perlmod。

#### 对象

# Perl 中的对象仅仅是知道它们自身属于哪个类（包）的引用。
# 从而当通过对象调用方法（子过程）时，可以在类（包）上找到。
# bless 函数用于构造器（通常是 new）中进行设置。
# 但是，当你使用了 Moose 或 Moo（见下面）等模块时，你无需自己
# 调用 bless。

package MyCounter;
use strict;
use warnings;

sub new {
  my $class = shift;
  my $self = {count => 0};
  return bless $self, $class;
}

sub count {
  my $self = shift;
  return $self->{count};
}

sub increment {
  my $self = shift;
  $self->{count}++;
}

1;

# bless 函数设置了该对象属于哪个类。

# 使用箭头操作符可以在类或对象实例上调用方法。

use MyCounter;
my $counter = MyCounter->new;
print $counter->count, "\n"; # 0
$counter->increment;
print $counter->count, "\n"; # 1

# 来自 CPAN 的 Moose 和 Moo 模块可以帮你设置好你的对象所属类。
# 它们提供了一个构造器和声明属性的简便语法。
# 本类与上面定义的那个等价。

package MyCounter;
use Moo; # imports strict and warnings

has 'count' => (is => 'rwp', default => 0, init_arg => undef);

sub increment {
  my $self = shift;
  $self->_set_count($self->count + 1);
}

1;

# 面向对象编程在 perlootut 中有更多讲述，
# 而关于它的低层实现在 perlobj 中有描述。
```

#### FAQ

perlfaq 包含了关于许多常见任务的问答，并经常提供关于如何使用优秀 CPAN 模块的建议。

#### 更多内容

 - [perl-tutorial](http://perl-tutorial.org/)
 - [Learn at www.perl.com](http://www.perl.org/learn.html)
 - [perldoc](http://perldoc.perl.org/)
 - 及 perl 内置 : `perldoc perlintro`

> 参考文献： [Learn Perl in Y minutes](https://learnxinyminutes.com/docs/perl/)
