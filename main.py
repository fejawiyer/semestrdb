from datetime import datetime
import sys
import re
import cx_Oracle
import logging
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QMessageBox, QVBoxLayout, \
    QScrollArea, QHBoxLayout, QDialog, QListWidget, QDateEdit, QComboBox


def is_date(string):
    pattern = r'^\d{2}\.\d{2}\.\d{2,4}$'
    return bool(re.match(pattern, string))


class App(QWidget):
    """Основной класс, в котором выполняется программа"""

    def __init__(self):
        logging.basicConfig(level=logging.INFO, filename='logs.log', filemode='w', format='%(asctime)s %(levelname)s '
                                                                                          '%(message)s')
        super().__init__()
        with open("style.css", "r") as file:
            sheet = file.read()
        self.setStyleSheet(sheet)
        file.close()

        self.setWindowTitle('Application')
        self.login_label = QLabel("Логин")
        self.login_enter = QLineEdit()
        self.password_label = QLabel("Пароль")
        self.password_enter = QLineEdit()
        self.password_enter.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton("Войти")
        self.sql_enter = QTextEdit()
        self.sql_enter.setPlaceholderText("Введите ваш SQL-запрос...")
        self.sql_ex_button = QPushButton("Выполнить")
        self.menu_button = QPushButton("Меню")
        self.logs_supplier_button = QPushButton("Логи Supplier")
        self.otchet_button = QPushButton("Отчет")
        self.logs_supplies_button = QPushButton("Логи Supplies")
        self.logs_product_button = QPushButton("Логи Product")

        self.base_create_button = QPushButton("Развернуть базу")
        self.insert_button = QPushButton("Вставить данные")
        self.update_button = QPushButton("Обновить данные")
        self.delete_button = QPushButton("Удалить данные")
        self.exit_button = QPushButton("Назад")

        self.sql_ex_res = QLabel()
        self.scrolling = QScrollArea()

        self.sql_enter.hide()
        self.sql_ex_button.hide()
        self.sql_ex_res.hide()
        self.scrolling.hide()
        self.menu_button.hide()
        self.base_create_button.hide()
        self.initUI()
        self.insert_button.hide()
        self.update_button.hide()
        self.delete_button.hide()
        self.exit_button.hide()
        self.logs_supplier_button.hide()
        self.logs_supplies_button.hide()
        self.logs_product_button.hide()
        self.otchet_button.hide()

        self.login_button.clicked.connect(self.login)
        self.sql_ex_button.clicked.connect(self.sql_ex)
        self.menu_button.clicked.connect(self.menu)
        self.base_create_button.clicked.connect(self.base_create)
        self.insert_button.clicked.connect(self.ins)
        self.update_button.clicked.connect(self.upd)
        self.delete_button.clicked.connect(self.remove)
        self.exit_button.clicked.connect(self.to_main)
        self.logs_supplier_button.clicked.connect(self.logs_supplier)
        self.logs_supplies_button.clicked.connect(self.logs_supplies)
        self.logs_product_button.clicked.connect(self.logs_product)
        self.otchet_button.clicked.connect(self.otchet)

    def initUI(self):
        """Эта функция осуществляет инициализацию UI не связанную с созданием объектов интерфейса"""
        main_layout = QVBoxLayout()
        main2_layout = QHBoxLayout()
        login_layout = QVBoxLayout()
        login_layout.addWidget(self.login_label)
        login_layout.addWidget(self.login_enter)
        password_layout = QVBoxLayout()
        password_layout.addWidget(self.password_label)
        password_layout.addWidget(self.password_enter)
        main_layout.addLayout(login_layout)
        main_layout.addLayout(password_layout)
        main_layout.addWidget(self.login_button)
        main_layout.addWidget(self.sql_enter)
        main_layout.addWidget(self.sql_ex_button)
        main_layout.addWidget(self.menu_button)
        main_layout.addWidget(self.sql_ex_res)
        main2_layout.addWidget(self.logs_supplies_button)
        main2_layout.addWidget(self.logs_product_button)
        main2_layout.addWidget(self.logs_supplier_button)
        main_layout.addLayout(main2_layout)
        main_layout.addWidget(self.otchet_button)
        main_layout.addWidget(self.scrolling)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.base_create_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.insert_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.exit_button)
        button_layout.setSpacing(10)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
        self.resize(600, 400)
        self.center_window()

    def center_window(self):
        """Эта функция центрирует окно"""
        self.frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        self.frameGm.moveCenter(centerPoint)
        self.move(self.frameGm.topLeft())
        self.show()

    def login(self):
        """Функция для логина"""
        logging.info("Try to login")
        user_login = str(self.login_enter.text())
        user_password = str(self.password_enter.text())
        logging.info(f"Login:{user_login}")
        try:
            self.connection = cx_Oracle.connect(user=user_login, password=user_password, dsn="localhost/XE")

            self.login_label.hide()
            self.password_label.hide()
            self.login_enter.hide()
            self.password_enter.hide()
            self.login_button.hide()
            self.sql_enter.show()
            self.sql_ex_button.show()
            self.menu_button.show()
            self.logs_supplier_button.show()
            self.logs_supplies_button.show()
            self.logs_product_button.show()
            self.otchet_button.show()

            self.resize(1280, 720)
            self.center_window()

        except cx_Oracle.DatabaseError as e:
            self.error_box("login", str(e))
        except Exception as e:
            self.error_box("error", str(e))
        logging.info('Login ok')

    def sql_ex(self):
        """Эта функция выполняет SQL-запрос"""
        sql_type = str(self.sql_enter.toPlainText()).lower()
        logging.info(f"SQL Query: {sql_type}")
        if sql_type.startswith("create") or sql_type.startswith("call"):  # Если запрос невозвратный
            typ = "create"
        else:  # Если запрос возвращает значение
            typ = "exec"
        with self.connection.cursor() as cursor:
            sql = self.sql_enter.toPlainText()  # Приводим в текст
            try:
                sql_res = ""
                if typ == "exec":
                    results = cursor.execute(sql).fetchall()
                    if not results:
                        sql_res = "Нет данных для отображения."
                    else:
                        sql_res += "<table style='border-collapse: collapse; width: 100%;'>"  # Создаем таблицу
                        # Первый элемент кортежа списков содержит названия столбцов
                        columns = [desc[0] for desc in cursor.description]

                        sql_res += "<tr>"  # Контейнер для строки
                        for col in columns:
                            sql_res += (f"<th style='border: 1px solid #ddd; padding: 8px; text-align: left; "
                                        f"background-color: #f4f4f9;'>{col}</th>")  # Создаем строку названий колонок
                        sql_res += "</tr>"
                        for row in results:  # И для всех строк
                            sql_res += "<tr>"
                            for value in row:
                                sql_res += f"<td style='border: 1px solid #ddd; padding: 8px;'>{value}</td>"
                            sql_res += "</tr>"
                        sql_res += "</table>"

                    self.sql_ex_res.setText(sql_res)
                    self.sql_ex_res.setTextFormat(1)  # 1 - HTML

                    # Данных бывает слишком много. Сделаем scrolling
                    self.scrolling.setWidget(self.sql_ex_res)
                    self.sql_ex_res.setAlignment(Qt.AlignTop)
                    self.sql_ex_res.setTextInteractionFlags(Qt.TextBrowserInteraction)
                    self.scrolling.setMinimumHeight(500)
                    self.scrolling.setWidgetResizable(True)

                    self.scrolling.show()
                elif typ == "create":
                    cursor.execute(sql)
                    self.error_box("ok")  # Обработка ошибок здесь не нужна, т.к. она вынесена в блок выше уровнем

            except cx_Oracle.DatabaseError as e:
                self.error_box("sqlerror", str(e))
            except Exception as e:
                self.error_box("error", str(e))
            else:
                logging.info("Success query")

    @staticmethod
    def error_box(typ, msg=None):
        """Эта функция создает message box с информацией."""
        err = QMessageBox()
        err.setWindowTitle("Ошибка")
        if typ == "login":
            err.setText(f"Неверный логин и/или пароль. {msg}")
        elif typ == "sqlerror":
            err.setText(f"Неправильный запрос. {msg}")
        elif typ == "ok":
            err.setText("Запрос выполнен")
            err.setWindowTitle("Успех")
            logging.info("Success query")
        else:
            err.setText(f"Что-то пошло не так. {msg}")
        if typ != "ok":
            logging.error(f"Something got wrong. {msg}")
        err.exec_()

    def menu(self):
        """Данная функция осуществляет переход в меню для работы с базой данных"""
        self.sql_enter.hide()
        self.sql_ex_button.hide()
        self.menu_button.hide()
        self.base_create_button.show()
        self.update_button.show()
        self.insert_button.show()
        self.delete_button.show()
        self.exit_button.show()
        self.logs_supplier_button.hide()
        self.logs_product_button.hide()
        self.logs_supplies_button.hide()
        self.scrolling.hide()
        self.otchet_button.hide()

    def to_main(self):
        """Данная функция осуществляет переход назад"""
        self.sql_enter.show()
        self.sql_ex_button.show()
        self.menu_button.show()
        self.base_create_button.hide()
        self.update_button.hide()
        self.insert_button.hide()
        self.delete_button.hide()
        self.exit_button.hide()
        self.logs_supplier_button.show()
        self.logs_supplies_button.show()
        self.logs_product_button.show()
        self.otchet_button.show()

    def base_create(self):
        """Данная функция создает базу на основе скрипта"""
        try:
            with open("generate.sql", "r", encoding="utf-8") as file:
                sql_script = file.read()
            sql_command = sql_script.split('/')
            with self.connection.cursor() as cursor:
                for command in sql_command:
                    command = command.strip()
                    logging.info(f"Try to {command}")
                    if command:
                        cursor.execute(command)
                    logging.info(f"Success")
            self.error_box("ok")

        except Exception as e:
            self.error_box("error", str(e))

    def ins(self):
        """Данная функция создает диалог для вставки значений"""
        dialog = InsertDialog(self.connection)
        if dialog.exec_() == QDialog.Accepted:
            selected_table = dialog.selected_table()
            if selected_table:
                logging.info(f"Selected table: {selected_table}")
                try:
                    insert_dialog = InsertDataDialog(self.connection, selected_table)
                    insert_dialog.exec_()
                except Exception as e:
                    self.error_box("error", str(e))
                else:
                    logging.info("Insert success")

    def upd(self):
        """Данная функция создает диалог для обновления значений"""
        dialog = UpdateDialog(self.connection)
        if dialog.exec_() == QDialog.Accepted:
            selected_table = dialog.selected_table()
            if selected_table:
                logging.info(f"Selected table: {selected_table}")
                try:
                    insert_dialog = UpdateDataDialog(self.connection, selected_table)
                    insert_dialog.exec_()
                except Exception as e:
                    self.error_box("error", str(e))
                else:
                    logging.info("Update success")

    def remove(self):
        """Данная функция создает диалог для удаления строк (по id)"""
        dialog = DeleteDialog(self.connection)
        if dialog.exec_() == QDialog.Accepted:
            selected_table = dialog.selected_table()
            if selected_table:
                logging.info(f"Selected table: {selected_table}")
                try:
                    insert_dialog = DeleteDataDialog(self.connection, selected_table)
                    insert_dialog.exec_()
                except Exception as e:
                    self.error_box("error", str(e))
                else:
                    logging.info("Delete success")

    def enable_dbms_output(self):
        cursor = self.connection.cursor()
        cursor.execute("BEGIN DBMS_OUTPUT.ENABLE(NULL); END;")
        cursor.close()

    def logs_supplier(self):
        self.show_log_filter_dialog("supplier")

    def logs_product(self):
        self.show_log_filter_dialog("product")

    def logs_supplies(self):
        self.show_log_filter_dialog("supplies")

    def show_log_filter_dialog(self, log_type):
        dialog = LogFilterDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            start_date, end_date, operation_type = dialog.get_filters()
            if log_type == "supplier":
                self.fetch_logs('get_supplier_logs', start_date, end_date, operation_type)
            elif log_type == "product":
                self.fetch_logs('get_product_logs', start_date, end_date, operation_type)
            elif log_type == "supplies":
                self.fetch_logs('get_supplies_logs', start_date, end_date, operation_type)


    def fetch_logs(self, procedure_name, start_date, end_date, operation_type):
        try:
            self.enable_dbms_output()

            p_start_time = datetime.strptime(start_date, "%Y-%m-%d")
            p_end_time = datetime.strptime(end_date, "%Y-%m-%d")

            cursor = self.connection.cursor()

            cursor.callproc(procedure_name, [p_start_time, p_end_time, operation_type])
            chunk_size = 1000

            lines_var = cursor.arrayvar(str, chunk_size)  # Массив для хранения строк
            num_lines_var = cursor.var(int)  # Переменная для хранения количества строк
            num_lines_var.setvalue(0, chunk_size)  # Инициализируем количество строк для получения

            all_logs = []  # Список для хранения всех логов

            while True:
                cursor.callproc("dbms_output.get_lines", (lines_var, num_lines_var))
                num_lines = num_lines_var.getvalue()
                lines = lines_var.getvalue()[:num_lines]

                all_logs.extend([line for line in lines if line])

                # Если строк меньше, чем размер блока, значит мы получили все строки
                if num_lines < chunk_size:
                    break

            # Отображение логов в таблице
            if all_logs:
                logs_data = "<table style='border-collapse: collapse; width: 100%;'>"

                logs_data += "<tr>"
                logs_data += "<th style='border: 1px solid #ddd; padding: 8px; text-align: left; background-color: #f4f4f9;'>Лог</th>"
                logs_data += "</tr>"

                for line in all_logs:
                    logs_data += "<tr>"
                    logs_data += f"<td style='border: 1px solid #ddd; padding: 8px;'>{line}</td>"
                    logs_data += "</tr>"

                logs_data += "</table>"
                self.sql_ex_res.setText(logs_data)
                self.sql_ex_res.setTextFormat(1)  # 1 - HTML

                # Данных бывает слишком много. Сделаем scrolling
                self.scrolling.setWidget(self.sql_ex_res)
                self.sql_ex_res.setAlignment(Qt.AlignTop)
                self.sql_ex_res.setTextInteractionFlags(Qt.TextBrowserInteraction)
                self.scrolling.setMinimumHeight(500)
                self.scrolling.setWidgetResizable(True)
                self.scrolling.show()
            else:
                self.sql_ex_res.setText("Нет данных для отображения.")

            cursor.close()

        except cx_Oracle.DatabaseError as e:
            self.error_box("sqlerror", str(e))
        except Exception as e:
            self.error_box("error", str(e))

    def otchet(self):
        dialog = OtchetFilterDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            flag1, flag2, flag3 = dialog.get_filters()
            self.fetch_otchet(bool(flag1), bool(flag2), bool(flag3))

    def fetch_otchet(self, flag1, flag2, flag3):
        try:
            self.enable_dbms_output()
            cursor = self.connection.cursor()
            cursor.callproc("generate_summary_report", [flag1, flag2, flag3])
            chunk_size = 1000

            lines_var = cursor.arrayvar(str, chunk_size)  # Массив для хранения строк
            num_lines_var = cursor.var(int)  # Переменная для хранения количества строк
            num_lines_var.setvalue(0, chunk_size)  # Инициализируем количество строк для получения

            all_logs = []

            while True:
                cursor.callproc("dbms_output.get_lines", (lines_var, num_lines_var))
                num_lines = num_lines_var.getvalue()
                lines = lines_var.getvalue()[:num_lines]

                all_logs.extend([line for line in lines if line])

                # Если строк меньше, чем размер блока, значит мы получили все строки
                if num_lines < chunk_size:
                    break

            if all_logs:
                logs_data = "<table style='border-collapse: collapse; width: 100%;'>"

                logs_data += "<tr>"
                logs_data += "<th style='border: 1px solid #ddd; padding: 8px; text-align: left; background-color: #f4f4f9;'>Лог</th>"
                logs_data += "</tr>"

                for line in all_logs:
                    logs_data += "<tr>"
                    logs_data += f"<td style='border: 1px solid #ddd; padding: 8px;'>{line}</td>"
                    logs_data += "</tr>"

                logs_data += "</table>"
                self.sql_ex_res.setText(logs_data)
                self.sql_ex_res.setTextFormat(1)  # 1 - HTML

                # Данных бывает слишком много. Сделаем scrolling
                self.scrolling.setWidget(self.sql_ex_res)
                self.sql_ex_res.setAlignment(Qt.AlignTop)
                self.sql_ex_res.setTextInteractionFlags(Qt.TextBrowserInteraction)
                self.scrolling.setMinimumHeight(500)
                self.scrolling.setWidgetResizable(True)
                self.scrolling.show()
            else:
                self.sql_ex_res.setText("Нет данных для отображения.")

            cursor.close()

        except cx_Oracle.DatabaseError as e:
            self.error_box("sqlerror", str(e))
        except Exception as e:
            self.error_box("error", str(e))


