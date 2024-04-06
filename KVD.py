import numpy as np
from scipy.fftpack import fftfreq, ifft, fft

time_list, ampl_list = [], []

count_of_lines_in_file = int(input('Пожалуйста, введите количество строк в файле '))
print('Скопируйте сюда строки из файла')
for i in range(count_of_lines_in_file):
    try:
        tim, ampl = map(float, input().split(','))
        time_list.append(tim)
        ampl_list.append(ampl)
    except:
        continue


def fourier_transform(y, t, s):
    s_fft_filtered = fft(y)
    freq = fftfreq(len(y), d=1./s)
    s_fft_filtered[np.abs(freq) > t] = 0
    return ifft(s_fft_filtered)

t = 10
s = 100

ampl_list = fourier_transform(ampl_list, t, s)

def average_reduction_value(ampl_list):
    reduction = []
    for i in range(1, len(ampl_list) - 1):
        reduction.append(np.abs(ampl_list[i] - ampl_list[i+1]))
    return sum(reduction)/len(reduction)

def average_value(ampl_list):
    return sum(ampl_list)/len(ampl_list)

sr_snij = average_reduction_value(ampl_list)
sr_zn = average_value(ampl_list)
vremena = []
launch = 0

for i in range(1, len(ampl_list) - 1):
    if np.abs(ampl_list[i] - ampl_list[i+1]) < sr_snij and launch == 0:
        launch = 1
    if ampl_list[i] + sr_snij >= max(ampl_list) and launch == 1:
        if len(vremena) == 0:
            vremena.append([time_list[i], ampl_list[i]])
        elif np.abs(vremena[-1][0] - time_list[i]) > 0.0001:
            vremena.append([time_list[i], ampl_list[i]])
    if np.abs(ampl_list[i] - ampl_list[i+1]) >= sr_snij and launch == 1:
        launch = 0

list_of_up = []
distance_in_time = []
for i in range(len(vremena) - 1):
    tim, ampl = vremena[i]
    distance_in_time.append(np.abs(vremena[i+1][0] - tim))
average_distance = sum(distance_in_time)/len(distance_in_time)
total_columns = []
interval_value = []
for i in range(len(distance_in_time)):
    if distance_in_time[i] <= average_distance:
        interval_value.append(i)
    else:
        interval_value.append(i)
        total_columns.append(interval_value)
        interval_value = []

for times in total_columns:
    maximums = 0
    total = []
    for t in times:
        if vremena[t][1] > maximums:
            maximums = vremena[t][1]
            total = vremena[t]
    list_of_up.append(total)

periods = []
terrible_errors = 0

for i in range(len(list_of_up) - 1):
    tim, ampl = list_of_up[i]
    periods.append(np.abs(list_of_up[i+1][0] - tim))


period = sum(periods)/len(periods)

for er in range(len(periods)):
    terrible_errors += (periods[er] - period)**2

odds = {2:12.7, 3:4.3, 4:3.2, 5:2.8, 6:2.6, 7:2.4, 8:2.4, 9:2.3, 10:2.3}
s1 = ((terrible_errors/((len(periods) - 1)*len(periods)))**0.5)*odds.get(len(periods), 2.3)

list_of_lines = []
all_time = np.abs(time_list[-1] - time_list[0])
wave = all_time/period
range_of_values = [sr_zn, sr_zn + sr_snij]

for i in range(len(time_list)):
    a = len(list_of_lines) == 0
    if range_of_values[0] <= ampl_list[i] <= range_of_values[1]:
        if a:
            list_of_lines.append(i)
        else:
            if np.abs(time_list[list_of_lines[-1]] - time_list[i]) > 0.0001:
                list_of_lines.append(i)

counts_of_lines = round(len(list_of_lines)/wave)
len_of_wave = 532
s3 = 0.1

print(f'Частота колебания зеркала равна {round(1/period, 3)} Гц, програмная погрешность может быть равна {round(s1/period**2, 3)} Гц')
print(f'Амплитуда перемещений зеркала равна {round((len_of_wave * counts_of_lines)/4, 3)} нм, програмная погрешность может быть равна {round(counts_of_lines*s3/4, 3)} нм')
print(f'Средняя скорость перемещения зеркала равна {round((len_of_wave * counts_of_lines)/(2 * period), 3)} нм/сек, програмная погрешность может быть равна {round((counts_of_lines * s3)/(2*period) + (counts_of_lines * len_of_wave * s1)/(2*(period**2)), 3)} нм/сек')
