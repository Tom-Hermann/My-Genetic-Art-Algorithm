from Population import Population, print_summary
import os
from PIL import Image
import sys
import argparse



parser = argparse.ArgumentParser()
parser.add_argument('--image', type=str, required=True, help='Path to the target image')
parser.add_argument('--result_file', type=str, required=True, help='Path to the result file')
parser.add_argument('--corner', type=int, help='Number of corner of the polygon. Range [3, 10], 1 for circle, -1 for random, default is 3', default=3)
parser.add_argument('--figures', type=int, help='Number of figure that compose the image, default is 150', default=150)
parser.add_argument('--population', type=int, help='Population size, default is 100', default=100)
parser.add_argument('--save', type=int, help='After how many generations the image is saved, default is 1 (every generation)', default=1)
parser.add_argument('--print', type=bool, help='Show progress, default True', default=True)
# parser.add_argument('--checkpoint', type=int, help='After how many generations the checkpoint is saved, default is 50', default=50)


args = parser.parse_args()

# target_image_path = sys.argv[1]
# checkpoint_path = sys.argv[2]
# nb_corner = int(sys.argv[3])

if __name__ == "__main__":


    # target_image_path = "./img/moi2.jpg"
    # checkpoint_path = "./res/"

    image_template = os.path.join(args.result_file, "drawing_%05d.png")
    target_image = Image.open(args.image).convert('RGBA')


    if args.print:
        print("Init population:")
    pop = Population(target_image, population_size=args.population, nb_figures=args.figures, nb_corner=args.corner, rate=0.20, swap=0.75, save_rate=args.save, printable=args.print)
    if args.print:
        print("Finish init")
    pop.evolution(300, img_template=image_template, checkpoint_path=args.result_file, rate=0.20, swap=0.75, bg_color_rate=0.15)
    pop.evolution(500, img_template=image_template, checkpoint_path=args.result_file, rate=0.15, swap=0.5, bg_color_rate=0)
    pop.evolution(1000, img_template=image_template, checkpoint_path=args.result_file, rate=0.10, swap=0.25, bg_color_rate=0)
    pop.evolution(1500, img_template=image_template, checkpoint_path=args.result_file, rate=0.05, swap=0, sigma=0.15, bg_color_rate=0)
    pop.evolution(2000, img_template=image_template, checkpoint_path=args.result_file, rate=0.03, swap=0, sigma=0.12, bg_color_rate=0)

    img = pop._current_best.draw()
    img.save(os.path.join(args.result_file, "res.png"), 'PNG')