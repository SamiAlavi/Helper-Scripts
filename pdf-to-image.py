import pdf2image

images = pdf2image.convert_from_path('pdf.pdf')

for i, image in enumerate(images):
    fname = f"image{i}.png"
    image.save(fname, "PNG")
