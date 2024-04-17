from os import listdir, popen, path
from random import choice

def get_after(text, substring):
    res = text[text.index(substring) + len(substring):]
    return res[:res.index('\n')].strip()

SYSTEM_DATA = {}
unparsed = popen('hostnamectl').read()
SYSTEM_DATA['Имя системы:   '] = get_after(unparsed, 'Operating System: ')
SYSTEM_DATA['Ядро:          '] = get_after(unparsed, 'Kernel: ')
SYSTEM_DATA['Работает:      '] = popen('uptime -p').read()[3:].strip()
SYSTEM_DATA['Пользователь:  '] = popen('whoami').read().strip()
SYSTEM_DATA['Заряд:         '] = popen('upower -i /org/freedesktop/UPower/devices/battery_BAT0').read().split('percentage:')[1].split('\n')[0].strip()
SYSTEM_DATA['ЦП:            '] = get_after(unparsed, 'Architecture: ')
SYSTEM_DATA['               '] = get_after(popen('cat /proc/cpuinfo').read(), 'model name')[3:]
with open('/proc/meminfo') as file:
    data = file.readlines()
    SYSTEM_DATA['ОЗУ занято:    '] = str(int(data[1].split()[-2]) // 1024) + ' MB'
    SYSTEM_DATA['ОЗУ всего:     '] = str(int(data[0].split()[-2]) // 1024) + ' MB'


keys = list(SYSTEM_DATA.keys())
dir_path = path.dirname(path.realpath(__file__))
flags = listdir(path.join(dir_path, 'flags'))
with open(path.join(dir_path, 'flags', choice(flags))) as file:
    pos = 0
    for line in file.readlines()[:-1]:
        try:
            print(line.strip(), '\t', keys[pos], SYSTEM_DATA[keys[pos]], sep=' ')
            pos += 1
        except IndexError:
            print(line)
    for i in keys[pos: ]:
        print('\t' * 6, i, SYSTEM_DATA[i] , sep=' ')
print('Боже, Царя храни!')
