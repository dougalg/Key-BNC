#import the 'tkinter' module
import tkinter as tk
from tkinter import filedialog
from LL_OR_BNC.LLORBNCer import LLORBNCer
import csv, platform

calculator = LLORBNCer()

#create a new window
window = tk.Tk()
window.title("LL/OR vs. BNC Calculator")
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
    word_text.tag_add(tk.SEL, "1.0", tk.END)
    word_text.mark_set(tk.INSERT, "1.0")
    word_text.see(tk.INSERT)

    f_text.tag_add(tk.SEL, "1.0", tk.END)
    f_text.mark_set(tk.INSERT, "1.0")
    f_text.see(tk.INSERT)

    fbnc_text.tag_add(tk.SEL, "1.0", tk.END)
    fbnc_text.mark_set(tk.INSERT, "1.0")
    fbnc_text.see(tk.INSERT)

    ll_text.tag_add(tk.SEL, "1.0", tk.END)
    ll_text.mark_set(tk.INSERT, "1.0")
    ll_text.see(tk.INSERT)

    or_text.tag_add(tk.SEL, "1.0", tk.END)
    or_text.mark_set(tk.INSERT, "1.0")
    or_text.see(tk.INSERT)
    return 'break'

def clear_all():
    calculator.clear()
    update_labels()
    clear_results()
    file_names.delete(1.0, tk.END)

def clear_results():
    word_text.delete(1.0, tk.END)
    f_text.delete(1.0, tk.END)
    fbnc_text.delete(1.0, tk.END)
    ll_text.delete(1.0, tk.END)
    or_text.delete(1.0, tk.END)

def load_corpus_file():
    the_file = filedialog.askopenfilename()
    if not (the_file == ''):
        bad_files = calculator.load_target_file(the_file, add_name)
        update_labels()
        calculate()
        if len(bad_files['ignored']) > 0 or len(bad_files['guessed']) > 0:
            encoding_warning(bad_files)

def load_corpus():
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

    word_text.insert(tk.END, "Word")
    f_text.insert(tk.END, "F")
    fbnc_text.insert(tk.END, "F(BNC)")
    ll_text.insert(tk.END, "LL")
    or_text.insert(tk.END, "OR")

    for d in data:
        word_text.insert(tk.END, "\n{}".format(d[0]))
        f_text.insert(tk.END, "\n{:,.0f}".format(d[1]))
        fbnc_text.insert(tk.END, "\n{:,.0f}".format(d[2]))
        ll_text.insert(tk.END, "\n{:,.3f}".format(d[3]))
        try:
            or_text.insert(tk.END, "\n{:,.3f}".format(d[4]))
        except ValueError:
            or_text.insert(tk.END, "\n{}".format(d[4]))

    f_text.tag_configure("right", justify='right')
    f_text.tag_add("right", 2.0, "end")

    fbnc_text.tag_configure("right", justify='right')
    fbnc_text.tag_add("right", 2.0, "end")

    ll_text.tag_configure("right", justify='right')
    ll_text.tag_add("right", 2.0, "end")

    or_text.tag_configure("right", justify='right')
    or_text.tag_add("right", 2.0, "end")

def save():
    file_name = filedialog.asksaveasfilename(initialfile='BNC_LL.csv')
    data = calculator.get_stats()

    with open(file_name, mode='w', encoding='utf8', newline='') as file_handle:
        writer = csv.writer(file_handle)
        writer.writerow(['Word', 'F', 'F(BNC)', 'LL', 'OL'])
        for d in data:
            writer.writerow(d)

def show_help():
    pass

def scrollResults(*args):
    word_text.yview(*args)
    f_text.yview(*args)
    fbnc_text.yview(*args)
    ll_text.yview(*args)
    or_text.yview(*args)
    return "break"

def onMouseWheel(event):
    system = platform.system()
    if system == 'Windows':
        scroll_dist = int((event.delta/120)*(-1))
    elif system == 'Darwin':
        scroll_dist = -1*event.delta
    else:
        scroll_dist  = event.delta

    word_text.yview("scroll", scroll_dist, "units")
    f_text.yview("scroll", scroll_dist, "units")
    fbnc_text.yview("scroll", scroll_dist, "units")
    ll_text.yview("scroll", scroll_dist, "units")
    or_text.yview("scroll", scroll_dist, "units")
    return "break"

# Type/Token information
button_frame = tk.Frame(window, relief=tk.RAISED, borderwidth=1)
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
right_frame = tk.Frame(window, relief=tk.RAISED)
scrollbar = tk.Scrollbar(window)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
scrollbar.config(command=scrollResults)

word_text = tk.Text(right_frame, relief=tk.RAISED, width=26, yscrollcommand=scrollbar.set)
word_text.pack(side=tk.LEFT, fill=tk.Y)
word_text.bind("<Control-Key-a>", select_all)
word_text.bind("<MouseWheel>", onMouseWheel)

f_text = tk.Text(right_frame, relief=tk.RAISED, width=11, yscrollcommand=scrollbar.set)
f_text.pack(side=tk.LEFT, fill=tk.Y)
f_text.bind("<Control-Key-a>", select_all)
f_text.bind("<MouseWheel>", onMouseWheel)

fbnc_text = tk.Text(right_frame, relief=tk.RAISED, width=11, yscrollcommand=scrollbar.set)
fbnc_text.pack(side=tk.LEFT, fill=tk.Y)
fbnc_text.bind("<Control-Key-a>", select_all)
fbnc_text.bind("<MouseWheel>", onMouseWheel)

ll_text = tk.Text(right_frame, relief=tk.RAISED, width=11, yscrollcommand=scrollbar.set)
ll_text.pack(side=tk.LEFT, fill=tk.Y)
ll_text.bind("<Control-Key-a>", select_all)
ll_text.bind("<MouseWheel>", onMouseWheel)

or_text = tk.Text(right_frame, relief=tk.RAISED, width=11, yscrollcommand=scrollbar.set)
or_text.pack(side=tk.LEFT, fill=tk.Y)
or_text.bind("<Control-Key-a>", select_all)
or_text.bind("<MouseWheel>", onMouseWheel)

right_frame.pack(side=tk.RIGHT, fill=tk.Y)

# Filename List
file_names = tk.Text(window, width=30)
file_names.pack(fill=tk.Y, side=tk.LEFT)

# Menu Bar
menubar = tk.Menu(window)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Load directory", command=load_corpus)
filemenu.add_command(label="Load file", command=load_corpus_file)
filemenu.add_command(label="Save CSV", command=save)
filemenu.add_command(label="Clear files and results", command=clear_all)
filemenu.add_command(label="Help", command=show_help)
filemenu.add_command(label="Quit", command=window.quit)
menubar.add_cascade(label="File", menu=filemenu)
# display the menu
window.config(menu=menubar)

#draw the window, and start the application
window.mainloop()