class UpdateDialog(QDialog):
    """Данный класс используется для создания диалоговог окна для выбора таблицы для вставки"""

    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.setWindowTitle("Выбор таблицы для обновления")
        self.setFixedSize(300, 400)

        layout = QVBoxLayout()

        self.label = QLabel("Выберите таблицу для обновления:")
        layout.addWidget(self.label)

        self.table_list = QListWidget()
        layout.addWidget(self.table_list)

        self.load_tables()

        self.buttons_layout = QHBoxLayout()
        self.cancel_button = QPushButton("Отмена")
        self.ok_button = QPushButton("Ок")
        self.buttons_layout.addWidget(self.cancel_button)
        self.buttons_layout.addWidget(self.ok_button)
        layout.addLayout(self.buttons_layout)

        self.cancel_button.clicked.connect(self.reject)
        self.ok_button.clicked.connect(self.accept)

        self.setLayout(layout)

    def load_tables(self):
        """Данная функция добавляет в список таблиц все необходимые таблицы"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT table_name FROM user_tables where lower(table_name) = 'supplier' or lower("
                               "table_name) = 'supplies' or lower(table_name) = 'product'")
                tables = cursor.fetchall()

                for table in tables:
                    self.table_list.addItem(table[0])

        except cx_Oracle.DatabaseError as e:
            App.error_box("sqlerror", str(e))
        except Exception as e:
            App.error_box("error", str(e))

    def selected_table(self):
        """Данная функция возвращает обратно список выбранную таблицу"""
        selected_items = self.table_list.selectedItems()
        if selected_items:
            return selected_items[0].text()
        else:
            logging.warning("Selected items is None")
        return None


class UpdateDataDialog(QDialog):
    """Данный класс используется для создания диалогового окна для обновления"""

    def __init__(self, connection, table_name):
        super().__init__()
        self.connection = connection
        self.table_name = table_name
        self.setWindowTitle(f"Обновление данных в таблице {self.table_name}")
        self.setFixedSize(400, 500)

        self.layout = QVBoxLayout()

        self.label = QLabel(f"Обновление происходит по ID.\nВведите данные для таблицы {self.table_name}:")
        self.layout.addWidget(self.label)

        self.input_fields = []

        self.load_table_structure()

        self.buttons_layout = QHBoxLayout()
        self.cancel_button = QPushButton("Отмена")
        self.ok_button = QPushButton("Ок")
        self.buttons_layout.addWidget(self.cancel_button)
        self.buttons_layout.addWidget(self.ok_button)
        self.layout.addLayout(self.buttons_layout)

        self.cancel_button.clicked.connect(self.reject)
        self.ok_button.clicked.connect(self.insert_data)

        self.setLayout(self.layout)

    def load_table_structure(self):
        """Данная функция добавляет все столбцы в layout"""
        logging.info("Try to load table struct")
        try:
            with self.connection.cursor() as cursor:
                logging.info(f"Describe {self.table_name}")

                # К сожалению, describe недоступен за пределами SQL+
                cursor.execute(f"select column_name, data_type from all_tab_columns "
                               f"where table_name = '{self.table_name}'")
                columns = cursor.fetchall()
                logging.info(f"Got columns:{columns}")
                for column in columns:
                    col_name = column[0]
                    col_type = column[1]

                    if col_name == "" or col_type == "":
                        logging.warning("Null col_name or col_type !")

                    label = QLabel(f"{col_name} ({col_type})")
                    line_edit = QLineEdit()
                    line_edit.setPlaceholderText(f"Введите значение для {col_name}")

                    self.input_fields.append((col_name, line_edit))
                    self.layout.addWidget(label)
                    self.layout.addWidget(line_edit)

        except cx_Oracle.DatabaseError as e:
            App.error_box("sqlerror", str(e))
        except Exception as e:
            App.error_box("error", str(e))

    def insert_data(self):
        """В данной функции обновлюятся данные в таблице"""
        values = []
        for col_name, line_edit in self.input_fields:
            value = line_edit.text().strip()
            values.append(value)
        procedure_name = f"update_{self.table_name.lower()}"
        insert_sql = f"call {procedure_name}("
        for i in range(len(values)):
            if is_date(values[i]):
                insert_sql += 'to_date(\'' + values[i] + '\'), '
            elif str(values[i])[0].isdigit():
                insert_sql += values[i] + ', '
            else:
                insert_sql += '\'' + values[i] + '\', '
        insert_sql = insert_sql[:-2]
        insert_sql += ')'

        logging.info(f"Try to {insert_sql}")
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(insert_sql)
                self.connection.commit()
            App.error_box("ok")
            self.accept()  # Закрываем диалог
        except cx_Oracle.DatabaseError as e:
            App.error_box("sqlerror", str(e))
        except Exception as e:
            App.error_box("error", str(e))


class DeleteDialog(QDialog):
    """Данный класс используется для создания диалоговог окна для выбора таблицы для удаления"""

    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.setWindowTitle("Выбор таблицы для удаления")
        self.setFixedSize(300, 400)

        layout = QVBoxLayout()

        self.label = QLabel("Выберите таблицу для удаления:")
        layout.addWidget(self.label)

        self.table_list = QListWidget()
        layout.addWidget(self.table_list)

        self.load_tables()

        self.buttons_layout = QHBoxLayout()
        self.cancel_button = QPushButton("Отмена")
        self.ok_button = QPushButton("Ок")
        self.buttons_layout.addWidget(self.cancel_button)
        self.buttons_layout.addWidget(self.ok_button)
        layout.addLayout(self.buttons_layout)

        self.cancel_button.clicked.connect(self.reject)
        self.ok_button.clicked.connect(self.accept)

        self.setLayout(layout)

    def load_tables(self):
        """Данная функция добавляет в список таблиц все необходимые таблицы"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT table_name FROM user_tables where lower(table_name) = 'supplier' or lower("
                               "table_name) = 'supplies' or lower(table_name) = 'product'")
                tables = cursor.fetchall()

                for table in tables:
                    self.table_list.addItem(table[0])

        except cx_Oracle.DatabaseError as e:
            App.error_box("sqlerror", str(e))
        except Exception as e:
            App.error_box("error", str(e))

    def selected_table(self):
        """Данная функция возвращает обратно список выбранную таблицу"""
        selected_items = self.table_list.selectedItems()
        if selected_items:
            return selected_items[0].text()
        else:
            logging.warning("Selected items is None")
        return None


