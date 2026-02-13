import tkinter as tk
import tkinter.messagebox
import tkinter.ttk as ttk
from time import time
from tkinter import filedialog

from configtoargs import Args, check_configfile_option_and_save, configtoargs


__default_args = {
    'mode': 'ontime',
    'time': 600,
    'seed': time(),
    'background': 'k',
    'screensize': '1000,1000',
    'client': 'mongodb://localhost:27017/',
    'database': 'RandomImage',
    'collection': ['ImagePath'],
    'targetpath': '目录.txt',
    'initialize': 0,
    'update': 0,
    'clear': 0,
    'hideimage': 0,
    'cache': 0,
    'debug': 0,
    'configfile': 1,
    'version': 'Random Image Viewer v2'
}
_default_args = Args(**__default_args)


class GUI(ttk.Frame):
    def __init__(self, args, master=None, ):
        self.args = args
        self.end_state = False

        ttk.Frame.__init__(self, master)

        self.Window = self.winfo_toplevel()
        self.window_init()

        self.panel_init()

        self.var_init()
        self.create_widgets()
        self.widgets_init()
        self.event_bind()

    def window_init(self):
        self.Window.title('随机图片浏览')
        self.Window.rowconfigure(0, weight=1)
        self.Window.columnconfigure(0, weight=1)
        # self.Window.resizable(width=False, height=False)

    def panel_init(self):
        self.rowconfigure(0, pad=100)
        self.columnconfigure(0, pad=10)
        self.grid(column=0, row=0, sticky=tk.N+tk.E+tk.W+tk.S)

    def var_init(self):
        self.var_client = tk.StringVar()
        self.var_database = tk.StringVar()
        self.collection_str = tk.StringVar()
        self.collection_list = []

        self.var_initialize = tk.IntVar()
        self.var_update = tk.IntVar()
        self.var_delete = tk.IntVar()

        self.var_mode = tk.StringVar()

        self.var_time = tk.IntVar()

        self.var_background = tk.StringVar()

        self.var_seed= tk.StringVar()

        self.var_hide_image = tk.IntVar()
        self.var_cache = tk.IntVar()
        self.var_config = tk.IntVar()

        self.var_version = tk.StringVar()

    def create_widgets(self):
        tmpstyle = ttk.Style()
        tmpstyle.configure('1.TFrame', background='red')

        self.widgets_top = []
        self.widgets_db = []

        # row0
        self.db_panel = ttk.Notebook(self, )

        self.db_func = ttk.Frame(self.db_panel)
        self.db_func.columnconfigure(0, weight=1)
        self.db_setting = ttk.Frame(self.db_panel)
        self.db_panel.add(self.db_setting, text='数据库设置')
        self.db_panel.add(self.db_func, text='数据库功能')

        self.client_label = ttk.Label(self.db_setting, text='地址：')
        self.client_label.grid(row=0, column=0, sticky=tk.W)
        self.client = ttk.Entry(self.db_setting, textvariable=self.var_client)
        self.client.grid(row=0, column=1, sticky=tk.E)
        self.database_label = ttk.Label(self.db_setting, text='数据库：')
        self.database_label.grid(row=1, column=0, sticky=tk.W)
        self.database = ttk.Entry(self.db_setting, textvariable=self.var_database)
        self.database.grid(row=1, column=1, sticky=tk.E)
        # self.collection_label = ttk.Label(self.db_setting, text='表名：')
        # self.collection_label.grid(row=2, column=0, sticky=tk.W)
        self.collection_button = ttk.Button(self.db_setting, text='数据表选择', command=self.open_collection_panel, name='collectionOpen')
        self.collection_button.grid(row=2, column=0, sticky=tk.W)
        self.collection_text = ttk.Label(self.db_setting, textvariable=self.collection_str)
        self.collection_text.grid(row=2, column=1, sticky=tk.E+tk.W)
        self.widgets_db.append(self.client)
        self.widgets_db.append(self.database)
        self.widgets_db.append(self.collection_button)
        self.widgets_db.append(self.collection_text)

        self.initialize = ttk.Checkbutton(self.db_func, text='初始化', variable=self.var_initialize)
        self.initialize.grid(row=0, column=0, sticky=tk.W)
        self.update = ttk.Checkbutton(self.db_func, text='更新', variable=self.var_update)
        self.update.grid(row=1, column=0, sticky=tk.W)
        self.delete = ttk.Checkbutton(self.db_func, text='删除', variable=self.var_delete)
        self.delete.grid(row=2, column=0, sticky=tk.W)
        self.widgets_db.append(self.initialize)
        self.widgets_db.append(self.update)
        self.widgets_db.append(self.delete)

        # self.db_panel.hide()
        self.db_panel.grid(row=0, column=3, rowspan=4, columnspan=6)


        # row1
        self.mode_frame = ttk.LabelFrame(self, borderwidth=3, text='模式', labelanchor=tk.N)
        self.mode_frame.rowconfigure(0, weight=1)
        # self.mode_frame.columnconfigure(0, weight=1)
        self.mode_frame.grid(row=1, column=0, rowspan=2, columnspan=3, sticky=tk.N+tk.S+tk.W+tk.E)

        self.mode_ontime = ttk.Radiobutton(self.mode_frame, text='实时', variable=self.var_mode, value='ontime')
        self.mode_ontime.grid(row=0, column=0)
        self.mode_mongo = ttk.Radiobutton(self.mode_frame, text='数据库', variable=self.var_mode, value='mongodb')
        self.mode_mongo.grid(row=0, column=1)
        self.widgets_top.append(self.mode_ontime)
        self.widgets_top.append(self.mode_mongo)


        # row4
        self.time_label = ttk.Label(self, text='定时:')
        self.time_label.grid(row=4, column=0, sticky=tk.E)
        self.time = ttk.Entry(self, textvariable=self.var_time)
        self.time.grid(row=4, column=1, sticky=tk.W)
        self.widgets_top.append(self.time)
        self.s_label = ttk.Label(self, text='秒')
        self.s_label.grid(row=4, column=2, sticky=tk.W)



        # self.seed_frame = ttk.LabelFrame(self, borderwidth=3, text='随机种子', labelanchor=tk.W)
        # self.seed_frame.rowconfigure(0, weight=1)
        # # self.seed_frame.columnconfigure(0, weight=1)
        # self.seed_frame.grid(row=4, column=3)
        #
        # self.seed_time = ttk.Radiobutton(self.seed_frame, text='随机', variable=self.var_seed, value=0)
        # self.seed_time.grid(row=0, column=0)

        self.seed_label = ttk.Label(self, text='随机种子:')
        self.seed_label.grid(row=4, column=3)
        self.seed = ttk.Entry(self, textvariable=self.var_seed)
        self.seed.grid(row=4, column=4, sticky=tk.W)
        self.widgets_top.append(self.seed)

        # row5
        self.bg_label = ttk.Label(self, text='背景颜色：')
        self.bg_label.grid(row=5, column=0)
        self.background = ttk.Entry(self, textvariable=self.var_background)
        self.background.grid(row=5, column=1)
        self.widgets_top.append(self.background)

        self.hide_image = ttk.Checkbutton(self, text='隐藏图片', variable=self.var_hide_image)
        self.hide_image.grid(row=5, column=2, columnspan=1, sticky=tk.W)
        self.widgets_top.append(self.hide_image)

        self.cache = ttk.Checkbutton(self, text='使用缓存', variable=self.var_cache)
        self.cache.grid(row=5, column=3, columnspan=1, sticky=tk.W)
        self.cache.config(state='disabled')     # 由于功能冲突 停用缓存功能
        self.widgets_top.append(self.cache)

        self.like_start_button = ttk.Button(self, text='喜爱列表', command=self.like_start, name='likestartButton')
        self.like_start_button.grid(row=5, column=4, columnspan=2, sticky=tk.W + tk.E)
        self.widgets_db.append(self.like_start_button)

        # row6
        self.config = ttk.Checkbutton(self, text='使用配置文件', variable=self.var_config)
        self.config.grid(row=6, column=0, columnspan=1, sticky=tk.W)
        self.widgets_top.append(self.config)

        self.save_config = ttk.Button(self, text='保存当前配置', command=self.save_config_file, name='saveConfig')
        self.save_config.grid(row=6, column=1)
        self.widgets_top.append(self.save_config)

        self.reset_button = ttk.Button(self, text='重置', command=self.reset_settings, name='resetButton')
        self.reset_button.grid(row=6, column=2, columnspan=2, sticky=tk.W + tk.E)
        self.widgets_top.append(self.reset_button)

        self.open_file_button = ttk.Button(self, text='打开目录文件', command=self.open_direc_file, name='openFile')
        self.open_file_button.grid(row=6, column=4, columnspan=2, sticky=tk.W+tk.E)
        self.widgets_top.append(self.open_file_button)

        # row7
        ttk.Separator(self, orient=tk.HORIZONTAL).grid(row=7, columnspan=10, sticky=tk.N+tk.W+tk.E)

        # row8
        self.strat_button = ttk.Button(self, text='开始', command=self.end, name='startButton')
        self.strat_button.grid(row=8, column=0, columnspan=2, sticky=tk.W + tk.E)
        self.widgets_top.append(self.strat_button)
        self.quit_button = ttk.Button(self, text='退出', command=self.Window.destroy, name='quitButton')
        self.quit_button.grid(row=8, column=2, columnspan=2, sticky=tk.W+tk.E)
        self.widgets_top.append(self.quit_button)

        self.version = ttk.Label(self, textvariable=self.var_version)
        self.version.grid(row=8, column=4)

    def widgets_init(self):
        if self.args.configfile:
            self.set_settings(self.args)
        else:
            self.set_settings(_default_args)
        if self.var_mode.get() == 'ontime':
            self.hide_db(0)
        else:
            self.show_db(0)



    def event_bind(self):
        self.version.bind('<Triple-Button-1>', self.debug)
        self.mode_mongo.bind('<Button-1>', self.show_db)
        self.mode_ontime.bind('<Button-1>', self.hide_db)
        self.bind_all('<Return>', lambda e: self.end())
        self.bind_all('<Shift-Return>', lambda e: self.like_start())
        self.bind_all('<Control-Return>', lambda e: self.like_start())

    def open_collection_panel(self):
        collection_window = tk.Toplevel(self)
        collection_window.title('数据库表选择')

        collection_window.grab_set()    # 锁定窗口操作

        frame1 = ttk.Frame(collection_window)
        frame1.pack(side='top', fill='both', expand=True)
        frame2 = ttk.Frame(collection_window)
        frame2.pack(anchor='center', fill='both', expand=True)
        frame3 = ttk.Frame(collection_window)
        frame3.pack(side='bottom', fill='both', expand=True)

        collction_list = []
        checkbox_vars = {}
        var_new_coolection = tk.StringVar()
        def refresh_collection(collction_list = collction_list, checkbox_vars = checkbox_vars):
            from pymongo import MongoClient
            client = MongoClient(self.args.client)
            db = client[self.args.database]
            collection_names = db.list_collection_names()
            collction_list = collection_names
            collction_list.sort()
            # print(collction_list)

            for each_collection in collction_list:
                if each_collection in checkbox_vars:
                    continue
                var = tk.IntVar()
                if each_collection in self.collection_list:
                    var.set(1)
                checkbox_vars[each_collection] = var
                collection_checkbox = ttk.Checkbutton(frame2, text=each_collection, variable=var)
                collection_checkbox.pack(anchor='center', expand=True, fill='x')

            if '__new' not in checkbox_vars:
                var = tk.IntVar()
                checkbox_vars['__new'] = var
                new_collection = ttk.Entry(frame2, textvariable=var_new_coolection)
                new_collection.pack(side='right', anchor='center', fill='x', expand=True)
                collection_checkbox = ttk.Checkbutton(frame2, variable=var)
                collection_checkbox.pack(side='left', anchor='center')

            collection_window.update()

        collecion_title = ttk.Label(frame1, text='数据库表选择')
        collecion_title.pack(anchor='center')
        refresh_collection_button = ttk.Button(frame1, text='更新表名', command=refresh_collection)
        refresh_collection_button.pack(side='left', anchor='s')
        var_all = tk.IntVar()
        collection_checkbox = ttk.Checkbutton(frame1, text='全选', variable=var_all)
        collection_checkbox.pack(side='right', anchor='s')

        refresh_collection()

        def collection_accept():
            if sum(k.get() for k in checkbox_vars.values()) < 1:
                tkinter.messagebox.showwarning('提示', '未选择数据库表!请至少选择一个数据库表!')
                return 0
            if var_all.get() == 1:
                del checkbox_vars['__new']
                for key in checkbox_vars.keys():
                    checkbox_vars[key].set(1)
            elif checkbox_vars['__new'].get()==1:
                del checkbox_vars['__new']
                var = tk.IntVar()
                var.set(1)
                checkbox_vars[var_new_coolection.get()] = var
            self.collection_list = [k for k in checkbox_vars.keys() if checkbox_vars[k].get()==1]
            self.collection_str.set('+'.join(self.collection_list))
            collection_window.destroy()
            print(self.collection_str.get())

        def collection_cancel():
            collection_window.destroy()

        collection_accept_button = ttk.Button(frame3, text='确定', command=collection_accept)
        collection_accept_button.pack(side='left', anchor='center',expand=True, fill='x')
        collection_cancel_button = ttk.Button(frame3, text='取消', command=collection_cancel)
        collection_cancel_button.pack(side='right', anchor='center',expand=True, fill='x')

        collection_window.mainloop()

        # self.Window.rowconfigure(0, weight=1)
        # self.Window.columnconfigure(0, weight=1)
        # self.Window.resizable(width=False, height=False)
        # self.rowconfigure(0, pad=100)
        # self.columnconfigure(0, pad=10)
        # self.grid(column=0, row=0, sticky=tk.N + tk.E + tk.W + tk.S)

    def clear_confirm(self):
        confirm = tk.tkMessageBox

    def debug(self, event):
        self.args.debug = True
        print("Debug On")

    def save_config_file(self):
        self.get_settings()
        self.args.initialize = False
        self.args.update = False
        self.args.clear = False
        # print(self.args.__dict__)
        check_configfile_option_and_save(self.args)
        self.get_settings()

    def reset_settings(self):
        if self.var_config.get():
            args = configtoargs()
            self.set_settings(configtoargs())
        else:
            self.set_settings(_default_args)

    def open_direc_file(self):
        file_path = self.args.targetpath
        from os import startfile
        startfile(file_path)

    def hide_db(self, event):
        for widget in self.widgets_db:
            widget.config(state='disabled')

    def show_db(self, event):
        for widget in self.widgets_db:
            widget.config(state='active')

    def set_settings(self, args):
        arg = args
        self.var_mode.set(arg.mode)

        self.var_time.set(int(arg.time))
        self.var_seed.set(str(arg.seed))
        self.var_background.set(str(arg.background))
        self.var_client.set(arg.client)
        self.var_database.set(arg.database)
        self.collection_list = arg.collection
        tmp_str = '+'.join(self.collection_list)
        self.collection_str.set(tmp_str)
        self.var_initialize.set(1 if arg.initialize else 0)
        self.var_update.set(1 if arg.update else 0)
        self.var_delete.set(1 if arg.clear else 0)
        self.var_hide_image.set(1 if arg.hideimage else 0)
        self.var_cache.set(1 if arg.cache else 0)
        self.var_config.set(1 if arg.configfile else 0)
        self.var_version.set(args.version)

    def get_settings(self):
        self.args.mode = self.var_mode.get()
        self.args.time = int(self.var_time.get())
        self.args.seed = float(self.var_seed.get())
        self.args.background = str(self.var_background.get())
        self.args.client = self.var_client.get()
        self.args.database = self.var_database.get()
        self.args.collection = self.collection_list
        self.args.initialize = True if self.var_initialize.get() else False
        self.args.update = True if self.var_update.get() else False
        self.args.clear = True if self.var_delete.get() else False
        self.args.hideimage = True if self.var_hide_image.get() else False
        self.args.cache = True if self.var_cache.get() else False
        self.args.configfile = True if self.var_config.get() else False

    def like_start(self):
        if self.var_mode.get() == 'mongodb':
            self.get_settings()
            self.args.collection = ['LIKES']
            self.args.initialize = False
            self.args.update = False
            self.args.clear = False
            self.end_state = True
            self.Window.destroy()
        else:
            pass

    def end(self):
        self.get_settings()
        self.end_state = True
        # 冻结面板
        # print('oppp')
        # self.mode_ontime.config(state='disabled')
        # # print('1')
        # for widget in self.widgets_top:
        #     widget.config(state='disabled')
        # # print('2')
        # self.hide_db(0)
        # print('3')
        # self.quit()
        self.Window.destroy()

    def __exit__(self, exc_type, exc_val, exc_tb):
        return True

    def __enter__(self):
        self.mainloop()

