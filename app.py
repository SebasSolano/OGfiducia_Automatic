from PyQt6.QtWidgets import QDockWidget, QApplication, QMessageBox, QMainWindow, QInputDialog, QListWidget, QListWidgetItem, QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QProgressBar, QMenuBar
from PyQt6.QtCore import QTimer, QThread, pyqtSignal
from PyQt6.QtGui import QAction, QPalette, QColor, QIcon
import os
from modules.combined import merge_and_delete
from modules.compressed import compress_pdf
from modules.getKEY import read_variable_from_env, write_variable_to_env
from PyQt6.QtCore import Qt


class CompressThread(QThread):
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal(bool)

    def __init__(self, console_text_widget):
        super().__init__()
        self.console_text_widget = console_text_widget

    def run(self):
        success = compress_pdf(self.console_text_widget, self.progress_signal)
        self.finished_signal.emit(success)


def show(self):
    if (read_variable_from_env("INTRODUCTION") == "True"):
        introduction_text = """
            Introducción:

            Para poder utilizar la herramienta, primero debes descargar todos los archivos necesarios y guardarlos en la carpeta "download" de la herramienta. A continuación, haz clic en el botón "COMPRESS", espera y, por último, ingresa el número de la planilla. Al final, este se guardará en la carpeta "save".

            Paso 1:

            - Descarga primero la planilla y asigna un número o una letra, por ejemplo: 1. Asegúrate de que al guardar, esté en la carpeta "download".

            Paso 2:

            - Descarga todos los archivos siguiendo una secuencia 2, 3, 4, 5, es decir, 
            el pdf OG, OP, Planilla, RUT, etc., deben tener una secuencia de números. Recuerda que tu primer número es la planilla original.

            Paso 3: 

            - Una vez que tengas todos los archivos necesarios en la carpeta "download", haz clic en el botón "COMPRESS" y espera.

            Paso 4:

            - Agrega el nombre de la planilla, por ejemplo: 148, y busca este archivo en la carpeta "save".
            """

        result = QMessageBox.information(
            self, "Introduccion", introduction_text)
        if result:
            write_variable_to_env("INTRODUCTION", "False")
            if (read_variable_from_env("UPDATE") == "True"):
                update_text = """
                    Esta es la versión 2.5.5

                    - Nuevo motor de IU.
                    - Nuevo estilo de la aplicación.
                    - Mejor rendimiento, más rápido.
                    - Ahora las consultas para comprimir se hacen en segundo plano, esto hace que se visualice mejor la consola.
                    - Se agregó una barra de progreso para verificar cómo va la compresión.
                    - Se agregó una lista a la derecha para ver los archivos de la carpeta download.
                    - Cuando se termine la compresión se te abrirá la carpeta save.
                    - Se optimizó la construcción de la aplicación.
                    """
                QMessageBox.information(self, "Actualizacion", update_text)
                write_variable_to_env("UPDATE", "False")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OG AUTOMATIC")
        self.setGeometry(100, 100, 400, 300)
        self.setFixedSize(500, 400)

        icon = QIcon("icon.ico")
        self.setWindowIcon(icon)

        self.initUI()
        self.initUpdateTimer()

        # Centrar la ventana en la pantalla
        screen = QApplication.primaryScreen()
        screen_size = screen.size()
        window_size = self.size()
        x = int((screen_size.width() - window_size.width()) / 2)
        y = int((screen_size.height() - window_size.height()) / 2)
        self.move(x, y)
        self.validate_folders(self)
        show(self)

    def initUI(self):
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.side_menu = QDockWidget("Files in Download: ", self)
        self.side_menu.setFeatures(
            QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.side_menu.setFloating(False)
        self.side_menu.setFixedWidth(150)
        self.addDockWidget(
            Qt.DockWidgetArea.RightDockWidgetArea, self.side_menu)

        self.side_menu_list = QListWidget()
        self.side_menu.setWidget(self.side_menu_list)

        self.label = QLabel("OG AUTOMATIC", self)
        self.label.setStyleSheet(
            "font-size: 20px; font-weight: bold; color: white;")
        layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.compress_button = QPushButton("COMPRESS", self)
        icon = QIcon("ico_b.svg")
        self.compress_button.setIcon(icon)
        self.compress_button.setStyleSheet(
            "QPushButton {"
            "background-color: #3E98FE;"
            "color: white;"
            "font-size: 14px;"
            "border: none;"
            "border-radius: 10px;"
            "padding: 10px 20px;"
            "}"
            "QPushButton:pressed {"
            "background-color: #005f5f;"
            "}"
            "QPushButton:hover {"
            "background-color: #6AAFFE;"
            "}"
        )
        self.compress_button.setToolTip("Click to compress PDF files")
        self.compress_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.compress_button.clicked.connect(self.compress)
        layout.addWidget(self.compress_button)

        self.console_text = QTextEdit(self)
        self.console_text.setReadOnly(True)
        self.console_text.setStyleSheet(
            "background-color: #333; color: white; font-family: 'Montserrat', sans-serif;")
        layout.addWidget(self.console_text)

        self.progress_bar = QProgressBar(self)
        layout.addWidget(self.progress_bar)
        self.progress_bar.setVisible(False)

        self.file_count_label = QLabel("", self)
        layout.addWidget(self.file_count_label)

        self.label_author = QLabel("By Sebastian Solano", self)
        self.label_author.setStyleSheet("color: white;")
        layout.addWidget(self.label_author)

        centralWidget.setLayout(layout)
        self.update_file_count()
        QTimer.singleShot(5000, self.update_file_count)
        QTimer.singleShot(2000, self.update_menu)

        self.initMenuBar()
        

    def initMenuBar(self):
        menuBar = QMenuBar(self)
        self.setMenuBar(menuBar)

        fileMenu = menuBar.addMenu("&Options")

        exitAction = QAction("&Exit", self)
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(exitAction)

    def update_menu(self):
        self.side_menu_list.clear()
        files = os.listdir("download")
        for file in files:
            item = QListWidgetItem(file)
            self.side_menu_list.addItem(item)

    def initUpdateTimer(self):
        self.updateTimer = QTimer(self)
        self.updateTimer.setInterval(1000)
        self.updateTimer.timeout.connect(self.update_file_count)
        self.updateTimer.timeout.connect(self.update_menu)
        self.updateTimer.start()

    def rename_files_in_output_folder(self, output_file):
        new_file_name, ok = QInputDialog.getText(
            self, "NUMBER", "Enter the form number e.g. 120")
        if ok and new_file_name:
            files = os.listdir(output_file)
            for file in files:
                if file.endswith('.pdf'):
                    new_name = os.path.join(
                        output_file, "SOPORTE PLANILLA "+new_file_name+'.pdf')
                    try:
                        os.rename(os.path.join(output_file, file), new_name)
                        print(f"File {file} renamed to "+new_file_name+'.pdf')
                    except FileExistsError:
                        print(f"File {new_name} already exists, skipping...")
        else:
            self.rename_files_in_output_folder(output_file)

    def update_file_count(self):
        download_folder = "download"
        file_count = len([name for name in os.listdir(
            download_folder) if os.path.isfile(os.path.join(download_folder, name))])
        self.file_count_label.setText(
            f"Number of files in 'download': {file_count}")

    def compress(self):
        self.compress_button.setEnabled(False)
        self.validate_folders()
        self.console_text.clear()
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        if (merge_and_delete(self.console_text)):
            self.progress_bar.setValue(30)
            self.compress_thread = CompressThread(self.console_text)
            self.compress_thread.progress_signal.connect(
                self.progress_bar.setValue)
            self.compress_thread.finished_signal.connect(
                self.on_compression_finished)
            self.compress_thread.start()
        else:
            self.progress_bar.setVisible(False)

    def on_compression_finished(self, success):
        if success:
            self.rename_files_in_output_folder("save")
            self.console_text.append("Compression completed.")
            self.progress_bar.setValue(100)
            self.compress_button.setEnabled(True)
            self.open_specific_folder("save")
        self.update_file_count()
        self.progress_bar.setVisible(False)

    def check_and_create_folder(self, folder_name):
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

    def validate_folders(self):
        self.check_and_create_folder("download")
        self.check_and_create_folder("save")

    def open_specific_folder(self, folder_name):
        os.startfile(folder_name)


if __name__ == "__main__":
    app = QApplication([])
    app.setStyle("Fusion")  # Set the application style to Fusion
    # Set the application palette to dark
    app.setPalette(QPalette(QColor("#333333"), QColor("#333333")))
    window = MainWindow()
    window.show()
    app.exec()
