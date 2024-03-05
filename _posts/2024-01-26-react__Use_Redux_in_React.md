---
title: Use Redux in React
date: 2024-01-26
tags: react state redux
categoris: Programming
---

**Redux** is a state management library. In Redux, the state lives in a centralized immutable object referred to as **store**. There is only a single store for the whole app.

## Install

```bash
npm i @reduxjs/toolkit react-redux
```

## create a store

```typescript
// in store.ts
import { configureStore } from "@reduxjs/toolkit";
import userReducer from './userSlice';

export const store = configureStore({
    reducer: {
        user: userReducer,
        someFeature: someFeatureReducer,
        anotherFeature: anotherFeatureReducer
    }
});

export type RootState = ReturnType<typeof store.getState>;
```

The **configureStore** function takes in the store's reducers. Each feature in the app can have its own area of state and reducers to change the state.

## Create slices

The different areas of state are often referred to **slices**.

```typescript
import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { User } from "../api/authenticate";

type State = {
  user: undefined | User;
  permissions: undefined | string[];
  loading: boolean;
};

const initialState: State = {
  user: undefined,
  permissions: undefined,
  loading: false
};

export const userSlice = createSlice({
    name: 'user',
    initialState,
    reducers: {
        authenticateAction: (state) => {
            state.loading = true;
        },
        authenticatedAction: (state, action: PayloadAction<User | undefined>) => {
            state.user = action.payload;
            state.loading = false;
        },
        authorizeAction: (state) => {
            state.loading = true;
        },
        authorizedAction: (state, action: PayloadAction<string[]>) => {
            state.permissions = action.payload;
            state.loading = false;
        }
    }
});

export const {
    authenticateAction,
    authenticatedAction,
    authorizeAction,
    authorizedAction
} = userSlice.actions;

export default userSlice.reducer;
```

The **createSlice** function takes in an object parameter containing the slice name, the initial state, and functions to handle the different actions and update the state.

The slice created from **createSlice** contains a **reducer** function that wraps the action handlers. This **reducer** can be referenced in the **reducer** property of **configureStore**.

## Provide the store to React components

```typescript
import { Header } from "./pages/Header";
import { Main } from "./pages/Main";
import { Provider } from "react-redux";
import { store } from "./store/store";

function App() {
  return (
    <div className="max-w-7xl mx-auto px-4">
      <Provider store={store}>
        <Header />
        <Main />
      </Provider>
    </div>
  )
}
```

## Access the store from a component using useSelector hook

```typescript
import { useSelector, useDispatch } from "react-redux";
import { RootState } from "../store/store";

export function Header() {
  const user = useSelector((state: RootState) => state.user.user);
  const loading = useSelector((state: RootState) => state.user.loading);
}
```

## Dispatch actions to the store from a component using useDispatch hook

```typescript
import { authenticate } from "../api/authenticate";
import { authorize } from "../api/authorize";
import { useSelector, useDispatch } from "react-redux";
import { RootState } from "../store/store";
import { authenticateAction, authenticatedAction, authorizeAction, authorizedAction } from "../store/userSlice";

export function Header() {
  const user = useSelector((state: RootState) => state.user.user);
  const loading = useSelector((state: RootState) => state.user.loading);
  const dispatch = useDispatch();

  async function handleSignInClick() {
    dispatch(authenticateAction());
    const authenticatedUser = await authenticate();
    dispatch(authenticatedAction(authenticatedUser));
    if (authenticatedUser !== undefined){
      dispatch(authorizeAction());
      const authorizedPermissons = await authorize(authenticatedUser.id);
      dispatch(authorizedAction(authorizedPermissons));
    }
  }
}
```