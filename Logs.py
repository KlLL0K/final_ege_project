import sqlite3

from PyQt5.QtWidgets import QWidget, QLabel


class Logs(QWidget):
    def __init__(self):
        super().__init__()
        self.constant = None
        self.result_time = None
        self.result_l = None
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 500, 150)
        self.setWindowTitle('история')
        self.result_l = QLabel(self)
        self.result_time = QLabel(self)
        self.constant = QLabel(self)
        conn1 = sqlite3.connect("my_database.db")
        cursor1 = conn1.cursor()
        result = cursor1.execute("""select * from result_table""").fetchall()[-1]
        conn1.close()
        conn1 = sqlite3.connect("my_database.db")
        cursor1 = conn1.cursor()
        const = cursor1.execute("""select * from my_table""").fetchall()[-1]
        conn1.close()
        self.constant.setText(f"Входные данные:{const}")
        self.constant.move(10, 10)
        self.result_l.setText(f'дата и время решения: {result[0]}')
        self.result_l.move(10, 50)
        self.result_time.setText(f'время выполнения кода: {str(result[1])[:8:]}')
        self.result_time.move(10, 90)
