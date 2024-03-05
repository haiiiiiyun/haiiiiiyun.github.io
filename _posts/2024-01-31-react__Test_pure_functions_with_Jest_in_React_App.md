---
title: Test pure functions with Jest in React App
date: 2024-01-31
tags: react tests jest
categoris: Programming
---

## Test file extensions

[Jest](https://jestjs.io/) is preinstalled in a create-react-app project and configured to look for test in files with particular extensions such as `.test.ts` for tests on pure functions and `.test.tsx` for tests on components.

Alternatively, a `.spec.*` file extension could be used.

## Define a test

A test is defined using Jest's `test` function:

```typescript
test('your test name', () => {
  // your test implementation
  const someResult = yourFunction('someArgument');
  expect(someResult).toBe('something');
});
```

The test implementation function can be asynchronous with a `async ()` keyword.

## Test name

It's best practice to use the following test naming  structure:

`should {expected output/behavio} when {input/state condition}`, for example: `should return true when in checkedIds`

## Test files location

It's best practice to place test files adjacent to the source file being tested. This allows the developers to navigate to the test for a function quickly.

## use toThrow match to test exceptions

Jest has a `toThrow` matcher that can be used to check whether an exception has been raised. For this to catch exceptions, the function being tested has to be executed inside the expectation:

```typescript
test('some test', () => {
  expect(() => {
    someAssertionFunction(someValue);
  }).toThrow('some error message');
});
```

## Matchers

`expect` function is used to define expectations, it returns an object containing methods we can use to check specific expectations for the result.

These methods are referred to as **matchers**.

Some are some metchers:

1. `toBe`: checks that primitive values are equal, for example `expect(someResult).toBe('something')`
2. `toStrictEqual`: recursively checks every property in an object or array, for example:

  ```typescript
  expect(someResult).toStrictEqual({
	field1: 'something',
	 field2: 'something else'
  })
```

 3.  `not` for checking the opposite of a matcher: `expect(someResult).not.toBe('something')`

4. `toMatch` for checking strings against **regexes**, `expect(someResult).toMatch(/error/)`

5. `toContain` for checking if an element is in an array: `expect(someRsult).toContain(99)`

A complete list of all the standard matches, see https://jestjs.io/docs/expect

## Run tests

```bash
npm run test
```

or just `npm t`