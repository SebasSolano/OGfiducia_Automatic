import os
from PyPDF2 import PdfMerger
from PyQt6.QtWidgets import QMessageBox

def merge_and_delete(console_text):
    directory = "download"
    pdf_files = [file for file in os.listdir(directory) if file.endswith('.pdf')]

    if len(pdf_files) <= 1:
        QMessageBox.information(None, "ERROR", "There are not enough PDF files in the directory to merge.")
        return False
    else:
        pdf_files.sort(key=lambda x: int(x.split('-')[-1].split('.')[0]))
        merger = PdfMerger()

        for file in pdf_files:
            full_path = os.path.join(directory, file)
            with open(full_path, 'rb') as pdf_file:
                merger.append(pdf_file)

        new_output_file = os.path.join(directory, "SOPORTE PLANILLA X.pdf")

        with open(new_output_file, 'wb') as output:
            merger.write(output)
        console_text.append(f"SOPORTE PLANILLA X created")
        for file in pdf_files:
            full_path = os.path.join(directory, file)
            try:
                if file != "SOPORTE PLANILLA X.pdf":
                    os.remove(full_path)
                    print(f"Deleted file: {file}")
            except PermissionError as e:
                print("Could not delete the file:", full_path, "Error:", e)
                console_text.append(f"Error deleting file: {full_path}, Error: {e}")
            else:
                print(f"Deleted file: {file}")
            console_text.append(f"Files deleted")
        return True