from PIL import Image, ImageOps, ImageFilter
import pytesseract

def ocr_image(pil_image, psm=6, oem=3, lang="eng"):
    """Run Tesseract OCR on a PIL image with light preprocessing."""
    gray = ImageOps.grayscale(pil_image)
    sharp = gray.filter(ImageFilter.UnsharpMask(radius=1.2, percent=150, threshold=3))
    config = f"--psm {psm} --oem {oem}"
    return pytesseract.image_to_string(sharp, lang=lang, config=config)
