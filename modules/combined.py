import os
from PyPDF2 import PdfMerger
from tkinter import messagebox

# Update the merge_and_delete function in combined.py to use the 'download' directory for input and output
def merge_and_delete(console_text, tk):
    directory = "download"
    pdf_files = [file for file in os.listdir(directory) if file.endswith('.pdf')]

    if len(pdf_files) <= 1:
        messagebox.showinfo(("ERROR"),"There are not enough PDF files in the directory to merge.")
        return False
    else:
        pdf_files.sort(key=lambda x: int(x.split('-')[-1].split('.')[0]))
        merger = PdfMerger()

        for file in pdf_files:
            full_path = os.path.join(directory, file)
            with open(full_path, 'rb') as pdf_file:
                merger.append(pdf_file)
                pdf_file.close()

        new_output_file = os.path.join(directory, "SOPORTE PLANILLA X.pdf")

        with open(new_output_file, 'wb') as output:
            merger.write(output)

        for file in pdf_files:
            full_path = os.path.join(directory, file)
            try:
                if file != "SOPORTE PLANILLA X.pdf":
                    os.remove(full_path)
                    print(f"Deleted file: {file}")
            except PermissionError as e:
                print("Could not delete the file:", full_path, "Error:", e)
                # Log errors to console_text in app.py
                console_text.config(state=tk.NORMAL)
                console_text.insert(tk.END, f"Error deleting file: {full_path}, Error: {e}\n")
                console_text.config(state=tk.DISABLED)
                console_text.see(tk.END)
            else:
                # Log successful deletions to console_text in app.py
                console_text.config(state=tk.NORMAL)
                console_text.insert(tk.END, f"Deleted file: {file}\n")
                console_text.config(state=tk.DISABLED)
                console_text.see(tk.END)
        return True