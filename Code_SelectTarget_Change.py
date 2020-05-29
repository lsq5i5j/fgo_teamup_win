import sys
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
import SelectTargetUi_Change


class Ui_SelectTarget_Change(QDialog, SelectTargetUi_Change.Ui_Dialog):
	my_Signal = pyqtSignal(tuple)
	def __init__(self):
		super(Ui_SelectTarget_Change, self).__init__()
		# QDialog.__init__(self)
		# SelectServantUi.Ui_Dialog.__init__(self)
		self.setupUi(self)
		self.btn_1.clicked.connect(lambda: self.select_front(1))
		self.btn_2.clicked.connect(lambda: self.select_front(2))
		self.btn_3.clicked.connect(lambda: self.select_front(3))
		self.btn_4.clicked.connect(lambda: self.select_front(4))
		self.btn_5.clicked.connect(lambda: self.select_front(5))
		self.btn_6.clicked.connect(lambda: self.select_front(6))
		self.btn_confirm.clicked.connect(self.confirm_selection)

		self.label_1.setScaledContents(True)
		self.label_2.setScaledContents(True)
		self.label_3.setScaledContents(True)
		self.label_4.setScaledContents(True)
		self.label_5.setScaledContents(True)
		self.label_6.setScaledContents(True)
		self.front = 0
		self.back = 0
		self.pic_select = QPixmap('./pic/icon/skill_used.png')

	def select_front(self, order):
		if order == 1:
			self.label_1.setPixmap(self.pic_select)
			self.label_2.setPixmap(QPixmap())
			self.label_3.setPixmap(QPixmap())
			self.front = 1
		elif order == 2:
			self.label_2.setPixmap(self.pic_select)
			self.label_1.setPixmap(QPixmap())
			self.label_3.setPixmap(QPixmap())
			self.front = 2
		elif order == 3:
			self.label_3.setPixmap(self.pic_select)
			self.label_1.setPixmap(QPixmap())
			self.label_2.setPixmap(QPixmap())
			self.front = 3
		elif order == 4:
			self.label_4.setPixmap(self.pic_select)
			self.label_5.setPixmap(QPixmap())
			self.label_6.setPixmap(QPixmap())
			self.back = 4
		elif order == 5:
			self.label_5.setPixmap(self.pic_select)
			self.label_4.setPixmap(QPixmap())
			self.label_6.setPixmap(QPixmap())
			self.back = 5
		elif order == 6:
			self.label_6.setPixmap(self.pic_select)
			self.label_4.setPixmap(QPixmap())
			self.label_5.setPixmap(QPixmap())
			self.back = 6

	def confirm_selection(self):
		if self.front == 0:
			QMessageBox.information(self, '提 醒', '检测到未选择前排从者, 请选择后继续', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
			return
		elif self.back == 0:
			QMessageBox.information(self, '提 醒', '检测到未选择后排从者, 请选择后继续', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
			return

		self.my_Signal.emit((self.front, self.back))
		self.close()

	def reset(self):
		self.close()
		self.front = 0
		self.back = 0
		self.label_1.setPixmap(QPixmap())
		self.label_2.setPixmap(QPixmap())
		self.label_3.setPixmap(QPixmap())
		self.label_4.setPixmap(QPixmap())
		self.label_5.setPixmap(QPixmap())
		self.label_6.setPixmap(QPixmap())

if __name__ == '__main__':
	app = QApplication(sys.argv)
	# 实例化子窗口
	selectservant = Ui_SelectTarget_Change()
	selectservant.show()
	sys.exit(app.exec_())



