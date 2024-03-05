---
title: Simulate user interactions using user-event in React
date: 2024-01-31
tags: react tests react-testing-library
categoris: Programming
---

`user-event` is a React Testing Library companion package that simulates user interactions rather than specific events.

create-react-app does preinstall the `user-event` package, but it may be a version before v14, which has as different API, if so install the latest version by:

```bash
npm i @testing-library/user-event@latest
```

## Simulate user interactions in tests

```typescript
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { Checklist } from "./Checklist";

test('should check items when clicked', async () => {
    const user = userEvent.setup();
    render(
        <Checklist
          data={[{id: 1, name: 'Lucy', role: 'Manager'}]}
          id="id"
          primary="name"
          secondary="role"
        />
    );
    const lucyCheckbox = screen.getByTestId('Checklist__input__1');
    expect(lucyCheckbox).not.toBeChecked();

    await user.click(lucyCheckbox);
    expect(lucyCheckbox).toBeChecked();
})
```

The `user-event` package can simulate many interactions, see https://testing-library.com/docs/user-event/intro/