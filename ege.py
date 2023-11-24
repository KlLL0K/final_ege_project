# по всем вопросом можно написать мне в телеграме
import time
import datetime
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QLabel, QMainWindow
import sqlite3
from Logs import Logs

zadanie = 0

# создание бд
# --------------------------------------
bunch = 0
vin_var = 0
conn = sqlite3.connect("my_database.db")
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS my_table (
    k_start INTEGER,
    k_max INTEGER,
    d1 TEXT,
    d2 TEXT,
    d3 TEXT
)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS result_table (
    time REAL,
    execution_time REAL
)''')
conn.commit()
conn.close()


# --------------------------------------
# вычисление времени выполнения кода
def timer_decorator(func):
    def wrapper(*args, **kwargs):
        connect = sqlite3.connect("my_database.db")
        cur = connect.cursor()
        start_time = time.time()
        result = func(*args, **kwargs)
        cur.execute("INSERT INTO result_table (result, execution_time) VALUES (?, ?)",
                    (datetime.datetime.now(), time.time() - start_time))
        connect.commit()
        connect.close()
        return result

    return wrapper


# --------------------------------------
# функции для вычисления ответа на 19 задание егэ
def sol_k1d3(x, p, k_max, d1, d2, d3):
    if x >= k_max and p == 3:
        return 1
    if x < k_max and p == 3:
        return 0
    if x >= k_max and p > 3:
        return 0
    if d3:
        return sol_k1d3(eval(d1), p + 1, k_max, d1, d2, d3) or sol_k1d3(eval(d2), p + 1, k_max, d1, d2, d3) or sol_k1d3(
            eval(d3), p + 1,
            k_max,
            d1, d2, d3)
    else:
        return sol_k1d3(eval(d1), p + 1, k_max, d1, d2, d3) or sol_k1d3(eval(d2), p + 1, k_max, d1, d2, d3)


@timer_decorator
def result_k1d3():
    k_start, k_max, d1, d2, d3 = 0, 0, 0, 0, 0
    conn1 = sqlite3.connect("my_database.db")
    cursor1 = conn1.cursor()
    cursor1.execute("SELECT * FROM my_table")
    row = cursor1.fetchall()[-1]
    if row is not None:
        k_start, k_max, d1, d2, d3 = row
    conn1.close()
    for i in range(100):
        if sol_k1d3(x=i, p=1, k_max=k_max, d1=d1, d2=d2, d3=d3):
            return i


def sol_k1d3_any(x, p, k_max, d1, d2, d3):
    if x >= k_max and p == 3:
        return 1
    if x < k_max and p == 3:
        return 0
    if x >= k_max and p > 3:
        return 0
    if d3:
        if p % 2 == 0:
            return (sol_k1d3_any(eval(d1), p + 1, k_max, d1, d2, d3) or sol_k1d3_any(eval(d2), p + 1, k_max, d1, d2,
                                                                                     d3) or
                    sol_k1d3_any(
                        eval(d3), p + 1,
                        k_max,
                        d1, d2, d3))
        else:
            return sol_k1d3_any(eval(d1), p + 1, k_max, d1, d2, d3) and sol_k1d3_any(eval(d2), p + 1, k_max, d1, d2,
                                                                                     d3) and sol_k1d3_any(
                eval(d3), p + 1,
                k_max,
                d1, d2, d3)
    else:
        if p % 2 == 0:
            return sol_k1d3_any(eval(d1), p + 1, k_max, d1, d2, d3) or sol_k1d3_any(eval(d2), p + 1, k_max, d1, d2, d3)
        else:
            return sol_k1d3_any(eval(d1), p + 1, k_max, d1, d2, d3) and sol_k1d3_any(eval(d2), p + 1, k_max, d1, d2, d3)


@timer_decorator
def result_k1d3_any():
    k_start, k_max, d1, d2, d3 = 0, 0, 0, 0, 0
    conn1 = sqlite3.connect("my_database.db")
    cursor1 = conn1.cursor()
    cursor1.execute("SELECT * FROM my_table")
    row = cursor1.fetchall()[-1]
    if row is not None:
        k_start, k_max, d1, d2, d3 = row
    conn1.close()
    for i in range(100):
        if sol_k1d3_any(x=i, p=1, k_max=k_max, d1=d1, d2=d2, d3=d3):
            return i


def sol_k2d3(x, y, p, k_max, d1, d2, d3):
    d4 = f"y{d1[1:]}"
    d5 = f"y{d2[1:]}"
    d6 = f"y{d3[1:]}"
    if x + y >= k_max and p == 3:
        return 1
    if x + y < k_max and p == 3:
        return 0
    if x + y >= k_max and p > 3:
        return 0
    if d3:
        return (sol_k2d3(eval(d1), y, p + 1, k_max, d1, d2, d3)
                or sol_k2d3(eval(d2), y, p + 1, k_max, d1, d2, d3)
                or sol_k2d3(eval(d3), y, p + 1, k_max, d1, d2, d3)
                or sol_k2d3(x, eval(d4), p + 1, k_max, d1, d2, d3)
                or sol_k2d3(x, eval(d5), p + 1, k_max, d1, d2, d3)
                or sol_k2d3(x, eval(d6), p + 1, k_max, d1, d2, d3)
                )

    else:
        return (sol_k2d3(eval(d1), y, p + 1, k_max, d1, d2, d3)
                or sol_k2d3(eval(d2), y, p + 1, k_max, d1, d2, d3)
                or sol_k2d3(x, eval(d4), p + 1, k_max, d1, d2, d3)
                or sol_k2d3(x, eval(d5), p + 1, k_max, d1, d2, d3)
                )


@timer_decorator
def result_k2d3():
    k_start, k_max, d1, d2, d3 = 0, 0, 0, 0, 0
    conn2 = sqlite3.connect("my_database.db")
    cursor2 = conn2.cursor()
    cursor2.execute("SELECT * FROM my_table")
    row = cursor2.fetchall()[-1]
    if row is not None:
        k_start, k_max, d1, d2, d3 = row
    conn2.close()
    for i in range(100):
        if sol_k2d3(x=i, y=k_start, p=1, k_max=k_max, d1=d1, d2=d2, d3=d3):
            return i


def sol_k2d3_any(x, y, p, k_max, d1, d2, d3):
    d4 = f"y{d1[1:]}"
    d5 = f"y{d2[1:]}"
    d6 = f"y{d3[1:]}"
    if x + y >= k_max and p == 3:
        return 1
    if x + y < k_max and p == 3:
        return 0
    if x + y >= k_max and p > 3:
        return 0
    if d3:
        if p % 2 == 0:
            return (sol_k2d3_any(eval(d1), y, p + 1, k_max, d1, d2, d3)
                    or sol_k2d3_any(eval(d2), y, p + 1, k_max, d1, d2, d3)
                    or sol_k2d3_any(eval(d3), y, p + 1, k_max, d1, d2, d3)
                    or sol_k2d3_any(x, eval(d4), p + 1, k_max, d1, d2, d3)
                    or sol_k2d3_any(x, eval(d5), p + 1, k_max, d1, d2, d3)
                    or sol_k2d3_any(x, eval(d6), p + 1, k_max, d1, d2, d3)
                    )
        else:
            return (sol_k2d3_any(eval(d1), y, p + 1, k_max, d1, d2, d3)
                    and sol_k2d3_any(eval(d2), y, p + 1, k_max, d1, d2, d3)
                    and sol_k2d3_any(eval(d3), y, p + 1, k_max, d1, d2, d3)
                    and sol_k2d3_any(x, eval(d4), p + 1, k_max, d1, d2, d3)
                    and sol_k2d3_any(x, eval(d5), p + 1, k_max, d1, d2, d3)
                    and sol_k2d3_any(x, eval(d6), p + 1, k_max, d1, d2, d3)
                    )

    else:
        if p % 2 == 0:
            return (sol_k2d3_any(eval(d1), y, p + 1, k_max, d1, d2, d3)
                    or sol_k2d3_any(eval(d2), y, p + 1, k_max, d1, d2, d3)
                    or sol_k2d3_any(x, eval(d4), p + 1, k_max, d1, d2, d3)
                    or sol_k2d3_any(x, eval(d5), p + 1, k_max, d1, d2, d3)
                    )
        else:
            return (sol_k2d3_any(eval(d1), y, p + 1, k_max, d1, d2, d3)
                    and sol_k2d3_any(eval(d2), y, p + 1, k_max, d1, d2, d3)
                    and sol_k2d3_any(x, eval(d4), p + 1, k_max, d1, d2, d3)
                    and sol_k2d3_any(x, eval(d5), p + 1, k_max, d1, d2, d3)
                    )


@timer_decorator
def result_k2d3_any():
    k_start, k_max, d1, d2, d3 = 0, 0, 0, 0, 0
    conn3 = sqlite3.connect("my_database.db")
    cursor3 = conn3.cursor()
    cursor3.execute("SELECT * FROM my_table")
    row = cursor3.fetchall()[-1]
    if row is not None:
        k_start, k_max, d1, d2, d3 = row
    conn3.close()
    for i in range(100):
        if sol_k2d3(x=i, y=k_start, p=1, k_max=k_max, d1=d1, d2=d2, d3=d3):
            return i


def n20_1k(x, p, k_max, d1, d2, d3):
    if x >= k_max and p == 4:
        return 1
    if x < k_max and p == 4:
        return 0
    if x >= k_max and p < 4:
        return 0
    else:
        if d3:
            if p % 2 != 0:
                return (n20_1k(eval(d1), p + 1, k_max, d1, d2, d3) or n20_1k(eval(d2), p + 1, k_max, d1, d2, d3) or
                        n20_1k(
                            eval(d3), p + 1,
                            k_max,
                            d1, d2, d3))
            else:
                return (n20_1k(eval(d1), p + 1, k_max, d1, d2, d3) and n20_1k(eval(d2), p + 1, k_max, d1, d2, d3)
                        and n20_1k(
                            eval(d3), p + 1,
                            k_max,
                            d1, d2, d3))
        else:
            if p % 2 != 0:
                return n20_1k(eval(d1), p + 1, k_max, d1, d2, d3) or n20_1k(eval(d2), p + 1, k_max, d1, d2, d3)
            else:
                return n20_1k(eval(d1), p + 1, k_max, d1, d2, d3) and n20_1k(eval(d2), p + 1, k_max, d1, d2, d3)


@timer_decorator
def result_n20_1k():
    k_start, k_max, d1, d2, d3 = 0, 0, 0, 0, 0
    conn3 = sqlite3.connect("my_database.db")
    cursor3 = conn3.cursor()
    cursor3.execute("SELECT * FROM my_table")
    row = cursor3.fetchall()[-1]
    if row is not None:
        k_start, k_max, d1, d2, d3 = row
    conn3.close()
    ans = []
    for i in range(100):
        if n20_1k(x=i, p=1, k_max=k_max, d1=d1, d2=d2, d3=d3):
            ans.append(i)
            print(i)
    return str(ans)


def n20_2k(x, y, p, k_max, d1, d2, d3):
    d4 = f"y{d1[1:]}"
    d5 = f"y{d2[1:]}"
    d6 = f"y{d3[1:]}"
    if x + y >= k_max and p == 4:
        return 1
    elif x + y < k_max and p == 4:
        return 0
    elif x + y >= k_max and p < 4:
        return 0
    else:
        if d3:
            if p % 2 != 0:
                return (n20_2k(eval(d1), y, p + 1, k_max, d1, d2, d3)
                        or n20_2k(eval(d2), y, p + 1, k_max, d1, d2, d3)
                        or n20_2k(eval(d3), y, p + 1, k_max, d1, d2, d3)
                        or n20_2k(x, eval(d4), p + 1, k_max, d1, d2, d3)
                        or n20_2k(x, eval(d5), p + 1, k_max, d1, d2, d3)
                        or n20_2k(x, eval(d6), p + 1, k_max, d1, d2, d3)
                        )
            else:
                return (n20_2k(eval(d1), y, p + 1, k_max, d1, d2, d3)
                        and n20_2k(eval(d2), y, p + 1, k_max, d1, d2, d3)
                        and n20_2k(eval(d3), y, p + 1, k_max, d1, d2, d3)
                        and n20_2k(x, eval(d4), p + 1, k_max, d1, d2, d3)
                        and n20_2k(x, eval(d5), p + 1, k_max, d1, d2, d3)
                        and n20_2k(x, eval(d6), p + 1, k_max, d1, d2, d3)
                        )

        else:
            if p % 2 != 0:
                return (n20_2k(eval(d1), y, p + 1, k_max, d1, d2, d3)
                        or n20_2k(eval(d2), y, p + 1, k_max, d1, d2, d3)
                        or n20_2k(x, eval(d4), p + 1, k_max, d1, d2, d3)
                        or n20_2k(x, eval(d5), p + 1, k_max, d1, d2, d3)
                        )
            else:
                return (n20_2k(eval(d1), y, p + 1, k_max, d1, d2, d3)
                        and n20_2k(eval(d2), y, p + 1, k_max, d1, d2, d3)
                        and n20_2k(x, eval(d4), p + 1, k_max, d1, d2, d3)
                        and n20_2k(x, eval(d5), p + 1, k_max, d1, d2, d3)
                        )


@timer_decorator
def result_n20_2k():
    k_start, k_max, d1, d2, d3 = 0, 0, 0, 0, 0
    conn3 = sqlite3.connect("my_database.db")
    cursor3 = conn3.cursor()
    cursor3.execute("SELECT * FROM my_table")
    row = cursor3.fetchall()[-1]
    if row is not None:
        k_start, k_max, d1, d2, d3 = row
    conn3.close()
    ans = []
    for i in range(100):
        if n20_2k(x=i, y=k_start, p=1, k_max=k_max, d1=d1, d2=d2, d3=d3):
            ans.append(i)
            print('---------------------')
            print(i)
            print(ans)
    return str(ans)


def banch2(selected):
    global bunch
    if selected:
        bunch = 1


def banch1(selected):
    global bunch
    if selected:
        bunch = 0


def var_any(selected):
    global vin_var
    if selected:
        vin_var = 1


def var_lost(selected):
    global vin_var
    if selected:
        vin_var = 0


# --------------------------------------
# Графический интерфейс
class Zad19(QDialog):
    def __init__(self):
        self.third_form = None
        self.second_form = None
        global bunch
        global vin_var
        super().__init__()
        uic.loadUi('project_ui.ui', self)
        self.pushButton.clicked.connect(self.res)
        self.radioButton.toggled.connect(banch1)
        self.radioButton_2.toggled.connect(banch2)
        self.radioButton_6.toggled.connect(var_lost)
        self.radioButton_7.toggled.connect(var_any)
        self.pushButton_2.clicked.connect(self.log)
        bunch = 0
        vin_var = 0

    def res(self):
        global bunch
        d1 = self.lineEdit.text()
        d2 = self.lineEdit_2.text()
        d3 = self.lineEdit_3.text()
        k_start = self.nach.text()
        k_max = self.kon.text()
        conn1 = sqlite3.connect("my_database.db")
        cursor1 = conn1.cursor()
        cursor1.execute("REPLACE INTO my_table (k_start, k_max, d1, d2, d3) VALUES (?, ?, ?, ?, ?)",
                        (k_start, k_max, d1, d2, d3))
        conn1.commit()
        result = cursor1.execute("""select * from my_table""").fetchall()
        print(result)

        self.second_form = Results()
        self.second_form.show()

    def log(self):
        self.third_form = Logs()
        self.third_form.show()


class Zad20(QDialog):
    def __init__(self):
        self.third_form = None
        self.second_form = None
        global bunch
        super().__init__()
        uic.loadUi('zad_20.ui', self)
        self.pushButton.clicked.connect(self.res)
        self.radioButton_2.toggled.connect(banch1)
        self.radioButton_3.toggled.connect(banch2)
        self.pushButton_2.clicked.connect(self.log)
        bunch = 0

    def res(self):
        global bunch
        d1 = self.lineEdit.text()
        d2 = self.lineEdit_2.text()
        d3 = self.lineEdit_3.text()
        k_start = self.nach.text()
        k_max = self.kon.text()
        conn1 = sqlite3.connect("my_database.db")
        cursor1 = conn1.cursor()
        cursor1.execute("REPLACE INTO my_table (k_start, k_max, d1, d2, d3) VALUES (?, ?, ?, ?, ?)",
                        (k_start, k_max, d1, d2, d3))
        conn1.commit()
        result = cursor1.execute("""select * from my_table""").fetchall()
        print(result)

        self.second_form = Results()
        self.second_form.show()

    def log(self):
        self.third_form = Logs()
        self.third_form.show()


class Results(QWidget):
    def __init__(self):
        super().__init__()
        self.result_time = None
        self.result_l = None
        self.initUI()

    def initUI(self):
        global bunch
        global vin_var
        global zadanie
        self.setGeometry(300, 300, 200, 150)
        self.setWindowTitle('ответ')
        self.result_l = QLabel(self)
        self.result_time = QLabel(self)
        if zadanie == 19:
            if bunch == 0 and vin_var == 0:
                self.result_l.setText(f'ответ: {result_k1d3()}')
                self.result_l.move(50, 50)
            elif bunch == 1 and vin_var == 0:
                self.result_l.setText(f'ответ: {result_k2d3()}')
                self.result_l.move(50, 50)
            elif bunch == 0 and vin_var == 1:
                self.result_l.setText(f'ответ: {result_k1d3_any()}')
                self.result_l.move(50, 50)
            elif bunch == 1 and vin_var == 1:
                self.result_l.setText(f'ответ: {result_k2d3_any()}')
                self.result_l.move(50, 50)
        if zadanie == 20:
            if bunch == 0:
                print(0)
                self.result_l.setText(f'ответ: {result_n20_1k()}')
                self.result_l.move(50, 50)
            if bunch == 1:
                print(1)
                self.result_l.setText(f'ответ: {result_n20_2k()}')
                self.result_l.move(50, 50)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.second_form = None
        uic.loadUi('main_w.ui', self)
        self.pushButton.clicked.connect(self.run_task)

    def run_task(self):
        global zadanie
        if self.comboBox.currentText() == '19 задание егэ. Выигрышная стратегия. Задание 1':
            self.second_form = Zad19()
            self.second_form.show()
            self.hide()
            zadanie = 19

        if self.comboBox.currentText() == '20 задание егэ. Выигрышная стратегия. Задание 2':
            self.second_form = Zad20()
            self.second_form.show()
            self.hide()
            zadanie = 20


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


# --------------------------------------
# Запуск приложения

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
