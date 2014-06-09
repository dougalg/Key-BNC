import os
import tkinter as tk
from tkinter import font
from KEY_BNC.KEY_BNC import data_dirs

def show_splash(title, source_name, **formats):
    data_path = os.path.join(data_dirs[0], data_dirs[1], source_name)
    my_text = ''
    with open(data_path, encoding="utf8") as f:
        my_text = f.read()

    root = tk.Tk()
    root.title(title)
    root.geometry("500x300")
    textbox = tk.Text(root, width=40, wrap=tk.WORD, font=("Times New Roman", 12))

    tscrollbar = tk.Scrollbar(root)
    tscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tscrollbar.config(command=textbox.yview)

    textbox.pack(fill=tk.BOTH, expand=tk.YES)
    textbox.delete(1.0, tk.END)
    textbox.insert("1.0", my_text)

    # Formatting
    for format_name in formats:
        for start, end in formats[format_name]:
            textbox.tag_add(format_name, start, end)

    textbox.tag_config('h1', font=("Times New Roman", 14, font.BOLD), justify=tk.CENTER)
    textbox.tag_config('h2', font=("Times New Roman", 13, font.BOLD))
    textbox.tag_config('bold', font=("Times New Roman", 12, font.BOLD))

    textbox.config(yscrollcommand=tscrollbar.set, state=tk.DISABLED)

    root.update_idletasks()
    root.wm_attributes("-topmost", 1)

    ## Run appliction
    root.mainloop()

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
