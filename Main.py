import sys
import os
from PyQt5 import QtWidgets, QtGui, QtCore
from VideoSource import bilibili
from PIL import Image


class VideoDownloader(QtWidgets.QMainWindow):
    """
    bug: 队列超过一个视频源时，画质选择会有冲突
         下载队列超过一个视频会有缩略图显示问题
         有多线程问题
    """

    def __init__(self):
        super(VideoDownloader, self).__init__()
        self.engine_list = ['b站', '...']
        self.sess = None
        self.video = []
        self.audio = []
        self.num = 0  # 记录表格行数，便于动态调整
        self.video_info = []

    def setup_ui(self):
        self.setObjectName("main_window")
        self.resize(1200, 800)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.central_widget = QtWidgets.QWidget(self)
        self.central_widget.setObjectName("central_widget")

        # 设置侧边栏
        self.left_widget = QtWidgets.QWidget(self.central_widget)
        self.left_widget.setGeometry(0, 60, 250, 800)
        self.left_widget.setObjectName("left_widget")
        # self.btn1 = QtWidgets.QPushButton("搜索", self.left_widget)
        self.btn1 = CustomBtn(self.left_widget)
        self.btn1.setGeometry(10, 20, 230, 50)
        self.setObjectName("left_btn1")
        self.btn1.clicked.connect(lambda: self.right_widget.setCurrentIndex(0))
        # self.btn2 = QtWidgets.QPushButton("设置", self.left_widget)
        self.btn2 = CustomBtn(self.left_widget)
        self.btn2.setGeometry(10, 90, 230, 50)
        self.btn2.setObjectName("left_btn2")
        self.btn2.clicked.connect(lambda: self.right_widget.setCurrentIndex(1))

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
        self.close_btn.clicked.connect(self.close)
        self.minimize_btn = QtWidgets.QPushButton(self.top_bar)
        self.minimize_btn.setGeometry(1110, 15, 1140, 45)
        self.minimize_btn.setFixedSize(30, 30)
        self.minimize_btn.setObjectName("minimize_btn")
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
        self.table.setFrameShape(QtWidgets.QFrame.NoFrame)
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
        self.option_page = QtWidgets.QWidget()
        self.option_page.setObjectName("option_page")
        self.option_page.setGeometry(250, 0, 1200, 800)

        self.right_widget.addWidget(self.download_page)
        self.right_widget.addWidget(self.option_page)
        self.right_widget.setCurrentIndex(0)

        self.setCentralWidget(self.central_widget)
        self.show()

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
        temp3 = [self.set_pic(), filename, time, self.set_quality_select(duration, self.num), self.set_dl_btn(self.num, duration)]
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
        sp = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.choose_vq.setSizePolicy(sp)
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
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.choose_vq.setPalette(palette)
        self.choose_vq.setLineEdit(text)
        combobox_drop_down = QtWidgets.QListWidget()  # 设置combobox下拉菜单字体
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

    def set_dl_btn(self, num, duration):
        # 设置开始下载按钮
        box2 = QtWidgets.QWidget()
        v_box_2 = QtWidgets.QVBoxLayout(box2)
        dl_btn = QtWidgets.QPushButton(box2)
        dl_btn.clicked.connect(lambda: self.download(num, self.choose_vq.currentIndex(), 0, duration))  # 设置下载按钮触发
        v_box_2.addWidget(dl_btn)
        return box2

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

    def download(self, num, vq, aq, duration):
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
        download_thread = DownloadThread(video_res, video_res.headers['Content-Length'], open("./temp/video.flv", 'wb'), 10240, 0)
        download_thread.download_proess_signal.connect(self.set_prosess)
        download_thread.start()

        audio_size = int((duration / 1000) * self.audio[num-1][aq][2] / 8)
        audio_res = self.sess.get_audio(self.audio[num-1][aq][1], audio_size)

        # 创建音频下载线程
        download_thread = DownloadThread(audio_res, audio_res.headers['Content-Length'], open("./temp/audio.mp3", 'wb'), 10240, 1)
        download_thread.download_proess_signal.connect(self.set_prosess)
        download_thread.start()

        if download_thread.isFinished() == 1:  # 判断是否下载完成
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


class DownloadThread(QtCore.QThread):
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
                    proess = offset / int(self.filesize) * 5 + 90  # 95%为视频下载完成
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
        self.hover_flag = 0

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        if self.hover_flag:
            pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 0))
            painter.setPen(pen)
            brush = QtGui.QBrush(QtGui.QColor(200, 200, 200))
            painter.setBrush(brush)
            painter.drawRoundedRect(0, 0, 230, 40, 7.0, 7.0)
        if not self.hover_flag:
            pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 0))
            painter.setPen(pen)
            brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
            painter.setBrush(brush)
            painter.drawRoundedRect(0, 0, 230, 40, 7.0, 7.0)
        pen = QtGui.QPen(QtGui.QColor(255, 0, 0))
        painter.setPen(pen)
        painter.drawText(0, 0, 230, 40, 0, "test")

    def enterEvent(self, event):
        self.hover_flag = 1

    def leaveEvent(self, event):
        self.hover_flag =0


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    run = VideoDownloader()
    run.setup_ui()
    run.engine_switch()
    with open('StyleSheet.qss', 'r') as f:
        style = f.read()
    app.setStyleSheet(style)
    sys.exit(app.exec_())
