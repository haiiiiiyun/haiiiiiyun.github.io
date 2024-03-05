---
title: Handle uncontrolled form fields in React
date: 2024-01-25
tags: react forms
categoris: Programming
---

**Uncontrolled fields** are the opposite of controlled fields--it's where field values aren't controlled by state, also see [[Handle controlled form fields in React]].

`FormData` is an interface that takes in a form element in its constructor parameter, and allows access to values in a form.

```typescript
import { FormEvent } from 'react';

type Contact = {
    name: string;
    notes: string;
};

export function ContactPage(){
    const fieldStyle = "flex flex-col mb-2";

    function handleSubmit(e: FormEvent<HTMLFormElement>) {
        e.preventDefault();
        const formData = new FormData(e.currentTarget);
        const contact = {
            name: formData.get('name'),
            notes: formData.get('notes'),
        } as Contact;
        console.log('Submitted details:', contact);
    }

    return (
        <div className="flex flex-col py-10 max-w-md mx-auto">
            <form onSubmit={handleSubmit}>
                <div className={fieldStyle}>
                    <label htmlFor='name'>Your name</label>
                    <input type="text" id="name" name="name"/>
                </div>
                <div className={fieldStyle}>
                    <label htmlFor='notes'>Additional notes</label>
                    <textarea id="notes" name="notes"/>
                </div>
                <div>
                    <button type="submit" className='mt-2 h-10 px-6 font-semibold bg-black text-white'>Submit</button>
                </div>
            </form>
        </div>
    )
}
```