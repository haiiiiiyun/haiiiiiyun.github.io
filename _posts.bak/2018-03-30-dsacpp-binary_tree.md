---
title: 数据结构 C++ 版本笔记--5.二叉树
date: 2018-03-30
writing-time: 2018-03-30
categories: programming
tags: Programming data&nbsp;structure algorithm
---

# 五、二叉树


任何有根有序的多叉树，都可等价地转化并实现为二叉树。

![btree.png](/assets/images/tsinghua_dsacpp/c5_binary_tree/btree.png)

+ 节点 v 的深度 depth(v): v 到根的通路上所经过的边的数目，也就是 v 所在的层。规定根在第 0 层
+ 节点 v 的度数或(出)度 deg(v): 即 v 的孩子总数。该值也表示该节点连出去的边数
+ n 个节点的树中，其边的总数为所有节点的出度（即 deg9v) 的总和，刚好为 n-1，O(n)
+ 树的所有节点深度的最大值称为树的高度 height(T)，约定只有一个节点（即根节点）的树的树高为 0,空树的高为 -1
+ 而节点 v 的高度即为其子树的高度 height(v)
+ 二叉树 binary tree: 即每个节点的度数不超过 2
+ K 叉树 k-ary tree: 每个节点的度数不超过 k 的有根树
+ 在二叉树中，在深度为 k 的层次上，最多有 $2^k$ 个节点
+ 在二叉树中，k 层最多 $2^k$ 个节点，则当有 h 层时，最多有节点数 n= $\sum_{k=0} ^{h}2^k$ = 2^{h+1} -1 `<` $2^{h+1}$，特别地，当 n= $2^{h+1} -1$，称为满树


![btree_numbers.png](/assets/images/tsinghua_dsacpp/c5_binary_tree/btree_numbers.png)

### 多叉树的表示方法

+ 以父节点表示，每个节点中存储父节点信息。访问父节点 O(1)，访问子节点，要遍历所有节点，O(n)。

![parent_representation.png](/assets/images/tsinghua_dsacpp/c5_binary_tree/parent_representation.png)

+ 以子节点表示，每个节点中将其所有子节点组织为一个列表或向量。若有 r 个子节点，则访问子节点 O(r+1)，访问父节点 O(n)。

![children_representation.png](/assets/images/tsinghua_dsacpp/c5_binary_tree/children_representation.png)


+ 父节点+子节点表示，操作方便，但节点的添加删除时，树拓扑结构的维护成本高。

![parent_children_representation.png](/assets/images/tsinghua_dsacpp/c5_binary_tree/parent_children_representation.png)

### 有序多叉树可转换为二叉树

有序多叉树中，同一节点的所有子节点也定义有次序。

转换时后，原节点的**长子（即第一个子节点）** 成为了其左节点，原节点的**下一个兄弟** 成为了其右节点。

![mTree2bTree.png](/assets/images/tsinghua_dsacpp/c5_binary_tree/mTree2bTree.png)

## 编码树

编码即将一个字符集中的每一个字符映射到一个唯一的二进制串。为避免解码时产生歧义，编码方案中每个字符对应的编码都不能是某个字符编码的前缀。这是一种可行的编码方案，叫 **前缀无歧义编码, Prefix-Free Code，PFC**。

### 二叉编码树

任一编码方案都可描述为一棵二叉树，每次向右（右）对应一个 0(1)。从根节点到每个节点的唯一通路，可以表述为一个二进制串，称为 **根通路串 root path string**。PFC 编码树的要求是，每个要映射的字符都必须位于叶子节点，否则，会出现某个字符是另一个字符的父节点，即其编码将会是另一编码的前缀。

如下图中，左边的是一个可行的 PFC 树，右边的不可行。

![PFC_instance.png](/assets/images/tsinghua_dsacpp/c5_binary_tree/PFC_instance.png)

基于 PFC 编码树的解码算法，可以在二进制串的接收过程中实时进行，属于**在线算法**。

