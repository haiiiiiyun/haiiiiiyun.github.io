---
title: Android 笔记
date: 2018-01-29
writing-time: 2018-01-01--
categories: programming
tags: Android Android&nbsp;Programming&nbsp;2nd
---

# Android 基本知识

1. Activity 子类用来管理用户界面。
1. layout 是一个 XML 文件，用来定义一组用户界面对象及它们在屏幕上的位置。
1. 多个 widget 组成一个用户界面，每个 widget 都是 View 及其子类的一个实例，如 TextView, Button。
1. widget 属性 layout_width, layout_height, 值为 **match_parent** 表示撑满父 widget(另一个过时的值为 fill_parent)，而 **wrap_content** 表示满足其内容所需的大小。
1. AppCompatActivity 是 Activity 的子类，实现了对旧版本的兼容功能。
1. Activity 实例化时会调用自身的 `onCreate(Bundle savedInstanceState)` 方法用来初始化，该方法中要调用 `setContentView(layoutResID)` 来设置要管理的用户界面。
1. 资源及资源 ID `src/main/res/` 目录下，例如 `res/layout/activity_quiz.xml`, `res/values/string.xml` 等。Android 会根据这些资源定义自动生成一个 `R.java` 文件，位于 `build/generated/source/r/debug` 下。这个文件自动与所有源代码文件关联，因此可以在源代码中使用 `R.string.app_name` 的形式引用资源 ID。
1. 布局 XML 文件中指定的单个 widget 不会自动关联一个资源 ID，如果要在源代码中引用这些 widget，需要手动指定，如:

```xml
<Button
android:id="@+id/true_button"
android:layout_width="wrap_content"
android:layout_height="wrap_content"
android:text="@string/true_button" />
```

这里 `android:id="@+id/true_button"` 表示创建的资源 ID 为 `true_button`，可以使用 Activity 的方法 `findViewById(R.id.true_button)` 获取该 widget。
1. Activity 是 Context 的子类，可以用在 `Toast.makeText(Context context, int resId, int duration)` 等中。

# build 过程

res 下的所有资源文件（XML）由 aapt 工具(Android Asset Packaging Tool) 编译成一个编译过的资源文件和 R.java 文件，`src/` 下的源代码编译成 Java 的字节码，再 cross compile 成 Dalvik 字节码(.dex)，最后资源文件和 .dex 文件合并签名成一个 apk 文件。


# build 工具

使用  Gradle 工具来管理构建过程。

打开 Android Studio 下边的 Terminal, 运行 `$ ./gradlew tasks` 将下载并显示所有可用的 task。

运行 `$ ./gradlew installDebug` 将应用安装到连接的设备上。

# MVC

Model 层保存应用的数据和业务逻辑。

View 层一般是由布局文件创建的界面。

Controller 层关联 View 和 Model，是应用逻辑所有。一个 Controller 一般就是 Activity, Fragment, Service 子类。

# Screen pixel density:

+ mdpi medium-density screens (~160dpi)
+ hdpi high-density screens (~240dpi)
+ xhdpi extra-high-density screens (~320dpi)
+ xxhdpi extra-extra-high-density screens (~480dpi)


# Activity 的生命周期

![Activity State Diagram](/assets/images/androidprogrammingv2/activity_state_diagram.png)

当设备的配置有修改时，例如切换了设备的方向，Android 会销毁并重装创建 Activity，以应用最适合当前配置的资源配置信息，例如将 `res/layout/` 下的默认布局切换为 `res/layout_land/` 下的横屏布局。设备配置的修改情况还有：键盘的显示和关闭，语言的修改等。


# Layout XML 中的 tools

```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:gravity="center"
    android:orientation="vertical"
    tools:context="com.bignerdranch.android.geoquiz.CheatActivity">

   
    <TextView
        android:id="@+id/answer_text_view"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:padding="24dp"
        tools:text="Answer"/>

</LinearLayout>
```

添加 `xmlns:tools` 命名空间后，可以用 `tools:attr` 覆盖子 widget 上的属性值，用以将该值显示在预览界面中。例如 `TextView` 有 `text` 属性，则 `tools:text` 可以设置该 widget 在预览界面上的值，相当于是 spaceholder。


