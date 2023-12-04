---
title: Android Fragment 中使用 TTF 矢量字体图标（以 Font Awesome 4.7.0 为例)
date: 2018-03-02
writing-time: 2018-03-02
categories: programming
tags: Programming android font&nbsp;awesome
---

# 创建 Assets 文件夹

在 Android Studio 中将项目显示方式改为 `Project`，在 `app/src/main` 上右键 `New -> Folder -> Assets Folder`，

在 `app/src/main/assets` 上右键 `New -> Directory -> 填写 font`。

将下载的 [fontawesome-webfont-ttf](https://fontawesome.com/v4.7.0/) 文件复制到新建的 `assets/font/` 下。


# 编写资源文件，将图标代码与资源名称绑定

```xml
<!--/res/values/strings.xml 文件-->
<string name="fa_car">&#xf1b9;</string>
<string name="fa_apple">&#xf179;</string>
<string name="fa_android">&#xf17b;</string>
```

图标代码与名称对应关系见 [Font Awesome Cheatsheet](https://fontawesome.com/cheatsheet)。


# 布局文件中的 TextView 使用 Font Awesome

```xml
<!-- in layout file fragment.xml -->
<TextView
    android:id="@+id/tv"
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:layout_marginStart="8dp"
    app:layout_constraintStart_toEndOf="@+id/textView8"
    app:layout_constraintTop_toTopOf="@+id/textView8"
    android:textSize="24sp"
    android:textColor="@color/colorAccent"
    android:text="@string/fa_android" />
```

# Fragment 中创建字体，并设置 TextView 使用该字体

```java
public View onCreateView(LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
    View view = inflater.inflate(R.layout.fragment, container, false);
    Typeface font = Typeface.createFromAsset(getActivity().getAssets(), "font/fontawesome-webfont.ttf");
    TextView tv = (TextView)view.findViewById(R.id.tv);
    tv.setTypeface(font);
    //...
}
```

如果你想改变图标大小和颜色，只要修改字体的大小和颜色即可，也就是说只要修改 TextView 的 textSize 和 textColor。


# 参考

+ [Android 使用Font Awesome 显示文字图标](https://www.jianshu.com/p/a1ab20158bc0)
+ [矢量图标字体集](https://www.npmjs.com/package/react-native-vector-icons)