class DeleteDataDialog(QDialog):
    """Данный класс используется для создания диалогового окна для удаления"""

    def __init__(self, connection, table_name):
        super().__init__()
        self.connection = connection
        self.table_name = table_name
        self.setWindowTitle(f"Удаление данных в таблице {self.table_name}")
        self.setFixedSize(400, 500)

        self.layout = QVBoxLayout()

        self.label = QLabel(f"Удаление происходит по ID.\nВведите данные для таблицы {self.table_name}:")
        self.layout.addWidget(self.label)

        self.input_fields = []

        self.load_table_structure()

        self.buttons_layout = QHBoxLayout()
        self.cancel_button = QPushButton("Отмена")
        self.ok_button = QPushButton("Ок")
        self.buttons_layout.addWidget(self.cancel_button)
        self.buttons_layout.addWidget(self.ok_button)
        self.layout.addLayout(self.buttons_layout)

        self.cancel_button.clicked.connect(self.reject)
        self.ok_button.clicked.connect(self.insert_data)

        self.setLayout(self.layout)

    def load_table_structure(self):
        """Данная функция добавляет все столбцы в layout"""
        logging.info("Try to load table struct")
        try:
            with self.connection.cursor() as cursor:
                logging.info(f"Describe {self.table_name}")

                # К сожалению, describe недоступен за пределами SQL+
                cursor.execute(f"select column_name, data_type from all_tab_columns "
                               f"where table_name = '{self.table_name}'")
                columns = cursor.fetchall()
                logging.info(f"Got columns:{columns}")
                for column in columns:
                    col_name = column[0]
                    col_type = column[1]
                    if col_name.lower() == "id":
                        label = QLabel(f"{col_name} ({col_type})")
                        line_edit = QLineEdit()
                        line_edit.setPlaceholderText(f"Введите значение для {col_name}")

                        self.input_fields.append((col_name, line_edit))
                        self.layout.addWidget(label)
                        self.layout.addWidget(line_edit)
                        break


        except cx_Oracle.DatabaseError as e:
            App.error_box("sqlerror", str(e))
        except Exception as e:
            App.error_box("error", str(e))

    def insert_data(self):
        """В данной функции удаляются данные из таблицы"""
        values = []
        for col_name, line_edit in self.input_fields:
            value = line_edit.text().strip()
            values.append(value)
        procedure_name = f"delete_from_{self.table_name.lower()}"
        insert_sql = f"call {procedure_name}({values[0]})"

        logging.info(f"Try to {insert_sql}")
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(insert_sql)
                self.connection.commit()
            App.error_box("ok")
            self.accept()  # Закрываем диалог
        except cx_Oracle.DatabaseError as e:
            App.error_box("sqlerror", str(e))
        except Exception as e:
            App.error_box("error", str(e))