# 先序遍历

![preorder_raversal.png](/assets/images/tsinghua_dsacpp/c5_binary_tree/preorder_raversal.png)

## 递归版本

```cpp
template <typename T, typename VST>
void travPre_R(BinNodePosi(T) p, VST& visit) { //二叉树先序遍历算法（递归版本）
    if (!p)
        return;

    visit(p->data);
    travPre_R(p->lChild, visit);
    travPre_R(p->rChild, visit);
}
```

## 消除尾递归

这是一个尾递归，引用辅助栈后可消除尾递归：

```cpp
//习题 5-10 使用栈消除尾递归
template <typename T, typename VST>
void travPre_I1(BinNodePosi(T) p, VST& visit) { //二叉树先序遍历算法（迭代1：使用栈消除尾递归）
    Stack<BinNodePosi(T)> s; //辅助栈

    if (p) //根节点入栈
        s.push(p);

    while (!s.empty()) { //在栈变空之前反复循环
        p = s.pop();
        visit(p->data); //先访问

        if (HasRChild(*p))
            s.push(p->rChild); //要先压入右子树节点

        if (HasLChild(*p))
            s.push(p->lChild);
    }
}
```

## 迭代版本 2

![travPre_Iterate.png](/assets/images/tsinghua_dsacpp/c5_binary_tree/travPre_Iterate.png)

考查先序遍历，它的过程，可分解为两段：

+ 先沿 **最左侧通路(leftmmost path)** 自顶而下访问沿途节点。
+ 再自底而上遍历对应的右子树。

在自顶而下过程中，引用辅助栈，存储对应节点的右子树。

```cpp
//从当前节点出发，自顶而下沿左分支不断深入，直到没有左分支的节点，沿途节点遇到后立即访问，
//引入辅助栈，存储对应节点的右子树
template <typename T, typename VST>
static void visitAlongLeftBranch(BinNodePosi(T) p, VST& visit, Stack<BinNodePosi(T)>& S){
    while (p) {
        visit(p->data); //访问当前节点

        if (p->rChild) //右孩子入栈暂存（优化：通过判断，避免空的右孩子入栈）
            S.push(p->rChild);
        
        p = p->lChild; //沿左分支深入一层
    }
}

template <typename T, typename VST>
void travPre_I2(BinNodePosi(T) p, VST& visit) { //二叉树先序遍历算法（迭代2）
    Stack<BinNodePosi(T)> S; //辅助栈

    S.push(p);

    while(!S.empty())
        visitAlongLeftBranch( S.pop(), visit, S);
}
```


```cpp
//习题 5-23, 在 O(n) 时间内将二叉树中每一节点的左右孩子（其中之一可能为空）互换
// 参考先序遍历的迭代版本
template <typename T>
void swap_pre_R(BinNodePosi(T) p) { //递归版本

    if (p)
        swap(p->lChild, p->rChild);

    if (p->lChild)
        swap_pre_R(p->lChild);

    if (p->rChild)
        swap_pre_R(p->rChild);
}

template <typename T>
void swap_pre_I1(BinNodePosi(T) p) { //使用栈消除尾递归
    Stack<BinNodePosi(T)> S;

    if (p)
        S.push(p);

    while( !S.empty() ){
        p = S.pop();
        swap(p->lChild, p->rChild);

        if (p->rChild)
            S.push(p->rChild);

        if (p->lChild)
            S.push(p->lChild);
    }
}

template <typename T>
void swapAlongLeftBranch(BinNodePosi(T) p, Stack<BinNodePosi(T)>& S) {

    while (p) {
        swap(p->lChild, p->rChild);

        if (p->rChild)
            S.push(p->rChild);

        p = p->lChild;
    }
}

template <typename T>
void swap_pre_I2(BinNodePosi(T) p) {
    Stack<BinNodePosi(T)> S;

    S.push(p);

    while( !S.empty() ) {
        p = S.pop();
        swapAlongLeftBranch(p, S);
    }
}
```


