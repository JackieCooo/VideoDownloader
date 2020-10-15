import sys
import os
from PyQt5 import QtWidgets, QtGui, QtCore
from VideoSource import bilibili, tencent
from PIL import Image
import ctypes
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")


class VideoDownloader(QtWidgets.QMainWindow):

    def __init__(self):
        super(VideoDownloader, self).__init__()
        self.engine_list = ['b站', '腾讯视频']
        self.sess = None
        self.video = []
        self.audio = []
        self.num = 0  # 记录表格行数，便于动态调整
        self.video_info = []
        self.m_flag = False
        if not os.path.exists("downloads"):
            os.mkdir("downloads")
        self.filepath = os.path.abspath(__file__)[:-7] + "downloads"

    def setup_ui(self):
        self.setObjectName("main_window")
        self.resize(1200, 800)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowIcon(QtGui.QIcon("./icons/window_icon.png"))
        self.central_widget = QtWidgets.QWidget(self)
        self.central_widget.setObjectName("central_widget")

        # 设置侧边栏
        self.left_widget = QtWidgets.QWidget(self.central_widget)
        self.left_widget.setGeometry(0, 60, 250, 740)
        self.left_widget.setObjectName("left_widget")
        self.btn1 = CustomBtn(self.left_widget)
        self.btn1.setText("搜索")
        self.btn1.setGeometry(10, 20, 230, 50)
        self.btn1.setChecked(True)
        self.btn1.clicked.connect(lambda: self.right_widget.setCurrentIndex(0))
        self.btn2 = CustomBtn(self.left_widget)
        self.btn2.setText("设置")
        self.btn2.setGeometry(10, 80, 230, 50)
        self.btn2.clicked.connect(lambda: self.right_widget.setCurrentIndex(1))
        self.about = QtWidgets.QLabel(self.left_widget)
        self.about.setGeometry(0, 640, 250, 100)
        self.about.setFont(QtGui.QFont("微软雅黑", 9))
        self.about.setAlignment(QtCore.Qt.AlignCenter)
        self.about.setText("ver 1.0\nDesigned by Jackie")
        self.about.setObjectName("about")

        # 设置上边栏
        self.top_bar = QtWidgets.QWidget(self.central_widget)
        self.top_bar.setGeometry(0, 0, 1200, 60)
        self.top_bar.setObjectName("top_bar")

        # logo设置
        self.logo = QtWidgets.QLabel(self.top_bar)
        self.logo.setGeometry(0, 0, 250, 60)
        self.logo.setPixmap(QtGui.QPixmap("./icons/logo.png"))

        # 窗口控制按钮设置
        self.close_btn = QtWidgets.QPushButton(self.top_bar)
        self.close_btn.setFixedSize(30, 30)
        self.close_btn.setGeometry(1155, 15, 1200, 45)
        self.close_btn.setObjectName("close_btn")
        self.close_btn.setCursor(QtCore.Qt.PointingHandCursor)
        self.close_btn.clicked.connect(self.close)
        self.minimize_btn = QtWidgets.QPushButton(self.top_bar)
        self.minimize_btn.setGeometry(1110, 15, 1140, 45)
        self.minimize_btn.setFixedSize(30, 30)
        self.minimize_btn.setObjectName("minimize_btn")
        self.minimize_btn.setCursor(QtCore.Qt.PointingHandCursor)
        self.minimize_btn.clicked.connect(self.showMinimized)

        # 搜索区域设置
        self.search_area = QtWidgets.QWidget(self.top_bar)
        self.search_area.setGeometry(250, 0, 700, 60)
        self.search_area.setObjectName("search_area")
        self.h_box_1 = QtWidgets.QHBoxLayout(self.search_area)

        # 搜索框设置
        self.search_box = QtWidgets.QLineEdit(self.search_area)
        sp = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sp.setHorizontalStretch(6)
        self.search_box.setSizePolicy(sp)
        self.search_box.setFixedHeight(36)
        self.search_box.setObjectName("search_box")
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.search_box.setTextMargins(5, 0, 0, 0)
        self.search_box.setFont(font)
        self.search_box.placeholderText()
        self.search_box.setPlaceholderText("输入视频地址")
        self.search_box.setCursor(QtCore.Qt.IBeamCursor)
        self.search_box.setFrame(False)
        # print(self.search_box.sizeHint().width())

        # 按钮设置
        self.search_btn = QtWidgets.QPushButton(self.search_area)
        sp = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sp.setHorizontalStretch(1)
        self.search_btn.setSizePolicy(sp)
        self.search_btn.setFixedHeight(36)
        self.search_btn.setObjectName("search_btn")
        self.search_btn.setCursor(QtCore.Qt.PointingHandCursor)
        self.search_btn.clicked.connect(lambda: self.search(self.search_box.text()))  # 按钮触发信号
        # print(self.search_btn.geometry().width())

        # 引擎切换设置
        self.engine = QtWidgets.QComboBox(self.search_area)
        self.engine.setSizePolicy(sp)
        self.engine.setFixedHeight(36)
        self.engine.setObjectName("engine")
        self.engine.setFrame(True)
        combobox_text = QtWidgets.QLineEdit()  # 设置combobox字体
        combobox_text.setReadOnly(True)
        combobox_text.setAlignment(QtCore.Qt.AlignCenter)
        self.engine.setLineEdit(combobox_text)
        combobox_drop_down = QtWidgets.QListWidget()  # 设置combobox下拉菜单字体
        combobox_drop_down.setFrameShape(QtWidgets.QFrame.NoFrame)
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

        # 设置右侧区域
        self.right_widget = QtWidgets.QStackedWidget(self.central_widget)
        self.right_widget.setObjectName("right_widget")
        self.right_widget.setGeometry(250, 60, 1200, 800)

        # 下载页设置
        self.download_page = QtWidgets.QWidget()
        self.download_page.setObjectName("download_page")
        self.download_page.setGeometry(250, 60, 1200, 800)

        # 基本信息设置
        self.info_box = QtWidgets.QTabWidget(self.download_page)
        self.info_box.setObjectName("info_box")
        self.info_box.setGeometry(0, 0, 950, 740)

        # 队列
        self.sequence = QtWidgets.QWidget()
        self.table = QtWidgets.QTableWidget(self.sequence)
        self.table.setGeometry(0, 0, 950, 700)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.table.setFont(font)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['', '视频名', '时长', '大小', '画质', ''])
        self.table.setMouseTracking(True)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.table.setShowGrid(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().resizeSection(0, 220)
        self.table.horizontalHeader().resizeSection(1, 300)
        self.table.horizontalHeader().resizeSection(2, 100)
        self.table.horizontalHeader().resizeSection(3, 100)
        self.table.horizontalHeader().resizeSection(4, 100)
        self.table.horizontalHeader().setSectionsClickable(False)
        self.table.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.table.viewport().setFocusPolicy(QtCore.Qt.NoFocus)
        self.table.setObjectName("table")

        # 正在下载
        self.downloading = QtWidgets.QWidget()
        self.list = QtWidgets.QListWidget(self.downloading)
        self.list.setGeometry(0, 0, 950, 700)
        self.list.setMouseTracking(True)
        self.list.setFrameStyle(0)

        self.info_box.addTab(self.sequence, "队列")
        self.info_box.addTab(self.downloading, "正在下载")

        # 设置设置页
        sp = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.option_page = QtWidgets.QWidget()
        self.option_page.setObjectName("option_page")
        self.option_page.setGeometry(250, 0, 950, 740)
        self.scroll_area = QtWidgets.QScrollArea(self.option_page)
        self.scroll_area.setGeometry(0, 0, 950, 740)
        self.scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.w1 = QtWidgets.QWidget()
        self.w1.resize(950, 1600)
        self.w1.setObjectName("w1")
        self.v_box_1 = QtWidgets.QVBoxLayout(self.w1)
        self.label1 = CustomLabel(self.w1)
        self.label1.setText("基本设置")
        self.label4 = QtWidgets.QLabel(self.w1)
        self.label4.setFont(QtGui.QFont("微软雅黑", 9))
        self.label4.setText("主题颜色")
        self.label4.setContentsMargins(20, 0, 0, 0)
        self.label4.setSizePolicy(sp)
        self.label4.setFixedSize(500, 50)
        self.w2 = QtWidgets.QWidget(self.w1)
        self.w2.setFixedSize(950, 100)
        self.blue_btn = ColorChangingBtn(self.w2, QtGui.QColor(52, 152, 219))
        self.blue_btn.setText("胖次蓝")
        self.blue_btn.setGeometry(50, 0, 60, 80)
        self.blue_btn.setChecked(True)
        self.red_btn = ColorChangingBtn(self.w2, QtGui.QColor(214, 69, 65))
        self.red_btn.setText("姨妈红")
        self.red_btn.setGeometry(150, 0, 60, 80)
        self.pink_btn = ColorChangingBtn(self.w2, QtGui.QColor(241, 130, 141))
        self.pink_btn.setText("少女粉")
        self.pink_btn.setGeometry(250, 0, 60, 80)
        self.yellow_btn = ColorChangingBtn(self.w2, QtGui.QColor(233, 212, 96))
        self.yellow_btn.setText("咸蛋黄")
        self.yellow_btn.setGeometry(350, 0, 60, 80)
        self.green_btn = ColorChangingBtn(self.w2, QtGui.QColor(77, 175, 124))
        self.green_btn.setText("草苗绿")
        self.green_btn.setGeometry(450, 0, 60, 80)
        self.purple_btn = ColorChangingBtn(self.w2, QtGui.QColor(155, 89, 182))
        self.purple_btn.setText("基佬紫")
        self.purple_btn.setGeometry(550, 0, 60, 80)
        self.label5 = QtWidgets.QLabel(self.w1)
        self.label5.setFont(QtGui.QFont("微软雅黑", 9))
        self.label5.setText("语言")
        self.label5.setContentsMargins(20, 0, 0, 0)
        self.label5.setSizePolicy(sp)
        self.label5.setFixedSize(500, 50)
        self.w3 = QtWidgets.QWidget(self.w1)
        self.w3.setFixedSize(400, 50)
        self.w3.setContentsMargins(50, 0, 0, 0)
        self.h_box_2 = QtWidgets.QHBoxLayout(self.w3)
        self.chs_btn = QtWidgets.QCheckBox(self.w3)
        self.chs_btn.setFont(QtGui.QFont("微软雅黑", 9))
        self.chs_btn.setText("简体中文")
        self.chs_btn.setChecked(True)
        self.chs_btn.setCursor(QtCore.Qt.PointingHandCursor)
        self.eng_btn = QtWidgets.QCheckBox(self.w3)
        self.eng_btn.setFont(QtGui.QFont("微软雅黑", 9))
        self.eng_btn.setText("English")
        self.eng_btn.setCursor(QtCore.Qt.PointingHandCursor)
        self.h_box_2.addWidget(self.chs_btn)
        self.h_box_2.addWidget(self.eng_btn)

        self.label2 = CustomLabel(self.w1)
        self.label2.setText("下载设置")
        self.label11 = QtWidgets.QLabel(self.w1)
        self.label11.setFont(QtGui.QFont("微软雅黑", 9))
        self.label11.setText("下载地址")
        self.label11.setFixedSize(500, 50)
        self.label11.setContentsMargins(20, 0, 0, 0)
        self.w7 = QtWidgets.QWidget(self.w1)
        self.w7.setFixedSize(750, 50)
        self.w7.setContentsMargins(50, 0, 0, 0)
        self.h_box_4 = QtWidgets.QHBoxLayout(self.w7)
        self.path_box = QtWidgets.QLineEdit(self.w7)
        self.path_box.setFixedSize(550, 36)
        self.path_box.setReadOnly(True)
        self.path_box.setFont(QtGui.QFont("微软雅黑", 10))
        self.path_box.setText(self.filepath)
        self.path_box.setObjectName("path_box")
        self.path_box.setContentsMargins(5, 0, 0, 0)
        self.change_btn = QtWidgets.QPushButton("更改", self.w7)
        self.change_btn.setFixedSize(80, 36)
        self.change_btn.clicked.connect(self.path_change)
        self.change_btn.setObjectName("change_btn")
        self.change_btn.setCursor(QtCore.Qt.PointingHandCursor)
        self.h_box_4.addWidget(self.path_box)
        self.h_box_4.addWidget(self.change_btn)
        self.label6 = QtWidgets.QLabel(self.w1)
        self.label6.setFont(QtGui.QFont("微软雅黑", 9))
        self.label6.setText("下载线程数(尚未加入)")
        self.label6.setContentsMargins(20, 0, 0, 0)
        self.label6.setSizePolicy(sp)
        self.label6.setFixedSize(500, 50)

        self.w6 = QtWidgets.QWidget(self.w1)
        self.w6.setFixedSize(950, 36)
        self.thead_choice = QtWidgets.QComboBox(self.w6)
        self.thead_choice.setFixedSize(100, 36)
        self.thead_choice.move(50, 0)
        self.thead_choice.setFrame(True)
        combobox_text = QtWidgets.QLineEdit()  # 设置combobox字体
        combobox_text.setReadOnly(True)
        combobox_text.setAlignment(QtCore.Qt.AlignCenter)
        self.thead_choice.setLineEdit(combobox_text)
        combobox_drop_down = QtWidgets.QListWidget()  # 设置combobox下拉菜单字体
        array = [i for i in range(1, 65)]
        for i in array:
            item = QtWidgets.QListWidgetItem(str(i))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            combobox_drop_down.addItem(item)
        self.thead_choice.setModel(combobox_drop_down.model())
        self.thead_choice.setView(combobox_drop_down)
        font = QtGui.QFont("微软雅黑", 10)
        self.thead_choice.setFont(font)
        self.thead_choice.setCursor(QtCore.Qt.PointingHandCursor)
        self.thead_choice.setObjectName("thread_choice")

        self.label10 = QtWidgets.QLabel(self.w1)
        self.label10.setFont(QtGui.QFont("微软雅黑", 9))
        self.label10.setText("下载音质")
        self.label10.setContentsMargins(20, 0, 0, 0)
        self.label10.setSizePolicy(sp)
        self.label10.setFixedSize(500, 50)

        self.w4 = QtWidgets.QWidget(self.w1)
        self.w4.setGeometry(0, 0, 950, 50)
        self.w4.setContentsMargins(50, 0, 0, 0)
        self.w4.setFixedSize(400, 50)
        self.h_box_3 = QtWidgets.QHBoxLayout(self.w4)
        self.h_aq = QtWidgets.QCheckBox(self.w4)
        self.h_aq.setFont(QtGui.QFont("微软雅黑", 9))
        self.h_aq.setText("高音质")
        self.h_aq.setChecked(True)
        self.h_aq.setCursor(QtCore.Qt.PointingHandCursor)
        self.s_aq = QtWidgets.QCheckBox(self.w4)
        self.s_aq.setFont(QtGui.QFont("微软雅黑", 9))
        self.s_aq.setText("标准音质")
        self.s_aq.setCursor(QtCore.Qt.PointingHandCursor)
        self.h_box_3.addWidget(self.h_aq)
        self.h_box_3.addWidget(self.s_aq)

        self.label3 = CustomLabel(self.w1)
        self.label3.setText("关于")
        self.label7 = QtWidgets.QLabel(self.w1)
        self.label7.setFont(QtGui.QFont("微软雅黑", 9))
        self.label7.setText("软件简介")
        self.label7.setContentsMargins(20, 0, 0, 0)
        self.label7.setSizePolicy(sp)
        self.label7.setFixedSize(500, 50)
        self.label9 = QtWidgets.QLabel(self.w1)
        self.label9.setFont(QtGui.QFont("微软雅黑", 9))
        self.label9.setText("软件版本: ver 1.0\n该软件为开源软件项目，并会持续更新\n开源地址:https://github.com/JackieCooo/VideoDownloader")
        self.label9.setContentsMargins(50, 0, 0, 0)
        self.label9.setSizePolicy(sp)
        self.label9.setFixedSize(600, 100)
        self.label8 = QtWidgets.QLabel(self.w1)
        self.label8.setFont(QtGui.QFont("微软雅黑", 9))
        self.label8.setText("赞助方式")
        self.label8.setContentsMargins(20, 0, 0, 0)
        self.label8.setSizePolicy(sp)
        self.label8.setFixedSize(500, 50)
        self.w5 = QtWidgets.QWidget(self.w1)
        self.w5.setFixedSize(950, 600)
        self.wechat_pay = QtWidgets.QLabel(self.w5)
        self.wechat_pay.setGeometry(500, 0, 400, 600)
        self.wechat_pay.setPixmap(QtGui.QPixmap("./icons/wechat_pay.png"))
        self.wechat_pay.setSizePolicy(sp)
        self.wechat_pay.setFixedSize(400, 600)
        self.Alipay = QtWidgets.QLabel(self.w5)
        self.Alipay.setGeometry(50, 0, 400, 600)
        self.Alipay.setPixmap(QtGui.QPixmap("./icons/Alipay.png"))
        self.Alipay.setSizePolicy(sp)
        self.Alipay.setFixedSize(400, 600)

        self.btn_group1 = QtWidgets.QButtonGroup()
        self.btn_group1.addButton(self.chs_btn)
        self.btn_group1.addButton(self.eng_btn)
        self.btn_group1.buttonToggled.connect(self.change_language)
        self.btn_group2 = QtWidgets.QButtonGroup()
        self.btn_group2.addButton(self.h_aq)
        self.btn_group2.addButton(self.s_aq)
        self.btn_group3 = QtWidgets.QButtonGroup()
        self.btn_group3.addButton(self.blue_btn)
        self.btn_group3.addButton(self.red_btn)
        self.btn_group3.addButton(self.yellow_btn)
        self.btn_group3.addButton(self.green_btn)
        self.btn_group3.addButton(self.pink_btn)
        self.btn_group3.addButton(self.purple_btn)
        self.btn_group3.buttonToggled.connect(self.style_change)

        self.v_box_1.addWidget(self.label1)
        self.v_box_1.addWidget(self.label4)
        self.v_box_1.addWidget(self.w2)
        self.v_box_1.addWidget(self.label11)
        self.v_box_1.addWidget(self.w7)
        self.v_box_1.addWidget(self.label5)
        self.v_box_1.addWidget(self.w3)
        self.v_box_1.addWidget(self.label2)
        self.v_box_1.addWidget(self.label6)
        self.v_box_1.addWidget(self.w6)
        self.v_box_1.addWidget(self.label10)
        self.v_box_1.addWidget(self.w4)
        self.v_box_1.addWidget(self.label3)
        self.v_box_1.addWidget(self.label7)
        self.v_box_1.addWidget(self.label9)
        self.v_box_1.addWidget(self.label8)
        self.v_box_1.addWidget(self.w5)
        self.v_box_1.setSpacing(0)
        self.v_box_1.setContentsMargins(10, 10, 10, 10)
        self.scroll_area.setWidget(self.w1)

        self.right_widget.addWidget(self.download_page)
        self.right_widget.addWidget(self.option_page)
        self.right_widget.setCurrentIndex(0)

        self.tran = QtCore.QTranslator(self)
        self.setCentralWidget(self.central_widget)
        self.show()

    def engine_switch(self):
        print(f'当前搜索引擎：{self.engine.currentIndex()}')
        if self.engine.currentIndex() == 0:
            self.sess = bilibili.bilibiliVideo()
        elif self.engine.currentIndex() == 1:
            self.sess = tencent.Tencent()
        elif self.engine.currentIndex() == 2:
            pass
        elif self.engine.currentIndex() == 3:
            pass
        elif self.engine.currentIndex() == 4:
            pass
        elif self.engine.currentIndex() == 5:
            pass

    def search(self, url):
        self.num += 1

        filename, duration, temp1, temp2 = self.sess.get_info(url)
        self.video.append(temp1)
        self.audio.append(temp2)

        # 计算时长
        minute = int(duration / 60000)
        second = int(duration / 1000 - minute * 60)
        if second < 10:
            time = f"{minute}:0{second}"
        else:
            time = f"{minute}:{second}"

        # 保存视频信息
        temp3 = [self.set_pic(), filename, time, self.set_quality_select(duration, self.num), self.set_op_btn(self.num, duration)]
        self.video_info.append(temp3)

        self.show_result()  # 展示视频信息

        self.size_count(self.choose_vq.currentIndex(), 0, duration, self.num)  # 刷新下载文件大小

    def size_count(self, vq, aq, duration, num):
        size = (duration / 1000) * (self.video[num-1][vq][2] + self.audio[num-1][aq][2]) / 8000000
        size = str(round(size, 2)) + 'M'
        item = QtWidgets.QTableWidgetItem(size)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.table.setItem(num-1, 3, item)

    @staticmethod
    def set_pic():
        # 设置缩略图
        front = QtWidgets.QLabel()
        front.resize(220, 124)
        pic = QtGui.QPixmap("./temp/pic.jpg")
        pic.scaled(220, 124, QtCore.Qt.KeepAspectRatio)
        front.setPixmap(pic)
        front.setAlignment(QtCore.Qt.AlignCenter)
        front.setScaledContents(True)
        return front

    def set_quality_select(self, duration, num):
        # 设置画质选择器
        box1 = QtWidgets.QWidget()
        v_box_1 = QtWidgets.QVBoxLayout(box1)
        v_box_1.setSpacing(0)
        v_box_1.setContentsMargins(0, 0, 0, 0)
        self.choose_vq = QtWidgets.QComboBox(box1)
        self.choose_vq.setObjectName("choose_vq")
        self.choose_vq.setFixedHeight(36)
        temp = []
        for i in self.video[num-1]:
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
        self.choose_vq.setFrame(True)
        text = QtWidgets.QLineEdit()  # 设置combobox字体
        text.setReadOnly(True)
        text.setAlignment(QtCore.Qt.AlignCenter)
        self.choose_vq.setLineEdit(text)
        combobox_drop_down = QtWidgets.QListWidget()  # 设置combobox下拉菜单字体
        combobox_drop_down.setFrameShape(QtWidgets.QListWidget.NoFrame)
        for i in temp:
            item = QtWidgets.QListWidgetItem(i)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            combobox_drop_down.addItem(item)
        self.choose_vq.setModel(combobox_drop_down.model())
        self.choose_vq.setView(combobox_drop_down)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setBold(True)
        font.setPointSize(10)
        self.choose_vq.setFont(font)
        self.choose_vq.setCursor(QtCore.Qt.PointingHandCursor)
        self.choose_vq.currentIndexChanged.connect(lambda: self.size_count(self.choose_vq.currentIndex(), 0, duration, num))  # 画质选择信号触发，实时修改大小显示
        v_box_1.addWidget(self.choose_vq)
        del temp
        return box1

    def set_op_btn(self, num, duration):
        # 设置开始下载按钮
        box2 = QtWidgets.QWidget()
        h_box_1 = QtWidgets.QHBoxLayout(box2)
        dl_btn = QtWidgets.QPushButton(box2)
        dl_btn.setObjectName("dl_btn")
        dl_btn.clicked.connect(lambda: self.download(num, self.choose_vq.currentIndex(), duration))  # 设置下载按钮触发
        delete_btn = QtWidgets.QPushButton(box2)
        delete_btn.setObjectName("delete_btn")
        delete_btn.clicked.connect(lambda: self.delete(num))  # 删除队列触发
        h_box_1.addWidget(dl_btn)
        h_box_1.addWidget(delete_btn)
        return box2

    def delete(self, num):
        pass

    def show_result(self):
        self.table.insertRow(self.table.rowCount())
        row = self.table.rowCount() - 1
        self.table.setRowHeight(row, 124)
        self.table.setCellWidget(row, 0, self.video_info[row][0])
        item = QtWidgets.QTableWidgetItem(self.video_info[row][1])
        self.table.setItem(row, 1, item)
        item = QtWidgets.QTableWidgetItem(self.video_info[row][2])
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.table.setItem(row, 2, item)
        self.table.setCellWidget(row, 4, self.video_info[row][3])
        self.table.setCellWidget(row, 5, self.video_info[row][4])

    def download(self, num, vq, duration):
        print("正在下载")
        item = QtWidgets.QListWidgetItem()
        item.setSizeHint(QtCore.QSize(950, 120))
        self.list.addItem(item)
        delegate = ListDelegate(self.video_info[num-1][1])
        self.list.setItemDelegateForRow(num-1, delegate)
        video_size = int((duration / 1000) * self.video[num-1][vq][2] / 8)
        video_res = self.sess.get_video(self.video[num-1][vq][1], video_size)
        self.download_filename = self.video_info[num-1][1]

        # 创建视频下载线程
        download_thread = DownloadThread(video_res, video_res.headers['Content-Length'], open(f"{self.filepath}/video.flv", 'wb'), 10240, 0)
        download_thread.download_proess_signal.connect(self.set_prosess)
        download_thread.start()

        if self.h_aq.isChecked():
            aq = 0
        else:
            aq = 1
        audio_size = int((duration / 1000) * self.audio[num-1][aq][2] / 8)
        audio_res = self.sess.get_audio(self.audio[num-1][aq][1], audio_size)

        # 创建音频下载线程
        download_thread = DownloadThread(audio_res, audio_res.headers['Content-Length'], open(f"{self.filepath}/audio.mp3", 'wb'), 10240, 1)
        download_thread.download_proess_signal.connect(self.set_prosess)
        download_thread.start()

        if download_thread.isFinished():  # 判断是否下载完成
            self.merge_file()  # 合并音视频
            self.set_prosess(100)  # 刷新进度

    def set_prosess(self, val):
        delegate = ListDelegate(self.download_filename, val)
        self.list.setItemDelegateForRow(0, delegate)

    def merge_file(self):
        video_path = "./temp/video.flv"
        audio_path = "./temp/audio.mp3"
        os.system("ffmpeg -i " + video_path + " -i " + audio_path + " -codec copy ./downloads/final.mp4")
        os.rename("./downloads/final.mp4", f"./downloads/{self.download_filename}.mp4")
        os.remove("./temp/video.flv")
        os.remove("./temp/audio.mp3")

    def path_change(self):
        self.filepath = QtWidgets.QFileDialog.getExistingDirectory(caption='选取文件夹', directory='./') + '/'
        # print(self.directory)
        self.path_box.setText(self.filepath)

    def style_change(self):
        if self.blue_btn.isChecked():
            with open('BlueStyle.qss', 'r') as f:
                style = f.read()
            app.setStyleSheet(style)
        elif self.red_btn.isChecked():
            with open('RedStyle.qss', 'r') as f:
                style = f.read()
            app.setStyleSheet(style)
        elif self.yellow_btn.isChecked():
            with open('YellowStyle.qss', 'r') as f:
                style = f.read()
            app.setStyleSheet(style)
        elif self.green_btn.isChecked():
            with open('GreenStyle.qss', 'r') as f:
                style = f.read()
            app.setStyleSheet(style)
        elif self.pink_btn.isChecked():
            with open('PinkStyle.qss', 'r') as f:
                style = f.read()
            app.setStyleSheet(style)
        elif self.purple_btn.isChecked():
            with open('PurpleStyle.qss', 'r') as f:
                style = f.read()
            app.setStyleSheet(style)

    def retranslateUi(self):
        self.btn1.setText(QtWidgets.QApplication.translate("VideoDownloader", "搜索"))
        self.btn2.setText(QtWidgets.QApplication.translate("VideoDownloader", "设置"))
        self.label1.setText(QtWidgets.QApplication.translate("VideoDownloader", "基本设置"))
        self.label2.setText(QtWidgets.QApplication.translate("VideoDownloader", "下载设置"))
        self.label3.setText(QtWidgets.QApplication.translate("VideoDownloader", "关于"))
        self.label4.setText(QtWidgets.QApplication.translate("VideoDownloader", "主题颜色"))
        self.label5.setText(QtWidgets.QApplication.translate("VideoDownloader", "语言"))
        self.label6.setText(QtWidgets.QApplication.translate("VideoDownloader", "下载线程数"))
        self.label7.setText(QtWidgets.QApplication.translate("VideoDownloader", "软件简介"))
        self.label8.setText(QtWidgets.QApplication.translate("VideoDownloader", "赞助方式"))
        self.label9.setText(QtWidgets.QApplication.translate("VideoDownloader", "软件版本: ver 1.0\n该软件为开源软件项目，并会持续更新\n开源地址:https://github.com/JackieCooo/VideoDownloader"))
        self.label10.setText(QtWidgets.QApplication.translate("VideoDownloader", "下载音质"))
        self.label11.setText(QtWidgets.QApplication.translate("VideoDownloader", "下载地址"))
        self.info_box.setTabText(0, QtWidgets.QApplication.translate("VideoDownloader", "队列"))
        self.info_box.setTabText(1, QtWidgets.QApplication.translate("VideoDownloader", "正在下载"))
        self.table.setHorizontalHeaderLabels(["", QtWidgets.QApplication.translate("VideoDownloader", "视频名"), QtWidgets.QApplication.translate("VideoDownloader", "时长"), QtWidgets.QApplication.translate("VideoDownloader", "大小"), QtWidgets.QApplication.translate("VideoDownloader", "画质"), ""])
        self.search_box.setPlaceholderText(QtWidgets.QApplication.translate("VideoDownloader", "输入视频地址"))
        self.engine.setItemText(0, QtWidgets.QApplication.translate("VideoDownloader", "b站"))
        self.blue_btn.setText(QtWidgets.QApplication.translate("VideoDownloader", "胖次蓝"))
        self.red_btn.setText(QtWidgets.QApplication.translate("VideoDownloader", "姨妈红"))
        self.yellow_btn.setText(QtWidgets.QApplication.translate("VideoDownloader", "咸蛋黄"))
        self.pink_btn.setText(QtWidgets.QApplication.translate("VideoDownloader", "少女粉"))
        self.purple_btn.setText(QtWidgets.QApplication.translate("VideoDownloader", "基佬紫"))
        self.green_btn.setText(QtWidgets.QApplication.translate("VideoDownloader", "草苗绿"))
        self.change_btn.setText(QtWidgets.QApplication.translate("VideoDownloader", "更改"))
        self.h_aq.setText(QtWidgets.QApplication.translate("VideoDownloader", "高音质"))
        self.s_aq.setText(QtWidgets.QApplication.translate("VideoDownloader", "标准音质"))

    def change_language(self):
        if self.eng_btn.isChecked():
            self.tran.load("chs-eng")
            _app = QtWidgets.QApplication.instance()
            _app.installTranslator(self.tran)
        else:
            _app = QtWidgets.QApplication.instance()
            _app.removeTranslator(self.tran)

    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.LanguageChange:
            self.retranslateUi()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()

    def mouseMoveEvent(self, event):
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(event.globalPos() - self.m_Position)  # 更改窗口位置
            event.accept()

    def mouseReleaseEvent(self, event):
        self.m_flag = False


class ListDelegate(QtWidgets.QStyledItemDelegate):

    def __init__(self, name, val=0):
        super(ListDelegate, self).__init__()
        self.name = name
        self.val = val

    def paint(self, painter, option, index):
        # 绘制缩略图
        img = Image.open("./temp/pic.jpg")
        painter.drawPixmap(QtCore.QRect(5, 5, 195, 110), QtGui.QPixmap("./temp/pic.jpg"), QtCore.QRect(0, 0, img.width, img.height))

        # 绘制视频名
        font = painter.font()
        font.setPixelSize(18)
        font.setFamily('黑体')
        painter.setFont(font)
        painter.drawText(QtCore.QRect(210, 10, 725, 40), 0, self.name)

        # 绘制下载信息
        font = painter.font()
        font.setPixelSize(15)
        font.setFamily('微软雅黑')
        info = "info, info, info"
        painter.setPen(QtGui.QColor(128, 128, 128))
        painter.drawText(QtCore.QRect(210, 60, 725, 90), 0, info)

        # 绘制进度条
        style = QtWidgets.QStyleOptionProgressBar()
        style.rect = QtCore.QRect(210, 85, 725, 15)
        style.minimum = 0
        style.maximum = 100
        style.progress = self.val
        QtWidgets.QApplication.style().drawControl(QtWidgets.QStyle.CE_ProgressBar, style, painter)

        if option.state & QtWidgets.QStyle.State_MouseOver:
            rect = option.rect
            painter.setBrush(QtGui.QColor(0, 0, 64, 32))
            painter.drawRect(rect.topLeft().x(), rect.topLeft().y(), rect.width(), rect.height())

        if option.state & QtWidgets.QStyle.State_Selected:
            rect = option.rect
            painter.setBrush(QtGui.QColor(0, 0, 64, 64))
            painter.drawRect(rect.topLeft().x(), rect.topLeft().y(), rect.width(), rect.height())


class DownloadThread(QtCore.QThread):  # 下载线程
    download_proess_signal = QtCore.pyqtSignal(int)  # 创建信号

    def __init__(self, res, filesize, fileobj, buffer, state):
        super(DownloadThread, self).__init__()
        self.filesize = filesize
        self.fileobj = fileobj
        self.buffer = buffer
        self.res = res
        self.state = state

    def run(self):
        try:
            rsp = self.res  # 流下载模式
            offset = 0
            for chunk in rsp.iter_content(chunk_size=self.buffer):
                if not chunk: break
                self.fileobj.seek(offset)  # 设置指针位置
                self.fileobj.write(chunk)  # 写入文件
                offset = offset + len(chunk)
                # print(f'offset:{offset}')
                if self.state == 0:
                    proess = offset / int(self.filesize) * 90  # 90%为视频下载完成
                elif self.state == 1:
                    proess = offset / int(self.filesize) * 5 + 90  # 95%为音频下载完成
                # print(f'proess:{proess}')
                self.download_proess_signal.emit(int(proess))  # 发送信号

            self.fileobj.close()  # 关闭文件
            self.exit(0)  # 关闭线程
            print("下载完成")

        except Exception as e:
            print(e)


class CustomBtn(QtWidgets.QAbstractButton):
    def __init__(self, parent):
        super(CustomBtn, self).__init__(parent)
        self.setAutoExclusive(True)
        self.setCheckable(True)
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.hover_flag = 0

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        if self.hover_flag and not self.isChecked():
            pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 0))
            painter.setPen(pen)
            brush = QtGui.QBrush(QtGui.QColor(200, 200, 200, 154))
            painter.setBrush(brush)
            painter.setRenderHint(QtGui.QPainter.Antialiasing)
            painter.drawRoundedRect(0, 0, 230, 40, 7.0, 7.0)
        if self.isChecked():
            pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 0))
            painter.setPen(pen)
            brush = QtGui.QBrush(QtGui.QColor(64, 64, 64, 154))
            painter.setBrush(brush)
            painter.setRenderHint(QtGui.QPainter.Antialiasing)
            painter.drawRoundedRect(0, 0, 230, 40, 7.0, 7.0)
        pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(pen)
        font = QtGui.QFont("微软雅黑", 12)
        painter.setFont(font)
        painter.drawText(0, 0, 230, 40, QtCore.Qt.AlignCenter, self.text())

    def enterEvent(self, event):
        self.hover_flag = 1

    def leaveEvent(self, event):
        self.hover_flag =0


