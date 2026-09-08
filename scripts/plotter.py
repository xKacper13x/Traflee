from matplotlib import pyplot
import csv


class Plotter:
    def __init__(self):
        pass

    def draw_plot(self, keys: list, values: list) -> None:
        i = 1
        for value_list in values:
            pyplot.plot(keys, value_list, label=f'label{i}')
            i+=1

        pyplot.legend()
        pyplot.xticks(rotation=90, fontsize='small')
        pyplot.show()


if __name__ == '__main__':
    plotter = Plotter()
    time_list = []
    load_list = []
    RPM_list = []

    with open('None_data.csv', 'r') as file_handle:
        reader = csv.DictReader(file_handle)

        for row in reader:
            time_list.append(float(row['time']))
            RPM_list.append(float(row['RPM']))
            load_list.append(float(row['load']))

    plotter.draw_plot(time_list, [load_list, RPM_list])
