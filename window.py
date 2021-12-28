import tkinter.messagebox, random
from tkinter import *
import tool


class Window():
    def __init__(self):
        self.__db_help = tool.DBHelp()
        self.__tk = tkinter.Tk()
        self.__tk.title('成语接龙')
        self.__tk.geometry('485x230+600+300') # 宽, 高, x, y
        self.__tk.resizable(width = False, height = False) # 固定窗体大小
        self.__index = -1 # 默认接最后一个

        '''显示框'''
        self.__show_entry_text = StringVar()
        self.__show_entry = Entry(
            self.__tk,
            justify = 'center',
            textvariable = self.__show_entry_text,
            font = '微软雅黑 28',
            state = 'readonly',
        )
        self.__show_entry.grid(row = 1, column = 0, columnspan = 3, padx = 20, pady = 10)
        self.__show_entry_text.set(self.__db_help.roll())

        '''输入框'''
        self.__input_entry_text = StringVar()
        self.__input_entry = Entry(
            self.__tk,
            justify = 'center',
            textvariable = self.__input_entry_text,
            font = '微软雅黑 28',
        )
        self.__input_entry.bind('<Return>', self.__entrySubmit) # 绑定回车键
        self.__input_entry_text.set('请接龙并回车')
        self.__input_entry.grid(row = 2, column = 0, columnspan = 3, padx = 20, pady = 10)

        '''学习该词按钮'''
        self.__mode_btn = Button(
            self.__tk,
            text = '学习该词',
            font = '微软雅黑 18',
            command = lambda: self.__btnClick(1),
        )
        self.__mode_btn.grid(row = 3, column = 0)

        '''开始按钮'''
        self.__start_btn = Button(
            self.__tk,
            text = '重新接龙',
            font = '微软雅黑 18',
            command = lambda: self.__btnClick(2),
        )
        self.__start_btn.grid(row = 3, column = 2)

        '''回合数'''
        self.__round_num = StringVar()
        Label(
            font = '微软雅黑 17',
            textvariable = self.__round_num,
        ).grid(row = 3, column = 1, padx = 20)
        self.__round_num.set('回合数 0')

        '''关于'''
        Label(
            text = 'GitHub: lilongxiang2000',
            font = '微软雅黑 12',
        ).grid(row = 4, column = 0, columnspan = 3)


        self.__tk.mainloop()

    def __entrySubmit(self, e):
        '''输入框回车时'''
        if len(self.__input_entry_text.get()) == 4:
            self.__start_btn.config(text = '重新开始')
            if self.__db_help.checkPy(
                self.__input_entry_text.get()[0],
                self.__show_entry_text.get()[self.__index]
            ):
                # 回合数 + 1
                self.__round_num.set(
                    self.__round_num.get().split(' ')[0] + ' ' \
                    + str(int(self.__round_num.get().split(' ')[-1]) + 1)
                )
                # 保存查询到的所有成语
                values = self.__db_help.selectFirst(self.__input_entry_text.get()[-1])
                if values == []:
                    self.__show_entry_text.set('你赢了')
                    '''未有的成语加入数据库'''
                    self.__start_btn.config(text = '重新开始')
                else:
                    # 随机挑选一个成语
                    value = random.choice(values)
                    self.__show_entry_text.set(self.__input_entry_text.get() +\
                    '→' + ''.join(i for i in value))
                    self.__input_entry_text.set('') # 清空输入框
            else:
                self.__show_entry_text.set('接龙失败，请重新开始')
                self.__input_entry.config(state = 'readonly') # 限制输入框只读
        else:
            self.__input_entry_text.set('请输入四字成语')
            self.__input_entry.config(state = 'readonly') # 限制输入框只读

    def __btnClick(self, btn):
        '''点击按钮时'''
        if btn == 1:
            info = self.__db_help.selectInfo(
                self.__show_entry_text.get().split('→')[-1]
            )
            tkinter.messagebox.showinfo(
                self.__show_entry_text.get().split('→')[-1] + ' ' + ' '.join(str(i) for i in info[1:]),
                info[0])
        if btn == 2:
            self.__show_entry_text.set(self.__db_help.roll())
            self.__input_entry.config(state = 'normal')
            self.__input_entry_text.set('请接龙并回车')
            self.__round_num.set('回合数 0') # 重置回合数
            self.__start_btn.config(text = '重新接龙')


if __name__ == '__main__':
    Window()
