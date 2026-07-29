import sys
import io
import cv2
import numpy as np
from PIL import Image
from rembg import remove



def enhance_image(img):
    # Convert PIL image to OpenCV format
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    # Convert to LAB color space
    lab = cv2.cvtColor(img_cv, cv2.COLOR_BGR2LAB)

    l, a, b = cv2.split(lab)

    # CLAHE for better contrast
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l = clahe.apply(l)

    lab = cv2.merge((l, a, b))
    enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    return Image.fromarray(cv2.cvtColor(enhanced, cv2.COLOR_BGR2RGB))


def main():
    if len(sys.argv) != 2:
        print("Usage: python clean_photo.py <image>")
        return

    input_path = sys.argv[1]

    # Remove background
    with open(input_path, "rb") as f:
        output = remove(f.read())

    img = Image.open(io.BytesIO(output)).convert("RGBA")

    # White background
    white = Image.new("RGBA", img.size, (255, 255, 255, 255))
    white.paste(img, mask=img)

    rgb = white.convert("RGB")

    # Improve contrast
    rgb = enhance_image(rgb)

    rgb.save("assets/photo-ready.png")

    print("Saved -> assets/photo-ready.png")


if __name__ == "__main__":
    main()


