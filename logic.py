import create_csv
from datetime import timedelta
import pandas as pd


class Position:
    def __init__(self, name, num):
        self.name = name
        self.soldiers_num = num


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


def get_slots_to_reduce(df):
    slots_to_reduce = 0
    time_constraint_dict = {}
    for ind, row in df.iterrows():
        if row.get('active'):
            sold_name = row['name']
            if row.get("constraint1"):
                if row.get("constraint1") not in time_constraint_dict:
                    time_constraint_dict[row.get("constraint1")] = [sold_name]
                else:
                    time_constraint_dict[row.get("constraint1")].append(sold_name)
                slots_to_reduce += 1
            if row.get("constraint2"):
                if row.get("constraint2") not in time_constraint_dict:
                    time_constraint_dict[row.get("constraint2")] = [sold_name]
                else:
                    time_constraint_dict[row.get("constraint2")].append(sold_name)
                slots_to_reduce += 1
            if row.get("constraint3"):
                if row.get("constraint3") not in time_constraint_dict:
                    time_constraint_dict[row.get("constraint3")] = [sold_name]
                else:
                    time_constraint_dict[row.get("constraint3")].append(sold_name)
                slots_to_reduce += 1
    return slots_to_reduce, time_constraint_dict


def create_shavtsak(guarding_soldiers, time_slots, position_names, interval_guard_num, do_shuffle, df):
    soldiers_num = len(guarding_soldiers)
    slots_to_reduce, time_constraint_dict = get_slots_to_reduce(df)
    total_slots = (interval_guard_num * len(time_slots)) - slots_to_reduce
    add_a_round = 0
    if total_slots % soldiers_num > 0:
        add_a_round = 1
    rounds = (total_slots // soldiers_num) + add_a_round
    final_soldier_list = guarding_soldiers * rounds
    shavtsak = {}
    pointer = 0
    for time_slot in time_slots:
        if time_slot in time_constraint_dict:
            added_sold_num = len(time_constraint_dict[time_slot])
            if added_sold_num == interval_guard_num:
                shavtsak[time_slot] = time_constraint_dict[time_slot]
            else:
                shavtsak[time_slot] = final_soldier_list[pointer:pointer+interval_guard_num-added_sold_num]
                for sold in time_constraint_dict[time_slot]:
                    shavtsak[time_slot].append(sold)
                pointer += interval_guard_num-added_sold_num
        else:
            shavtsak[time_slot] = final_soldier_list[pointer:pointer+interval_guard_num]
            pointer += interval_guard_num
    file_name = create_csv.write_to_file(shavtsak, position_names, do_shuffle)
    df = create_df(shavtsak, position_names, do_shuffle, file_name)
    return df