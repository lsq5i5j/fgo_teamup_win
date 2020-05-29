import pandas as pd


def main(type):
	df = pd.read_csv('./data/servant_data_'+type+'.csv')
	df_event = pd.read_csv('./data/event_list_bk.csv')
	event_list = tuple(df_event['事件名称'].values)
	print(event_list)
	df1 = df[df['强化'] == '强化前']
	df2 = df[df['强化'] == '强化后']
	df3 = df[df['强化'] == '未强化']
	df_jp = pd.concat([df2, df3])

	df_furture = pd.DataFrame()
	for event in event_list:
		df_temp1 = df[df['强化时间'] == event]
		df_furture = pd.concat([df_furture, df_temp1])
	print(df_furture)

	df_enhanced = pd.concat([df1, df2])
	df_now = df_enhanced.drop(labels=df_furture.axes[0])
	print(df_now)

	df_now = df_now[df_now['强化'] == '强化后']
	df_furture = df_furture[df_furture['强化'] == '强化前']
	df_cn = pd.concat([df_now, df_furture, df3])
	df_cn = df_cn.sort_values(by="ID", ascending=True)  # by指定按哪列排序。ascending表示是否升序
	df_jp = df_jp.sort_values(by="ID", ascending=True)  # by指定按哪列排序。ascending表示是否升序
	df_cn.to_csv('./data/servant_data_'+type+'_cn.csv', encoding='utf-8-sig')
	df_jp.to_csv('./data/servant_data_'+type+'_jp.csv', encoding='utf-8-sig')


def main2(event_name):
	df_event = pd.read_csv('./data/event_list_bk.csv')
	df_event_new = pd.read_csv('./data/event_list_bk.csv')
	for index, row in df_event.iterrows():
		if row['事件名称'] != event_name:
			df_event_new = df_event_new.drop([index])
		else:
			break
	print(df_event_new)




if __name__ == '__main__':
	# main('skill')
	# main('noblephantasm')
	main2('从者强化任务第11弹')

