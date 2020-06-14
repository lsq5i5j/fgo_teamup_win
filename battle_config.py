import pandas as pd
import numpy as np
import time
import os


# 定义基础数据
class Role:
    def __init__(self):
        # 导入从者职介克制表格
        df = pd.read_csv('data/servant/servant_data_class.csv')
        df = df.fillna(1)
        df_temp1 = df.iloc[:, 4:]
        df.index = df_temp1.columns
        df_temp1.index = df_temp1.columns
        self.servant_damage_rate_class = df_temp1

        # 获取敌方各个职介基础np补正
        self.enemy_np_rate_class_1 = df['NP敌补正1']
        self.enemy_np_rate_class_2 = df['NP敌补正2']

        # 从者基础atk倍率
        df_temp2 = df['职介倍率']
        df_temp2.index = df_temp1.columns
        self.servant_damage_rate_basic = df_temp2

        # 计算天地人克制关系
        data = np.array(
            [[1, 1.1, 0.9, 1, 1], [0.9, 1, 1.1, 1, 1], [1.1, 0.9, 1, 1, 1], [1, 1, 1, 1, 1.1], [1, 1, 1, 1.1, 1]])
        c = ['天', '地', '人', '星', '兽']
        self.servant_damage_rate_class_hide = pd.DataFrame(data=data, columns=c, index=c)

        # NP补正
        self.np_correction_dict = {'Rider': 1.1, 'Caster': 1.2, 'Assassin': 0.9, 'Berserker': 0.8, 'MoonCancer': 1.2}

        # 基本数据:
        self.order = 0  # 从者编队位置
        self.name = ''  # 从者名称
        self.health = 0
        self.health_start = 0
        self.pic_path = ''
        self.damage = 0
        self.damage_total = 0
        self.np_gain_perhit = 0
        self.damage_list = []
        self.enemy_np_type = 1

        # 状态列表
        self.state = pd.DataFrame(columns=['效果', '幅度', '剩余次数', '开始回合', '结束回合', '触发回合'])
        self.attribute = []
        self.inherent_skill = pd.DataFrame()


# 定义敌人
class Enemy(Role):
    def __init__(self, name='', enemy_attribute='', enemy_class='Shielder', enemy_class_hide='星', enemy_np_type=1, health=0, pic_path=''):
        # 基本数据
        super().__init__()
        self.enemy_basic = pd.read_csv('data/enemy/enemy_data_basic.csv')
        self.health = int(health)
        self.health_start = int(health)
        self.enemy_np_type = enemy_np_type
        self.name = name
        self.pic_path = pic_path

        if self.health > 0:
            self.np_charge = float(0)
            self.class_target_role = enemy_class
            list_temp = enemy_attribute.split(',')
            if enemy_class not in list_temp:
                list_temp.append(enemy_class)
            if enemy_class_hide not in list_temp:
                list_temp.append(enemy_class_hide)
            df_temp = pd.DataFrame(list_temp)
            df_temp = df_temp
            df_temp.columns = ['特性']
            if '' in list_temp:
                list_temp.remove('')
            self.attribute = list_temp
            self.class_hide = enemy_class_hide

            # NP补正
            dict1 = self.np_correction_dict
            if self.class_target_role in dict1:
                self.np_correction = dict1[self.class_target_role]
            else:
                self.np_correction = 1

            if self.enemy_np_type != 1:
                self.np_correction *= 1.2


# 定义从者
class Servant(Role):

    def __init__(self, order, servant_id=0, level=1, skill_level=(10, 10, 10), np_level=1, atk_fufu=1000, enemy_np_type=1):
        # 练度数据
        super().__init__()
        self.servant_id = servant_id
        self.order = order
        dict1 = {1: 100, 2: 200, 3: 200, 4: 200, 5: 300}
        self.np_charge_max = dict1[np_level]
        self.skill_pic = ['', '', '']
        self.skill_used = [-1, -1, -1]
        self.skill_type = ['', '', '']
        self.np_charge = float(0)  # 初始np
        self.health = 0
        self.enemy_np_type = enemy_np_type

        if self.servant_id <= 0:
            return

        # 设定从者数据
        self.health = 1
        self.health_start = 1
        self.skill_level = skill_level  # 技能等级
        self.skill_used = [0, 0, 0]
        self.np_level = np_level  # 宝具数
        self.level = level  # 等级
        self.oc_level = 1  # 过冲能等级
        self.pic_path = "./pic/servant_logo/Servant" + str(self.servant_id).zfill(3) + ".jpg"

        # 确定从者文件夹路径
        path = ''
        all_file = os.listdir('data/servant')
        for folder in all_file:
            if folder.startswith(str(self.servant_id).zfill(3)):
                path = 'data/servant/' + folder
        if path == '':
            return

        # atk
        df = pd.read_csv(path + '/data_atk.csv')
        df = df['lv.' + str(level)]
        self.atk = df.values[0]  # 卡面atk
        self.atk_fufu = atk_fufu
        self.atk_costume = 0

        # 从者基本数据
        df = pd.read_csv(path + '/data_basic.csv')
        self.name = df['中文名'].values[0]
        self.rarity = df['稀有度'].values[0]
        self.class_hide = df['隐藏属性'].values[0]
        self.class_target_role = df['职阶'].values[0]
        self.np_rate = df['宝具np率'].values[0]
        self.np_hit = df['宝具卡hit数'].values[0]
        self.np_damage_distribute = df['宝具卡伤害分布'].values[0]

        # 从者特性
        column = ['属性1', '属性2', '性别', '隐藏属性', '职阶', '分类']
        df_temp = df[column]
        df_temp = df_temp.dropna(axis=1)
        list_temp = df_temp.values.tolist()[0]
        servant_attribute = df[['特性']].values[0][0]
        list_attribute = servant_attribute.split(',')
        list_temp += list_attribute
        df_temp = pd.DataFrame({'特性': list_temp})
        list_temp = [df['属性1'].values[0] + '·' + df['属性2'].values[0]] + list_temp
        self.attribute = list_temp

        # 从者固有技能
        df = pd.read_csv(path + '/data_inherent_skill.csv')
        df['次数'] = df['次数'].fillna(-1)
        df['持续回合'] = df['持续回合'].fillna(-1)
        df['延迟'] = df['延迟'].fillna(0)
        df['概率'] = df['概率'].fillna('500%')
        self.inherent_skill = df.dropna(subset=["效果"])

        # 从者技能
        df = pd.read_csv(path + '/data_skill.csv')
        df['次数'] = df['次数'].fillna(-1)
        df['持续回合'] = df['持续回合'].fillna(1)
        df['延迟'] = df['延迟'].fillna(0)
        df['概率'] = df['概率'].fillna('100%')

        # 技能效果
        for i in range(1, 4):
            df_temp = df[df['技能序号'] == '技能' + str(i)]
            df_temp = self.select_skill_progress(df_temp.copy())

            skill_level = '等级' + str(self.skill_level[i-1])
            df_temp.loc[df_temp['提升类型'] == '幅度', '幅度'] = df_temp[skill_level]
            df_temp.loc[df_temp['提升类型'] == '概率', '概率'] = df_temp[skill_level]

            # 技能图标
            pic_path = './pic/icon/'
            skill_pic = pic_path + df_temp['技能图标'].values[0] + '.png'
            self.skill_pic[i - 1] = skill_pic
            df_temp = df_temp.dropna(subset=['效果'])

            # 判断是否需要选择作用对象
            self.skill_type[i-1] = df_temp['作用对象'].values.tolist()

            if i == 1:
                self.skill_1 = df_temp
            elif i == 2:
                self.skill_2 = df_temp
            elif i == 3:
                self.skill_3 = df_temp

        # 从者宝具
        df = pd.read_csv(path + '/data_np.csv')
        df = self.select_skill_progress(df.copy())
        self.np_type = df['类型'].values[0]
        self.np_color = df['卡色'].values[0]
        df = df.dropna(subset=['效果'])
        df['次数'] = df['次数'].fillna(-1)
        df['持续回合'] = df['持续回合'].fillna(1)
        df['延迟'] = df['延迟'].fillna(0)
        df['概率'] = df['概率'].fillna('100%')

        self.np = df

        # 作为敌人时, NP补正
        dict1 = self.np_correction_dict
        if self.class_target_role in dict1:
            self.np_correction = dict1[self.class_target_role]
        else:
            self.np_correction = 1

        if self.enemy_np_type != 1:
            self.np_correction *= 1.2

    @staticmethod
    def select_skill_progress(df):
        list1 = df['强化'].values.tolist()
        if '未强化' in list1:
            return df

        with open('data/level/progress.txt', 'r', encoding='utf-8-sig') as f:
            data = f.read()
        event_name = data.replace('\n', '')

        df_event = pd.read_csv('data/level/event_list.csv')
        df_event_new = pd.read_csv('data/level/event_list.csv')
        for index, row in df_event.iterrows():
            if row['事件名称'] != event_name:
                df_event_new = df_event_new.drop([index])
            else:
                df_event_new = df_event_new.drop([index])
                break

        event_list = df_event_new['事件名称'].values.tolist()
        skill_event = df['强化时间'].values.tolist()
        if len(set(event_list) & set(skill_event)) == 0:
            # 表明该技能已被强化过
            return df[df['强化'] == '强化后']
        else:
            # 表明该技能被强化过 但尚未实装
            return df[df['强化'] == '强化前']


