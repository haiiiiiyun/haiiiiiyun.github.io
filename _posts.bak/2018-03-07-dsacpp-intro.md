---
title: 数据结构 C++ 版本笔记--1.绪论
date: 2018-03-07
writing-time: 2018-03-07
categories: programming
tags: Programming data&nbsp;structure algorithm
---

# 一、绪论

## 算法要素：

+ 输入与输出
+ 基本操作、确定性与可行性、有穷性
+ 有穷性 finiteness， 正确性 correctness
+ 退化（degeneracy, 即极端情况）与鲁棒性（robustness)
+ 重用性

证明算法有穷性和正确性的技巧：从适当的角度审视整个计算过程，并找出其所具有的某种不变性和单调性。单调性指算法会推进问题规模递减，不变性则不仅在算法初始状态下自然满足，而且应与最终的正确性相对应，当问题规模减小时，不变性应随即等价于正确性。


## 有穷性

Hailstone(n) 序列：

$$
Hailstone(n) = \begin{cases}
  \{1\}  & n \le 1 \\
  \{n\} \cup Hailstone(n/2) & n为偶 \\
  \{n\} \cup Hailstone(3n+1) & n为奇
\end{cases}
$$

例子：

Hailstone(42) = {42, 21, 64, 32, ..., 1}
Hailstone(7) = {7, 22, 11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, ..., 1}
Hailstone(27) = {27, 82, 41, 124, 62, 31, 94, 47, 142, 71, 214, 107, ... } 

它会持续下降，但不会持续上升，其变化捉摸不定，与冰雹运动过程非常相似：有时上升，有时下降，当为 1 时表示落地。

序列长度与 n 不成正比。

Hailstone(n) 是否有穷，现在还没有定论。

## 时间复杂度

time complexity 是输入规模 n 的一个函数，在所有的 n! 种输入中，选择执行时间最长者记为 T(n)，作为算法的时间复杂度。

利用理想计算模型，如图灵机模型或 RAM 模型，将算法的运行时间计算转化成算法的基本操作次数的计算。

### 渐进复杂度 (主流长远）

即只关注算法在输入规模大时的复杂度，用大 O 记号(big-o notation) 来表示 T(n) 的渐进上界。

此时，若存在正常数 c 和函数 f(n)，使得对任何 n >> 2 都有 $T(n) \le c \bullet f(n)$，则可认为在 n 足够大后，f(n) 给出了 T(n) 增长速度的一个渐进上界，记为： T(n) = O(f(n))。

大 O 记号的性质：

+ 对于任一常数 c > 0, 有 $O(f(n)) = O(c \bullet f(n))$，即函数各项的正常系数可忽略并等同于 1
+ 对于任意常数 a > b > 0, 有 $O(n^a + n^b) = O(n^a)$，即多项式中的低次项可忽略。 

用 O 记号确定上界，大 $\Omega$ 记号确定下界，而 大 $\Theta$ 记号给出了一个确界，是一个准确估计：

![time_complexity.png](/assets/images/tsinghua_dsacpp/c1_intro/time_complexity.png)


## 复杂度分析

### 1. 常数时间复杂度算法 constant-time algorithm， O(1)

### 2. 对数复杂度 O(logn)

整数 n 二进制展开的位数为 $1+\lfloor log_2 n \rfloor$

由于当 c >0 时， $log_ab = log_cb / log_ca$, 因此对于任意 a, b > 0, $log_an = log_ab \bullet log_bn$，根据 O 记号定义，有 $log_r n$ 界定时，常底数 r 具体取值无所谓，故对数复杂度直接记为 O(logn)，为 logarithmic-time algorithm。

而对数多项式复杂度表示为 $T(n) = O(log^c n), c>0$，为对数多项式时间复杂度算法，polylogarithmic-time algorithm。其效率无限接近于常复杂度。

### 3. 线性 O(n)， linear-time algorithm

### 4. 多项式 O(polynomial(n)), polynomial-time algorithm

实际应用中，一般认为这种复杂度是可接受的，其问题是可有效求解或易解的 (tractable)。

对于任意 c>1，$n^c = O(2^n)$，即指数是多项式的上界，相应地，前者是后者的下界。


