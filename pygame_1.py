import pygame
from sys import exit
from random import randint
from typing import Tuple, Dict


hauteur = 400
largeur = 400
WINDOW_SIZE: Tuple[int, int] = (largeur, hauteur)
WINDOW_TITLE: str = "pygame window"
FPS = 12



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



class Renard(ActorSpriteDrivenBySpeed):
    _energie : int

    def __init__(self, energie: int, surface: pygame.Surface, position: pygame.Vector2, speed: pygame.Vector2, color = "red") -> None:
        super().__init__(surface, position, speed, color)
        self._energie = energie



class Lapin(ActorSpriteDrivenBySpeed):
    _energie : int

    def __init__(self, energie: int, surface: pygame.Surface,position: pygame.Vector2, speed: pygame.Vector2, color="white") -> None:
        super().__init__(surface, position, speed, color)
        self._energie = energie



class Plante(ActorSpriteDrivenBySpeed):
    energie : int

    def __init__(self, surface: pygame.Surface,position: pygame.Vector2, speed: pygame.Vector2, color="green" ) -> None:
        super().__init__(surface,position, speed, color)



class App:
    __window_size: Tuple[int, int] = WINDOW_SIZE
    __window_title: str = WINDOW_TITLE
    __screen: pygame.Surface = None
    __running: bool = False
    __clock: pygame.time.Clock = pygame.time.Clock()
    __FPS: int = FPS

    __actors_sprites: pygame.sprite.Group

    def __init__(self) -> None:
        pygame.init()
        self.__init_screen()
        self.__init_actors()
        self.__running = True

    def __init_screen(self) -> None:
        self.__screen = pygame.display.set_mode(self.__window_size)
        pygame.display.set_caption(self.__window_title)

    def __handle_events(self, event) -> None:
        if event.type == pygame.QUIT:
            self.__running = False
            pygame.quit()
            exit()

    def __update_actors(self) -> None:
        self.__actors_sprites.update()
        

    def __draw_screen(self) -> None:
        self.__screen.fill(pygame.color.THECOLORS["black"])

    def __draw_actors(self) -> None:
        self.__actors_sprites.draw(self.__screen)

    def execute(self) -> None:
        while self.__running:
            self.__clock.tick(self.__FPS)
            for event in pygame.event.get():
                self.__handle_events(event)
            self.__update_actors()
            self.__draw_screen()
            self.__draw_actors()
            pygame.display.flip()

    def __init_actors(self) -> None:
        self.__actors_sprites = pygame.sprite.Group()
        self.__renards_sprites = pygame.sprite.Group()
        self.__lapins_sprites = pygame.sprite.Group()
        self.__plantes_sprites = pygame.sprite.Group()


        
        for _ in range(22) :
            actor_position = pygame.Vector2(randint(0, ((hauteur-10)//10))*10, randint(0, ((largeur-10)//10))*10)
            actor_speed = pygame.Vector2(randint(-1, 1), randint(-1, 1))
            renard = Renard(self.__screen, 25, actor_position, actor_speed)
            self.__actors_sprites.add(renard)
            self.__renards_sprites.add(renard)

            

        for _ in range(520) :
            actor_position = pygame.Vector2(randint(0, ((hauteur-10)//10))*10, randint(0, ((largeur-10)//10))*10)
            actor_speed = pygame.Vector2(randint(-1, 1), randint(-1, 1))
            lapin = Lapin(self.__screen, 10, actor_position, actor_speed)
            self.__actors_sprites.add(lapin)
            self.__lapins_sprites.add(lapin)
 

        list_position_plante = []
        for _ in range(700) :
            actor_position = pygame.Vector2(randint(0, ((hauteur-10)//10))*10, randint(0, ((largeur-10)//10))*10)
            actor_speed = (0,0)
            plante = Plante(self.__screen, actor_position, actor_speed)            
            while actor_position in list_position_plante :    # vérifier que les plantes ne spown pas les unes sur les autres
                    actor_position = pygame.Vector2(randint(0, ((hauteur-10)//10))*10, randint(0, ((largeur-10)//10))*10)
            list_position_plante.append(actor_position)
            self.__actors_sprites.add(plante)
            self.__plantes_sprites.add(plante)





        




