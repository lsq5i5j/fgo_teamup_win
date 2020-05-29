import sys
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import pyqtSignal
import SelectServantUi
import pandas as pd


class Ui_SelectServant(QDialog, SelectServantUi.Ui_Dialog):
	my_Signal = pyqtSignal(dict)

	def __init__(self):
		super(Ui_SelectServant, self).__init__()
		# QDialog.__init__(self)
		# SelectServantUi.Ui_Dialog.__init__(self)
		self.setupUi(self)
		self.update_servant_list()
		df = pd.read_csv('data/save/servant_data_save.csv')
		self.servant_data = df[['序号', '稀有度', '中文名', '职阶', '圣杯', '芙芙', '宝具数', '1技能', '2技能', '3技能']]
		self.chosen_class = 'Saber'
		self.chosen_rarity = '5stars'
		self.chosen_list = []
		self.servant_list()
		self.servant_display()
		self.chosen_servant_id = 0
		self.chosen_servant_name = ''
		self.chosen_servant_rarity = 0
		self.chosen_servant_class = ''
		self.chosen_servant_holygrail = 0
		self.chosen_servant_level = 0
		self.chosen_servant_np = 0
		self.chosen_servant_skill1 = 10
		self.chosen_servant_skill2 = 10
		self.chosen_servant_skill3 = 10
		self.chosen_servant_fufu = 1000
		self.choose_servant(1)

		# 设定滑块功能
		self.bar_servant_holygrail.valueChanged.connect(lambda: self.change_value())
		self.bar_servant_np.valueChanged.connect(lambda: self.change_value())
		self.bar_servant_skill1.valueChanged.connect(lambda: self.change_value())
		self.bar_servant_skill2.valueChanged.connect(lambda: self.change_value())
		self.bar_servant_skill3.valueChanged.connect(lambda: self.change_value())
		self.bar_servant_fufu.valueChanged.connect(lambda: self.change_value())

		# 设定基本功能
		self.btn_confirm.clicked.connect(lambda: self.servant_confirm())
		self.btn_cancel.clicked.connect(self.close)
		self.btn_data_reset.clicked.connect(lambda: self.reset_data())
		self.btn_data_output.clicked.connect(lambda: self.save_data_local())
		self.btn_clear.clicked.connect(lambda: self.servant_clear())

		# 设置选择从者
		self.btn_saber.clicked.connect(lambda: self.set_servant_class('Saber'))
		self.btn_archer.clicked.connect(lambda: self.set_servant_class('Archer'))
		self.btn_lancer.clicked.connect(lambda: self.set_servant_class('Lancer'))
		self.btn_rider.clicked.connect(lambda: self.set_servant_class('Rider'))
		self.btn_caster.clicked.connect(lambda: self.set_servant_class('Caster'))
		self.btn_assassin.clicked.connect(lambda: self.set_servant_class('Assassin'))
		self.btn_berserker.clicked.connect(lambda: self.set_servant_class('Berserker'))
		self.btn_extra.clicked.connect(lambda: self.set_servant_class('Extra'))

		self.btn_5stars.clicked.connect(lambda: self.set_servant_rarity('5stars'))
		self.btn_4stars.clicked.connect(lambda: self.set_servant_rarity('4stars'))
		self.btn_lowstars.clicked.connect(lambda: self.set_servant_rarity('lowstars'))

		self.btn_servant_1.clicked.connect(lambda: self.choose_servant(1))
		self.btn_servant_2.clicked.connect(lambda: self.choose_servant(2))
		self.btn_servant_3.clicked.connect(lambda: self.choose_servant(3))
		self.btn_servant_4.clicked.connect(lambda: self.choose_servant(4))
		self.btn_servant_5.clicked.connect(lambda: self.choose_servant(5))
		self.btn_servant_6.clicked.connect(lambda: self.choose_servant(6))
		self.btn_servant_7.clicked.connect(lambda: self.choose_servant(7))
		self.btn_servant_8.clicked.connect(lambda: self.choose_servant(8))
		self.btn_servant_9.clicked.connect(lambda: self.choose_servant(9))
		self.btn_servant_10.clicked.connect(lambda: self.choose_servant(10))
		self.btn_servant_11.clicked.connect(lambda: self.choose_servant(11))
		self.btn_servant_12.clicked.connect(lambda: self.choose_servant(12))
		self.btn_servant_13.clicked.connect(lambda: self.choose_servant(13))
		self.btn_servant_14.clicked.connect(lambda: self.choose_servant(14))
		self.btn_servant_15.clicked.connect(lambda: self.choose_servant(15))
		self.btn_servant_16.clicked.connect(lambda: self.choose_servant(16))
		self.btn_servant_17.clicked.connect(lambda: self.choose_servant(17))
		self.btn_servant_18.clicked.connect(lambda: self.choose_servant(18))
		self.btn_servant_19.clicked.connect(lambda: self.choose_servant(19))
		self.btn_servant_20.clicked.connect(lambda: self.choose_servant(20))
		self.btn_servant_21.clicked.connect(lambda: self.choose_servant(21))
		self.btn_servant_22.clicked.connect(lambda: self.choose_servant(22))
		self.btn_servant_23.clicked.connect(lambda: self.choose_servant(23))
		self.btn_servant_24.clicked.connect(lambda: self.choose_servant(24))
		self.btn_servant_25.clicked.connect(lambda: self.choose_servant(25))
		self.btn_servant_26.clicked.connect(lambda: self.choose_servant(26))
		self.btn_servant_27.clicked.connect(lambda: self.choose_servant(27))
		self.btn_servant_28.clicked.connect(lambda: self.choose_servant(28))
		self.btn_servant_29.clicked.connect(lambda: self.choose_servant(29))
		self.btn_servant_30.clicked.connect(lambda: self.choose_servant(30))

		self.btn_kongming.clicked.connect(lambda: self.choose_servant_fast(37))
		self.btn_merlin.clicked.connect(lambda: self.choose_servant_fast(150))
		self.btn_cba.clicked.connect(lambda: self.choose_servant_fast(215))
		self.btn_tamamo.clicked.connect(lambda: self.choose_servant_fast(62))
		self.btn_nero_bride.clicked.connect(lambda: self.choose_servant_fast(90))

	def update_servant_list(self):
		with open('data/servant/servant_list.txt', 'r', encoding='utf-8-sig') as f:
			data = f.read()
		servant_list = data.split('\n')
		try:
			df_save = pd.read_csv('data/save/servant_data_save.csv')
		except IOError:
			df_save = pd.DataFrame(columns=['序号', '稀有度', '中文名', '职阶', '圣杯', '芙芙', '宝具数', '1技能', '2技能', '3技能'])
		try:
			df_save_bk = pd.read_csv('data/servant/servant_data_save_bk.csv')
		except IOError:
			df_save_bk = pd.DataFrame(columns=['序号', '稀有度', '中文名', '职阶', '圣杯', '芙芙', '宝具数', '1技能', '2技能', '3技能'])
		for item in servant_list:
			servant = item.split(',')
			servant_id = int(servant[0])
			servant_rarity = int(servant[1])
			servant_name = servant[5]
			servant_class = servant[12]
			if servant[9] == '无法获得':
				continue
			dict1 = {'序号': servant_id,
			         '稀有度': servant_rarity,
			         '中文名': servant_name,
			         '职阶': servant_class,
			         '圣杯': 0,
			         '芙芙': 1000,
			         '宝具数': 1,
			         '1技能': 10,
			         '2技能': 10,
			         '3技能': 10}
			if '活动赠送' in servant[9] or servant_rarity <= 3:
				dict1.update({'宝具数': 5})

			df = df_save[df_save['序号'] == servant_id]
			if len(df) == 0:
				df_save = df_save.append(dict1,ignore_index=True)
				df_save = df_save.sort_values(by='序号')
				print('更新', servant_name)

			df = df_save_bk[df_save_bk['序号'] == servant_id]
			if len(df) == 0:
				df_save_bk = df_save_bk.append(dict1, ignore_index=True)
				df_save_bk = df_save_bk.sort_values(by='序号')
				print('更新', servant_name)
		df_save.to_csv('./data/save/servant_data_save.csv', encoding='utf-8-sig', index=False)
		df_save_bk.to_csv('./data/servant/servant_data_save_bk.csv', encoding='utf-8-sig', index=False)

	# 让多窗口之间传递信号 刷新主窗口信息
	def sendEditContent(self):
		content = {
			'ID': self.chosen_servant_id,
			'等级': self.chosen_servant_level,
			'宝具数': self.chosen_servant_np,
			'技能': [self.chosen_servant_skill1, self.chosen_servant_skill2, self.chosen_servant_skill3],
			'芙芙': self.chosen_servant_fufu,
			'职阶': self.chosen_class,
			'稀有度':self.chosen_rarity}
		self.my_Signal.emit(content)

	def save_data(self):
		self.chosen_servant_np = self.bar_servant_np.value()
		self.chosen_servant_holygrail = self.bar_servant_holygrail.value()
		self.chosen_servant_skill1 = self.bar_servant_skill1.value()
		self.chosen_servant_skill2 = self.bar_servant_skill2.value()
		self.chosen_servant_skill3 = self.bar_servant_skill3.value()
		self.chosen_servant_fufu = self.bar_servant_fufu.value()*10
		# 计算等级
		if self.chosen_servant_id == 1:
			# 学妹专属
			level_list = (80, )
		elif self.chosen_servant_rarity == 5:
			level_list = (90, 92, 94, 96, 98, 100)
		elif self.chosen_servant_rarity == 4:
			level_list = (80, 85, 90, 92, 94, 96, 98, 100)
		elif self.chosen_servant_rarity == 3:
			level_list = (70, 75, 80, 85, 90, 92, 94, 96, 98, 100)
		elif self.chosen_servant_rarity == 2:
			level_list = (65, 70, 75, 80, 85, 90, 92, 94, 96, 98, 100)
		elif self.chosen_servant_rarity == 1:
			level_list = (60, 70, 75, 80, 85, 90, 92, 94, 96, 98, 100)
		else:
			# 小安专属
			level_list = (65, 70, 75, 80, 85, 90, 92, 94, 96, 98, 100)
		self.chosen_servant_level = level_list[self.chosen_servant_holygrail]

		df = self.servant_data
		df1 = df[df['序号'] == self.chosen_servant_id]
		row_name = df1._stat_axis.values.tolist()
		self.servant_data.loc[row_name, ['宝具数']] = self.chosen_servant_np
		self.servant_data.loc[row_name, ['圣杯']] = self.chosen_servant_holygrail
		self.servant_data.loc[row_name, ['3技能']] = self.chosen_servant_skill3
		self.servant_data.loc[row_name, ['1技能']] = self.chosen_servant_skill1
		self.servant_data.loc[row_name, ['2技能']] = self.chosen_servant_skill2
		self.servant_data.loc[row_name, ['3技能']] = self.chosen_servant_skill3
		self.servant_data.loc[row_name, ['芙芙']] = self.chosen_servant_fufu

	def save_data_local(self):
		self.save_data()
		df = self.servant_data
		df.to_csv('./data/save/servant_data_save.csv', encoding='utf-8-sig', index=False)
		QMessageBox.information(self, '提 醒', '当前从者数据已保存到本地', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

	def reset_data(self):
		reply = QMessageBox.question(self, '警 告', '还原数据会删除已保存的所有从者数据，是否继续？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

		if reply == QMessageBox.Yes:
			df = pd.read_csv('data/servant/servant_data_save_bk.csv', encoding='utf-8-sig')
			self.servant_data = df[['序号', '稀有度', '中文名', '职阶', '圣杯', '芙芙', '宝具数', '1技能', '2技能', '3技能']]
			self.servant_data.to_csv('./data/save/servant_data_save.csv', encoding='utf-8-sig', index=False)
			self.set_servant_data()
			self.display_servant_data()
			QMessageBox.information(self, '提 醒', '从者数据已还原', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

	def servant_confirm(self):
		self.save_data()
		self.sendEditContent()
		self.close()

	def servant_clear(self):
		self.chosen_servant_id = 0
		self.sendEditContent()
		self.close()

	def choose_servant(self, number):
		if number <= len(self.chosen_list):
			self.chosen_servant_id = self.chosen_list[number-1]
			# 设定从者数据
			self.set_servant_data()
			# 显示数据
			self.display_servant_data()

	def choose_servant_fast(self, number):
		self.chosen_servant_id = number
		# 设定从者数据
		self.set_servant_data()

		# 设定从者数据
		df = self.servant_data
		df1 = df[df['序号'] == number]
		self.chosen_class = df1['职阶'].values[0]
		if df1['稀有度'].values[0] == 5:
			self.chosen_rarity = '5stars'
		elif df1['稀有度'].values[0] == 4:
			self.chosen_rarity = '4stars'
		else:
			self.chosen_rarity = 'lowstars'
		# 显示数据
		self.servant_display()
		self.display_servant_data()

	def set_servant_data(self):
		if self.chosen_servant_id != 0:
			df = self.servant_data

			df1 = df[df['序号'] == self.chosen_servant_id]
			self.chosen_servant_name = df1['中文名'].values[0]
			self.chosen_servant_rarity = df1['稀有度'].values[0]
			self.chosen_servant_class = df1['职阶'].values[0]
			self.chosen_servant_np = df1['宝具数'].values[0]
			self.chosen_servant_holygrail = df1['圣杯'].values[0]
			self.chosen_servant_skill1 = df1['1技能'].values[0]
			self.chosen_servant_skill2 = df1['2技能'].values[0]
			self.chosen_servant_skill3 = df1['3技能'].values[0]
			self.chosen_servant_fufu = df1['芙芙'].values[0]

	def change_value(self):
		servant_np = self.bar_servant_np.value()
		servant_holygrail = self.bar_servant_holygrail.value()
		servant_skill1 = self.bar_servant_skill1.value()
		servant_skill2 = self.bar_servant_skill2.value()
		servant_skill3 = self.bar_servant_skill3.value()
		servant_fufu = self.bar_servant_fufu.value()*10
		# 计算等级
		if self.chosen_servant_id == 1:
			# 学妹专属
			level_list = (80, )
		elif self.chosen_servant_rarity == 5:
			level_list = (90, 92, 94, 96, 98, 100)
		elif self.chosen_servant_rarity == 4:
			level_list = (80, 85, 90, 92, 94, 96, 98, 100)
		elif self.chosen_servant_rarity == 3:
			level_list = (70, 75, 80, 85, 90, 92, 94, 96, 98, 100)
		elif self.chosen_servant_rarity == 2:
			level_list = (65, 70, 75, 80, 85, 90, 92, 94, 96, 98, 100)
		elif self.chosen_servant_rarity == 1:
			level_list = (60, 70, 75, 80, 85, 90, 92, 94, 96, 98, 100)
		else:
			# 小安专属
			level_list = (65, 70, 75, 80, 85, 90, 92, 94, 96, 98, 100)
		# 显示数据
		servant_level = level_list[servant_holygrail]
		self.label_servant_level.setText('等级(' + str(servant_level) + ')')
		self.label_servant_np.setText('宝具(' + str(servant_np) + ')')
		self.label_servant_skill1.setText('1技能(' + str(servant_skill1) + ')')
		self.label_servant_skill2.setText('2技能(' + str(servant_skill2) + ')')
		self.label_servant_skill3.setText('3技能(' + str(servant_skill3) + ')')
		self.label_servant_skill3.setText('3技能(' + str(servant_skill3) + ')')
		self.label_servant_fufu.setText('芙芙(' + str(servant_fufu) + ')')

	def display_servant_data(self):
		if self.chosen_servant_id != 0:
			if self.chosen_servant_id == 1:
				# 学妹专属
				level_list = (80, )
				self.bar_servant_holygrail.setMaximum(0)
			elif self.chosen_servant_rarity == 5:
				level_list = (90, 92, 94, 96, 98, 100)
				self.bar_servant_holygrail.setMaximum(5)
			elif self.chosen_servant_rarity == 4:
				self.bar_servant_holygrail.setMaximum(7)
				level_list = (80, 85, 90, 92, 94, 96, 98, 100)
			elif self.chosen_servant_rarity == 3:
				self.bar_servant_holygrail.setMaximum(9)
				level_list = (70, 75, 80, 85, 90, 92, 94, 96, 98, 100)
			elif self.chosen_servant_rarity == 2:
				self.bar_servant_holygrail.setMaximum(10)
				level_list = (65, 70, 75, 80, 85, 90, 92, 94, 96, 98, 100)
			elif self.chosen_servant_rarity == 1:
				self.bar_servant_holygrail.setMaximum(10)
				level_list = (60, 70, 75, 80, 85, 90, 92, 94, 96, 98, 100)
			else:
				# 小安专属
				self.bar_servant_holygrail.setMaximum(10)
				level_list = (65, 70, 75, 80, 85, 90, 92, 94, 96, 98, 100)

			self.chosen_servant_level = level_list[int(self.chosen_servant_holygrail)]
			# 显示设置的数据
			pix = QPixmap("./pic/servant_logo/servant" + str(self.chosen_servant_id).zfill(3) + ".jpg")
			self.label_servant_pic.setPixmap(pix)
			self.label_servant_pic.setScaledContents(True)
			self.label_servant_level.setText('等级('+str(self.chosen_servant_level)+')')
			self.label_servant_np.setText('宝具('+str(self.chosen_servant_np)+')')
			self.label_servant_skill1.setText('1技能(' + str(self.chosen_servant_skill1) + ')')
			self.label_servant_skill2.setText('2技能(' + str(self.chosen_servant_skill2) + ')')
			self.label_servant_skill3.setText('3技能(' + str(self.chosen_servant_skill3) + ')')
			self.label_servant_fufu.setText('芙芙(' + str(self.chosen_servant_fufu) + ')')
			self.bar_servant_holygrail.setValue(self.chosen_servant_holygrail)
			self.bar_servant_np.setValue(self.chosen_servant_np)
			self.bar_servant_skill1.setValue(self.chosen_servant_skill1)
			self.bar_servant_skill2.setValue(self.chosen_servant_skill2)
			self.bar_servant_skill3.setValue(self.chosen_servant_skill3)
			self.bar_servant_fufu.setValue(self.chosen_servant_fufu/10)

	def set_servant_class(self, servant_class):
		self.chosen_class = servant_class
		self.servant_display()

	def set_servant_rarity(self, servant_rarity):
		self.chosen_rarity = servant_rarity
		self.servant_display()

	def set_icon(self, i, icon):
		if i == 0:
			self.btn_servant_1.setIcon(icon)
		elif i == 1:
			self.btn_servant_2.setIcon(icon)
		elif i == 2:
			self.btn_servant_3.setIcon(icon)
		elif i == 3:
			self.btn_servant_4.setIcon(icon)
		elif i == 4:
			self.btn_servant_5.setIcon(icon)
		elif i == 5:
			self.btn_servant_6.setIcon(icon)
		elif i == 6:
			self.btn_servant_7.setIcon(icon)
		elif i == 7:
			self.btn_servant_8.setIcon(icon)
		elif i == 8:
			self.btn_servant_9.setIcon(icon)
		elif i == 9:
			self.btn_servant_10.setIcon(icon)
		elif i == 10:
			self.btn_servant_11.setIcon(icon)
		elif i == 11:
			self.btn_servant_12.setIcon(icon)
		elif i == 12:
			self.btn_servant_13.setIcon(icon)
		elif i == 13:
			self.btn_servant_14.setIcon(icon)
		elif i == 14:
			self.btn_servant_15.setIcon(icon)
		elif i == 15:
			self.btn_servant_16.setIcon(icon)
		elif i == 16:
			self.btn_servant_17.setIcon(icon)
		elif i == 17:
			self.btn_servant_18.setIcon(icon)
		elif i == 18:
			self.btn_servant_19.setIcon(icon)
		elif i == 19:
			self.btn_servant_20.setIcon(icon)
		elif i == 20:
			self.btn_servant_21.setIcon(icon)
		elif i == 21:
			self.btn_servant_22.setIcon(icon)
		elif i == 22:
			self.btn_servant_23.setIcon(icon)
		elif i == 23:
			self.btn_servant_24.setIcon(icon)
		elif i == 24:
			self.btn_servant_25.setIcon(icon)
		elif i == 25:
			self.btn_servant_26.setIcon(icon)
		elif i == 26:
			self.btn_servant_27.setIcon(icon)
		elif i == 27:
			self.btn_servant_28.setIcon(icon)
		elif i == 28:
			self.btn_servant_29.setIcon(icon)
		elif i == 29:
			self.btn_servant_30.setIcon(icon)
		else:
			QMessageBox.about(self, "警 告", "当前类别从者数目过多, 请联系作者修改程序")
			return

	def servant_display(self):
		self.servant_list()
		for i in range(30):
			icon = QIcon()
			if i < len(self.chosen_list):
				icon.addPixmap(QPixmap("./pic/servant_logo/servant" + str(self.chosen_list[i]).zfill(3) + ".jpg"), QIcon.Normal, QIcon.Off)
			self.set_icon(i, icon)

	def servant_list(self):
		df = self.servant_data
		if self.chosen_class != 'Extra':
			df1 = df[df['职阶'] == self.chosen_class]
		else:
			df1 = df[df['职阶'] != 'Saber']
			df1 = df1[df1['职阶'] != 'Archer']
			df1 = df1[df1['职阶'] != 'Lancer']
			df1 = df1[df1['职阶'] != 'Rider']
			df1 = df1[df1['职阶'] != 'Caster']
			df1 = df1[df1['职阶'] != 'Assassin']
			df1 = df1[df1['职阶'] != 'Berserker']

		if self.chosen_rarity == '5stars':
			df2 = df1[df1['稀有度'] == 5]
		elif self.chosen_rarity == '4stars':
			df2 = df1[df1['稀有度'] == 4]
		else:
			df2 = df1[df1['稀有度'] != 5]
			df2 = df2[df2['稀有度'] != 4]
		df2 = df2[['序号']]
		if len(df2) > 0:
			self.chosen_list = [a[0] for a in df2.values]
		else:
			self.chosen_list = []


if __name__ == '__main__':
	app = QApplication(sys.argv)
	# 实例化子窗口
	selectservant = Ui_SelectServant()
	selectservant.show()
	sys.exit(app.exec_())



