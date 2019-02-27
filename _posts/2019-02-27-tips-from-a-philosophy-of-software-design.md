---
title: Tips from "A philosophy of software design"
date: 2019-02-27
writing-time: 2019-02-27
categories: software design
tags: software design
---

# Design Principles

## Make investments in design

1. Complexity is incremental: you have to sweat the small stuff.
1. Working code isn't enough.
1. Make continual small investments to improve system design.
1. Design it twice.
1. The increments of software development should be abstractions, not features.

## Simple Interface, Deep Implementation

1. Modules should be deep.
1. Interfaces should be designed to make the most common usage as simple as possible.
1. It's more important for a module to have a simple interface than a simple implementation.
1. General-purpose modules are deeper.
1. Seperate general-purpose and special-purpose code.
1. Different layers should have different abstractions: no pass-through methods, aware of interface duplication.
1. Pull complexity downward: pull the complexity down to implementation, keep the interface simple.
1. Define errors and special cases out of existence: don't throw unnecessary error to users, try to handle it in your code.

## Comment for reader, not for writer.

1. Comments should describe things that are not obvious from the code.
1. Software should be designed for ease of reading, not ease of writing.


# Summary of Red Flags: the presence of any of these symptoms in a system suggests that there is a problem with the system's design

+ **Shallow Module**: the interface for a class or method isn't much simpler than its implementation.
+ **Information Leakage**: a design decision is reflected in multiple modules.
+ **Temporal Decomposition**: the code structure is based on the order in which operations are executed, not on information hiding.
+ **Overexposure**: An API forces callers to be aware of rarely used features in order to use commonly used features.
+ **Pass-Through Method**: a method does almost nothing except pass its arguments to another mehod with a similar signature.
+ **Repetition**: a nontrivial piece of code is repeated over and over.
+ **Special-General Mixture**: special-purpose code is not cleanly separated from general-purpose code.
+ **Conjoined Methods**: two methods have so many dependencies that its hard to understand the implementation of one without understanding the implementation of the other.
+ **Comment Repeats Code**: all of the information in a comment is immediately obvious from the code next to the comment.
+ **Implementation Documentation Contaminates Interface**: an interface comment describes implementation details not needed by users of the thing being documented.
+ **Vague name**: the name of a variable or method is so imprecise that it doesn't convery much useful information.
+ **Hard to Pick Name**: it is difficult to come up with a precise an intuitive name for an entity.
+ **Hard to Describe**: in order to be complete, the documentation for a variable or method must be long.
+ **Nonobvious Code**: the behavior or meaning of a piece of code cannot be understood easily.


# Resources

+ [A Philosophy of Software Design 1st Edition](https://www.amazon.com/Philosophy-Software-Design-John-Ousterhout/dp/1732102201)
