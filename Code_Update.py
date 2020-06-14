import sys
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
import UpdateUi
import json
import time
import requests
import os
import shutil
import zipfile
import subprocess


# 编写bat脚本，删除旧程序，运行新程序



class Ui_Update(QDialog, UpdateUi.Ui_Dialog):
	def __init__(self):

		super(Ui_Update, self).__init__()
		self.setupUi(self)
		# github项目名称
		self.git_name_data = 'Fgo_teamup_database_beta_v1.31'
		self.git_name_software = 'Fgo_teamup_software'
		# 获取本地时间
		self.local_time = time.localtime()
		# 获取本地版本数据
		data = {"data_time": "2020-01-01T00:00:00Z", "software_time": "2020-01-01T00:00:00Z"}
		self.data = data
		self.data_time_old = data['data_time']
		self.data_time_new = data['data_time']
		self.software_time_old = data['data_time']
		self.software_time_new = data['data_time']
		# 获取本地版本数据
		self.get_local_version()
		# 绑定按钮
		self.btn_data_update.clicked.connect(self.check_data)
		self.btn_data_confirm.clicked.connect(self.download_data_update)
		self.btn_remove_backup.clicked.connect(self.remove_backup)
		'''
		self.btn_software_update.clicked.connect(self.check_software)
		self.btn_software_confirm.clicked.connect(self.download_software_update)
		'''

	@staticmethod
	def write_restart_cmd():
		b = open("upgrade.bat", 'w')
		TempList = "@echo off\n"  # 关闭bat脚本的输出
		TempList += "if not exist .\Fgo_teamup_software-master\Fgo_Teamup.exe exit\n"  # 新文件不存在,退出脚本执行
		TempList += "ping -n 5 127.0.0.1>nul\n"  # 3秒后删除旧程序（3秒后程序已运行结束，不延时的话，会提示被占用，无法删除）
		TempList += "del Fgo_Teamup.exe\n"  # 删除当前文件
		TempList += "move .\Fgo_teamup_software-master\Fgo_Teamup.exe\n"  # 删除当前文件
		TempList += "rd Fgo_teamup_software-master\n"  # 启动新程序
		TempList += "start Fgo_Teamup.exe"  # 启动新程序
		b.write(TempList)
		b.close()
		subprocess.Popen("upgrade.bat")
		sys.exit()  # 进行升级，退出此程序

	def remove_backup(self):
		text = '警告! 此操作将会清空所有的数据备份文件, 是否继续?\nPS: 建议仅在当前数据库无明显错误时清空备份'
		reply = QMessageBox.warning(self, '警  告', text, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if reply == QMessageBox.No:
			return
		if os.path.exists('backup'):
			shutil.rmtree('backup')
			text = '数据备份文件已全部清除。'
			QMessageBox.information(self, '提  示', text)
		else:
			text = '没有可清除的备份文件。'
			QMessageBox.information(self, '提  示', text)

	def get_local_version(self):
		# 获取本地版本数据
		try:
			with open('data/version.json', 'r', encoding='utf-8') as file:
				data = json.load(file)
		except Exception:
			return

		if 'data_time' in data:
			self.data.update({'data_time': data['data_time']})
			self.data_time_old = data['data_time']
		'''
		if 'software_time' in data:
			self.data.update({'software_time': data['software_time']})
			self.software_time_old = data['software_time']
		'''
		# 显示当前版本
		text = self.data_time_old
		self.label_data_old.setText(self.change_time_formula(text))
		# text = self.software_time_old
		# self.label_software_old.setText(self.change_time_formula(text))

	@staticmethod
	def change_time_formula(text):
		text = text.replace('T', ' ')
		text = text.replace('Z', '')
		return text

	def check_data(self):
		self.label_data_new.setText('')
		self.btn_data_update.setEnabled(False)
		self.btn_data_confirm.setEnabled(False)
		self.btn_remove_backup.setEnabled(False)
		# self.btn_data_cancle.setEnabled(False)
		# 其他的三个按钮, 保留其初始状态
		'''
		btn_update_state = self.btn_software_update.isEnabled()
		btn_confirm = self.btn_software_confirm.isEnabled()
		# btn_cancle = self.btn_software_cancle.isEnabled()
		self.btn_software_update.setEnabled(False)
		self.btn_software_confirm.setEnabled(False)
		# self.btn_software_cancle.setEnabled(False)
		'''
		# 开始更新
		self.label_data_state.setText('正在检查更新, 请稍后...')
		QApplication.processEvents()
		state = self.check_data_update()
		time.sleep(1)
		if state == 'True':
			self.label_data_state.setText('检测到新版数据库, 可以更新')
			self.btn_data_confirm.setText('开始更新')
			self.label_data_new.setText(self.change_time_formula(self.data_time_new))
			self.btn_data_confirm.setEnabled(True)
			self.btn_remove_backup.setEnabled(True)
			# self.btn_data_cancle.setEnabled(True)
			self.btn_data_update.setEnabled(True)
		elif state == 'False':
			self.label_data_state.setText('当前版本为最新版本')
			self.btn_data_confirm.setText('重新下载')
			self.label_data_new.setText(self.change_time_formula(self.data_time_new))
			self.btn_data_confirm.setEnabled(True)
			self.btn_remove_backup.setEnabled(True)
			# self.btn_data_cancle.setEnabled(True)
			self.btn_data_update.setEnabled(True)
		else:
			self.btn_data_confirm.setText('确  认')
			self.label_data_state.setText(state)
			self.label_data_new.setText('获取失败')
			self.btn_data_confirm.setEnabled(False)
			self.btn_remove_backup.setEnabled(True)
			# self.btn_data_cancle.setEnabled(False)
			self.btn_data_update.setEnabled(True)

		# 还原三个按钮的状态
		'''
		self.btn_software_update.setEnabled(btn_update_state)
		self.btn_software_confirm.setEnabled(btn_confirm)
		# self.btn_software_cancle.setEnabled(btn_cancle)
		'''

	def check_data_update(self):
		url = 'https://api.github.com/repos/lsq5i5j/' + self.git_name_data
		print(url)
		try:
			r = requests.get(url).json()
		except:
			return '无法和服务器建立连接, 请稍后再试'
		try:
			self.data_time_new = r['updated_at']
		except:
			return '当前版本软件的数据库已不再维护, 请下载新版本'
		time_old = time.strptime(self.data_time_old, "%Y-%m-%dT%H:%M:%SZ")
		time_new = time.strptime(self.data_time_new, "%Y-%m-%dT%H:%M:%SZ")
		if time_new > time_old:
			return 'True'
		else:
			return 'False'

	def download_data_update(self):
		# 禁止按钮
		self.btn_remove_backup.setEnabled(False)
		self.btn_data_confirm.setEnabled(False)
		self.btn_data_update.setEnabled(False)
		# 首先下载文件
		self.label_data_state.setText('开始下载...')
		QApplication.processEvents()
		url = 'https://github.com/lsq5i5j/' + self.git_name_data + '/archive/master.zip'
		self.download_file('data_temp.zip', url)
		# 将之前保存的数据储存到backup文件夹下, 并按照日期保存

		folder = time.strftime('backup/%Y-%m-%d', self.local_time)
		i = 0
		while True:
			if i == 0:
				path = folder
			else:
				path = folder + '_' + str(i)
			i += 1

			if not os.path.exists(path):
				os.makedirs(path)
				break
		# 移动文件到backup文件夹
		try:
			shutil.move('data', path)
			shutil.move('pic', path)
		except IOError as e:
			print("Unable to copy file. %s" % e)
		except:
			print("Unexpected error:", sys.exc_info())
		# 解压缩下载的文件
		z = zipfile.ZipFile('data_temp.zip', 'r')
		z.extractall()
		z.close()
		# 将文件放入对应位置
		try:
			shutil.move(self.git_name_data + '-master/data', '.')
			shutil.move(self.git_name_data + '-master/pic', '.')
		except IOError as e:
			print("Unable to copy file. %s" % e)
		except:
			print("Unexpected error:", sys.exc_info())
		# 写入新的数据库的版本号
		print(self.data)
		self.data["data_time"] = self.data_time_new
		print(self.data)
		with open('data/version.json', 'w', encoding='utf-8') as file:
			json.dump(self.data, file)
		# 删除临时文件
		os.remove('data_temp.zip')
		shutil.rmtree(self.git_name_data + '-master')
		# 复制练度文件
		if os.path.exists(path + '/data/save/servant_data_save.csv'):
			shutil.copy(path + '/data/save/servant_data_save.csv', 'data/save/servant_data_save.csv')
		if os.path.exists(path + '/data/save/master_data_save.csv'):
			shutil.copy(path + '/data/save/master_data_save.csv', 'data/save/master_data_save.csv')
		time.sleep(1)
		self.label_data_state.setText('更新完成!')
		QApplication.processEvents()
		self.btn_remove_backup.setEnabled(True)
		self.btn_data_confirm.setEnabled(True)
		self.btn_data_update.setEnabled(True)
		text = '更新完成, 请重新启动程序来更新数据。是否关闭程序？'
		reply = QMessageBox.question(self, '提  示', text, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
		if reply == QMessageBox.Yes:
			sys.exit()


	def check_software(self):
		self.label_software_new.setText('')
		self.btn_software_update.setEnabled(False)
		self.btn_software_confirm.setEnabled(False)
		# self.btn_software_cancle.setEnabled(False)
		# 其他的三个按钮, 保留其初始状态
		btn_update_state = self.btn_data_update.isEnabled()
		btn_confirm = self.btn_data_confirm.isEnabled()
		# btn_cancle = self.btn_data_cancle.isEnabled()
		self.btn_data_update.setEnabled(False)
		self.btn_data_confirm.setEnabled(False)
		# self.btn_data_cancle.setEnabled(False)
		# 开始更新
		self.label_software_state.setText('正在检查更新, 请稍后...')
		QApplication.processEvents()
		state = self.check_software_update()
		time.sleep(1)
		if state == 'True':
			self.label_software_state.setText('检测到新版软件, 可以更新')
			self.btn_software_confirm.setText('开始更新')
			self.label_software_new.setText(self.change_time_formula(self.software_time_new))
			self.btn_software_confirm.setEnabled(True)
			# self.btn_software_cancle.setEnabled(True)
			self.btn_software_update.setEnabled(True)
		elif state == 'False':
			self.label_software_state.setText('当前版本为最新版本')
			self.btn_software_confirm.setText('重新下载')
			self.label_software_new.setText(self.change_time_formula(self.software_time_new))
			self.btn_software_confirm.setEnabled(True)
			# self.btn_software_cancle.setEnabled(True)
			self.btn_software_update.setEnabled(True)
		else:
			self.btn_software_confirm.setText('确  认')
			self.label_software_state.setText(state)
			self.label_software_new.setText('获取失败')
			self.btn_software_confirm.setEnabled(False)
			# self.btn_software_cancle.setEnabled(False)
			self.btn_software_update.setEnabled(True)

		# 还原三个按钮的状态
		self.btn_data_update.setEnabled(btn_update_state)
		self.btn_data_confirm.setEnabled(btn_confirm)
		# self.btn_data_cancle.setEnabled(btn_cancle)

	def check_software_update(self):
		url = 'https://api.github.com/repos/lsq5i5j/' + self.git_name_software
		print(url)
		try:
			r = requests.get(url).json()
		except:
			return '无法和服务器建立连接, 请稍后再试'
		self.software_time_new = r['updated_at']
		time_old = time.strptime(self.software_time_old, "%Y-%m-%dT%H:%M:%SZ")
		time_new = time.strptime(self.software_time_new, "%Y-%m-%dT%H:%M:%SZ")
		if time_new > time_old:
			return 'True'
		else:
			return 'False'

	def download_software_update(self):
		# 首先下载文件
		self.label_software_state.setText('开始下载...')
		QApplication.processEvents()
		url = 'https://github.com/lsq5i5j/' + self.git_name_software + '/archive/master.zip'
		self.download_file('software_temp.zip', url)
		# 解压缩下载的文件
		z = zipfile.ZipFile('software_temp.zip', 'r')
		z.extractall()
		z.close()
		# 写入新的软件的版本号
		print(self.data)
		self.data.update({"software_time": self.software_time_new})
		print(self.data)
		with open('data/version.json', 'w', encoding='utf-8') as file:
			json.dump(self.data, file)
		# 删除临时文件
		os.remove('software_temp.zip')

		self.label_software_state.setText('下载完成! 即将重新启动')
		QApplication.processEvents()
		time.sleep(1)
		self.write_restart_cmd()
		QApplication.processEvents()

	def download_file(self, name, url):
		headers = {'Proxy-Connection': 'keep-alive'}
		try:
			r = requests.get(url, stream=True, headers=headers)
		except:
			print('无法和服务器建立连接, 请稍后再试')
			return

		length = 15 * 1024 * 1024
		f = open(name, 'wb')
		count = 0
		count_tmp = 0
		time1 = time.time()
		t = 0.2
		for chunk in r.iter_content(chunk_size=512):
			if chunk:
				f.write(chunk)
				count += len(chunk)
				if time.time() - time1 > t:
					p = count / length * 100
					speed = (count - count_tmp) / 1024 / 1024 / t
					count_tmp = count
					text = '已下载: ' + '{:.2f}'.format(count / 1024 / 1024) + 'M, '
					text += '速度: ' + '{:.2f}'.format(speed) + 'M/S'
					print(name + ': ' + '{:.2f}'.format(p) + '%' + ' Speed: ' + '{:.2f}'.format(speed) + 'M/S')
					if 'data' in name:
						self.label_data_state.setText(text)
						QApplication.processEvents()
					elif 'software' in name:
						self.label_software_state.setText(text)
						QApplication.processEvents()
					time1 = time.time()
		f.close()
		if 'data' in name:
			self.label_data_state.setText('下载完成, 正在安装...')
			QApplication.processEvents()
		elif 'software' in name:
			self.label_software_state.setText('下载完成, 正在安装...')
			QApplication.processEvents()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	# 实例化子窗口
	selectmaster = Ui_Update()


	selectmaster.show()
	sys.exit(app.exec_())
