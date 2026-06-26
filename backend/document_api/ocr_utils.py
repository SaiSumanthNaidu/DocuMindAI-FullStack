from PIL import Image
from PIL import ImageEnhance
from PIL import ImageFilter
import pytesseract


def enhance_image(file_path):

    image = Image.open(file_path)

    # grayscale
    image = image.convert("L")

    # enlarge image
    image = image.resize(
        (
            image.width * 4,
            image.height * 4
        )
    )

    # improve contrast
    image = ImageEnhance.Contrast(
        image
    ).enhance(2)

    # sharpen text
    image = image.filter(
        ImageFilter.SHARPEN
    )

    # reduce noise
    image = image.filter(
        ImageFilter.MedianFilter()
    )

    return image


def extract_text(file_path):

    image = enhance_image(file_path)

    text = pytesseract.image_to_string(
        image,
        lang="eng",
        config="--oem 3 --psm 11"
    )

    return text