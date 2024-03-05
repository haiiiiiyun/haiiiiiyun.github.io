---
title: Invoke functions with call apply bind in Typescript
date: 2023-12-21
tags: typescript functions
categoris: Programming
---

| method | example                   | description                                                                                                 |
| ------ | ------------------------- | ----------------------------------------------------------------------------------------------------------- |
| ()     | add(1,2)                  | normal function call                                                                                        |
| apply  | add.apply(null, [10, 20]) | binds a value to this, and spreads its second arguments over fun's paramaeters                              |
| call   | add.call(null, 10, 20)    | binds a value to this, but applies its arguments in order                                                   |
| bind   | add.bind(null, 10, 20)()  | binds a this-argument and a list of arguments to the fun. It returns a new function that we can then invoke | 