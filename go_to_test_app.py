import datetime 
import json 
import random
import tkinter as tk

from tkinter import messagebox
from tkinter import ttk
from tkinter import simpledialog
from RangeSlider.RangeSlider import RangeSliderH, RangeSliderV
import pyttsx3
import logging
from tkinter import font as tkFont
import winsound
from PIL import Image, ImageTk

APP_CFG_FILENAME = "app_cfg.json"

CONST_CURRENT_TEST_DATA_SET = "NONE" # "1A" or "AL"
gamer_id = "NONE"

q_start_idx = 31
q_end_idx = 40

logger = None
logger_name = 'spelling_bee_logger'
log_filehandler = None

log_stream_handler = logging.StreamHandler()

def reset_logger():
    global log_filehandler
    _logger = logging.getLogger(__name__)
    _logger.setLevel(logging.INFO)
    if log_filehandler is not None:
        _logger.removeHandler(log_filehandler)
    log_filehandler = logging.FileHandler(f"testing_{CONST_CURRENT_TEST_DATA_SET}_{gamer_id}.log")    
    _logger.addHandler(log_filehandler)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_filehandler.setFormatter(formatter)
    log_stream_handler.setFormatter(formatter)
    if log_stream_handler not in _logger.handlers:
        _logger.addHandler(log_stream_handler)

    return _logger

logger = reset_logger()


def show_input_dialog():
    dialog = tk.Toplevel()
    dialog.title("Select Name")

    tk.Label(dialog, text="請選擇一個名字:").pack(pady=10)

    name_var = tk.StringVar()
    name_combobox = ttk.Combobox(dialog, textvariable=name_var)
    
    with open(APP_CFG_FILENAME, 'r') as f:
        cfg = json.load(f)

    name_combobox['values'] = cfg.get("Users", ["USER1", "USER2", "USER3"])
    name_combobox.current(0)
    name_combobox.pack(pady=10, padx=10)

    test_paper = tk.StringVar()
    test_paper_combobox = ttk.Combobox(dialog, textvariable=test_paper)
    test_paper_combobox['values'] = ("AL", "1A", "1ARS")
    test_paper_combobox.current(0)
    test_paper_combobox.pack(pady=10, padx=10)

    hLeft = tk.IntVar(value = 31)  #left handle variable initialised to value 0.2
    hRight = tk.IntVar(value = 40)  #right handle variable initialised to value 0.85
    hSlider = RangeSliderH( dialog , [hLeft, hRight], digit_precision='.0f',padX = 25, min_val=1, max_val=84, step_marker = True, step_size = 1)   #horizontal slider
    hSlider.pack()   # or grid or place method could be used


    
    def on_ok():
        global gamer_id
        global CONST_CURRENT_TEST_DATA_SET
        global q_start_idx, q_end_idx
        selected_name = name_var.get()
        if selected_name:
            gamer_id = selected_name
            CONST_CURRENT_TEST_DATA_SET = test_paper.get()
            q_start_idx = hLeft.get()
            q_end_idx = hRight.get()

            print(gamer_id, CONST_CURRENT_TEST_DATA_SET)
            print(q_start_idx, q_end_idx)

            dialog.destroy()
            root.deiconify()  # 顯示主視窗
        else:
            tk.messagebox.showwarning("Warning", "請選擇一個名字")

    ok_button = tk.Button(dialog, text="確定", command=on_ok)
    ok_button.pack(pady=10)

    dialog.transient(root)  # 將對話框設置為模式對話框
    dialog.grab_set()  # 獲取焦點
    root.wait_window(dialog)



def log_data(message, level="info"):
    global logger
    if level == "debug":
        logger.debug(message)
    elif level == "info":
        logger.info(message)
    elif level == "warning":
        logger.warning(message)
    elif level == "error":
        logger.error(message)
    elif level == "critical":
        logger.critical(message)
    else:
        logger.info(message)

def ddd_x(obj, x):
    obj.destroy()

