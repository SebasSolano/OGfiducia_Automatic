# You can encapsulate the existing code in a function that takes directory, output_directory, and output_base_name as parameters.
def merge_and_delete(directory, output_directory, output_base_name):
    import os
    from PyPDF2 import PdfMerger

    # Get the list of PDF files in the directory
    pdf_files = [file for file in os.listdir(directory) if file.endswith('.pdf')]

    # Check if there are less than 2 PDF files in the directory
    if len(pdf_files) <= 1:
        print("There are not enough PDF files in the directory to merge.")
    else:
        # Sort the files by name
        pdf_files.sort(key=lambda x: int(x.split('-')[-1].split('.')[0]))

        # Create an object to merge the PDF files
        merger = PdfMerger()

        # Add each PDF file to the merge object and close them
        for file in pdf_files:
            full_path = os.path.join(directory, file)
            with open(full_path, 'rb') as pdf_file:
                merger.append(pdf_file)
                pdf_file.close()

        # Save the merged file to a new file
        existing_files = [file for file in os.listdir(output_directory) if file.startswith(output_base_name)]
        new_file_number = len(existing_files) + 1
        new_output_file = os.path.join(output_directory, f"{output_base_name}-{new_file_number}.pdf")

        # Save the merged file with the new name
        with open(new_output_file, 'wb') as output:
            merger.write(output)

        # Delete the original files from the input directory
        for file in pdf_files:
            full_path = os.path.join(directory, file)
            try:
                os.remove(full_path)
            except PermissionError as e:
                print("Could not delete the file:", full_path, "Error:", e)