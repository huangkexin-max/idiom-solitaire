import sqlite3, random


class DBHelp():
    def __init__(self, db_path = 'DB/idioms.db'):
        self.__db_path = db_path
        self.__coon = sqlite3.connect(self.__db_path)
        print('已连接数据库')
        self.__cur = self.__coon.cursor()

    def selectInfo(self, text: str):
        '''查询该成语详细信息'''
        self.__cur.execute(
            '''select mean, pytone1, pytone2, pytone3, pytone4 from idiom
            where char1 = ? and char2 = ? and char3 = ? and char4 = ?
            ''',
            (text[-4], text[-3], text[-2], text[-1],)
        )
        info = self.__cur.fetchall()
        return info[0]

    def selectFirst(self, text: str):
        '''查询首字与 text 音相同的成语'''
        # 需要传递一个序列，哪怕只有一个参数
        self.__cur.execute('select py1 from idiom where char1 = ?', (text[-1],))
        py = self.__cur.fetchall() # 获取该字拼音
        if py == []:
            return []
        else:
            py = py[0][0]
        # 模糊音处理
        if py[0:2] in ['zh', 'ch', 'sh']:
            self.__cur.execute(
                'select char1, char2, char3, char4 from idiom where py1 = ? or py1 = ?',
                (py[0] + py[2:], py)
            )
            return self.__cur.fetchall()
        elif py[0] in ['z', 'c', 's']:
            self.__cur.execute(
                'select char1, char2, char3, char4 from idiom where py1 = ? or py1 = ?',
                (py, py[0] + 'h' + py[1:])
            )
            return self.__cur.fetchall()
        else:
            self.__cur.execute(
                'select char1, char2, char3, char4 from idiom where py1 = ?',
                (py,)
            )
            return self.__cur.fetchall() # [('哀', '思', '如', '潮'), ...]

    def checkPy(self, text1, text2):
        '''检查 text1 与 text2 拼音是否相同，不分翘平舌'''
        self.__cur.execute('select py1 from idiom where char1 = ?', (text1,))
        py1 = self.__cur.fetchall()
        if py1 == []:
            self.__cur.execute('select py2 from idiom where char2 = ?', (text1,))
            py1 = self.__cur.fetchall()
        if py1 == []:
            self.__cur.execute('select py3 from idiom where char3 = ?', (text1,))
            py1 = self.__cur.fetchall()
        if py1 == []:
            self.__cur.execute('select py4 from idiom where char4 = ?', (text1,))
            py1 = self.__cur.fetchall()

        self.__cur.execute('select py1 from idiom where char1 = ?', (text2,))
        py2 = self.__cur.fetchall()
        if py2 == []:
            self.__cur.execute('select py2 from idiom where char2 = ?', (text2,))
            py2 = self.__cur.fetchall()
        if py2 == []:
            self.__cur.execute('select py3 from idiom where char3 = ?', (text2,))
            py2 = self.__cur.fetchall()
        if py2 == []:
            self.__cur.execute('select py4 from idiom where char4 = ?', (text2,))
            py2 = self.__cur.fetchall()

        if py1 == [] or py2 == []:
            return False
        py1, py2 = py1[0][0], py2[0][0]
        if py1[0:2] in ['zh', 'ch', 'sh']:
            py1 = py1[0] + py1[2:]
        if py2[0:2] in ['zh', 'ch', 'sh']:
            py2 = py2[0] + py2[2:]
        return py1 == py2

    def roll(self):
        '''随机生成一个成语'''
        self.__cur.execute('select count(*) from idiom')
        rows = int(self.__cur.fetchall()[0][0]) # 获取总行数
        # 需要传递一个序列，哪怕只有一个参数
        self.__cur.execute('select char1, char2, char3, char4\
        from idiom where id = ?', (str(random.randint(1, rows + 1)),))

        return ''.join(i for i in self.__cur.fetchall()[0])
