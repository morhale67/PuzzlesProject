import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np
from PIL import Image
import cv2
from skimage.feature import _canny as canny
# import skimage.feature._canny as canny

# import skimage.feature


# create template - failed for now

# load picture
path_images = Path(r'C:\Users\user\Desktop\PuzzleProject\Pictures\Templates')
image_to_open = path_images / "6x8.jpg"
template_image = np.asarray(Image.open(image_to_open).convert('L'))
threshold = 220  # !!!!!!!!! hard coded !!!!!!!!!!!!!!!!!
template_image = np.where(template_image < threshold, 0, 255)
plt.imshow(template_image, cmap='gray', vmin=0, vmax=255)

# erosion
template_image = template_image.astype('uint8')
# kernel = np.ones((3, 3), np.uint8)
kernel = (np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])).astype('uint8')
img_erosion = cv2.erode(template_image, kernel, iterations=1)
plt.imshow(img_erosion, cmap='gray', vmin=0, vmax=255)

# contour
ret, thresh = cv2.threshold(template_image, 150, 255, cv2.THRESH_BINARY)
contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)  # draw
# contours on the original image
image_copy = template_image.copy()
cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2,
                 lineType=cv2.LINE_AA)

# see the results
cv2.imshow('None approximation', image_copy)
plt.imshow(image_copy, cmap='gray', vmin=0, vmax=255)

############################################################################################################

# identify pieces
path_images = Path(r'C:\Users\user\Desktop\PuzzleProject\Pictures')
image_to_open = path_images / "second_level.jpg"
image_second_level = np.asarray(Image.open(image_to_open).convert('L'))
fig = plt.figure(figsize=(6, 6))
plt.imshow(image_second_level, cmap='gray', vmin=0, vmax=255)

##############
img = image_second_level
img_contours = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2]
""" Edge Based Segmentation """
""" edge detection with canny """
edges = canny(img)
fig, ax = plt.subplots(figsize=(4, 4))
ax.imshow(edges, cmap=plt.cm.gray)
ax.axis('off')
ax.set_title('Canny detector')
""" region - hole filling """
fill_holes = ndi.binary_fill_holes(edges)
fig, ax = plt.subplots(figsize=(4, 3))
ax.imshow(fill_holes, cmap=plt.cm.gray, interpolation='nearest')
ax.axis('off')
ax.set_title('Filling the holes')

plt.imshow(new_img, cmap='gray', vmin=0, vmax=255)

