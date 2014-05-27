import tkinter as tk
from tkinter import filedialog
from operator import itemgetter
from KEY_BNC.KEY_BNC import KEY_BNC
import csv, platform

calculator = KEY_BNC()

#create a new window
window = tk.Tk()
window.title("LL/OR vs. BNC Keyword Calculator")
window.geometry("700x500")

def encoding_warning(file_names):
    num_skipped = len(file_names['ignored'])
    num_opened = len(file_names['guessed'])

    text = 'Warning:'
    if num_opened > 0:
        text += "\n{} files were opened but may contain errors as they are not encoded as UTF8.".format(num_opened)
    if num_skipped > 0:
        text += "\n{} files were skipped. Please make sure that they are TXT files.".format(num_skipped)
    if num_opened >0 :
        text += "\n\nOpened files:\n{}".format("\n".join(file_names['guessed']))
    if num_skipped >0 :
        text += "\n\nSkipped files:\n{}".format("\n".join(file_names['ignored']))

    root = tk.Tk()
    root.title("Warning")
    root.geometry("500x300")

    tk.Button(root, text="Close", activebackground="white", bg="white", command=lambda: root.destroy()).pack(side=tk.BOTTOM)

    textbox = tk.Text(root, width=40)

    tscrollbar = tk.Scrollbar(root)
    tscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    textbox.config(yscrollcommand=tscrollbar.set)
    tscrollbar.config(command=textbox.yview)

    textbox.pack(fill=tk.BOTH)
    textbox.insert(tk.END, text)

    root.update_idletasks()
    root.wm_attributes("-topmost", 1)

    ## Run appliction
    root.mainloop()

def select_all(event):
    for c in columns:
        c.tag_add(tk.SEL, "1.0", tk.END)
        c.mark_set(tk.INSERT, "1.0")
        c.see(tk.INSERT)
    return 'break'

def clear_all():
    calculator.clear()
    update_labels()
    clear_results()
    file_names.delete(1.0, tk.END)

def clear_results():
    for c in columns:
        c.delete(1.0, tk.END)

def load_corpus_file(event=None):
    the_file = filedialog.askopenfilename()
    if not (the_file == ''):
        bad_files = calculator.load_target_file(the_file, add_name)
        update_labels()
        calculate()
        if len(bad_files['ignored']) > 0 or len(bad_files['guessed']) > 0:
            encoding_warning(bad_files)

def load_corpus(event=None):
    the_dir = filedialog.askdirectory()
    if not (the_dir == ''):
        bad_files = calculator.load_target_data_dir(the_dir, add_name)
        update_labels()
        calculate()
        if len(bad_files['ignored']) > 0 or len(bad_files['guessed']) > 0:
            encoding_warning(bad_files)

def add_name(file_name):
    """
    Adds a filename to the file_frame
    """
    file_names.insert(tk.END, "{}\n".format(file_name))

def update_labels():
    text1 = '{:,.0f}'.format(len(calculator.target_words))
    text2 = '{:,.0f}'.format(calculator.target_corpus_size)
    user_types['text'] = text1
    user_tokens['text'] = text2

def calculate():
    data = calculator.get_stats()

    clear_results()

    formats = ["{}\n", "{:,.0f}\n", "{:,.0f}\n", "{:,.2f}\n", "{:,.2f}\n"]
    inf = float('inf')
    for d in data:
        for i, datum in enumerate(d):
            if i == 4 and datum == inf:
                columns[i].insert(tk.END, "∞\n")
            else:
                columns[i].insert(tk.END, formats[i].format(datum))

    for c in columns[1:]:
        c.tag_configure("right", justify='right')
        c.tag_add("right", 1.0, "end")

def save(event=None):
    file_name = filedialog.asksaveasfilename(initialfile='BNC_LL.csv')

    if file_name != None and file_name != '':
        data = calculator.get_stats()
        with open(file_name, mode='w', encoding='utf8', newline='') as file_handle:
            writer = csv.writer(file_handle)
            writer.writerow(calculator.get_cols())
            for d in data:
                writer.writerow(d)

def show_help(event=None):
    pass

def scrollResults(*args):
    for c in columns:
        c.yview(*args)

    return "break"

