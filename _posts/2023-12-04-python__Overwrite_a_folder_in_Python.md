---
title: Overwrite a folder in Python
date: 2023-12-04
tags: python shell
categoris: Programming
---

```python
import os
import shutil

dir = 'path_to_my_folder'
if os.path.exists(dir):
    shutil.rmtree(dir)
os.makedirs(dir)
```

See https://stackoverflow.com/questions/11660605/how-to-overwrite-a-folder-if-it-already-exists-when-creating-it-with-makedirs