class CustomTable(QtWidgets.QTableWidget):

    def __init__(self, parent):
        super(CustomTable, self).__init__(parent)
        self.cellEntered.connect(self.cell_enter)
        self.pre_row = -1

    def leaveEvent(self, event):
        item = self.item(self.pre_row, 0)
        if item is not None:
            self.set_row_color(self.pre_row, QtGui.QColor(0, 0, 0, 0))

    def cell_enter(self, row, col):
        if self.pre_row != -1:
            item = self.item(self.pre_row, 0)
            if item is not None:
                self.set_row_color(self.pre_row, QtGui.QColor(0, 0, 0, 0))
        item = self.item(row, col)
        if item is not None and not item.isSelected():
            self.set_row_color(row, QtGui.QColor(255, 0, 0, 50))
        self.pre_row = row

    def set_row_color(self, row, color):
        for i in range(self.columnCount()):
            item = self.item(row, i)
            item.setBackground(color)


class CustomLabel(QtWidgets.QLabel):

    def __init__(self, parent):
        super(CustomLabel, self).__init__(parent)
        self.setFixedSize(950, 30)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QColor(0, 0, 0, 0))
        painter.setBrush(QtGui.QColor(67, 125, 198))
        painter.drawRect(0, 0, 10, 30)
        painter.setPen(QtGui.QColor(0, 0, 0))
        painter.setFont(QtGui.QFont("微软雅黑", 12))
        painter.drawText(20, 0, 180, 30, QtCore.Qt.AlignVCenter, self.text())


