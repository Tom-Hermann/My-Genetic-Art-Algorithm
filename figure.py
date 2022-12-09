from abc import ABC, abstractmethod
import random
from PIL import Image, ImageDraw


class Figure(ABC):
    @abstractmethod
    def mutate(self):
        pass

    @abstractmethod
    def draw(self, img: Image, scale=1.0):
        pass

    @abstractmethod
    def isCircle(self):
        pass

class Polygon(Figure):
    def __init__(self, img_width, img_height, nb_corner=-1):
        x = random.randint(0, int(img_width))
        y = random.randint(0, int(img_height))
        self.nb_corner = nb_corner

        if nb_corner != -1:
            self.points = [(x + random.randint(-50, 50), y + random.randint(-50, 50)) for _ in range(nb_corner)]
        else:
            self.points = [(x + random.randint(-50, 50), y + random.randint(-50, 50)) for _ in range(random.randint(3, 10))]

        self.color = (
            random.randint(0, 256),
            random.randint(0, 256),
            random.randint(0, 256),
            random.randint(0, 256)
        )

        self._img_width = img_width
        self._img_height = img_height

    def draw(self, img: Image, scale=1.0):
        new_figure = Image.new('RGBA', (self._img_width, self._img_height))
        draw = ImageDraw.Draw(new_figure)
        draw.polygon([(x * scale, y * scale) for x, y in self.points], fill=self.color)
        img = Image.alpha_composite(img, new_figure)
        return img

    def __repr__(self) -> str:
        return f"Polygone(size:{len(self.points)},[{','.join([str(p) for p in self.points])}] in colors {str(self.color)})"

    def mutate(self, sigma=1.0):
        mutations = ['move', 'point', 'color', 'reset']
        weights = [30, 35, 30, 5]

        mutation_type = random.choices(mutations, weights=weights, k=1)[0]

        if mutation_type == 'move': # move the whole triangle
            x_shift = int(random.randint(-50, 50)*sigma)
            y_shift = int(random.randint(-50, 50)*sigma)
            self.points = [(x + x_shift, y + y_shift) for x, y in self.points]
        elif mutation_type == 'point': # change one point
            index = random.choice(list(range(len(self.points))))
            self.points[index] = (self.points[index][0] + int(random.randint(-50, 50)*sigma), self.points[index][1] + int(random.randint(-50, 50)*sigma))
        elif mutation_type == 'color': # change color
            self.color = tuple(c + int(random.randint(-50, 50)*sigma) for c in self.color) # move color by random value
            self.color = tuple(min(max(c, 0), 255) for c in self.color) # clamp to 0-255
        else: # create new triangle
            new_Polygon = Polygon(self._img_width, self._img_height, self.nb_corner)

            self.points = new_Polygon.points
            self.color = new_Polygon.color
        return self

    def isCircle(self):
        return False

    def copy(self):
        new_polygon = Polygon(self._img_width, self._img_height, self.nb_corner)
        new_polygon.points = self.points.copy()
        new_polygon.color = self.color.copy()
        return new_polygon



class Circle(Figure):
    def __init__(self, img_width, img_height, nb_corner=1) -> None:
        x = random.randint(0, int(img_width))
        y = random.randint(0, int(img_height))
        self.nb_corner = nb_corner

        center = (x + random.randint(-50, 50), y + random.randint(-50, 50))
        radius = random.randint(10, 70)

        # get upper left and lower right of the bounding box
        self.points = (center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius)
        self.color = (
            random.randint(0, 256),
            random.randint(0, 256),
            random.randint(0, 256),
            random.randint(0, 256)
        )

        self._img_width = img_width
        self._img_height = img_height

    def __repr__(self) -> str:
        return f"Cirlce({','.join([str(p) for p in self.points])} in colors {str(self.color)})"

    def mutate(self, sigma=1.0):
        mutations = ['move', 'color', 'reset']
        weights = [30, 35, 30, 5]

        mutation_type = random.choices(mutations, weights=weights, k=1)[0]

        if mutation_type == 'move': # move the whole triangle
            x_shift = int(random.randint(-50, 50)*sigma)
            y_shift = int(random.randint(-50, 50)*sigma)
            self.points = [(x + x_shift, y + y_shift) for x, y in self.points]
        elif mutation_type == 'color': # change color
            self.color = tuple(c + int(random.randint(-50, 50)*sigma) for c in self.color) # move color by random value
            self.color = tuple(min(max(c, 0), 255) for c in self.color) # clamp to 0-255
        else: # create new triangle
            new_circle = Circle(self._img_width, self._img_height, self.nb_corner)
            self.points = new_circle.points
            self.color = new_circle.color

    def draw(self, img: ImageDraw, scale=1.0):
        new_figure = Image.new('RGBA', (self._img_width, self._img_height))
        draw = ImageDraw.Draw(new_figure)
        w,x,y,z = self.points
        draw.ellipse((w * scale, x * scale, y * scale, z * scale), fill=self.color)
        img = Image.alpha_composite(img, new_figure)
        return img

    def isCircle(self):
        return True

    def copy(self) -> 'Circle':
        new = Circle(self._img_width, self._img_height, self.nb_corner)
        new.points = self.points.copy()
        new.color = self.color.copy()
        return new

