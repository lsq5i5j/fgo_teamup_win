import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox, QFileDialog
import MainUi
import pandas as pd
import os
import webbrowser
from Code_SelectServant import Ui_SelectServant
from Code_SelectMaster import Ui_SelectMaster
from Code_SelectCostume import Ui_SelectCostume
from Code_SelectLevel import Ui_SelectLevel
from Code_SelectTarget import Ui_SelectTarget
from Code_SelectTarget_Inverse import Ui_SelectTarget_Inverse
from Code_SelectTarget_Change import Ui_SelectTarget_Change
from Code_SelectProgress import Ui_SelectProgress
from Code_ViewDetails import Ui_ViewDetails
from Code_Update import Ui_Update
from battle_config import BattleConfig, Role, Servant, Enemy, Master
from PyQt5.QtGui import QPixmap, QIcon
from copy import copy, deepcopy


class Ui_MainWindow(QMainWindow, MainUi.Ui_MainWindow):

	def __init__(self):
		QMainWindow.__init__(self)
		MainUi.Ui_MainWindow.__init__(self)
		self.setupUi(self)
		self.servant_order = 0
		self.costume_order = 0
		# 更新按钮
		self.action_update.triggered.connect(self.program_update)
		self.update_window = Ui_Update()
		# 网站链接
		self.action_about.triggered.connect(self.open_about)
		self.action_mooncell.triggered.connect(self.open_mooncell)
		self.action_kazemai.triggered.connect(self.open_kazemai)
		self.action_support.triggered.connect(self.open_nga)
		# 开场技能
		self.skill_round_start = pd.DataFrame()

		# 绑定从者选择窗口
		self.select_servant_window = Ui_SelectServant()
		self.select_servant_window.my_Signal.connect(self.set_servant)
		self.btn_select_servant_1.clicked.connect(lambda: self.choose_servant(1))
		self.btn_select_servant_2.clicked.connect(lambda: self.choose_servant(2))
		self.btn_select_servant_3.clicked.connect(lambda: self.choose_servant(3))
		self.btn_select_servant_4.clicked.connect(lambda: self.choose_servant(4))
		self.btn_select_servant_5.clicked.connect(lambda: self.choose_servant(5))
		self.btn_select_servant_6.clicked.connect(lambda: self.choose_servant(6))
		# 绑定礼装选择窗口
		self.select_costume_window = Ui_SelectCostume()
		self.select_costume_window.my_Signal.connect(self.set_costume)
		self.btn_select_costume_1.clicked.connect(lambda: self.choose_costume(1))
		self.btn_select_costume_2.clicked.connect(lambda: self.choose_costume(2))
		self.btn_select_costume_3.clicked.connect(lambda: self.choose_costume(3))
		self.btn_select_costume_4.clicked.connect(lambda: self.choose_costume(4))
		self.btn_select_costume_5.clicked.connect(lambda: self.choose_costume(5))
		self.btn_select_costume_6.clicked.connect(lambda: self.choose_costume(6))
		# 绑定御主礼装选择窗口
		self.select_master_window = Ui_SelectMaster()
		self.select_master_window.my_Signal.connect(self.set_master)
		self.btn_select_master.clicked.connect(self.choose_master)
		# 从者设置
		self.servant_1 = {'ID': 0, '等级': 1, '宝具数': 1, '技能': [10, 10, 10], '芙芙': 1000}
		self.servant_2 = {'ID': 0, '等级': 1, '宝具数': 1, '技能': [10, 10, 10], '芙芙': 1000}
		self.servant_3 = {'ID': 0, '等级': 1, '宝具数': 1, '技能': [10, 10, 10], '芙芙': 1000}
		self.servant_4 = {'ID': 0, '等级': 1, '宝具数': 1, '技能': [10, 10, 10], '芙芙': 1000}
		self.servant_5 = {'ID': 0, '等级': 1, '宝具数': 1, '技能': [10, 10, 10], '芙芙': 1000}
		self.servant_6 = {'ID': 0, '等级': 1, '宝具数': 1, '技能': [10, 10, 10], '芙芙': 1000}
		# 礼装设置
		self.costume_1 = {'atk': 0, 'range': '自身', 'ID': -1, 'level': 1, 'full': 0}
		self.costume_2 = {'atk': 0, 'range': '自身', 'ID': -1, 'level': 1, 'full': 0}
		self.costume_3 = {'atk': 0, 'range': '自身', 'ID': -1, 'level': 1, 'full': 0}
		self.costume_4 = {'atk': 0, 'range': '自身', 'ID': -1, 'level': 1, 'full': 0}
		self.costume_5 = {'atk': 0, 'range': '自身', 'ID': -1, 'level': 1, 'full': 0}
		self.costume_6 = {'atk': 0, 'range': '自身', 'ID': -1, 'level': 1, 'full': 0}
		# 御主技能设置
		self.master = {'ID': 0, '等级': 1}
		# 敌人设置
		self.df_enemy = pd.DataFrame()
		# 战斗配置
		self.battle_config = BattleConfig()
		self.battle_config_list = []
		# 确认队伍选择
		self.btn_confirm_team.clicked.connect(self.battle_confirm_team)
		# 修改队伍选择
		self.btn_change_team.clicked.connect(self.battle_change_team)
		# 选择战斗副本
		self.btn_choose_level.clicked.connect(self.battle_choose_level)
		self.select_level_window = Ui_SelectLevel()
		self.select_level_window.my_Signal.connect(self.set_level)
		# 下一回合
		self.btn_round1_next.clicked.connect(self.next_round)
		self.btn_round2_next.clicked.connect(self.next_round)
		# 下一回合
		self.btn_output_strategy.clicked.connect(self.output_strategy)

		# 使用从者技能
		self.round1_servant1_skill1.clicked.connect(lambda: self.servant_use_skill(1, 1, 1))
		self.round1_servant1_skill2.clicked.connect(lambda: self.servant_use_skill(1, 1, 2))
		self.round1_servant1_skill3.clicked.connect(lambda: self.servant_use_skill(1, 1, 3))
		self.round1_servant2_skill1.clicked.connect(lambda: self.servant_use_skill(1, 2, 1))
		self.round1_servant2_skill2.clicked.connect(lambda: self.servant_use_skill(1, 2, 2))
		self.round1_servant2_skill3.clicked.connect(lambda: self.servant_use_skill(1, 2, 3))
		self.round1_servant3_skill1.clicked.connect(lambda: self.servant_use_skill(1, 3, 1))
		self.round1_servant3_skill2.clicked.connect(lambda: self.servant_use_skill(1, 3, 2))
		self.round1_servant3_skill3.clicked.connect(lambda: self.servant_use_skill(1, 3, 3))

		self.round2_servant1_skill1.clicked.connect(lambda: self.servant_use_skill(2, 1, 1))
		self.round2_servant1_skill2.clicked.connect(lambda: self.servant_use_skill(2, 1, 2))
		self.round2_servant1_skill3.clicked.connect(lambda: self.servant_use_skill(2, 1, 3))
		self.round2_servant2_skill1.clicked.connect(lambda: self.servant_use_skill(2, 2, 1))
		self.round2_servant2_skill2.clicked.connect(lambda: self.servant_use_skill(2, 2, 2))
		self.round2_servant2_skill3.clicked.connect(lambda: self.servant_use_skill(2, 2, 3))
		self.round2_servant3_skill1.clicked.connect(lambda: self.servant_use_skill(2, 3, 1))
		self.round2_servant3_skill2.clicked.connect(lambda: self.servant_use_skill(2, 3, 2))
		self.round2_servant3_skill3.clicked.connect(lambda: self.servant_use_skill(2, 3, 3))

		self.round3_servant1_skill1.clicked.connect(lambda: self.servant_use_skill(3, 1, 1))
		self.round3_servant1_skill2.clicked.connect(lambda: self.servant_use_skill(3, 1, 2))
		self.round3_servant1_skill3.clicked.connect(lambda: self.servant_use_skill(3, 1, 3))
		self.round3_servant2_skill1.clicked.connect(lambda: self.servant_use_skill(3, 2, 1))
		self.round3_servant2_skill2.clicked.connect(lambda: self.servant_use_skill(3, 2, 2))
		self.round3_servant2_skill3.clicked.connect(lambda: self.servant_use_skill(3, 2, 3))
		self.round3_servant3_skill1.clicked.connect(lambda: self.servant_use_skill(3, 3, 1))
		self.round3_servant3_skill2.clicked.connect(lambda: self.servant_use_skill(3, 3, 2))
		self.round3_servant3_skill3.clicked.connect(lambda: self.servant_use_skill(3, 3, 3))

		# 使用御主技能
		self.round1_master_skill1.clicked.connect(lambda: self.master_use_skill(1, 1))
		self.round1_master_skill2.clicked.connect(lambda: self.master_use_skill(1, 2))
		self.round1_master_skill3.clicked.connect(lambda: self.master_use_skill(1, 3))
		self.round2_master_skill1.clicked.connect(lambda: self.master_use_skill(2, 1))
		self.round2_master_skill2.clicked.connect(lambda: self.master_use_skill(2, 2))
		self.round2_master_skill3.clicked.connect(lambda: self.master_use_skill(2, 3))
		self.round3_master_skill1.clicked.connect(lambda: self.master_use_skill(3, 1))
		self.round3_master_skill2.clicked.connect(lambda: self.master_use_skill(3, 2))
		self.round3_master_skill3.clicked.connect(lambda: self.master_use_skill(3, 3))

		# 使用宝具
		self.round1_servant1_np.clicked.connect(lambda: self.servant_use_np(1, 1))
		self.round1_servant2_np.clicked.connect(lambda: self.servant_use_np(1, 2))
		self.round1_servant3_np.clicked.connect(lambda: self.servant_use_np(1, 3))
		self.round2_servant1_np.clicked.connect(lambda: self.servant_use_np(2, 1))
		self.round2_servant2_np.clicked.connect(lambda: self.servant_use_np(2, 2))
		self.round2_servant3_np.clicked.connect(lambda: self.servant_use_np(2, 3))
		self.round3_servant1_np.clicked.connect(lambda: self.servant_use_np(3, 1))
		self.round3_servant2_np.clicked.connect(lambda: self.servant_use_np(3, 2))
		self.round3_servant3_np.clicked.connect(lambda: self.servant_use_np(3, 3))

		# 选择技能/宝具使用对象
		self.current_used_name = ''
		self.current_used_role = ''
		self.select_target_window = Ui_SelectTarget()
		self.select_target_window.my_Signal.connect(self.set_target)
		self.select_target_inverse_window = Ui_SelectTarget_Inverse()
		self.select_target_inverse_window.my_Signal.connect(self.set_target)

		# 选择换人对象
		self.select_target_change_window = Ui_SelectTarget_Change()
		self.select_target_change_window.my_Signal.connect(self.set_target_change)

		# 回合重置
		self.btn_round_reset.clicked.connect(self.battle_reset)

		# 设置随机数
		self.round1_bar_random.valueChanged[int].connect(self.set_random_number)
		self.round2_bar_random.valueChanged[int].connect(self.set_random_number)
		self.round3_bar_random.valueChanged[int].connect(self.set_random_number)

		# 设置游戏进度
		self.select_progress_window = Ui_SelectProgress()
		self.btn_set_progress.clicked.connect(self.select_progress_window.show)

		# 展示从者/敌人详细信息
		self.view_details_window = Ui_ViewDetails()
		self.round1_servant1_pic.clicked.connect(lambda: self.view_role_detail(1, 'servant', 1))
		self.round1_servant2_pic.clicked.connect(lambda: self.view_role_detail(1, 'servant', 2))
		self.round1_servant3_pic.clicked.connect(lambda: self.view_role_detail(1, 'servant', 3))
		self.round2_servant1_pic.clicked.connect(lambda: self.view_role_detail(2, 'servant', 1))
		self.round2_servant2_pic.clicked.connect(lambda: self.view_role_detail(2, 'servant', 2))
		self.round2_servant3_pic.clicked.connect(lambda: self.view_role_detail(2, 'servant', 3))
		self.round3_servant1_pic.clicked.connect(lambda: self.view_role_detail(3, 'servant', 1))
		self.round3_servant2_pic.clicked.connect(lambda: self.view_role_detail(3, 'servant', 2))
		self.round3_servant3_pic.clicked.connect(lambda: self.view_role_detail(3, 'servant', 3))

		self.round1_enemy1_pic.clicked.connect(lambda: self.view_role_detail(1, 'enemy', 1))
		self.round1_enemy2_pic.clicked.connect(lambda: self.view_role_detail(1, 'enemy', 2))
		self.round1_enemy3_pic.clicked.connect(lambda: self.view_role_detail(1, 'enemy', 3))
		self.round2_enemy1_pic.clicked.connect(lambda: self.view_role_detail(2, 'enemy', 1))
		self.round2_enemy2_pic.clicked.connect(lambda: self.view_role_detail(2, 'enemy', 2))
		self.round2_enemy3_pic.clicked.connect(lambda: self.view_role_detail(2, 'enemy', 3))
		self.round3_enemy1_pic.clicked.connect(lambda: self.view_role_detail(3, 'enemy', 1))
		self.round3_enemy2_pic.clicked.connect(lambda: self.view_role_detail(3, 'enemy', 2))
		self.round3_enemy3_pic.clicked.connect(lambda: self.view_role_detail(3, 'enemy', 3))

		self.round1_master_pic.clicked.connect(lambda: self.view_role_detail(1, 'master', 0))
		self.round2_master_pic.clicked.connect(lambda: self.view_role_detail(2, 'master', 0))
		self.round3_master_pic.clicked.connect(lambda: self.view_role_detail(3, 'master', 0))

		# 设置保存的游戏操作
		self.battle_strategy = '第1回合：'

	# 更新程序
	def program_update(self):
		self.update_window.show()

	def open_about(self):
		QMessageBox.information(self, 'FGO周回组队器', '版本信息: beta v1.31  \n更新日期: 2020/06/05  ')

	@staticmethod
	def open_mooncell():
		webbrowser.open('https://fgo.wiki/w/%E9%A6%96%E9%A1%B5')

	@staticmethod
	def open_kazemai():
		webbrowser.open('https://kazemai.github.io/fgo-vz/')

	@staticmethod
	def open_nga():
		webbrowser.open('https://bbs.nga.cn/read.php?tid=21054760')

	# 关闭程序时，关闭所有子窗口
	def closeEvent(self, event):
		if self.battle_strategy != self.battle_config.battle_strategy:
			# 重新定义 closeEvent
			reply = QMessageBox.question(self, '信息', "检测到操作流程未保存，是否仍然退出?", QMessageBox.Yes, QMessageBox.No)
			if reply == QMessageBox.Yes:
				event.accept()
				sys.exit(app.exec_())
			else:
				event.ignore()

	# 展示从者/敌人详细信息
	def view_role_detail(self, battle_round, role_type, role_num):
		battle_config = self.battle_config
		if role_type == 'servant':
			if role_num == 1:
				role = battle_config.servant_1
			elif role_num == 2:
				role = battle_config.servant_2
			elif role_num == 3:
				role = battle_config.servant_3
			else:
				return

		elif role_type == 'enemy':
			if battle_round == 1:
				if role_num == 1:
					role = battle_config.enemy_11
				elif role_num == 2:
					role = battle_config.enemy_12
				elif role_num == 3:
					role = battle_config.enemy_13
				else:
					return
			elif battle_round == 2:
				if role_num == 1:
					role = battle_config.enemy_21
				elif role_num == 2:
					role = battle_config.enemy_22
				elif role_num == 3:
					role = battle_config.enemy_23
				else:
					return
			elif battle_round == 3:
				if role_num == 1:
					role = battle_config.enemy_31
				elif role_num == 2:
					role = battle_config.enemy_32
				elif role_num == 3:
					role = battle_config.enemy_33
				else:
					return
			else:
				return
		elif role_type == 'master':
			role = battle_config.master
		else:
			return

		if role_type == 'servant':
			if role.health <= 0:
				return
		elif role_type == 'enemy':
			if role.health_start <= 0:
				return
		elif role_type == 'master':
			if role.master_id <= 0:
				return
		self.view_details_window.view_role(battle_round, role_type, role)
		self.view_details_window.close()
		self.view_details_window.show()

	# 设置随机数
	def set_random_number(self):
		num = self.round1_bar_random.value() / 100
		self.round1_label_random.setText('随机数: ' + str(num))
		num = self.round2_bar_random.value() / 100
		self.round2_label_random.setText('随机数: ' + str(num))
		num = self.round3_bar_random.value() / 100
		self.round3_label_random.setText('随机数: ' + str(num))

	# 选择FREE副本
	def battle_choose_level(self):
		self.select_level_window.close()
		self.select_level_window.show()

	# 从子窗口接受选择的Free本信息
	def set_level(self, df):
		self.df_enemy = df
		self.round1_enemy1_pic.setIcon(QIcon())
		self.round1_enemy2_pic.setIcon(QIcon())
		self.round1_enemy3_pic.setIcon(QIcon())
		self.round2_enemy1_pic.setIcon(QIcon())
		self.round2_enemy2_pic.setIcon(QIcon())
		self.round2_enemy3_pic.setIcon(QIcon())
		self.round3_enemy1_pic.setIcon(QIcon())
		self.round3_enemy2_pic.setIcon(QIcon())
		self.round3_enemy3_pic.setIcon(QIcon())

		self.round1_enemy1_health.setText('')
		self.round1_enemy2_health.setText('')
		self.round1_enemy3_health.setText('')
		self.round2_enemy1_health.setText('')
		self.round2_enemy2_health.setText('')
		self.round2_enemy3_health.setText('')
		self.round3_enemy1_health.setText('')
		self.round3_enemy2_health.setText('')
		self.round3_enemy3_health.setText('')

		self.round1_enemy1_class.setText('')
		self.round1_enemy2_class.setText('')
		self.round1_enemy3_class.setText('')
		self.round2_enemy1_class.setText('')
		self.round2_enemy2_class.setText('')
		self.round2_enemy3_class.setText('')
		self.round3_enemy1_class.setText('')
		self.round3_enemy2_class.setText('')
		self.round3_enemy3_class.setText('')

		# 关卡特性
		self.battle_config.battle_ground = df['关卡特性'].values[0]
		for index, row in df.iterrows():
			pic_path = row['图片路径']
			icon = QIcon()
			icon.addPixmap(QPixmap(pic_path), QIcon.Normal, QIcon.Off)
			if row['回合'] == 1 and row['位置'] == 1:
				self.round1_enemy1_pic.setIcon(icon)
				self.round1_enemy1_health.setText('血量: ' + str(int(row['血量'])))
				self.round1_enemy1_class.setText('职阶: ' + row['职阶'])
			elif row['回合'] == 1 and row['位置'] == 2:
				self.round1_enemy2_pic.setIcon(icon)
				self.round1_enemy2_health.setText('血量: ' + str(int(row['血量'])))
				self.round1_enemy2_class.setText('职阶: ' + row['职阶'])
			elif row['回合'] == 1 and row['位置'] == 3:
				self.round1_enemy3_pic.setIcon(icon)
				self.round1_enemy3_health.setText('血量: ' + str(int(row['血量'])))
				self.round1_enemy3_class.setText('职阶: ' + row['职阶'])
			elif row['回合'] == 2 and row['位置'] == 1:
				self.round2_enemy1_pic.setIcon(icon)
				self.round2_enemy1_health.setText('血量: ' + str(int(row['血量'])))
				self.round2_enemy1_class.setText('职阶: ' + row['职阶'])
			elif row['回合'] == 2 and row['位置'] == 2:
				self.round2_enemy2_pic.setIcon(icon)
				self.round2_enemy2_health.setText('血量: ' + str(int(row['血量'])))
				self.round2_enemy2_class.setText('职阶: ' + row['职阶'])
			elif row['回合'] == 2 and row['位置'] == 3:
				self.round2_enemy3_pic.setIcon(icon)
				self.round2_enemy3_health.setText('血量: ' + str(int(row['血量'])))
				self.round2_enemy3_class.setText('职阶: ' + row['职阶'])
			elif row['回合'] == 3 and row['位置'] == 1:
				self.round3_enemy1_pic.setIcon(icon)
				self.round3_enemy1_health.setText('血量: ' + str(int(row['血量'])))
				self.round3_enemy1_class.setText('职阶: ' + row['职阶'])
			elif row['回合'] == 3 and row['位置'] == 2:
				self.round3_enemy2_pic.setIcon(icon)
				self.round3_enemy2_health.setText('血量: ' + str(int(row['血量'])))
				self.round3_enemy2_class.setText('职阶: ' + row['职阶'])
			elif row['回合'] == 3 and row['位置'] == 3:
				self.round3_enemy3_pic.setIcon(icon)
				self.round3_enemy3_health.setText('血量: ' + str(int(row['血量'])))
				self.round3_enemy3_class.setText('职阶: ' + row['职阶'])

	# 设定模拟战斗的Free本
	def set_level_confirm(self):
		self.battle_config.enemy_11 = Enemy()
		self.battle_config.enemy_11 = Enemy()
		self.battle_config.enemy_12 = Enemy()
		self.battle_config.enemy_13 = Enemy()
		self.battle_config.enemy_21 = Enemy()
		self.battle_config.enemy_22 = Enemy()
		self.battle_config.enemy_23 = Enemy()
		self.battle_config.enemy_31 = Enemy()
		self.battle_config.enemy_32 = Enemy()
		self.battle_config.enemy_33 = Enemy()

		self.round1_enemy1_pic.setIcon(QIcon())
		self.round1_enemy2_pic.setIcon(QIcon())
		self.round1_enemy3_pic.setIcon(QIcon())
		self.round2_enemy1_pic.setIcon(QIcon())
		self.round2_enemy2_pic.setIcon(QIcon())
		self.round2_enemy3_pic.setIcon(QIcon())
		self.round3_enemy1_pic.setIcon(QIcon())
		self.round3_enemy2_pic.setIcon(QIcon())
		self.round3_enemy3_pic.setIcon(QIcon())

		self.round1_enemy1_health.setText('')
		self.round1_enemy2_health.setText('')
		self.round1_enemy3_health.setText('')
		self.round2_enemy1_health.setText('')
		self.round2_enemy2_health.setText('')
		self.round2_enemy3_health.setText('')
		self.round3_enemy1_health.setText('')
		self.round3_enemy2_health.setText('')
		self.round3_enemy3_health.setText('')

		self.round1_enemy1_class.setText('')
		self.round1_enemy2_class.setText('')
		self.round1_enemy3_class.setText('')
		self.round2_enemy1_class.setText('')
		self.round2_enemy2_class.setText('')
		self.round2_enemy3_class.setText('')
		self.round3_enemy1_class.setText('')
		self.round3_enemy2_class.setText('')
		self.round3_enemy3_class.setText('')
		# 关卡特性
		df = self.df_enemy
		self.battle_config.battle_ground = df['关卡特性'].values[0]
		# 判断有无开场技能
		name_list = df['中文名'].values
		if '管制塔巴巴妥司' in name_list:
			self.skill_round_start = pd.read_csv('./data/level/Barbatos_skill.csv')
		else:
			self.skill_round_start = pd.DataFrame()
		print(df)
		for index, row in df.iterrows():
			enemy = self.select_level_window.set_enemy(row)
			icon = QIcon()
			icon.addPixmap(QPixmap(enemy.pic_path), QIcon.Normal, QIcon.Off)
			if row['回合'] == 1 and row['位置'] == 1:
				self.battle_config.enemy_11 = enemy
				self.round1_enemy1_pic.setIcon(icon)
				self.round1_enemy1_health.setText('血量: ' + str(int(row['血量'])))
				self.round1_enemy1_class.setText('职阶: ' + row['职阶'])
			elif row['回合'] == 1 and row['位置'] == 2:
				self.battle_config.enemy_12 = enemy
				self.round1_enemy2_pic.setIcon(icon)
				self.round1_enemy2_health.setText('血量: ' + str(int(row['血量'])))
				self.round1_enemy2_class.setText('职阶: ' + row['职阶'])
			elif row['回合'] == 1 and row['位置'] == 3:
				self.battle_config.enemy_13 = enemy
				self.round1_enemy3_pic.setIcon(icon)
				self.round1_enemy3_health.setText('血量: ' + str(int(row['血量'])))
				self.round1_enemy3_class.setText('职阶: ' + row['职阶'])
			elif row['回合'] == 2 and row['位置'] == 1:
				self.battle_config.enemy_21 = enemy
				self.round2_enemy1_pic.setIcon(icon)
				self.round2_enemy1_health.setText('血量: ' + str(int(row['血量'])))
				self.round2_enemy1_class.setText('职阶: ' + row['职阶'])
			elif row['回合'] == 2 and row['位置'] == 2:
				self.battle_config.enemy_22 = enemy
				self.round2_enemy2_pic.setIcon(icon)
				self.round2_enemy2_health.setText('血量: ' + str(int(row['血量'])))
				self.round2_enemy2_class.setText('职阶: ' + row['职阶'])
			elif row['回合'] == 2 and row['位置'] == 3:
				self.battle_config.enemy_23 = enemy
				self.round2_enemy3_pic.setIcon(icon)
				self.round2_enemy3_health.setText('血量: ' + str(int(row['血量'])))
				self.round2_enemy3_class.setText('职阶: ' + row['职阶'])
			elif row['回合'] == 3 and row['位置'] == 1:
				self.battle_config.enemy_31 = enemy
				self.round3_enemy1_pic.setIcon(icon)
				self.round3_enemy1_health.setText('血量: ' + str(int(row['血量'])))
				self.round3_enemy1_class.setText('职阶: ' + row['职阶'])
			elif row['回合'] == 3 and row['位置'] == 2:
				self.battle_config.enemy_32 = enemy
				self.round3_enemy2_pic.setIcon(icon)
				self.round3_enemy2_health.setText('血量: ' + str(int(row['血量'])))
				self.round3_enemy2_class.setText('职阶: ' + row['职阶'])
			elif row['回合'] == 3 and row['位置'] == 3:
				self.battle_config.enemy_33 = enemy
				self.round3_enemy3_pic.setIcon(icon)
				self.round3_enemy3_health.setText('血量: ' + str(int(row['血量'])))
				self.round3_enemy3_class.setText('职阶: ' + row['职阶'])

	# 选择魔术礼装
	def choose_master(self):
		self.select_master_window.close()
		self.select_master_window.show()
		master = self.master
		self.select_master_window.receiveContent(master)

	# 保存礼装数据
	def set_master(self, data):
		master_id = data['ID']
		master_level = data['等级']
		icon = QIcon()
		text = '等级: '
		if master_id > 0:
			pixmap = QPixmap("./pic/Master_logo/mystic_code_" + str(master_id).zfill(2) + "_a.png")
			icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
			text += '(' + str(master_level) + ')'
		self.master = data
		self.btn_select_master.setIcon(icon)
		self.round1_master_pic.setIcon(icon)
		self.round2_master_pic.setIcon(icon)
		self.round3_master_pic.setIcon(icon)
		self.label_master_state.setText(text)

	# 选择礼装
	def choose_costume(self, order):
		self.costume_order = order
		self.select_costume_window.close()
		self.select_costume_window.show()
		if order == 1:
			costume = self.costume_1
		elif order == 2:
			costume = self.costume_2
		elif order == 3:
			costume = self.costume_3
		elif order == 4:
			costume = self.costume_4
		elif order == 5:
			costume = self.costume_5
		elif order == 6:
			costume = self.costume_6
		else:
			return
		self.select_costume_window.receiveContent(costume)

	# 选择从者
	def choose_servant(self, order):
		self.servant_order = order
		self.select_servant_window.close()
		self.select_servant_window.show()

		if order == 1:
			data = self.servant_1
		elif order == 2:
			data = self.servant_2
		elif order == 3:
			data = self.servant_3
		elif order == 4:
			data = self.servant_4
		elif order == 5:
			data = self.servant_5
		elif order == 6:
			data = self.servant_6
		else:
			return
		print(data)

		servant_id = data['ID']
		if servant_id != 0:
			self.select_servant_window.chosen_rarity = data['稀有度']
			self.select_servant_window.chosen_class = data['职阶']
			self.select_servant_window.chosen_servant_id = servant_id
			self.select_servant_window.set_servant_data()
			self.select_servant_window.display_servant_data()
			self.select_servant_window.servant_display()

	# 保存礼装数据
	def set_costume(self, data):
		costume_id = data['ID']
		costume_level = data['level']
		icon = QIcon()
		text = '等级: '
		if costume_id != -1:
			icon.addPixmap(QPixmap("./pic/costume_logo/礼装" + str(costume_id).zfill(3) + ".jpg"), QIcon.Normal,
			               QIcon.Off)
			if data['full'] == 0:
				text = '等级: ' + str(costume_level)
			else:
				text = '等级: ' + str(costume_level) + '(满破)'

		if self.costume_order == 1:
			self.costume_1 = data
			self.btn_select_costume_1.setIcon(icon)
			self.label_costume_state_1.setText(text)
		elif self.costume_order == 2:
			self.costume_2 = data
			self.btn_select_costume_2.setIcon(icon)
			self.label_costume_state_2.setText(text)
		elif self.costume_order == 3:
			self.costume_3 = data
			self.btn_select_costume_3.setIcon(icon)
			self.label_costume_state_3.setText(text)
		elif self.costume_order == 4:
			self.costume_4 = data
			self.btn_select_costume_4.setIcon(icon)
			self.label_costume_state_4.setText(text)
		elif self.costume_order == 5:
			self.costume_5 = data
			self.btn_select_costume_5.setIcon(icon)
			self.label_costume_state_5.setText(text)
		elif self.costume_order == 6:
			self.costume_6 = data
			self.btn_select_costume_6.setIcon(icon)
			self.label_costume_state_6.setText(text)

	# 根据得来的数据设置从者的战斗配置
	def set_servant(self, data):
		if self.servant_order == 1:
			self.servant_1 = data
		elif self.servant_order == 2:
			self.servant_2 = data
		elif self.servant_order == 3:
			self.servant_3 = data
		elif self.servant_order == 4:
			self.servant_4 = data
		elif self.servant_order == 5:
			self.servant_5 = data
		elif self.servant_order == 6:
			self.servant_6 = data
		self.display_battle_config()

	@staticmethod
	def display_servant_level(servant):
		skill_level = servant['技能']
		np_level = servant['宝具数']
		level = servant['等级']
		fufu = servant['芙芙']
		text = '技能: ' + str(skill_level[0]) + '/' + str(skill_level[1]) + '/' + str(skill_level[2]) \
		       + '\n宝具: ' + str(np_level) + '\n等级: ' + str(level) + '\n芙芙: ' + str(fufu)
		return text

	# 将设置已选择从者的练度显示在视图中
	def display_battle_config(self):
		for i in range(1, 7):
			icon = QIcon()
			text = '技能: \n宝具: \n等级: \n芙芙: '
			if i == 1:
				servant_id = self.servant_1['ID']
				pic_path = "./pic/servant_logo/servant" + str(servant_id).zfill(3) + ".jpg"
				if servant_id != 0:
					pixmap = QPixmap(pic_path)
					icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
					text = self.display_servant_level(self.servant_1)
				self.btn_select_servant_1.setIcon(icon)
				self.label_servant_state_1.setText(text)
				'''
				self.round1_servant1_pic.setIcon(icon)
				self.round2_servant1_pic.setIcon(icon)
				self.round3_servant1_pic.setIcon(icon)
				'''
			elif i == 2:
				servant_id = self.servant_2['ID']
				pic_path = "./pic/servant_logo/servant" + str(servant_id).zfill(3) + ".jpg"
				if servant_id != 0:
					pixmap = QPixmap(pic_path)
					icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
					text = self.display_servant_level(self.servant_2)
				self.btn_select_servant_2.setIcon(icon)
				self.label_servant_state_2.setText(text)
				'''
				self.round1_servant2_pic.setIcon(icon)
				self.round2_servant2_pic.setIcon(icon)
				self.round3_servant2_pic.setIcon(icon)
				'''
			elif i == 3:
				servant_id = self.servant_3['ID']
				pic_path = "./pic/servant_logo/servant" + str(servant_id).zfill(3) + ".jpg"
				if servant_id != 0:
					pixmap = QPixmap(pic_path)
					icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
					text = self.display_servant_level(self.servant_3)
				self.btn_select_servant_3.setIcon(icon)
				self.label_servant_state_3.setText(text)
				'''
				self.round1_servant3_pic.setIcon(icon)
				self.round2_servant3_pic.setIcon(icon)
				self.round3_servant3_pic.setIcon(icon)
				'''
			elif i == 4:
				servant_id = self.servant_4['ID']
				pic_path = "./pic/servant_logo/servant" + str(servant_id).zfill(3) + ".jpg"
				if servant_id != 0:
					pixmap = QPixmap(pic_path)
					icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
					text = self.display_servant_level(self.servant_4)
				self.btn_select_servant_4.setIcon(icon)
				self.label_servant_state_4.setText(text)
			elif i == 5:
				servant_id = self.servant_5['ID']
				pic_path = "./pic/servant_logo/servant" + str(servant_id).zfill(3) + ".jpg"
				if servant_id != 0:
					pixmap = QPixmap(pic_path)
					icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
					text = self.display_servant_level(self.servant_5)
				self.btn_select_servant_5.setIcon(icon)
				self.label_servant_state_5.setText(text)
			elif i == 6:
				servant_id = self.servant_6['ID']
				pic_path = "./pic/servant_logo/servant" + str(servant_id).zfill(3) + ".jpg"
				if servant_id != 0:
					pixmap = QPixmap(pic_path)
					icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
					text = self.display_servant_level(self.servant_6)
				self.btn_select_servant_6.setIcon(icon)
				self.label_servant_state_6.setText(text)

	# 确认战斗配置
	def battle_confirm_team(self):
		self.battle_config.battle_strategy = '第1回合：'
		if self.servant_1['ID'] < 1 and self.servant_2['ID'] < 1 and self.servant_3['ID'] < 1:
			QMessageBox.information(self, '提 醒', '检测到未设置前排从者, 请设置后继续')
			return
		elif len(self.df_enemy) == 0:
			self.battle_choose_level()
			return
		elif self.master['ID'] <= 0:
			text = '检测到没有携带御主魔术礼装, 是否继续?'
			reply = QMessageBox.information(self, '提 醒', text, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
			if reply == QMessageBox.No:
				return
		for order in range(1, 7):
			if order == 1:
				# 设定从者数据
				data = self.servant_1
				servant = Servant(order=1, servant_id=data['ID'], level=data['等级'], skill_level=data['技能'],
				                  np_level=data['宝具数'], atk_fufu=data['芙芙'])
				self.battle_config.servant_1 = servant
				# 设定礼装数据
				data = self.costume_1
				self.battle_config.use_costume_skill(order, data)
			elif order == 2:
				# 设定从者数据
				data = self.servant_2
				print(data)
				servant = Servant(order=2, servant_id=data['ID'], level=data['等级'], skill_level=data['技能'],
				                  np_level=data['宝具数'], atk_fufu=data['芙芙'])
				self.battle_config.servant_2 = servant
				# 设定礼装数据
				data = self.costume_2
				self.battle_config.use_costume_skill(order, data)
			elif order == 3:
				# 设定从者数据
				data = self.servant_3
				servant = Servant(order=3, servant_id=data['ID'], level=data['等级'], skill_level=data['技能'],
				                  np_level=data['宝具数'], atk_fufu=data['芙芙'])
				self.battle_config.servant_3 = servant
				# 设定礼装数据
				data = self.costume_3
				self.battle_config.use_costume_skill(order, data)
			elif order == 4:
				# 设定从者数据
				data = self.servant_4
				servant = Servant(order=4, servant_id=data['ID'], level=data['等级'], skill_level=data['技能'],
				                  np_level=data['宝具数'], atk_fufu=data['芙芙'])
				self.battle_config.servant_4 = servant
				# 设定礼装数据
				data = self.costume_4
				self.battle_config.use_costume_skill(order, data)
			elif order == 5:
				# 设定从者数据
				data = self.servant_5
				servant = Servant(order=5, servant_id=data['ID'], level=data['等级'], skill_level=data['技能'],
				                  np_level=data['宝具数'], atk_fufu=data['芙芙'])
				self.battle_config.servant_5 = servant
				# 设定礼装数据
				data = self.costume_5
				self.battle_config.use_costume_skill(order, data)
			elif order == 6:
				# 设定从者数据
				data = self.servant_6
				servant = Servant(order=6, servant_id=data['ID'], level=data['等级'], skill_level=data['技能'],
				                  np_level=data['宝具数'], atk_fufu=data['芙芙'])
				self.battle_config.servant_6 = servant
				# 设定礼装数据
				data = self.costume_6
				self.battle_config.use_costume_skill(order, data)

		# 设置敌人配置
		self.set_level_confirm()
		# 设置魔术礼装
		data = self.master
		self.battle_config.master = Master(master_id=data['ID'], level=data['等级'])
		# 启动战斗副本
		self.battle_config.round_start(1)
		self.battle_config.fill_back_servant()
		self.battle_config_list = []
		# 设置开场技能
		for index, row in self.skill_round_start.iterrows():
			self.battle_config.skill_target_range(user=Role(), buff=row)
		self.show_battle_state_all(pic=True)
		# 开启技能/宝具使用按钮
		self.set_button_enable(True)
		self.set_button_enable_round(self.battle_config.battle_round)
		# 开启回合重置, 下一回合按钮
		# self.btn_round1_next.setEnabled(True)
		self.btn_round_reset.setEnabled(True)

	# 修改队伍配置
	def battle_change_team(self):
		self.set_button_enable(False)
		self.set_button_enable_round(0)
		self.btn_round_reset.setEnabled(False)

	# 从者使用技能
	def servant_use_skill(self, battle_round, servant_order, skill_num):
		if self.battle_config.battle_round != battle_round:
			print('当前回合与设定回合不相符, 请检查程序')
			return

		if servant_order == 1:
			servant = self.battle_config.servant_1
		elif servant_order == 2:
			servant = self.battle_config.servant_2
		elif servant_order == 3:
			servant = self.battle_config.servant_3
		else:
			return

		if skill_num == 1:
			skill = servant.skill_1
		elif skill_num == 2:
			skill = servant.skill_2
		elif skill_num == 3:
			skill = servant.skill_3
		else:
			return
		text = ''
		for i in skill[['技能效果', '幅度']].values:
			name = i[0]
			num = str(i[1])
			if '(' in name:
				a = name.rfind('(')
				name = name[0:a] + num + name[a:len(name)]
			else:
				name = name + num
			text += name + '\n'
		text = text.replace('nan', '')

		if text == '':
			text = '当前技能效果暂不支持或对速刷无帮助'
		else:
			text = '技能效果:\n\n' + text + '\n是否确定使用?'

		if self.box_skill_confirm.checkState() != 0:
			reply = QMessageBox.question(self, '提  醒', text, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
			if reply == QMessageBox.No:
				return

		if skill_num == 1:
			self.current_used_name = '技能1'
		elif skill_num == 2:
			self.current_used_name = '技能2'
		elif skill_num == 3:
			self.current_used_name = '技能3'
		else:
			return

		if servant_order == 1:
			servant = self.battle_config.servant_1
			self.current_used_role = '从者1'
		elif servant_order == 2:
			servant = self.battle_config.servant_2
			self.current_used_role = '从者2'
		elif servant_order == 3:
			servant = self.battle_config.servant_3
			self.current_used_role = '从者3'
		else:
			return

		skill_type = servant.skill_type[skill_num - 1]

		# 特殊效果(指令卡色卡变化)
		if '宝具指令卡' in text and '类型变化' in text:
			self.select_target_inverse_window.btn_1.setEnabled(True)
			self.select_target_inverse_window.btn_2.setEnabled(True)
			self.select_target_inverse_window.btn_3.setEnabled(True)
			icon = QIcon()
			icon.addPixmap(QPixmap('./pic/icon/Buster.png'))
			self.select_target_inverse_window.btn_1.setIcon(icon)
			icon = QIcon()
			icon.addPixmap(QPixmap('./pic/icon/Arts.png'))
			self.select_target_inverse_window.btn_2.setIcon(icon)
			icon = QIcon()
			icon.addPixmap(QPixmap('./pic/icon/Quick.png'))
			self.select_target_inverse_window.btn_3.setIcon(icon)
			self.current_used_name = '宝具指令卡类型变化'
			self.select_target_inverse_window.close()
			self.select_target_inverse_window.show()
			return

		if '己方单体' in skill_type:
			role1 = self.battle_config.servant_1
			role2 = self.battle_config.servant_2
			role3 = self.battle_config.servant_3
			window = self.select_target_window
		elif '敌方单体' in skill_type:
			role1 = self.battle_config.enemy_1
			role2 = self.battle_config.enemy_2
			role3 = self.battle_config.enemy_3
			window = self.select_target_inverse_window
		else:
			self.set_target(0)
			return

		icon = QIcon()
		if role1.health > 0:
			window.btn_1.setEnabled(True)
		else:
			window.btn_1.setEnabled(False)
		icon.addPixmap(QPixmap(role1.pic_path), QIcon.Normal, QIcon.Off)
		window.btn_1.setIcon(icon)

		icon = QIcon()
		if role2.health > 0:
			window.btn_2.setEnabled(True)
		else:
			window.btn_2.setEnabled(False)
		icon.addPixmap(QPixmap(role2.pic_path), QIcon.Normal, QIcon.Off)
		window.btn_2.setIcon(icon)

		icon = QIcon()
		if role3.health > 0:
			window.btn_3.setEnabled(True)
		else:
			window.btn_3.setEnabled(False)
		icon.addPixmap(QPixmap(role3.pic_path), QIcon.Normal, QIcon.Off)
		window.btn_3.setIcon(icon)

		window.close()
		window.show()

	# 御主使用技能
	def master_use_skill(self, battle_round, skill_num):

		if self.battle_config.battle_round != battle_round:
			print('当前回合与设定回合不相符, 请检查程序')
			return
		master = self.battle_config.master
		if skill_num == 1:
			skill = master.skill_1
		elif skill_num == 2:
			skill = master.skill_2
		elif skill_num == 3:
			skill = master.skill_3
		else:
			return
		text = ''
		for i in skill[['技能效果', '幅度']].values:
			name = i[0]
			num = str(i[1])
			if '(' in name:
				a = name.rfind('(')
				name = name[0:a] + num + name[a:len(name)]
			else:
				name = name + num
			text += name + '\n'
		text = text.replace('nan', '')

		if text == '':
			text = '当前技能效果暂不支持或对速刷无帮助'
		else:
			text = '技能效果:\n\n' + text + '\n是否确定使用?'

		if self.box_skill_confirm.checkState() != 0:
			reply = QMessageBox.question(self, '提  醒', text, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
			if reply == QMessageBox.No:
				return

		if skill_num == 1:
			self.current_used_name = '技能1'
		elif skill_num == 2:
			self.current_used_name = '技能2'
		elif skill_num == 3:
			self.current_used_name = '技能3'
		else:
			return

		master = self.battle_config.master
		self.current_used_role = '御主'
		skill_type = master.skill_type[skill_num - 1]

		if '己方单体' in skill_type:
			role1 = self.battle_config.servant_1
			role2 = self.battle_config.servant_2
			role3 = self.battle_config.servant_3
			window = self.select_target_window
		elif '敌方单体' in skill_type:
			role1 = self.battle_config.enemy_1
			role2 = self.battle_config.enemy_2
			role3 = self.battle_config.enemy_3
			window = self.select_target_inverse_window
		elif '换人' in skill_type:
			self.select_target_change_window.reset()

			icon = QIcon()
			pixmap = QPixmap(self.battle_config.servant_1.pic_path)
			icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
			self.select_target_change_window.btn_1.setIcon(icon)

			icon = QIcon()
			pixmap = QPixmap(self.battle_config.servant_2.pic_path)
			icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
			self.select_target_change_window.btn_2.setIcon(icon)

			icon = QIcon()
			pixmap = QPixmap(self.battle_config.servant_3.pic_path)
			icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
			self.select_target_change_window.btn_3.setIcon(icon)

			icon = QIcon()
			pixmap = QPixmap(self.battle_config.servant_4.pic_path)
			icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
			self.select_target_change_window.btn_4.setIcon(icon)

			icon = QIcon()
			pixmap = QPixmap(self.battle_config.servant_5.pic_path)
			icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
			self.select_target_change_window.btn_5.setIcon(icon)

			icon = QIcon()
			pixmap = QPixmap(self.battle_config.servant_6.pic_path)
			icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
			self.select_target_change_window.btn_6.setIcon(icon)

			# 设置按钮激活状态
			if self.battle_config.servant_1.health > 0:
				self.select_target_change_window.btn_1.setEnabled(True)
			else:
				self.select_target_change_window.btn_1.setEnabled(False)

			if self.battle_config.servant_2.health > 0:
				self.select_target_change_window.btn_2.setEnabled(True)
			else:
				self.select_target_change_window.btn_2.setEnabled(False)

			if self.battle_config.servant_3.health > 0:
				self.select_target_change_window.btn_3.setEnabled(True)
			else:
				self.select_target_change_window.btn_3.setEnabled(False)

			if self.battle_config.servant_4.health > 0:
				self.select_target_change_window.btn_4.setEnabled(True)
			else:
				self.select_target_change_window.btn_4.setEnabled(False)

			if self.battle_config.servant_5.health > 0:
				self.select_target_change_window.btn_5.setEnabled(True)
			else:
				self.select_target_change_window.btn_5.setEnabled(False)

			if self.battle_config.servant_6.health > 0:
				self.select_target_change_window.btn_6.setEnabled(True)
			else:
				self.select_target_change_window.btn_6.setEnabled(False)
			self.select_target_change_window.close()
			self.select_target_change_window.show()
			return
		else:
			self.current_used_role = '御主'
			self.current_used_name = '技能' + str(skill_num)
			self.set_target(0)
			return

		icon = QIcon()
		if role1.health > 0:
			window.btn_1.setEnabled(True)
		else:
			window.btn_1.setEnabled(False)
		icon.addPixmap(QPixmap(role1.pic_path), QIcon.Normal, QIcon.Off)
		window.btn_1.setIcon(icon)

		icon = QIcon()
		if role2.health > 0:
			window.btn_2.setEnabled(True)
		else:
			window.btn_2.setEnabled(False)
		icon.addPixmap(QPixmap(role2.pic_path), QIcon.Normal, QIcon.Off)
		window.btn_2.setIcon(icon)

		icon = QIcon()
		if role3.health > 0:
			window.btn_3.setEnabled(True)
		else:
			window.btn_3.setEnabled(False)
		icon.addPixmap(QPixmap(role3.pic_path), QIcon.Normal, QIcon.Off)
		window.btn_3.setIcon(icon)

		window.close()
		window.show()

	# 设置技能作用对象
	def set_target(self, target):

		# 设置随机数
		if self.battle_config.battle_round == 1:
			random_num = self.round1_bar_random.value() / 100
		elif self.battle_config.battle_round == 2:
			random_num = self.round2_bar_random.value() / 100
		elif self.battle_config.battle_round == 3:
			random_num = self.round3_bar_random.value() / 100
		else:
			random_num = 0.9

		dict_color = {1: 'Buster', 2: 'Arts', 3: 'Quick'}

		if self.current_used_role == '从者1' and self.current_used_name == '技能1':
			self.battle_config.use_skill(order=1, skill=1, target=target, required_prob=self.spinbox_required_prob.value())
		elif self.current_used_role == '从者1' and self.current_used_name == '技能2':
			self.battle_config.use_skill(order=1, skill=2, target=target, required_prob=self.spinbox_required_prob.value())
		elif self.current_used_role == '从者1' and self.current_used_name == '技能3':
			self.battle_config.use_skill(order=1, skill=3, target=target, required_prob=self.spinbox_required_prob.value())
		elif self.current_used_role == '从者2' and self.current_used_name == '技能1':
			self.battle_config.use_skill(order=2, skill=1, target=target, required_prob=self.spinbox_required_prob.value())
		elif self.current_used_role == '从者2' and self.current_used_name == '技能2':
			self.battle_config.use_skill(order=2, skill=2, target=target, required_prob=self.spinbox_required_prob.value())
		elif self.current_used_role == '从者2' and self.current_used_name == '技能3':
			self.battle_config.use_skill(order=2, skill=3, target=target, required_prob=self.spinbox_required_prob.value())
		elif self.current_used_role == '从者3' and self.current_used_name == '技能1':
			self.battle_config.use_skill(order=3, skill=1, target=target, required_prob=self.spinbox_required_prob.value())
		elif self.current_used_role == '从者3' and self.current_used_name == '技能2':
			self.battle_config.use_skill(order=3, skill=2, target=target, required_prob=self.spinbox_required_prob.value())
		elif self.current_used_role == '从者3' and self.current_used_name == '技能3':
			self.battle_config.use_skill(order=3, skill=3, target=target, required_prob=self.spinbox_required_prob.value())
		elif self.current_used_role == '从者1' and self.current_used_name == '宝具':
			self.battle_config.use_np(order=1, target=target, random_num=random_num, required_prob=self.spinbox_required_prob.value())
		elif self.current_used_role == '从者2' and self.current_used_name == '宝具':
			self.battle_config.use_np(order=2, target=target, random_num=random_num, required_prob=self.spinbox_required_prob.value())
		elif self.current_used_role == '从者3' and self.current_used_name == '宝具':
			self.battle_config.use_np(order=3, target=target, random_num=random_num, required_prob=self.spinbox_required_prob.value())
		elif self.current_used_role == '御主' and self.current_used_name == '技能1':
			self.battle_config.use_master_skill(skill=1, target=target)
		elif self.current_used_role == '御主' and self.current_used_name == '技能2':
			self.battle_config.use_master_skill(skill=2, target=target)
		elif self.current_used_role == '御主' and self.current_used_name == '技能3':
			self.battle_config.use_master_skill(skill=3, target=target)
		elif self.current_used_name == '宝具指令卡类型变化':
			if self.current_used_role == '从者1':
				servant = self.battle_config.servant_1
				self.battle_config.use_skill(order=1, skill=2, target=1, required_prob=self.spinbox_required_prob.value())
			elif self.current_used_role == '从者2':
				servant = self.battle_config.servant_2
				self.battle_config.use_skill(order=2, skill=2, target=2, required_prob=self.spinbox_required_prob.value())
			elif self.current_used_role == '从者3':
				servant = self.battle_config.servant_3
				self.battle_config.use_skill(order=3, skill=2, target=3, required_prob=self.spinbox_required_prob.value())
			else:
				return

			servant.np_color = dict_color[target]
			df = servant.np
			if dict_color[target] == 'Quick':
				list_np_rate = ['600%', '800%', '900%', '950%', '1000%']
			elif dict_color[target] == 'Buster':
				list_np_rate = ['300%', '400%', '450%', '475%', '500%']
			elif dict_color[target] == 'Arts':
				list_np_rate = ['450%', '600%', '675%', '712.5%', '750%']
			else:
				return
			df.loc[df['效果'].str.contains('强大攻击'), ['等级' + str(i) for i in range(1, 6)]] = list_np_rate
			print(servant.np)
			self.battle_config.battle_strategy = self.battle_config.battle_strategy.replace('宝具指令卡类型变化nan',
			                                                                                '宝具指令卡变化为' + dict_color[
				                                                                                target])
			self.battle_config.battle_strategy += '：' + dict_color[target]

		if self.battle_config.enemy_1.health <= 0 and self.battle_config.enemy_2.health <= 0 and self.battle_config.enemy_3.health <= 0:
			'''
			if self.battle_config.battle_round < 3:
				text = '当前回合敌人已全部击杀, 自动开启下一回合'
				QMessageBox.information(self, '提 醒', text, QMessageBox.Yes, QMessageBox.Yes)
			'''
			self.show_battle_state_all_nosave(pic=True)
			self.next_round()
		else:
			self.show_battle_state_all(pic=True)
			# 使用宝具后, 禁止使用所有技能
			if self.current_used_name == '宝具':
				self.disable_round_skill()

	# 换人
	def set_target_change(self, target_list):
		self.battle_config.master.skill_used[2] = 1
		self.battle_config.change_order(target_list)
		self.show_battle_state_all(pic=True)

	# 显示当前回合之后回合的所有信息(不保存)
	def show_battle_state_all_nosave(self, pic=False):
		if self.battle_config.battle_round == 1:
			self.btn_round1_next.setEnabled(True)
			self.btn_round2_next.setEnabled(False)
			self.round1_bar_random.setEnabled(True)
			self.round2_bar_random.setEnabled(False)
			self.round3_bar_random.setEnabled(False)
		elif self.battle_config.battle_round == 2:
			self.btn_round2_next.setEnabled(True)
			self.btn_round1_next.setEnabled(False)
			self.round1_bar_random.setEnabled(False)
			self.round2_bar_random.setEnabled(True)
			self.round3_bar_random.setEnabled(False)
		elif self.battle_config.battle_round == 3:
			self.btn_round2_next.setEnabled(False)
			self.btn_round1_next.setEnabled(False)
			self.round1_bar_random.setEnabled(False)
			self.round2_bar_random.setEnabled(False)
			self.round3_bar_random.setEnabled(True)
		for i in range(self.battle_config.battle_round, 4):
			self.show_battle_state(i)
			if pic is True:
				self.show_battle_state_pic(i)
		self.set_button_enable_round(self.battle_config.battle_round)

	# 显示当前回合之后回合的所有信息
	def show_battle_state_all(self, pic=False):
		if self.battle_config.battle_round == 1:
			self.btn_round1_next.setEnabled(True)
			self.btn_round2_next.setEnabled(False)
		elif self.battle_config.battle_round == 2:
			self.btn_round2_next.setEnabled(True)
			self.btn_round1_next.setEnabled(False)
		elif self.battle_config.battle_round == 3:
			self.btn_round2_next.setEnabled(False)
			self.btn_round1_next.setEnabled(False)

		for i in range(self.battle_config.battle_round, 4):
			self.show_battle_state(i)
			if pic is True:
				self.show_battle_state_pic(i)
		self.set_button_enable_round(self.battle_config.battle_round)
		# 保存一次进度
		self.battle_config_list.append(deepcopy(self.battle_config))

	# 显示各种信息(敌方血量, 己方np)
	def show_battle_state(self, battle_round):

		if battle_round == 1:
			self.round1_servant1_np.setText('')
			self.round1_servant2_np.setText('')
			self.round1_servant3_np.setText('')
			self.round1_enemy1_health.setText('')
			self.round1_enemy2_health.setText('')
			self.round1_enemy3_health.setText('')
			if self.battle_config.servant_1.health > 0:
				np_charge = self.battle_config.servant_1.np_charge
				self.round1_servant1_np.setText('宝具: ' + str(round(np_charge, 2)) + '%')
			if self.battle_config.servant_2.health > 0:
				np_charge = self.battle_config.servant_2.np_charge
				self.round1_servant2_np.setText('宝具: ' + str(round(np_charge, 2)) + '%')
			if self.battle_config.servant_3.health > 0:
				np_charge = self.battle_config.servant_3.np_charge
				self.round1_servant3_np.setText('宝具: ' + str(round(np_charge, 2)) + '%')
			if self.battle_config.enemy_11.health_start > 0:
				health = self.battle_config.enemy_11.health
				self.round1_enemy1_health.setText('血量: ' + str(int(health)))
			if self.battle_config.enemy_12.health_start > 0:
				health = self.battle_config.enemy_12.health
				self.round1_enemy2_health.setText('血量: ' + str(int(health)))
			if self.battle_config.enemy_13.health_start > 0:
				health = self.battle_config.enemy_13.health
				self.round1_enemy3_health.setText('血量: ' + str(int(health)))

		elif battle_round == 2:
			self.round2_servant1_np.setText('')
			self.round2_servant2_np.setText('')
			self.round2_servant3_np.setText('')
			self.round2_enemy1_health.setText('')
			self.round2_enemy2_health.setText('')
			self.round2_enemy3_health.setText('')
			if self.battle_config.servant_1.health > 0:
				np_charge = self.battle_config.servant_1.np_charge
				self.round2_servant1_np.setText('宝具: ' + str(round(np_charge, 2)) + '%')
			if self.battle_config.servant_2.health > 0:
				np_charge = self.battle_config.servant_2.np_charge
				self.round2_servant2_np.setText('宝具: ' + str(round(np_charge, 2)) + '%')
			if self.battle_config.servant_3.health > 0:
				np_charge = self.battle_config.servant_3.np_charge
				self.round2_servant3_np.setText('宝具: ' + str(round(np_charge, 2)) + '%')
			if self.battle_config.enemy_21.health_start > 0:
				health = self.battle_config.enemy_21.health
				self.round2_enemy1_health.setText('血量: ' + str(int(health)))
			if self.battle_config.enemy_22.health_start > 0:
				health = self.battle_config.enemy_22.health
				self.round2_enemy2_health.setText('血量: ' + str(int(health)))
			if self.battle_config.enemy_23.health_start > 0:
				health = self.battle_config.enemy_23.health
				self.round2_enemy3_health.setText('血量: ' + str(int(health)))

		elif battle_round == 3:
			self.round3_servant1_np.setText('')
			self.round3_servant2_np.setText('')
			self.round3_servant3_np.setText('')
			self.round3_enemy1_health.setText('')
			self.round3_enemy2_health.setText('')
			self.round3_enemy3_health.setText('')
			if self.battle_config.servant_1.health > 0:
				np_charge = self.battle_config.servant_1.np_charge
				self.round3_servant1_np.setText('宝具: ' + str(round(np_charge, 2)) + '%')
			if self.battle_config.servant_2.health > 0:
				np_charge = self.battle_config.servant_2.np_charge
				self.round3_servant2_np.setText('宝具: ' + str(round(np_charge, 2)) + '%')
			if self.battle_config.servant_3.health > 0:
				np_charge = self.battle_config.servant_3.np_charge
				self.round3_servant3_np.setText('宝具: ' + str(round(np_charge, 2)) + '%')
			if self.battle_config.enemy_31.health_start > 0:
				health = self.battle_config.enemy_31.health
				self.round3_enemy1_health.setText('血量: ' + str(int(health)))
			if self.battle_config.enemy_32.health_start > 0:
				health = self.battle_config.enemy_32.health
				self.round3_enemy2_health.setText('血量: ' + str(int(health)))
			if self.battle_config.enemy_33.health_start > 0:
				health = self.battle_config.enemy_33.health
				self.round3_enemy3_health.setText('血量: ' + str(int(health)))

	# 显示御主图片(头像,技能图标)
	def show_master_pic(self, battle_round):
		if battle_round == 1:
			# 设置魔术礼装头像
			icon = QIcon()
			pixmap = QPixmap(self.battle_config.master.pic_path)
			icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
			self.round1_master_pic.setIcon(icon)

			# 设置魔术礼装技能使用情况
			icon = QIcon()
			pixmap = QPixmap(self.battle_config.master.skill_pic[0])
			icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
			self.round1_master_skill1.setIcon(icon)

			icon = QIcon()
			pixmap = QPixmap(self.battle_config.master.skill_pic[1])
			icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
			self.round1_master_skill2.setIcon(icon)

			icon = QIcon()
			pixmap = QPixmap(self.battle_config.master.skill_pic[2])
			icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
			self.round1_master_skill3.setIcon(icon)
		elif battle_round == 2:
			# 设置魔术礼装头像
			icon = QIcon()
			pixmap = QPixmap(self.battle_config.master.pic_path)
			icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
			self.round2_master_pic.setIcon(icon)

			# 设置魔术礼装技能使用情况
			icon = QIcon()
			pixmap = QPixmap(self.battle_config.master.skill_pic[0])
			icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
			self.round2_master_skill1.setIcon(icon)

			icon = QIcon()
			pixmap = QPixmap(self.battle_config.master.skill_pic[1])
			icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
			self.round2_master_skill2.setIcon(icon)

			icon = QIcon()
			pixmap = QPixmap(self.battle_config.master.skill_pic[2])
			icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
			self.round2_master_skill3.setIcon(icon)
		elif battle_round == 3:
			# 设置魔术礼装头像
			icon = QIcon()
			pixmap = QPixmap(self.battle_config.master.pic_path)
			icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
			self.round3_master_pic.setIcon(icon)

			# 设置魔术礼装技能使用情况
			icon = QIcon()
			pixmap = QPixmap(self.battle_config.master.skill_pic[0])
			icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
			self.round3_master_skill1.setIcon(icon)

			icon = QIcon()
			pixmap = QPixmap(self.battle_config.master.skill_pic[1])
			icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
			self.round3_master_skill2.setIcon(icon)

			icon = QIcon()
			pixmap = QPixmap(self.battle_config.master.skill_pic[2])
			icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
			self.round3_master_skill3.setIcon(icon)

	# 显示从者图片(头像,技能图标)
	def show_servant_pic(self, battle_round, servant_order):
		if battle_round == 1:
			if servant_order == 1:
				# 设置从者1头像
				icon = QIcon()
				pixmap = QPixmap(self.battle_config.servant_1.pic_path)
				icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
				self.round1_servant1_pic.setIcon(icon)

				# 设置从者1技能使用情况
				icon = QIcon()
				pixmap = QPixmap(self.battle_config.servant_1.skill_pic[0])
				icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
				self.round1_servant1_skill1.setIcon(icon)

				icon = QIcon()
				pixmap = QPixmap(self.battle_config.servant_1.skill_pic[1])
				icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
				self.round1_servant1_skill2.setIcon(icon)

				icon = QIcon()
				pixmap = QPixmap(self.battle_config.servant_1.skill_pic[2])
				icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
				self.round1_servant1_skill3.setIcon(icon)

			elif servant_order == 2:
				# 设置从者2头像
				icon = QIcon()
				pixmap = QPixmap(self.battle_config.servant_2.pic_path)
				icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
				self.round1_servant2_pic.setIcon(icon)

				# 设置从者2技能使用情况
				icon = QIcon()
				pixmap = QPixmap(self.battle_config.servant_2.skill_pic[0])
				icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
				self.round1_servant2_skill1.setIcon(icon)

				icon = QIcon()
				pixmap = QPixmap(self.battle_config.servant_2.skill_pic[1])
				icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
				self.round1_servant2_skill2.setIcon(icon)

				icon = QIcon()
				pixmap = QPixmap(self.battle_config.servant_2.skill_pic[2])
				icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
				self.round1_servant2_skill3.setIcon(icon)

			elif servant_order == 3:
				# 设置从者3头像
				icon = QIcon()
				pixmap = QPixmap(self.battle_config.servant_3.pic_path)
				icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
				self.round1_servant3_pic.setIcon(icon)

				# 设置从者3技能使用情况
				icon = QIcon()
				pixmap = QPixmap(self.battle_config.servant_3.skill_pic[0])
				icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
				self.round1_servant3_skill1.setIcon(icon)

				icon = QIcon()
				pixmap = QPixmap(self.battle_config.servant_3.skill_pic[1])
				icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
				self.round1_servant3_skill2.setIcon(icon)

				icon = QIcon()
				pixmap = QPixmap(self.battle_config.servant_3.skill_pic[2])
				icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
				self.round1_servant3_skill3.setIcon(icon)
		elif battle_round == 2:
			if servant_order == 1:
				# 设置从者1头像
				icon = QIcon()
				pixmap = QPixmap(self.battle_config.servant_1.pic_path)
				icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
				self.round2_servant1_pic.setIcon(icon)

				# 设置从者1技能使用情况
				icon = QIcon()
				pixmap = QPixmap(self.battle_config.servant_1.skill_pic[0])
				icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
				self.round2_servant1_skill1.setIcon(icon)

				icon = QIcon()
				pixmap = QPixmap(self.battle_config.servant_1.skill_pic[1])
				icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
				self.round2_servant1_skill2.setIcon(icon)

				icon = QIcon()
				pixmap = QPixmap(self.battle_config.servant_1.skill_pic[2])
				icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
				self.round2_servant1_skill3.setIcon(icon)

			elif servant_order == 2:
				# 设置从者2头像
				icon = QIcon()
				pixmap = QPixmap(self.battle_config.servant_2.pic_path)
				icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
				self.round2_servant2_pic.setIcon(icon)

				# 设置从者2技能使用情况
				icon = QIcon()
				pixmap = QPixmap(self.battle_config.servant_2.skill_pic[0])
				icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
				self.round2_servant2_skill1.setIcon(icon)

				icon = QIcon()
				pixmap = QPixmap(self.battle_config.servant_2.skill_pic[1])
				icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
				self.round2_servant2_skill2.setIcon(icon)

				icon = QIcon()
				pixmap = QPixmap(self.battle_config.servant_2.skill_pic[2])
				icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
				self.round2_servant2_skill3.setIcon(icon)

			elif servant_order == 3:
				# 设置从者3头像
				icon = QIcon()
				pixmap = QPixmap(self.battle_config.servant_3.pic_path)
				icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
				self.round2_servant3_pic.setIcon(icon)

				# 设置从者3技能使用情况
				icon = QIcon()
				pixmap = QPixmap(self.battle_config.servant_3.skill_pic[0])
				icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
				self.round2_servant3_skill1.setIcon(icon)

				icon = QIcon()
				pixmap = QPixmap(self.battle_config.servant_3.skill_pic[1])
				icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
				self.round2_servant3_skill2.setIcon(icon)

				icon = QIcon()
				pixmap = QPixmap(self.battle_config.servant_3.skill_pic[2])
				icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
				self.round2_servant3_skill3.setIcon(icon)

		elif battle_round == 3:
			if servant_order == 1:
				# 设置从者1头像
				icon = QIcon()
				pixmap = QPixmap(self.battle_config.servant_1.pic_path)
				icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
				self.round3_servant1_pic.setIcon(icon)

				# 设置从者1技能使用情况
				icon = QIcon()
				pixmap = QPixmap(self.battle_config.servant_1.skill_pic[0])
				icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
				self.round3_servant1_skill1.setIcon(icon)

				icon = QIcon()
				pixmap = QPixmap(self.battle_config.servant_1.skill_pic[1])
				icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
				self.round3_servant1_skill2.setIcon(icon)

				icon = QIcon()
				pixmap = QPixmap(self.battle_config.servant_1.skill_pic[2])
				icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
				self.round3_servant1_skill3.setIcon(icon)

			elif servant_order == 2:
				# 设置从者2头像
				icon = QIcon()
				pixmap = QPixmap(self.battle_config.servant_2.pic_path)
				icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
				self.round3_servant2_pic.setIcon(icon)

				# 设置从者2技能使用情况
				icon = QIcon()
				pixmap = QPixmap(self.battle_config.servant_2.skill_pic[0])
				icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
				self.round3_servant2_skill1.setIcon(icon)

				icon = QIcon()
				pixmap = QPixmap(self.battle_config.servant_2.skill_pic[1])
				icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
				self.round3_servant2_skill2.setIcon(icon)

				icon = QIcon()
				pixmap = QPixmap(self.battle_config.servant_2.skill_pic[2])
				icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
				self.round3_servant2_skill3.setIcon(icon)

			elif servant_order == 3:
				# 设置从者3头像
				icon = QIcon()
				pixmap = QPixmap(self.battle_config.servant_3.pic_path)
				icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
				self.round3_servant3_pic.setIcon(icon)

				# 设置从者3技能使用情况
				icon = QIcon()
				pixmap = QPixmap(self.battle_config.servant_3.skill_pic[0])
				icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
				self.round3_servant3_skill1.setIcon(icon)

				icon = QIcon()
				pixmap = QPixmap(self.battle_config.servant_3.skill_pic[1])
				icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
				self.round3_servant3_skill2.setIcon(icon)

				icon = QIcon()
				pixmap = QPixmap(self.battle_config.servant_3.skill_pic[2])
				icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
				self.round3_servant3_skill3.setIcon(icon)

	# 显示回合图片(从者+御主)
	def show_battle_state_pic(self, battle_round):
		self.show_master_pic(battle_round)
		for servant_order in range(1, 4):
			self.show_servant_pic(battle_round, servant_order)

	# 从者使用宝具
	def servant_use_np(self, battle_round, servant_order):
		if self.battle_config.battle_round != battle_round:
			print('当前回合与设定回合不相符, 请检查程序')
			return

		if servant_order == 1:
			servant = self.battle_config.servant_1
		elif servant_order == 2:
			servant = self.battle_config.servant_2
		elif servant_order == 3:
			servant = self.battle_config.servant_3
		else:
			return

		if servant.np_charge < 99:
			text = '当前从者NP不足以发动宝具, 是否强行发动?'
			reply = QMessageBox.question(self, '提  醒', text, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
			if reply == QMessageBox.No:
				return

		servant_np = servant.np
		text = ''
		for i in servant_np['宝具效果'].values:
			text += str(i) + '\n'

		if text == '':
			text = '当前宝具效果暂不支持或对速刷无帮助'
		else:
			text = '宝具效果:\n\n' + text + '\n是否确定使用?'

		if self.box_skill_confirm.checkState() != 0:
			reply = QMessageBox.question(self, '提  醒', text, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
			if reply == QMessageBox.No:
				return

		self.current_used_name = '宝具'
		if servant_order == 1:
			servant = self.battle_config.servant_1
			self.current_used_role = '从者1'
		elif servant_order == 2:
			servant = self.battle_config.servant_2
			self.current_used_role = '从者2'
		elif servant_order == 3:
			servant = self.battle_config.servant_3
			self.current_used_role = '从者3'
		else:
			return
		# 设置OC level
		if servant.np_charge < 200:
			oc_level_add = 0
		elif servant.np_charge < 300:
			oc_level_add = 1
		else:
			oc_level_add = 2
		servant.oc_level = self.battle_config.oc_level + oc_level_add
		self.battle_config.oc_level += 1
		np_type = servant.np_type

		if '单体' in np_type:
			role1 = self.battle_config.enemy_1
			role2 = self.battle_config.enemy_2
			role3 = self.battle_config.enemy_3
			self.select_target_inverse_window.close()
			self.select_target_inverse_window.show()
			window = self.select_target_inverse_window
		else:
			self.set_target(0)
			return

		icon = QIcon()
		if role1.health > 0:
			window.btn_1.setEnabled(True)
		else:
			window.btn_1.setEnabled(False)
		icon.addPixmap(QPixmap(role1.pic_path), QIcon.Normal, QIcon.Off)
		window.btn_1.setIcon(icon)

		icon = QIcon()
		if role2.health > 0:
			window.btn_2.setEnabled(True)
		else:
			window.btn_2.setEnabled(False)
		icon.addPixmap(QPixmap(role2.pic_path), QIcon.Normal, QIcon.Off)
		window.btn_2.setIcon(icon)

		icon = QIcon()
		if role3.health > 0:
			window.btn_3.setEnabled(True)
		else:
			window.btn_3.setEnabled(False)
		icon.addPixmap(QPixmap(role3.pic_path), QIcon.Normal, QIcon.Off)
		window.btn_3.setIcon(icon)

	# 撤销
	def battle_reset(self):
		if len(self.battle_config_list) <= 1:
			print('无法撤回')
			return
		print('正在撤回')
		self.battle_config_list.pop()
		self.battle_config = deepcopy(self.battle_config_list[-1])
		self.show_battle_state_all_nosave(pic=True)

	# 开始下一回合
	def next_round(self):
		if self.battle_config.enemy_1.health > 0 or self.battle_config.enemy_2.health > 0 or self.battle_config.enemy_3.health > 0:
			text = '当前回合有敌人未击杀, 是否确认开启下一回合?'
			reply = QMessageBox.information(self, '提 醒', text, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
			if reply == QMessageBox.No:
				return
		# 计算每回合NP增加
		self.battle_config.round_end()

		# 开始下一回合
		battle_round = self.battle_config.battle_round + 1
		if battle_round <= 3:
			self.battle_config.round_start(battle_round)
			if self.battle_config.enemy_1.health <= 0 and self.battle_config.enemy_2.health <= 0 and self.battle_config.enemy_3.health <= 0:
				text = '恭喜! 当前剧本可以完成速刷'
				QMessageBox.information(self, '提 醒', text)
				return
			self.show_battle_state_all(pic=True)
			self.set_button_enable_round(battle_round)
			self.battle_config.battle_strategy += '\n\n第' + str(battle_round) + '回合：'
		elif battle_round > 3:
			QMessageBox.information(self, '提 醒', '恭喜! 当前剧本可以完成速刷')

	# 停止所有技能的使用(用在使用宝具后)
	def disable_round_skill(self):
		round1 = False
		round2 = False
		round3 = False
		self.round1_servant1_skill1.setEnabled(round1)
		self.round1_servant1_skill2.setEnabled(round1)
		self.round1_servant1_skill3.setEnabled(round1)
		self.round1_servant2_skill1.setEnabled(round1)
		self.round1_servant2_skill2.setEnabled(round1)
		self.round1_servant2_skill3.setEnabled(round1)
		self.round1_servant3_skill1.setEnabled(round1)
		self.round1_servant3_skill2.setEnabled(round1)
		self.round1_servant3_skill3.setEnabled(round1)
		self.round1_master_skill1.setEnabled(round1)
		self.round1_master_skill2.setEnabled(round1)
		self.round1_master_skill3.setEnabled(round1)

		self.round2_servant1_skill1.setEnabled(round2)
		self.round2_servant1_skill2.setEnabled(round2)
		self.round2_servant1_skill3.setEnabled(round2)
		self.round2_servant2_skill1.setEnabled(round2)
		self.round2_servant2_skill2.setEnabled(round2)
		self.round2_servant2_skill3.setEnabled(round2)
		self.round2_servant3_skill1.setEnabled(round2)
		self.round2_servant3_skill2.setEnabled(round2)
		self.round2_servant3_skill3.setEnabled(round2)
		self.round2_master_skill1.setEnabled(round2)
		self.round2_master_skill2.setEnabled(round2)
		self.round2_master_skill3.setEnabled(round2)

		self.round3_servant1_skill1.setEnabled(round3)
		self.round3_servant1_skill2.setEnabled(round3)
		self.round3_servant1_skill3.setEnabled(round3)
		self.round3_servant2_skill1.setEnabled(round3)
		self.round3_servant2_skill2.setEnabled(round3)
		self.round3_servant2_skill3.setEnabled(round3)
		self.round3_servant3_skill1.setEnabled(round3)
		self.round3_servant3_skill2.setEnabled(round3)
		self.round3_servant3_skill3.setEnabled(round3)
		self.round3_master_skill1.setEnabled(round3)
		self.round3_master_skill2.setEnabled(round3)
		self.round3_master_skill3.setEnabled(round3)

	# 确认每回合可以使用的按钮
	def set_button_enable_round(self, battle_round):
		round1 = False
		round2 = False
		round3 = False
		# 首先禁用所有按钮
		self.round1_servant1_np.setEnabled(round1)
		self.round1_servant2_np.setEnabled(round1)
		self.round1_servant3_np.setEnabled(round1)
		self.round1_servant1_skill1.setEnabled(round1)
		self.round1_servant1_skill2.setEnabled(round1)
		self.round1_servant1_skill3.setEnabled(round1)
		self.round1_servant2_skill1.setEnabled(round1)
		self.round1_servant2_skill2.setEnabled(round1)
		self.round1_servant2_skill3.setEnabled(round1)
		self.round1_servant3_skill1.setEnabled(round1)
		self.round1_servant3_skill2.setEnabled(round1)
		self.round1_servant3_skill3.setEnabled(round1)
		self.round1_master_skill1.setEnabled(round1)
		self.round1_master_skill2.setEnabled(round1)
		self.round1_master_skill3.setEnabled(round1)
		self.round1_bar_random.setEnabled(round1)
		# self.btn_round1_next.setEnabled(round1)

		self.round2_servant1_np.setEnabled(round2)
		self.round2_servant2_np.setEnabled(round2)
		self.round2_servant3_np.setEnabled(round2)
		self.round2_servant1_skill1.setEnabled(round2)
		self.round2_servant1_skill2.setEnabled(round2)
		self.round2_servant1_skill3.setEnabled(round2)
		self.round2_servant2_skill1.setEnabled(round2)
		self.round2_servant2_skill2.setEnabled(round2)
		self.round2_servant2_skill3.setEnabled(round2)
		self.round2_servant3_skill1.setEnabled(round2)
		self.round2_servant3_skill2.setEnabled(round2)
		self.round2_servant3_skill3.setEnabled(round2)
		self.round2_master_skill1.setEnabled(round2)
		self.round2_master_skill2.setEnabled(round2)
		self.round2_master_skill3.setEnabled(round2)
		self.round2_bar_random.setEnabled(round2)
		# self.btn_round2_next.setEnabled(round2)

		self.round3_servant1_np.setEnabled(round3)
		self.round3_servant2_np.setEnabled(round3)
		self.round3_servant3_np.setEnabled(round3)
		self.round3_servant1_skill1.setEnabled(round3)
		self.round3_servant1_skill2.setEnabled(round3)
		self.round3_servant1_skill3.setEnabled(round3)
		self.round3_servant2_skill1.setEnabled(round3)
		self.round3_servant2_skill2.setEnabled(round3)
		self.round3_servant2_skill3.setEnabled(round3)
		self.round3_servant3_skill1.setEnabled(round3)
		self.round3_servant3_skill2.setEnabled(round3)
		self.round3_servant3_skill3.setEnabled(round3)
		self.round3_master_skill1.setEnabled(round3)
		self.round3_master_skill2.setEnabled(round3)
		self.round3_master_skill3.setEnabled(round3)
		self.round3_bar_random.setEnabled(round3)

		if battle_round == 1:
			if self.battle_config.servant_1.skill_used[0] == 0:
				self.round1_servant1_skill1.setEnabled(True)
			if self.battle_config.servant_1.skill_used[1] == 0:
				self.round1_servant1_skill2.setEnabled(True)
			if self.battle_config.servant_1.skill_used[2] == 0:
				self.round1_servant1_skill3.setEnabled(True)
			if self.battle_config.servant_2.skill_used[0] == 0:
				self.round1_servant2_skill1.setEnabled(True)
			if self.battle_config.servant_2.skill_used[1] == 0:
				self.round1_servant2_skill2.setEnabled(True)
			if self.battle_config.servant_2.skill_used[2] == 0:
				self.round1_servant2_skill3.setEnabled(True)
			if self.battle_config.servant_3.skill_used[0] == 0:
				self.round1_servant3_skill1.setEnabled(True)
			if self.battle_config.servant_3.skill_used[1] == 0:
				self.round1_servant3_skill2.setEnabled(True)
			if self.battle_config.servant_3.skill_used[2] == 0:
				self.round1_servant3_skill3.setEnabled(True)
			if self.battle_config.master.skill_used[0] == 0:
				self.round1_master_skill1.setEnabled(True)
			if self.battle_config.master.skill_used[1] == 0:
				self.round1_master_skill2.setEnabled(True)
			if self.battle_config.master.skill_used[2] == 0:
				self.round1_master_skill3.setEnabled(True)
			self.round1_label_random.setEnabled(True)
			self.round1_bar_random.setEnabled(True)
			# self.btn_round1_next.setEnabled(True)
			self.round1_servant1_np.setEnabled(True)
			self.round1_servant2_np.setEnabled(True)
			self.round1_servant3_np.setEnabled(True)
		elif battle_round == 2:
			if self.battle_config.servant_1.skill_used[0] == 0:
				self.round2_servant1_skill1.setEnabled(True)
			if self.battle_config.servant_1.skill_used[1] == 0:
				self.round2_servant1_skill2.setEnabled(True)
			if self.battle_config.servant_1.skill_used[2] == 0:
				self.round2_servant1_skill3.setEnabled(True)
			if self.battle_config.servant_2.skill_used[0] == 0:
				self.round2_servant2_skill1.setEnabled(True)
			if self.battle_config.servant_2.skill_used[1] == 0:
				self.round2_servant2_skill2.setEnabled(True)
			if self.battle_config.servant_2.skill_used[2] == 0:
				self.round2_servant2_skill3.setEnabled(True)
			if self.battle_config.servant_3.skill_used[0] == 0:
				self.round2_servant3_skill1.setEnabled(True)
			if self.battle_config.servant_3.skill_used[1] == 0:
				self.round2_servant3_skill2.setEnabled(True)
			if self.battle_config.servant_3.skill_used[2] == 0:
				self.round2_servant3_skill3.setEnabled(True)
			if self.battle_config.master.skill_used[0] == 0:
				self.round2_master_skill1.setEnabled(True)
			if self.battle_config.master.skill_used[1] == 0:
				self.round2_master_skill2.setEnabled(True)
			if self.battle_config.master.skill_used[2] == 0:
				self.round2_master_skill3.setEnabled(True)
			self.round2_label_random.setEnabled(True)
			self.round2_bar_random.setEnabled(True)
			# self.btn_round2_next.setEnabled(True)
			self.round2_servant1_np.setEnabled(True)
			self.round2_servant2_np.setEnabled(True)
			self.round2_servant3_np.setEnabled(True)
		elif battle_round == 3:
			if self.battle_config.servant_1.skill_used[0] == 0:
				self.round3_servant1_skill1.setEnabled(True)
			if self.battle_config.servant_1.skill_used[1] == 0:
				self.round3_servant1_skill2.setEnabled(True)
			if self.battle_config.servant_1.skill_used[2] == 0:
				self.round3_servant1_skill3.setEnabled(True)
			if self.battle_config.servant_2.skill_used[0] == 0:
				self.round3_servant2_skill1.setEnabled(True)
			if self.battle_config.servant_2.skill_used[1] == 0:
				self.round3_servant2_skill2.setEnabled(True)
			if self.battle_config.servant_2.skill_used[2] == 0:
				self.round3_servant2_skill3.setEnabled(True)
			if self.battle_config.servant_3.skill_used[0] == 0:
				self.round3_servant3_skill1.setEnabled(True)
			if self.battle_config.servant_3.skill_used[1] == 0:
				self.round3_servant3_skill2.setEnabled(True)
			if self.battle_config.servant_3.skill_used[2] == 0:
				self.round3_servant3_skill3.setEnabled(True)
			if self.battle_config.master.skill_used[0] == 0:
				self.round3_master_skill1.setEnabled(True)
			if self.battle_config.master.skill_used[1] == 0:
				self.round3_master_skill2.setEnabled(True)
			if self.battle_config.master.skill_used[2] == 0:
				self.round3_master_skill3.setEnabled(True)
			self.round3_label_random.setEnabled(True)
			self.round3_bar_random.setEnabled(True)
			self.round3_servant1_np.setEnabled(True)
			self.round3_servant2_np.setEnabled(True)
			self.round3_servant3_np.setEnabled(True)

	# 切换队伍设定/模拟战斗功能
	def set_button_enable(self, state):
		if state is True:
			btn_open = True
			btn_close = False
		else:
			btn_open = False
			btn_close = True
		# 禁止全部接口
		self.btn_select_servant_1.setEnabled(btn_close)
		self.btn_select_servant_2.setEnabled(btn_close)
		self.btn_select_servant_3.setEnabled(btn_close)
		self.btn_select_servant_4.setEnabled(btn_close)
		self.btn_select_servant_5.setEnabled(btn_close)
		self.btn_select_servant_6.setEnabled(btn_close)
		self.btn_select_costume_1.setEnabled(btn_close)
		self.btn_select_costume_2.setEnabled(btn_close)
		self.btn_select_costume_3.setEnabled(btn_close)
		self.btn_select_costume_4.setEnabled(btn_close)
		self.btn_select_costume_5.setEnabled(btn_close)
		self.btn_select_costume_6.setEnabled(btn_close)
		self.btn_select_master.setEnabled(btn_close)
		self.btn_set_progress.setEnabled(btn_close)
		self.btn_choose_level.setEnabled(btn_close)
		self.btn_confirm_team.setEnabled(btn_close)

		# 开启从者/敌人战斗状态图标
		self.btn_change_team.setEnabled(btn_open)
		self.btn_output_strategy.setEnabled(btn_open)
		self.round1_servant1_pic.setEnabled(btn_open)
		self.round1_servant2_pic.setEnabled(btn_open)
		self.round1_servant3_pic.setEnabled(btn_open)
		self.round1_enemy1_pic.setEnabled(btn_open)
		self.round1_enemy2_pic.setEnabled(btn_open)
		self.round1_enemy3_pic.setEnabled(btn_open)
		self.round1_master_pic.setEnabled(btn_open)

		self.round2_servant1_pic.setEnabled(btn_open)
		self.round2_servant2_pic.setEnabled(btn_open)
		self.round2_servant3_pic.setEnabled(btn_open)
		self.round2_enemy1_pic.setEnabled(btn_open)
		self.round2_enemy2_pic.setEnabled(btn_open)
		self.round2_enemy3_pic.setEnabled(btn_open)
		self.round2_master_pic.setEnabled(btn_open)

		self.round3_servant1_pic.setEnabled(btn_open)
		self.round3_servant2_pic.setEnabled(btn_open)
		self.round3_servant3_pic.setEnabled(btn_open)
		self.round3_enemy1_pic.setEnabled(btn_open)
		self.round3_enemy2_pic.setEnabled(btn_open)
		self.round3_enemy3_pic.setEnabled(btn_open)
		self.round3_master_pic.setEnabled(btn_open)
		# 重置随机数:
		self.round1_bar_random.setValue(0.9)
		self.round2_bar_random.setValue(0.9)
		self.round3_bar_random.setValue(0.9)

	# 输出战斗操作
	def output_strategy(self):
		directory = QFileDialog.getSaveFileName(self, "getSaveFileName", "./", "Text Files (*.txt)")
		if len(directory[0]) > 0:
			self.battle_strategy = copy(self.battle_config.battle_strategy)
			text = self.battle_config.battle_strategy
			text = text.replace('∅', '')
			text = text.replace('nan', '')
			text = text.replace('对己方单体', '己方单体')
			text = text.replace('对敌方单体', '敌方单体')
			text = text.replace('己方单体的', '己方单体')
			text = text.replace('敌方单体的', '敌方单体')
			text = text.replace('己方单体', '')
			text = text.replace('敌方单体', '')
			with open(directory[0], "w", encoding='utf-8-sig') as f:
				f.write(text)
			QMessageBox.information(self, '提 醒', '导出成功')


if __name__ == '__main__':
	if os.path.isfile("upgrade.bat"):
		os.remove("upgrade.bat")
	app = QApplication(sys.argv)
	# 实例化主窗口
	main = Ui_MainWindow()
	main.show()
	sys.exit(app.exec_())