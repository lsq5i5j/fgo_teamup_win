import sys
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import pyqtSignal
import SelectMasterUi
import pandas as pd
import os


class Ui_SelectMaster(QDialog, SelectMasterUi.Ui_Dialog):

	my_Signal = pyqtSignal(dict)

	def __init__(self):
		super(Ui_SelectMaster, self).__init__()
		# QDialog.__init__(self)
		# SelectmasterUi.Ui_Dialog.__init__(self)
		self.setupUi(self)
		self.update_master_list()
		df = pd.DataFrame()
		all_file = os.listdir('data/master')
		for file in all_file:
			if file.endswith('.csv'):
				path = 'data/master/' + file
				df = df.append(pd.read_csv(path), ignore_index=True)
		self.master_data_skill = df
		self.master_data = pd.read_csv('data/save/master_data_save.csv')
		df = self.master_data['序号']
		self.suit_num = max(df.values.tolist())
		self.chosen_master_id = 0
		self.chosen_master_name = ''
		self.chosen_master_level = 0
		self.choose_master(1)

		self.master_display()
		# 计算礼装数
		self.label_master_pic_a.setScaledContents(True)

		# 设定滑块功能
		self.bar_master_level.valueChanged.connect(lambda: self.change_value())
		#
		self.btn_confirm.clicked.connect(lambda: self.master_confirm())
		self.btn_data_reset.clicked.connect(lambda: self.reset_data())
		self.btn_data_output.clicked.connect(lambda: self.save_data_local())
		self.btn_clear.clicked.connect(lambda: self.master_clear())
		self.btn_cancel.clicked.connect(self.close)

		self.btn_master_1.clicked.connect(lambda: self.choose_master(1))
		self.btn_master_2.clicked.connect(lambda: self.choose_master(2))
		self.btn_master_3.clicked.connect(lambda: self.choose_master(3))
		self.btn_master_4.clicked.connect(lambda: self.choose_master(4))
		self.btn_master_5.clicked.connect(lambda: self.choose_master(5))
		self.btn_master_6.clicked.connect(lambda: self.choose_master(6))
		self.btn_master_7.clicked.connect(lambda: self.choose_master(7))
		self.btn_master_8.clicked.connect(lambda: self.choose_master(8))
		self.btn_master_9.clicked.connect(lambda: self.choose_master(9))
		self.btn_master_10.clicked.connect(lambda: self.choose_master(10))
		self.btn_master_11.clicked.connect(lambda: self.choose_master(11))
		self.btn_master_12.clicked.connect(lambda: self.choose_master(12))
		self.btn_master_13.clicked.connect(lambda: self.choose_master(13))
		self.btn_master_14.clicked.connect(lambda: self.choose_master(14))
		self.btn_master_15.clicked.connect(lambda: self.choose_master(15))
		self.btn_master_16.clicked.connect(lambda: self.choose_master(16))
		self.btn_master_17.clicked.connect(lambda: self.choose_master(17))
		self.btn_master_18.clicked.connect(lambda: self.choose_master(18))
		self.btn_master_19.clicked.connect(lambda: self.choose_master(19))
		self.btn_master_20.clicked.connect(lambda: self.choose_master(20))
		self.btn_master_21.clicked.connect(lambda: self.choose_master(21))
		self.btn_master_22.clicked.connect(lambda: self.choose_master(22))
		self.btn_master_23.clicked.connect(lambda: self.choose_master(23))
		self.btn_master_24.clicked.connect(lambda: self.choose_master(24))
		self.btn_master_25.clicked.connect(lambda: self.choose_master(25))
		self.label_skill_1.setWordWrap(True)
		self.label_skill_2.setWordWrap(True)
		self.label_skill_3.setWordWrap(True)

	def update_master_list(self):
		df = pd.DataFrame()
		all_file = os.listdir('data/master')
		for file in all_file:
			if file.endswith('.csv'):
				path = 'data/master/' + file
				df = df.append(pd.read_csv(path), ignore_index=True)
		df = df[['序号', '中文名']]
		df1 = df.drop_duplicates()

		try:
			df2 = pd.read_csv('data/save/master_data_save.csv')
		except IOError:
			df2 = pd.DataFrame(columns=['序号', '中文名', '等级'])

		for index, row in df1.iterrows():
			df = df2[df2['序号'] == row['序号']]
			if len(df) == 0:
				df2 = df2.append({'序号': row['序号'], '中文名': row['中文名'], '等级': 10}, ignore_index=True)
				df2.to_csv('data/save/master_data_save.csv', encoding='utf-8-sig', index=False)
				print('更新完毕', row['中文名'])

	def sendEditContent(self):
		content = {'ID': self.chosen_master_id, '等级': self.chosen_master_level}
		self.my_Signal.emit(content)

	def save_data(self):
		self.chosen_master_level = self.bar_master_level.value()
		df = self.master_data
		df1 = df[df['序号'] == self.chosen_master_id]
		row_name = df1._stat_axis.values.tolist()
		self.master_data.loc[row_name, ['等级']] = self.chosen_master_level

	def save_data_local(self):
		self.save_data()
		df = self.master_data
		df = df.sort_values(by='序号')
		df.to_csv('data/save/master_data_save.csv', encoding='utf-8-sig', index=False)
		QMessageBox.information(self, '提 醒', '当前数据已保存到本地', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

	def reset_data(self):
		reply = QMessageBox.question(self, '警 告', '还原数据会删除已保存的所有魔术礼装数据，是否继续？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if reply == QMessageBox.Yes:
			self.update_master_list()
			df = pd.read_csv('data/save/master_data_save.csv', encoding='utf-8-sig')
			df['等级'] = 10
			print(df)
			df = df[['序号', '中文名', '等级']]
			df = df.sort_values(by='序号')
			self.master_data = df
			self.master_data.to_csv('data/save/master_data_save.csv', encoding='utf-8-sig', index=False)
			self.set_master_data()
			self.display_master_data()
			QMessageBox.information(self, '提 醒', '魔术礼装数据已还原', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

	def master_confirm(self):
		self.save_data()
		self.sendEditContent()
		self.close()

	def master_clear(self):
		self.chosen_master_id = 0
		self.sendEditContent()
		self.close()

	def choose_master(self, number):
		if number <= self.suit_num:
			self.chosen_master_id = number
			# 设定魔术礼装数据
			self.set_master_data()
			# 显示数据
			self.display_master_data()

	def set_master_data(self):
		if self.chosen_master_id != 0:
			df = self.master_data
			df1 = df[df['序号'] == self.chosen_master_id]
			self.chosen_master_name = df1['中文名'].values[0]
			self.chosen_master_level = df1['等级'].values[0]
			self.label_name.setText(self.chosen_master_name + '\n')

			df = self.master_data_skill
			df1 = df[df['序号'] == self.chosen_master_id]
			df2 = df1[df1['技能序号'] == '技能1']
			list1 = df2['技能效果'].values.tolist()
			text = ''
			for i in list1:
				text += i+'\n'
			if text != '':
				text = '技能1: \n' + text
			self.label_skill_1.setText(text)

			df2 = df1[df1['技能序号'] == '技能2']
			list1 = df2['技能效果'].values.tolist()
			text = ''
			for i in list1:
				text += i + '\n'
			if text != '':
				text = '技能2: \n' + text
			self.label_skill_2.setText(text)

			df2 = df1[df1['技能序号'] == '技能3']
			list1 = df2['技能效果'].values.tolist()
			text = ''
			for i in list1:
				text += i + '\n'
			if text != '':
				text = '技能3: \n' + text
			self.label_skill_3.setText(text.strip('\n'))
		else:
			self.label_name.setText('')
			self.label_skill_1.setText('')
			self.label_skill_2.setText('')
			self.label_skill_3.setText('')

	def change_value(self):
		master_level = self.bar_master_level.value()
		# 显示数据
		self.label_master_level.setText('等级(' + str(master_level) + ')')

	def display_master_data(self):
		if self.chosen_master_id != 0:
			# 显示设置的数据
			pix = QPixmap("./pic/Master_logo/mystic_code_" + str(self.chosen_master_id).zfill(2) + "_a.png")
			self.label_master_pic_a.setPixmap(pix)
			self.label_master_level.setText('等级('+str(self.chosen_master_level)+')')
			self.bar_master_level.setValue(self.chosen_master_level)
		else:
			self.label_master_pic_a.setPixmap(QPixmap())
			self.label_master_level.setText('等级')
			self.bar_master_level.setValue(1)

	def receiveContent(self, data):
		id = data['ID']
		if id == 0:
			id = 1
		self.choose_master(id)

	def master_display(self):
		for i in range(1, self.suit_num+1):
			icon = QIcon()
			icon.addPixmap(QPixmap("./pic/Master_logo/mystic_code_" + str(i).zfill(2) + "_a.png"), QIcon.Normal, QIcon.Off)
			if i == 1:
				self.btn_master_1.setIcon(icon)
			elif i == 2:
				self.btn_master_2.setIcon(icon)
			elif i == 3:
				self.btn_master_3.setIcon(icon)
			elif i == 4:
				self.btn_master_4.setIcon(icon)
			elif i == 5:
				self.btn_master_5.setIcon(icon)
			elif i == 6:
				self.btn_master_6.setIcon(icon)
			elif i == 7:
				self.btn_master_7.setIcon(icon)
			elif i == 8:
				self.btn_master_8.setIcon(icon)
			elif i == 9:
				self.btn_master_9.setIcon(icon)
			elif i == 10:
				self.btn_master_10.setIcon(icon)
			elif i == 11:
				self.btn_master_11.setIcon(icon)
			elif i == 12:
				self.btn_master_12.setIcon(icon)
			elif i == 13:
				self.btn_master_13.setIcon(icon)
			elif i == 14:
				self.btn_master_14.setIcon(icon)
			elif i == 15:
				self.btn_master_15.setIcon(icon)
			elif i == 16:
				self.btn_master_16.setIcon(icon)
			elif i == 17:
				self.btn_master_17.setIcon(icon)
			elif i == 18:
				self.btn_master_18.setIcon(icon)
			elif i == 19:
				self.btn_master_19.setIcon(icon)
			elif i == 20:
				self.btn_master_20.setIcon(icon)
			elif i == 21:
				self.btn_master_21.setIcon(icon)
			elif i == 22:
				self.btn_master_22.setIcon(icon)
			elif i == 23:
				self.btn_master_23.setIcon(icon)
			elif i == 24:
				self.btn_master_24.setIcon(icon)
			elif i == 25:
				self.btn_master_25.setIcon(icon)
			else:
				QMessageBox.about(self, "警 告", "当前类别魔术礼装数目过多, 请联系作者修改程序")
				return

if __name__ == '__main__':
	app = QApplication(sys.argv)
	# 实例化子窗口
	selectmaster = Ui_SelectMaster()
	selectmaster.show()
	sys.exit(app.exec_())



