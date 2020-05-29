import sys
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, pyqtSignal
from battle_config import Servant, Enemy, Master, BattleConfig
import ViewDetailsUi
import pandas as pd


class Ui_ViewDetails(QDialog, ViewDetailsUi.Ui_Dialog):
	def __init__(self):
		super(Ui_ViewDetails, self).__init__()
		self.setupUi(self)
		self.label_attribute.setWordWrap(True)
		self.label_details.setWordWrap(True)
		self.label_pic.setScaledContents(True)
		self.view_role_empty()

	def view_role_servant(self, battle_round, role):
		attribute = role.attribute
		state = role.state
		# 设置头像
		self.label_pic.setPixmap(QPixmap(role.pic_path))
		# 宝具
		text = '宝具类型: ' + role.np_type + ' | ' + role.np_color + '\n\n'
		np = role.np
		if len(np) > 0:
			text += '效果: ' + '\n'
		for name in np['宝具效果'].values:
			text += str(name) + '\n'
		text += '\n'
		# 输出 3 个技能
		for i in range(1, 4):
			if i == 1:
				skill = role.skill_1
			elif i == 2:
				skill = role.skill_2
			elif i == 3:
				skill = role.skill_3
			else:
				return

			text += '技能' + str(i) + ': \n'
			if len(skill) == 0:
				text += '效果暂不支持或对速刷无帮助\n'

			for i in skill[['技能效果', '幅度']].values:
				name = i[0]
				num = str(i[1])
				if '(' in name:
					a = name.rfind('(')
					name = name[0:a] + num + name[a:len(name)]
				else:
					name = name + num
				text += name + '\n'
			text += '\n'
		text = text.strip('\n')
		text = text.replace('nan', '')
		text = text.replace('\n\n\n', '\n\n')
		text = text.replace('\n\n\n', '\n\n')
		self.label_details.setText(text)
		# 输出从者特性
		text = ''
		for item in attribute:
			text += item + ', '
		text = text.strip(', ')
		self.label_attribute.setText(text)
		# 输出从者buff状态
		text_name = ' 状态 \n\n'
		text_num = ' 幅度 \n\n'
		text_times = ' 剩余次数 \n\n'
		text_round = ' 剩余回合 \n\n'
		print(state)
		for index, row in state.iterrows():
			if row['开始回合'] <= battle_round <= row['结束回合']:
				text_name += row['效果'] + '\n'
				text_num += row['幅度'] + '\n'
				if row['剩余次数'] > 10:
					text_times += '\n'
				else:
					text_times += str(int(row['剩余次数'])) + '\n'
				if row['结束回合'] > 10:
					text_round += '\n'
				else:
					text_round += str(int(row['结束回合']) - battle_round + 1) + '\n'

		text_times = text_times.replace('-1', '')
		text_round = text_round.replace('-1', '')
		self.label_state.setText(text_name.replace('nan', ''))
		self.label_state_num.setText(text_num.replace('nan', ''))
		self.label_state_times.setText(text_times.replace('nan', ''))
		self.label_state_round.setText(text_round.replace('nan', ''))

	def view_role_enemy(self, battle_round, role):
		attribute = role.attribute
		state = role.state
		# 设置头像
		self.label_pic.setPixmap(QPixmap(role.pic_path))
		# 设置敌人信息
		text = '初始血量: '
		text += str(role.health_start) + '\n\n'
		text += '现有血量: '
		text += str(int(round(role.health))) + '\n\n'
		text += '当前宝具伤害: '
		text += str(int(round(role.damage))) + '\n\n'
		text += '总计受到伤害: '
		text += str(int(round(role.damage_total))) + '\n\n'
		text += '死灵补正: '
		if role.enemy_np_type == 1:
			text += '否'
		else:
			text += '是'
		self.label_details.setText(text.replace('nan', ''))
		# 输出敌人特性
		text = ''
		for item in attribute:
			text += item + ', '
		text = text.strip(', ')
		self.label_attribute.setText(text)
		# 输出敌人buff状态
		text_name = ' 状态 \n\n'
		text_num = ' 幅度 \n\n'
		text_times = ' 剩余次数 \n\n'
		text_round = ' 剩余回合 \n\n'
		print(state)
		for index, row in state.iterrows():
			if row['开始回合'] <= battle_round <= row['结束回合']:
				text_name += row['效果'] + '\n'
				text_num += row['幅度'] + '\n'
				if row['剩余次数'] > 10:
					text_times += '\n'
				else:
					text_times += str(int(row['剩余次数'])) + '\n'
				if row['结束回合'] > 10:
					text_round += '\n'
				else:
					text_round += str(int(row['结束回合']) - battle_round + 1) + '\n'

		text_times = text_times.replace('-1', '')
		text_round = text_round.replace('-1', '')
		self.label_state.setText(text_name.replace('nan', ''))
		self.label_state_num.setText(text_num.replace('nan', ''))
		self.label_state_times.setText(text_times.replace('nan', ''))
		self.label_state_round.setText(text_round.replace('nan', ''))

	def view_role_master(self, battle_round, role):
		# 设置头像
		self.label_pic.setPixmap(QPixmap(role.pic_path))
		text = ''
		# 输出 3 个技能
		for i in range(1, 4):
			if i == 1:
				skill = role.skill_1
			elif i == 2:
				skill = role.skill_2
			elif i == 3:
				skill = role.skill_3
			else:
				return

			text += '技能' + str(i) + ': \n'
			if len(skill) == 0:
				text += '效果暂不支持或对速刷无帮助\n'

			for i in skill[['技能效果', '幅度']].values:
				name = i[0]
				num = str(i[1])
				if '(' in name:
					a = name.rfind('(')
					name = name[0:a] + num + name[a:len(name)]
				else:
					name = name + num
				text += name + '\n'
			text += '\n'
		text = text.strip('\n')
		text = text.replace('nan', '')
		text = text.replace('\n\n\n', '\n\n')
		text = text.replace('\n\n\n', '\n\n')
		self.label_details.setText(text)

		self.label_attribute.setText('')
		self.label_state.setText('')
		self.label_state_num.setText('')
		self.label_state_times.setText('')
		self.label_state_round.setText('')

	def view_role_empty(self):
		self.label_attribute.setText('')
		self.label_state.setText('')
		self.label_state_num.setText('')
		self.label_state_times.setText('')
		self.label_state_round.setText('')
		self.label_pic.setPixmap(QPixmap())
		self.label_details.setText('')

	def view_role(self, battle_round, role_type, role):
		if role_type == 'servant':
			if role.health > 0:
				self.view_role_servant(battle_round, role)
			else:
				self.view_role_empty()
		elif role_type == 'enemy':
			if role.health_start > 0:
				self.view_role_enemy(battle_round, role)
			else:
				self.view_role_empty()
		elif role_type == 'master':
			if role.order > 0:
				self.view_role_master(battle_round, role)
			else:
				self.view_role_empty()
		else:
			self.view_role_empty()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	# 实例化子窗口
	selectservant = Ui_ViewDetails()
	selectservant.show()

	bc = BattleConfig()
	bc.battle_ground = '燃烧'
	bc.servant_1 = Servant(order=1, servant_id=163, level=90, skill_level=(10, 10, 10), np_level=5)
	bc.servant_2 = Servant(order=2, servant_id=215, level=70, skill_level=(10, 10, 10), np_level=5)
	bc.servant_3 = Servant(order=3, servant_id=215, level=70, skill_level=(10, 10, 10), np_level=5)
	bc.enemy_11 = Enemy(enemy_class='Berserker', health=100)
	# bc.enemy_12 = enemy(enemy_class='Saber', health=1000000)
	bc.enemy_13 = Enemy(enemy_class='Assassin', health=100, enemy_attribute='龙')

	bc.use_inherent_skill()
	dict1 = {'atk': 1000,
	         'range': '己方全体',
	         '状态[Quick指令卡提升(不可解除)]': ['30%', 1, 3],
	         '初始NP': 50}
	bc.use_costume_skill(1, dict1)
	bc.round_start(1)
	bc.use_skill(order=2, skill=1, target=1)
	bc.use_skill(order=2, skill=1)
	bc.use_skill(order=2, skill=3, target=1)
	bc.use_skill(order=3, skill=1, target=1)
	bc.use_skill(order=3, skill=1)
	bc.use_skill(order=3, skill=3, target=1)
	bc.use_skill(order=1, skill=3)
	bc.use_np(order=1, target=1)
	bc.master = Master(1, 10)
	selectservant.view_role(1, 'master', bc.master)
	#selectservant.view_role(1, 'enemy', bc.enemy_11)




	sys.exit(app.exec_())



