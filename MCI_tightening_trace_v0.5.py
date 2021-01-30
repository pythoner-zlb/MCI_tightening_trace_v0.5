#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/4 21:06
# @Author  : LBZ

"""
    软件功能：
    TTP:Tightening Traces Presenting
    1.使用tkinter显示界面
    2.通过File-Open选择txt，xlsx，csv格式文件
    3.选择合适的坐标轴参数，选择是否同步至某点，点击“确定”就可以打开浏览器生成曲线
    4.如果浏览器生成曲线缓慢，重新点击“确定”
"""

import tkinter
from tkinter import ttk
import tkinter.filedialog as fd
import pandas as pd
import tkinter.messagebox
import plotly.graph_objects as go
import plotly.validators.scatter
import plotly.validators.layout.legend
import plotly.validators.layout.legend.font
import plotly.validators.layout.legend.title
import plotly.validators.layout.title
import plotly.validators.layout.title.font
import plotly.validators.layout.font
import plotly.validators.layout.xaxis
import plotly.validators.layout.xaxis.title
import plotly.validators.layout.yaxis
import plotly.validators.layout.yaxis.title
import plotly.validators.layout.grid

# 选中文件路径变量
file_paths_in_window = None
# 要显示坐标轴，顺序是[xaxis, yaxis1, yaxis2]，非None的位置有效
axis = [None, None, None]
# 决定是否需要同步曲线及同步起点，仅对yaxis1做同步
synch_value = None    # None代表无动作
# labels表示坐标轴名称
labels = [None, ]
# units表示坐标轴单位
units = {}
# labels和units组成字典
labels_units = {}


class Openfiles(object):
    def __init__(self):
        print('正在打开文件对话框... ...')
        filenames = None
        pass

    def openfiles(self):
        # 读取选中的文件绝对路径名称
        filenames = fd.askopenfilenames(initialdir=r'C:\Users\dabinde\Desktop',
                                       filetypes=[('text files', '.txt'), ('ecxel files', '.xlsx'),
                                                  ('csv files', '.csv')])
        return filenames