class Message(ttk.Frame):
    def __init__(self, message, master=None, ):
        self.message = message

        ttk.Frame.__init__(self, master)
        self.Window = self.winfo_toplevel()
        self.window_init()

        self.panel_init()

        self.create_widgets()

    def panel_init(self):
        self.grid(column=0, row=0, sticky=tk.N + tk.E + tk.W + tk.S)
        # self.rowconfigure(0, weight=7)
        # self.columnconfigure(0, weight=3)

    def window_init(self):
        self.Window.title('Attention!')
        self.Window.rowconfigure(0, weight=1)
        self.Window.columnconfigure(0, weight=1)
        # self.Window.resizable(width=False, height=False)

    def create_widgets(self):
        self.var_message = tk.StringVar()
        self.var_message.set(self.message)
        self.message_label = ttk.Label(self, textvariable=self.var_message)
        self.message_label.grid(row=0)
        self.quit_button = ttk.Button(self, text='退出', command=self.quit)
        self.quit_button.grid(row=1)

    def __enter__(self):
        self.mainloop()

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


if __name__ == '__main__':
    # tmp = Message('a\n\naoeuiniaoubvhisuofbn\nioavbuerib')

    tkk = tk.Tk()
    app = GUI(_default_args, tkk)
    # app.hide_db()
    with app:
        pass
    from time import sleep
    sleep(2)
    print(app.args.collection)
    print(app.args.mode)
    print('Done')