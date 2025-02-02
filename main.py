# 词云图
import time
from posix import write

from IPython.core.release import author
from encodings.utf_7 import encode
from posixpath import split
from pydoc import browse
from tkinter.ttk import Button
import pyecharts.options as opts
from PyQt5.QtGui import QFont, QImage
from numpy.f2py.crackfortran import currentfilename
from pyecharts.charts import WordCloud
from pyecharts.globals import SymbolType
from pyecharts.render import make_snapshot
# from snapshot_selenium import snapshot
from snapshot_phantomjs import snapshot
# GUI
import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QDesktopWidget,
                             QApplication, QWidget, QHBoxLayout,
                             QStyleFactory, QTextEdit, QPushButton,
                             QVBoxLayout, QLabel, QComboBox, QAction,
                             QMenu, QDialog, QFileDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import json
import ast
example_json='''{
    "date": [
        ["花鸟市场", 1446],
        ["汽车", 928],
        ["视频", 906],
        ["电视", 825]
    ]
}'''
class EchartsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.rootFile = "/home/Deepin-MHC/Documents/Python/Echarts"
        self.currentFile = ""
        self.imgUrl = ""
        self.widget = QWidget(self)
        self.resize(720, 420)
        # 布局
        vbox=QVBoxLayout()
        hbox=QHBoxLayout()
        # 菜单
        menubar = self.menuBar()
        fileMenu = menubar.addMenu("文件")
        createAct = QAction("新建", self)
        createAct.setShortcut('Ctrl+N')
        createAct.triggered.connect(self.createFile)
        openAct = QAction("打开", self)
        openAct.setShortcut('Ctrl+O')
        openAct.triggered.connect(self.openFile)
        saveAct = QAction("保存", self)
        saveAct.setShortcut("Ctrl+S")
        saveAct.triggered.connect(self.saveFile)
        exitAct = QAction("退出", self)
        exitAct.setShortcut("Ctrl+Q")
        exitAct.triggered.connect(self.exitWindow)
        fileMenu.addAction(createAct)
        fileMenu.addAction(openAct)
        fileMenu.addAction(saveAct)
        fileMenu.addAction(exitAct)

        setMenu = menubar.addMenu("设置")
        themeMenu = QMenu("主题", self)
        lightTheme = QAction("浅色", self)
        darkTheme = QAction("深色", self)
        themeMenu.addAction(lightTheme)
        themeMenu.addAction(darkTheme)
        minFontMenu = QMenu("最小字体", self)
        maxFontMenu = QMenu("最大字体", self)
        font_10 = QAction("10", self)
        font_15 = QAction("15", self)
        font_20 = QAction("20", self)
        font_25 = QAction("25", self)
        font_30 = QAction("30", self)
        font_35 = QAction("35", self)
        minFontMenu.addAction(font_10)
        minFontMenu.addAction(font_15)
        minFontMenu.addAction(font_20)
        minFontMenu.addAction(font_25)
        minFontMenu.addAction(font_30)
        minFontMenu.addAction(font_35)
        font_100 = QAction("100", self)
        font_110 = QAction("110", self)
        font_120 = QAction("120", self)
        font_130 = QAction("130", self)
        font_140 = QAction("140", self)
        font_150 = QAction("150", self)
        maxFontMenu.addAction(font_100)
        maxFontMenu.addAction(font_110)
        maxFontMenu.addAction(font_120)
        maxFontMenu.addAction(font_130)
        maxFontMenu.addAction(font_140)
        maxFontMenu.addAction(font_150)
        setMenu.addMenu(themeMenu)
        setMenu.addMenu(minFontMenu)
        setMenu.addMenu(maxFontMenu)

        aboutMenu = menubar.addMenu("帮助")
        aboutAct = QAction("关于", self)
        aboutAct.triggered.connect(self.showAbout)
        aboutMenu.addAction(aboutAct)

        self.minFontSize = 5
        self.maxFontSize = 80
        # 组件
        self.textEdit = QTextEdit(self)
        self.textEdit.setEnabled(True)
        self.textEdit.setFontFamily("仿宋")
        self.textEdit.setFontPointSize(12)
        self.wordCloudType = QComboBox(self)
        self.wordtype = "BASIC词云图"
        self.wordCloudType.addItem("BASIC词云图")
        self.wordCloudType.addItem("DIAMOND词云图")
        self.wordCloudType.addItem("自定义图片词云图")
        self.wordCloudType.activated[str].connect(self.onActivated)
        exampleBtn = QPushButton("查看示例")
        clearBtn = QPushButton("清空内容")
        startBtn = QPushButton("生成网页")
        toImgBtn = QPushButton("生成图片")
        self.statusInfo = QLabel("操作")
        vbox.addWidget(self.textEdit)
        vbox.addWidget(self.wordCloudType)
        hbox.addWidget(exampleBtn)
        hbox.addWidget(startBtn)
        hbox.addWidget(toImgBtn)
        hbox.addWidget(clearBtn)
        vbox.addLayout(hbox)
        vbox.addWidget(self.statusInfo)
        # 事件处理
        clearBtn.clicked.connect(self.clearClicked)
        exampleBtn.clicked.connect(self.loadExample)
        startBtn.clicked.connect(self.toHtml)
        toImgBtn.clicked.connect(self.toImg)
        self.widget.setLayout(vbox)
        self.setCentralWidget(self.widget)
        self.center()
        self.setWindowTitle('词云图生成器')
        self.show()
    def createFile(self):
        fname = QFileDialog.getSaveFileName(self, "创建文件", self.rootFile, "Json Files(*.json)")
        if fname[0]:
            with open(fname[0], 'w') as f:
                f.write(example_json)
            self.currentFile = fname[0]
            self.textEdit.setText(example_json)
            self.statusInfo.setText("新建文件" + fname[0])
    def openFile(self):
        fname = QFileDialog.getOpenFileName(self, '打开文件', self.rootFile, "Json Files (*.json)")
        if fname[0]:
            f = open(fname[0], 'r')
            with f:
                data = f.read()
                self.textEdit.setText(data)
            self.currentFile = fname[0]
            self.statusInfo.setText("打开文件" + fname[0])
    def saveFile(self):
        date = self.textEdit.toPlainText()
        if self.currentFile == "":
            fname = QFileDialog.getSaveFileName(self, "创建文件", self.rootFile,
                                                "Json Files(*.json)")
            if fname[0]:
                with open(fname[0], 'w') as f:
                    f.write(date)
                self.currentFile = fname[0]
                self.statusInfo.setText("新建文件" + self.currentFile)
        else:
            with open(self.currentFile, "w") as f:
                f.write(date)
            self.statusInfo.setText("保存文件"+self.currentFile)
    def exitWindow(self):
        QApplication.instance().quit()
    def clearClicked(self):
        sender = self.sender()
        self.textEdit.clear()
        self.statusInfo.setText(sender.text())
    def loadExample(self):
        exampleDialog = QDialog(self)
        layout = QHBoxLayout()
        exampleText = QTextEdit()
        exampleText.setText(example_json)
        layout.addWidget(exampleText)
        exampleDialog.setLayout(layout)
        exampleDialog.exec()
        self.statusInfo.setText(self.sender().text()+"example/example.json")
    def onActivated(self, text):
        self.wordtype = text
        if self.wordtype == "自定义图片词云图":
            fname = QFileDialog.getOpenFileName(self, '选择图片', self.rootFile,
                                                "Images(*.jpg *.png)")
            if fname[0]:
                self.imgUrl = fname[0]
                self.statusInfo.setText("选择图片" + fname[0])
    def toHtml(self):
        strText = self.textEdit.toPlainText()
        if strText != "":
            if self.wordtype == "BASIC词云图":
                self.toBasicHtml(strText)
            elif self.wordtype == "DIAMOND词云图":
                self.toDiamondHtml(strText)
            elif self.wordtype == "自定义图片词云图":
                self.toCustom_mask_image(strText)
        else:
            self.statusInfo.setText("内容为空")
    def encodeTuple(self, str):
        print(json.loads(str)['date'])
        return json.loads(str)['date']
        # return [tuple(ast.literal_eval(s)) for s in str.split("\n")]
    def toBasicHtml(self, strText):
        date = self.encodeTuple(strText)
        (
            WordCloud()
            .add(series_name="", data_pair=date, word_size_range=[self.minFontSize, self.maxFontSize])
            .render("wordcloud_basic.html")
        )
        self.statusInfo.setText("已生成网页wordcloud_basic.html")
    def toDiamondHtml(self, strText):
        date = self.encodeTuple(strText)
        (
            WordCloud()
            .add("", date, word_size_range=[self.minFontSize, self.maxFontSize], shape=SymbolType.DIAMOND)
            .render("wordcloud_diamond.html")
        )
        self.statusInfo.setText("已生成网页wordcloud_diamond.html")
    def toCustom_mask_image(self, strText):
        date = self.encodeTuple(strText)
        if self.imgUrl != "":
            (
                WordCloud()
                .add("", date, word_size_range=[self.minFontSize, self.maxFontSize], mask_image=self.imgUrl)
                .render("wordcloud_custom_mask_image.html")
            )
            self.statusInfo.setText("已生成网页wordcloud_custom_mask_image.html")
        else:
            self.statusInfo.setText("选择的图片为空")
    def toImg(self):
        self.statusInfo.setText("正在生成图片")
        str = self.textEdit.toPlainText()
        if str != "":
            date = []
            for s in str.split(";"):
                if s != "":
                    name = s.split(",")[0].strip().replace("\n", "")
                    value = s.split(",")[1].strip().replace("\n", "")
                    date.append((name, value))
            wc = (
                WordCloud()
                .add("", date, word_size_range=[10, 70], shape=self.wordtype)
            )
            make_snapshot(snapshot, wc.render(), "wordcloud.png")
            self.statusInfo.setText("已生成图片wordcloud.png")
        else:
            self.statusInfo.setText("内容为空")
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    def showAbout(self):
        aboutDialog = QDialog(self)
        aboutDialog.setWindowTitle("关于")
        title = QLabel("词云图生成器")
        info = QLabel("简介:一键生成不同类型的词云图，支持自定义图片词云图。")
        project = QLabel("项目地址:https://github.com/mhc2910463910/WordCloudWindow")
        author = QLabel("联系作者:2910463910@qq.com")
        font = title.font()
        font.setPointSize(25)
        title.setFont(font)
        title.setAlignment(Qt.AlignHCenter)
        info.setAlignment(Qt.AlignHCenter)
        project.setAlignment(Qt.AlignHCenter)
        author.setAlignment(Qt.AlignHCenter)
        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(info)
        layout.addWidget(project)
        layout.addWidget(author)
        aboutDialog.setLayout(layout)
        aboutDialog.exec()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EchartsWindow()
    sys.exit(app.exec_())