class Window(object):
    def __init__(self):
        print('正在运行界面... ...')
        pass

    def window(self):
        # 创建窗口
        tk = tkinter.Tk()
        tk.title('TTP_v0.1 By ZLB')
        tk.geometry('640x400+400+200')

        # 创建下拉菜单menu_bar，和下拉内容
        menu_bar = tkinter.Menu(tk)
        tk.config(menu=menu_bar)

        def openFile():
            # 创建全局变量，以便得到的结果能在函数外使用
            global file_paths_in_window, labels, units, labels_units
            file_paths_in_window = list(Openfiles().openfiles())

            ### 新插入
            # 查找文件中空白行的行数，方便后期pandas读取文件时读到指定起始行
            blank_row_nums = 0
            # 将每个文件的空白行行数存入列表
            blank_row_nums_list = []
            # 查找以‘Time;’开头的起始行，作为后期pandas读取数据的首行标题
            start_row = 0
            # 将每个文件起始行行数值存入列表
            start_row_list = []
            # 获得每个文件的数据起始行，以适应不同文件起始行不一样的问题，以‘Time;’为查找依据
            for i in range(len(file_paths_in_window)):
                with open(file_paths_in_window[i], 'r', encoding='gbk') as f:
                    #     print(f.readlines())
                    for line in f.readlines():
                        start_row += 1
                        if line is '\n':
                            blank_row_nums += 1
                        if 'Time;' in line:
                            start_row_list.append(start_row)
                            blank_row_nums_list.append(blank_row_nums)
                            # print(start_row)
                            blank_row_nums = 0
                            start_row = 0
                            break
                        else:
                            pass
            # print(start_row_list)
            # print(blank_row_nums_list)

            # 从选中文件的绝对路径打开文件内容，将内容存到DataFrame中，并得到坐标名称和单位
            for i in range(len(file_paths_in_window)):
                if (str(file_paths_in_window[i])).endswith(('.csv', '.CSV')):
                    df = pd.read_csv(str(file_paths_in_window[i]),
                                     header=(start_row_list[i]-blank_row_nums_list[i]-1), delimiter=';')
                    labels = list(df.columns)
                    units = list(df.iloc[0])
                    labels_units = dict(zip(labels, units))
                    labels.insert(0, '')

                elif (str(file_paths_in_window[i])).endswith(('.txt', '.TXT')):
                    df = pd.read_csv(str(file_paths_in_window[i]),
                                     header=(start_row_list[i]-blank_row_nums_list[i]-1), delimiter=';')
                    labels = list(df.columns)
                    units = list(df.iloc[0])
                    labels_units = dict(zip(labels, units))
                    labels.insert(0, '')
                elif (str(file_paths_in_window[i])).endswith(('.xlsx', '.XLSX')):
                    df = pd.read_excel(str(file_paths_in_window[i]),
                                       header=(start_row_list[i]-blank_row_nums_list[i]-1))
                    labels = list(df.columns)
                    units = list(df.columns.str.split(';'))
                    labels_units = dict(zip(labels, units))
                    labels.insert(0, '')
                else:
                    pass

            # 将坐标名称传给combobox，以便后期选取
            combobox1['value'] = labels
            combobox2['value'] = labels
            combobox3['value'] = labels

            return file_paths_in_window, labels, units

        def savedAs():
            tkinter.messagebox.showinfo(title='Tips', message='Under developing...')
            return

        def version():
            tkinter.messagebox.showinfo(title='Tips', message='Under developing...')
            return

        def help():
            tkinter.messagebox.showinfo(title='Tips', message='Under developing...')
            return

        # 创建下拉菜单-1
        file_menu1 = tkinter.Menu(menu_bar, tearoff=0)
        file_menu1.add_command(label='Open', command=openFile)
        file_menu1.add_command(label='Saved as', command=savedAs)
        menu_bar.add_cascade(label='File', menu=file_menu1)

        # 创建下拉菜单-2
        file_menu2 = tkinter.Menu(menu_bar, tearoff=0)
        file_menu2.add_command(label='Version', command=version)
        file_menu2.add_command(label='Help', command=help)
        menu_bar.add_cascade(label='Help', menu=file_menu2)

        # 显示提示信息
        label0 = tkinter.Label(tk, text='***首先点击\'File->Open\'，选择文件***', font=('yahei', 10, 'bold'))
        label0.grid(row=0, column=1, rowspan=1, columnspan=1, padx=20, pady=10, ipadx=0, ipady=0,
                         sticky=tkinter.W)

        # 创建‘选择坐标轴’栏及内部内容
        labelframe1 = tkinter.LabelFrame(tk, text='选择坐标轴', width=550, height=100)
        labelframe1.grid(row=1, column=1, rowspan=1, columnspan=1, padx=20, pady=5, ipadx=20, ipady=0,
                         sticky=tkinter.W)

        # 创建x轴label及选项菜单
        label1 = tkinter.Label(labelframe1, text='  X轴', font=('yahei', 16, 'bold'))
        label1.grid(row=2, column=1, rowspan=1, columnspan=1, ipadx=0, ipady=0, padx=0, pady=20)
        var1 = tkinter.StringVar()
        combobox1 = ttk.Combobox(labelframe1, textvariable=var1, state='readonly', width=10)
        # combobox1['value'] = labels
        # combobox1.current()
        combobox1.grid(row=2, column=2, rowspan=1, columnspan=2, ipadx=0, ipady=0, padx=0, pady=20)

        # 创建y1轴label及选项菜单
        label2 = tkinter.Label(labelframe1, text='  Y1轴', font=('yahei', 16, 'bold'))
        label2.grid(row=2, column=4, rowspan=1, columnspan=1, ipadx=0, ipady=0, padx=0, pady=20)
        var2 = tkinter.StringVar()
        combobox2 = ttk.Combobox(labelframe1, textvariable=var2, state='readonly', width=10)
        # combobox2['value'] = labels
        # combobox2.current(1)
        combobox2.grid(row=2, column=5, rowspan=1, columnspan=2, ipadx=0, ipady=0, padx=0, pady=20)

        # 创建y2轴label及选项菜单
        label3 = tkinter.Label(labelframe1, text='  Y2轴', font=('yahei', 16, 'bold'))
        label3.grid(row=2, column=7, rowspan=1, columnspan=1, ipadx=0, ipady=0, padx=0, pady=20)
        var3 = tkinter.StringVar()
        combobox3 = ttk.Combobox(labelframe1, textvariable=var3, state='readonly', width=10)
        # combobox3['value'] = labels
        # # combobox3.current()
        combobox3.grid(row=2, column=8, rowspan=1, columnspan=2, ipadx=0, ipady=0, padx=0, pady=20)

        var1 = tkinter.IntVar()
        var2 = tkinter.IntVar()
        def not_merge_traces():
            if var1.get() == 1:
                checkbutton2.config(state=tkinter.DISABLED)
                e1.delete(0, tkinter.END)
                e1.config(state=tkinter.DISABLED)
                b2.config(state=tkinter.NORMAL)
            elif var1.get() == 0:
                checkbutton2.config(state=tkinter.NORMAL)
                e1.config(state=tkinter.NORMAL)
                b2.config(state=tkinter.DISABLED)
            return
        def merge_traces():
            # print('merge_traces')
            if var2.get() == 1:
                checkbutton1.config(state=tkinter.DISABLED)
                b2.config(state=tkinter.NORMAL)
            elif var2.get() == 0:
                checkbutton1.config(state=tkinter.NORMAL)
                b2.config(state=tkinter.DISABLED)
            return
        # 创建‘合并拧紧曲线’栏
        labelframe2 = tkinter.LabelFrame(tk, text='同步拧紧曲线', width=550, height=200)
        labelframe2.grid(row=2, column=1, rowspan=1, columnspan=1, padx=20, pady=10, ipadx=20, ipady=0,
                         sticky=tkinter.W)

        label6 = tkinter.Label(labelframe2, text='是否需要同步曲线?', font=('yahei', 16, 'bold'))
        label6.grid(row=2, column=1, rowspan=1, columnspan=3, padx=10, pady=10, ipadx=10, ipady=10, sticky=tkinter.W)
        checkbutton1 = tkinter.Checkbutton(labelframe2, text='No', variable=var1, onvalue=1, offvalue=0, height=2,
                                           font=('yahei', 16, 'bold'), takefocus=1, command=not_merge_traces)
        checkbutton1.grid(row=2, column=4, rowspan=1, columnspan=1, padx=10, pady=0, ipadx=0, ipady=0)
        checkbutton2 = tkinter.Checkbutton(labelframe2, text='Yes', variable=var2, onvalue=1, offvalue=0,
                                           font=('yahei', 16, 'bold'), takefocus=1, command=merge_traces)
        checkbutton2.grid(row=2, column=5, rowspan=1, columnspan=1, padx=10, pady=0, ipadx=0, ipady=0)
        checkbutton2.config(state=tkinter.DISABLED)

        label7 = tkinter.Label(labelframe2, text='请输入合并值：', font=('yahei', 16, 'bold'))
        label7.grid(row=3, column=1, rowspan=1, columnspan=3, padx=10, pady=10, ipadx=10, ipady=10, sticky=tkinter.W)
        e1 = tkinter.Entry(labelframe2, font=('yahei', 16, 'bold'), width=16)
        e1.grid(row=3, column=4, rowspan=1, columnspan=6, padx=0, pady=0, ipadx=0, ipady=0, sticky=tkinter.W)
        e1.config(state=tkinter.DISABLED)

        # 关闭程序
        def b1():
            tk.destroy()
            return
        # 点击‘确认’键后，显示曲线
        def b2():
            # 列表初始化
            axis = []
            # 获得选择的关键参数结果
            axis.append(combobox1.get())
            axis.append(combobox2.get())
            axis.append(combobox3.get())
            synch_value = e1.get()

            # 类的实例化
            data = Data()

            # 判断是否选中文件
            if file_paths_in_window in (None, ''):
                # print(type(file_paths_in_window))  # 可能是''，也可能是None
                tkinter.messagebox.showerror(title='No File Found', message='未选择文件！')
            else:
                # 判断坐标轴是否选择正确
                # if '' not in axis and len(axis) == 3:
                if axis.count('') == 0:
                    # 判断是否需要同步x-y1曲线
                    if synch_value is '':
                        pass
                    else:
                        try:
                            synch_value = float(synch_value)
                        except Exception as e:
                            tkinter.messagebox.showerror(title='数据错误', message=e)

                    # 实例化使用
                    data.dataprocessing(file_paths_in_window, axis=axis, synch_value=synch_value)

                elif axis.count('') == 1:
                    # 判断是否需要同步x-y1曲线
                    if synch_value is '':
                        pass
                    else:
                        try:
                            synch_value = float(synch_value)
                        except Exception as e:
                            tkinter.messagebox.showerror(title='数据错误', message=e)

                    # 实例化使用
                    data.dataprocessing(file_paths_in_window, axis=axis, synch_value=synch_value)

                elif axis.count('') >= 2:
                    tkinter.messagebox.showerror(title='数据缺失', message='数据缺失，请设定正确的坐标参数')
                else:
                    pass

        # 清除synch_value的输入值
        def b3():
            e1.delete(0, tkinter.END)
            return
        # 创建关键按钮，确保可以退出程序
        b1 = tkinter.Button(labelframe2, text='关闭', command=b1, font=('yahei', 20, 'bold'), width=6, height=1)
        b1.grid(row=4, column=2, rowspan=1, columnspan=1, padx=0, pady=20, ipadx=0, ipady=0, sticky=tkinter.W)
        b2 = tkinter.Button(labelframe2, text='确认', command=b2, font=('yahei', 20, 'bold'), width=6, height=1)
        b2.grid(row=4, column=4, rowspan=1, columnspan=1, padx=0, pady=20, ipadx=0, ipady=0, sticky=tkinter.W)
        b2.config(state=tkinter.DISABLED)
        b3 = tkinter.Button(labelframe2, text='清除', command=b3, font=('yahei', 20, 'bold'), width=6, height=1)
        b3.grid(row=4, column=6, rowspan=1, columnspan=1, padx=0, pady=20, ipadx=0, ipady=0, sticky=tkinter.W)

        tk.mainloop()

