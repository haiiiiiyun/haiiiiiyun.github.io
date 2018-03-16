---
title: 数据结构 C++ 版本笔记--3.列表
date: 2018-03-16
writing-time: 2018-03-16
categories: programming
tags: Programming data&nbsp;structure algorithm
---


# 三、列表

列表中元素的前驱后续索引关系，用位置 position 表示，元素 “循位置访问” call-by-position，或 call-by-link，如同通过你的朋友找到他的朋友。

![header_trailer.png](/assets/images/tsinghua_dsacpp/c3_list/header_trailer.png)

封装时，对象中始终包含两个哨兵节点(sentinel node) 头节点 header 和尾节点 trailer。而真正的第一个节点和最后一个节点称为首节点 first node 和 末结点 last node。

引用哨兵节点能简化算法的描述与实现，避免对各种分界退化情况做专门处理。


## 插入排序 insertion sort

适用于包括向量与列表在内的任何序列结构。

思路：始终将整个序列视作并切分为两部分，有序的前缀 s[0, r) 和无序了后缀 S[r, n);通过迭代，反复地将后缀的首元素转移到前缀中。

由此亦看出插入排序算法的不变性。

**在任何时刻，相对于当前节点 e=S[r], 前缀 S[0, r) 总是业已有序。**

![insertionsort.png](/assets/images/tsinghua_dsacpp/c3_list/insertionsort.png)

借助有序序列的查找算法，可在该前缀中定位到不大于 e 的最大元素，再将 e  从无序后缀中取出，并紧邻于查找返回的位置之后插入。

```cpp
//插入排序
template <typename T> //列表的插入排序：对起始于位置 p 的 n 个元素排序
void List<T>::insertionSort( ListNodePosi(T) p, int n) { //valid(p) && rank(p) + n <= size
    for (int r=0; r<n; r++) { //逐一为各节点
        // search(e, r, p) 返回 p 的 r 个真前驱中不大于 e 的最后者位置
        insertA( search(p->data, r, p), p->data); 
        p = p->succ; //转向下一节点
        remove(p->pred);
    }
} //O(n^2)

//有序列表的查找
//返回的位置应便于后续的（插入等）操作
template <typename T> //在有序列表内节点 p(可能是 trailer) 的 n 个真前驱中，找到 <= e 的最后者
ListNodePosi(T) List<T>::search( T const& e, int n , ListNodePosi(T) p ) const {
    // assert: 0 <= n <= rank(p) < _size
    while( 0 <= n--) //对于 p 的最近的 n 个前驱，从右到左逐个比较
        if ( ((p=p->pred)->data) <= e) //直到命中，数值越界或范围越界
            break;
    //assert: 至此位置 p 必符合输出语义约定--尽管此前最后一次关键码比较可能没有意义（等效于与 -inf比较)
    return p; //返回查找终止的位置
} //失败时，返回区间左边界的前驱（可能是 header) --调用者可通过 valid() 判断成功与否
//O(n)
```

### 向后分析 backward analysis

![backwardAnalysis.png](/assets/images/tsinghua_dsacpp/c3_list/backwardAnalysis.png)

插入排序时，分析第 r 个元素插入完成的时刻。在独立均匀分布的情况下，L[r] 插入到前面的 r+1 个位置的概率都是相同的，都是 1/(r+1)，而插入各位置所需的操作次数分别是 0, 1, ... r，从而 S[r] 表示花费时间的数学期望是 [r+(r-1)+...+1+0]/(r+1) + 1 = r/2 + 1

从而知道第 r 个元素的插入期望值为 r/2+1，从而总体元素的期望，即全部元素的期望的总和即为插入排序的平均时间复杂度，为 $O(n^2)$。



## 选择排序 selection sort

也适用于向量与列表之类的序列结构。

构思： 将序列划分为无序的前缀 S[0, r) 及有序的后缀 S[r, n)，此后还要求前缀中的元素都不大于后缀中的元素。如此，每次只需从前缀中选出最大者，并作为最小元素转移至后缀中，即可使有序部分的范围不断扩张。

![selectionSort.png](/assets/images/tsinghua_dsacpp/c3_list/selectionSort.png)

