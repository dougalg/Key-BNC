import tkinter as tk
from tkinter import filedialog, Frame
from KEY_BNC.KEY_BNC import KEY_BNC
from KEY_BNC import windows
import csv, platform

#create a new window
class UI(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        self.pack(fill=tk.BOTH, expand=1)

        self.calculator = KEY_BNC()
        self.data = []
        self.init_options()
        self.init_menus()
        self.init_frames()

    def init_options(self):
        self.opt_ignore_numbers = tk.IntVar()
        self.opt_min_f = tk.IntVar()
        self.opt_min_f_bnc = tk.IntVar()

    def add_menu_option(self, parent, menu):
        parent.add_command(label=menu['label'], command=menu['command'])

        for k in menu['bind_keys']:
            self.bind_key(self.master, k, menu['command'])

    def bind_key(self, master, k, command):
        """
        Custom key binding method to support cross-platform
        key bindings for command/ctrl keys
        """
        system = platform.system()
        if system == 'Windows':
            master.bind("<Control-Key-{}>".format(k), command)
        elif system == 'Darwin':
            master.bind("<Command-{}>".format(k), command)
        else:
            master.bind("<Control-Key-{}>".format(k), command)

    def init_menus(self):
        # Menu Bar
        menubar = tk.Menu(self.master)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenus = [{'label': "Load directory (d)",
                      'command': self.load_corpus,
                      'bind_keys': ["d"]},
                     {'label': "Load file (f)",
                      'command': self.load_corpus_file,
                      'bind_keys': ["f"]},
                     {'label': "Save Results (s)",
                      'command': self.save,
                      'bind_keys': ["s"]},
                     {'label': "Clear files and results",
                     'command': self.clear_all,
                     'bind_keys': []},
                     {'label': "Quit (q)",
                     'command': self.quit,
                     'bind_keys': ['q']}
                    ]

        for m in filemenus:
            self.add_menu_option(filemenu, m)

        menubar.add_cascade(label="File", menu=filemenu)

        helpmenu = tk.Menu(menubar, tearoff=0)

        helpmenus = [{'label': "About & References",
                     'command': self.show_about,
                     'bind_keys': []},
                     {'label': "Help (/)",
                     'command': self.show_help,
                     'bind_keys': ['/']}]

        for m in helpmenus:
            self.add_menu_option(helpmenu, m)

        menubar.add_cascade(label="Help", menu=helpmenu)

        # display the menu
        self.master.config(menu=menubar)

    def init_frames(self):
        # Type/Token information
        self.init_top_frame()

        # Results section
        self.init_bottom_frame()

    def init_top_frame(self):
        top_frame = tk.Frame(self, borderwidth=1)

        # BNC
        tk.Label(top_frame, text="BNC Types:").grid(row=0, column=0, sticky=tk.W)
        self.bnc_types = tk.Label(top_frame, text='{:,.0f}'.format(len(self.calculator.bnc_words)))
        self.bnc_types.grid(row=0, column=1, sticky=tk.E)
        tk.Label(top_frame, text="BNC Tokens:").grid(row=1, column=0, sticky=tk.W)
        self.bnc_tokens = tk.Label(top_frame, text='{:,.0f}'.format(self.calculator.bnc_corpus_size))
        self.bnc_tokens.grid(row=1, column=1, sticky=tk.E)

        # User corpus
        tk.Label(top_frame, text="Your Types:").grid(row=0, column=2, sticky=tk.W)
        self.user_types = tk.Label(top_frame, text='None')
        self.user_types.grid(row=0, column=3, sticky=tk.E)
        tk.Label(top_frame, text="Your Tokens:").grid(row=1, column=2, sticky=tk.W)
        self.user_tokens = tk.Label(top_frame, text='None')
        self.user_tokens.grid(row=1, column=3, sticky=tk.E)

        # Additional toggles/options
        # Allow hiding of #s
        self.ignore_num = tk.Checkbutton(top_frame, variable=self.opt_ignore_numbers, command=self.calculate)
        ignore_num_label = tk.Label(top_frame, text="Ignore Numbers:")
        ignore_num_label.bind('<Button-1>', lambda e: self.toggle_number_ignore())

        ignore_num_label.grid(row=0, column=4, sticky=tk.W)
        self.ignore_num.grid(row=0, column=5, sticky=tk.W)

        top_frame.pack(side=tk.TOP, fill=tk.X)

    def toggle_number_ignore(self):
        self.ignore_num.toggle()
        self.calculate()

    def init_bottom_frame(self):
        self.bottom_frame = bottom_frame = tk.Frame(self)
        tk.Grid.rowconfigure(bottom_frame,1,weight=1)
        tk.Grid.columnconfigure(bottom_frame,0,weight=1)
        tk.Grid.columnconfigure(bottom_frame,1,weight=1)

        # Filename List
        tk.Label(bottom_frame, text="File Names").grid(row=0, column=0, sticky=tk.W)
        self.file_names = tk.Text(bottom_frame, relief=tk.RAISED, width=20, state=tk.DISABLED)
        self.file_names.grid(row=1, column=0, sticky=tk.N+tk.E+tk.W+tk.S)

        self.scrollbar = tk.Scrollbar(bottom_frame)

        self.scrollbar.grid(row=1, column=6, sticky=tk.N+tk.S)
        self.scrollbar.config(command=self.scroll_results)

        self.columns = self.init_columns()

        bottom_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=tk.YES)

    def init_columns(self):
        columns = []
        widths = [15, 8, 10, 10, 16]
        for i, col_header in enumerate(self.calculator.get_cols()):
            index = i+1 # Offset for the "file names" column

            label = tk.Label(self.bottom_frame, text=col_header, fg="blue", cursor="hand2")
            label.grid(row=0, column=index, sticky=tk.W)
            label.bind('<Button-1>', lambda e,col=i:self.sort_results(col))

            if i == 0:
                sticky = tk.N+tk.E+tk.W+tk.S
            else:
                sticky=tk.N+tk.S

            column = tk.Text(self.bottom_frame, relief=tk.RAISED, width=widths[i], yscrollcommand=self.scrollbar.set, wrap=tk.NONE, state=tk.DISABLED)
            column.grid(row=1, column=index, sticky=sticky)
            self.bind_key(column, 'a', self.select_all)
            column.bind("<MouseWheel>", self.on_mouse_wheel)
            column.bind('<Home>', self.to_home)
            column.bind('<End>', self.to_end)
            column.bind('<Prior>', self.to_page_up)
            column.bind('<Next>', self.to_page_down)

            columns.append(column)
        return columns

    def select_all(self, event):
        for c in self.columns:
            c.tag_add(tk.SEL, "1.0", tk.END)
            c.mark_set(tk.INSERT, "1.0")
            c.see(tk.INSERT)
        return 'break'

    def clear_all(self):
        self.calculator.clear()
        self.update_labels()
        self.clear_results()
        self.clear_files()

    def clear_files(self):
        self.file_names.config(state=tk.NORMAL)
        self.file_names.delete(1.0, tk.END)
        self.file_names.config(state=tk.DISABLED)

    def clear_results(self):
        for c in self.columns:
            c.config(state=tk.NORMAL)
            c.delete(1.0, tk.END)
            c.config(state=tk.DISABLED)

    def load_corpus_file(self, event=None):
        the_file = filedialog.askopenfilename()
        if not (the_file == ''):
            bad_files = self.calculator.load_target_file(the_file, self.add_name)
            self.show_load_results(bad_files)

    def load_corpus(self, event=None):
        the_dir = filedialog.askdirectory()
        if not (the_dir == ''):
            bad_files = self.calculator.load_target_data_dir(the_dir, self.add_name)
            self.show_load_results(bad_files)

    def show_load_results(self, bad_files):
        self.update_labels()
        self.calculate()
        if len(bad_files['ignored']) > 0 or len(bad_files['guessed']) > 0:
            windows.encoding_warning(bad_files)

    def add_name(self, file_name):
        """
        Adds a filename to the file_frame
        """
        self.file_names.config(state=tk.NORMAL)
        self.file_names.insert(tk.END, "{}\n".format(file_name))
        self.file_names.config(state=tk.DISABLED)

    def update_labels(self):
        text1 = '{:,.0f}'.format(len(self.calculator.target_words))
        text2 = '{:,.0f}'.format(self.calculator.target_corpus_size)
        self.user_types['text'] = text1
        self.user_tokens['text'] = text2

        text1 = '{:,.0f}'.format(len(self.calculator.bnc_words))
        text2 = '{:,.0f}'.format(self.calculator.bnc_corpus_size)
        self.bnc_types['text'] = text1
        self.bnc_tokens['text'] = text2

    def calculate(self):
        self.calculator.ignore_numbers = self.opt_ignore_numbers.get()

        data = self.calculator.get_stats()

        self.update_labels()
        self.clear_results()

        # Make sure writing is enabled
        for c in self.columns:
            c.config(state=tk.NORMAL)

        formats = ["{}\n", "{:,.0f}\n", "{:,.0f}\n", "{:,.2f}\n", "{:,.2f}\n"]
        inf = float('inf')
        for d in data:
            for i, datum in enumerate(d):
                if i == 4 and datum == inf:
                    self.columns[i].insert(tk.END, "∞\n")
                else:
                    self.columns[i].insert(tk.END, formats[i].format(datum))

        # Format text and disable writing so users don't accidentally edit
        # results
        for c in self.columns[1:]:
            c.tag_configure("right", justify='right')
            c.tag_add("right", 1.0, "end")
            c.config(state=tk.DISABLED)

        self.columns[0].config(state=tk.DISABLED)

    def save(self, event=None):
        file_name = filedialog.asksaveasfilename(initialfile='BNC_LL_OR.csv')

        if file_name != None and file_name != '':
            data = self.calculator.get_stats()
            with open(file_name, mode='w', encoding='utf8', newline='') as file_handle:
                writer = csv.writer(file_handle)
                writer.writerow(calculator.get_cols())
                for d in data:
                    writer.writerow(d)

    def show_help(self, event=None):
        formats = {'h1': [('1.0', '1.end')],
                   'h2': [('2.0', '2.end'),
                          ('9.0', '9.end'),
                          ('12.0', '12.end'),
                          ('15.0', '15.end')]
                  }
        windows.show_splash("Key-BNC Help", "Help.txt", **formats)

    def show_about(self, event=None):
        formats = {'h1': [('1.0', '1.end')],
                   'h2': [('2.0', '2.end'),
                          ('5.0', '5.end'),
                          ('8.0', '8.end'),
                          ('11.0', '11.end'),
                          ('14.0', '14.end'),
                          ('18.0', '18.end')],
                   'bold': [('19.0', '19.end'),
                            ('23.0', '23.end'),
                            ('26.0', '26.end'),
                            ('29.0', '29.end')]
                  }
        windows.show_splash("About Key-BNC", "About.txt", **formats)

    def scroll_results(self, *args):
        """
        Scrolls all columns
        """
        for c in self.columns:
            c.yview(*args)
        return "break"

    def to_page_up(self, event):
        """
        Scrolls all columns up one page
        """
        for c in self.columns:
            c.yview_scroll(-1, tk.PAGES)
        return "break"

    def to_page_down(self, event):
        """
        Scrolls all columns down one page
        """
        for c in self.columns:
            c.yview_scroll(1, tk.PAGES)
        return "break"

    def to_end(self, event):
        """
        Scrolls all columns to bottom
        """
        for c in self.columns:
            c.see("end")
        return "break"

    def to_home(self, event):
        """
        Scrolls all columns to top
        """
        for c in self.columns:
            c.see("1.0")
        return "break"

    def on_mouse_wheel(self, event):
        """
        Scrolls all columns on mousewheel
        """
        system = platform.system()
        if system == 'Windows':
            scroll_dist = int((event.delta/120)*(-1))
        elif system == 'Darwin':
            scroll_dist = -1*event.delta
        else:
            scroll_dist  = event.delta

        for c in self.columns:
            c.yview("scroll", scroll_dist, "units")
        return "break"

    def sort_results(self, the_col):
        """
        Sets the current sort option and refreshes the view
        """
        self.calculator.set_sort(the_col)
        self.calculate()

    def quit(self, e=None):
        self.master.quit()

def run():
    splash_formats = {'h1': [('1.0', '1.end')],
                      'h2': [('2.0', '2.end'),
                             ('5.0', '5.end'),
                             ('8.0', '8.end')],
                      'bold': [('6.404', '6.463'),
                               ('9.354', '9.407')]
                      }
    windows.show_splash("Introduction", "About Short.txt", **splash_formats)

    #draw the window, and start the application
    root = tk.Tk()
    root.title("LL/OR vs. BNC Keyword Calculator")
    root.geometry("700x500")

    ui = UI(root)
    ui.mainloop()