# 中序遍历

![inorder_traverse.png](/assets/images/tsinghua_dsacpp/c5_binary_tree/inorder_traverse.png)

## 递归版本

```cpp
template <typename T, typename VST>
void travIn_R(BinNodePosi(T) p, VST& visit) { //二叉树中序遍历算法（递归版本）
    if (!p)
        return;

    travIn_R(p->lChild, visit);
    visit(p->data);
    travIn_R(p->rChild, visit);
}
```


## 迭代版本 1

![inorder_trav_interate.png](/assets/images/tsinghua_dsacpp/c5_binary_tree/inorder_trav_interate.png)

考查遍历过程：

1. 从根结点开始，先沿最左侧通路自顶而下，到达最左的节点（即没有左孩子的节点），将沿途的节点压入辅助栈
2. 现在可以访问最左的节点了，因此从栈中弹出该节点，访问它，如果它有右孩子，则将右孩子压入栈中（此后在迭代中能完成该右孩子为根的子树的相同遍历过程）
3. 从栈中弹出一个节点，再次迭代。

```cpp
template <typename T> //从当前节点出发，沿左分支不断深入，直到没有左分支的节点
static void goAlongLeftBranch(BinNodePosi(T) p, Stack<BinNodePosi(T)>& S) {
    while (p){
        S.push(p);
        p = p->lChild;
    }
}

template <typename T, typename VST>
void travIn_I1(BinNodePosi(T) p, VST& visit) { //二叉树中序遍历算法，迭代版本 1
    Stack<BinNodePosi(T)> S; //辅助栈

    while( true ){
        goAlongLeftBranch(p, S); //从当前节点出发，逐批入栈
        if (S.empty()) //直到所有节点处理完毕
            break;
        p = S.pop(); visit(p->data); //弹出栈顶节点并访问
        p = p->rChild; //转向右子树
    }
}
```

## 迭代版本 2

```cpp

template <typename T, typename VST>
void travIn_I2(BinNodePosi(T) p, VST& visit) { //二叉树中序遍历算法，迭代版本 2
    Stack<BinNodePosi(T)> S; //辅助栈

    while( true ){
        if (p) { //沿最左侧通路自顶而下，将节点压入栈
            S.push(p);
            p = p->lChild;
        }
        else if (!S.empty()) {
            p = S.pop(); //尚未访问的最低祖先节点
            visit(p->data);
            p = p->rChild; //遍历该节点的右子树
        }
        else 
            break;  //遍历完成
    }
}
```

## 直接后继及其定位

遍历能将半线性的二叉树转化为线性结构。于是指定遍历策略后，就能在节点间定义前驱和后继了。其中没有前驱（后继）的节点称作首（末）节点。

定位中序遍历中的直接后继对二叉搜索树很重要。

```cpp
template <typename T>
BinNodePosi(T) BinNode<T>::succ() { //定位节点 v 的直接后继
    BinNodePosi(T) s = this; //记录后继的临时变量

    if (rChild) { //若有右孩子，则直接后继必在右子树中，具体地就是
        s = rChild; //右子树中的
        while (HasLChild(*s)) //最靠左（最小）的节点
            s = s->lChild;
    } else { //否则，直接后继应是 “将当前节点包含于基左子树中的最低祖先”，具体地就是
        while (IsRChild(*s))
            s = s->parent; //逆向地沿右向分支，不断朝左上方移动

        s = s->parent; //最后再朝右上方移动一步，即抵达直接后继（如果存在）
    }

    return s;
}
```

有右孩子的情况，如下图中的节点 b, 直接后继就是右子树中的最左节点 c。

没有右孩子的情况，如图中的 e, 查找过程是先沿右向分支不断朝左上方移到 d，最后再朝右上方移动一步到 f，即后继为 f，特别地，节点 g 的后继为 NULL。

