import tkinter as tk
from tkinter import filedialog, messagebox
import string
import re
from PyPDF2 import PdfReader
import docx

# Create a new tkinter window
root = tk.Tk()
root.title("Plagiarism Checker")
root.configure(bg="#7EBEEB")

# Function to open file dialog and select file 1
def open_file1():
    filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("PDF Files", "*.pdf"), ("Word Files", "*.docx")])
    file1_entry.delete(0, tk.END)
    file1_entry.insert(0, filepath)

# Function to open file dialog and select file 2
def open_file2():
    filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("PDF Files", "*.pdf"), ("Word Files", "*.docx")])
    file2_entry.delete(0, tk.END)
    file2_entry.insert(0, filepath)

# Function to clean text by removing punctuation and spaces and converting to lowercase
def clean_text(text):
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\s+", "", text)
    return text.lower()

# Function to view the content of a selected file in a new window
def view_file_content(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            file_content = file.read()
        file_content_window = tk.Toplevel()
        file_content_window.title("File Content")
        file_content_label = tk.Label(file_content_window, text=file_content, wraplength=600, justify="left")
        file_content_label.pack(padx=10, pady=10)
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found.")
    except UnicodeDecodeError:
        messagebox.showerror("Error", "The file contains unsupported characters or is not in UTF-8 format.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to extract text from PDF files
def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, "rb") as file:
            reader = PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
    except Exception as e:
        messagebox.showerror("Error", f"Error reading PDF file: {e}")
        return ""

# Function to extract text from Word files
def extract_text_from_docx(docx_path):
    try:
        doc = docx.Document(docx_path)
        text = ""
        for para in doc.paragraphs:
            text += para.text
        return text
    except Exception as e:
        messagebox.showerror("Error", f"Error reading DOCX file: {e}")
        return ""

# Function to compare the contents of two selected files for plagiarism
def compare_files():
    file1_path = file1_entry.get()
    file2_path = file2_entry.get()

    try:
        # Extract text from File 1
        ext1 = file1_path.split('.')[-1].lower()
        if ext1 == 'pdf':
            file1_text = extract_text_from_pdf(file1_path)
        elif ext1 == 'docx':
            file1_text = extract_text_from_docx(file1_path)
        elif ext1 == 'txt':
            with open(file1_path, "r", encoding="utf-8") as file1:
                file1_text = file1.read()
        else:
            messagebox.showerror("Error", "Unsupported file format for File 1.")
            return

        # Extract text from File 2
        ext2 = file2_path.split('.')[-1].lower()
        if ext2 == 'pdf':
            file2_text = extract_text_from_pdf(file2_path)
        elif ext2 == 'docx':
            file2_text = extract_text_from_docx(file2_path)
        elif ext2 == 'txt':
            with open(file2_path, "r", encoding="utf-8") as file2:
                file2_text = file2.read()
        else:
            messagebox.showerror("Error", "Unsupported file format for File 2.")
            return

        # Clean the text of the two files
        file1_text = clean_text(file1_text)
        file2_text = clean_text(file2_text)

        # Calculate the similarity
        if len(file1_text) == 0 or len(file2_text) == 0:
            result_label.config(text="Error: One or both files are empty.", bg="red")
        else:
            common_chars = sum((file1_text.count(char) for char in set(file2_text)))
            similarity = (common_chars / max(len(file1_text), len(file2_text))) * 100

            # Update the result label with the similarity percentage
            if similarity < 30:
                result_label.config(text=f"Similarity: {similarity:.2f}%", bg="#a7c957")  # Low similarity
            elif 30 <= similarity <= 60:
                result_label.config(text=f"Similarity: {similarity:.2f}%", bg="#f77f00")  # Medium similarity
            else:
                result_label.config(text=f"Similarity: {similarity:.2f}%", bg="#c9184a")  # High similarity

    except Exception as e:
        result_label.config(text=f"Error: {str(e)}", bg="red")

# Create labels and buttons for the tkinter window
title_label = tk.Label(root, text="Plagiarism Checker", font=("Calibri", 28), fg="#333333", bg="#7EBEEB")
title_label.grid(row=0, column=0, columnspan=6, pady=(50, 20))

file1_label = tk.Label(root, text="File 1:", font='Calibri 19', bg="#7EBEEB")
file1_label.grid(row=1, column=0, pady=25, columnspan=2)

file1_entry = tk.Entry(root, width=50)
file1_entry.grid(row=2, column=0, padx=50, pady=50, columnspan=2)

file1_button = tk.Button(root, text="Select File", command=open_file1, font='Calibri 14')
file1_button.grid(row=3, column=0)

view_file1_button = tk.Button(root, text="View Content", font='Calibri 14', command=lambda: view_file_content(file1_entry.get()))
view_file1_button.grid(row=3, column=1, padx=10, pady=15)

file2_label = tk.Label(root, text="File 2:", font='Calibri 19', bg="#7EBEEB")
file2_label.grid(row=1, column=3, pady=25, columnspan=2)

file2_entry = tk.Entry(root, width=50)
file2_entry.grid(row=2, column=3, padx=50, pady=50, columnspan=2)

file2_button = tk.Button(root, text="Select File", command=open_file2, font='Calibri 14')
file2_button.grid(row=3, column=3)

view_file2_button = tk.Button(root, text="View Content", font='Calibri 14', command=lambda: view_file_content(file2_entry.get()))
view_file2_button.grid(row=3, column=4, padx=10, pady=15)

compare_button = tk.Button(root, text="Compare Files", command=compare_files, font='Calibri 14')
compare_button.grid(row=4, column=2, padx=50, pady=50)

result_label = tk.Label(root, text=" ", font='Calibri 20 bold', bg='red')
result_label.grid(row=5, column=2, padx=10, pady=50)

# Run the program
root.mainloop()
