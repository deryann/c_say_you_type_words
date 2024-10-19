import json 
import random
import tkinter as tk
from tkinter import messagebox
import pyttsx3
import logging
from tkinter import font as tkFont
import winsound

from PIL import Image, ImageTk


# Configure logger
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("testing.log"),
                        logging.StreamHandler()
                    ])

logger = logging.getLogger()

def log_data(message, level="info"):
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


def custom_messagebox(title, message, font, icon=None):
    global root
    root.update_idletasks()
    custom_box = tk.Toplevel()
    
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
    root.wait_window(custom_box)  # 等待對話框關閉





correct = 0 
wrong = 0 
n_current_idx = 0
label_current_progress = 0 

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
        
        label_current_progress.config(text=f"{n_current_idx+1}/{n_total}" +f" Correct: {correct}, Wrong: {wrong}")
        custom_messagebox("Total Result", f"Correct: {correct}, Wrong: {wrong}",  font=custom_font_tuple)
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
    correct = 0 
    wrong = 0 
    n_current_idx = 0
    random.shuffle(word_list)
    label_current_progress.config(text=f"{n_current_idx+1}/{n_total}" +f" Correct: {correct}, Wrong: {wrong}")
    root.update_idletasks()
    speak_word(word_list[n_current_idx])


def load_data_set():
    b_1A = True
    #1A
    _word_list = []
    if b_1A:
        idx_useful =(11, 31)
        idx_reading = (0, -1)
        with open('1A_useful_words.json', 'r') as f:
            dic_words = json.load(f)
        for i in range(idx_useful[0], idx_useful[1]+1):
            _word_list.append(dic_words[str(i)])
        with open('1A_reading_science.json', 'r') as f:
            dic_words = json.load(f)
        for i in range(idx_reading[0], idx_reading[1]+1):
            _word_list.append(dic_words[str(i)])
    else:
        #5A 
        # word_list = ['reject', 'continue', 'remind', 'congratulations', 'interrupt', 'terrific', 'unique', 'satisfy', 'ordinary', 'consider']

        with open('5_spelling_bee.json', 'r') as f:
            dic_words = json.load(f)
        for i in range(21, 31):
            _word_list.append(dic_words[str(i)])
    log_data(f'This time word list:{word_list}')
    return _word_list


def main():
    global word_list
    global root, entry, label_current_progress
    global n_total
    global custom_font
    word_list = load_data_set()

    random.shuffle(word_list)

    

    # Create the main window
    root = tk.Tk()
    root.title("Word Test")
    # 自定義字型
    
    root.geometry("400x600")  # Set the window size

    # Create and place widgets
    entry = tk.Entry(root, font=("Helvetica", 16))
    entry.pack(pady=20)

    n_total = len(word_list)

    # show 出目前進度

    label_current_progress = tk.Label(root, text=f"{n_current_idx+1}/{n_total}" +f" Correct: {correct}, Wrong: {wrong}", font=("Helvetica", 16))
    label_current_progress.pack(pady=10)

    submit_button = tk.Button(root, text="送出", command=check_word, font=("Helvetica", 16))
    submit_button.pack(pady=10)

    replay_button = tk.Button(root, text="重新撥放1", command=replay_word_1, font=("Helvetica", 16))
    replay_button.pack(pady=10)

    replay_button = tk.Button(root, text="重新撥放2", command=replay_word_2, font=("Helvetica", 16))
    replay_button.pack(pady=10)

    restart_test_button = tk.Button(root, text="重新測試", command=restart_test, font=("Helvetica", 16))
    restart_test_button.pack(pady=10)



    # Play the first word
    speak_word(word_list[0])

    # Start the GUI event loop
    root.mainloop()




if __name__ == '__main__':
    main()
    pass 