2-Subset 子集问题： 集合 S 中包含 n 个正整数，$\sum S = 2m$，则 S 是否有子集 T，满足 $\sum T = m$

实例：美国大选，51 个州共 538 票，各州票数不同，获得 270 票即当选，问是否会出现恰好各得 269 票？

直觉算法：逐一枚举每一子集统计，复杂度为 $2^n$

有 n 个项的集合，子集共有 $2^n$ 个（考虑每个项包含和不包含在子集中的情况），遍历 0 ~ $2^n$，每个值转成二进制，依次判断：

```cpp
// 习题 [1-16]
//2-Subset 子集问题
int subset(int A[], int n, int m) {
    int end = (1<<n)-1; //2^n - 1
    for (int mask=0; mask<=end; mask ++) {
        int sum = 0;
        for(int i=0; i<n; i++) {
            if (mask & (1<<i)) {
                sum += A[i];
            }
        }
        if (sum == m)
            return mask; //mask 中的各个位数 1 代表所含的项
    }
    return 0;
}


int main() {
    int A[6] = {1, 2, 3, 4, 2, 6}; //sum=18=2X9
    cout << "subset(A, 6, 9)=" << subset(A, 6, 9) << endl;  //14, 1110, 表示 {2, 3, 4} 子集符合
}  
```

定理： 2-Subset is NP-complete，目前没有多项式复杂度的算法。


### 5. 指数 $O(2^n)$  exponential-time algorithm

指数复杂度算法无法真正应用于实际中。

## 复杂度层次

![complexity_scale.png](/assets/images/tsinghua_dsacpp/c1_intro/complexity_scale.png)


## 复杂度分析的方法

+ 迭代： 级数求和
+ 递归： 递归跟踪 + 递推方程
+ 猜测 + 验证

## 级数

### 算数级数： 与末项平方同阶

$T(n) = 1+2+ \cdots +n = n(n+1)/2 = O(n^2)$

### 幂方级数，：比幂次高出一阶：

$T_2(n) = 1^2 + 2^2 + 3^2 + \cdots + n^2 = n(n+1)(2n+1)/6 = O(n^3)$

$T_3(n) = 1^3 + 2^3 + 3^3 + \cdots + n^3 = n^2(n+1)^2/4 = O(n^4)$

$T_4(n) = 1^4 + 2^4 + 3^4 + \cdots + n^4 = n(n+1)(2n+1)(3n^2+3n-1)/30 = O(n^5)$

### 几何级数（a>1)：与末项同阶

$T_a(n) = a^0 + a^1 + \cdots + a^n = (a^{n+1}-1)/(a-1) = O(a^n)$

$T_2(n) = 1 + 2 + 4 + \cdots + 2^n = (2^{n+1}-1) = O(2^{n+1}) = O(2^n)$

### 等差级数：之和与其中最大一项的平方同阶

$x + (x+d) + (x+2d) + \cdots + (x+(n-1)d) = (d/2)n^2 + (x-d/2)n = \Theta(n^2)$

### 等比级数之和与其中最大一项同阶

$x + xd + xd^2 + \cdots + xd^{n-1} = nx + x(d^n-1)/d-1 = \Theta(d^{n-1})$



### 收敛级数： O(1)

### 可能未必收敛，但长度有限：

调和级数： $h(n) = 1 + 1/2 + 1/3 + \cdots + 1/n = \Theta(logn)$

对数级数： $log1 + log2 + log3 + \cdots + logn = log(n!) = \Theta(nlogn)$

书： Concrete Mathematics


### 循环 vs. 级数

循环次数的统计转为级数的计算。


次数对应面积：

![intro_loop_counter_vs_area.png](/assets/images/tsinghua_dsacpp/c1_intro/intro_loop_counter_vs_area.png)


次数对应级数和，几何级数与末项同阶：

![intro_loop_counter2.png](/assets/images/tsinghua_dsacpp/c1_intro/intro_loop_counter2.png)

![intro_loop_counter3.png](/assets/images/tsinghua_dsacpp/c1_intro/intro_loop_counter3.png)


## 封底估算， Back-of-The-Envelope Calculation

即在信封或不用纸笔在脑中进行估算。

$1 天 = 24 hr X 60min X 60sec \approx 25 X 4000 = 10^5 sec$

