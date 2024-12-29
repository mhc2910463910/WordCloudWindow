# 词云图
from posixpath import split
from pydoc import browse
from tkinter.ttk import Button

import pyecharts.options as opts
from PyQt5.QtGui import QFont
from pyecharts.charts import WordCloud
from pyecharts.globals import SymbolType
from pyecharts.render import make_snapshot
# from snapshot_selenium import snapshot
from snapshot_phantomjs import snapshot
# data = [
#     ("无人机", "800"),
#     ("索尼", "700"),
#     ("程序猿", "900"),
#     ("Java", "850"),
#     ("Python", "840"),
#     ("HTML", "680"),
#     ("CSS", "680"),
#     ("JavaScript", "680"),
#     ("C", "600"),
#     ("C++", "650"),
#     ("Linux", "850"),
#     ("NAS", "830"),
#     ("OpenWrt", "830"),
#     ("JavaFx", "830"),
#     ("SpringBoot", "830"),
#     ("Swing", "820"),
#     ("Git", "800"),
#     ("FPV", "800"),
#     ("单片机", "650"),
#     ("浪潮之巅", "700"),
#     ("吃喝玩乐", "999"),
#     ("deepin", "800"),
#     ("穿越机", "800"),
#     ("社交恐惧", "750")
# ]
# wc = (
#     WordCloud()
#     .add("", data, word_size_range=[10, 70], shape=SymbolType.DIAMOND)
#     .render("lzmhc.html")
# )
# make_snapshot(snapshot, wc.render(), "lzmhc.png")


# GUI
import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QDesktopWidget,
                             QApplication, QWidget, QHBoxLayout, QFrame,
                             QSplitter, QStyleFactory, QTextEdit, QPushButton,
                             QVBoxLayout, QLineEdit, QLabel)
from PyQt5.QtCore import Qt


class EchartsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.resize(720, 420)
        vbox=QVBoxLayout(self)
        hbox=QHBoxLayout()
        self.textEdit = QTextEdit(self)
        self.textEdit.setEnabled(True)
        self.textEdit.setFontFamily("仿宋")
        self.textEdit.setFontPointSize(12)
        exampleBtn = QPushButton("示例", self)
        clearBtn = QPushButton("清空", self)
        startBtn = QPushButton("生成网页", self)
        browseBtn = QPushButton("查看网页", self)
        toImgBtn = QPushButton("转换图片", self)
        imgBtn = QPushButton("查看图片", self)
        self.statusInfo = QLabel("操作", self)
        vbox.addWidget(self.textEdit)
        hbox.addWidget(exampleBtn)
        hbox.addWidget(startBtn)
        hbox.addWidget(clearBtn)
        hbox.addWidget(browseBtn)
        hbox.addWidget(toImgBtn)
        hbox.addWidget(imgBtn)
        vbox.addLayout(hbox)
        vbox.addWidget(self.statusInfo)
        # 事件处理
        clearBtn.clicked.connect(self.clearClicked)
        exampleBtn.clicked.connect(self.loadExample)
        self.setLayout(vbox)
        self.center()
        self.setWindowTitle('词云图生成器')
        self.show()
    def clearClicked(self):
        sender = self.sender()
        self.textEdit.clear()
        self.statusInfo.setText(sender.text())
    def loadExample(self):
        data=[
                ("Java", "850"),
                ("Python", "840"),
                ("HTML", "680"),
                ("CSS", "680"),
                ("JavaScript", "680"),
                ("C", "600"),
                ("C++", "650"),
                ("Linux", "850"),
                ("OpenWrt", "830")
        ]
        str = ""
        for d in data:
            print(d[0]+" "+d[1])
            str+=d[0]+" "+d[1]+",\n"
        self.textEdit.setText(str)
        self.statusInfo.setText(self.sender().text())
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EchartsWindow()
    sys.exit(app.exec_())