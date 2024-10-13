import random
import tkinter as tk
from tkinter import messagebox
import pyttsx3


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
    print(f"{index}: {voice.name}")

engine.setProperty('rate', 150)    # Speed percent (can go over 100)


def speak_word(word):
    # 從1,2 隨便選一個
    id_random_012 = random.randint(1, 2)
    engine.setProperty('voice', voices[id_random_012].id)
    # 語音合成
    engine.say(word)
    engine.runAndWait()

def speak_word_by_ids(word, id_input):
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

    user_input = entry.get()
    if user_input == word_list[n_current_idx]:
        correct += 1
        messagebox.showinfo("Result", "Correct!")
        print("O: "+word_list[n_current_idx])
    else:
        wrong += 1
        print("X: "+word_list[n_current_idx] + " Your answer: " + user_input)
        messagebox.showinfo("Result", "Wrong! Correct answer is: " + word_list[n_current_idx])

    if n_current_idx == n_total - 1:
        
        label_current_progress.config(text=f"{n_current_idx+1}/{n_total}" +f" Correct: {correct}, Wrong: {wrong}")
        messagebox.showinfo("Total Result", f"Correct: {correct}, Wrong: {wrong}")
        print(f"Correct: {correct}, Wrong: {wrong}")
    else:
        # Speak the next word
        n_current_idx += 1
        label_current_progress.config(text=f"{n_current_idx+1}/{n_total}" +f" Correct: {correct}, Wrong: {wrong}")
        root.update_idletasks()
        speak_word(word_list[n_current_idx])
    
def main():
    global word_list
    global root, entry, label_current_progress
    global n_total


    #1A
    word_list = [ 'carry', 'show', 'before', 'think', 'plant' , 'roots', 'stem', 'hold' ]
    word_extra = [ 'arm', 'airplane', 'April', 'bakery', 'bottom', 'camera', 'classmate', 'classroom', 'dark', 'daughter', 'December', 'dish', 'easy', 'exam', 'false', 'farmer', 'February', 'floor', 'follow', 'friend' ]

    word_list.extend(word_extra)

    #5A 
    word_list = ['reject', 'continue', 'remind', 'congratulations', 'interrupt', 'terrific', 'unique', 'satisfy', 'ordinary', 'consider']

    random.shuffle(word_list)


    # Create the main window
    root = tk.Tk()
    root.title("Word Test")
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


    # Play the first word
    speak_word(word_list[0])

    # Start the GUI event loop
    root.mainloop()




if __name__ == '__main__':
    main()
    pass 