$1 生 \approx 100 yr = 100 X 365 day = 3 X 10^4 day = 3 X 10^9 sec$ 

即 300 年为 $10^{10} sec$，三生三世为 $10^{10}sec$

宇宙大爆炸至今为 $10^{21} = 10 X (10^{10})^2 sec$

fib(n) = $O(\Phi ^ n)$, 其中 $\Phi$ 是黄金分割点的值 1.168...，

而 $\Phi ^ {36} = 2^{25}$， （36 为 6 的平方， 25 为 5 的平方)。

$\Phi ^ 5$ 约为 10

$\Phi ^ 3$ 约为 $2^2$




## 递归

### 线性递归

```cpp
// 数组求和算法，线性递归版
int sum_linear_recursion(int A[], int n) {
    if (n < 1) // 平凡情况，递归基
        return 0;
    else //一般情况
        return sum_linear_recursion(A, n-1) + A[n-1]; //递归：前 n-1 项之和，再累计第 n-1 项
} //O(1)*递归深度 = O(1)*(n+1) = O(n)
```

平凡情况称为 **递归基** base case of recursion，用于结束递归。

`sum_linear_recursion` 算法是线性递归：每一递归实例对自身的调用至多一次，每一层上最多一个实例，且它们构成一线性次序关系。

这种形式中，问题总可分解成两个独立子问题：其一对应于单独的某元素，如 A[n-1]，故可直接求解;另一个对应剩余部分，且其结构与原问题相同，如 A[0, n-1]，最后，子问题解经过简单合并，可得到原问题的解。

线性递归模式，往往对应于 **减而治之 (decrease-and-conquer)** 的算法策略：递归每深入一层，问题的规模都缩减一个常数，直到最终蜕化为平凡的小（简单）问题。

### 递归分析

#### 递归跟踪法（recursion trace)

1. 算法的每一递归实例都表示为一个方框，其中注明该实例调用的参数
2. 若实例 M 调用实例 N，则在 M 与 N 对应的方框之间添加一条有向联线

![recursion_trace.png](/assets/images/tsinghua_dsacpp/c1_intro/recursion_trace.png)

#### 递推方程法 (recurrence equation) 

通过对递归模式的数学归纳，导出复杂度定界函数的递推方程（组）及边界条件，从而将复杂度的分析，转化为递归方程（组）的求解。

而对递归基的分析通常可获得边界条件。

比如上面的数组求和算法，设长度为 n 时的时间成本为 T(n)，为解析 sum_linear_recursion(A, n)，需递归解决 sum_linear_recursion（A, n-1)，再加上 A[n-1]，则： $T(n) = T(n-1) + O(1) = T(n-1) + c_1$，$c_1$ 为常数

而抵达递归基时， sum_linear_recursion(A, 0) 只需常数时间，则 $T(0) = O(1) = c_2$，联立以上两个方程，得到：

$T(n) = c_1 n + c_2 = O(n)$


## 多向递归

$2^n$ 的求解。

一般的定义为:

$$
power2(n) = \begin{cases}
1, & \text{n=0} \\
2 \bullet power2(n-1)
\end{cases}
$$

这是一个线性递归，复杂度为 O(n)


若 n 的二进制展开式为 $b_1b_2b_3\cdots b_k$，则：

$2^n = (\cdots(((1\times2^{b_1})^2 \times 2^{b_2})^2 \times 2^{b_3})^2 \cdots \times 2^{b_k})$

则 $n_{k-1}$ 和 $n_k$ 的幂值关系有：

$2^{n_k} = (2^{n_{k-1}})^2 \times 2^{b_k}$， 由归纳得递推式：

$$
power2(n_k) = \begin{cases}
power2(n_{k-1})^2 \times 2, & 若 b_k = 1 \\
power2(n_{k-1})^2, & b_k=0
\end{cases}
$$

```cpp
typedef long long tint64;

inline tint64 square(tint64 a) { return a*a; }

tint64 power2(int n) { //幂函数 2^n算法，优化递归版本, n>=0
    if (0==n) return 1; //递归基
    return (n&1) ? square(power2(n >> 1)) << 1 : square(power2(n >> 1)); //视 n 的 奇偶分别递归
} // O(logn) = O(r), r 为输入指数 n 的比特位数
```

