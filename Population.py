from painting import Painting
import random
from PIL import Image, ImageDraw
from copy import deepcopy
import threading

save = 0

def pick_random(pop):
    mom = random.choice(pop)
    dad = random.choice(pop)
    return mom, dad


def pick_best_and_random(pop: 'Population', maximize=False):
    if evaluated_individuals := tuple(filter(lambda x: x.fiting is not None, pop)):
        mom = max(evaluated_individuals, key=lambda x: x.fiting if maximize else -x.fiting)
    else:
        mom = random.choice(pop)
    dad = random.choice(pop)
    return mom, dad


def print_summary(pop: 'Population', img_template="output%d.png", checkpoint_path="output") -> int:

    global save

    avg_fitness = sum(i.fiting for i in pop.induviduals) / pop._population_size

    if pop.printable:
        print(f"\tBest score {pop._current_best.fiting}, pop. avg. {avg_fitness}")
    if (save != pop._current_best.fiting and pop.current_generation % pop.save_rate == 0):
        save = pop._current_best.fiting
        img = pop._current_best.draw()
        img.save(img_template % pop._id_image, 'PNG')
        pop._id_image += 1


    # if pop.current_generation % 50 == 0:
    #     pop.checkpoint(target=checkpoint_path, id=pop.current_generation)

class Population():
    def __init__(self, target_img, population_size= 50, generation=0, nb_figures=100, background_color=None, nb_corner=-1, rate=0.04, swap=0.5, sigma=1, bg_color_rate=0.1, save_rate=1, printable=True) -> None:
        self._id_image = 0
        self._population_size: int = population_size
        self.induviduals: list[Painting] = []
        for _ in range(population_size):
            self.induviduals.append(Painting(nb_figures, target_img, background_color, nb_corner, printable=printable))
            if self.printable:
                print('.', end='', flush=True)
        if self.printable:
            print()
        self.current_generation: int = generation
        self._current_best = None
        self._current_wors = None
        self.rate=rate
        self.swap=swap
        self.sigma=sigma
        self.bg_color_rate=bg_color_rate
        self._target_img: Image = target_img

        self.save_rate = save_rate
        self.printable = printable


        self.set_current_best()
        self.set_current_worst()


    def __iter__(self):
        return iter(self.induviduals)

    def __len__(self):
        return len(self.induviduals)

    def __getitem__(self, index):
        return self.induviduals[index]

    def __setitem__(self, index, value):
        self.induviduals[index] = value

    def __delitem__(self, index):
        del self.induviduals[index]

    def __contains__(self, item):
        return item in self.induviduals

    @property
    def get_current_best(self):
        return self._current_best

    def set_current_best(self, maximize=False):
        if evaluated_individuals := tuple(filter(lambda x: x.fiting is not None, self.induviduals)):
            self._current_best = max(evaluated_individuals, key=lambda x: x.fiting if maximize else -x.fiting)
        else:
            self._current_best = random.choice(self.induviduals)

    def set_current_worst(self, maximize=False):
        if evaluated_individuals := tuple(filter(lambda x: x.fiting is not None, self.induviduals)):
            self._current_wors = min(evaluated_individuals, key=lambda x: x.fiting if maximize else -x.fiting)
        else:
            self._current_wors = random.choice(self.induviduals)

    def mutate_population(self, rate=0.04, swap=0.5, sigma=1, bg_color_rate=0.1):
        if self.printable:
            print(f'\tMutating induviduals:\t\t', end='', flush=True)
        for individual in self.induviduals:
            individual.mutate_population(rate, swap, sigma, bg_color_rate)
        if self.printable:
            print()


    def evolve(self):
        self.current_generation += 1
        save = self._current_best.copy()
        new_induviduals = []

        print(f'Generation {self.current_generation}:\n\tCreating new induviduals:\t', end='', flush=True)
        for _ in range(self._population_size):
            mom, dad = pick_best_and_random(self)
            child_a, child_b = Painting.get_child(mom, dad)
            new_induviduals.extend((child_a, child_b))
            print('.', end='', flush=True)
        print()
        new_induviduals.sort(key=lambda x: x.fiting)
        new_induviduals = new_induviduals[:self._population_size]

        self.induviduals = new_induviduals.copy()

        self.mutate_population(rate=self.rate, swap=self.swap, sigma=self.sigma, bg_color_rate=self.bg_color_rate)


        self.set_current_worst()

        self.induviduals.remove(self._current_wors)
        self.induviduals.append(save)

        self.set_current_best()




    def evolution(self, nb_generation, img_template="output%d.png", checkpoint_path="output", rate=None, swap=None, sigma=None, bg_color_rate=None):
        global save
        if rate is not None:
            self.rate=rate
        if swap is not None:
            self.swap=swap
        if sigma is not None:
            self.sigma=sigma
        if bg_color_rate is not None:
            self.bg_color_rate=bg_color_rate
        for _ in range(nb_generation):
            self.evolve()
            #  mutltithreading print_summary(self, img_template, checkpoint_path) using threading lib:
            threading.Thread(target=print_summary, args=(self, img_template, checkpoint_path)).start()







    def checkpoint(self, target, id):
        with open(target + str(id) + '.txt', 'w') as f:
            f.write(str(self))







