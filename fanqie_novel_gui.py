import sys
from PySide6 import QtWidgets
# from PySide2 import QtWidgets
# from PyQt5 import QtWidgets
# from qt_material import apply_stylesheet
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile, QIODevice  
from PySide6.QtCore import Slot, QStringListModel, QStringListModel
import requests, time, re, json
from lxml import etree, html

def getHtml(url, enc):
    headers = {
    'User-Agent' :'Mozilla/5.0 (Danger hiptop 3.4; U; AvantGo 3.2)'
    }
    html = requests.get(url, headers=headers)
    html.encoding = enc
    return html.text

def get_in_fan(uid):
    '''
    uid:书本的book_id，可以在get_in_book模块里面查询得到
    这个模块可以查询到所有的章节id，然后传输到get_in_text里面
    '''
    url = f"https://api5-normal-lf.fqnovel.com/reading/bookapi/directory/all_items/v/?need_version=true&book_id={uid}&iid=2665637677906061&aid=1967&app_name=novelapp&version_code=495"
    allpoint = []
    data = getHtml(url, 'utf-8')
    data = json.loads(data)
    data = data["data"]
    data = data["item_data_list"]
    return data

def get_in_book(name):
    '''搜索书本的基础信息，获取book_id以供使用'''
    url = f"https://api5-normal-lf.fqnovel.com/reading/bookapi/search/page/v/?offset=0&passback=&query={name}&search_id=&iid=4125792742674311&aid=1967"
    allpoint = []
    try:
        data = getHtml(url, 'utf-8')
        data = json.loads(data)
        data = data["data"]
        for i in data:
            data = i["book_data"]
            data = data[0]
            res = {
            'book_name': data["book_name"],
            'abstract': data["abstract"],
            'author': data["author"],
            'score': data["score"],
            'book_id': data["book_id"]
            }
            allpoint.append(res)
        return allpoint
    except:
        return None

@Slot()
def AddButton(self):
    info = self.textEdit.toPlainText()
    allpoint = []
    lis = get_in_fan(info)
    for i in lis:
        data = i["title"]
        allpoint.append(data)
    slm = QStringListModel()
    slm.setStringList(allpoint)
    self.listView.setModel(slm)

@Slot()
def Click(self):
    self.plainTextEdit.clear()
    info = self.textEdit.toPlainText()
    info1 = self.listView.selectionModel().selectedIndexes()[0].row()
    allpoint = get_in_fan(info)
    op = allpoint[info1]["item_id"]
    url = f"https://novel.snssdk.com/api/novel/book/reader/full/v1/?group_id={op}&item_id={op}"
    data = getHtml(url, 'utf-8')
    data = json.loads(data)
    data = data["data"]
    data2 = data["content"] # 正文
    data2 = etree.HTML(data2)
    data3 = data2.xpath('//*[@class="tt-title"]/text()')[0] # 标题
    self.plainTextEdit.appendPlainText(data3 + "\n")
    data4 = data2.xpath('/html/body/article/p')
    for i in data4:
        data4 = i.xpath('string(.)').strip()
        self.plainTextEdit.appendPlainText("      " + data4 + "\n")
    self.plainTextEdit.ensureCursorVisible()
    cursor = self.plainTextEdit.textCursor()
    cursor.setPosition(0)
    self.plainTextEdit.setTextCursor(cursor)

@Slot()
def AddButton_2(self):
    info = self.textEdit.toPlainText()
    allpoint = get_in_book(info)
    allpoint = json.dumps(allpoint, ensure_ascii=False, indent=2)
    self.plainTextEdit.appendPlainText(allpoint)
    self.plainTextEdit.ensureCursorVisible()
    cursor = self.plainTextEdit.textCursor()
    cursor.setPosition(0)
    self.plainTextEdit.setTextCursor(cursor)

if __name__ == "__main__":
    # create the application and the main window
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()

    # setup stylesheet
    # apply_stylesheet(app, theme='dark_teal.xml')

    ui_file = QFile("untitled1.ui")
    ui_file.open(QFile.ReadOnly)

    loader = QUiLoader()
    window = loader.load(ui_file)
    ui_file.close()
    if not window:
        print(loader.load(ui_file))
        sys.exit(-1)

    # 在这里加入信号触发、空间控制等代码
    window.pushButton_2.clicked.connect(lambda:AddButton_2(window))
    window.pushButton.clicked.connect(lambda:AddButton(window))
    window.textEdit.setPlaceholderText("请输入book_id或者输入书名点击获取book_id")
    window.plainTextEdit.setPlaceholderText("软件使用说明\n为了防止bug，请始终保持book_id框不为空\n本软件一切数据来源api，作者只是提供数据整理的工具")
    window.listView.clicked.connect(lambda:Click(window))
    # 添加结束
    # run
    window.show()
    sys.exit(app.exec_())