class Data(object):
    def __init__(self):
        print('正在处理数据... ...')
        pass

    def dataprocessing(self, file_paths, axis=[None, None, None], synch_value=None):
        # 去除axis中的空字符串，方便后续分析
        for i in range(axis.count('')):
            if '' in axis:
                axis.remove('')
            else:
                pass

        # 确定文件个数
        trace_num = len(file_paths)
        # 将文件名存到列表中，以便后期网页数据呈现时做标题
        file_names = []
        for i in range(len(file_paths)):
            file_names.append(file_paths[i].split('/')[-1])

        # 查找文件中空白行的行数，方便后期pandas读取文件时读到指定起始行
        blank_row_nums = 0
        # 将每个文件的空白行行数存入列表
        blank_row_nums_list = []
        # 查找以‘Time;’开头的起始行，作为后期pandas读取数据的首行标题
        start_row = 0
        # 将每个文件起始行行数值存入列表
        start_row_list = []
        # 获得每个文件的数据起始行，以适应不同文件起始行不一样的问题，以‘Time;’为查找依据
        for i in range(len(file_paths)):
            with open(file_paths[i], 'r', encoding='gbk') as f:
                #     print(f.readlines())
                for line in f.readlines():
                    start_row += 1
                    if line is '\n':
                        blank_row_nums += 1
                    if 'Time;' in line:
                        start_row_list.append(start_row)
                        blank_row_nums_list.append(blank_row_nums)
                        # print(start_row)
                        blank_row_nums = 0
                        start_row = 0
                        break
                    else:
                        pass
        # print(start_row_list)
        # print(blank_row_nums_list)


        # 存放每条曲线数据对应的Dataframe对象名
        df_list = []
        # 存放经过同步处理后的每条曲线数据对应的Dataframe对象名
        df_synch_list = []
        # 存放每条曲线数据对应的同步点序号
        df_breakpoint_index_list = []
        # # 设置坐标轴名称
        # labels = []
        # # 设置坐标单位
        # units = []

        for i in range(trace_num):
            # 获得文件数据(csv,txt,xlsx三种类型)，存入DataFrame，并将DataFrame放到列表中，方便以后调用
            if (str(file_paths[i])).endswith(('.csv', '.CSV')):
                df = pd.read_csv(str(file_paths[i]), header=(start_row_list[i]-blank_row_nums_list[i]-1), delimiter=';')
                labels = list(df.columns)
                units = list(df.iloc[0])
                labels_units = dict(zip(labels, units))
                labels.insert(0, '')
                df = df.iloc[1:, ].astype(float)
                df_list.append(df)
            elif (str(file_paths[i])).endswith(('.txt', '.TXT')):
                df = pd.read_csv(str(file_paths[i]), header=(start_row_list[i]-blank_row_nums_list[i]-1), delimiter=';')
                labels = list(df.columns)
                units = list(df.iloc[0])
                labels_units = dict(zip(labels, units))
                labels.insert(0, '')
                df = df.iloc[1:, ].astype(float)
                df_list.append(df)
            elif (str(file_paths[i])).endswith(('.xlsx', '.XLSX')):
                df = pd.read_excel(str(file_paths[i]), header=2)
                labels = list(df.columns)
                units = list(df.columns.str.split(';'))
                labels_units = dict(zip(labels, units))
                labels.insert(0, '')
                df.iloc[:, 0].str.split(';', expand=True).astype(float)
                df = df.iloc[1:, ].astype(float)
                df_list.append(df)
            else:
                pass

            # 合并曲线的关键参数！！！将Y1轴列中大于synch_value的数据提取出来存入df_breakpoint_index中
            if isinstance(synch_value, (int, float)):
                try:
                    df_breakpoint_index = df[df[axis[1]] > synch_value].index[0]
                except Exception as e:
                    tkinter.messagebox.showerror(title='Error!', message=e)
                    break
                df_breakpoint_index_list.append(df_breakpoint_index)

                # 将原Dataframe数据，经过同步处理成synchronized-data
                # 将X轴坐标同步化
                df_synch = df_list[i]
                # 将第0列整体减去synch_value值对应的数
                df_synch[axis[0]] = df_synch[axis[0]]-df_synch[axis[0]][df_breakpoint_index_list[i]]
                df_synch_list.append(df_synch)

        # 数据呈现
        # 判断是否使用双Y轴：axis==3：双Y轴；axis==2：仅1个Y轴.
        data = []    # 用于存放不同步曲线
        data_synch = []    # 用于存放同步曲线
        if len(axis) == 3:    # ==3：双轴；==2：单轴
            for i in range(len(df_list)):
                # # 判断是否显示同步后的曲线：df_synch_list非空列表，则显示同步；反之，则显示原有结果
                # if df_synch_list is not []:
                # 同步
                if isinstance(synch_value, (int, float)):    # 为True：需要同步；为False：不需要同步
                    # 创建Y1-X轴数据
                    data1 = go.Scatter(x=df_synch_list[i][axis[0]], y=df_synch_list[i][axis[1]],
                                       mode='lines', name=file_names[i] + '-' + axis[1], text=axis[1], yaxis='y')
                    # 创建Y2-X轴数据
                    data2 = go.Scatter(x=df_synch_list[i][axis[0]], y=df_synch_list[i][axis[2]],
                                       mode='lines', name=file_names[i] + '-' + axis[2], text=axis[2], yaxis='y2')
                    data_synch.append(data1)
                    data_synch.append(data2)
                else:
                    # 创建Y1-X轴数据
                    data1 = go.Scatter(x=df_list[i][axis[0]], y=df_list[i][axis[1]],
                                       mode='lines', name=file_names[i] + '-' + axis[1], text=axis[1], yaxis='y')
                    # 创建Y2-X轴数据
                    data2 = go.Scatter(x=df_list[i][axis[0]], y=df_list[i][axis[2]],
                                       mode='lines', name=file_names[i] + '-' + axis[2], text=axis[2], yaxis='y2')
                    data.append(data1)
                    data.append(data2)

            if isinstance(synch_value, (int, float)):
                layout = dict(title='[Synchronized] ' + axis[2] + '/' + axis[1] + ' vs. ' + axis[0],
                              xaxis=dict(title=axis[0]+'-'+labels_units[axis[0]], zeroline=False),  # tick0=10, dtick=10),
                              yaxis=dict(title=axis[1]+'-'+labels_units[axis[1]], zeroline=False),
                              yaxis2=dict(title=axis[2]+'-'+labels_units[axis[2]], zeroline=False, overlaying='y', side='right',
                                          showgrid=False, gridcolor='red'),
                              legend=dict(x=1.05, y=1, font=dict(color='steelblue', family='Arial', size=12)),
                              )
                fig = go.Figure(data=data_synch, layout=layout)
            else:
                layout = dict(title=axis[2] + '/' + axis[1] + ' vs. ' + axis[0],
                              xaxis=dict(title=axis[0]+'-'+labels_units[axis[0]], zeroline=False),  # tick0=10, dtick=10),
                              yaxis=dict(title=axis[1]+'-'+labels_units[axis[1]], zeroline=False),
                              yaxis2=dict(title=axis[2]+'-'+labels_units[axis[2]], zeroline=False, overlaying='y', side='right',
                                          showgrid=False, gridcolor='red'),
                              legend=dict(x=1.05, y=1, font=dict(color='steelblue', family='Arial', size=12)),
                              )
                fig = go.Figure(data=data, layout=layout)
            fig.show()

        # 判断是否使用双Y轴：axis==3：双Y轴；axis==2：仅Y1轴.
        elif len(axis) == 2:
            for i in range(len(df_list)):
                # 判断是否显示同步后的曲线：synch_value非空字符串，则显示同步；反之，则显示原有结果
                if isinstance(synch_value, (int, float)):
                    # 创建Y1-X轴数据
                    # print('a-', axis)
                    data1 = go.Scatter(x=df_synch_list[i][axis[0]], y=df_synch_list[i][axis[1]],
                                       mode='lines', name=file_names[i] + '-' + axis[1], text=axis[1])
                    data_synch.append(data1)
                else:
                    # 创建Y1-X轴数据
                    # print('b-', axis)
                    data1 = go.Scatter(x=df_list[i][axis[0]], y=df_list[i][axis[1]],
                                       mode='lines', name=file_names[i] + '-' + axis[1], text=axis[1])
                    data.append(data1)

            if isinstance(synch_value, (int, float)):
                layout = dict(title='[Synchronized] ' + axis[1] + ' vs. ' + axis[0],
                              xaxis=dict(title=axis[0]+'-'+labels_units[axis[0]], zeroline=False),  # tick0=10, dtick=10),
                              yaxis=dict(title=axis[1]+'-'+labels_units[axis[1]], zeroline=False),
                              legend=dict(x=1.05, y=1, font=dict(color='steelblue', family='Arial', size=12))
                              )
                fig = go.Figure(data=data_synch, layout=layout)
            else:
                layout = dict(title=axis[1] + ' vs. ' + axis[0],
                              xaxis=dict(title=axis[0]+'-'+labels_units[axis[0]], zeroline=False),  # tick0=10, dtick=10),
                              yaxis=dict(title=axis[1]+'-'+labels_units[axis[1]], zeroline=False),
                              legend=dict(x=1.05, y=1, font=dict(color='steelblue', family='Arial', size=12))
                              )
                fig = go.Figure(data=data, layout=layout)
            fig.show()

        else:
            tkinter.messagebox.showerror(title='缺少数据', message='请选择X和Y轴坐标数据！')

# 类的实例化
window = Window()
# 实例化使用
window.window()