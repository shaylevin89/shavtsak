import logic
import random
import streamlit as st
import pandas as pd
import datetime


def prepare_data(guarding_soldiers, first_shuffle, start_time, end_time, intervals, positions, row_shuffle):
    if first_shuffle:
        random.shuffle(guarding_soldiers)
    do_shuffle = row_shuffle
    positions_num = len(positions)
    position_names = []
    interval_guard_num = 0
    for position_num in range(positions_num):
        position_dict = positions[f"pos_{position_num}"]
        position_name = position_dict["pos_name"]
        soldier_in_position = position_dict["guards"]
        interval_guard_num += soldier_in_position
        if soldier_in_position > 1:
            for i in range(1, soldier_in_position + 1):
                position_names.append(f"{position_name}_{i}")
        else:
            position_names.append(position_name)

    shavtzak = logic.create_shavtsak(guarding_soldiers,
                                     start_time,
                                     end_time,
                                     intervals,
                                     position_names,
                                     interval_guard_num,
                                     do_shuffle)
    st.session_state.shavtsak = shavtzak


def get_soldiers(edited_df):
    soldiers = []
    for ind, row in edited_df.iterrows():
        if row.get('active'):
            soldiers.append(row['name'])
    return soldiers


def change_stage(stage_name):
    st.session_state.stage = stage_name
    if st.session_state.stage == "done":
        soldiers = get_soldiers(st.session_state.edited_df)
        prepare_data(soldiers,
                     st.session_state.shuffle_names,
                     st.session_state.start_time,
                     st.session_state.end_time,
                     st.session_state.intervals,
                     st.session_state.positions,
                     st.session_state.do_shuffle)
        st.session_state.stage = "show"


def get_names():
    """
    this function take the file names.txt and parse it line by line to names list
    no comma or any seperator. one name per line
    :return: names
    """
    with open('names.txt', 'r') as f:
        names = []
        for line in f:
            names.append(line)
        return names


if __name__ == '__main__':
    default_soldiers = get_names()
    st.set_page_config(page_title="shavtsak", layout="centered")
    st.header(':blue[שבצק] :sunglasses:', divider='rainbow')

    if 'stage' not in st.session_state:
        st.session_state.stage = "start"
    if st.session_state.stage == "start":
        start_date = st.date_input("תאריך התחלה")
        s_time = st.time_input("שעת התחלה", datetime.time(16, 0))
        start_time = datetime.datetime(start_date.year, start_date.month, start_date.day, s_time.hour, s_time.minute)
        st.session_state.start_time = start_time
        st.button("המשך", on_click=change_stage, args=["start_time"])
    if st.session_state.stage == "start_time":
        end_date = st.date_input("תאריך סיום", datetime.datetime.today() + datetime.timedelta(days=1))
        e_time = st.time_input("שעת סיום", datetime.time(16, 0))
        end_time = datetime.datetime(end_date.year, end_date.month, end_date.day, e_time.hour, e_time.minute)
        st.session_state.end_time = end_time
        st.button("המשך", on_click=change_stage, args=["end_time"])
    if st.session_state.stage == "end_time":
        shuffle_names = st.checkbox("לערבב את סדר רשימת השמות")
        do_shuffle = st.checkbox("לערבב כל שורה בשבצק")
        intervals = st.slider("?כמה שעות כל שמירה", 1, 8, 2)
        positions_num = st.slider("?כמה עמדות יש", 1, 7, 3)
        st.session_state.shuffle_names = shuffle_names
        st.session_state.do_shuffle = do_shuffle
        st.session_state.intervals = intervals
        st.session_state.positions_num = positions_num
        st.button("המשך", on_click=change_stage, args=["positions"])
    if st.session_state.stage == "positions":
        for pos in range(st.session_state.positions_num):
            if pos == 0:
                pos_name = st.text_input("שם העמדה", "ש.ג", key=f"pos_{pos}")
                guards = st.slider("מספר שומרים", 1, 4, 2, key=f"guards_{pos}")
                st.session_state.positions = {f"pos_{pos}": {"pos_name": pos_name, "guards": guards}}
            elif pos == 1:
                pos_name = st.text_input("שם העמדה", "פחיות", key=f"pos_{pos}")
                guards = st.slider("מספר שומרים", 1, 4, 1, key=f"guards_{pos}")
                st.session_state.positions[f"pos_{pos}"] = {"pos_name": pos_name, "guards": guards}
            elif pos == 2:
                pos_name = st.text_input("שם העמדה", "תצפית", key=f"pos_{pos}")
                guards = st.slider("מספר שומרים", 1, 4, 1, key=f"guards_{pos}")
                st.session_state.positions[f"pos_{pos}"] = {"pos_name": pos_name, "guards": guards}
            else:
                pos_name = st.text_input("שם העמדה", "", key=f"pos_{pos}")
                guards = st.slider("מספר שומרים", 1, 4, 1, key=f"guards_{pos}")
                st.session_state.positions[f"pos_{pos}"] = {"pos_name": pos_name, "guards": guards}
        st.button("המשך", on_click=change_stage, args=["choose_soldiers"])
    if st.session_state.stage == "choose_soldiers":
        df = pd.DataFrame(
            [
                {"name": x, "active": True} for x in default_soldiers
            ]
        )
        edited_df = st.data_editor(df, num_rows="dynamic", width=300, height=1200)
        st.session_state.edited_df = edited_df
        st.button("סיום", on_click=change_stage, args=["done"])
    if st.session_state.stage == "show":
        st.table(st.session_state.shavtsak)
        st.balloons()
