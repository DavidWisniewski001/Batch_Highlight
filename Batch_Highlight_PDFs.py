import csv
import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog

def is_already_highlighted(page, match):
    # Check if the match is already highlighted on the page
    for annot in page.annots():
        if annot.type[0] == 8 and annot.info['content'] == match:
            return True
    return False

def highlight_text(input_pdf_path, search_strings, output_pdf_path=None):
    found_strings = []
    not_found_strings = []

    # Open the PDF file
    pdf_document = fitz.open(input_pdf_path)

    for page in pdf_document:
        for search_string in search_strings:
            # Search for the string in the page
            matches = page.search_for(search_string)
            
            # Highlight each match if it's not already highlighted
            found = False
            for match in matches:
                if not is_already_highlighted(page, match):
                    highlight = page.add_highlight_annot(match)
                    highlight.update()
                    found = True
                    found_strings.append(search_string)
                    break

            if not found:
                not_found_strings.append(search_string)

    # Save the modified PDF if an output path is provided
    if output_pdf_path:
        pdf_document.save(output_pdf_path)
    else:
        # Save the modified PDF with a default name/location
        default_output_path = input_pdf_path.replace('.pdf', '_NEW.pdf')
        pdf_document.save(default_output_path)

    # Close the PDF document
    pdf_document.close()

    # Write found strings to CSV
    with open('strings_found.csv', 'w', newline='', encoding='utf-8-sig') as found_csv:
        writer = csv.writer(found_csv)
        writer.writerow(['Found Strings'])
        writer.writerows([[s] for s in found_strings])

    # Write not found strings to CSV
    with open('strings_not_found.csv', 'w', newline='', encoding='utf-8-sig') as not_found_csv:
        writer = csv.writer(not_found_csv)
        writer.writerow(['Not Found Strings'])
        writer.writerows([[s] for s in not_found_strings])

def browse_file(entry_var):
    file_path = filedialog.askopenfilename()
    entry_var.set(file_path)

def run_highlighter():
    input_pdf_path = entry_input_pdf.get()
    csv_file_path = entry_csv_file.get()
    output_pdf_path = entry_output_pdf.get()

    search_strings = read_search_strings_from_csv(csv_file_path)
    highlight_text(input_pdf_path, search_strings, output_pdf_path)
    tk.messagebox.showinfo("Information", "Text highlighted successfully! Check CSV files for results.")

# Read search strings from CSV
def read_search_strings_from_csv(csv_file_path):
    search_strings = []
    with open(csv_file_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            search_strings.extend(row)
    return search_strings

# Create the GUI
root = tk.Tk()
root.title("PDF Highlighter")

# Input PDF file path
label_input_pdf = tk.Label(root, text="Input PDF File Path:")
label_input_pdf.pack()
entry_input_pdf = tk.Entry(root, width=50)
entry_input_pdf.pack()
button_browse_input_pdf = tk.Button(root, text="Browse", command=lambda: browse_file(entry_input_pdf))
button_browse_input_pdf.pack()

# CSV file path
label_csv_file = tk.Label(root, text="CSV File Path:")
label_csv_file.pack()
entry_csv_file = tk.Entry(root, width=50)
entry_csv_file.pack()
button_browse_csv_file = tk.Button(root, text="Browse", command=lambda: browse_file(entry_csv_file))
button_browse_csv_file.pack()

# Output PDF file path
label_output_pdf = tk.Label(root, text="Output PDF File Path:")
label_output_pdf.pack()
entry_output_pdf = tk.Entry(root, width=50)
entry_output_pdf.pack()
button_browse_output_pdf = tk.Button(root, text="Browse", command=lambda: browse_file(entry_output_pdf))
button_browse_output_pdf.pack()

# Run button
button_run = tk.Button(root, text="Run Highlighter", command=run_highlighter)
button_run.pack()

# Start the GUI event loop
root.mainloop()