class InsertDialog(QDialog):
    """Данный класс используется для создания диалоговог окна для выбора таблицы для вставки"""

    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.setWindowTitle("Выбор таблицы для вставки")
        self.setFixedSize(300, 400)

        layout = QVBoxLayout()

        self.label = QLabel("Выберите таблицу для вставки:")
        layout.addWidget(self.label)

        self.table_list = QListWidget()
        layout.addWidget(self.table_list)

        self.load_tables()

        self.buttons_layout = QHBoxLayout()
        self.cancel_button = QPushButton("Отмена")
        self.ok_button = QPushButton("Ок")
        self.buttons_layout.addWidget(self.cancel_button)
        self.buttons_layout.addWidget(self.ok_button)
        layout.addLayout(self.buttons_layout)

        self.cancel_button.clicked.connect(self.reject)
        self.ok_button.clicked.connect(self.accept)

        self.setLayout(layout)

    def load_tables(self):
        """Данная функция добавляет в список таблиц все необходимые таблицы"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT table_name FROM user_tables where lower(table_name) = 'supplier' or lower("
                               "table_name) = 'supplies' or lower(table_name) = 'product'")
                tables = cursor.fetchall()

                for table in tables:
                    self.table_list.addItem(table[0])

        except cx_Oracle.DatabaseError as e:
            App.error_box("sqlerror", str(e))
        except Exception as e:
            App.error_box("error", str(e))

    def selected_table(self):
        """Данная функция возвращает обратно список выбранную таблицу"""
        selected_items = self.table_list.selectedItems()
        if selected_items:
            return selected_items[0].text()
        else:
            logging.warning("Selected items is None")
        return None


class InsertDataDialog(QDialog):
    """Данный класс используется для создания диалогового окна для заполнения столбцов, которые пользователь
    будет вставлять в таблицу"""

    def __init__(self, connection, table_name):
        super().__init__()
        self.connection = connection
        self.table_name = table_name
        self.setWindowTitle(f"Вставка данных в таблицу {self.table_name}")
        self.setFixedSize(400, 500)

        self.layout = QVBoxLayout()

        self.label = QLabel(f"Введите данные для таблицы {self.table_name}:")
        self.layout.addWidget(self.label)

        self.input_fields = []

        self.load_table_structure()

        self.buttons_layout = QHBoxLayout()
        self.cancel_button = QPushButton("Отмена")
        self.ok_button = QPushButton("Ок")
        self.buttons_layout.addWidget(self.cancel_button)
        self.buttons_layout.addWidget(self.ok_button)
        self.layout.addLayout(self.buttons_layout)

        self.cancel_button.clicked.connect(self.reject)
        self.ok_button.clicked.connect(self.insert_data)

        self.setLayout(self.layout)

    def load_table_structure(self):
        """Данная функция добавляет все столбцы в layout"""
        logging.info("Try to load table struct")
        try:
            with self.connection.cursor() as cursor:
                logging.info(f"Describe {self.table_name}")

                # К сожалению, describe недоступен за пределами SQL+
                cursor.execute(f"select column_name, data_type from all_tab_columns "
                               f"where table_name = '{self.table_name}'")
                columns = cursor.fetchall()
                logging.info(f"Got columns:{columns}")
                for column in columns:
                    col_name = column[0]
                    col_type = column[1]

                    if col_name == "" or col_type == "":
                        logging.warning("Null col_name or col_type !")

                    label = QLabel(f"{col_name} ({col_type})")
                    line_edit = QLineEdit()
                    line_edit.setPlaceholderText(f"Введите значение для {col_name}")

                    self.input_fields.append((col_name, line_edit))
                    self.layout.addWidget(label)
                    self.layout.addWidget(line_edit)

        except cx_Oracle.DatabaseError as e:
            App.error_box("sqlerror", str(e))
        except Exception as e:
            App.error_box("error", str(e))

    def insert_data(self):
        """В данной функции вставляются данные в таблицу"""
        values = []
        for col_name, line_edit in self.input_fields:
            value = line_edit.text().strip()
            values.append(value)
        procedure_name = f"insert_{self.table_name.lower()}"
        insert_sql = f"call {procedure_name}("
        for i in range(len(values)):
            if is_date(values[i]):
                insert_sql += 'to_date(\'' + values[i] + '\'), '
            elif str(values[i])[0].isdigit():
                insert_sql += values[i] + ', '
            else:
                insert_sql += '\'' + values[i] + '\', '
        insert_sql = insert_sql[:-2]
        insert_sql += ')'

        logging.info(f"Try to {insert_sql}")
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(insert_sql)
                self.connection.commit()
            App.error_box("ok")
            self.accept()  # Закрываем диалог
        except cx_Oracle.DatabaseError as e:
            App.error_box("sqlerror", str(e))
        except Exception as e:
            App.error_box("error", str(e))


class LogFilterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Фильтрация логов")

        self.start_date_label = QLabel("Начальная дата:")
        self.start_date_edit = QDateEdit(self)
        self.start_date_edit.setDate(QDate.currentDate())

        self.end_date_label = QLabel("Конечная дата:")
        self.end_date_edit = QDateEdit(self)
        self.end_date_edit.setDate(QDate.currentDate())

        self.operation_label = QLabel("Тип операции:")
        self.operation_combo = QComboBox(self)
        self.operation_combo.addItems(["INSERT", "UPDATE", "DELETE"])

        self.ok_button = QPushButton("ОК", self)
        self.cancel_button = QPushButton("Отмена", self)

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        layout = QVBoxLayout()
        layout.addWidget(self.start_date_label)
        layout.addWidget(self.start_date_edit)
        layout.addWidget(self.end_date_label)
        layout.addWidget(self.end_date_edit)
        layout.addWidget(self.operation_label)
        layout.addWidget(self.operation_combo)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)
        self.resize(300, 200)

    def get_filters(self):
        """Возвращает выбранные параметры"""
        return self.start_date_edit.date().toString("yyyy-MM-dd"), \
               self.end_date_edit.date().toString("yyyy-MM-dd"), \
               self.operation_combo.currentText()


class OtchetFilterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Фильтрация логов")

        self.sort_1 = QLabel("Сортировка по сущности:")
        self.sort_1_line = QLineEdit(self)

        self.sort_2 = QLabel("Сортировка по типу операции:")
        self.sort_2_line = QLineEdit(self)

        self.sort_3 = QLabel("Сортировка по количеству операции:")
        self.sort_3_line = QLineEdit(self)

        self.ok_button = QPushButton("ОК", self)
        self.cancel_button = QPushButton("Отмена", self)

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        layout = QVBoxLayout()
        layout.addWidget(self.sort_1)
        layout.addWidget(self.sort_1_line)
        layout.addWidget(self.sort_2)
        layout.addWidget(self.sort_2_line)
        layout.addWidget(self.sort_3)
        layout.addWidget(self.sort_3_line)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)
        self.resize(300, 200)

    def get_filters(self):
        """Возвращает выбранные параметры"""
        return self.sort_1_line.text(), self.sort_2_line.text(), self.sort_3_line.text()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
