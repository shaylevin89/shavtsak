import csv
from datetime import date
from random import shuffle


def write_to_file(shavtsak_data, position_names, do_shuffle):
    file_name = f'shavtsak-{date.today()}.csv'
    with open(file_name, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["time"] + position_names)
        for time_slot in shavtsak_data:
            shavtsak_row = shavtsak_data[time_slot]
            if do_shuffle:
                shuffle(shavtsak_row)
            writer.writerow([time_slot] + shavtsak_row)
    return file_name
