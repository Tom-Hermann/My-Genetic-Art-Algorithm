from PIL import Image
from imgcompare import image_diff
import os

target_image = Image.open("./img/moi2.jpg").convert('RGBA')
nb_error=0

print(f'test: {image_diff(target_image, target_image)}')

for i in range(1, len(os.listdir('./res'))):
    im1 = Image.open(f'./res/drawing_{"0" * (5-len(str(i)))}{i}.png').convert('RGBA')
    im2 = Image.open(f'./res/drawing_{"0" * (5-len(str(i+1)))}{i+1}.png').convert('RGBA')
    score_im1=image_diff(target_image, im1)
    score_im2=image_diff(target_image, im2)
    nb_error+=score_im2>score_im1
    print(f"score image {i}: {score_im1}")
print(f"score image {i+1}: {score_im2}")
print(f"nb error  = {nb_error}")