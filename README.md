<div align="center">  

# 随机图片查看器
# Random Image Viewer

</div>


# 简 介
一个类似于Line of Action的随机显示本地图片的程序。可以对着自己收集的参考图练习，不用受制于非会员的图库和自己的选择困难症了。  
可以遍历给定目录下的所有图像，通过方向键右随机查看。
支持以原顺序查看之前随机的图片，支持定时切换图片，支持暂停定时，支持图片旋转。  
可以将遍历的文件路径放在内存里，每次运行程序重新遍历；也可以将文件路径保存在数据库中，省去每次遍历目录的时间。  
可以设置全屏/窗口大小、窗口背景色。可以让每次随机的顺序相同。  


# 程序下载

戳[这里](https://github.com/passerbyzhao/RandomImageViewer/releases)


# 使用方法
## 0.本地图片目录

首先选择一个心仪的图片文件夹，将其路径粘贴到程序根目录下的`目录.txt`中。
- 如果根目录下没有`目录.txt`可以手动创建，也可以运行一次程序让程序创建。
- 文件夹中可以嵌套文件夹，也可以包含非图像文件（但是文件多的话会延长文件树生成速度）。
- 可以一次性放入多条路径。此时请每行只粘贴一条路径。
- 路径需要使用绝对路径。
- 支持的图片格式：`.jpg .png .jpeg .bmp .tif .tga .eps .psd` 
想要增加支持的图片格式需要使用源码。
- 根目录下的`config.ini`是配置文件。


## 1.运行模式
运行模式指遍历后的文件路经保存方式，通过修改配置文件参数`mode`指定。有`ontime`和`mongodb`两个选项。
默认使用实时模式。

#### ontime 实时模式

将生成的文件树保存在内存里。每次运行程序需要重新生成文件树。文件数量较少时比较好用，省去配置数据库的烦恼。
那么什么程度文件算多呢，...自己试试？~~1w以下？~~

#### mongodb 数据库模式

使用MongoDB数据库保存文件树。相比实时模式只需要生成一次文件树，对于包含大量图像的文件夹来说省去了每次启动程序等待文件树生成的时间。
通过使用不同的数据库表还可以快速更改目标文件树。  

使用数据库模式需要安装pymongo。具体操作请看下文[-1.使用MongoDB](#-1.使用MongoDB)



## 2.快捷键

### 2.1 GUI快捷键
`enter(回车键)` 开始图片浏览（相当于点击开始）  
`shift+enter`或`ctrl+enter` 开始浏览LIKES数据库表（相当于点击喜爱列表）（仅限数据库模式）  

### 2.2 浏览中快捷键

`esc ctrl+q q` 关闭图片窗口 退出程序  
`f ctrl+f` 全屏/窗口切换  
`方向键右(->)` 下一张图片  
`方向键左(<-)` 上一张图片  
`<(，逗号)` 顺时针旋转90度  
`>(。句号)` 逆时针旋转90度  
`enter(回车键)` 开始/暂停计时切图  
`鼠标滚轮` 上一张/下一张图片  
`ctrl+s` 将本次运行种子保存到程序目录下的‘SavedSeed.txt’文件内  
`l` 将当前图片路径储存到LIKES数据库表内（仅限数据库模式）  
`crtl+l`  将当前图片路径从LIKES数据库表内删除（仅限数据库模式）

除了这些，还支持matplotlib的快捷键。如果有需要（缩放什么的）可以
[去看看](https://matplotlib.org/stable/users/explain/interactive.html#key-event-handling) 。


## 3.小功能
- #### 计时功能

通过修改配置文件参数`time`设置。单位是秒，默认是600秒（10分钟）。计时结束后会自动切换到下一张图片。

- #### 背景色  

通过修改配置文件参数`background`设置。默认为黑色。可以通过（部分）颜色的英文单词指定。
可接收参数请看[这里](https://matplotlib.org/stable/tutorials/colors/colors.html#sphx-glr-tutorials-colors-colors-py)

- #### 随机

可以通过修改配置文件`seed`参数设置随机数生成器的种子，固定随机模式。每次运行会输出当前使用的种子（默认为程序启动时间）。


## 4.示例
> 默认情况（实时模式、时间间隔10分钟、背景为黑色、全屏）  
> 效果：  
> <img alt="regular" src="https://github.com/passerbyzhao/RandomImageViewer/blob/318c99f711c641b7176f011cc3a69db0f5eb520c/img/regular.png" width=889 height=555.5/>

> 背景色为白色 时间间隔30秒（实时模式、全屏）  
> `background=white time= 30`  
> 效果：  
> <img alt="white_background" src="https://github.com/passerbyzhao/RandomImageViewer/blob/318c99f711c641b7176f011cc3a69db0f5eb520c/img/back-white.png" width=889 height=555.5/>

> 指定窗口尺寸为800*600 设置随机数生成器种子为42 使用数据库模式（时间间隔10分钟、背景为黑色）  
> `screensize=800,600 seed=42 mode=mongodb`  
> 效果：  
> <img alt="window" src="https://github.com/passerbyzhao/RandomImageViewer/blob/318c99f711c641b7176f011cc3a69db0f5eb520c/img/window.png" width=889 height=555.5/>


## 5.高级设置
- #### 屏幕尺寸

用`screensize`指定。想调整尺寸请传入宽和高，单位是像素，宽在前高在后，用英文逗号分隔，如`600,600`。

也可以在运行时手动拖动窗口修改。~~这个功能有什么意义~~

- #### 自定义目标文件
用`targetpath`指定，默认为根目录下的`目录.txt`。如需指定需要传入目标文件的绝对路径。

- #### debug模式
debug模式会输出每张图片的地址。

## -1.使用MongoDB
通过`mode=mongodb`指定使用数据库模式。
`client`参数指定数据库地址，默认是本地数据库。`database`参数指定数据库名称，默认为`RandomImage`。
`collection`参数指定数据库表名，默认为`ImagePath`。  

初次使用数据库或者图片目录发生改动需要使用`initialize`参数调用数据库初始化方法，将文件树保存到数据库内。
```diff
- 注意：
```
`initialize`方法会清空当前数据库表之后再保存新文件树。  

当图片目录中添加新图片可以使用`update`调用数据库更新方法，将新图片的路径保存到数据库中。
目录中少几张图片无需调用该方法，程序运行时会自动删除无效路径。  

当想清除数据库表中的数据时可以通过`clear`调用删除方法。
```diff
- 一定要想清楚再删库。
```


# 注意
- 程序初始化稍微有些慢。
- 暂停计时切图的时候没有提示，你可能不清楚当前计时是运行还是暂停的状态。
- 暂停计时时计时器其实还在走，如果等待时间超过设定值，在取消暂停后会立刻切换到下一张图片。
- <font color=red>`clear`参数慎用！会删除当前配置的数据库表！</font>
- 加载大图片的时候会费点劲。
- ~~在某些版本下会有白边（我只试了matplotlib 2.0.2），我也没定位到bug，也不一定会修。~~
- `shift+enter`和`ctrl+enter`在实时模式下依旧可用，如果没装MongoDB会导致程序报错。
- 请不要给数据库表起名为`__new`，可能会导致未知bug。
- GUI未经过完整测试，可能存在未知bug，欢迎反馈。

# 使用源码

## 1.依 赖
[pillow](https://pillow.readthedocs.io/en/stable/installation.html)  
[matplotlib](https://matplotlib.org/stable/)  
[pymongo](https://github.com/mongodb/mongo-python-driver) （可选 不用数据库模式可以不装）  

## 2. 使用GUI请用`main_GUI.py`

GUI模式下的设定可以通过`config.ini`调整并保存，或者为什么不直接在GUI里操作呢 :-)

### 2.1 使用`main.py`时的可用参数

基础设置  
`-m` `--mode` 文件树保存模式 可选`ontime`和`mongodb` 默认为`ontime`  

`-t` `--time` 指定切换图片的等待时间 单位为秒 默认为600秒（10分钟）  
`-b` `--background` 指定背景颜色 默认为黑色  
`--seed` 指定随机数生成器的种子  

数据库相关  
`--client` 指定数据库地址 默认是`mongodb://localhost:27017/`  
`--database` 指定数据库名称 默认为`RandomImage`  
`--collection` 指定数据库表名 默认为`ImagePath`  
`--initialize` 调用数据库初始化方法 布尔值 默认为`False`  
`--update` 调用数据库更新方法 布尔值 默认为`False`   
`--clear` 调用删除方法 布尔值 默认为`False`
<font color=red> 慎用！ </font>

高级设置  
`--screensize` 指定窗口大小 设置请看下文  
`--showimage` 是否显示图片 默认显示 只是为了调试方便 给数据库喂数据时也挺好用  
`--configfile`  
`--targetpath`  

irrelevant  
`-v` `--version` 版本号  
`-d` `--debug` debug模式   

## 3.高级设置
- #### 缓存 

~~提前读取几张图片，在显示图片时可以少花点时间（但是好像影响了初始化时间？）。~~ 由于功能冲突暂时禁用了缓存功能，反正目前也没起什么作用。  
~~反正我每次也画不了几张~~  

~~不建议自己修改，但是有需求可以去`imgcache.py`。
`INITCACHE`是初始化缓存大小，`MAXCACHE`每次更新后最多缓存数量，`CACHE`是启动更新的标志。
`CLEARCACHE`是总缓存的大小。~~

- #### 添加支持图片格式

理论上PIL能打开的图片都可以支持，但是我只添加了几个我认为比较常见的图片格式。
添加新的图片格式需要修改`dirtree.py`中的`ImageType`，将想添加的文件后缀加到列表里。

- #### 调整图片文件最小大小

为了防止程序读取到错误图片崩溃，添加了文件大小校验。默认大小小于100b的文件不会读取。修改该变量可以到`dirtree.py`的`MINFILESIZE`。


- #### debug模式
使用debug模式需要通过`--configfile`关闭配置文件，即配置文件的debug比命令行参数的debug优先级高。
debug模式的参数需要通过`main.py`中指定。debug模式会输出每张图片的地址。

## 4.实现方法
文件遍历通过`pathlib`的`iterdir`方法递归实现。  
数据库通过`pymongo`实现。  
随机通过`random.randint`结合列表/`find_one`方法的`skip`参数实现。  
图片通过`PIL`读取，缓存通过`Thread`实现，显示通过`matplotlib`实现。按键通过`mpl_connect`实现。

###### <font color=Black>Random Image Viewer v1.0</font>