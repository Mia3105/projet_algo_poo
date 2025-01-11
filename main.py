from pygame_1 import *
from actors import *

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


    def __init_actors(self) -> None:
        self.__actors_sprites = pygame.sprite.Group()
        self.__renards_sprites = pygame.sprite.Group()
        self.__lapins_sprites = pygame.sprite.Group()
        self.__plantes_sprites = pygame.sprite.Group()
           
        Etres_vivants.creer(self, Renard, self.__renards_sprites, self.__actors_sprites, self.__screen, nbre_initial_renards, 25)
        Etres_vivants.creer(self, Lapin, self.__lapins_sprites, self.__actors_sprites, self.__screen, nbre_initial_lapins, 10)
        Etres_vivants.creer(self, Plante, self.__plantes_sprites, self.__actors_sprites, self.__screen, nbre_initial_plantes)


    def __update_actors(self) -> None:
        self.__actors_sprites.update()

        Animaux.predateur_mange_proie(self.__lapins_sprites, self.__plantes_sprites, 20)
        Animaux.predateur_mange_proie(self.__renards_sprites, self.__lapins_sprites, 50) 




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



    

    

if __name__ == "__main__":
    app = App()
    app.execute()
