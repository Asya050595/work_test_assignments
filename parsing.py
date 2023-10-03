#Работа была выполнена в Google Colab

os.system('wget -O sample.vcf https://www.dropbox.com/scl/fi/w1n7b36bndw9fvbvw1vg7/sample.vcf?rlkey=ip24fyzjorfumc8fkw8qp3y7k&dl=0')
from pandas import DataFrame

with open('/content/sample.vcf', 'r', encoding='utf-8') as f:
    head = None
    while True:
        head = f.readline()
        if '#CHROM' in head:
            break

    headers = head.replace('\n', '').replace('#', '').split('\t')

    d = [[] for _ in range(len(headers))]

    for a in f.readlines():
        r = a.split('\t')
        if len(r) != len(headers):
            continue
        for i in range(len(r)):
            d[i].append(r[i])

    p = {}

    for i in range(len(headers)):
        title = headers[i]
        column = d[i]
        p[title] = column

    pd = DataFrame(p)

    pd.to_excel('/content/test.xlsx', sheet_name='Sheet1', index=False)

# VCF (от Variant Call Format) - формат файла, используемый для записи вариантов (SNP / InDel). В таблице, полученной по ссылке, приведены следующие колонки:
  #CHROM - номер хромосомы;    POS - позиция, в которой вариант изменен (первое основание);
  #ID - идентификатор варианта (соответствует базе данных dbSNP; "." по умолчанию при несоответствии dbSNP);
  #REF - аллель эталонной последовательности;
  #ALT - вариант аллель;
  #QUAL - качество варианта (чем выше значения, тем выше вероятность мутации);
  #FILTER - отвечает на вопрос, надо ли отфильтровать вариант: если 'PASS' - не нужно;
  #INFO - информация о варианте;
  #FORMAT - формат вариантов;
  #3 - от Samples, значения соответствуют форматам столбца FORMAT и разделяются двоеточиями.

#DP (от 'Read Depth' - 'Покрытие чтения') - указывает покрытие чтения после фильтрации.
#MQ (от 'Mapping quality' - 'Качество сопоставления') - значение качества сопоставления.
#ExcessHet (от 'Excess heterozygosity' - 'Избыточная гетерозиготность') - оценивает вероятность
#избыточной гетерозиготности образцов при нулевой гипотезе о том, что образцы не связаны между собой.

# !!! Нарисуйте распределение параметров DP и MQ из колонки INFO !!!

from pandas import DataFrame
import matplotlib.pyplot as plt


with open('sample.vcf', 'r', encoding='utf-8') as f:
    head = None
    while True:
        head = f.readline()
        if '#CHROM' in head:
            break

    headers = head.replace('\n', '').replace('#', '').split('\t')

    d = [[] for _ in range(len(headers))]
    for a in f.readlines():
        r = a.split('\t')
        if len(r) != len(headers):
            continue
        for i in range(len(r)):
            d[i].append(r[i])

    p = {}


    for i in range(len(headers)):
        title = headers[i]
        column = d[i]
        p[title] = column

    infos = p['INFO']

    freq_dp = {}
    freq_mq = {}

    for info_str in infos:

        info = info_str.split(';')

        data_dp_raw = list(filter(lambda x: x.startswith('DP='), info))[0]
        data_dp = data_dp_raw.split('=')[-1]

        data_mq_raw = list(filter(lambda x: x.startswith('MQ='), info))[0]
        data_mq = data_mq_raw.split('=')[-1]

        if data_dp in freq_dp:
            freq_dp[data_dp] += 1
        else:
            freq_dp[data_dp] = 1

        if data_mq in freq_mq:
            freq_mq[data_mq] += 1
        else:
            freq_mq[data_mq] = 1

    plt.bar(freq_dp.keys(), freq_dp.values())
    plt.savefig('plot_dp.png')

    plt.clf()
    plt.bar(freq_mq.keys(), freq_mq.values())
    plt.savefig('plot_mq.png') #во всех строках mq оказался равен 60.00

    pd = DataFrame(p)

    pd.to_excel('test.xlsx', sheet_name='Sheet1', index=False)

# !!! Отфильтруйте SNP, оставьте только "Coding", "HIGH", "MODERATE". Что значат эти парметры? !!!

from typing import List

LIMIT = -1

def get_from_info(info: List[str], parameter: str) -> str:
    data_raw = list(filter(lambda x: x.startswith(parameter + '='), info))[0]
    return data_raw.split('=')[-1]


def rows_to_dict(rows: list, headers: list) -> dict:
    d = [[] for _ in range(len(headers))]
    p = {}

    for a in rows:
        r = a.split('\t')
        if len(r) != len(headers):
            continue
        for i in range(len(r)):
            d[i].append(r[i])

    for i in range(len(headers)):
        title = headers[i]
        column = d[i]
        p[title] = column

    return p


with open('sample.vcf', 'r', encoding='utf-8') as f:
    head = None
    while True:
        head = f.readline()
        if '#CHROM' in head:
            break

    headers = head.replace('\n', '').replace('#', '').split('\t')

    data = f.readlines()
    if LIMIT != -1:
        data = data[:LIMIT]

    p = rows_to_dict(data, headers)

    data_filtered = []
    for i in range(len(data)):
        info = p['INFO'][i].split(';')
        ann = get_from_info(info, 'ANN')
        if 'Coding' and 'HIGH' in ann or 'Coding' and 'MODERATE' in ann:
            data_filtered.append(data[i])

    p_filtered = rows_to_dict(data_filtered, headers)

    pd = DataFrame(p)
    pd.to_excel('test.xlsx', sheet_name='Sheet1', index=False)

    pd2 = DataFrame(p_filtered)
    pd2.to_excel('test2.xlsx', sheet_name='Sheet1', index=False)

#Показатели 'HIGH' и 'MODERATE' (а также 'LOW') относятся к оценке патогенности варианта. 'Coding' указывает, является ли вариант кодирующим.

# !!! Выберете 3 типа мутаций и опишите их !!!

freq_var = {}
    for info_str in p['INFO']:
        info = info_str.split(';')
        ann = get_from_info(info, 'ANN')
        variant = ann.split('|')[1].replace('_variant', '')
        if variant in freq_var:
            freq_var[variant] += 1
        else:
            freq_var[variant] = 1

    for k in freq_var.keys():
        print(f'{k}: {freq_var[k]}')

#Missense variant - измененный кодон кодирует другую аминокислоту.
#Synonymous variant - синонимическая мутация, то есть кодон продолжает кодировать ту же аминокислоту.
#Stop lost variant - вариант, при котором стоп-кодон изменен так, что транскрипт оказался длинее референса.

#!!! Сколько в файле "missense_variant"? !!!

 freq_var = {}
    for info_str in p['INFO']:
        info = info_str.split(';')
        ann = get_from_info(info, 'ANN')
        variant = ann.split('|')[1].replace('_variant', '')
        if variant in freq_var:
            freq_var[variant] += 1
        else:
            freq_var[variant] = 1

    for k in freq_var.keys():
          if k == 'missense':
            print(f'{k}: {freq_var[k]}')