![inorder_I_instance.png](/assets/images/tsinghua_dsacpp/c5_binary_tree/inorder_I_instance.png)

![succ_inorder.png](/assets/images/tsinghua_dsacpp/c5_binary_tree/succ_inorder.png)


```cpp
//习题 5-14
//遍历能将半线性的二叉树转化为线性结构。于是指定遍历策略后，就能在节点间定义前驱和后继了。其中没有前驱（后继）的节点称作首（末）节点。
template <typename T>
BinNodePosi(T) BinNode<T>::pred() { //定位节点 v 的直接前驱
    BinNodePosi(T) s = this; //记录前驱的临时变量

    if (lChild) { //若有左孩子，则直接前继必在左子树中，具体地就是
        s = lChild; //左子树中的
        while (HasRChild(*s)) //最靠右（最大）的节点
            s = s->rChild;
    } else { //否则，直接前继应是 “将当前节点包含于其左子树中的最低祖先”，具体地就是
        while (IsLChild(*s))
            s = s->parent; //逆向地沿左向分支，不断朝右上方移动

        s = s->parent; //最后再朝左上方移动一步，即抵达直接前驱（如果存在）
    }

    return s;
}
```

## 迭代版本 3

```cpp
template <typename T, typename VST>
void travIn_I3(BinNodePosi(T) p, VST& visit) { //二叉树中序遍历算法：版本 3, 无需辅助栈
    bool backtrack = false; //前一步是否刚从右子树回溯 -- 省去栈，仅 O(1) 辅助空间
                            //回溯回来的表示当前节点的左侧都已经访问过了

    while (true)
        if (!backtrack && HasLChild(*p)) //若有左子树且不是刚刚回溯，则
            p = p->lChild; //深入遍历左子树
        else { //否则--无左子树或刚刚回溯（左子树已访问完毕）
            visit(p->data); //访问该节点
            if (HasRChild(*p)) { //若有右子树，则
                p = p->rChild; //深入右子树继续遍历
                backtrack = false; //并关闭回溯标志
            } else { // 若右子树为空，则
                if (!(p=p->succ())) //后继为空，表示抵达了末节点
                    break;
                backtrack = true; //并设置回溯标志
            }
        }
}
```

![inorder_backtrack.png](/assets/images/tsinghua_dsacpp/c5_binary_tree/inorder_backtrack.png)


## 迭代版本 4

```cpp
//习题 5-17
template <typename T, typename VST>
void travIn_I4(BinNodePosi(T) p, VST& visit) { //二叉树中序遍历算法：版本4,无需辅助栈和标记
    while (true) {
        if (HasLChild(*p))  //若有左子树，则
            p = p->lChild;  //深入遍历左子树
        else {              //否则
            visit(p->data);  //访问当前节点，并
            while (!HasRChild(*p))   //不断地在无右分支处
                if (!(p=p->succ()))  //回溯至直接后继（在没有后继的末节点处，直接退出）
                    return;
                else
                    visit(p->data);  //访问新的当前节点
            p = p->rChild;           //直到有右分支处，转向非空的右子树
        }
    }
}
```


# 后序遍历

![postorder_traverse.png](/assets/images/tsinghua_dsacpp/c5_binary_tree/postorder_traverse.png)

## 递归版本

```cpp
template <typename T, typename VST>
void travPost_R(BinNodePosi(T) p, VST& visit) { //二叉树后序遍历算法（递归版本）
    if (!p)
        return;

    travPost_R(p->lChild, visit);
    travPost_R(p->rChild, visit);
    visit(p->data);
}
```

## 迭代版本

![postorder_iterate.png](/assets/images/tsinghua_dsacpp/c5_binary_tree/postorder_iterate.png)

将树 T 画在二维平面上，从左侧水平向右看去，未被遮挡的最高叶节点 v（称作最高左侧可见叶节点 HLVFL），即为后序遍历首先访问的节点，该节点可能是左孩子，也可能是右孩子（故用垂直边表示）。

