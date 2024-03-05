---
title: Implementing interfaces versus extending abstract classes in Typescript
date: 2023-12-28
tags: typescript types classes interfaces
categoris: Programming
---

They're really similar.

1. An interface is a way to model a shape. It's more general and lightweight. Interfaces do not emit JS code, only exist at compile time.
2. An abstract class can only model a class. It's more special-purpose and feature-rich. They emit runtime code that is a JS class.