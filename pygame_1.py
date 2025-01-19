import pygame
from typing import Tuple, Dict
from math import sqrt


# Variables à définir :
print("")
print("Bienvenu dans ma simulation de Prédateurs et Proies")

"""borne_min_ecran = 300
borne_max_ecran = 700

hauteur = int(input(f" - Entrez une hauteur pour l'ecran (entre {borne_min_ecran} et {borne_max_ecran}) : ") or 400)
while hauteur < borne_min_ecran or hauteur > borne_max_ecran:
    print("La hauteur n'est pas dans l'intervalle")
    hauteur = int(input(f" - Entrez une hauteur pour l'ecran (entre {borne_min_ecran} et {borne_max_ecran}) : "))

largeur = int(input(f" - Entrez une largeur pour l'ecran (entre {borne_min_ecran} et {borne_max_ecran}) : ") or 400)
while largeur < borne_min_ecran or largeur > borne_max_ecran:
    print("La largeur n'est pas dans l'intervalle")
    largeur = int(input(f" - Entrez une largeur pour l'ecran (entre {borne_min_ecran} et {borne_max_ecran}) : "))"""
largeur = 400
hauteur = 400

WINDOW_SIZE: Tuple[int, int] = (largeur, hauteur)
WINDOW_TITLE: str = "Predateurs et Proies"
FPS = 12



"""max_renards = int(0.055 * sqrt(hauteur*largeur) * 2) 
nbre_initial_renards = int(input(f" - Entrez un nombre initial de renards (inférieur à {max_renards}) : ") or 22)
while nbre_initial_renards < 0 or nbre_initial_renards > max_renards:
    print("Le nombre n'est pas dans l'intervalle")
    nbre_initial_renards = int(input(f" - Entrez un nombre initial de renards (inférieur à {max_renards}) : "))

max_lapins = int(1.3 * sqrt(hauteur*largeur) * 2)
nbre_initial_lapins = int(input(f" - Entrez un nombre initial de lapins (inférieur à {max_lapins}) : ") or 520)
while nbre_initial_lapins < 0 or nbre_initial_lapins > max_lapins:
    print("Le nombre n'est pas dans l'intervalle")
    nbre_initial_lapins = int(input(f" - Entrez un nombre initial de lapins (inférieur à {max_lapins}) : "))

max_plantes = int(1.75 * sqrt(hauteur*largeur) * 2)
nbre_initial_plantes = int(input(f" - Entrez un nombre initial de plantes (inférieur à {max_plantes}) : ") or 700)
while nbre_initial_plantes < 0 or nbre_initial_plantes > max_plantes:
    print("Le nombre n'est pas dans l'intervalle")
    nbre_initial_plantes = int(input(f" - Entrez un nombre initial de plantes (inférieur à {max_plantes}) : "))"""

nbre_initial_lapins = 520
nbre_initial_renards = 22
nbre_initial_plantes = 700



colors: Dict = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "cyan": (0, 255, 255),
    "magenta": (255, 0, 255),
    "yellow": (255, 255, 0),
}

class Actor:
    _position: pygame.Vector2
    _speed: pygame.Vector2
    _dimension: Tuple[int, int]

    def __init__(self, position: pygame.Vector2, speed: pygame.Vector2, dimension: Tuple[int, int] = (10,10)) -> None:
        self._position = position
        self._speed = speed
        self._dimension = dimension

    @property
    def position(self) -> pygame.Vector2:
        return self._position

    @position.setter
    def position(self, position: pygame.Vector2) -> None:
        if position.x < 0 or position.y < 0:
            raise ValueError("each position values must be zero or positive")
        self._position = position

    @property
    def speed(self) -> pygame.Vector2:
        return self._speed

    @speed.setter
    def speed(self, speed: pygame.Vector2) -> None:
        self._speed = speed

    @property
    def dimension(self) -> Tuple[int, int]:
        return self._dimension

    @dimension.setter
    def dimension(self, dimension: Tuple[int, int]) -> None:
        if dimension[0] <= 0 or dimension[1] <= 0:
            raise ValueError("each dimension value must be positive")
        self._dimension = dimension


class ActorSprite(pygame.sprite.Sprite):
    _surface: pygame.Surface
    _actor: Actor
    _color: pygame.Color
    _image: pygame.Surface
    _rect: pygame.Rect

    def __init__(self, surface : pygame.Surface, position :pygame.Vector2, speed:pygame.Vector2, color_name: str) -> None:
        pygame.sprite.Sprite.__init__(self)
        self._surface = surface
        self.position = position
        self.speed = speed
        self._actor = Actor(self.position, self.speed)
        self._set_color(color_name)
        self._set_image()
        self._set_rect()

    @property
    def color(self) -> pygame.Color:
        return self._color

    def _set_color(self, color_name: str) -> None:
        if color_name not in pygame.color.THECOLORS.keys():
            raise ValueError("color must be in list of pygame.Color")
        self._color = pygame.Color(color_name)

    @property
    def image(self) -> pygame.Surface:
        return self._image

    def _set_image(self) -> None:
        image = pygame.Surface(self._actor.dimension)
        image.fill(pygame.Color("black"))
        image.set_colorkey(pygame.Color("black"))
        image.set_alpha(255)
        pygame.draw.rect(image, self.color, ((0, 0), image.get_size()), 5)
        # only the border will be drawn
        self._image = image

    @property
    def rect(self) -> pygame.Rect:
        return self._rect

    def _set_rect(self) -> None:
        rect = self.image.get_rect()
        rect.update(self._actor.position, self.image.get_size())
        self._rect = rect

    def update(self) -> None:
        pass


class ActorSpriteDrivenBySpeed(ActorSprite):
    def __init__(self, surface, position, speed, color_name: str) -> None:
        super().__init__(surface, position, speed, color_name)
        

    def update(self):
        #self._rect.clamp_ip(self._surface.get_rect())

        self._rect.move_ip(self._actor.speed) 
        if self._rect.x <= 0 or self._rect.x >= largeur-10 :
            self._actor.speed = (self._actor.speed[0] * -1, self._actor.speed[1])
            self._rect.move_ip(self._actor.speed) 
        if self._rect.y <= 0 or self._rect.y >= hauteur-10 :
            self._actor.speed = (self._actor.speed[0], self._actor.speed[1] * -1)
            self._rect.move_ip(self._actor.speed) 

        self._actor.position = pygame.Vector2(self._rect.topleft)











        