沿着v 与树根之间的通路自底而上，整个遍历也可分解为若干个片段。每一片段，分别起始于通路上的一个节点，并包括三步：访问当前节点，遍历以其右兄弟（若存在）为根的子树，最后向上回溯至其父节点（若存在）并转下下一片段。

在此过程中，依然利用栈逆序地保存沿途所经各节点，以确定遍历序列各个片段在宏观上的拼接次序。

```cpp
template <typename T> //在以栈 S 顶节点为根的子树中，找到最高左侧可见叶节点
static void gotoHLVFL(Stack<BinNodePosi(T)> & S) { //沿途所遇节点依次入栈
    while (BinNodePosi(T) p = S.top()) //自顶而下，反复检查当前节点（即栈顶）
        if (HasLChild(*p)) { //尽可能向左
            if (HasRChild(*p))
                S.push(p->rChild); //若有右孩子，优先入栈
            S.push(p->lChild); //然后才转至左孩子
        }
        else //实不得已
            S.push(p->rChild); //才向右

    S.pop();//返回之前，弹出栈顶的空节点
}

template <typename T, typename VST>
void travPost_I(BinNodePosi(T) p, VST& visit) { //二叉树的后序遍历（迭代版本）
    Stack<BinNodePosi(T)> S; //辅助栈

    if (p)
        S.push(p); //根入栈

    while (!S.empty()) {
        if (S.top() != p->parent) //若栈顶不是当前节点之父（则必为其右兄），
            gotoHLVFL(S); //则此时以其右兄为根的子树中，找到 HLVFL

        p = S.pop(); //弹出该前一节点之后继，并访问
        visit(p->data); 
    }
}
```


```cpp
//习题 5-25
// O(n) 内将每个节点的数值替换为其后代中的最大数值
// 参考后序遍历
#define MIN_T 0  //设 T 类型的最小值为 0
template <typename T>
T replace_as_children_largest_post_R(BinNodePosi(T) p) { //参考后序递归版本
    if (!p)
        return MIN_T;

    T max_left = replace_as_children_largest_post_R(p->lChild);
    T max_right = replace_as_children_largest_post_R(p->rChild);
    p->data = max( p->data, max( max_left, max_right));
    return p->data;
}

template <typename T>
void replace_as_children_largest_post_I(BinNodePosi(T) p) { //参考后序迭代版本
    Stack<BinNodePosi(T)> S;

    if (p)
        S.push(p);

    while(!S.empty()) {
        if (S.top() != p->parent) //若栈顶不是当前节点之父，则必为其右兄
            gotoHLVFL(S); //则此时以其兄为根的子树中，找到 HLVFL

        p = S.pop();

        if (p->lChild && p->data < p->lChild->data)
            p->data = p->lChild->data;
        if (p->rChild && p->data < p->rChild->data)
            p->data = p->rChild->data;

    }
}
```

# 层次遍历

即先上后下，先左后右，借助队列实现。

![levelorder_traversal.png](/assets/images/tsinghua_dsacpp/c5_binary_tree/levelorder_traversal.png)

```cpp
// 层次遍历
//即先上后下，先左后右，借助队列实现。
template <typename T, typename VST>
void travLevel(BinNodePosi(T) p, VST& visit) { //二叉树层次遍历
    Queue<BinNodePosi(T)> Q; //辅助队列
    Q.enqueue(p); //根入队

    while (!Q.empty()) {
        BinNodePosi(T) p = Q.dequeue(); visit(p->data); //取出队首节点并访问

        if (HasLChild(*p))
                Q.enqueue(p->lChild);

        if (HasRChild(*p))
                Q.enqueue(p->rChild);
    }
}
```

## 完全二叉树  complete binary tree

叶节点只能出现在最底部的两层，且最底层叶节点均处于次底层叶节点的左侧。

![complete_btree.png](/assets/images/tsinghua_dsacpp/c5_binary_tree/complete_btree.png)