# Starting an Activity

![Starting an Activity](/assets/images/androidprogrammingv2/start_an_activity.png)


所有组件（Activities, services, broadcast receivers, content providers) 都通过 **intent** 进行通信。`Intent` 类提供多种构造器，适用于多种用途。

用于开启 Activity 的 Intent 构造器： `public Intent(Context packageContext, Class<?> cls)`。

`Class` 参数指定要开启的 `Activity` 类，`Context` 参数指定要哪个 package 中查找该类。

## Activity 间的数据传输

![Intent extras](/assets/images/androidprogrammingv2/intent_extras.png)

在 `Intent` 上使用 `public Intent putExtra(String name, boolean value)` 等多种形式（值参数有多种）来携带数据进行传送，对方通过 `getIntent().getBooleanExtra(name, defaultValue)` 取值。

## 开启  Activity 并返回结果

使用 `public void startActivityForResult(Intent intent, int requestCode)` 开启。其中 `requestCode` 是原样返回，当启动多个子 Activity 后，可用来区别是哪个 Activity 返回。

子 Activity 中使用 `public final void setResult(int resultCode[, Intent data])` 设置返回结果。其中 resultCode 的值一般为 `Activity.RESULT_OK` 和 `Activity.RESULT_CANCELED`。 如果子 Activity 没有调用 setResult 进行设置，当用户点回退键返回父 Activity 时，结果的 resultCode 默认为 `RESULT_CANCELED`。

父 Activity 中要重载 `protected void onActivityResult(int requestCode, int resultCode, Intent data)` 处理返回的结果。

## ActivityManager

系统只有一个 ActivityManger 和一个 Activity 的 Back Stack。

# Fragment

UI Fragment 也基于布局文件创建 UI，Activity 可由多个 Fragment 组合起来。

一般使用 support library 中的 Fragment 实现，而不使用本地 SDK 中的实现，这样可以在更低版本中使用。

需要在 app 模块中的 build.gradle 文件中指明依赖： `File->Project Structure...->Modules app->Dependencies->+->Library dependency`，添加 `support-v4`。


## Fragment 生命周期

![fragment_lifecycle.png](/assets/images/androidprogrammingv2/fragment_lifecycle.png)

和 Activity 不同，Fragment 的生命周期方法不是由 OS 调用，而是由其所在的 Activity 管理和调用。

Activity 通过 FragmentManager 管理其所有的 Fragment，以及一个 Back Stack.

![fragmentmanager.png](/assets/images/androidprogrammingv2/fragmentmanager.png)

Activity 中的一个容器放置一个 Fragment，因此 FragmentManger 通过容器的 ResID 来查找和标识 Fragment：

```java
FragmentManager fm = getSupportFragmentManager();
Fragment fragment = fm.findFragmentById(R.id.fragment_container);

if (fragment == null) {
    fragment = new CrimeFragment();
    fm.beginTransaction()
         .add(R.id.fragment_container, fragment)
         .commit();
}
```

当一个 Fragment 被添加到 FragmentManager 后，会依赖调用其生命周期函数 `onAttach(Activity)`, `onCreate(Bundle)`, `onCreateView(...)`，并随着 Activity 的状态同步执行 `onStart()`, `onResume`, ...

使用 Fragement 原则：屏幕上同时包含的 Fragment 个数不多于 2 或 3 个。


# RecyclerView, Adapter, ViewHolder


每个 ViewHolder 实例对应一个列表的行：

![ViewHolder.png](/assets/images/androidprogrammingv2/ViewHolder.png)

RecyclerView 通过 ViewHolder 管理每个具体列表行：

![ViewHolder.png](/assets/images/androidprogrammingv2/ViewHolder.png)

RecyclerView 通过  Adapter 创建 ViewHolder，并与具体的数据模型绑定：

![RecyclerView-Adapter.png](/assets/images/androidprogrammingv2/RecyclerView-Adapter.png)


