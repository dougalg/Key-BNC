#import the 'tkinter' module
import tkinter as tk
from tkinter import filedialog
from LL_OR_BNC.LLORBNCer import LLORBNCer
import csv

calculator = LLORBNCer()

#create a new window
window = tk.Tk()
window.title("LL/OR vs. BNC Calculator")
window.geometry("700x500")

def select_all(event):
    results_text.tag_add(tk.SEL, "1.0", tk.END)
    results_text.mark_set(tk.INSERT, "1.0")
    results_text.see(tk.INSERT)
    return 'break'

def load_corpus():
    the_dir = filedialog.askdirectory()
    calculator.load_target_data_dir(the_dir, add_name)
    update_labels()
    calculate()

def add_name(file_name):
    """
    Adds a filename to the file_frame
    """
    textbox.insert(tk.END, "{}\n".format(file_name))

def update_labels():
    user_types['text'] = '{:,.0f}'.format(len(calculator.target_words))
    user_tokens['text'] = '{:,.0f}'.format(calculator.target_corpus_size)

def calculate():
    data = calculator.get_stats()

    results_text.delete(1.0, tk.END)
    results_text.insert(tk.END, "Word\tF\tF(BNC)\tLL\tOR\n")
    for d in data:
        results_text.insert(tk.END, "{}\t{}\t{}\t{}\t{}\n".format(*d))

def save():
    file_name = filedialog.asksaveasfilename(initialfile='BNC_LL.csv')
    data = calculator.get_stats()

    with open(file_name, mode='w', encoding='utf8', newline='') as file_handle:
        writer = csv.writer(file_handle)
        writer.writerow(['Word', 'F', 'F(BNC)', 'LL', 'OL'])
        for d in data:
            writer.writerow(d)

def show_help():
    results_text.delete(1.0, tk.END)
    results_text.insert(tk.END,
        """1) Click "load corpus" and choose a directory containing UTF8 encoded text files (.txt)
2) You will see a list of the files loaded. Loading new files replaces old ones, so put all files in one directory before loading
3) Save your results (2 ways)
    3a) You can copy/paste results by clicking in the middle window and typing "ctrl-a" followed by "ctrl-c" in MS Excel
    3b) Use the "save csv" button to save the results to a file which can be opened by MS Excel (You don't need to click "calculate" first)""")

# Set up the frames.
# There should be 3 columns
# 1) A list of loaded files
# 2) The results pane
# 3) The buttons
textbox = tk.Text(window, width=25)
textbox.pack(fill=tk.Y, side=tk.LEFT)

right_frame = tk.Frame(window, relief=tk.RAISED)
results_text = tk.Text(window, width=20)
results_text.bind("<Control-Key-a>", select_all)
button_frame = tk.Frame(right_frame, relief=tk.RAISED, width=150, borderwidth=1)

# Add a help button
help_button = tk.Button(button_frame, text="Help", command=show_help).pack()

# Set up the menu items
# A button to load a directory (It should be UTF8)
corpus_button = tk.Button(button_frame, text="Load Corpus", command=load_corpus).pack()

# A button to save as CSV
save_button = tk.Button(button_frame, text="Save CSV", command=save).pack()

# Type/Token information
# BNC
tk.Label(button_frame, text="BNC Types").pack()
tk.Label(button_frame, text='{:,.0f}'.format(len(calculator.bnc_words))).pack()
tk.Label(button_frame, text="BNC Tokens").pack()
tk.Label(button_frame, text='{:,.0f}'.format(calculator.bnc_corpus_size)).pack()
# User corpus
tk.Label(button_frame, text="Your Types").pack()
user_types = tk.Label(button_frame, text='None')
user_types.pack()
tk.Label(button_frame, text="Your Tokens").pack()
user_tokens = tk.Label(button_frame, text='None')
user_tokens.pack()

right_frame.pack(side=tk.RIGHT, fill=tk.Y)

scrollbar = tk.Scrollbar(window)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
results_text.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=results_text.yview)

results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
button_frame.pack(side=tk.RIGHT, fill=tk.Y)

#draw the window, and start the 'application'
window.mainloop()