def onMouseWheel(event):
    system = platform.system()
    if system == 'Windows':
        scroll_dist = int((event.delta/120)*(-1))
    elif system == 'Darwin':
        scroll_dist = -1*event.delta
    else:
        scroll_dist  = event.delta

    for c in columns:
        c.yview("scroll", scroll_dist, "units")

    return "break"

def sort_results(the_col):
    calculator.set_sort(the_col)
    calculate()

# Type/Token information
button_frame = tk.Frame(window, borderwidth=1)
# BNC
tk.Label(button_frame, text="BNC Types:").grid(row=0, column=0, sticky=tk.W)
tk.Label(button_frame, text='{:,.0f}'.format(len(calculator.bnc_words))).grid(row=0, column=1, sticky=tk.E)
tk.Label(button_frame, text="BNC Tokens:").grid(row=1, column=0, sticky=tk.W)
tk.Label(button_frame, text='{:,.0f}'.format(calculator.bnc_corpus_size)).grid(row=1, column=1, sticky=tk.E)
# User corpus
tk.Label(button_frame, text="Your Types:").grid(row=0, column=2, sticky=tk.W)
user_types = tk.Label(button_frame, text='None')
user_types.grid(row=0, column=3, sticky=tk.E)
tk.Label(button_frame, text="Your Tokens:").grid(row=1, column=2, sticky=tk.W)
user_tokens = tk.Label(button_frame, text='None')
user_tokens.grid(row=1, column=3, sticky=tk.E)

button_frame.pack(side=tk.TOP, fill=tk.X)

# Results section
right_frame = tk.Frame(window)
tk.Grid.rowconfigure(right_frame,1,weight=1)
tk.Grid.columnconfigure(right_frame,0,weight=1)
tk.Grid.columnconfigure(right_frame,1,weight=1)

# Filename List
tk.Label(right_frame, text="File Names").grid(row=0, column=0, sticky=tk.W)
file_names = tk.Text(right_frame, relief=tk.RAISED, width=20)
file_names.grid(row=1, column=0, sticky=tk.N+tk.E+tk.W+tk.S)

scrollbar = tk.Scrollbar(right_frame)

columns = []
widths = [15, 11, 11, 11, 11]
for i, col_header in enumerate(calculator.get_cols()):
    index = i+1 # Offset for the "file names" column

    label = tk.Label(right_frame, text=col_header)
    label.grid(row=0, column=index, sticky=tk.W)
    label.bind('<Button-1>', lambda e,col=i:sort_results(col))

    if i == 0:
        sticky = tk.N+tk.E+tk.W+tk.S
    else:
        sticky=tk.N+tk.S

    column = tk.Text(right_frame, relief=tk.RAISED, width=widths[i], yscrollcommand=scrollbar.set)
    column.grid(row=1, column=index, sticky=sticky)
    column.bind("<Control-Key-a>", select_all)
    column.bind("<MouseWheel>", onMouseWheel)

    columns.append(column)

scrollbar.grid(row=1, column=6, sticky=tk.N+tk.S)
scrollbar.config(command=scrollResults)

right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=tk.YES)

# Menu Bar
menubar = tk.Menu(window)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Load directory (d)", command=load_corpus)
window.bind("<Control-Key-d>", load_corpus)
window.bind("<Command-d>", load_corpus)

filemenu.add_command(label="Load file (f)", command=load_corpus_file)
window.bind("<Control-Key-f>", load_corpus_file)
window.bind("<Command-f>", load_corpus_file)

filemenu.add_command(label="Save CSV (s)", command=save)
window.bind("<Control-Key-s>", save)
window.bind("<Command-s>", save)

filemenu.add_command(label="Clear files and results", command=clear_all)

filemenu.add_command(label="Help (?)", command=show_help)
window.bind("<Control-Key-?>", show_help)
window.bind("<Command-?>", show_help)

filemenu.add_command(label="Quit (q)", command=window.quit)
window.bind("<Control-Key-q>", window.quit)
window.bind("<Command-q>", window.quit)

menubar.add_cascade(label="File", menu=filemenu)
# display the menu
window.config(menu=menubar)

#draw the window, and start the application
window.mainloop()
