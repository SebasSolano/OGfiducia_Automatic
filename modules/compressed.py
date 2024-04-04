from pylovepdf.ilovepdf import ILovePdf
import os
from modules.getKEY import read_variable_from_env
from tkinter import messagebox


def compress_pdf(console_text, tk):
    input_file = "download/SOPORTE PLANILLA X.pdf"

    if not os.path.exists(input_file):
        messagebox.showinfo(("ERROR"),"No files found in the output directory. Exiting function.")
        return False
    else:
        PUBLIC_KEY = read_variable_from_env("PUBLIC_KEY")
        

        ilovepdf = ILovePdf(PUBLIC_KEY, verify_ssl=True)
        task = ilovepdf.new_task('compress')
        task.add_file(input_file)
        task.set_output_folder("save")
        console_text.config(state=tk.NORMAL)
        console_text.insert(tk.END, f"Upload file...\n")
        console_text.config(state=tk.DISABLED)
        console_text.see(tk.END)
        task.execute()
 
        console_text.config(state=tk.NORMAL)
        console_text.insert(tk.END, f"Download File...\n")
        console_text.config(state=tk.DISABLED)
        console_text.see(tk.END)
        task.download()
        task.delete_current_task()
        os.remove(input_file)
        return True