# 定义魔术礼装
class Master(Role):
    def __init__(self, master_id=0, level=1):
        # 练度数据
        super().__init__()
        self.master_id = master_id
        self.level = level
        self.skill_used = [-1, -1, -1]
        self.skill_type = ['', '', '']
        self.skill_pic = ['', '', '']
        self.pic_path = ""
        if master_id > 0:
            self.order = 0
            self.skill_used = [0, 0, 0]
            # 图标
            self.pic_path = "./pic/Master_logo/mystic_code_" + str(master_id).zfill(2) + "_a.png"
            # 技能效果
            # 确定从者文件夹路径
            path = ''
            all_file = os.listdir('data/master')
            for file in all_file:
                if file.startswith(str(self.master_id).zfill(2)) and file.endswith('.csv'):
                    path = 'data/master/' + file
            if path == '':
                return

            df = pd.read_csv(path)
            df['次数'] = df['次数'].fillna(-1)
            df['持续回合'] = df['持续回合'].fillna(1)
            df['延迟'] = df['延迟'].fillna(0)
            df['概率'] = df['概率'].fillna('500%')

            skill_level = '等级' + str(self.level)
            df.loc[df['提升类型'] == '幅度', '幅度'] = df[skill_level]
            df.loc[df['提升类型'] == '概率', '概率'] = df[skill_level]

            # 技能效果
            for i in range(1, 4):
                df_temp = df.loc[df['技能序号'] == '技能' + str(i)]
                # 技能图标
                pic_path = './pic/icon/'
                skill_pic = pic_path + df_temp['技能图标'].values[0] + '.png'
                self.skill_pic[i - 1] = skill_pic
                df_temp = df_temp.dropna(subset=['效果'])
                # 判断是否需要选择作用对象
                self.skill_type[i - 1] = df_temp['作用对象'].values.tolist()
                if i == 1:
                    self.skill_1 = df_temp
                elif i == 2:
                    self.skill_2 = df_temp
                elif i == 3:
                    self.skill_3 = df_temp


