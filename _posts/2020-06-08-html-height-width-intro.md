---
title: Html 中各种宽高尺寸汇总
date: 2020-06-08
writing-time: 2020-06-08
categories: html
tags: html
---

# 1. window innerHeight 和 outerHeight

innerHeight 表示浏览器中页面内部呈现部分的高度，包括水平滚动条部分（如果有的话），不包括页面标签部分。

outerHeight 表示整个浏览器的高度。

![outerHeight and innerHeight](/assets/images/html/FirefoxInnerVsOuterHeight2.png)

参考 [Window innerHeight](https://developer.mozilla.org/en-US/docs/Web/API/Window/innerHeight)。


# 2. Element.clientHeight

元素内容在 box 中呈现部分高度：包括 padding，但不包括 borders, margins, horizontal scrollbars。

clientHeight = CSS height + CSS padding - height of horizontal scrollbar。

document height 等同于 html.clientHeight 或 body.clientHeight。

![Dimensions-client.png](/assets/images/html/Dimensions-client.png)

参考 [Element clientHeight](https://developer.mozilla.org/en-US/docs/Web/API/Element/clientHeight)

# 3. Element.offsetHeight

与 clientHeight 的区别是： offsetHeight 包含 borders 高度。

::before or ::after

参考 [HTMLElement offsetHeight](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/offsetHeight)

# 4. Element.scrollHeight

元素全部内容（包含因溢出未呈现部分）的高度。度量方式和 Element.clientHeight 一样，包括 padding，但不包括 borders, margins, horizontal scrollbars。

如果元素全部内容都能够呈现在 box 中，不出现垂直滚动条，则 Element.scrollHeight 等于 Element.clientHeight。

![Element scrollHeight](/assets/images/html/scrollHeight.png)

参考 [Element scrollHeight](https://developer.mozilla.org/en-US/docs/Web/API/Element/scrollHeight)


# 5. Element.scrollTop

表示元素内容向上滚动的高度值，即元素内容的顶部与呈现部分的顶部的距离，因此其值 `>=0`。

如果元素没有滚动条（未溢出），即 scollTtop 为 0，如果元素内容滚动到最下端，则 scrollHeight = scrollTop + clientHeight。

参考 [Element scrollTop](https://developer.mozilla.org/en-US/docs/Web/API/Element/scrollTop)
