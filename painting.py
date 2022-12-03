from figure import Circle, Polygon, Figure
from PIL import Image, ImageDraw
from imgcompare import image_diff
import random
from copy import deepcopy


class Painting:
    def __init__(self,nb_figures, target_img: Image, background_color=(0,0,0,255), nb_corner=-1, set_figures:bool = True):
        self._target_img = target_img
        self._img_width, self._img_height = target_img.size
        self._nb_figures = nb_figures
        self._background_color = background_color if len(background_color) == 4 else background_color + (255,)
        self.nb_corner = nb_corner

        if (set_figures):
            figure = Circle if self.nb_corner == 1 else Polygon
            self.figures = [figure(self._img_width, self._img_height, self.nb_corner) for _ in range(nb_figures)]
            self.fiting = self.image_diff()
        else:
            self.fiting = None
            self.figures = []


    def copy(self):
        copy = Painting(self._nb_figures, self._target_img, self._background_color, self.nb_corner)
        copy.figures = list(self.figures)
        return copy


    @property
    def get_background_color(self):
        return self._background_color[:3]

    @property
    def get_img_width(self):
        return self._img_width

    @property
    def get_img_height(self):
        return self._img_height

    @property
    def num_element(self):
        return len(self.figures)


    def image_diff(self) -> int:
        return image_diff(self.draw(), self._target_img)

    def reset_figures(self):
        self.figures = []

    def draw(self, scale=1) -> Image:
        img = Image.new("RGBA", (self._img_width*scale, self._img_height*scale))
        draw = ImageDraw.Draw(img)

        if not hasattr(self, '_background_color'):
            self._background_color = (0, 0, 0, 255)

        draw.polygon([(0, 0), (0, self._img_height*scale), (self._img_width*scale, self._img_height*scale), (self._img_width*scale, 0)], fill=self._background_color)

        for figure in self.figures:
            img = figure.draw(img, scale)

        return img

    @staticmethod
    def _mate_possible(a: 'Painting', b: 'Painting') -> bool:
        return all([a.num_element == b.num_element,
                   a.get_img_width == b.get_img_width,
                   a.get_img_height == b.get_img_height])

    @staticmethod
    def get_child(parrent_a: 'Painting', parrent_b: 'Painting'):
        if not Painting._mate_possible(parrent_a, parrent_b):
            raise Exception("Cannot mate images with different dimensions or number of triangles")
        bg = tuple(int(a + b / 2) for a, b in zip(parrent_a.get_background_color, parrent_b.get_background_color))
        childa = Painting(parrent_a.num_element, parrent_a._target_img, bg, parrent_a.nb_corner, set_figures=False)
        childb = Painting(parrent_b.num_element, parrent_b._target_img, bg, parrent_b.nb_corner, set_figures=False)


        for i in range(parrent_a.num_element):
            if random.random() < 0.5:
                childa.figures.append(parrent_a.figures[i])
                childb.figures.append(parrent_b.figures[i])
            else:
                childa.figures.append(parrent_b.figures[i])
                childb.figures.append(parrent_a.figures[i])

        childa.fiting = childa.image_diff()
        childb.fiting = childa.image_diff()

        return deepcopy(childa), deepcopy(childb)


    def mutate_population(self, rate=0.04, swap=0.5, sigma=1.0):
        total_mutations = int(rate*self.num_element)
        random_indices = list(range(self.num_element))
        random.shuffle(random_indices)

        # mutate random triangles
        for i in range(total_mutations):
            index = random_indices[i]
            self.figures[index].mutate(sigma=sigma)


        # Swap two triangles randomly
        if random.random() < swap:
            random.shuffle(random_indices)
            self.figures[random_indices[0]], self.figures[random_indices[1]] = self.figures[random_indices[1]], self.figures[random_indices[0]]

        self.fiting = self.image_diff()
        print('.', end='', flush=True)