迭代版本为：

```cpp
typedef long long tint64;
//迭代版本
tint64 power2_loop(int n) {
    tint64 pow = 1; // 累积器初始化为 2^0
    tint64 p = 2; // 累乘项初始化为 2，对应最低位为 1 的情况
    while (n>0) { // 迭代 log(n) 轮
        if (n&1) // 根据当前比特位是否为 1, 决定
            pow *= p; // 将当前累乘项计入累积器
        n >>= 1; //指数减半
        p *= p; //累乘项自乘
    }
    return pow; 
} // O(logn) = O(r), r 为输入指数 n 的比特位数

//而一般性的 a^n 计算如下 
tint64 power_loop(tint64 a, int n) { // a^n 算法： n >= 0
    tint64 pow = 1; // 累积器初始化为 a^0
    tint64 p = a; // 累乘项初始化为 a，对应最低位为 1 的情况
    while (n>0) { // 迭代 log(n) 轮
        if (n&1) // 根据当前比特位是否为 1, 决定
            pow *= p; // 将当前累乘项计入累积器
        n >>= 1; //指数减半
        p *= p; //累乘项自乘
    }
    return pow; 
} // O(logn) = O(r), r 为输入指数 n 的比特位数
```

## 递归消除

### 尾递归及消除

递归调用为算法的最后一步操作（即递归的任一实例都终止于这一递归调用），为尾递归，它们可转换为等效的迭代版本。

但上面数组求和的线性递归版本中，最后的操作是加法运算，不是纯递归调用，因此不是尾递归，但是也可以转换成迭代版本。


```cpp
// 数组倒置，将尾递归优化为迭代版本
void reverse_loop_version(int* A, int lo, int hi){
    while (lo < hi) {
        //swap(A[lo++], A[hi--]); //交换 A[lo], A[hi], 收缩待倒置区间
        int tmp = A[lo];
        A[lo] = A[hi];
        A[hi] = tmp;
        lo++;
        hi--;
    }
} // O(hi-lo+1)

```


### 二分递归

使用 **分而治之 divide-and-conquer** 的策略，将问题持续分解成更小规模的子问题，至平凡情况。

和减而治之策略一样，也要对原问题重新表述，保证子问题与原问题在接口形式上一致。

每一递归实例都可能做多次递归，故称作 **多路递归 multi-way recursion**。通常是将原问题二分，故称 **二分递归 binary recursion**。

数组求和采用二分递归：

```cpp
// 数组求和算法，二分递归版本，入口为 sum_binary_recursion(A, 0, n-1)
int sum_binary_recursion(int A[], int lo, int hi) {
    if (lo == hi) //如遇递归基（区间长度已降至 1)，则
        return A[lo]; //直接返回该元素
    else { // 否则是一般情况 lo < hi, 则
        int mi = (lo+hi) >> 1; //以居中单元为界，将原区间一分为二
        return sum_binary_recursion(A, lo, mi) + sum_binary_recursion(A, mi+1, hi); //递归对各子数组求和，然后合计
    }
} //O(hi-lo+1)，线性正比于区间的长度
```

当 $n=2^m$ 的形式下的 n=8 时，递归跟踪分析为：

![sum_binary_recursion.png](/assets/images/tsinghua_dsacpp/c1_intro/sum_binary_recursion.png)

其递归调用关系构成一个层次结构（二叉树），每降一层，都分裂为一个更小规模的实例。经过 $m=log_2 n$ 将递归调用，数组区间长度从 n 首次缩减为 1, 并到达第一个递归基。

其递归调用深度不超 m+1，每个实例仅需常数空间，故空间复杂度是 O(m+1) = O(logn)，比线性递归版本的空间复杂度 O(n) 优。

递归调用次数是 2n-1，故时间复杂度也是 O(2n-1)=O(n)。

分治递归要有效率，要保证子问题之间相互独立，不做重复递归。


Fibonacci 数的二分递归：

$$
fib(n) = \begin{cases}
n, & n \le 1 \\
fib(n-1) + fib(n-2), & n \ge 2
\end{cases}
$$