# 定义战斗配置
class BattleConfig:
    def __init__(self):
        self.battle_strategy = '第1回合：'
        self.enemy_11 = Enemy()
        self.enemy_12 = Enemy()
        self.enemy_13 = Enemy()
        self.enemy_21 = Enemy()
        self.enemy_22 = Enemy()
        self.enemy_23 = Enemy()
        self.enemy_31 = Enemy()
        self.enemy_32 = Enemy()
        self.enemy_33 = Enemy()
        self.servant_1 = Servant(order=1)
        self.servant_2 = Servant(order=2)
        self.servant_3 = Servant(order=3)
        self.servant_4 = Servant(order=4)
        self.servant_5 = Servant(order=5)
        self.servant_6 = Servant(order=6)
        self.master = Master()

        self.enemy_1 = self.enemy_11
        self.enemy_2 = self.enemy_12
        self.enemy_3 = self.enemy_13
        self.oc_level = 1
        self.battle_round = 1
        self.battle_ground = ''
        self.round_start(1)

    def round_start(self, battle_round):
        self.battle_round = battle_round
        if self.battle_round == 1:
            self.enemy_1 = self.enemy_11
            self.enemy_2 = self.enemy_12
            self.enemy_3 = self.enemy_13
        elif self.battle_round == 2:
            self.enemy_1 = self.enemy_21
            self.enemy_2 = self.enemy_22
            self.enemy_3 = self.enemy_23
        elif self.battle_round == 3:
            self.enemy_1 = self.enemy_31
            self.enemy_2 = self.enemy_32
            self.enemy_3 = self.enemy_33
        else:
            return
        # 设置新敌人的职阶技能
        self.use_enemy_inherent_skill()
        # 设置己方的职阶技能
        if self.battle_round == 1:
            self.use_inherent_skill()
        # 设置OC level
        self.oc_level = 1

    def use_inherent_skill(self):
        # 从者职阶技能
        for order in range(1, 7):
            if order == 1:
                role = self.servant_1
            elif order == 2:
                role = self.servant_2
            elif order == 3:
                role = self.servant_3
            elif order == 4:
                role = self.servant_4
            elif order == 5:
                role = self.servant_5
            elif order == 6:
                role = self.servant_6
            else:
                return
            if role.health <= 0:
                continue
            df_skill = role.inherent_skill
            for index, row in df_skill.iterrows():
                self.skill_target_range(user=role, buff=row, order=order)

    def use_enemy_inherent_skill(self):
        # 敌人释放职阶技能
        for order in range(1, 4):
            if order == 1:
                role = self.enemy_1
            elif order == 2:
                role = self.enemy_2
            elif order == 3:
                role = self.enemy_3
            else:
                return
            if role.health <= 0:
                continue
            df_skill = role.inherent_skill
            for index, row in df_skill.iterrows():
                self.skill_target_range(user=role, buff=row, order=order, team='enemy')

    # 从者使用技能
    def use_skill(self, order, skill, target=0, required_prob=0):
        if order == 1:
            role = self.servant_1
        elif order == 2:
            role = self.servant_2
        elif order == 3:
            role = self.servant_3
        else:
            return

        if skill == 1:
            df_skill = role.skill_1
        elif skill == 2:
            df_skill = role.skill_2
        elif skill == 3:
            df_skill = role.skill_3
        else:
            return

        role.skill_used[skill-1] = 1

        for row_index in range(len(df_skill)):
            row = df_skill.iloc[row_index, :]
            self.skill_target_range(user=role, buff=row, order=order, target=target, prob=required_prob)

        # 记录技能使用记录
        text = str(order)+'号位'+str(role.name)
        if target == order:
            text += '对自身'
        elif target == 1:
            text += '对1号位'+str(self.servant_1.name)
        elif target == 2:
            text += '对2号位'+str(self.servant_2.name)
        elif target == 3:
            text += '对3号位'+str(self.servant_3.name)
        text += '使用' + str(skill) + '技能：'
        if len(df_skill) == 0:
            text += '无效果'
        for i in df_skill[['技能效果', '幅度']].values:
            name = i[0]
            num = str(i[1])
            if '(' in name:
                a = name.rfind('(')
                name = name[0:a] + num + name[a:len(name)]
            else:
                name = name + num
            text += name + '，'
        text = text.strip('，')
        text += '。'
        self.battle_strategy += '\n' + text

    # 使用御主技能
    def use_master_skill(self, skill, target=0, required_prob=0):
        master = self.master
        if skill == 1:
            df_skill = master.skill_1
        elif skill == 2:
            df_skill = master.skill_2
        elif skill == 3:
            df_skill = master.skill_3
        else:
            return
        master.skill_used[skill - 1] = 1
        for row_index in range(len(df_skill)):
            row = df_skill.iloc[row_index, :]
            self.skill_target_range(user=master, buff=row, order=0, target=target, prob=required_prob)
        # 记录技能使用记录
        text = '御主'
        if target == 1:
            text += '对1号位' + str(self.servant_1.name)
        elif target == 2:
            text += '对2号位' + str(self.servant_2.name)
        elif target == 3:
            text += '对3号位' + str(self.servant_3.name)
        text += '使用' + str(skill) + '技能：'
        if len(df_skill) == 0:
            text += '无效果'
        for i in df_skill[['技能效果', '幅度']].values:
            name = i[0]
            num = str(i[1])
            if '(' in name:
                a = name.rfind('(')
                name = name[0:a] + num + name[a:len(name)]
            else:
                name = name + num
            text += name + '，'
        text = text.strip('，')
        text += '。'
        self.battle_strategy += '\n' + text

    # 判断技能作用对象以及作用对象是否符合要求
    def skill_target_range(self, user, buff, order=0, team='team', target=0, random_num=0.9, prob=0):

        # 筛选作用对象
        if buff['作用对象'] == '自身':
            target_list = [order]
        elif buff['作用对象'] == '己方单体':
            target_list = [target]
        elif buff['作用对象'] == '己方全体' and user.order <= 3:
            target_list = [1, 2, 3]
        elif buff['作用对象'] == '除自身以外己方全体' and user.order <= 3:
            target_list = [1, 2, 3]
            target_list.remove(order)
        elif buff['作用对象'] == '敌方全体':
            target_list = [1, 2, 3]
        elif buff['作用对象'] == '敌方单体':
            target_list = [target]
        else:
            return
        # 筛选作用对象阵营
        if '己方' in buff['作用对象']:
            if team == 'team':
                target_type = 'servant'
            else:
                target_type = 'enemy'
        elif '敌方' in buff['作用对象']:
            if team == 'team':
                target_type = 'enemy'
            else:
                target_type = 'servant'
        else:
            if team == 'team':
                target_type = 'servant'
            else:
                target_type = 'enemy'

        for target in target_list:
            if target_type == 'servant':
                if target == 1:
                    target_role = self.servant_1
                elif target == 2:
                    target_role = self.servant_2
                elif target == 3:
                    target_role = self.servant_3
                elif target == 4:
                    target_role = self.servant_4
                elif target == 5:
                    target_role = self.servant_5
                elif target == 6:
                    target_role = self.servant_6
                else:
                    continue
            elif target_type == 'enemy':
                if target == 1:
                    target_role = self.enemy_1
                elif target == 2:
                    target_role = self.enemy_2
                elif target == 3:
                    target_role = self.enemy_3
                else:
                    continue
            else:
                continue
            # 如果目标死亡, 则不能添加buff
            if target_role.health <= 0:
                continue

            buff = buff.fillna('')
            if buff['作用场景'] != '':
                temp = buff['作用场景']
                required_battleground = temp.split(',')
                battleground_list = self.battle_ground.split(',')

                list1 = list(set(required_battleground).intersection(set(battleground_list)))
                if len(list1) == 0:
                    print('场地不符合要求')
                    continue
            if buff['对象特性'] != '':
                temp = buff['对象特性']
                require_attribute_list = temp.split(',')
                servant_attribute_list = target_role.attribute
                list1 = list(set(require_attribute_list).intersection(set(servant_attribute_list)))
                state = False
                for attribute in require_attribute_list:
                    if self.state_presence(target_role, attribute) is True:
                        state = True
                if len(list1) >0 :
                    state = True

                if state is False:
                    print('对象不符合要求')
                    continue
            # print('技能可以添加')

            if buff['效果'].startswith('状态'):
                self.add_state(user, buff, target_role, prob_require=prob)
            elif buff['效果'].startswith('效果'):
                self.change_attribute(user, buff, order, target_role, random_num=random_num, prob_require=prob)
            else:
                continue

    @staticmethod
    def remove_brackets(text):
        start = text.find('[')
        end = text.rfind(']')
        if start != -1 and end != -1:
            return text[start + 1: end]
        else:
            return text

    # 状态效果附加到指定的从者/敌人上
    def add_state(self, user, buff, target_role, prob_require=0):
        '''
        此时buff类型为'状态'
        每个buff都包含如下几个参数
        ['效果', '幅度', '作用对象', '对象特性', '作用场景', '次数', '持续回合', '延迟']
        需要根据场地以及特性分析将buff转化为如下格式
        ['效果', '幅度', '剩余次数', '开始回合', '结束回合']
        '''
        buff_type = self.remove_brackets(buff['效果'])
        if '付与特性' in buff_type:
            buff_type = self.remove_brackets(buff_type)
        num = buff['幅度']
        prob = float(buff['概率'].strip('%'))
        left = buff['次数']
        start = self.battle_round + buff['延迟']
        end = start + buff['持续回合'] - 1
        if buff['持续回合'] == -1:
            end = 100
        if left == -1:
            left = 100

        a = {'效果': buff_type, '幅度': num, '剩余次数': left, '开始回合': start, '结束回合': end}

        # 计算强化状态施加概率
        num = self.state_amount(role=user, target_attribute='强化成功率提升')
        num_attack = self.state_amount(role=user, target_attribute='攻击强化成功率提升')
        num_defence = self.state_amount(role=user, target_attribute='防御强化成功率提升')
        num_down = self.state_amount(role=user, target_attribute='强化成功率下降')
        num_down_attack = self.state_amount(role=user, target_attribute='攻击强化成功率下降')
        num_down_defence = self.state_amount(role=user, target_attribute='防御强化成功率下降')
        prob_buff = prob + num - num_down
        prob_buff_attack = prob_buff + num_attack - num_down_attack
        prob_buff_defence = prob_buff + num_defence - num_down_defence

        # 计算弱化状态施加概率
        num = self.state_amount(role=user, target_attribute='弱化状态成功率提升')
        num_attack = self.state_amount(role=user, target_attribute='攻击弱化状态成功率提升')
        num_defence = self.state_amount(role=user, target_attribute='防御弱化状态成功率提升')
        num_down = self.state_amount(role=user, target_attribute='弱化状态成功率下降')
        num_down_attack = self.state_amount(role=user, target_attribute='攻击弱化状态成功率下降')
        num_down_defence = self.state_amount(role=user, target_attribute='防御弱化状态成功率下降')

        de_num = self.state_amount(role=target_role, target_attribute='弱化状态耐性提升')
        de_num_attack = self.state_amount(role=target_role, target_attribute='攻击弱化状态耐性提升')
        de_num_defence = self.state_amount(role=target_role, target_attribute='防御弱化状态耐性提升')
        de_num_down = self.state_amount(role=target_role, target_attribute='弱化状态耐性下降')
        de_num_down_attack = self.state_amount(role=target_role, target_attribute='攻击弱化状态耐性下降')
        de_num_down_defence = self.state_amount(role=target_role, target_attribute='防御弱化状态耐性下降')

        prob_debuff = prob + num - num_down - de_num + de_num_down
        prob_debuff_attack = prob_debuff + num_attack - num_down_attack - de_num_attack + de_num_down_attack
        prob_debuff_defence = prob_debuff + num_defence - num_down_defence - de_num_defence + de_num_down_defence

        if '提升' in buff_type or '伤害附加' in buff_type or '伤害减免' in buff_type:
            if '攻击力' in buff_type or '指令卡性能' in buff_type or '宝具威力' in buff_type or '伤害附加' in buff_type:
                prob = prob_buff_attack
            elif '防御力' in buff_type or '攻击耐性' in buff_type or '伤害减免' in buff_type:
                prob = prob_buff_defence
            else:
                prob = prob_buff
            if prob >= prob_require:
                target_role.state = target_role.state.append(a, ignore_index=True)
        elif '下降' in buff_type:
            if self.state_presence(target_role, '弱化无效') is True:
                for index, row in target_role.state.iterrows():
                    if row['效果'] == '弱化无效':
                        target_role.state.loc[[index], ['剩余次数']] = row['剩余次数'] - 1
                        break
                return
            if '攻击力' in buff_type or '指令卡性能' in buff_type or '宝具威力' in buff_type:
                prob = prob_debuff_attack
            elif '防御力' in buff_type or '攻击耐性' in buff_type:
                prob = prob_debuff_defence
            else:
                prob = prob_debuff
            if prob >= prob_require:
                target_role.state = target_role.state.append(a, ignore_index=True)
        else:
            if prob >= prob_require:
                target_role.state = target_role.state.append(a, ignore_index=True)

    # 这些是'效果'类别的技能, 特点是马上生效, 如加NP, 解弱体等
    def change_attribute(self, user, buff, order, target_role, random_num=0.9, prob_require=0):
        buff_type = buff['效果']
        buff_type = buff_type[3:-1]

        prob = float(buff['概率'].strip('%'))
        num = self.state_amount(role=target_role, target_attribute='强化解除耐性提升')
        num_attack = self.state_amount(role=target_role, target_attribute='攻击强化解除耐性提升')
        num_defence = self.state_amount(role=target_role, target_attribute='防御强化解除耐性提升')
        num_down = self.state_amount(role=target_role, target_attribute='强化解除耐性下降')
        num_down_attack = self.state_amount(role=target_role, target_attribute='攻击强化解除耐性下降')
        num_down_defence = self.state_amount(role=target_role, target_attribute='防御强化解除耐性下降')
        prob_buff = prob - num + num_down
        prob_buff_attack = prob_buff - num_attack + num_down_attack
        prob_buff_defence = prob_buff - num_defence + num_down_defence

        num = buff['幅度']
        if '解除' in buff_type and '强化状态' in buff_type:
            if '攻击' in buff_type:
                prob = prob_buff_attack
            elif '防御' in buff_type:
                prob = prob_buff_defence
            else:
                prob = prob_buff

        if prob >= prob_require:
            if '解除' in buff_type and '强化状态' in buff_type:
                if self.state_presence(target_role, '弱化无效') is True:
                    for index, row in target_role.state.iterrows():
                        if row['效果'] == '弱化无效':
                            target_role.state.loc[[index], ['剩余次数']] = row['剩余次数'] - 1
                            break
                    return
                df = target_role.state
                if buff_type == '解除强化状态':
                    df.loc[~ df['效果'].str.contains('不可解除')
                           & df['效果'].str.contains('提升|上升|附加|减免'), '结束回合'] = self.battle_round - 1
                elif buff_type == '解除攻击强化状态':
                    df.loc[~ df['效果'].str.contains('不可解除')
                           & df['效果'].str.contains('提升|上升')
                           & df['效果'].str.contains('攻击力|指令卡性能|宝具威力|附加|减免'), '结束回合'] = self.battle_round - 1
                elif buff_type == '解除防御强化状态':
                    df.loc[~ df['效果'].str.contains('不可解除')
                           & df['效果'].str.contains('提升|上升')
                           & df['效果'].str.contains('防御力|耐性'), '结束回合'] = self.battle_round - 1
            elif buff_type == 'NP增加':
                num = float(num.strip('%'))
                target_role.np_charge += num
                target_role.np_charge = min(target_role.np_charge, target_role.np_charge_max)
            elif buff_type == 'NP减少':
                num = float(num.strip('%'))
                target_role.np_charge -= num
                target_role.np_charge = max(target_role.np_charge, 0)
            elif buff_type.startswith('付与特性'):
                temp = self.remove_brackets(buff_type)
                target_role.attribute.append(temp)
            elif buff_type.startswith('改变场地'):
                temp = self.remove_brackets(buff_type)
                if temp not in self.battle_ground:
                    self.battle_ground += ',' + temp
                    self.battle_ground = self.battle_ground.strip(',')
            elif buff_type == '解除弱化状态':
                df = target_role.state
                df.loc[~ df['效果'].str.contains('不可解除') & df['效果'].str.contains('下降'), '结束回合'] = self.battle_round - 1
            elif buff_type == '强大攻击':
                num = float(num.strip('%'))
                target_role.damage_list = self.damage_enemy(servant_order=order, enemy=target_role, random_num=random_num, rate_magnify=num)
                self.np_recharge(servant_order=order, enemy=target_role)
            elif buff_type == '无视防御强大攻击':
                num = float(num.strip('%'))
                target_role.damage_list = self.damage_enemy(servant_order=order, enemy=target_role, random_num=random_num, rate_magnify=num, ignore_defence=True)
                self.np_recharge(servant_order=order, enemy=target_role)
            elif '特攻' in buff_type and '威力随特性数量增加' in buff_type:
                print('!!!!!!!!!')
                temp = self.remove_brackets(buff_type)
                require_attribute_list = temp.split(',')
                enemy_attribute_list = target_role.attribute
                # print(enemy_attribute_list)
                # print(require_attribute_list)
                list1 = list(set(require_attribute_list).intersection(set(enemy_attribute_list)))
                state_num = len(list1)
                for attribute in require_attribute_list:
                    if self.state_presence(target_role, attribute) is True:
                        state_num += 1
                state_num = min(state_num, 10)
                if state_num > 0:
                    print('触发特攻状态', state_num)
                    num = 100 + float(num.strip('%')) * state_num
                    required_attribute = self.remove_brackets(buff_type)
                    self.damage_special(enemy=target_role, rate_special=num, attribute=required_attribute)
            elif buff_type.startswith('特攻'):
                required_attribute = self.remove_brackets(buff_type)
                num = float(num.strip('%'))
                self.damage_special(enemy=target_role, rate_special=num, attribute=required_attribute)
            elif buff_type == '威力提升':
                num = float(num.strip('%'))
                damage_list_add = self.damage_enemy(servant_order=order, enemy=target_role, rate_magnify=num, random_num=random_num)
                if sum(target_role.damage_list) >= target_role.health:
                    print('上一发宝具击杀')
                else:
                    target_role.damage_list += damage_list_add
                    print('上一发宝具没有击杀')
                self.np_recharge(servant_order=order, enemy=target_role)
            elif '职阶相性改变' in buff_type:
                self_class = target_role.class_target_role
                target_class = self.remove_brackets(buff_type)
                num = float(num)
                target_role.servant_damage_rate_class.loc[[self_class], [target_class]] = num
            elif buff_type == '即死':
                self.servant_die(order)
            elif buff_type == '吸收NP':
                if order == 1:
                    servant = self.servant_1
                    servant_a = self.servant_2
                    servant_b = self.servant_3
                elif order == 2:
                    servant = self.servant_2
                    servant_a = self.servant_3
                    servant_b = self.servant_1
                elif order == 3:
                    servant = self.servant_3
                    servant_a = self.servant_1
                    servant_b = self.servant_2
                else:
                    return
                num = float(num.strip('%'))
                if servant_a.health > 0:
                    np_a = min(servant_a.np_charge, num)
                    servant_a.np_charge -= np_a
                else:
                    np_a = 0
                if servant_b.health > 0:
                    np_b = min(servant_b.np_charge, num)
                    servant_b.np_charge -= np_b
                else:
                    np_b = 0
                servant.np_charge += np_a + np_b
                servant.np_charge = min(servant.np_charge, servant.np_charge_max)

            elif buff_type == '活祭除自身以外的己方单体':
                list1 = [1, 2, 3]
                list1.remove(order)
                if list1[0] == 1:
                    servant = self.servant_1
                elif list1[0] == 2:
                    servant = self.servant_2
                elif list1[0] == 3:
                    servant = self.servant_3
                else:
                    return
                if servant.health > 0:
                    print('即死', list1[0])
                    self.servant_die(list1[0])
                else:
                    if list1[1] == 1:
                        servant = self.servant_1
                    elif list1[1] == 2:
                        servant = self.servant_2
                    elif list1[1] == 3:
                        servant = self.servant_3
                    else:
                        return
                    if servant.health > 0:
                        print('即死', list1[1])
                        self.servant_die(list1[1])
                    else:
                        return
            else:
                return

    # 使用宝具
    def use_np(self, order, target=0, random_num=0.9, required_prob=0):

        if order == 1:
            servant = self.servant_1
        elif order == 2:
            servant = self.servant_2
        elif order == 3:
            servant = self.servant_3
        else:
            return

        if servant.health <= 0:
            return
        # 清空宝具充能
        servant.np_charge = 0

        # 检查从者状态有无 OC 提升
        df = servant.state
        for index, row in df.iterrows():
            if '充能阶段上升' in row['效果'] :
                if row['剩余次数'] > 0 and row['开始回合'] <= self.battle_round <= row['结束回合']:
                    servant.oc_level += int(row['幅度'])
                    df.loc[[index], ['剩余次数']] = row['剩余次数'] - 1

        # print('充能阶段: ', servant.oc_level)
        # 设置OC最大值
        servant.oc_level = min(servant.oc_level, 5)

        # 根据OC信息设置宝具数据
        df_np = servant.np.copy()
        for index, row in df_np.iterrows():
            if '提升类型' == '概率':
                enhance_type = '概率'
            else:
                enhance_type = '幅度'
            if 'Over Charge' in str(row['增益方式']):
                df_np.loc[[index], [enhance_type]] = row['等级'+str(servant.oc_level)]
            elif '宝具升级' in str(row['增益方式']):
                df_np.loc[[index], [enhance_type]] = row['等级' + str(servant.np_level)]
            else:
                df_np.loc[[index], [enhance_type]] = row['等级1']
        # 记录宝具信息:
        text_temp = []
        # 根据设定的等级, 计算宝具效果/状态
        for index, row in df_np.iterrows():
            self.skill_target_range(user=servant, buff=row, order=order, target=target, random_num=random_num, prob=required_prob)
            num = row['幅度']
            text_temp.append(str(num))
        # 宝具伤害计算完成, 根据伤害数据计算敌方血量, 并计算NP补正
        for i in range(1, 4):
            if i == 1:
                enemy = self.enemy_1
            elif i == 2:
                enemy = self.enemy_2
            elif i == 3:
                enemy = self.enemy_3
            else:
                return
            if enemy.health <= 0:
                continue
            enemy.damage = 0
            health_start = round(enemy.health)
            for damage in enemy.damage_list:
                enemy.health -= damage
                enemy.damage += damage
                if enemy.damage >= health_start:
                    np_overkill = 1.5
                else:
                    np_overkill = 1
                servant.np_charge += np_overkill*enemy.np_gain_perhit
                servant.np_charge = min(servant.np_charge, servant.np_charge_max)
            # 结算数据数据
            enemy.damage_total += enemy.damage
            enemy.np_gain_perhit = 0
            enemy.damage_list = []

        # 记录宝具使用
        text = str(order) + '号位' + str(servant.name)
        if target == 1:
            text += '对1号位敌人'
        elif target == 2:
            text += '对2号位敌人'
        elif target == 3:
            text += '对3号位敌人'

        text += '使用宝具：'
        if len(df_np) == 0:
            text += '无效果'
        list1 = df_np['宝具效果'].values
        for i in range(len(list1)):
            name = str(list1[i])
            num = text_temp[i]
            if '(' in name:
                a = name.rfind('(')
                name = name[0:a] + num + name[a:len(name)]
            else:
                name = name + num
            text += name + '，'
        text = text.strip('，')
        text += '。'
        self.battle_strategy += '\n' + text
        # 记录宝具造成的伤害
        text = ''
        for i in range(1, 4):
            if i == 1:
                enemy = self.enemy_1
            elif i == 2:
                enemy = self.enemy_2
            elif i == 3:
                enemy = self.enemy_3
            else:
                return
            if enemy.damage == 0:
                continue
            text += '\n'+ str(i) + '号位敌人' + enemy.name + '受到伤害：' + str(int(enemy.damage)) + '，'
            text += '平均伤害：' + str(int(enemy.damage/random_num)) + '，'
            text += '伤害范围：' + str(int(enemy.damage/random_num*0.9)) + '-' + str(int(enemy.damage/random_num*1.1)) + '，'
        text = text.strip('，')
        text += '。'
        self.battle_strategy += text

    def skill_left_times(self, df, index, row):
        if row['触发回合'] != self.battle_round:
            df.loc[[index], ['触发回合']] = self.battle_round
            df.loc[[index], ['剩余次数']] = row['剩余次数'] - 1

    # 查看各个从者的各种情况
    def state_amount(self, role, target_attribute):
        df = role.state.copy()
        num = 0
        for index, row in df.iterrows():
            if row['开始回合'] <= self.battle_round <= row['结束回合']:
                buff_type = row['效果']
                buff_type = buff_type.replace('(不可解除)', '')
                if buff_type == target_attribute:
                    temp = row['幅度'].strip('%')
                    num += float(temp)
        return num

    # 查看各个从者buff列表是否含有某种属性
    def state_presence(self, role, target_attribute):
        df = role.state.copy()
        state = False
        for index, row in df.iterrows():
            if row['开始回合'] <= self.battle_round <= row['结束回合']:
                buff_type = row['效果']
                buff_type = buff_type.replace('(不可解除)', '')
                if buff_type == target_attribute:
                    state = True
        return state

    # 伤害计算
    def damage_enemy(self, servant_order, enemy, rate_magnify, random_num=0.9, ignore_defence=False):
        if enemy.health <= 0:
            return

        if servant_order == 1:
            servant = self.servant_1
        elif servant_order == 2:
            servant = self.servant_2
        elif servant_order == 3:
            servant = self.servant_3
        else:
            return

        if servant.health <= 0:
            return
        # 基础atk
        df = servant.servant_damage_rate_basic
        atk = (servant.atk + servant.atk_costume + servant.atk_fufu) * df[servant.class_target_role]
        # 色卡倍率
        dict_color = {'Buster': 1.5, 'Arts': 1, 'Quick': 0.8}
        rate_card = dict_color[servant.np_color]
        # 计算职介克制倍率
        df = servant.servant_damage_rate_class
        rate_class = df.at[(servant.class_target_role, enemy.class_target_role)]
        # 计算天地人克制
        df = servant.servant_damage_rate_class_hide
        rate_class_hide = df.at[(servant.class_hide, enemy.class_hide)]
        # 计算自身buff
        rate_attack = 0
        rate_defence = 0
        rate_attack_special = 100  # 包含特攻和宝具威力
        rate_attack_color = 100
        rate_attack_extra = 0

        df = servant.state
        for index, row in df.iterrows():
            if self.battle_round+1 < row['开始回合'] or self.battle_round > row['结束回合']:
                continue
            buff_type = row['效果']
            buff_num = row['幅度']
            if '攻击力提升' in buff_type:
                rate_attack += float(buff_num.strip('%'))
                self.skill_left_times(df, index, row)
            elif '攻击力下降' in buff_type:
                rate_attack -= float(buff_num.strip('%'))
                self.skill_left_times(df, index, row)
            elif '宝具威力提升' in buff_type:
                rate_attack_special += float(buff_num.strip('%'))
                self.skill_left_times(df, index, row)
            elif '活动攻击力提升' in buff_type:
                rate_attack_special += float(buff_num.strip('%'))
                self.skill_left_times(df, index, row)
            elif '宝具威力下降' in buff_type:
                rate_attack_special -= float(buff_num.strip('%'))
                self.skill_left_times(df, index, row)
            elif servant.np_color + '指令卡性能提升' in buff_type:
                rate_attack_color += float(buff_num.strip('%'))
                self.skill_left_times(df, index, row)
            elif servant.np_color + '指令卡性能下降' in buff_type:
                rate_attack_color -= float(buff_num.strip('%'))
                self.skill_left_times(df, index, row)
            elif '伤害附加' in buff_type:
                rate_attack_extra += float(buff_num)
                self.skill_left_times(df, index, row)
            elif '无视防御' in buff_type:
                ignore_defence = True
            elif '特攻' in buff_type:
                print(buff_type)
                temp = self.remove_brackets(buff_type)
                require_attribute_list = temp.split(',')
                enemy_attribute_list = enemy.attribute
                # print(enemy_attribute_list)
                # print(require_attribute_list)
                list1 = list(set(require_attribute_list).intersection(set(enemy_attribute_list)))
                state = False
                for attribute in require_attribute_list:
                    if self.state_presence(enemy, attribute) is True:
                        state = True
                if len(list1) > 0:
                    state = True

                if state is True > 0:
                    print('触发特攻状态')
                    rate_attack_special += float(buff_num.strip('%'))
                    self.skill_left_times(df, index, row)


        # 计算敌方debuff
        df = enemy.state
        for index, row in df.iterrows():
            buff_type = row['效果']
            buff_num = row['幅度']
            if '防御力上升' in buff_type and ignore_defence is False:
                rate_defence += float(buff_num.strip('%'))
                self.skill_left_times(df, index, row)
            elif '防御力下降' in buff_type:
                rate_defence -= float(buff_num.strip('%'))
                self.skill_left_times(df, index, row)
            elif servant.np_color + '指令卡攻击耐性上升' in buff_type:
                rate_attack_color -= float(buff_num.strip('%'))
                self.skill_left_times(df, index, row)
            elif servant.np_color + '指令卡攻击耐性下降' in buff_type:
                rate_attack_color += float(buff_num.strip('%'))
                self.skill_left_times(df, index, row)
            elif '伤害减免' in buff_type:
                rate_attack_extra -= float(buff_num)
                self.skill_left_times(df, index, row)

        rate_attack = max(-100, rate_attack)
        rate_defence = min(100, rate_defence)
        rate_attack_all = 100+rate_attack-rate_defence
        rate_attack_all = max(0, rate_attack_all)

        rate_attack_special = max(0, rate_attack_special)
        rate_attack_color = max(0, rate_attack_color)
        rate_attack_extra = max(0, rate_attack_extra)
        damage_all = atk * rate_magnify / 100 \
                         * rate_card \
                         * (rate_attack_color / 100) \
                         * (rate_attack_all / 100) \
                         * rate_class_hide \
                         * rate_class \
                         * (rate_attack_special / 100) \
                         * 0.23 \
                         * random_num
        # 将伤害分布到每hit上
        temp = str(servant.np_damage_distribute)
        temp_list = temp.split(',')
        return [int(x)*damage_all/100 for x in temp_list]

    def damage_special(self, enemy, rate_special, attribute):
        # 计算宝具特攻伤害
        temp = attribute
        require_attribute_list = temp.split(',')
        enemy_attribute_list = enemy.attribute
        list1 = list(set(require_attribute_list).intersection(set(enemy_attribute_list)))
        if len(list1) == 0 and self.state_presence(enemy, attribute) is False:
            return
        print('宝具特攻', rate_special)
        temp = enemy.damage_list
        enemy.damage_list = [rate_special/100*x for x in temp]



    def np_recharge(self, servant_order, enemy):
        if enemy.health <= 0:
            return

        if servant_order == 1:
            servant = self.servant_1
        elif servant_order == 2:
            servant = self.servant_2
        elif servant_order == 3:
            servant = self.servant_3
        else:
            return

        if servant.health <= 0:
            return
        # 色卡np倍率
        dict_color = {'Buster': 0, 'Arts': 3, 'Quick': 1}
        np_rate_card = dict_color[servant.np_color]
        # 若为红卡则放弃计算
        if np_rate_card == 0:
            enemy.np_gain_perhit = 0
            return
        # 宝具np率
        np_rate = servant.np_rate
        np_rate = float(np_rate.strip('%'))
        # 计算自身buff
        np_buff_color = 100
        np_buff = 100
        df = servant.state
        for index, row in df.iterrows():
            if self.battle_round+1 < row['开始回合'] or self.battle_round > row['结束回合']:
                continue
            buff_type = row['效果']
            buff_num = row['幅度']
            if 'NP获得量提升' in buff_type:
                np_buff += float(buff_num.strip('%'))
                self.skill_left_times(df, index, row)
            elif 'NP获得量下降' in buff_type:
                np_buff -= float(buff_num.strip('%'))
                self.skill_left_times(df, index, row)
            elif servant.np_color + '指令卡性能提升' in buff_type:
                np_buff_color += float(buff_num.strip('%'))
            elif servant.np_color + '指令卡性能下降' in buff_type:
                np_buff_color -= float(buff_num.strip('%'))

        # 计算敌方debuff
        df = enemy.state
        for index, row in df.iterrows():
            buff_type = row['效果']
            buff_num = row['幅度']
            if servant.np_color + '指令卡攻击耐性上升' in buff_type:
                np_buff_color -= float(buff_num.strip('%'))
                df.loc[[index], ['剩余次数']] = row['剩余次数'] - 1
            elif servant.np_color + '指令卡攻击耐性下降' in buff_type:
                np_buff_color += float(buff_num.strip('%'))
                df.loc[[index], ['剩余次数']] = row['剩余次数'] - 1
        np_correction_enemy = enemy.np_correction

        '''NP获得量 =NP获取率* 卡片倍率* (1+卡片性能Buff)* (1+NP获得量Buff)* Overkill补正* 敌方补正'''
        np_gain = np_rate * np_rate_card * (np_buff_color/100) * (np_buff/100)* np_correction_enemy
        enemy.np_gain_perhit = np_gain
        # print('每张卡获得np', np_gain)

    # 将后背从者补全(比如4号位空, 则5号位移到四号位, 6号位移动到5号位)
    def fill_back_servant(self):
        for _ in range(2):
            if self.servant_4.health <= 0:
                self.servant_4, self.servant_5 = self.servant_5, self.servant_6
                self.servant_6 = Servant(order=6)
            if self.servant_5.health <= 0:
                self.servant_5 = self.servant_6
                self.servant_6 = Servant(order=6)
        self.servant_4.order = 4
        self.servant_5.order = 5
        self.servant_6.order = 6

    # 计算回合结束后的效果(目前支持:每回合回复NP)
    def round_end(self):
        for i in range(1, 4):
            if i == 1:
                servant = self.servant_1
            elif i == 2:
                servant = self.servant_2
            elif i == 3:
                servant = self.servant_3
            else:
                return
            if servant.health <= 0:
                continue

            df = servant.state
            for index, row in df.iterrows():
                if row['开始回合'] <= self.battle_round <= row['结束回合']:
                    buff_type = row['效果']
                    buff_num = row['幅度']
                    if '每回合NP增加' in buff_type:
                        servant.np_charge += float(buff_num.strip('%'))
                        servant.np_charge = min(servant.np_charge, servant.np_charge_max)
                        self.skill_left_times(df, index, row)
                    elif '每回合NP减少' in buff_type:
                        servant.np_charge -= float(buff_num.strip('%'))
                        servant.np_charge = max(servant.np_charge, 0)
                        self.skill_left_times(df, index, row)

    def use_costume_skill(self, order, dict1):
        if order == 1:
            servant = self.servant_1
        elif order == 2:
            servant = self.servant_2
        elif order == 3:
            servant = self.servant_3
        elif order == 4:
            servant = self.servant_4
        elif order == 5:
            servant = self.servant_5
        elif order == 6:
            servant = self.servant_6
        else:
            return
        if servant.health <= 0:
            return

        list_skill_parameter = ['效果', '幅度', '作用对象', '对象特性', '作用场景', '次数', '持续回合', '延迟']
        df = pd.DataFrame(columns=list_skill_parameter)

        for buff_name in dict1:
            buff_num = dict1[buff_name]
            if buff_name == 'atk':
                servant.atk_costume = buff_num
            elif buff_name == '初始NP':
                servant.np_charge = buff_num
                servant.np_charge = min(servant.np_charge, servant.np_charge_max)
                print('初始NP: ', servant.np_charge)
            elif buff_name.startswith('状态') and buff_num[0] != 0:
                dict_temp = {'效果': buff_name,
                             '概率': '500%',
                             '幅度': buff_num[0],
                             '作用对象': dict1['range'],
                             '次数': buff_num[1],
                             '持续回合': buff_num[2],
                             '延迟': 0}
                df = df.append(dict_temp, ignore_index=True)

        for row_index in range(len(df)):
            row = df.iloc[row_index, :]
            self.skill_target_range(user=servant, buff=row, order=order)

    def servant_die(self, order):
        # 首先,计算死亡退场技能
        if order == 1:
            servant = self.servant_1
        elif order == 2:
            servant = self.servant_2
        elif order == 3:
            servant = self.servant_3
        else:
            return
        if servant.health <= 0:
            return

        df = servant.state
        target_list = [1, 2, 3]
        target_list.remove(order)
        for index, row in df.iterrows():

            if self.battle_round + 1 < row['开始回合'] or self.battle_round > row['结束回合']:
                continue
            buff_type = row['效果']
            buff_num = row['幅度']
            if '退场时NP增加' in buff_type:
                for i in target_list:
                    if i == 1:
                        if self.servant_1.health <= 0:
                            continue
                        self.servant_1.np_charge += float(buff_num.strip('%'))
                        self.servant_1.np_charge = min(self.servant_1.np_charge, self.servant_1.np_charge_max)
                    elif i == 2:
                        if self.servant_2.health <= 0:
                            continue
                        self.servant_2.np_charge += float(buff_num.strip('%'))
                        self.servant_2.np_charge = min(self.servant_2.np_charge, self.servant_2.np_charge_max)
                    elif i == 3:
                        if self.servant_3.health <= 0:
                            continue
                        self.servant_3.np_charge += float(buff_num.strip('%'))
                        self.servant_3.np_charge = min(self.servant_3.np_charge, self.servant_3.np_charge_max)
        # 之后计算死亡
        if order == 1:
            self.servant_1 = self.servant_4
            self.servant_4 = self.servant_5
            self.servant_5 = self.servant_6
            self.servant_6 = Servant(order=6)
        elif order == 2:
            self.servant_2 = self.servant_4
            self.servant_4 = self.servant_5
            self.servant_5 = self.servant_6
            self.servant_6 = Servant(order=6)
        elif order == 3:
            self.servant_3 = self.servant_4
            self.servant_4 = self.servant_5
            self.servant_5 = self.servant_6
            self.servant_6 = Servant(order=6)
        else:
            return
        self.servant_1.order = 1
        self.servant_2.order = 2
        self.servant_3.order = 3
        self.servant_4.order = 4
        self.servant_5.order = 5
        self.servant_6.order = 6

     # 换人
    def change_order(self, order_list):
        if order_list == (1, 4):
            self.servant_1, self.servant_4 = self.servant_4, self.servant_1
            servant_a, servant_b = self.servant_4, self.servant_1
        elif order_list == (1, 5):
            self.servant_1, self.servant_5 = self.servant_5, self.servant_1
            servant_a, servant_b = self.servant_5, self.servant_1
        elif order_list == (1, 6):
            self.servant_1, self.servant_6 = self.servant_6, self.servant_1
            servant_a, servant_b = self.servant_6, self.servant_1
        elif order_list == (2, 4):
            self.servant_2, self.servant_4 = self.servant_4, self.servant_2
            servant_a, servant_b = self.servant_4, self.servant_2
        elif order_list == (2, 5):
            self.servant_2, self.servant_5 = self.servant_5, self.servant_2
            servant_a, servant_b = self.servant_5, self.servant_2
        elif order_list == (2, 6):
            self.servant_2, self.servant_6 = self.servant_6, self.servant_2
            servant_a, servant_b = self.servant_6, self.servant_2
        elif order_list == (3, 4):
            self.servant_3, self.servant_4 = self.servant_4, self.servant_3
            servant_a, servant_b = self.servant_4, self.servant_3
        elif order_list == (3, 5):
            self.servant_3, self.servant_5 = self.servant_5, self.servant_3
            servant_a, servant_b = self.servant_5, self.servant_3
        elif order_list == (3, 6):
            self.servant_3, self.servant_6 = self.servant_6, self.servant_3
            servant_a, servant_b = self.servant_6, self.servant_3
        else:
            return

        self.servant_1.order = 1
        self.servant_2.order = 2
        self.servant_3.order = 3
        self.servant_4.order = 4
        self.servant_5.order = 5
        self.servant_6.order = 6
        self.battle_strategy += '\n御主使用3技能：交换' + str(servant_b.order) + '号位' + servant_b.name
        self.battle_strategy += '与' + str(servant_a.order) + '号位' + servant_a.name


