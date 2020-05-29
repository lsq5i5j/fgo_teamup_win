import sys
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import pyqtSignal
import SelectProgressUi
import pandas as pd


class Ui_SelectProgress(QDialog, SelectProgressUi.Ui_Dialog):
	def __init__(self):
		super(Ui_SelectProgress, self).__init__()
		self.setupUi(self)
		# 读取已保存的进度
		with open("data/level/progress.txt", 'r', encoding='utf-8-sig') as f:
			data = f.readline()
			self.current_event = data.replace('\n', '')
		# 读取未来事件列表
		self.df_future_event = pd.read_csv('data/level/event_list.csv')
		event_list = tuple(self.df_future_event['事件名称'].values)
		self.box_select_event.clear()
		self.box_select_event.addItems(event_list)
		self.df_future_event_new = pd.read_csv('data/level/event_list.csv')
		self.box_select_event.setCurrentText(self.current_event)
		# 绑定按钮
		self.btn_confirm.clicked.connect(self.confirm)
		self.btn_cancle.clicked.connect(self.close)

	def confirm(self):
		event_name = self.box_select_event.currentText()
		# 保存进度到本地
		with open("data/level/progress.txt", "w", encoding='utf-8-sig') as f:
			f.write(event_name)
		QMessageBox.question(self, '提  醒', '进度设置成功!', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		self.close()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	# 实例化子窗口
	selectmaster = Ui_SelectProgress()
	selectmaster.show()
	sys.exit(app.exec_())


