import logic
import random
import streamlit as st
import pandas as pd
import datetime
from datetime import timedelta
from time import sleep
import os


colors = [
         "#FF0000",  # Red
         "#0000FF",  # Blue
         "#800080",  # Purple
         "#FFC0CB",  # Pink
         "#FF69B4",  # Fuchsia
         "#FFA07A",  # Coral
         "#ADD8E6",  # Light blue 10
         "#FF007F",  # Maroon
         "#9932CC",  # Steel blue
         "#8A2BE2",  # Blue violet
         "#EE82EE",  # Violet
         "#DA70D6",  # Orchid
         "#FF1493",  # Deep pink
         "#A0522D",  # Sienna
         "#CD5C5C",  # Indian red
         "#B22222",  # Firebrick
         "#8B0000",  # Dark red 20
         "#8B4513",  # Saddle brown
         "#A020F0",  # Purple
         "#483D8B",  # Dark slate blue
         "#00CED1",  # Dark turquoise
         "#4169E1",  # Royal blue
         "#000080",  # Navy 30
         "#C5E0DC",  # Pastel blue
         "#B8B8B8",  # Light goldenrod yellow
         "#B4EEB4",  # Pale green
         "#B0C4DE",  # Powder blue
         "#A9A9A9",  # Dark gray
         "#A5D6A7",  # Pale turquoise
         "#A8DADC",  # Light cornflower blue
         "#A52A2A",  # Brown
         "#A2A2A2",  # Light slate gray
         "#9E9E9E",  # Dim gray
         "#9ACD32",  # Yellow green
         "#98FB98",  # Green yellow
         "#9470D4",  # Light slate violet
         "#90EE90",  # Light sea green
         "#87CEFA",  # Light sky blue
         "#87CEEB",  # Baby blue
         "#81C784",  # Pale green
         "#7FFFD4",  # Aquamarine
         "#7EC0EE",  # Powder blue
         "#7CFC00",  # Lawn green
         "#778899",  # Light slate gray
         "#76EEC6",  # Light cyan
         "#708090",  # Slate gray
         "#66CDFF",  # Sky blue
         "#66CACA",  # Gray web
         "#6495ED",  # Cornflower blue
         "#607B8B",  # Slate gray
         "#5F9EA0",  # Cadet blue
         "#556B2F",  # Dark olive green
         "#548B57"  # Sea green
]


def handle_time(start_time, end_time, intervals):
    try:
        time_list = []
        last_time = start_time
        intervals = timedelta(hours=intervals)
        while last_time < end_time:
            time_list.append(str(last_time))
            last_time += intervals
        return time_list
    except Exception as e:
        print("error in handle time:")
        print(e)


def prepare_data(guarding_soldiers, first_shuffle, positions, row_shuffle, df):
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
    st.session_state.position_names = position_names
    shavtzak = logic.create_shavtsak(guarding_soldiers,
                                     st.session_state.time_slots,
                                     position_names,
                                     interval_guard_num,
                                     do_shuffle,
                                     df)
    st.session_state.shavtsak = shavtzak


def get_soldiers(edited_df):
    soldiers = []
    for ind, row in edited_df.iterrows():
        if row.get('active'):
            if not row.get("constraint1"):
                if not row.get("constraint2"):
                    if not row.get("constraint3"):
                        soldiers.append(row['name'])
    return soldiers


def create_colors_dict(edited_df):
    colors_dict = {}
    for ind, row in edited_df.iterrows():
        if row.get('active'):
            name = row['name']
            if ind <= len(colors):
                colors_dict[name] = colors[ind]
    return colors_dict

def paint_names(name):
    color = st.session_state.paints[name]
    return f'background-color: {color}'


def get_names():
    """
    this function take the file names.txt and parse it line by line to names list
    no comma or any seperator. one name per line
    :return: names
    """
    if st.session_state.admin_pass == os.getenv('ADMIN_PASS', 'nopass'):
        names = os.getenv('NAMES').split(",")
    else:
        with open('names.txt', 'r') as f:
            names = []
            for line in f:
                names.append(line)
    return names


def change_stage(stage_name):
    st.session_state.stage = stage_name
    if stage_name == "connect":
        if st.session_state.admin_pass != os.getenv('ADMIN_PASS', 'nopass'):
            st.warning("אתה לא ממחלקה 2 כנראה. ניכנסת כאנונימי")
            sleep(3)
            st.session_state.stage = "start"
        else:
            st.warning("אתה ממחלקה 2. ברוך הבא")
            sleep(3)
            st.session_state.stage = "start"
    if st.session_state.stage == "positions":
        time_slots = handle_time(
            st.session_state.start_time,
            st.session_state.end_time,
            st.session_state.intervals
        )
        st.session_state.time_slots = time_slots
    if st.session_state.stage == "done":
        soldiers = get_soldiers(st.session_state.edited_df)
        st.session_state.paints = create_colors_dict(st.session_state.edited_df)
        prepare_data(soldiers,
                     st.session_state.shuffle_names,
                     st.session_state.positions,
                     st.session_state.do_shuffle,
                     st.session_state.edited_df)
        st.session_state.stage = "show"


if __name__ == '__main__':
    # default_soldiers = get_names()
    st.set_page_config(page_title="shavtsak", layout="centered")
    st.header(':blue[שבצק] :sunglasses:', divider='rainbow')

    if 'stage' not in st.session_state:
        st.session_state.stage = "login"
    if st.session_state.stage == "login":
        password = st.text_input("סיסמה למחלקה 2:", type="password")
        st.session_state.admin_pass = password
        st.button("התחבר", on_click=change_stage, args=["connect"])
        st.button("דלג", on_click=change_stage, args=["start"])
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
        default_soldiers = get_names()
        df = pd.DataFrame(
            [
                {"name": x, "active": True, "constraint1": "", "constraint2": "", "constraint3": ""} for x in default_soldiers
            ]
        )
        edited_df = st.data_editor(
            df, num_rows="dynamic", width=800, height=1200,
            column_config={
                "constraint1": st.column_config.SelectboxColumn(
                    "constraint1",
                    width="small",
                    options=st.session_state.time_slots,
                    required=False,
                ),
                "constraint2": st.column_config.SelectboxColumn(
                    "constraint1",
                    width="small",
                    options=st.session_state.time_slots,
                    required=False,
                ),
                "constraint3": st.column_config.SelectboxColumn(
                    "constraint1",
                    width="small",
                    options=st.session_state.time_slots,
                    required=False,
                )
            },
            hide_index=False,
        )
        st.session_state.edited_df = edited_df
        st.button("סיום", on_click=change_stage, args=["done"])
    if st.session_state.stage == "show":
        st.dataframe(
            st.session_state.shavtsak.style.applymap(
                paint_names,
                subset=st.session_state.position_names
            ),
            hide_index=False,
            width=600,
            height=600
        )
        st.balloons()

