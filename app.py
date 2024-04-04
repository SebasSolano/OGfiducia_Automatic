import tkinter as tk
from modules.combined import merge_and_delete
from modules.compressed import compress_pdf
import os
from tkinter import simpledialog
from tkinter import messagebox
from modules.getKEY import read_variable_from_env, write_variable_to_env




def rename_files_in_output_folder(output_file):

    new_file_name = simpledialog.askstring("NUMBER", "Enter the form number e.g. 120")
    files = os.listdir(output_file)
    for file in files:
        if file.endswith('.pdf'):
            new_name = os.path.join(output_file, "SOPORTE PLANILLA "+new_file_name+'.pdf')
            os.rename(os.path.join(output_file, file), new_name)
            print(f"File {file} renamed to "+new_file_name+'.pdf')

    
def int_and_update(window):
    if (read_variable_from_env("INTRODUCTION") == "True"):
        introduction_text = """
        Introduccion:

        Para poder utilizar la herramienta primero debes descargar todos los archivos necesarios y guardarlos en la carpeta download de los archivos de la herramienta. A continuacion darle al boton de COMPRESS, esperar y por ultimo poner el numerod e la planilla. Al final esta se guardara en la carpeta save.

        Paso 1:

        - Debes descargar primero la planilla, ponerle un numero o una letra por ejemplo: 1. Se debe saber que este al guardar debe estar en download.

        Paso 2:

        - Descarga todos los archivos teniendo una secuencia 2, 3, 4, 5, es decir, 
        el pdf OG, OP, Planilla, RUT etc deben tener una secuencia de numeros. recuerda que tu primer numero es la planilla original.

        Paso 3: 

        - Al tener todos los archivos necesarios en download, dale al boton de COMPRESS y espera.

        Paso 4:

        - Agrega el nombre de la planilla, por ejemplo: 148 y busca este archivo en la carpeta save.
        """

        result = messagebox.showinfo("Introduccion", introduction_text, parent=window)
        if result == "ok":
            write_variable_to_env("INTRODUCTION", "False")
            if (read_variable_from_env("UPDATE") == "True"):
                update_text = "Esta es la version 1.0.0."
                messagebox.showinfo("Actualizacion", update_text, parent=window)
                write_variable_to_env("UPDATE", "False")

def compress_pdf_gui():
    window = tk.Tk()
    window.title("OG AUTOMATIC")
    window.geometry("400x300")
    window.resizable(False, False)
    
    
    window_width = window.winfo_reqwidth()
    window_height = window.winfo_reqheight()
    position_right = int(window.winfo_screenwidth() / 2 - window_width / 2)
    position_down = int(window.winfo_screenheight() / 2.5 - window_height / 2.5)
    window.geometry("+{}+{}".format(position_right, position_down))
    
    window.iconbitmap("icon.ico")
    
    def update_file_count():
        download_folder = "download"
        file_count = len([name for name in os.listdir(download_folder) if os.path.isfile(os.path.join(download_folder, name))])
        file_count_label.config(text=f"Number of files in 'download': {file_count}")
        window.after(5000, update_file_count)

    def compress():
        console_text.config(state=tk.NORMAL)
        console_text.delete("1.0", tk.END)
        console_text.config(state=tk.DISABLED)
        if(merge_and_delete(console_text, tk)):
            window.after(1000)
            if(compress_pdf(console_text, tk)):
                window.after(3000)
                rename_files_in_output_folder("save")
                window.after(2000)
                console_text.config(state=tk.NORMAL)
                console_text.insert(tk.END, "Compression completed.\n")
                console_text.config(state=tk.DISABLED) 
        update_file_count()


    menu_bar = tk.Menu(window)
    window.config(menu=menu_bar)  
    
    option_menu = tk.Menu(menu_bar, tearoff=0)
    option_menu.add_separator()
    option_menu.add_command(label="Exit", command=window.quit)
    option_menu.add_separator()
    menu_bar.add_cascade(label="Options", menu=option_menu)

    label = tk.Label(window, text="OG AUTOMATIC", font=("Arial", 20))
    label.pack(pady=20)
    
    compress_button = tk.Button(window, text="COMPRESS", command=compress, bg="blue", fg="white", font=("Arial", 12), cursor="hand2")
    compress_button.pack(pady=10)
    
    console_text = tk.Text(window, height=5, width=50, state=tk.DISABLED, cursor="hand2")
    console_text.pack(pady=10)
    
    file_count_label = tk.Label(window, text="", font=("Arial", 10))
    file_count_label.pack(side=tk.LEFT, anchor=tk.SW, padx=10, pady=10)
    
    
    label_author = tk.Label(window, text="By Sebastian Solano", font=("Arial", 10))
    label_author.pack(side=tk.RIGHT, anchor=tk.SE, padx=10, pady=10)
    
    int_and_update(window)
    update_file_count()       
                    
    window.mainloop()

compress_pdf_gui()