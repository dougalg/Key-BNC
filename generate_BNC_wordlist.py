from KEY_BNC.KEY_BNC import KEY_BNC
import csv

def print_name(the_name):
	print(the_name)

target_dir = r'D:\BNC-TXT'

calculator = KEY_BNC()
calculator.load_target_data_dir(target_dir)

with open('New_BNC_wordlist.csv', mode='w', encoding='utf8', newline='') as outf:
	writer = csv.writer(outf)
	i = 0
	writer.writerow(['Rank', 'Frequency', 'Word'])
	for rank, fw in enumerate(calculator.target_words.most_common()):
		writer.writerow([rank, fw[1], fw[0]])
