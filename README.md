# File and Folder Finder

This Python script is designed to streamline the process of searching and opening files and folders on your computer. Primarily focused on the C drive for Windows users, it provides a convenient way to find files by name without requiring you to specify their extensions. Additionally, the script can locate folders by their exact names, making it a versatile tool for managing your file system.

## Features

- Search by file name without needing the file extension.
- Locate folders by their exact names.
- Open found files and folders with the default application.

## Usage

1. Clone the repository to your local machine.
2. Run the script and enter the file or folder name when prompted.
3. The script will search the C drive and open the found files or folders.


# File Searching Code for Aadhaar and PAN Numbers

This project is a Python script designed to search for Aadhaar and PAN numbers within image and PDF files in a specified folder. It uses Tesseract OCR to extract text from images and PyMuPDF to handle PDF files.

## Prerequisites

- Python 3.x
- OpenCV
- pytesseract
- Pillow (PIL)
- PyMuPDF (fitz)

### Installation

1. **Install Python packages:**
   ```bash
   pip install opencv-python pytesseract Pillow PyMuPDF

2. **Install Tesseract OCR:**
Download and install Tesseract OCR from [here](https://github.com/UB-Mannheim/tesseract/wiki).
Update the path to the Tesseract-OCR executable in the script if necessary:
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

