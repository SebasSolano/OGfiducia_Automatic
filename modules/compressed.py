from pylovepdf.ilovepdf import ILovePdf
import os
from modules.getKEY import read_variable_from_env
from PyQt6.QtWidgets import QMessageBox

def compress_pdf(console_text, progress_signal=None):
    input_file = "download/SOPORTE PLANILLA X.pdf"

    if not os.path.exists(input_file):
        QMessageBox.information(None, "ERROR", "No files found in the output directory. Exiting function.")
        return False
    else:
        if progress_signal:
            progress_signal.emit(40)
            console_text.append("Checking API...")
            PUBLIC_KEY = read_variable_from_env("PUBLIC_KEY")
            ilovepdf = ILovePdf(PUBLIC_KEY, verify_ssl=True)
        
        if progress_signal:
            progress_signal.emit(50)
            console_text.append("Creating task...")# 
            task = ilovepdf.new_task('compress')
            
        
        if progress_signal:
            progress_signal.emit(60)
            console_text.append("Upload file...")
            task.add_file(input_file)
            task.set_output_folder("save")
            task.execute()

        
        if progress_signal:
            progress_signal.emit(80)  
            console_text.append("Download File...")
            task.download()
            task.delete_current_task()
        os.remove(input_file)
        return True