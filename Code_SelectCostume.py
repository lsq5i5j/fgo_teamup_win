import sys
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, pyqtSignal
import SelectCostumeUi
import pandas as pd


class Ui_SelectCostume(QDialog, SelectCostumeUi.Ui_Dialog):
	my_Signal = pyqtSignal(dict)
	def __init__(self):
		super(Ui_SelectCostume, self).__init__()
		# QDialog.__init__(self)
		# SelectServantUi.Ui_Dialog.__init__(self)
		self.setupUi(self)
		self.box_level.setMaximum(1000)

		self.set_zero()
		self.costume_data = pd.read_csv('data/costume/costume_data.csv')
		self.costume_atk_all = pd.read_csv('data/costume/costume_atk.csv')
		# self.disable_costume_setting()

		icon = QIcon()
		icon.addPixmap(QPixmap("./pic/costume_logo/礼装000.jpg"), QIcon.Normal, QIcon.Off)
		self.btn_000.setIcon(icon)
		icon = QIcon()
		icon.addPixmap(QPixmap("./pic/costume_logo/礼装028.jpg"), QIcon.Normal, QIcon.Off)
		self.btn_028.setIcon(icon)
		icon = QIcon()
		icon.addPixmap(QPixmap("./pic/costume_logo/礼装034.jpg"), QIcon.Normal, QIcon.Off)
		self.btn_034.setIcon(icon)
		icon = QIcon()
		icon.addPixmap(QPixmap("./pic/costume_logo/礼装048.jpg"), QIcon.Normal, QIcon.Off)
		self.btn_048.setIcon(icon)
		icon = QIcon()
		icon.addPixmap(QPixmap("./pic/costume_logo/礼装052.jpg"), QIcon.Normal, QIcon.Off)
		self.btn_052.setIcon(icon)
		icon = QIcon()
		icon.addPixmap(QPixmap("./pic/costume_logo/礼装053.jpg"), QIcon.Normal, QIcon.Off)
		self.btn_053.setIcon(icon)
		icon = QIcon()
		icon.addPixmap(QPixmap("./pic/costume_logo/礼装181.jpg"), QIcon.Normal, QIcon.Off)
		self.btn_181.setIcon(icon)
		icon = QIcon()
		icon.addPixmap(QPixmap("./pic/costume_logo/礼装261.jpg"), QIcon.Normal, QIcon.Off)
		self.btn_261.setIcon(icon)
		icon = QIcon()
		icon.addPixmap(QPixmap("./pic/costume_logo/礼装265.jpg"), QIcon.Normal, QIcon.Off)
		self.btn_265.setIcon(icon)
		icon = QIcon()
		icon.addPixmap(QPixmap("./pic/costume_logo/礼装295.jpg"), QIcon.Normal, QIcon.Off)
		self.btn_295.setIcon(icon)
		icon = QIcon()
		icon.addPixmap(QPixmap("./pic/costume_logo/礼装309.jpg"), QIcon.Normal, QIcon.Off)
		self.btn_309.setIcon(icon)
		icon = QIcon()
		icon.addPixmap(QPixmap("./pic/costume_logo/礼装390.jpg"), QIcon.Normal, QIcon.Off)
		self.btn_390.setIcon(icon)
		icon = QIcon()
		icon.addPixmap(QPixmap("./pic/costume_logo/礼装400.jpg"), QIcon.Normal, QIcon.Off)
		self.btn_400.setIcon(icon)
		icon = QIcon()
		icon.addPixmap(QPixmap("./pic/costume_logo/礼装570.jpg"), QIcon.Normal, QIcon.Off)
		self.btn_570.setIcon(icon)
		icon = QIcon()
		icon.addPixmap(QPixmap("./pic/costume_logo/礼装655.jpg"), QIcon.Normal, QIcon.Off)
		self.btn_655.setIcon(icon)
		icon = QIcon()
		icon.addPixmap(QPixmap("./pic/costume_logo/礼装683.jpg"), QIcon.Normal, QIcon.Off)
		self.btn_683.setIcon(icon)
		icon = QIcon()
		icon.addPixmap(QPixmap("./pic/costume_logo/礼装792.jpg"), QIcon.Normal, QIcon.Off)
		self.btn_792.setIcon(icon)
		icon = QIcon()
		icon.addPixmap(QPixmap("./pic/costume_logo/礼装871.jpg"), QIcon.Normal, QIcon.Off)
		self.btn_871.setIcon(icon)
		icon = QIcon()
		icon.addPixmap(QPixmap("./pic/costume_logo/礼装1126.jpg"), QIcon.Normal, QIcon.Off)
		self.btn_1126.setIcon(icon)

		self.check_full.stateChanged.connect(self.change_check_full)
		self.costume_isfull = 0

		self.atk_list = [0 for _ in range(100)]
		self.level = 0
		self.atk = 0
		self.id = 0
		self.data = pd.DataFrame({'效果': [''], '幅度': [0]})
		self.data_full = pd.DataFrame({'效果': [''], '幅度': [0]})
		self.btn_000.clicked.connect(lambda: self.choose_costume(0))
		self.btn_028.clicked.connect(lambda: self.choose_costume(28))
		self.btn_034.clicked.connect(lambda: self.choose_costume(34))
		self.btn_048.clicked.connect(lambda: self.choose_costume(48))
		self.btn_052.clicked.connect(lambda: self.choose_costume(52))
		self.btn_053.clicked.connect(lambda: self.choose_costume(53))
		self.btn_181.clicked.connect(lambda: self.choose_costume(181))
		self.btn_261.clicked.connect(lambda: self.choose_costume(261))
		self.btn_265.clicked.connect(lambda: self.choose_costume(265))
		self.btn_295.clicked.connect(lambda: self.choose_costume(295))
		self.btn_309.clicked.connect(lambda: self.choose_costume(309))
		self.btn_390.clicked.connect(lambda: self.choose_costume(390))
		self.btn_400.clicked.connect(lambda: self.choose_costume(400))
		self.btn_570.clicked.connect(lambda: self.choose_costume(570))
		self.btn_655.clicked.connect(lambda: self.choose_costume(655))
		self.btn_683.clicked.connect(lambda: self.choose_costume(683))
		self.btn_792.clicked.connect(lambda: self.choose_costume(792))
		self.btn_871.clicked.connect(lambda: self.choose_costume(871))
		self.btn_1126.clicked.connect(lambda: self.choose_costume(1126))
		self.btn_reset.clicked.connect(lambda: self.reset())
		self.btn_confirm.clicked.connect(lambda: self.confirm())
		self.btn_cancle.clicked.connect(self.close)
		self.box_level.valueChanged.connect(lambda: self.set_atk())

	def set_atk(self):
		if self.box_level.value() > 100:
			self.box_level.setValue(100)
		self.level = self.box_level.value()
		self.atk = self.atk_list[self.level - 1]
		self.box_atk.setValue(self.atk)
		if self.level > 80:
			self.change_check_full(2)

	def reset(self):
		self.id = -1
		dict = {'atk': 0, 'range': '', 'ID': self.id, 'level': self.level, 'full': self.costume_isfull}
		self.my_Signal.emit(dict)
		self.close()

	def confirm(self):
		self.sendEditContent()
		self.close()

	def change_check_full(self, state):
		if state == 0:
			self.check_full.setChecked(False)
			self.costume_isfull = 0
		else:
			self.check_full.setChecked(True)
			self.costume_isfull = 1
		self.show_data()

	def set_zero(self):
		self.box_atk.setValue(0)
		self.box_np_start.setValue(0)
		self.box_np_end.setValue(0)

		self.box_attack.setValue(0)
		self.box_buster.setValue(0)
		self.box_arts.setValue(0)
		self.box_quick.setValue(0)
		self.box_np.setValue(0)
		self.box_np_gain.setValue(0)
		self.box_oc.setValue(0)
		self.lineEdit_attribute.setText('')

		self.box_attack_times.setValue(-1)
		self.box_buster_times.setValue(-1)
		self.box_arts_times.setValue(-1)
		self.box_quick_times.setValue(-1)
		self.box_np_times.setValue(-1)
		self.box_np_gain_times.setValue(-1)
		self.box_oc_times.setValue(-1)
		self.box_attribute_times.setValue(-1)

		self.box_attack_round.setValue(-1)
		self.box_buster_round.setValue(-1)
		self.box_arts_round.setValue(-1)
		self.box_quick_round.setValue(-1)
		self.box_np_round.setValue(-1)
		self.box_np_gain_round.setValue(-1)
		self.box_oc_round.setValue(-1)
		self.box_attribute_round.setValue(-1)

	def choose_costume(self, id):
		if id in [-1, 0, 34, 48, 295, 400]:
			self.change_check_full(0)
		else:
			self.change_check_full(2)

		self.set_zero()
		self.id = id
		if id > 0:
			df = self.costume_atk_all
			list1 = df[df['ID'] == self.id].values.tolist()[0]
			self.atk_list = list1[len(list1)-100: len(list1)]
		else:
			self.atk_list = [0 for _ in range(100)]
		pix = QPixmap()
		if id != -1:
			pix = QPixmap('./pic/costume_logo/礼装'+str(id).zfill(3)+'.jpg')
		self.label_costume_pic.setPixmap(pix)
		self.label_costume_pic.setScaledContents(True)

		if id == 0:
			pass
			# self.enable_costume_setting()
		elif id < 0:
			pass
			# self.disable_costume_setting()
		elif id > 0:

			# self.disable_costume_setting()
			df = self.costume_data
			df1 = df[df['ID'] == id]
			self.data = df1[['效果', '幅度']]
			self.data_full = df1[['效果', '幅度(满破)']]
			self.data_full.columns = ['效果', '幅度']
			self.show_data()

	def show_data(self):
		if self.id <= 0:
			return
		self.set_zero()
		if self.costume_isfull == 0:
			df2 = self.data
		else:
			df2 = self.data_full

		self.level = self.box_level.value()
		self.atk = self.atk_list[self.level - 1]
		self.box_atk.setValue(self.atk)
		for index, row in df2.iterrows():
			num = row['幅度']
			if row['效果'] == '初始NP':
				self.box_np_start.setValue(num)
			elif row['效果'] == '攻击力提升':
				self.box_attack.setValue(num)
			elif row['效果'] == 'Buster指令卡性能提升':
				self.box_buster.setValue(num)
			elif row['效果'] == 'Arts指令卡性能提升':
				self.box_arts.setValue(num)
			elif row['效果'] == 'Quick指令卡性能提升':
				self.box_quick.setValue(num)
			elif row['效果'] == '宝具威力提升':
				self.box_np.setValue(num)
			elif row['效果'] == '活动攻击力提升':
				self.box_np_event.setValue(num)
			elif row['效果'] == 'NP获得量提升':
				self.box_np_gain.setValue(num)
			elif row['效果'] == '充能阶段上升':
				self.box_oc.setValue(num)
			elif row['效果'] == '退场时己方全体NP增加':
				self.box_np_end.setValue(num)
		if self.id == 400:
			self.box_oc_times.setValue(1)

	def sendEditContent(self):
		atk = self.box_atk.value()
		target_range = '自身'
		costume_dict = {'atk': atk, 'range': target_range, 'ID': self.id, 'level': self.level, 'full': self.costume_isfull}
		if self.box_attack.value() != 0:
			costume_dict.update({'状态[攻击力提升(不可解除)]': [str(self.box_attack.value())+'%', self.box_attack_times.value(), self.box_attack_round.value()]})
		if self.box_buster.value() != 0:
			costume_dict.update({'状态[Buster指令卡性能提升(不可解除)]': [str(self.box_buster.value())+'%', self.box_buster_times.value(),self.box_buster_round.value()]})
		if self.box_arts.value() != 0:
			costume_dict.update({'状态[Arts指令卡性能提升(不可解除)]': [str(self.box_arts.value())+'%', self.box_arts_times.value(), self.box_arts_round.value()]})
		if self.box_quick.value() != 0:
			costume_dict.update({'状态[Quick指令卡性能提升(不可解除)]': [str(self.box_quick.value())+'%', self.box_quick_times.value(), self.box_quick_round.value()]})
		if self.box_np.value() != 0:
			costume_dict.update({'状态[宝具威力提升(不可解除)]': [str(self.box_np.value())+'%', self.box_np_times.value(), self.box_np_round.value()]})
		if self.box_np_event.value() != 0:
			costume_dict.update({'状态[活动攻击力提升(不可解除)]': [str(self.box_np_event.value()) + '%', -1, -1]})
		if self.box_np_gain.value() != 0:
			costume_dict.update({'状态[NP获得量提升(不可解除)]': [str(self.box_np_gain.value())+'%', self.box_np_gain_times.value(), self.box_np_gain_round.value()]})
		if self.box_oc.value() != 0:
			costume_dict.update({'状态[充能阶段上升(不可解除)]': [str(self.box_oc.value()), self.box_oc_times.value(), self.box_oc_round.value()]})
		if self.box_np_end.value() != 0:
			costume_dict.update({'状态[退场时NP增加(不可解除)]': [str(self.box_np_end.value())+'%', -1, -1]})
		if self.box_np_start.value() != 0:
			costume_dict.update({'初始NP': self.box_np_start.value()})
		if self.lineEdit_attribute.text() != '':
			text = '状态[特攻['+self.lineEdit_attribute.text()+']]'
			costume_dict.update({text: [str(self.box_attribute.value())+'%', self.box_attribute_times.value(), self.box_attribute_round.value()]})
		print(target_range)
		print(costume_dict)
		self.my_Signal.emit(costume_dict)

	def receiveContent(self, costume_dict):
		print(costume_dict)
		self.set_zero()
		self.level = costume_dict['level']
		self.atk = costume_dict['atk']
		self.id = costume_dict['ID']
		self.box_atk.setValue(self.atk)
		self.box_level.setValue(self.level)

		self.choose_costume(self.id)
		self.box_atk.setValue(costume_dict['atk'])
		if costume_dict['full'] == 0:
			self.check_full.setCheckState(0)
		else:
			self.check_full.setCheckState(2)
		for buff in costume_dict:
			if buff == '状态[攻击力提升(不可解除)]':
				temp = costume_dict[buff]
				self.box_attack.setValue(int(temp[0].strip("%")))
				self.box_attack_times.setValue(temp[1])
				self.box_attack_round.setValue(temp[2])
			elif buff == '状态[Buster指令卡性能提升(不可解除)]':
				temp = costume_dict[buff]
				self.box_buster.setValue(int(temp[0].strip("%")))
				self.box_buster_times.setValue(temp[1])
				self.box_buster_round.setValue(temp[2])
			elif buff == '状态[Arts指令卡性能提升(不可解除)]':
				temp = costume_dict[buff]
				self.box_arts.setValue(int(temp[0].strip("%")))
				self.box_arts_times.setValue(temp[1])
				self.box_arts_round.setValue(temp[2])
			elif buff == '状态[Quick指令卡性能提升(不可解除)]':
				temp = costume_dict[buff]
				self.box_quick.setValue(int(temp[0].strip("%")))
				self.box_quick_times.setValue(temp[1])
				self.box_quick_round.setValue(temp[2])
			elif buff == '状态[宝具威力提升(不可解除)]':
				temp = costume_dict[buff]
				self.box_np.setValue(int(temp[0].strip("%")))
				self.box_np_times.setValue(temp[1])
				self.box_np_round.setValue(temp[2])
			elif buff == '状态[活动攻击力提升(不可解除)]':
				temp = costume_dict[buff]
				self.box_np_event.setValue(int(temp[0].strip("%")))
			elif buff == '状态[NP获得量提升(不可解除)]':
				temp = costume_dict[buff]
				self.box_np_gain.setValue(int(temp[0].strip("%")))
				self.box_np_gain_times.setValue(temp[1])
				self.box_np_gain_round.setValue(temp[2])
			elif buff == '状态[充能阶段上升(不可解除)]':
				temp = costume_dict[buff]
				self.box_oc.setValue(int(temp[0].strip("%")))
				self.box_oc_times.setValue(temp[1])
				self.box_oc_round.setValue(temp[2])
			elif buff == '状态[退场时NP增加(不可解除)]':
				temp = costume_dict[buff]
				self.box_np_end.setValue(int(temp[0].strip("%")))
			elif buff == '初始NP':
				temp = costume_dict[buff]
				self.box_np_start.setValue(temp)
			elif buff.startswith('状态[特攻['):
				text = buff.strip('状态[特攻[]]')
				self.lineEdit_attribute.setText(text)
				temp = costume_dict[buff]
				self.box_attribute.setValue(int(temp[0].strip("%")))
				self.box_attribute_times.setValue(temp[1])
				self.box_attribute_round.setValue(temp[2])

	def disable_costume_setting(self):
		self.box_level.setEnabled(True)
		self.box_np_start.setEnabled(False)
		self.box_np_end.setEnabled(False)
		self.box_atk.setEnabled(False)
		self.box_attack.setEnabled(False)
		self.box_attack.setEnabled(False)
		self.box_attack_times.setEnabled(False)
		self.box_attack_round.setEnabled(False)
		self.box_buster.setEnabled(False)
		self.box_buster_times.setEnabled(False)
		self.box_buster_round.setEnabled(False)
		self.box_arts.setEnabled(False)
		self.box_arts_times.setEnabled(False)
		self.box_arts_round.setEnabled(False)
		self.box_quick.setEnabled(False)
		self.box_quick_times.setEnabled(False)
		self.box_quick_round.setEnabled(False)
		self.box_np.setEnabled(False)
		self.box_np_times.setEnabled(False)
		self.box_np_round.setEnabled(False)
		self.box_np_gain.setEnabled(False)
		self.box_np_gain_times.setEnabled(False)
		self.box_np_gain_round.setEnabled(False)
		self.box_oc.setEnabled(False)
		self.box_oc_times.setEnabled(False)
		self.box_oc_round.setEnabled(False)
		self.box_np_end.setEnabled(False)
		self.box_np_start.setEnabled(False)
		self.lineEdit_attribute.setEnabled(False)
		self.box_attribute.setEnabled(False)
		self.box_attribute_times.setEnabled(False)
		self.box_attribute_round.setEnabled(False)

	def enable_costume_setting(self):
		self.box_level.setEnabled(False)
		self.box_np_start.setEnabled(True)
		self.box_np_end.setEnabled(True)
		self.box_atk.setEnabled(True)
		self.box_attack.setEnabled(True)
		self.box_attack.setEnabled(True)
		self.box_attack_times.setEnabled(True)
		self.box_attack_round.setEnabled(True)
		self.box_buster.setEnabled(True)
		self.box_buster_times.setEnabled(True)
		self.box_buster_round.setEnabled(True)
		self.box_arts.setEnabled(True)
		self.box_arts_times.setEnabled(True)
		self.box_arts_round.setEnabled(True)
		self.box_quick.setEnabled(True)
		self.box_quick_times.setEnabled(True)
		self.box_quick_round.setEnabled(True)
		self.box_np.setEnabled(True)
		self.box_np_times.setEnabled(True)
		self.box_np_round.setEnabled(True)
		self.box_np_gain.setEnabled(True)
		self.box_np_gain_times.setEnabled(True)
		self.box_np_gain_round.setEnabled(True)
		self.box_oc.setEnabled(True)
		self.box_oc_times.setEnabled(True)
		self.box_oc_round.setEnabled(True)
		self.box_np_end.setEnabled(True)
		self.box_np_start.setEnabled(True)
		self.lineEdit_attribute.setEnabled(True)
		self.box_attribute.setEnabled(True)
		self.box_attribute_times.setEnabled(True)
		self.box_attribute_round.setEnabled(True)














if __name__ == '__main__':
	app = QApplication(sys.argv)
	# 实例化子窗口
	selectservant = Ui_SelectCostume()
	selectservant.show()
	sys.exit(app.exec_())



