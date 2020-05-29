import sys
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtCore import Qt, pyqtSignal
import SelectTargetUi_Inverse


class Ui_SelectTarget_Inverse(QDialog, SelectTargetUi_Inverse.Ui_Dialog):
	my_Signal = pyqtSignal(int)
	def __init__(self):
		super(Ui_SelectTarget_Inverse, self).__init__()
		# QDialog.__init__(self)
		# SelectServantUi.Ui_Dialog.__init__(self)
		self.setupUi(self)
		self.btn_1.clicked.connect(lambda: self.sendEditContent(1))
		self.btn_2.clicked.connect(lambda: self.sendEditContent(2))
		self.btn_3.clicked.connect(lambda: self.sendEditContent(3))

	def sendEditContent(self, target):
		self.my_Signal.emit(target)
		self.close()






if __name__ == '__main__':
	app = QApplication(sys.argv)
	# 实例化子窗口
	selectservant = Ui_SelectTarget_Inverse()
	selectservant.show()
	sys.exit(app.exec_())



