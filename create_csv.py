import csv
from datetime import date
from random import shuffle


def prettify_date(time_slot):
    just_time = time_slot.split(" ")[-1]
    no_seconds_split = just_time.split(":")
    pretty_time = f'{no_seconds_split[0]}:{no_seconds_split[1]}'
    return pretty_time


def write_to_file(shavtsak_data, position_names, do_shuffle):
    file_name = f'shavtsak-{date.today()}.csv'
    with open(file_name, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["time"] + position_names)
        for time_slot in shavtsak_data:
            shavtsak_row = shavtsak_data[time_slot]
            if do_shuffle:
                shuffle(shavtsak_row)
            pretty_time = prettify_date(time_slot)
            writer.writerow([pretty_time] + shavtsak_row)
    return file_name
