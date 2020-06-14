import sys
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, pyqtSignal
from battle_config import Servant, Enemy
import SelectLevelUi
import pandas as pd
import os


class Ui_SelectLevel(QDialog, SelectLevelUi.Ui_Dialog):
	my_Signal = pyqtSignal(pd.DataFrame)
	def __init__(self):
		super(Ui_SelectLevel, self).__init__()
		# QDialog.__init__(self)
		# SelectServantUi.Ui_Dialog.__init__(self)
		self.setupUi(self)

		self.emit_data = pd.DataFrame()

		# 职阶转化表
		self.class_dict = {'剑': 'Saber', '弓': 'Archer', '枪': 'Lancer', '骑': 'Rider', '术': 'Caster', '狂': 'Berserker',
							'杀': 'Assassin', '月': 'Mooncancer', '他': 'Alterego', '仇': 'Avenger', '降': 'Foreigner',
							'裁': 'Ruler', '盾': 'Shielder'}
		# 储存信息表
		self.battle_config_data = [{} for _ in range(9)]

		# 导入关卡配置
		df_all = pd.DataFrame()

		# 导入Free本
		path = r'data/level/Free'
		all_list = os.listdir(path)
		df1 = pd.DataFrame()
		for i in all_list:
			if i.endswith('.csv'):
				df = pd.read_csv(path + "/" + i, encoding="utf-8")
				df1 = df1.append(df, ignore_index=True)
		df1['活动'] = '主线自由关卡'
		df_all = df_all.append(df1, ignore_index=True)

		# 导入加勒底之门副本
		path = r'data/level/ChaldeaGate'
		all_list = os.listdir(path)
		df1 = pd.DataFrame()
		for i in all_list:
			if i.endswith('.csv'):
				df = pd.read_csv(path + "/" + i)
				df1 = df1.append(df, ignore_index=True)
		df1['活动'] = '加勒底之门'
		df1 = df1.rename(columns={'名称cn': '地点cn', '名称jp': '地点jp'})

		df_all = df_all.append(df1, ignore_index=True)
		df_all = df_all.fillna('')
		self.level_data = df_all

		# 导入活动本
		path = r'data/level/Event'
		all_list = os.listdir(path)
		df1 = pd.DataFrame()
		for i in all_list:
			if i.endswith('.csv'):
				df = pd.read_csv(path + "/" + i)
				df = df.rename(columns={'名称cn': '地点cn', '名称jp': '地点jp'})
				df1 = df1.append(df, ignore_index=True)
		df1['活动'] = '活动周回本'


		df_all = df_all.append(df1, ignore_index=True)
		df_all = df_all.fillna('')
		self.level_data = df_all

		# 绑定按钮
		self.box_choose_event.activated.connect(self.event_change)
		self.box_choose_section.activated.connect(self.section_change)
		self.box_choose_level.activated.connect(self.level_change)
		self.box_choose_level_sub.activated.connect(self.sub_level_change)
		self.btn_confirm.clicked.connect(self.confirm)

		# 敌人数据
		df = pd.read_csv('data/enemy/enemy_data_basic.csv')
		df = df.fillna('')
		df.loc[df['特性'] != '', '特性'] = df['隐藏属性'] + ',' + df['特性']
		df.loc[df['特性'] == '', '特性'] = df['隐藏属性']
		df = df[['中文名', '隐藏属性', '特性']]
		self.enemy_data = df

		# 从者数据
		df = pd.DataFrame(columns=['序号', '中文名', '职阶'])
		with open('data/servant/servant_list.txt', encoding='utf-8-sig') as f:
			data = f.read()
		lines = data.split('\n')
		for line in lines:
			servant = line.split(',')
			if servant[9] == '无法获得':
				continue
			dict1 = {'序号': servant[0], '中文名': servant[5], '职阶': servant[12]}
			df = df.append(dict1, ignore_index=True)
		self.servant_data = df

		# 初始化列表
		df = self.level_data
		df1 = df[['活动']]
		df1 = df1.drop_duplicates()
		for x in df1.values:
			self.box_choose_event.addItem(x[0])
		self.event_change()

	def confirm(self):
		self.sendEditContent()
		self.close()

	def sendEditContent(self):
		self.save_level()
		self.my_Signal.emit(self.emit_data)

	def event_change(self):
		event = self.box_choose_event.currentText()
		df = self.level_data
		df1 = df[df['活动'] == event]
		df1 = df1['章名称']
		df1 = df1.drop_duplicates()
		self.box_choose_section.clear()
		for x in df1.values:
			# print(x)
			self.box_choose_section.addItem(x)
		self.section_change()

	def section_change(self):
		event = self.box_choose_event.currentText()
		section = self.box_choose_section.currentText()
		df = self.level_data
		df1 = df[df['活动'] == event]
		df2 = df1[df1['章名称'] == section]
		df2 = df2['地点cn']
		df2 = df2.drop_duplicates()
		self.box_choose_level.clear()
		for x in df2.values:
			# print(x)
			self.box_choose_level.addItem(x)
		self.level_change()

	def level_change(self):
		event = self.box_choose_event.currentText()
		section = self.box_choose_section.currentText()
		level = self.box_choose_level.currentText()
		df = self.level_data
		df1 = df[df['活动'] == event]
		df2 = df1[df1['章名称'] == section]
		df3 = df2[df2['地点cn'] == level]
		df3 = df3['级别']
		df3 = df3.drop_duplicates()
		self.box_choose_level_sub.clear()
		for x in df3.values:
			# print(x)
			self.box_choose_level_sub.addItem(x)
		self.sub_level_change()

	def sub_level_change(self):
		self.show_level()

	def set_enemy_data(self, enemy_list):
		name = enemy_list[1]
		enemy_class = self.class_dict[enemy_list[3]]
		type = enemy_list[2]
		health = enemy_list[5]
		np_type = 1
		pic_path = './pic/enemy_logo/' + name + '_头像.png'
		for text1 in ['骷髅兵', '龙牙兵', '僵尸', '鬼魂', '七人御佐姬', '雾绘', '忌灵']:
			if text1 in name:
				np_type = 2
				break

		if '_' in name:
			a = name.index('_')
			name1 = name[0: a]
		else:
			name1 = name

		dict1 = {'序号': 0, '中文名': name, '职阶': enemy_class, '类别': type, 'NP敌补正': np_type, '血量': health, '图片路径': pic_path}
		return dict1

	def set_servant_data(self, enemy_list):
		name = enemy_list[1]
		type = enemy_list[2]
		enemy_class = self.class_dict[enemy_list[3]]
		health = enemy_list[5]
		np_type = 1

		df = self.servant_data
		df = df[df['中文名'] == name]

		if len(df) > 0:
			df1 = df[df['职阶'] == enemy_class]
			if len(df1) == 1:
				servant_id = df1['序号'].values[0]
			else:
				servant_id = df['序号'].values[0]
		else:
			servant_id = 0

		pic_path = 'pic/servant_logo/Servant' + str(servant_id).zfill(3) + '.jpg'
		dict1 = {'序号': servant_id, '中文名': name, '职阶': enemy_class, '类别': type, 'NP敌补正': np_type, '血量': health, '图片路径': pic_path}
		return dict1

	def show_enemy_data(self, enemy_list):
		np_type = 1
		name = enemy_list[1]
		if '_' in name:
			name = name[0:name.index('_')]
		type = enemy_list[2]
		enemy_class = self.class_dict[enemy_list[3]]
		health = enemy_list[5]
		# 首先, 如果已经确认了为从者/影从者, 则直接设定
		if type == '从者' or type == '影从者':
			dict1 = self.set_servant_data(enemy_list)
		elif type == '小怪':
			dict1 = self.set_enemy_data(enemy_list)
		else:
			# 否则,需要判断敌人为小兵还是从者
			df = self.servant_data
			df_servant = df[df['中文名'] == name]
			df = self.enemy_data
			df_enemy = df[df['中文名'] == name]
			if len(df_servant) == 0 and len(df_enemy) > 0:
				# 此时说明是小怪
				dict1 = self.set_enemy_data(enemy_list)
			elif len(df_servant) > 0 and len(df_enemy) == 0:
				# 此时说明是从者
				dict1 = self.set_servant_data(enemy_list)
			elif len(df_servant) > 0 and len(df_enemy) > 0:
				# 此时说明存在歧义, 默认为小怪,不过需要手动确认
				dict1 = self.set_enemy_data(enemy_list)
				print('存在歧义', dict1['中文名'])
			else:
				# 说明该从者不存在, 请录入从者信息
				print(name, '不存在')
				dict1 = {'序号': 0, '中文名': '', '职阶': enemy_class, '类别': type, 'NP敌补正': 1, '血量': health, '图片路径': ''}
		return dict1

	def show_level(self):
		self.battle_config_data = [{} for _ in range(9)]
		event = self.box_choose_event.currentText()
		section = self.box_choose_section.currentText()
		level = self.box_choose_level.currentText()
		sub_level = self.box_choose_level_sub.currentText()
		df = self.level_data

		df1 = df[df['活动'] == event]
		df1 = df1[df1['章名称'] == section]
		df1 = df1[df1['地点cn'] == level]
		df1 = df1[df1['级别'] == sub_level]
		df_level = df1.fillna('')
		# print(df_level)
		self.pic_round1_enemy1.setPixmap(QPixmap())
		self.pic_round1_enemy2.setPixmap(QPixmap())
		self.pic_round1_enemy3.setPixmap(QPixmap())
		self.pic_round2_enemy1.setPixmap(QPixmap())
		self.pic_round2_enemy2.setPixmap(QPixmap())
		self.pic_round2_enemy3.setPixmap(QPixmap())
		self.pic_round3_enemy1.setPixmap(QPixmap())
		self.pic_round3_enemy2.setPixmap(QPixmap())
		self.pic_round3_enemy3.setPixmap(QPixmap())

		self.pic_round1_enemy1.setScaledContents(True)
		self.pic_round1_enemy2.setScaledContents(True)
		self.pic_round1_enemy3.setScaledContents(True)
		self.pic_round2_enemy1.setScaledContents(True)
		self.pic_round2_enemy2.setScaledContents(True)
		self.pic_round2_enemy3.setScaledContents(True)
		self.pic_round3_enemy1.setScaledContents(True)
		self.pic_round3_enemy2.setScaledContents(True)
		self.pic_round3_enemy3.setScaledContents(True)

		self.label_round1_enemy1.setText('')
		self.label_round1_enemy2.setText('')
		self.label_round1_enemy3.setText('')
		self.label_round2_enemy1.setText('')
		self.label_round2_enemy2.setText('')
		self.label_round2_enemy3.setText('')
		self.label_round3_enemy1.setText('')
		self.label_round3_enemy2.setText('')
		self.label_round3_enemy3.setText('')
		self.line_battle_ground.setText('')

		self.round1_enemy1_np_type.setCheckState(0)
		self.round1_enemy2_np_type.setCheckState(0)
		self.round1_enemy3_np_type.setCheckState(0)
		self.round2_enemy1_np_type.setCheckState(0)
		self.round2_enemy2_np_type.setCheckState(0)
		self.round2_enemy3_np_type.setCheckState(0)
		self.round3_enemy1_np_type.setCheckState(0)
		self.round3_enemy2_np_type.setCheckState(0)
		self.round3_enemy3_np_type.setCheckState(0)

		self.round1_enemy1_np_type.setEnabled(False)
		self.round1_enemy2_np_type.setEnabled(False)
		self.round1_enemy3_np_type.setEnabled(False)
		self.round2_enemy1_np_type.setEnabled(False)
		self.round2_enemy2_np_type.setEnabled(False)
		self.round2_enemy3_np_type.setEnabled(False)
		self.round3_enemy1_np_type.setEnabled(False)
		self.round3_enemy2_np_type.setEnabled(False)
		self.round3_enemy3_np_type.setEnabled(False)
		text = df_level['关卡特性'].values[0]
		text = text.replace('无,', '')
		text = text.strip(',')
		self.line_battle_ground.setText(text)

		for i in range(1, 4):
			for j in range(1, 4):
				enemy_order = str(i)+'敌人'+str(j)
				enemy = df_level[enemy_order].values[0]
				if "}" in enemy:
					enemy = enemy[0: enemy.index('}')]
					print('发现重复, 自动修正', section, level)

				if enemy != '':
					enemy_list = enemy.split('|')
					name = enemy_list[1]
					type = enemy_list[2]
					if enemy_list[3] in self.class_dict:
						enemy_class = self.class_dict[enemy_list[3]]
					else:
						enemy_class = 'Shielder'
						QMessageBox.warning(self, '警告', '无法识别以下从者职介, 请检查数据格式, 如为新职介, 请与作者联系\n' + enemy)
					health = enemy_list[5]
					if not health.isdigit():
						QMessageBox.warning(self, '警告', '无法识别以下从者血量, 请检查数据格式\n' + enemy)
					text = '中文名: ' + name +'\n' + '职阶: ' + enemy_class +'\n' + '类别: ' + type +'\n' + '血量: ' + health

					dict1 = self.show_enemy_data(enemy_list)
					pic_path = dict1['图片路径']
					np_type = dict1['NP敌补正']
					if event == 'BATTLE IN NEWYORK 2020':
						np_type = 1
					# 将数据保存起来
					num = 3 * (i - 1) + (j - 1)
					self.battle_config_data[num] = dict1

					if i == 1 and j == 1:
						box_np_type = self.round1_enemy1_np_type
						self.pic_round1_enemy1.setPixmap(QPixmap(pic_path))
						self.label_round1_enemy1.setText(text)
					elif i == 1 and j == 2:
						box_np_type = self.round1_enemy2_np_type
						self.pic_round1_enemy2.setPixmap(QPixmap(pic_path))
						self.label_round1_enemy2.setText(text)
					elif i == 1 and j == 3:
						box_np_type = self.round1_enemy3_np_type
						self.pic_round1_enemy3.setPixmap(QPixmap(pic_path))
						self.label_round1_enemy3.setText(text)
					elif i == 2 and j == 1:
						box_np_type = self.round2_enemy1_np_type
						self.pic_round2_enemy1.setPixmap(QPixmap(pic_path))
						self.label_round2_enemy1.setText(text)
					elif i == 2 and j == 2:
						box_np_type = self.round2_enemy2_np_type
						self.pic_round2_enemy2.setPixmap(QPixmap(pic_path))
						self.label_round2_enemy2.setText(text)
					elif i == 2 and j == 3:
						box_np_type = self.round2_enemy3_np_type
						self.pic_round2_enemy3.setPixmap(QPixmap(pic_path))
						self.label_round2_enemy3.setText(text)
					elif i == 3 and j == 1:
						box_np_type = self.round3_enemy1_np_type
						self.pic_round3_enemy1.setPixmap(QPixmap(pic_path))
						self.label_round3_enemy1.setText(text)
					elif i == 3 and j == 2:
						box_np_type = self.round3_enemy2_np_type
						self.pic_round3_enemy2.setPixmap(QPixmap(pic_path))
						self.label_round3_enemy2.setText(text)
					elif i == 3 and j == 3:
						box_np_type = self.round3_enemy3_np_type
						self.pic_round3_enemy3.setPixmap(QPixmap(pic_path))
						self.label_round3_enemy3.setText(text)
					else:
						continue

					box_np_type.setEnabled(True)
					if np_type == 2:
						box_np_type.setCheckState(2)
					else:
						box_np_type.setCheckState(0)

	def save_level(self):
		df_enemy_data = pd.DataFrame()
		for i in range(1, 4):
			for j in range(1, 4):
				# 获取NP补正
				if i == 1 and j == 1:
					box_np_type = self.round1_enemy1_np_type
				elif i == 1 and j == 2:
					box_np_type = self.round1_enemy2_np_type
				elif i == 1 and j == 3:
					box_np_type = self.round1_enemy3_np_type
				elif i == 2 and j == 1:
					box_np_type = self.round2_enemy1_np_type
				elif i == 2 and j == 2:
					box_np_type = self.round2_enemy2_np_type
				elif i == 2 and j == 3:
					box_np_type = self.round2_enemy3_np_type
				elif i == 3 and j == 1:
					box_np_type = self.round3_enemy1_np_type
				elif i == 3 and j == 2:
					box_np_type = self.round3_enemy2_np_type
				elif i == 3 and j == 3:
					box_np_type = self.round3_enemy3_np_type
				else:
					continue
				dict_np_type = {0: 1, 2: 2}
				np_type = dict_np_type[box_np_type.checkState()]
				num = 3 * (i - 1) + (j - 1)
				dict1 = self.battle_config_data[num]
				# dict1)
				if len(dict1) > 0:
					dict1.update({'回合': i, '位置': j, 'NP敌补正': np_type})
					df_enemy_data = df_enemy_data.append(dict1, ignore_index=True)
		text = self.line_battle_ground.text()
		typo_list = ["'", '"', ' ', '/', ':', ';', '，', '。', '；', '：', '.']
		for typo in typo_list:
			if typo in text:
				text = text.replace(typo, ',')
		while ',,' in text:
			text = text.replace(',,', ',')
		text = text.strip(',')
		df_enemy_data['关卡特性'] = text
		# print(df_enemy_data)
		self.emit_data = df_enemy_data

	# 根据字典设定从者
	def set_enemy(self, dict1):
		# dict1 = {'序号': servant_id, '中文名': name, '职阶': enemy_class, 'NP敌补正': np_type, '血量': health, '图片路径': pic_path}
		name = dict1['中文名']
		enemy_class = dict1['职阶']
		health = int(dict1['血量'])
		np_type = dict1['NP敌补正']
		pic_path = dict1['图片路径']
		role_id = int(dict1['序号'])
		if role_id == 0:
			df = self.enemy_data
			df = df[df['中文名'] == name]
			if len(df) > 0:
				attribute = df['特性'].values[0]
				class_hide = df['隐藏属性'].values[0]
			else:
				attribute = ''
				class_hide = '星'
			attribute = enemy_class + ',' + attribute
			attribute = attribute.strip(',')
			attribute = attribute.replace(',,', ',')
			role = Enemy(name=name, enemy_attribute=attribute, enemy_class=enemy_class, enemy_class_hide=class_hide,
			             enemy_np_type=np_type, health=health, pic_path=pic_path)
		elif role_id > 0:
			role = Servant(order=0, servant_id=role_id, enemy_np_type=np_type)
			# print(role.name)
			role.health = health
			role.health_start = health
			role.class_target_role = enemy_class
			print(role.attribute)
			if dict1['类别'] == '影从者':
				# print(role.attribute)
				role.attribute.append('影从者')
		else:
			role = Enemy()
		role.order = int(dict1['位置'])
		return role


if __name__ == '__main__':
	app = QApplication(sys.argv)
	# 实例化子窗口
	selectservant = Ui_SelectLevel()
	selectservant.show()
	sys.exit(app.exec_())



