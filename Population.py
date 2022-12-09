from painting import Painting
import random
from PIL import Image, ImageDraw
from copy import deepcopy


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


def print_summary(pop: 'Population', img_template="output%d.png", checkpoint_path="output") -> Painting:
    avg_fitness = sum(i.fiting for i in pop.induviduals) / pop._population_size

    print(f"generation {pop.current_generation}, best score {pop._current_best.fiting}, pop. avg. {avg_fitness}")
    img = pop._current_best.draw()
    img.save(img_template % pop.current_generation, 'PNG')

    # if pop.current_generation % 50 == 0:
    #     pop.checkpoint(target=checkpoint_path, id=pop.current_generation)

class Population():
    def __init__(self, target_img, population_size= 50, generation=0, nb_figures=100, background_color=None, nb_corner=-1, rate=0.04, swap=0.5, sigma=1, color_rate=0.1) -> None:
        self._population_size: int = population_size
        self.induviduals: list[Painting] = [Painting(nb_figures, target_img, background_color, nb_corner) for _ in range(population_size)]
        self.current_generation: int = generation
        self._current_best = None
        self._current_wors = None
        self.rate=rate
        self.swap=swap
        self.sigma=sigma
        self.color_rate=color_rate
        self._target_img: Image = target_img


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

    def mutate_population(self, rate=0.04, swap=0.5, sigma=1, color_rate=0.1):
        for individual in self.induviduals:
            individual.mutate_population(rate, swap, sigma, color_rate)
        print()


    def evolve(self):
        self.current_generation += 1
        save = self._current_best.copy()
        # save = deepcopy(self._current_best)
        new_induviduals = []


        for _ in range(self._population_size):
            mom, dad = pick_best_and_random(self)
            child_a, child_b = Painting.get_child(mom, dad)
            new_induviduals.extend((child_a, child_b))

        ## remove the half worst
        new_induviduals.sort(key=lambda x: x.fiting)
        new_induviduals = new_induviduals[:self._population_size]

        # self.induviduals = deepcopy(new_induviduals)
        self.induviduals = new_induviduals.copy()

        self.mutate_population(rate=self.rate, swap=self.swap, sigma=self.sigma, color_rate=self.color_rate)

        # new_induviduals += deepcopy(self.induviduals)
        # new_induviduals.sort(key=lambda x: x.fiting)
        # self.induviduals = deepcopy(new_induviduals[:self._population_size])

        self.set_current_worst()

        self.induviduals.remove(self._current_wors)
        self.induviduals.append(save)

        self.set_current_best()




    def evolution(self, nb_generation, img_template="output%d.png", checkpoint_path="output", rate=None, swap=None, sigma=None, color_rate=None):
        if rate is not None:
            self.rate=rate
        if swap is not None:
            self.swap=swap
        if sigma is not None:
            self.sigma=sigma
        if color_rate is not None:
            self.color_rate=color_rate
        for _ in range(nb_generation):
            self.evolve()
            print_summary(self, img_template, checkpoint_path)

    def checkpoint(self, target, id):
        with open(target + str(id) + '.txt', 'w') as f:
            f.write(str(self))







