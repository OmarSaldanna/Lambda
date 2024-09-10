import io
import base64
from PIL import Image


# function implemented to load images on GPT and Claude models
# converts incomming images to pngs
def base64_to_png_base64(base64_string):
    # decode the image to bytes
    img_bytes = base64.b64decode(base64_string)
    # create the image instance from pillow
    img = Image.open(io.BytesIO(img_bytes))
    # save the image as PNG
    with io.BytesIO() as output:
        img.save(output, format="PNG")
        output.seek(0)
        png_bytes = output.read()

    # now, convert those bytes into a base64 image
    return base64.b64encode(png_bytes).decode('utf-8')