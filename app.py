from combined import merge_and_delete
from compressed import compress_pdf
import os


# DIRECTORIES
directory = "C:/Users/Accor/Documents/OGfiducia_Automatic/Download"
output_directory = "C:/Users/Accor/Documents/OGfiducia_Automatic/Combined"
output_base_name = "merged"

input_file = "C:/Users/Accor/Documents/OGfiducia_Automatic/Final_Combined/Final_Combined-1.pdf"
output_file = "C:/Users/Accor/Documents/OGfiducia_Automatic/Compressed/"


def rename_files_in_output_folder(output_file):

    new_file_name = input("Enter a name for the file: ")
    files = os.listdir(output_file)
    for file in files:
        if file.endswith('.pdf'):
            new_name = os.path.join(output_file, new_file_name+'.pdf')
            os.rename(os.path.join(output_file, file), new_name)
            print(f"File {file} renamed to "+new_file_name+'.pdf')


def display_menu():

    while True:
        print("Menu:")
        print("1. Download - No Found")
        print("2. Combined")
        print("3. Final Combined")
        print("4. Compressed")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            link = input("Enter the link: ")
            print("This option is not found!")

            pass
        elif choice == '2':
            merge_and_delete(directory, output_directory, output_base_name)
        elif choice == '3':

            directory = output_directory
            output_directory = "C:/Users/Accor/Documents/OGfiducia_Automatic/Final_Combined"
            output_base_name = "Final_Combined"

            merge_and_delete(directory, output_directory, output_base_name)
            pass
        elif choice == '4':
            compress_pdf(input_file, output_file)
            rename_files_in_output_folder(output_file)
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

        # os.system('cls' if os.name == 'nt' else 'clear')

display_menu()
