---
title: Test components with Jest and React Testing Library in React
date: 2024-01-31
tags: react tests jest react-testing-library
categoris: Programming
---

React Testing Library provides functions to render components and then select internal elements. Those internal elements can then be checked using special matchers provided by `jest-dom`, also see [[Test pure functions with Jest in React App]].

Both of these are preinstalled in a create-react-app project.

1. React Testing Library's `render` function renders the component.
2. `screen` object has many queries methods such as `getByText` that allows to select internal elements.
3. we use Jest's matcher to check expectation:

```typescript
import { render, screen } from '@testing-library/react';

test('should render heading when content specified', () => {
  render(<Heading>Some heading</Heading>);
  const heading = screen.getByText('Some heading');
  expect(heading).toBeInDocument();
})
```

## React Testing Library queries

Query is a method that selects a DOM element within the component being rendered.

### Find element in different ways:

1. ByRole: Quries elements by their role, see https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Roles
2. ByLabelText: Queries elements by their associated label.
3. ByPlaceholderText
4. ByText: by their text content
5. ByDisplayValue: Queries input, textarea, and select elements by their value.
6. ByAltText: Queries img elements by their alt attribute.
7. ByTitle: title attribute
8. ByTestId: by data-testid attribute

### Different types of queries, each query type has a particular prefix on the query method name:

1. getBy: Throws an error if a single element is not found. Used for synchronously getting a single element.
2. getAllBy: Throws an error if at least one element is not found. Used for synchronously getting multiple elements.
3. findBy: Throws an error if a single element is not found within a certain amount of time(1 second by default). Used for asynchronously getting a single element.
4. findAllBy: Throws an error if at least one element is not found within a certain time(1 second by default). Used for asynchronously getting multiple elements.
5. queryBy: This returns `null` if an element is not found. For checking that an element does not exist
6. queryAllBy: Same as queryBy, but returns an array of elements.

See https://testing-library.com/docs/queries/about/

Combine together, we get the query methods, such as `getByText()`, `queryByRole`,...

Notice that none of these queries references implementation details such as an element name, ID, or CSS class. If those implementation details change due to code refactoring, the tests shouldn't break, which is precisely what we want.

## Mathers

jest-dom contains lots of useful matchers for checking DOM elements, for example:

+ toBeInDocument: verifies an element is in the DOM
+ toBeChecked: checks whether an element is checked