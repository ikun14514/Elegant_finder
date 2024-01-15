# FanQieNovel

## 目录结构
- App.py # 文件主体
- config.py # 配置文件

## 示例
`search`方法获得书本基本信息，例如标题、作者、类型、封面等等，实例展示:  
```python
fanqie = FanQie() # 实例化类
fanqie.search('要搜索的内容')
```
返回数据结构:  
```
{
  msg:
    [
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
```python
fanqie.direct(book_id)
```
返回数据结构：
```
{
  msg:
    [
      {
        item_id: '章节独一无二的标识',
        title: '章节标题',
        volume_name: '卷名'
      }
    ]
}
```
`content`方法获取正文，传参**item_id**，返回类型是一段**html**代码，实例展示：  
```python
fanqie.content(item_id)
```
