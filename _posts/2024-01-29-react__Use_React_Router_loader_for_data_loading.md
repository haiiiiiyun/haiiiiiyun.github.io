---
title: Use React Router loader for data loading
date: 2024-01-29
tags: react router
categoris: Programming
---

1. We define a **loader** that handle data loading in route.
2. React Router calls the loader to get the data before it renders the component defined on the route.
3. The data is available in the component via `useLoaderData` hook.
4. Component is rendered only after the data is fetched.
5. The data is fetched only once and won't be re-fetched again.

```typescript
// router
const router = createBrowserRouter([
  ...,
  { path: '/some-page', element: <SomePage />,
	loader: async () => {
	  const response = await fetch('https://somewhere');
	  return await response.json();
	}
  }
])
```

```typescript
// component
export function SomePage(){
  const data = useLoaderData();
}
```

## Deferred React Router data fetching

If the data-fetching process is slow, there will be a noticeable delay before a component is rendered by React Route. We can use React Router's `defer` function and `Await` component, along with React's `Suspense` component to resolve this:

```typescript
// route
import { createBrowserRouter, RouterProvider, defer } from "react-router-dom";
import { getPosts } from "./posts/getPosts";
import { PostsPage } from "./posts/Posts.Page";

const router = createBrowserRouter([
  { path: '/', element: <PostsPage />, 
    loader: async () => defer({
      posts: getPosts()
    })
  }
])
```

```typescript
// component
import { Suspense } from "react";
import { useLoaderData, Await } from "react-router-dom";
import { assertIsPosts } from "./getPosts";
import { PostData, NewPostData } from "./types";
import { PostsList } from "./PostsList";
import { savePost } from "./savePost";
import { NewPostForm } from "./NewPostForm";

type Data = {
    posts: PostData[]
};

export function assertIsData(data: unknown): asserts data is Data {
    if (typeof data !== "object") {
        throw new Error("Data isn't an object");
    }
    if (data === null){
        throw new Error("Data is null");
    }
    if (!("posts" in data)){
        throw new Error("data doesn't contain posts");
    }
}

export function PostsPage() {
    const data = useLoaderData();
    assertIsData(data);

    async function handleSave(newPostData:NewPostData) {
        await savePost(newPostData);
    }

    return (
        <div className="w-96 mx-auto mt-6">
            <h2 className="text-xl text-slate-900 font-bold">Posts</h2>
            <NewPostForm onSave={handleSave} />
            <Suspense fallback={<div>Fetching...</div>}>
                <Await resolve={data.posts}>
                    {(posts) => {
                        assertIsPosts(posts);
                        return  <PostsList posts={posts} />;
                    }}
                </Await>
            </Suspense>
        </div>
    )
}
```