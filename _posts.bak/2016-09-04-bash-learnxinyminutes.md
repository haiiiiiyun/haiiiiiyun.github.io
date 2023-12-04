---
title: Bash 基础知识
date: 2016-09-04
writing-time: 2016-09-04 08:44--12:45
categories: programming
tags: Utility LearnXinYminutes
---

Bash 是一个 unix shell 的名字，它即是 GNU 操作系统的御用 shell，也是 Linux 和 Mac OS X 上的默认 shell。

[更多请看这里。](http://www.gnu.org/software/bash/manual/bashref.html)

还有一个推荐链接: [The Command Line Crash Course](http://cli.learncodethehardway.org/book/)

```bash
#!/bin/bash
# 脚本的首行是 shebang，
# 用于告诉系统如何执行该脚本： http://en.wikipedia.org/wiki/Shebang_(Unix)
# 同时你也看到了，注释以 # 开头。Shebang 也是一条注释。

# 一个简单的 hello world 例子：
echo Hello world!

# 每个命令始于一个新行，或者始于分号之后：
echo 'This is the first line'; echo 'This is the second line'

# 定义一个变量像这样：
Variable="Some string"

# 但不能这样：
Variable = "Some string"
# Bash 会认为 Variable 是一个需要执行的命令，但因无法找到
# 会提示错误。

# 或者也可以这样：
Variable= 'Some string'
# Bash 会认为 'Some string' 是一个需要执行的命令，但因无法找到
# 会提示错误。（这种情况下只有当 'Some string' 是一个命令时
# 'Variable=' 部分才会被看做为一个有效的变量赋值项。)

# 使用变量：
echo $Variable #=> Some string
echo "$Variable" #=> Some string
echo '$Variable' #=> $Variable
# 当你使用变量自身时 — 赋值，导出等时 — 你只需写出
# 它的名字，无需带 $。如果要使用变量的值时，应该要使用 $。
# 注意 ' (单引号) 中不会解析变量！

# 参数扩展 Parameter Expansion ${ }:
echo ${Variable} #=> Some string
# 这是参数扩展的一种简单使用方式
# 参数扩展 Parameter Expansion 从一个变量中获取值。它能 “展开” 或打印输出该值。
# 在展开时，该值或参数可以被修改。
# 下面是一些进行修改的扩展示例。

# 变量中的字符串替换
echo ${Variable/Some/A} #=> A sring
# 这里的第一个 "Some" 将被替换成 "A"

# 变量的子字符串
Length=7
echo ${Variable:0:Length} #=> Some st
# 这里将只返回变量值中的最先 7 个字符

# 变量的默认值
echo ${Foo:-"DefaultValueIfFooIsMissingOrEmpty"}
# 只有当 Foo 值为 null (Foo=)，空字符串 (Foo=""); 零 (Foo=0) 等返回为 0 时有效果。
# 注意它只是返回该默认值，并不会修改变量的值。

# 括号展开 Brace Expansion { }
# 用于生产区间
echo {1..10} #=> 0 1 2 3 4 5 6 7 8 9 10
echo {a..z} #=> a b c d e f g h i j k l m n o p q r s t u v w x y z
echo {z..a} #=> z y x w v u t s r q p o n m l k j i h g f e d c b a
# 输出从开始值到结束值的一个范围区间

# 内置变量：
# 有一些很有用的内置变量，像
echo "Last program's return value: $?"
echo "Script's PID: $$"
echo "Number of arguments passed to script: $#"
echo "All arguments passed to script: $@"
echo "Script's arguments separated into different variables: $1 $2..."

# 现在既然了解了如何 echo 和使用变量，
# 让我们学习 bash 的其它基础知识吧！

# 通过 `pwd` 命令可以获取我们的当前目录。
# `pwd` 代表 "print working directory"。
# 我们也可以使用内置变量 `$PWD`。
# 注意下面的都是等价的：
echo "I'm in $(pwd)" # 先执行 `pwd` 然后再修改输出
echo "I'm in $PWD" # 修改变量

# 如果你的终端中输出内容过多，
# `clear` 命令可以用来清屏
clear

# 读取一个输入值：
echo "What's your name?"
read Name # 注意我们无需先对变量进行声明
echo Hello, $Name!

# 我们有常见的 if 结构：
# 执行 'man test' 可以了解条件判断的更多信息
if [ $Name != $USER ]
then
    echo "Your name isn't your username"
else
    echo "Your name is your username"
fi

# 注意：如果 $Name 为空，bash 会将上面的条件视为：
if [ != $USER ]
# 这是一条无效语法
# 因此在 bash 中使用有可能为空值的变量的 “安全” 方式为：
if [ "$Name" != $USER ] ...
# 此时，当 $Name 为空时，bash 视其为：
if [ "" != $USER ] ...
# 它能预期工作

# 还有条件执行
echo "Always executed" || echo "Only executed if first command fails"
echo "Always executed" && echo "Only executed if first command does NOT fail"

# 要想在 if 语句中使用 && 和 ||, 你需要多对方括号：
if [ "$Name" == "Steve" ] && [ "$Age" -eq 15 ]
then
    echo "This will run if $Name is Steve AND $Age is 15."
fi

if [ "$Name" == "Daniya" ] || [ "$Name" == "Zach" ]
then
    echo "This will run if $Name is Daniya OR Zach."
fi

# 表达式用下面的格式表示：
echo $(( 10 + 5 ))

# 不像其它编程语言，bash 是一个 shell，因此它在当前目录上下文中运行。
# 你可以使用 `ls` 命令来列出当前目录下的文件和目录：
ls

# 下列命令选项可以控制它们的执行：
ls -l # 将每个文件和目录都单列在一行上
ls -t # 根据最后修改日期（降序）排序目录内容
ls -R # 对该目录及其所有子目标进行递归 `ls`

# 以上命令的结果可以传给下个命令作为输入。
# grep 命令根据提供的模式对输入进行过滤。因此我们可以这样列出
# 当前目录下的 .txt 文件：
ls -l | grep "\.txt"

# 使用 `cat` 将文件打印到标准输出：
cat file.txt

# 我们也可以使用 `cat` 来读取文件：
Contents=$(cat file.txt)
echo "START OF FILE\n$Contents\nEND OF FILE"

# 使用 `cp` 将文件或目录从一个地方复制到另一个地方。
# `cp` 创建源内容的一个新版本。
# 因此编辑复制版本不会影响原来的版本（相反也一样）。
# 注意如果目标已经存在了的话会被覆盖。
cp srcFile.txt clone.txt
cp -r srcDirectory/ dst/ # 递归复制

# 如果打算在计算机间交换文件，查看 `scp` 或 `sftp`。
# `scp` 和 `cp` 非常相似。
# `sftp` 更具交互性。

# 使用 `mv` 将文件或目录从一个地方移到另一个地方。
# `mv` 类似 `cp`, 但它会删除源内容。
# `mv` 对于重命名文件也很有用！
mv s0urc3.txt dst.txt # sorry, l33t hackers...

# 因 bash 在当前目录上下文中运行，而你可能需要
# 在其它目录下运行你的命令。我们的 cd 命令可以修改位置：
cd ~    # 修改成 HOME 目录
cd ..   # 到上一级目录
        # (^^例如, 从 /home/username/Downloads 转到 /home/username)
cd /home/username/Documents   # 修改到一个特定目录
cd ~/Documents/..    # 还在 HOME 目录，不是吧？？

# 使用子 shell 进行跨目录操作
(echo "First, I'm here: $PWD") && (cd someDir; echo "Then, I'm here: $PWD")
pwd # 仍然在先前的目录中

# 使用 `mkdir` 创建新目录。
mkdir myNewDir
# `-p` 选项使得中间目录在必要时会被新建。
mkdir -p myNewDir/with/intermediate/directories

# 你可以重定向命令的输入和输出 (stdin, stdout, 和 stderr)。
# 从标准输入 stdin 中读取内容直到 ^EOF$，然后使用 "EOF" 之间的行对 hello.py 
# 进行覆盖：
cat > hello.py << EOF
#!/usr/bin/env python
from __future__ import print_function
import sys
print("#stdout", file=sys.stdout)
print("#stderr", file=sys.stderr)
for line in sys.stdin:
    print(line, file=sys.stdout)
EOF
# 这里 << EOF 表示 EOF 是输入的结尾符
# 而如果用 < EOF 则表示从文件 EOF 中读入内容

# 使用不同的 stdin, stdout, 和 stderr 重定向运行 hello.py：
python hello.py < "input.in"
python hello.py > "output.out"
python hello.py 2> "error.err"
python hello.py > "output-and-error.log" 2>&1
python hello.py > /dev/null 2>&1
# 错误输出内容会覆盖已存在的文件。
# 如果你是想进行追加，使用 ">>"：
python hello.py >> "output.out" 2>> "error.err"

# 覆盖 output.out, 追加到 error.err, 再统计行数：
info bash 'Basic Shell Features' 'Redirections' > output.out 2>> error.err
wc -l output.out error.err

# 运行一个命令并打印输出其文件描述符 (例如 /dev/fd/123)
# 参阅: man fd
echo <(echo "#helloworld")

# 将 output.out 内容覆盖为 "#helloworld"：
cat > output.out <(echo "#helloworld")
echo "#helloworld" > output.out
echo "#helloworld" | cat > output.out
echo "#helloworld" | tee output.out >/dev/null
# 这里的 tee 命令从标准输入读取数据，然后输出到标准输出及文件上。

# 显式地清理临时文件 (要交互添加 '-i')
# 警告：`rm` 命令无法撤销
rm -v output.out error.err output-and-error.log
rm -r tempDir/ # 递归删除

# 命令可以通过 $( ) 嵌套在其它命令中：
# 下面的的命令会显示当前目录下的文件和目录数。
echo "There are $(ls | wc -l) items here."

# 以上的也可以使用撇号 `` 完成，但它们无法嵌套 - 因此
# 优先使用 $( )。
echo "There are `ls | wc -l` items here."

# Bash 使用的 case 语句和 Java 和 C++ 中的 switch 语句类似：
case "$Variable" in
    #列出你会碰到的条件模式
    0) echo "There is a zero.";;
    1) echo "There is a one.";;
    *) echo "It is not null.";;
esac

# for 循环将遍历给定的许多参数：
# 下面将打印输出区间的内容。
for Variable in {1..3}
do
    echo "$Variable"
done

# 或者也可以按 “传统的 for 循环” 方式进行编写：
for ((a=1; a <= 3; a++))
do
    echo $a
done

# 它们也可作用于文件上..
# 这里将在文件 file1 和 file2 上运行 'cat'
for Variable in file1 file2
do
    cat "$Variable"
done

# ..也可以作用于一个命令的输出上
# 这里将在 ls 的每行输出内容上运行 cat
for Output in $(ls)
do
    cat "$Output"
done

# while 循环：
while [ true ]
do
    echo "loop body here..."
    break
done

# 你也可以定义函数
# 定义:
function foo ()
{
    echo "Arguments work just like script arguments: $@"
    echo "And: $1 $2..."
    echo "This is a function"
    return 0
}

# 或者简单地
bar ()
{
    echo "Another way to declare functions!"
    return 0
}

# 调用你的 foo 函数
foo "My name is" $Name

# 有许多很有用的命令你应该学习下：
# 打印 file.txt 的最后 10 行
tail -n 10 file.txt

# 打印 file.txt 的最先 10 行
head -n 10 file.txt

# 排序 file.txt 中的行
sort file.txt

# 报告或忽略临近的重复行，使用 -d 将只输出有重复的行
uniq -d file.txt

# 只输出位于 ',' 之前的首列
# cut 命令将文件的每行按 delimiter 分割，再选择特定区域输出
# -d 指定 delimiter, -f 指定 fields list
cut -d ',' -f 1 file.txt

# 将文件中的所有 'okay' 替换为 'great' (兼容 regex)
sed -i 's/okay/great/g' file.txt

# 将文件中匹配正则表达式的所有行打印输出
# 本例中将以 "foo" 开头并以 "bar" 结尾的行打印输出
grep "^foo.*bar$" file.txt
# 传入选项 "-c"，输出将是匹配的行数
grep -c "^foo.*bar$" file.txt
# 其它有用的选项：
grep -r "^foo.*bar$" someDir/ # 递归 `grep`
grep -n "^foo.*bar$" file.txt # 给出行号
grep -rI "^foo.*bar$" someDir/ # 递归 `grep`，但是忽略二进制文件
# 先执行之前的搜索，但是过滤掉含有 "baz" 的行
grep "^foo.*bar$" file.txt | grep -v "baz"

# 如果你只是想对该字符串进行搜索，
# 不想匹配正则表达式，使用 fgrep (或 grep -F)
fgrep "foobar" file.txt

# trap 命令允许当你的脚本接收到某个信号时才执行命令。
# 这里 trap 命令只当在接收到列表中的任何一个信号时将执行 rm。
trap "rm $TEMP_FILE; exit" SIGHUP SIGINT SIGTERM

# `sudo` 用来以 superuser 身份执行命令
$NAME1=$(whoami)
$NAME2=$(sudo whoami)
echo "Was $NAME1, then became more powerful $NAME2"

# 使用 bash 的 'help' 内置命令查阅 Bash shell 内置命令文档：
help
help help
help for
help return
help source
help .

# 使用 man 来查阅 Bash manpage 文档：
apropos bash
man 1 bash
man bash

# 使用 info (? 表示 help) 来查阅 info 文档 ：
apropos info | grep '^info.*('
man info
info info
info 5 info

# 查阅 bash info 文档：
info bash
info bash 'Bash Features'
info bash 6
info --apropos bash

```

> 参考文献： [Learn Bash in Y minutes](https://learnxinyminutes.com/docs/bash/)
