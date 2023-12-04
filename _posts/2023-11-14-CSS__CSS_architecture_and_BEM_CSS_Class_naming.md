---
title: CSS architecture and BEM CSS Class naming
date: 2023-11-14
tags: css class-naming
categoris: Programming
---

## CSS architecture

1. BEM(Block Element Modifier https://en.bem.info/methodology)
2. SMACSS(Scalable and Modular Architecture for CSS http://smacss.com)
3. OOCSS(Object-Oriented CSS: https://github.com/stubbornella/oocss/wiki).

## BEM: Block, Element, Modifier

BEM is a component-based architecture that aims to break user interface into independent, reusable blocks.

1. **Block**:  An example would be a class for an element, such as `header`
2. **Element**: The class name is the block name followed by two underscores and the element, such as `header__menu`.
3. **Modifier**:   describes the appearance, state and behavior. The class pattern is `blockName_modifierName`(example `header_mobile`) or `blockName__elementName_modifierName`(example `header__menu_open`)

CSS class and HTML tag id pattern is `cameralCase`.