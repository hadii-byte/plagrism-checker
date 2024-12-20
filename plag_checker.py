import os
import string
import re
from PyPDF2 import PdfReader
import docx

# Function to clean text by removing punctuation and spaces and converting to lowercase
def clean_text(text):
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\s+", "", text)
    return text.lower()

# Function to extract text from PDF files
def extract_text_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error reading PDF file {pdf_path}: {e}")
        return ""

# Function to extract text from Word files
def extract_text_from_docx(docx_path):
    try:
        doc = docx.Document(docx_path)
        text = "".join(para.text for para in doc.paragraphs)
        return text
    except Exception as e:
        print(f"Error reading DOCX file {docx_path}: {e}")
        return ""

# Function to load file content based on its extension
def load_file_content(file_path):
    ext = file_path.split('.')[-1].lower()
    if ext == 'pdf':
        return extract_text_from_pdf(file_path)
    elif ext == 'docx':
        return extract_text_from_docx(file_path)
    elif ext == 'txt':
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        except Exception as e:
            print(f"Error reading TXT file {file_path}: {e}")
            return ""
    else:
        print(f"Unsupported file format: {file_path}")
        return ""

# Function to calculate similarity between two texts
def calculate_similarity(text1, text2):
    text1 = clean_text(text1)
    text2 = clean_text(text2)

    if len(text1) == 0 or len(text2) == 0:
        return 0.0

    common_chars = sum((text1.count(char) for char in set(text2)))
    similarity = (common_chars / max(len(text1), len(text2))) * 100
    return similarity

# Main function
def main():
    print("Welcome to the CLI Plagiarism Checker!")
    file1_path = input("Enter the path to File 1: ").strip()
    file2_path = input("Enter the path to File 2: ").strip()

    if not os.path.exists(file1_path) or not os.path.exists(file2_path):
        print("One or both file paths are invalid. Please try again.")
        return

    # Load content from files
    file1_content = load_file_content(file1_path)
    file2_content = load_file_content(file2_path)

    if not file1_content or not file2_content:
        print("Could not read one or both files. Please check the file paths and formats.")
        return

    # Calculate similarity
    similarity = calculate_similarity(file1_content, file2_content)
    print(f"Similarity between the files: {similarity:.2f}%")

    if similarity < 30:
        print("Low similarity. Files are likely not plagiarized.")
    elif 30 <= similarity <= 60:
        print("Medium similarity. Some overlap detected.")
    else:
        print("High similarity. Possible plagiarism!")

if __name__ == "__main__":
    main()
