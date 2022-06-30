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
~~一个让你在运动时不用考虑选择困难症的程序~~


# 依 赖
[matplotlib](https://matplotlib.org/stable/)  
[pymongo](https://github.com/mongodb/mongo-python-driver) （可选 不用数据库模式可以不装）  


# 使用方法
##0.本地图片目录

首先选择一个心仪的图片文件夹，将其路径粘贴到程序根目录下的`目录.txt`中。
- 如果根目录下没有`目录.txt`可以手动创建，也可以运行一次程序让程序创建。
- 文件夹中可以嵌套文件夹，也可以包含非图像文件（但是文件多的话会延长文件树生成速度）。
- 可以一次性放入多条路径。此时请每行只粘贴一条路径。
- 路径需要使用绝对路径。
- 支持的图片格式：`.jpg .png .jpeg .bmp .tif .tga .eps .psd` 可以扩展。 关于增加支持的图片格式，请看[注意](#注意 "a")。


## 1.运行模式
运行模式指遍历后的文件路经保存方式，通过参数`--mode`指定。有`ontime`和`mongodb`两个选项。
默认使用实时模式。

####ontime 实时模式

将生成的文件树保存在内存里。每次运行程序需要重新生成文件树。文件数量较少时比较好用，省去配置数据库的烦恼。
那么什么程度文件算多呢，...自己试试？~~1w以下？~~

####mongodb 数据库模式

使用MongoDB数据库保存文件树。相比实时模式只需要生成一次文件树，对于包含大量图像的文件夹来说省去了每次启动程序等待文件树生成的时间。
通过使用不同的数据库表还可以快速更改目标文件树。  
使用数据库模式需要安装pymongo。具体操作请看[-1.使用MongoDB](#-1.使用MongoDB)


##2.快捷键
`esc ctrl+q q`  <font color=yellow>关闭图片窗口 退出程序</font>  
`f` 全屏/窗口切换  
`方向键右(->)` 下一张图片  
`方向键左(<-)` 上一张图片  
`<` 顺时针旋转90度  
`>` 逆时针旋转90度  
`enter(回车键)` 开始/暂停计时切图  

除了这些，还支持matplotlib的快捷键。如果有需要（缩放什么的）可以
[去看看](https://matplotlib.org/stable/users/explain/interactive.html#key-event-handling) 。


##3.小功能
- ####计时功能

通过参数`-t --time`设置。单位是秒，默认是600秒（10分钟）。计时结束后会自动切换到下一张图片。

- ####背景色  

通过参数`-b --background`设置。默认为黑色。可以通过（部分）颜色的英文单词指定。
其他可接收参数请看[这里](https://matplotlib.org/stable/tutorials/colors/colors.html#sphx-glr-tutorials-colors-colors-py)

- ####随机

可以通过`--seed`参数设置随机数生成器的种子，固定随机模式。每次运行会输出当前使用的种子（默认为程序启动时间）。


##4.示例
> 默认情况（实时模式、时间间隔10分钟、背景为黑色、全屏）  
> `python main.py`  
> 效果：  
> <img alt="regular" src="https://github.com/passerbyzhao/RandomImageViewer/blob/318c99f711c641b7176f011cc3a69db0f5eb520c/img/regular.png" width=889 height=555.5/>

> 背景色为白色 时间间隔30秒（实时模式、全屏）  
> `python main.py --background white -t 30`  
> 效果：  
> <img alt="white_background" src="https://github.com/passerbyzhao/RandomImageViewer/blob/318c99f711c641b7176f011cc3a69db0f5eb520c/img/back-white.png" width=889 height=555.5/>

> 指定窗口尺寸为800*600 设置随机数生成器种子为42 使用数据库模式（时间间隔10分钟、背景为黑色）  
> `python main.py --screensize 800,600 --seed 42 --mode mongodb`  
> 效果：  
> <img alt="window" src="https://github.com/passerbyzhao/RandomImageViewer/blob/318c99f711c641b7176f011cc3a69db0f5eb520c/img/window.png" width=889 height=555.5/>

##-1.使用MongoDB
数据库模式需要`pymongo`包。通过`--mode mongodb`指定使用数据库模式。
`--client`参数指定数据库地址，默认是本地数据库。`--database`参数指定数据库名称，默认为`RandomImage`。
`--collection`参数指定数据库表名，默认为`ImagePath`。  

初次使用数据库或者图片目录发生改动需要使用`--initialize`参数调用数据库初始化方法，将文件树保存到数据库内。
<font color=red>注意：</font>`initialize`方法会清空当前数据库表之后再保存新文件树。  
当图片目录中添加新图片可以使用`--update`调用数据库更新方法，将新图片的路径保存到数据库中。
目录中少几张图片无需调用该方法，程序运行时会自动删除无效路径。  
当想清除数据库表中的数据时可以通过`--clear`调用删除方法。<font color=red>一定要想清楚再删库。</font>


#注意
- 程序反应有点慢，特别是刚打开的时候。
- 暂停计时切图的时候没有提示，你可能不清楚当前计时是运行还是暂停的状态。
- 关于添加支持图片格式：理论上PIL能打开的图片都可以支持，但是我只添加了几个我认为比较常见的图片格式。
添加新的图片格式需要修改`dirtree.py`中的`ImageType`，将想添加的文件后缀加到列表里。注意：对大小写敏感。
- 暂停计时时计时器其实还在走，如果等待时间超过设定值，在取消暂停后会立刻切换到下一张图片。
- <font color=red>`--clear`参数慎用！会删除当前配置的数据库表！</font>
- 运行的时候会切换不了窗口。这是个bug，得改。
- 加载大图片的时候会费点劲，这时切换图片和旋转的响应时间会比较长。


#可用参数

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
<font color=red>慎用！</font>

高级设置  
`--screensize` 指定窗口大小 默认为全屏模式 设置请看下文  
`--cache` 缓存队列大小 可能对性能有稍微的改进？ 默认为15  

irrelevant  
`-v` `--version` 版本号  
`-d` `--debug` debug模式   


#高级设置
- ####窗口尺寸  

用`--screensize`指定。默认为全屏。
想调整尺寸请传入宽和高，单位是像素，宽在前高在后，用英文逗号分隔，如`600,600`。

也可以在运行时手动拖动窗口修改。~~这个功能有什么意义~~

- ####缓存 

提前从数据库或者内存中读取几条随机路径，在显示图片时可以少花点时间（存疑）。~~反正我每次也画不了几张~~
可能有作用也可能没作用。默认缓存15条路径。

缓存存在上限30，可以在`pathholder`中通过`MAXCACHE`修改


#实现方法
文件遍历通过`pathlib`的`iterdir`方法递归实现。  
数据库通过`pymongo`实现。  
随机通过`random.randint`结合列表/`find_one`方法的`skip`参数实现。  
图片通过`PIL`读取，显示通过`matplotlib`实现。按键通过`mpl_connect`实现。


###### <font color=Black>Random Image Viewer v0.1</font>