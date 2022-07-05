import base64

str = ""
with open("./image/caption4090.jpg", "rb") as imageFile:
    str = base64.b64encode(imageFile.read())
    print(str)

imgdata = base64.b64decode(str)
filename = './image/some_image.jpg'  # I assume you have a way of picking unique filenames
with open(filename, 'wb') as f:
    f.write(imgdata)