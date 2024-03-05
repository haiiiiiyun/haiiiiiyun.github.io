---
title: Use React Router Form and action
date: 2024-01-25
tags: react forms router
categoris: Programming
---

1. React Router's **Form** component is a wrapper around the HTML **form** element.
2. The form is submitted to the current route by default, but can be submitted to a different path using the **path** attribute
3. We specify the form action handler function with `action` prop on the route that is submitted to
4. The action handler function takes an `{ request }` argument of type `ActionFunctionArgs` and we can get the formData with `const formData = await request.formData()`

```typescript
// form and action handler in Page.tsx
import {Form, ActionFunctionArgs, redirect} from 'react-router-dom';

type Contact = {
    name: string;
    notes: string;
};

export function ContactPage(){
    const fieldStyle = "flex flex-col mb-2";

    return (
        <div className="flex flex-col py-10 max-w-md mx-auto">
            <Form method='post'>
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
            </Form>
        </div>
    )
}

export async function contactPageAction({request}: ActionFunctionArgs) {
    const formData = await request.formData();
    const contact = {
        name: formData.get('name'),
        notes: formData.get('notes'),
    } as Contact;
    console.log('Submitted details:', contact);
    return redirect(`/thank-you/${formData.get('name')}`);
}
```

```typescript
// define form action in route:
const router = createBrowserRouter([
  {path: '/', element: <Navigate to="contact" />},
  {path: '/contact', element: <ContactPage />, action: contactPageAction},
  {path: '/thank-you/:name', element: <ThankYouPage />}
])
```