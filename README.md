# 说明

这是[haiiiiiyun](hhttps://haiiiiiyun.github.io)的个人博客。

本博客运行于 [Jekyll](http://jekyllrb.com) @ [GitHub](http://github.com/haiiiiiyun/haiiiiiyun.github.io)。

博客模板修改自 [github.com/Yonsm/NET](http://github.com/Yonsm/NET) 和 [github.com/webfrogs/webfrogs.github.com](https://github.com/webfrogs/webfrogs.github.com) 

若你对本博的模板感兴趣，欢迎克隆。

# 在本机运行

```bash
docker run \
  --name atjiang \
  -t \
  --restart always \
  -v "/home/hy/workspace/haiiiiiyun.github.io":/usr/src/app \
  -e JEKYLL_GITHUB_TOKEN=your_github_token \
  -p "9900:4000" starefossen/github-pages
```