def main():
    bc = BattleConfig()
    bc.battle_ground = '燃烧'
    start = time.time()
    bc.servant_1 = Servant(order=1, servant_id=6, level=80, skill_level=(4, 4, 8), np_level=5)
    bc.servant_2 = Servant(order=2, servant_id=24, level=70, skill_level=(10, 10, 10), np_level=5)
    bc.enemy_11 = Servant(order=3, servant_id=215, level=70, skill_level=(10, 10, 10), np_level=5)
    bc.enemy_11.health = 100000
    bc.enemy_11.health_start = 100000
    bc.master = Master(1, 10)
    bc.round_start(1)
    bc.use_skill(order=1, skill=1)
    bc.use_skill(order=1, skill=2)
    bc.use_skill(order=1, skill=3)
    # bc.use_np(order=2, target=1)
    bc.use_np(order=1, target=1)
    print(bc.enemy_1.damage)
    print(bc.enemy_1.state)


def test():
    bc = BattleConfig()
    df_result = pd.DataFrame()
    for i in range(1, 281):
        # bc = BattleConfig()
        # bc.battle_ground = '燃烧'
        start = time.time()
        try:
            bc.servant_1 = Servant(order=1, servant_id=i, level=90, skill_level=(10, 10, 10), np_level=5)
        except:
            continue
        if bc.servant_1.name == '':
            continue

        bc.enemy_11 = Servant(order=1, servant_id=112, level=90, skill_level=(10, 10, 10), np_level=5)
        bc.enemy_11.health = 100000
        bc.enemy_11.health_start = 100000
        bc.master = Master(1, 10)
        bc.round_start(1)
        try:
            bc.use_skill(order=1, skill=1, target=1)
        except Exception as f:
            print(bc.servant_1.servant_id, bc.servant_1.name, '1技能无法触发', f)

        try:
            bc.use_skill(order=1, skill=2, target=1)
        except Exception as f:
            print(bc.servant_1.servant_id, bc.servant_1.name, '2技能无法触发', f)

        try:
            bc.use_skill(order=1, skill=3, target=1)
        except Exception as f:
            print(bc.servant_1.servant_id, bc.servant_1.name, '3技能无法触发', f)

        try:
            bc.use_np(order=1, target=1, random_num=1)
        except Exception as f:
            print(bc.servant_1.servant_id, bc.servant_1.name, '宝具无法触发', f)

        # print(bc.enemy_1.damage, bc.servant_1.name)
        df_result = df_result.append({'中文名': bc.servant_1.name, '伤害':bc.enemy_1.damage}, ignore_index=True)

    df_result = df_result.sort_values(by='伤害', ascending=False)
    df_result.to_csv('test_result.csv', encoding='utf-8-sig', index=False)




if __name__ == '__main__':
    test()