RecyclerView 以支持库的形式提供，故要在 app 模块的 build.gradle 中添加依赖：

`compile 'com.android.support:recyclerview-v7:27.0.2'`， 见 https://developer.android.com/topic/libraries/support-library/packages.html 和 https://stackoverflow.com/questions/25477860/error-inflating-class-android-support-v7-widget-recyclerview


RecyclerView 对于显示组件的布局也是委托给布局管理器完成的，因此要设置一个布局管理器：

```java
public class CrimeListFragment extends Fragment {

    private RecyclerView mCrimeRecyclerView;

    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_crime_list, container, false);
        mCrimeRecyclerView = (RecyclerView) view.findViewById(R.id.crime_recycler_view);
        mCrimeRecyclerView.setLayoutManager(new LinearLayoutManager(getActivity()));
        
        return view;
    }
}
```

# Fragment Result

类似 Activity，Fragment 中也可以 `Fragment.startActivityForResult(Intent, int)` 启动一个返回结果的 Activity，同时也可以重载 `onActivityResult()` 来获取返回的结果。 但是只能是 Activity 才有结果，Fragment 不能有结果，因此，Fragment 没有 setResult 方法，只能设置 Activity 的结果： `getActivity().setResult(Activity.RESULT_OK, null)`。


# ViewPager

+ ViewPager 类直接继承了ViewGroup类，所有它是一个容器类，可以在其中添加其他的 View 类。
+ ViewPager 类需要一个 PagerAdapter 适配器类给它提供数据。
+ ViewPager 经常和 Fragment 一起使用，并且提供了专门的 FragmentPagerAdapter 和 FragmentStatePagerAdapter 类供 Fragment 中的 ViewPager 使用。

FragmentStatePagerAdapter 节约内存，它会调用 remove(Fragment) 将用不到的 Fragment 销毁。FragmentPagerAdapter 性能更好，但耗内存，它只调用 `detach(Fragment)`，不从内存中删除。


# AlertDialog

使用依赖包 AppCompat 中的 `android.support.v7.app.AlertDialog`, 确保新旧系统上界面风格一致。

AlertDialog 直接显示后，当设备方位转动后退出显示，因此应将 AlertDialog 封装成一个 `android.support.v4.app.DialogFragment`  中。

运行错误： `java.lang.NoSuchMethodError: No static method getFont...`： 确保支持包和编译的 SDK 版本都一致，例如：

```gradle
android {
    compileSdkVersion 27
    defaultConfig {
        applicationId "com.bignerdranch.android.criminalintent"
        minSdkVersion 16
        targetSdkVersion 27
        versionCode 1
        versionName "1.0"
        testInstrumentationRunner "android.support.test.runner.AndroidJUnitRunner"
    }
    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
        }
    }
}

dependencies {
    implementation fileTree(include: ['*.jar'], dir: 'libs')
    implementation 'com.android.support:appcompat-v7:27.0.0'
    compile 'com.android.support:recyclerview-v7:27.0.0'
}
```

# Fragment 间的数据交互

`父 -> 子`: 子中的 `newInstance(data)` 方法将由父传入的 data 封装成 Bundle，通过 Fragment.setArguments(bundle) 设置成 Fragment 的参数。父中调用子的 `newInstance(data)` 获取一个子的实例，子中通过 `getArguments().getSerializable(TAG)` 获取父传入的数据。

`子 -> 父`: 父中为子 Fragment 设置结果处理的目标 Fragment 为自身，`childFragment.setTargetFragment(parentFragment, REQUEST_CODE)`，子中通过 `Intent` 封装返回值，并调用父的 `parentFragment.onActivityResult(REQUEST_CODE, resultCode, intent)` 传回给父，父中重载 `onActivityResult()`。

父中通过 `startActivityForResult()` 开启普通的 Fragment，而通过 `show` 开启 `DialogFragment`。


# Toolbar

