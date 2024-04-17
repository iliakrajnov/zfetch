from os import listdir, popen, path
from random import choice


# Получение текста между указанным и концом строки
def get_after(text, substring):
    res = text[text.index(substring) + len(substring):]
    return res[:res.index('\n')].strip()


# Сбор данных о системе
SYSTEM_DATA = {}
unparsed = popen('hostnamectl').read()
SYSTEM_DATA['Имя системы:   '] = get_after(unparsed, 'Operating System: ')
SYSTEM_DATA['Ядро:          '] = get_after(unparsed, 'Kernel: ')
SYSTEM_DATA['Работает:      '] = popen('uptime -p').read()[3:].strip()
SYSTEM_DATA['Машина:        '] = get_after(unparsed, 'hostname: ')
SYSTEM_DATA['Пользователь:  '] = popen('whoami').read().strip()
try:
    SYSTEM_DATA['Питание:       '] = popen('upower -i /org/freedesktop/UPower/devices/battery_BAT0').read().split('percentage:')[1].split('\n')[0].strip()
except IndexError:
    SYSTEM_DATA['Питание:       '] = 'От сети'
SYSTEM_DATA['ЦП:            '] = get_after(unparsed, 'Architecture: ')
SYSTEM_DATA['               '] = get_after(popen('cat /proc/cpuinfo').read(), 'model name')[1:].strip()
with open('/proc/meminfo') as file:
    data = file.readlines()
    SYSTEM_DATA['ОЗУ занято:    '] = str(int(data[1].split()[-2]) // 1024) + ' MB'
    SYSTEM_DATA['ОЗУ всего:     '] = str(int(data[0].split()[-2]) // 1024) + ' MB'

# Начало вывода данных
keys = list(SYSTEM_DATA.keys())
dir_path = path.dirname(path.realpath(__file__))        # Папка, где находится скрипт
flags = listdir(path.join(dir_path, 'flags'))           # Все доступные флаги
with open(path.join(dir_path, 'flags', choice(flags))) as file:     # Печать флага и параметров
    pos = 0
    for line in file.readlines():
        try:
            print(line[:-1], '\t', keys[pos], SYSTEM_DATA[keys[pos]], sep=' ')
            pos += 1
        except IndexError:
            print(line)
for i in keys[pos: ]:       # Печать параметров после флага
    print('\t' * 6, i, SYSTEM_DATA[i] , sep=' ')
