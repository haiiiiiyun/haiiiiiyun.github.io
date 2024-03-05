---
title: Handle controlled form fields in React
date: 2024-01-25
tags: react forms
categoris: Programming
---

The values of **controlled fields** are stored in the state, user typing in fields will trigger page re-rendering, which is a performance issue.

The event type for form submitter handler is `FormEvent<HTMLFormElement>`.

```typescript
import { useState, FormEvent } from 'react';

type Contact = {
    name: string;
    notes: string;
};

export function ContactPage(){
	const [contact, setContact] = useState<Contact>({name: "", notes: ""});
    const fieldStyle = "flex flex-col mb-2";

    function handleSubmit(e: FormEvent<HTMLFormElement>) {
        e.preventDefault();
        console.log('Submitted details:', contact);
    }

    return (
        <div className="flex flex-col py-10 max-w-md mx-auto">
            <form onSubmit={handleSubmit}>
                <div className={fieldStyle}>
                    <label htmlFor='name'>Your name</label>
                    <input type="text" id="name" name="name" value={contact.name} onChange={(e) => setContact({...contact, name: e.target.value })} />
                </div>
                <div className={fieldStyle}>
                    <label htmlFor='notes'>Additional notes</label>
                    <textarea id="notes" name="notes" value={contact.notes} onChange={(e) => setContact({...contact, notes: e.target.value })}/>
                </div>
                <div>
                    <button type="submit" className='mt-2 h-10 px-6 font-semibold bg-black text-white'>Submit</button>
                </div>
            </form>
        </div>
    )
}
```