对于高度为 h 的完全二叉树，规模应在 $2^h$ 和 $2^{h+1} - 1$ 之间。

完全二叉树 可借助向量结构实现紧凑存储和高效访问。

## 满二叉树 full binary tree

每层结点都饱和。

![full_btree.png](/assets/images/tsinghua_dsacpp/c5_binary_tree/full_btree.png)

第 k 层的节点数是 $2^k$，当高为 h 时，总结点数是 $2^0+ 2^1+\cdots+2^h = 2^{h+1}-1$，内部节点是 $2^{h+1}-1 -2^h = 2^h-1$，叶结点为 $2^h$，叶节点总是恰好比内部节点数多 1。


# 二叉树的重构

中序 + 先序（或后序）就能还原二叉树。

![btree_rebuild.png](/assets/images/tsinghua_dsacpp/c5_binary_tree/btree_rebuild.png)

以先序+中序为例，用数学归纳法，设当 `n<N` 时以上结论成立。当 `n=N` 时，由先序遍历序列可知，这一节点为根节点。再由中序序列，可得出左子树和右子树，从而问题规模减少为两个子树，和假设相符，故成立。

只用先序+后序无法还原，因为当某个子树为空时会有岐义，但是当任何节点的子树个数为偶数时（0或2时，即为真二叉树）可还原。


# Huffman 编码

## PFC 编解码

![PFC_progress.png](/assets/images/tsinghua_dsacpp/c5_binary_tree/PFC_progress.png)

可自底而上，两两子集合并，最终生成一个全集。首先，由每一字符分别构造一棵单节点二叉树，并将它们视作一个森林（向量），此后，反复从森林中取出两棵树并将其合二为一，从而合并生成一棵完整的 PFC 编码树。再将 PFC 编码树转译成编码表。之后通过查表，将字符转化成对应的二进制编码串。

解码过程为，将接收到的编码串在编码树中反复从根节点出发做相应的漫游，依次完成各字符的解码。

## 最优编码树

编码效率主要体现在所生成的二进制编码串的平均长度。

字符 x 的编码长度即为其对应叶节点的深度 depth(v(x))，而各字符的平均编码长度即为编码树 T 中各叶子节点的平均深度 (average leaf depth, ald)。

ald(T) 值最小时，对应一棵最优编码树。

最优编码树的性质：

+ 双子性：即该树必是真二叉树，其内部节点的左右子全双。
+ 层次性：任何叶节点间的深度差不得超过 1。

因此，其叶节点只能出现于最低两层，这类树的一种特例就是真完全树。

### 构建方法

若字符集含 n 个字符，则先创建一棵规模为 2n-1 的完全二叉树，将字符集中的字符任意分配给 T 的 n 个叶节点即可。

## Huffman 编码树

考虑字符出现的概率不同，考查带权平均编码长度与叶节点的带权平均深度 wald(T)。

这种情况下，完全二叉编码树或满树，其对应的 wald(T) 不一定是最小的。

### 最优带权编码树

其 wald(T) 最小。

性质：

+ 双子性依然满足
+ 层次性： 若字符 x 和 y 出现的概率最低，则它们必同处于最优树的最底层，且互为兄弟。

### Huffman 编码算法

已知字符集以及各字符出现的概率。

1、选出概率最小的两个字符，根据层次性，这两节点必处于最底层，将这两节点合并成一棵二叉树，树根节点的概率为该两字符概率之和。
2、将以上构建的子树的根假想为一个字符，返回原来的字符集中一并处理，返回第 1 步再反复合并。最后可得到一棵最优带权编码树（即 Huffman 编码树）。

Huffman 编码树只是最优带权编码树中的一棵。

# 参考

+ [学堂在线公开课](http://www.xuetangx.com/courses/TsinghuaX/30240184X/2014_T2/about?Spam=3)
+ [数据结构 C++ 版第三版](https://book.douban.com/subject/25859528/)

