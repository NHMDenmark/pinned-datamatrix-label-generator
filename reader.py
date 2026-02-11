from PIL import Image
import zxingcpp

# Open the image file using Pillow
image = Image.open('./NHMA_label.png')

# Convert the image to a format compatible with zxingcpp (e.g., grayscale or RGB)
image = image.convert('RGB')  # For 3D buffer, or use 'L' for grayscale (2D)

# Pass the processed image to the read_barcode function
result = zxingcpp.read_barcode(image, zxingcpp.BarcodeFormat.DataMatrix)

# Print the result
print(result.text)
