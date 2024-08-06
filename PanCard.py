import cv2
import pytesseract
import re
from PIL import Image, ImageEnhance, ImageFilter
import os
import fitz  # PyMuPDF

# Path to the Tesseract-OCR executable (update if necessary)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def convert_pdf_to_images(pdf_path):
    try:
        # Open the PDF file
        pdf_document = fitz.open(pdf_path)
        images = []
        # Iterate over each page
        for page_num in range(len(pdf_document)):
            # Get the page
            page = pdf_document.load_page(page_num)
            # Convert the page to a pixmap (image)
            pix = page.get_pixmap()
            # Convert pixmap to a PIL Image
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            images.append(img)
        return images
    except Exception as e:
        print(f"An error occurred while converting PDF to images: {e}")
        return []

def preprocess_image(image_path):
    try:
        # Check if the file exists
        if not os.path.isfile(image_path):
            raise FileNotFoundError(f"Image file not found at the path: {image_path}")
        
        # Read the image using OpenCV
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Unable to read the image file: {image_path}")
        
        # Convert the image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply bilateral filter to preserve edges
        bilateral = cv2.bilateralFilter(gray, 9, 75, 75)
        
        # Apply adaptive thresholding
        adaptive_thresh = cv2.adaptiveThreshold(bilateral, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
        
        # Apply median blur to reduce noise
        median_blur = cv2.medianBlur(adaptive_thresh, 3)
        
        # Apply morphological operations to reduce noise
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        morph = cv2.morphologyEx(median_blur, cv2.MORPH_CLOSE, kernel, iterations=2)
        
        # Convert the image back to PIL format and enhance it
        pil_img = Image.fromarray(morph)
        pil_img = pil_img.filter(ImageFilter.SHARPEN)
        enhancer = ImageEnhance.Contrast(pil_img)
        pil_img = enhancer.enhance(2)
        
        return pil_img
    except FileNotFoundError as e:
        print(e)
        return None
    except ValueError as e:
        print(e)
        return None
    except Exception as e:
        print(f"An unexpected error occurred during image preprocessing: {e}")
        return None

def extract_pan_number(image_path, keyword):
    try:
        # Check if the input is a PDF or an image
        if image_path.lower().endswith('.pdf'):
            images = convert_pdf_to_images(image_path)
        else:
            images = [preprocess_image(image_path)]
        
        if not images:
            raise ValueError("No images to process. Conversion or preprocessing failed.")
        
        pan_number = None
        
        for img in images:
            if img is None:
                continue
            
            # Perform OCR on the image with custom configuration
            custom_config = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(img, config=custom_config, lang='eng')
            
            # Convert text to lowercase and keyword to lowercase for case-insensitive comparison
            text_lower = text.lower()
            keyword_lower = keyword.lower()
            
            # Split the keyword into individual words
            keyword_words = keyword_lower.split()
            
            # Check if all individual words are in the text
            all_words_found = all(word in text_lower for word in keyword_words)
            
            # Define the PAN card number pattern (10-character alphanumeric)
            pan_pattern = r'\b[A-Z]{5}\d{4}[A-Z]\b'
            
            if all_words_found:
                pan_matches = re.findall(pan_pattern, text)
                if pan_matches:
                    pan_number = pan_matches[0]
                    break  # Stop searching if we found a PAN number
            
            print("Extracted Text:\n", text)
        
        return pan_number
    except ValueError as e:
        print(e)
        return None
    except Exception as e:
        print(f"An unexpected error occurred during OCR extraction: {e}")
        return None

def process_folder(folder_path, keyword):
    try:
        # Iterate over all files in the folder
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                print(f"Processing file: {file_path}")
                pan_number = extract_pan_number(file_path, keyword)
                if pan_number:
                    print(f"PAN Number: {pan_number}")
                    return pan_number
                else:
                    print("PAN number not found in this file.")
        print("No PAN number found in any file.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while processing the folder: {e}")
        return None

if __name__ == "__main__":
    while True:
        # Get user input for folder path and keyword
        folder_path = input("Enter the folder path: ").strip()
        keyword = input("Enter the keyword: ").strip()

        # Process the folder to find PAN number
        pan_number = process_folder(folder_path, keyword)

        if pan_number:
            print(f"Found PAN Number: {pan_number}")
        else:
            print("PAN number not found in any file.")

        # Ask user if they want to exit
        exit_choice = input("Do you want to exit? (yes/no): ").strip().lower()
        if exit_choice == 'yes':
            print("Exiting the program.")
            break
        else:
            print("Continuing with the next folder and keyword.")