class ColorChangingBtn(QtWidgets.QAbstractButton):

    def __init__(self, parent, color):
        super(ColorChangingBtn, self).__init__(parent)
        self.setCheckable(True)
        self.setAutoExclusive(True)
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.resize(60, 80)
        self.color = color

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QColor(0, 0, 0, 0))
        painter.setBrush(self.color)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.drawRoundedRect(5, 5, 50, 50, 7.0, 7.0)
        painter.setPen(QtGui.QColor(0, 0, 0))
        painter.setFont(QtGui.QFont("微软雅黑", 9))
        painter.drawText(0, 60, 58, 20, QtCore.Qt.AlignCenter, self.text())
        if self.isChecked():
            pen = QtGui.QPen(self.color)
            pen.setWidth(3)
            painter.setPen(pen)
            painter.setBrush(QtGui.QColor(0, 0, 0, 0))
            painter.setRenderHint(QtGui.QPainter.Antialiasing)
            painter.drawRoundedRect(1, 1, 58, 58, 7.0, 7.0)
            painter.setPen(self.color)
            painter.setFont(QtGui.QFont("微软雅黑", 9))
            painter.drawText(0, 60, 58, 20, QtCore.Qt.AlignCenter, self.text())


class CustomWidget(QtWidgets.QWidget):

    def __init__(self, parent):
        super(CustomWidget, self).__init__(parent)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()

    def mouseMoveEvent(self, event):
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(event.globalPos() - self.m_Position)  # 更改窗口位置
            event.accept()

    def mouseReleaseEvent(self, event):
        self.m_flag = False


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    run = VideoDownloader()
    run.setup_ui()
    run.engine_switch()
    run.style_change()
    sys.exit(app.exec_())
