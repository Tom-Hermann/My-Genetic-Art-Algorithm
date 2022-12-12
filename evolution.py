from Population import Population
import os
from PIL import Image
import sys

target_image_path = sys.argv[1]
checkpoint_path = sys.argv[2]
nb_corner = int(sys.argv[3])
# target_image_path = "./img/moi2.jpg"
# checkpoint_path = "./res/"
image_template = os.path.join(checkpoint_path, "drawing_%05d.png")
target_image = Image.open(target_image_path).convert('RGBA')

num_triangles = 150
population_size = 100

print("Init population:")
pop = Population(target_image, population_size=population_size, nb_figures=num_triangles, nb_corner=nb_corner, rate=0.20, swap=0.75)
print("Finish init")
pop.evolution(300, img_template=image_template, checkpoint_path=checkpoint_path, rate=0.20, swap=0.75, color_rate=0.15)
pop.evolution(500, img_template=image_template, checkpoint_path=checkpoint_path, rate=0.15, swap=0.5, color_rate=0)
pop.evolution(1000, img_template=image_template, checkpoint_path=checkpoint_path, rate=0.10, swap=0.25, color_rate=0)
pop.evolution(1500, img_template=image_template, checkpoint_path=checkpoint_path, rate=0.05, swap=0, sigma=0.15, color_rate=0)
pop.evolution(2000, img_template=image_template, checkpoint_path=checkpoint_path, rate=0.03, swap=0, sigma=0.12, color_rate=0)