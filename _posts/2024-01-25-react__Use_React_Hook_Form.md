---
title: Use React Hook Form
date: 2024-01-25
tags: react forms
categoris: Programming
---

**React Hook Form** is a React library for building forms. The key part of React Hook Form is a `useForm` hook, which returns useful functions and the state:

```typescript
const {
  register,
  handleSubmit,
  formState: { errors, isSubmitting, isSubmitSuccessful }
} = useForm<FormData>();
```

1. register

The **register** function takes in a unique field name and returns the following in an object structure:

+ **onChange** handler, which happens when the field editor's value changes
+ **onBlur** handler, which happens when the field editor losses focus
+ A reference to the field editor element
+ The field name

`<input {...register('name')} />` will become: 

```typescript
<input
  ref={someVariableInRHF}
  name="name"
  onChange={someHandlerInRHF}
  onBlur={someHandlerInRHF}
/>
```

2. Specifying validation

Field validation is defined in the register field in an options parameter as follows:

`<input {...register('name', {required: true})} />` or 
`<input {...register('name', {required: 'You must enter a name'})} />`.

All the validations rules, see https://react-hook-form.com/get-started#applyvalidation.

3. Obtaining validation errors

`errors` object could be as follows:

```typescript
{
  name: {
    message: 'You must enter a name',
    type: 'required'
  }
}
```

We can render it conditionally:

```typescript
{errors.name && <div>{errors.name.message}</div>}
```

4. Handling submission

**handleSubmit** can be used for form submission, it takes in a callback function that React Hook Form calls when it has successfully validated the form:

```typescript
function onSubmit(data: FormData){}

return (
  <form onSubmit={handleSubmit(onSubmit)}></form>
);
```

5. submitting state

**isSubmitting** state can be used to disable elements:

```typescript
<button type="submit" disabled={isSubmitting}>Submit</button>
```

**isSubmitSuccessful** state can be used to conditionally render a successful submission message:

```typescript
if (isSubmitSuccessful) {
	return <div>The form was successfully submitted</div>;
}
```