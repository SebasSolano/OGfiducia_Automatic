from pylovepdf.ilovepdf import ILovePdf
import os
from getKEY import read_variable_from_env


def compress_pdf(input_file, output_directory):

    if not os.path.exists(input_file):
        print("No files found in the output directory. Exiting function.")
        return
    else:
        PUBLIC_KEY = read_variable_from_env("PUBLIC_KEY")
        # print(public_key)

        ilovepdf = ILovePdf(PUBLIC_KEY, verify_ssl=True)
        task = ilovepdf.new_task('compress')
        task.add_file(input_file)
        task.set_output_folder(output_directory)
        task.execute()
 
        task.download()
        task.delete_current_task()
        os.remove(input_file)


