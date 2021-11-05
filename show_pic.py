import matplotlib.pyplot as plt
import numpy as np


def show_pic(pics, width=1):
    fig = plt.figure(figsize=(6, 6))
    num_pic = len(pics)
    length = np.ceil(num_pic/width)
    for i in range(num_pic):
        fig.add_subplot(width, length, i + 1, xticks=[], yticks=[])
        plt.imshow(np.uint8(pics[i]), vmin=0, vmax=255)