通过 AppCompat 支持库，可以在 API 7 之后的系统中使用 Toolbar。要使用 Toolbar 功能，确保所有的 Activity 都继承自 AppCompatActivity(它继承于 FragmentActivity）。


## Toolbar VS ACtion Bar

Action Bar 总是要在屏幕上方显示，且只能有一个 Action Bar，其尺寸固定。

Toolbar 没有这些限制，尺寸可调整，可以有多个 Toolbar（每个 View 有可设置自己的 Toolbar），Toolbar 中的 View 可设置。


# 应用的可访问目录

每个应该都有一个 sandbox 目录，以应用的包名命名，在 `/data/data` 目录下，例如 `/data/data/com.bignerdranch.android.criminalintent`。

# 编辑器

+ 安装 ideaVIM 插件： `File->Settings...->Plugins`。
+ 设置方向键的快捷键，方便在代码提示框中上下移动： `File-Settings...->Keymap->Editor Actions->`，Down 改为 `Ctrl J`，Up 改为 `Ctrl K`。


# Implicit Intent

通过 Implicit Intent 通知 OS 开启特定功能的应用。

Intent 中需指定的参数有：

+ action: 指定需开启的应用的功能，如 `Intent.ACTION_VIEW` 是打开浏览器，`Intent.ACTION_SEND` 是发送
+ data: 内容的 URI
+ type: 内容的类型，是 MIME 值
+ categories: 可选，描述你 where, when, how 使用打开的应用，例如 `android.intent.category.LAUNCHER` 表示该 Activity 应显示在 top-level app launcher 中。

每个应用的 Manifest 的 `intent-filter` 中声明自己的功能及参数，例如声明为浏览器功能：

```xml
<activity
    android:name=".BrowserActivity"
    android:label="@string/app_name" >
    <intent-filter>
        <action android:name="android.intent.action.VIEW" />
        <category android:name="android.intent.category.DEFAULT" />
        <data android:scheme="http" android:host="www.bignerdranch.com" />
    </intent-filter>
</activity>
```

当应用中通过 Implicit Intent 开启通讯录程序获取部分联系人信息时，通讯录程序返回包含 URI 的 intent 给父 Activity 时，会一并添加 `Intent.FLAG_GRANT_READ_URI_PERMISSION`，即父 Activity 无需声明要求的权限就能完成此次的权限操作（只这一次）。

## 获取联系人信息的 Intent

###  1. 在 AndroidManifest 中加入读写权限

<uses-permission android:name="android.permission.READ_CONTACTS" />
<uses-permission android:name="android.permission.WRITE_CONTACTS" />

### 2.  Android 系统管理联系人的 URI

+ 获取联系人的 ID 和 NAME: `ContactsContract.Contacts.CONTENT_URI`
+ 获取联系人的电话号码: `ContactsContract.CommonDataKinds.Phone.CONTENT_URI`
+ 获取联系人的邮箱地址: `ContactsContract.CommonDataKinds.Email.CONTENT_URI`

Contacts 有两个表，分别是 rawContact 和 Data，rawContact 记录了用户的 id 和 name,其中 id 栏名称为：`ContactsContract.Contacts._ID`, name 名称栏为 `ContactContract.Contracts.DISPLAY_NAME`,电话信息表的外键 id 为`ContactsContract.CommonDataKinds.Phone.CONTACT_ID`,电话号码栏为：`ContactsContract.CommonDataKinds.Phone.NUMBER`（字符串值）。

### 3. 获取手机号码并打开拨打电话界面的代码

```java
private static final int REQUEST_CONTACT_PHONE = 2;

mCallButton = (Button) v.findViewById(R.id.crime_call);
mCallButton.setOnClickListener(new View.OnClickListener() {
    @Override
    public void onClick(View v) {
        Intent pickContact = new Intent(Intent.ACTION_PICK,
            ContactsContract.CommonDataKinds.Phone.CONTENT_URI);
        startActivityForResult(pickContact, REQUEST_CONTACT_PHONE);
    }
});

@Override
public void onActivityResult(int requestCode, int resultCode, Intent data) {
    if (resultCode != Activity.RESULT_OK) {
        return;
    }

    if (requestCode == REQUEST_CONTACT_PHONE && data != null) {
        Uri contactUri = data.getData();
        String[] queryFields = new String[] {
            ContactsContract.CommonDataKinds.Phone.NUMBER
        };
        Cursor c = getActivity().getContentResolver()
                    .query(contactUri, queryFields, null, null, null);

        try {
            if (c.getCount() == 0) {
                return;
            }

            c.moveToFirst();
            String numberString = c.getString(0);
            Uri number = Uri.parse("tel:" + numberString);

            // to Dial
            Intent dialIntent = new Intent(Intent.ACTION_DIAL, number);
            startActivity(dialIntent);
        } finally {
            c.close();
        }
    }
}
```

# 为 Tablet 设置不同的资源值

创建资源时，将 qualifier 设置为 sw600dp，即 `smallest width` 为 600dp。

+ `wXXXdp` 表示宽度大于等于 XXX dp 的设备。
+ `hXXXdp` 表示高度大于等于 XXX dp 的设备。
+ `swXXXdp` 表示宽度或高度（测试小的那个量）大于等于 XXX dp 的设备。

# Assets

相当于打包进应用中的一个文件系统。

但是 Asset 文件路径不能像普通文件一样打开为 `File`，必须通过 `AssetManager` 操作：

```java
AssetManager mAssets = context.getAssets();
String assetPath = sound.getAssetPath();
InputStream soundData = mAssets.open(assetPath);

// AssetFileDescriptors are different from FileDescriptors,
AssetFileDescriptor assetFd = mAssets.openFd(assetPath);
// but you get can a regular FileDescriptor easily if you need to.
FileDescriptor fd = assetFd.getFileDescriptor();
```

# Retained Fragment

Fragment 可以设置为 retained(默认为 False)，这样当其父 Activity 销毁（如旋转）时，只进行 detach，不进行销毁，从而能保持 Fragment 中的数据和状态的一致性。

```java
    @Override
    public void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        // when a fragment is retained, the fragement is not
        // destroyed with the activity.
        // It is preserved and passed along intact to the new activity.
        setRetainInstance(true);
    }
```

![retained_fragment_life_cycle.png](/assets/images/androidprogrammingv2/retained_fragment_life_cycle.png)


# Style 和 Theme

style 名中用 `BaseStyleName.InheritedStyleName` 表示 `BaseStyleName.InheritedStyleName` 继承 `BaseStyleName`（只有当所有样式代码在相同包中才可以用）。

也可能过 `parent` 属性值指定父样式。

## 属性值的访问

在 XML 中，当引用一个具体值，如颜色值时，用 `@`，例如： `@color/gray`。当引用主题中的资源时，用 `?`，例如： `android:background="?attr/colorAccent"`，表示引用主题中名为 `colorAccent` 这个属性值。

而代码中引用主题属性值：

```java
Resources.Theme theme = getActivity().getTheme();
int[] attrsToFetch = { R.attr.colorAccent };
TypedArray a = theme.obtainStyledAttributes(R.style.AppTheme, attrsToFetch);
int accentColor = a.getInt(0, 0);
a.recycle();
```

# Launchable app

使用 `PackageManager` 查询 launchable main activity，即应用的 `AndroidManifest.xml` 中的 `intent-filter` 有：

```xml
<intent-filter>
<action android:name="android.intent.action.MAIN" />
<category android:name="android.intent.category.LAUNCHER" />
</intent-filter>
```

`startActivity(Intent)` 时， OS 会自动添加 category `CATEGORY_DEFAULT` 的匹配，故不适合用来启动 Launchable main activity.

## Tasks

一个 Task 关联一组开启的应用，用来保存用户的状态及 Back Stack。点击右下角的 Recent tasks list 按钮，可打开 Overview screen, 进行 Task 的切换。

开启新的 Task 只需添加一个 Flag 即可：

```java
Intent i = new Intent(Intent.ACTION_MAIN)
    .setClassName(activityInfo.applicationInfo.packageName,
        activityInfo.name)
    .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
startActivity(i);
```

## 使用 AsyncTaskLoader 完成数据任务

### Parse JSON in JAVA

[Gson](https://github.com/google/gson) 能直接将 JSON 转成 Java 对象。# 参考

...
