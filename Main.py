import sys
import os
from PyQt5 import QtWidgets, QtGui, QtCore
from VideoSource import bilibili


class VideoDownloader(object):

    def __init__(self):
        self.engine_list = ['b站', '...']
        self.sess = None

    def setup_ui(self):
        self.main_window = QtWidgets.QMainWindow()
        self.main_window.setObjectName("main_window")
        self.main_window.resize(1200, 800)
        # self.main_window.setWindowIcon()
        self.main_window.setWindowTitle("Video Downloader - Designed by Jackie")
        self.central_widget = QtWidgets.QWidget(self.main_window)
        self.central_widget.setObjectName("central_widget")

        # 设置侧边栏
        self.left_widget = QtWidgets.QWidget(self.central_widget)
        self.left_widget.setGeometry(QtCore.QRect(0, 0, 250, 800))
        self.left_widget.setObjectName("left_widget")
        self.v_box_1 = QtWidgets.QVBoxLayout(self.left_widget)
        self.btn1 = QtWidgets.QPushButton("搜索", self.left_widget)
        self.btn2 = QtWidgets.QPushButton("设置", self.left_widget)
        self.logo = QtWidgets.QLabel(self.left_widget)
        self.logo.setObjectName("logo")
        self.spacer1 = QtWidgets.QSpacerItem(250, 100, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        self.spacer2 = QtWidgets.QSpacerItem(250, 500, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        self.v_box_1.addWidget(self.logo)
        self.v_box_1.addItem(self.spacer1)
        self.v_box_1.addWidget(self.btn1)
        self.v_box_1.addWidget(self.btn2)
        self.v_box_1.addItem(self.spacer2)

        # 设置右侧区域
        self.right_widget = QtWidgets.QStackedWidget(self.central_widget)
        self.right_widget.setObjectName("right_widget")
        self.right_widget.setGeometry(QtCore.QRect(250, 0, 1200, 800))

        # 下载页设置
        self.download_page = QtWidgets.QWidget()
        self.download_page.setObjectName("download_page")
        self.download_page.setGeometry(QtCore.QRect(250, 0, 1200, 800))
        self.search_area = QtWidgets.QWidget(self.download_page)
        self.search_area.setGeometry(QtCore.QRect(0, 0, 950, 60))
        self.search_area.setObjectName("search_area")
        self.h_box_1 = QtWidgets.QHBoxLayout(self.search_area)

        # 搜索框设置
        self.search_box = QtWidgets.QLineEdit(self.search_area)
        sp = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sp.setHorizontalStretch(6)
        self.search_box.setSizePolicy(sp)
        self.search_box.setFixedHeight(40)
        self.search_box.setObjectName("search_box")
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.search_box.setTextMargins(5, 0, 0, 0)
        self.search_box.setFont(font)
        self.search_box.placeholderText()
        self.search_box.setPlaceholderText("输入视频地址")
        self.search_box.setCursor(QtCore.Qt.IBeamCursor)

        # 按钮设置
        self.search_btn = QtWidgets.QPushButton("添加", self.search_area)
        sp = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sp.setHorizontalStretch(1)
        self.search_btn.setSizePolicy(sp)
        self.search_btn.setFixedHeight(40)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.search_btn.setFont(font)
        self.search_btn.setObjectName("search_btn")
        self.search_btn.setCursor(QtCore.Qt.PointingHandCursor)
        self.search_btn.clicked.connect(lambda: self.search(self.search_box.text()))  # 按钮触发信号

        # 引擎切换设置
        self.engine = QtWidgets.QComboBox(self.search_area)
        self.engine.setSizePolicy(sp)
        self.engine.setFixedHeight(40)
        self.engine.setObjectName("engine")
        self.engine.setFrame(True)
        combobox_text = QtWidgets.QLineEdit()  # 设置combobox字体
        combobox_text.setReadOnly(True)
        combobox_text.setAlignment(QtCore.Qt.AlignCenter)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.engine.setPalette(palette)
        self.engine.setLineEdit(combobox_text)
        combobox_drop_down = QtWidgets.QListWidget()  # 设置combobox下拉菜单字体
        for i in self.engine_list:
            item = QtWidgets.QListWidgetItem(i)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            combobox_drop_down.addItem(item)
        self.engine.setModel(combobox_drop_down.model())
        self.engine.setView(combobox_drop_down)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setBold(True)
        font.setPointSize(10)
        self.engine.setFont(font)
        self.engine.setCursor(QtCore.Qt.PointingHandCursor)
        self.engine.currentIndexChanged.connect(self.engine_switch)  # 搜索引擎切换
        
        self.h_box_1.setContentsMargins(10, 10, 10, 10)
        self.h_box_1.setSpacing(0)
        self.h_box_1.addWidget(self.engine)
        self.h_box_1.addWidget(self.search_box)
        self.h_box_1.addWidget(self.search_btn)

        # 基本信息设置
        self.info_box = QtWidgets.QTabWidget(self.download_page)
        self.info_box.setObjectName("info_box")
        self.info_box.setGeometry(QtCore.QRect(0, 90, 950, 760))

        # 队列
        self.sequence = QtWidgets.QWidget()
        self.table = QtWidgets.QTableWidget(self.sequence)
        self.table.setGeometry(QtCore.QRect(0, 0, 950, 700))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.table.setFont(font)
        self.table.setColumnCount(6)
        # self.table.setRowCount(20)
        self.table.setHorizontalHeaderLabels(['', '视频名', '时长', '大小', '画质', ''])
        self.table.setMouseTracking(True)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.table.setShowGrid(False)
        self.table.setGridStyle(QtCore.Qt.NoPen)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().resizeSection(0, 220)
        self.table.horizontalHeader().resizeSection(1, 300)
        self.table.horizontalHeader().resizeSection(2, 100)
        self.table.horizontalHeader().resizeSection(3, 100)
        self.table.horizontalHeader().resizeSection(4, 100)
        self.table.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.table.setObjectName("table")

        # 正在下载
        self.downloading = QtWidgets.QWidget()

        # 已完成
        self.finished = QtWidgets.QWidget()

        self.info_box.addTab(self.sequence, "队列")
        self.info_box.addTab(self.downloading, "正在下载")
        self.info_box.addTab(self.finished, "已完成")

        # 设置设置页
        self.option_page = QtWidgets.QWidget()
        self.option_page.setObjectName("option_page")
        self.option_page.setGeometry(QtCore.QRect(250, 0, 1200, 800))

        self.right_widget.addWidget(self.download_page)
        self.right_widget.addWidget(self.option_page)
        self.right_widget.setCurrentIndex(0)

        self.main_window.setCentralWidget(self.central_widget)
        self.main_window.show()

    def engine_switch(self):
        print(f'当前搜索引擎：{self.engine.currentIndex()}')
        if self.engine.currentIndex() == 0:
            self.sess = bilibili.bilibiliVideo()
        elif self.engine.currentIndex() == 1:
            pass
        elif self.engine.currentIndex() == 2:
            pass
        elif self.engine.currentIndex() == 3:
            pass
        elif self.engine.currentIndex() == 4:
            pass
        elif self.engine.currentIndex() == 5:
            pass

    def search(self, url):
        filename, duration, video, audio = self.sess.get_info(url)
        self.table.insertRow(self.table.rowCount())
        self.table.setRowHeight(self.table.rowCount()-1, 124)
        front = QtWidgets.QLabel()
        front.resize(220, 124)
        pic = QtGui.QPixmap("./temp/pic.jpg")
        pic.scaled(220, 124, QtCore.Qt.KeepAspectRatio)
        front.setPixmap(pic)
        front.setAlignment(QtCore.Qt.AlignCenter)
        front.setScaledContents(True)
        self.table.setCellWidget(0, 0, front)
        item = QtWidgets.QTableWidgetItem(filename)
        self.table.setItem(self.table.rowCount()-1, 1, item)
        item = QtWidgets.QTableWidgetItem(duration)
        self.table.setItem(self.table.rowCount()-1, 2, item)
        choose_vq = QtWidgets.QComboBox()
        sp = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        choose_vq.setSizePolicy(sp)
        choose_vq.setFixedHeight(36)
        temp = []
        for i in video:
            if i[0] == 112:
                temp.append("1080p+")
            elif i[0] == 80:
                temp.append("1080p")
            elif i[0] == 64:
                temp.append("720p")
            elif i[0] == 32:
                temp.append("480p")
            elif i[0] == 16:
                temp.append("360p")
        choose_vq.setFrame(True)
        text = QtWidgets.QLineEdit()  # 设置combobox字体
        text.setReadOnly(True)
        text.setAlignment(QtCore.Qt.AlignCenter)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        choose_vq.setPalette(palette)
        choose_vq.setLineEdit(text)
        combobox_drop_down = QtWidgets.QListWidget()  # 设置combobox下拉菜单字体
        for i in temp:
            item = QtWidgets.QListWidgetItem(i)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            combobox_drop_down.addItem(item)
        choose_vq.setModel(combobox_drop_down.model())
        choose_vq.setView(combobox_drop_down)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setBold(True)
        font.setPointSize(10)
        choose_vq.setFont(font)
        choose_vq.setCursor(QtCore.Qt.PointingHandCursor)
        # choose_vq.currentIndexChanged.connect()  # 搜索引擎切换
        self.table.setCellWidget(self.table.rowCount()-1, 4, choose_vq)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    run = VideoDownloader()
    run.setup_ui()
    run.engine_switch()
    run.search("https://www.bilibili.com/video/BV1zV411k7pr")
    with open('StyleSheet.qss', 'r') as f:
        style = f.read()
    app.setStyleSheet(style)
    sys.exit(app.exec_())