```cpp
//选择排序
//将序列划分为无序的前缀 S[0, r) 及有序的后缀 S[r, n)，此后还要求前缀中的元素都不大于后缀中的元素。如此，每次只需从前缀中选出最大者，并作为最小元素转移至后缀中，即可使有序部分的范围不断扩张。
template <typename T> //列表的选择排序算法，对起始于位置 p 的 n 个元素排序
void List<T>::selectionSort ( ListNodePosi(T) p, int n) { //valid(p) && rank(p)+n <= size
    ListNodePosi(T) head = p->pred;
    ListNodePosi(T) tail = p;
    for (int i=0; i<n; i++)
        tail = tail->succ; //将 head 和 tail 指向排序区列表的 header 和 tailer

    while( 1<n ) { //在至少还剩下两个节点之前，在待排序区间内
        ListNodePosi(T) max = selectMax( head->succ, n); //找出最大者
        insertB( tail, remove(max) ); // 将无序前缀中的最大者移到有序后缀中作为首元素
        // swap(tail->pred->data, max->data); // 优化：可以不用按上面进行删除和插入操作，只需互换数值即可, 习题 3-13
        tail = tail->pred;
        n--;
    }
} //O(n^2)


template <typename T> //从起始于位置 p 的 n 个元素中选出最大者，相同的返回最后者
ListNodePosi(T) List<T>::selectMax( ListNodePosi(T) p, int n) {
    ListNodePosi(T) max = p; //最大者暂定为首节点 p
    for ( ListNodePosi(T) cur = p; 1 < n; n--) //从首节点 p 出发，将后续节点逐一与 max 比较
        if ((cur=cur->succ)->data >= max->data) //若当前元素 >= max, 则
            max = cur;
    return max; //返回最大节点位置
}
```

## 归并排序 merge sort

```cpp
template <typename T> //有序列表的归并：当前列表中自 p 起的 n 个元素，与列表 L 中自 q 起的 m 个元素归并
void List<T>::merge( ListNodePosi(T) &p, int n, List<T>& L, ListNodePosi(T) q, int m) {
    //assert: this.valid(p) && rank(p)+n<=_size && this.sorted(p,n)
    //        L.valid(q) && rank(q)+m<=L._size && L.sorted(q,m)
    //注：在归并排序之类的场合，有可能 this==L && rank(p)+n=rank(q)
    //为方便归并排序，归并所得的有序列表依然起始于节点 p
    ListNodePosi(T) pp = p->pred; //方便之后能返回 p

    while ( 0 < m ) //在 q 尚未移出区间之前
        if ( (0<n) && (p->data <= q->data) ){ //若 p 仍在区间内且 v(p) <= v(q)
            if ( q == ( p=p->succ ) ) // 如果此时 p 部分已经处理完，则提前返回
                break;
            n--;  // p 归入合并的列表，并替换为其直接后继
        }
        else { //若 p 已超出右界或 v(q) < v(p) 则
            ListNodePosi(T) bb = insertB( p, L.remove( (q=q->succ)->pred )); //将 q 转移到 p 之前
            m--;
        }

    p = pp->succ; //确定归并后区间的起点
}


template <typename T> //列表的归并排序算法：对起始于位置 p 的 n 个元素排序
void List<T>::mergeSort( ListNodePosi(T) & p, int n) { //valid(p) && rank(p)+n <= _size
    if (n<2) 
        return;

    int m = n >> 1; //以中点为界
    ListNodePosi(T) q = p;
    for ( int i=0; i<m; i++) //均分列表
        q = q->succ; 

    mergeSort(p, m);
    mergeSort(q, n-m); //对前后子列表排序

    merge(p, m, *this, q, n-m); //归并
}//注意：排序后，p 依然指向归并后区间的起点

ListNodePosi(int) create_node(int data) {
    ListNodePosi(int) node = new ListNode<int>();
    node->data = data;
    return node;
}
```

## 倒置

```cpp
//习题 3-18，共 3 种实现方式
template <typename T>
void List<T>::reverse() {  //适合 T 类型不复杂，能在常数时间内完成赋值操作的情况
    ListNodePosi(T) p = header;
    ListNodePosi(T) q = trailer;
    for (int i=0; i<_size; i+=2){ //从首末节点开始，由外而内，捉对地
        /*p = p->succ;              // 交换对称节点的数据项
        q = q->pred;
        swap(p->data, q->data);
        */
        swap( (p=p->succ)->data, (q=q->pred)->data );
    }
}


template <typename T>
void List<T>::reverse2() {  //适合 T 类型复杂，不能在常数时间内完成赋值操作的情况
    if (_size < 2)
        return;

    ListNodePosi(T) p; ListNodePosi(T) q;

    for ( p = header, q = p->succ; p != trailer; p = q, q = p->succ )
        p->pred = q; //自前向后，依次颠倒各节点的前驱指针

    for ( p = header, q = p->pred; p != trailer; p = q, q = p->pred )
        q->succ = p; //自前向后，依次颠倒各节点的后续指针

    // 准备互换头尾
    trailer->pred = NULL;
    header->succ = NULL;
    swap( header, trailer);
}

template <typename T>
void List<T>::reverse3() {  //适合 T 类型复杂，不能在常数时间内完成赋值操作的情况
    if (_size < 2)
        return;

    for ( ListNodePosi(T) p = header; p; p = p->pred ) //自前向后，依次
        swap(p->pred, p->succ);
    swap(header, trailer);
}
```

# 参考

+ [学堂在线公开课](http://www.xuetangx.com/courses/TsinghuaX/30240184X/2014_T2/about?Spam=3)
+ [数据结构 C++ 版第三版](https://book.douban.com/subject/25859528/)