```cpp
// 计算 Fibonacci 数列的第 n 项，二分递归版本，O(2^n)
tint64 fibonacci_binary_recursion(int n) {
    return (n<2) ? 
        (tint64) n // 若到达递归基，直接取值
        : fibonacci_binary_recursion(n-1) + fibonacci_binary_recursion(n-2);
}
```

fib(n) = $O(\Phi ^ n)$, 其中 $\Phi$ 是黄金分割点的值 1.168...，

而 $\Phi ^ {36} = 2^{25}$， （36 为 6 的平方， 25 为 5 的平方)。

其时间复杂度是 $2^n$，原因是计算中出现的递归实例的重复度极高。


#### 优化策略，消除递归算法中重复的递归实例

即：借助一定量的辅助空间，在各子问题求解后，及时记录下其对应的解。

1. 从原问题出发自顶向下，遇到子问题时，先查验是否计算过，避免重新计算，为制表(tabulation) 或记忆 (memoization) 策略。
2. 从递归基出发，自底而上递推地得出各子问题的解，直到最终原问题的解，即为动态规划(dynamic programming) 策略。

#### Fibonacci 数：线性递归

fib(n-1) 和 fib(n-2) 并非独立，将递归函数改为计算一对相邻的 Fib 数：

```cpp
// Fibonacci 线性递归版本，入口形式 fibonacci_linear_recursion(n, prev)
// 使用临时变量，避免重复递归计算
tint64 fibonacci_linear_recursion(int n, tint64& prev) {
    if (n == 0){ //若到达递归基，则
        prev = 1;
        return 0; // 直接取值： fib(-1) = 1, fib(0)=0
    } else {
        tint64 prevPrev; prev = fibonacci_linear_recursion(n-1, prevPrev); //递归计算前两项
        return prevPrev + prev; //其和即为正解
    }
} // 用辅助变量记录前一项，返回数列的当前项, O(n)
```
通过 prevPrev 调阅此前的记录，从而省略了 fib(n-2) 的递归计算，呈线性递归模式，递归深度线性正比于输入值 n，共出现 O(n) 的递归实例，时间和空间复杂度都为 O(n)。

#### Fibonacci 数：动态规划

```cpp
// Fibonacci 迭代版本： O(n)
// 采用动态规划策略，按规模自小而大求解各子问题
tint64 fibonacci_loop_version(int n) {
    tint64 f = 0, g = 1; // 初始化 fib(0)=0, fib(1)=1
    while (0 < n--) {
        g += f; f = g-f; //依原始定义，通过 n 次加法和减法计算 fib(n)
    }
    return f;
}
```

#### 最长公共子序列 LCS 问题：

![intro_LCS.png](/assets/images/tsinghua_dsacpp/c1_intro/intro_LCS.png)

递归版本 LCS(A[0,n], B[0,m]):

两个序列 A[0, n], B[0, m]

1. 若 n=-1 或 m=-1，则返回空串，这是一个递归基。
2. 自后向前比较，或 A[n] == B[m] == x，则取作 LCS(A[0, n), B[0, m)) + x，减而治之。
3. 若 A[n] != B[m]，这里分 2 种情况，一种是 B[m] 对 LCS 无贡献，此时最终值为 LCS(A[0, n], B[0, m)); 另一种是 A[n] 对 LCS 无贡献，此时最终值为 LCS(A[0, n), B[0, m])，返回这 2 种情况的最长者。

复杂度为 $2^n$。

这和 Fib() 类似，有大量重复的递归实例（子问题）。

各子问题，分别对应于 A 和 B 的某前缀组合，总共有 O(nm) 种。 采用动态规划策略，只需 O(nm) 时间。

1. 将所有子问题（假想地）列表一个表
2. 颠倒计算方向，从 LCS(A[0], B[0]) 出发，依次计算所有项，并填写表格。
3. 对于每个单元，如果减而治之情况（元素匹配），则值取左上值+1，如果是分而治之（不匹配），则值为左边和右边值的最大值。

![intro_LCS_dynamic_programming.png](/assets/images/tsinghua_dsacpp/c1_intro/intro_LCS_dynamic_programming.png)

动态规划能消除重复。


# 参考

+ [学堂在线公开课](http://www.xuetangx.com/courses/TsinghuaX/30240184X/2014_T2/about?Spam=3)
+ [数据结构 C++ 版第三版](https://book.douban.com/subject/25859528/)

