---
title: Use TanStack React Query for REST API calling cache
date: 2024-01-29
tags: react react-query todo ignore
categoris: Programming
---

[TanStack Query](https://tanstack.com/query/v4/docs/framework/react/overview) is a REST API data-fetching library which makes fetching, caching, synchronizing and updating server state in web applications a breeze.

## Install

```bash
npm i @tanstack/react-query
```

## Query Provider and client

React Query requires a `QueryClientProvider` component in the component tree above the components that need access to the data it manages. 

The provider also holds a `QueryClient` instance,  in component, we use `useQueryClient()` hook to get this instance, and use it for data accessing.

```typescript
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  );
}
```

## Get data using useQuery hook

```typescript
import { getPosts } from "./getPosts";
import { useQuery } from "@tanstack/react-query";

export function PostsPage() {
    const {isLoading, isFetching, isError, data:posts, } = useQuery(['postsData'], getPosts);
```

1. The first arg to `useQuey` is a unique key for the data.
2. The second arg is the fetching function

The following some of the de-structured state variables from `useQuery`:

+ `isLoading`: whether the component is being loaded for the first time
+ `isFetching`: whether the fetching function is being called.
+ `data`: the data has been fetched
+ `isError`: whether the fetch function errored.