def custom_messagebox(title, message, font, icon=None):
    global root
    root.update_idletasks()
    custom_box = tk.Toplevel()
    custom_box.bind("<Return>", lambda x: ddd_x(custom_box,x))
    x = root.winfo_x() + (root.winfo_width() // 2) - (custom_box.winfo_reqwidth() // 2)
    y = root.winfo_y() + (root.winfo_height() // 2) - (custom_box.winfo_reqheight() // 2)
    custom_box.geometry(f"+{x}+{y}")
    
    custom_box.title(title)

    if icon is not None:
        jpg_file = f'{icon}'
        image = Image.open(jpg_file)
        img = ImageTk.PhotoImage(image)
        icon_label = tk.Label(custom_box, image=img)
        icon_label.pack(padx=20, pady=20)

    
    message_label = tk.Label(custom_box, text=message, font=font)
    message_label.pack(padx=20, pady=20)
    
    ok_button = tk.Button(custom_box, text="確定", font=font, command=custom_box.destroy)
    ok_button.pack(pady=10)
    
    custom_box.transient(root)  # 將對話框設置為模式對話框
    custom_box.grab_set()  # 獲取焦點

    # 設置焦點在對話框的確定上
    ok_button.focus_set()

    
    root.wait_window(custom_box)  # 等待對話框關閉





correct = 0 
wrong = 0 
n_current_idx = 0
label_current_progress = 0 

dt_start_time = datetime.datetime.now()

CONST_FONT_TUPLE = ("Helvetica", 16)

word_list = []


engine = pyttsx3.init()

# UI part
entry = None
label_current_progress = None

# 列出可用的聲音
voices = engine.getProperty('voices')
for index, voice in enumerate(voices):
    log_data(f"{index}: {voice.name}")

engine.setProperty('rate', 150)    # Speed percent (can go over 100)


def speak_word(word):
    # 從1,2 隨便選一個
    id_random_012 = random.randint(1, 2)
    speak_word_by_ids(word, id_random_012)


def speak_word_by_ids(word, id_input):
    log_data(f"Speak word: {word} with voice id: {id_input}")
    engine.setProperty('voice', voices[id_input].id)
    # 語音合成
    engine.say(word)
    engine.runAndWait()


# Function to replay the word
def replay_word_1():
    global n_current_idx
    speak_word_by_ids(word_list[n_current_idx], 1)

def replay_word_2():
    global n_current_idx
    speak_word_by_ids(word_list[n_current_idx], 2)


# Function to check the word
def check_word():
    global correct, wrong
    global n_current_idx
    global label_current_progress, root
    global word_list
    global total 
    custom_font_tuple = tkFont.Font(family="Helvetica", size=16, weight="bold")

    user_input = entry.get()
    if user_input == word_list[n_current_idx]:
        correct += 1
        # Play the "yes.wav" sound
        winsound.PlaySound("yes.wav", winsound.SND_FILENAME)
        custom_messagebox("Result", "Correct!", font=custom_font_tuple, icon="r.jpg")
        log_data("O: "+word_list[n_current_idx])

    else:
        wrong += 1
        log_data("X: "+word_list[n_current_idx] + " Your answer: " + user_input)
        winsound.PlaySound("no.wav", winsound.SND_FILENAME)
        custom_messagebox("Result", "Wrong! Correct answer is: " + word_list[n_current_idx], font=custom_font_tuple, icon="w.jpg" )

    if n_current_idx == n_total - 1:
        dt_end_time = datetime.datetime.now()
        dt_total_time = dt_end_time - dt_start_time
        log_data(f"Total time: {dt_total_time}")
        label_current_progress.config(text=f"{n_current_idx+1}/{n_total}" +f" Correct: {correct}, Wrong: {wrong}\n Total time: {dt_total_time}")
        custom_messagebox("Total Result", f"Correct: {correct}, Wrong: {wrong} \n Total time: {dt_total_time}",  font=custom_font_tuple)
        log_data(f"Correct: {correct}, Wrong: {wrong}")
    else:
        entry.delete(0, tk.END)
        root.update_idletasks()
        # Speak the next word
        n_current_idx += 1
        label_current_progress.config(text=f"{n_current_idx+1}/{n_total}" +f" Correct: {correct}, Wrong: {wrong}")
        root.update_idletasks()
        speak_word(word_list[n_current_idx])


def restart_test():
    global correct, wrong, n_current_idx, word_list, root
    global dt_start_time
    dt_end_time = datetime.datetime.now()
    dt_total_time = dt_end_time - dt_start_time
    log_data(f"Total time: {dt_total_time}")

    correct = 0 
    wrong = 0 
    n_current_idx = 0
    dt_start_time = datetime.datetime.now()
    random.shuffle(word_list)

    label_current_progress.config(text=f"{n_current_idx+1}/{n_total}" +f" Correct: {correct}, Wrong: {wrong}")
    root.update_idletasks()
    speak_word(word_list[n_current_idx])


def load_data_set():

    global CONST_CURRENT_TEST_DATA_SET
    global q_start_idx, q_end_idx
    _word_list = []
    if CONST_CURRENT_TEST_DATA_SET == "1A":
        idx_useful =(q_start_idx, q_end_idx)
        # idx_reading = (0, -1)
        with open('1A.json', 'r') as f:
            dic_words = json.load(f)
        for i in range(idx_useful[0], idx_useful[1]+1):
            _word_list.append(dic_words[str(i)])
    elif CONST_CURRENT_TEST_DATA_SET == "1ARS":
        idxs =(q_start_idx, q_end_idx)
        with open('1ARS.json', 'r') as f:
            dic_words = json.load(f)
        for i in range(idxs[0], idxs[1]+1):
            _word_list.append(dic_words[str(i)])
    else:
        #AL
        ids_t = (q_start_idx, q_end_idx)
        with open('AL.json', 'r') as f:
            dic_words = json.load(f)
        for i in range(ids_t[0], ids_t[1]+1):
            _word_list.append(dic_words[str(i)])
    log_data(f'This time word list:{_word_list}')
    return _word_list


def main():
    global word_list
    global root, entry, label_current_progress
    global n_total
    global custom_font
    global logger

    # Create the main window
    root = tk.Tk()

    show_input_dialog()
    word_list = load_data_set()
    random.shuffle(word_list)

    logger = reset_logger()

    root.title("Word Test")

    
    root.geometry("400x600")  # Set the window size


    str_paper_title = f"考生: {gamer_id}, {CONST_CURRENT_TEST_DATA_SET} 測驗, 題目: {q_start_idx}~{q_end_idx}"
    label_title = tk.Label(root, text=str_paper_title, font=CONST_FONT_TUPLE)
    label_title.pack(pady=10)

    # Create and place widgets
    entry = tk.Entry(root, font=CONST_FONT_TUPLE)
    entry.bind("<Return>", lambda x: check_word())
    entry.pack(pady=20)

    n_total = len(word_list)

    # show 出目前進度

    label_current_progress = tk.Label(root, text=f"{n_current_idx+1}/{n_total}" +f" Correct: {correct}, Wrong: {wrong}", font=CONST_FONT_TUPLE)
    label_current_progress.pack(pady=10)

    submit_button = tk.Button(root, text="送出", command=check_word, font=CONST_FONT_TUPLE)
    submit_button.pack(pady=10)

    replay_button = tk.Button(root, text="重新撥放1", command=replay_word_1, font=CONST_FONT_TUPLE)
    replay_button.pack(pady=10)

    replay_button = tk.Button(root, text="重新撥放2", command=replay_word_2, font=CONST_FONT_TUPLE)
    replay_button.pack(pady=10)

    restart_test_button = tk.Button(root, text="重新測試", command=restart_test, font=CONST_FONT_TUPLE)
    restart_test_button.pack(pady=10)







    # Play the first word
    speak_word(word_list[0])
    entry.focus_set()
    # Start the GUI event loop
    root.mainloop()




if __name__ == '__main__':
    main()
    pass 