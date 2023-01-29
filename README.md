# reptile.inclued/爬虫库
个人写的一点点爬虫.  
通过不断优化、改进慢慢做成这样.  
也会定期进行维护检测(**可能**).  
**meth.py**是我二次封装的**requests库**，毕竟那么大一堆重复性的代码，谁也不想每次都写吧(**偷懒罢了**).  
使用之前请务必安装**requests库**:
```
pip install requests
```
## Change Log
### v0.1.0 (2023/1/30)
- 更正目录结构，增加可读性  
- 新增**Pixivel.reptile**
- 优化**FanQie.Novel.reptile**结构
- python版本需要3.10+来支持**match-case**语句
## Pixivel.reptile
言归正传，这个爬虫文件我一年前就做好了，近期进行重构了一下，并加入了**多线程**下载的功能.  
**Pixivel**是国内的网站，具体和国外是镜像还是啥关系没看过，只不过**api**极其相似(**懂我意思吧**).  
使用案例：  
```
pa = Pa() # 实例化类
pa.run('这里填写检索的内容', 这里填写页数) # 这是填了多少页就获取第多少页的图片
```
在这里推荐一种循环方法`map()`，具体操作看下面  
```
list(map(lambda x: a.run('大白腿', x), range(11)))
```
如果第24行报错，你们把`image`文件夹建好就行，修改保存位置也是第24行.  
```
open(f'image/{pid}.jpg', "wb")
```
多线程的关闭方法(**其实我觉得没必要写，这爬虫的效率全靠多线程**):  
第71行中的`thread`换成`download`就好了:  
```
lambda x, y: self.thread(x, y)
```
后面如果有不错的想法会补充进去的.
## FanQie.Novel.reptile
得益于各路大神对**app**的一些操作，我们也就看到了某知名小说平台的爬虫(**广告少点我能写这个？**)  
要使用程序，你得获取你某小说的**cookie**，也就是**fanqienovel.com**中去获取.  
然后在``Cookie line:7``这里填写上，或者你们自己添加一个方法来添加.  
`search`方法获得书本基本信息，例如标题、作者、类型、封面等等，实例展示:  
```
fanqie = FanQie() # 实例化类
fanqie.search('要搜索的内容')
```
返回数据结构:  
```
{
  msg: [
  {
    abstract: '简介',
    author: '作者',
    book_id: '书的唯一标识',
    thumb_url: '封面链接',
    title: '书名'
  }
  ]
}
```
`direct`方法获得书本目录，传参进去呢，就是**book_id**，实例展示：  
```
fanqie.direct(book_id)
```
返回数据结构：
```
{
  "msg": [
    {
      item_id: '章节独一无二的标识',
      title: '章节标题',
      volume_name: '卷名'
    }
    ]
}
```
`content`方法获取正文，传参**item_id**，返回类型是一段**html**代码，实例展示：  
```
fanqie.content(item_id)
```
## 其他爬虫
整理灵感，多久更新我也不知道，感觉自己在写一些过时的东西
## LICENSE
MIT
