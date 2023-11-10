import create_csv
from datetime import datetime, timedelta
import pandas as pd


class Position:
    def __init__(self, name, num):
        self.name = name
        self.soldiers_num = num


def handle_time(start_time, end_time, intervals):
    try:
        time_list = []
        last_time = start_time
        intervals = timedelta(hours=intervals)
        while last_time < end_time:
            time_list.append(last_time)
            last_time += intervals
        return time_list
    except Exception as e:
        print("error in handle time:")
        print(e)


def get_int_guard_num(positions: list[Position]) -> int:
    guard_num = 0
    for pos in positions:
        guard_num += pos.soldiers_num
    return guard_num


def create_df(shavtsak, position_names, do_shuffle, file_name):
    # writer = csv.writer(csv_file)
    # writer.writerow(["time"] + position_names)
    # for time_slot in shavtsak_data:
    #     shavtsak_row = shavtsak_data[time_slot]
    #     if do_shuffle:
    #         shuffle(shavtsak_row)
    #     writer.writerow([time_slot] + shavtsak_row)
    df = pd.read_csv(file_name)
    return df


def create_shavtsak(guarding_soldiers, start_time, end_time, intervals, position_names, interval_guard_num, do_shuffle):
    soldiers_num = len(guarding_soldiers)
    time_slots = handle_time(
        start_time,
        end_time,
        intervals)
    total_slots = interval_guard_num * len(time_slots)
    add_a_round = 0
    if total_slots % soldiers_num > 0:
        add_a_round = 1
    rounds = (total_slots // soldiers_num) + add_a_round
    final_soldier_list = guarding_soldiers * rounds
    shavtsak = {}
    pointer = 0
    for time_slot in time_slots:
        shavtsak[time_slot] = final_soldier_list[pointer:pointer+interval_guard_num]
        pointer += interval_guard_num
    file_name = create_csv.write_to_file(shavtsak, position_names, do_shuffle)
    df = create_df(shavtsak, position_names, do_shuffle, file_name)
    return df