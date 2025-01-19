from pygame_structure import *
from actors import *

class App:
    __window_size: Tuple[int, int] = WINDOW_SIZE
    __window_title: str = WINDOW_TITLE
    __screen: pygame.Surface = None
    __running: bool = False
    __clock: pygame.time.Clock = pygame.time.Clock()
    __FPS: int = FPS
    __compteur_actions: int = 0
    __longueur_cycle: int = 20
    __cycle: int = 1

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
        self._renards_sprites = pygame.sprite.Group()
        self._lapins_sprites = pygame.sprite.Group()
        self._plantes_sprites = pygame.sprite.Group()
       
        Animaux.creer(self, Renard, self._renards_sprites, self.__actors_sprites, self.__screen, nbre_initial_renards)
        Animaux.creer(self, Lapin, self._lapins_sprites, self.__actors_sprites, self.__screen, nbre_initial_lapins)
        Etres_vivants.creer(self, Plante, self._plantes_sprites, self.__actors_sprites, self.__screen, nbre_initial_plantes)


    def __update_actors(self) -> None:
        self.__actors_sprites.update()

        for renard in self._renards_sprites :
            renard._energie -= Etres_vivants.energie_deplacement_renard
            if renard._energie <= 0 :
                renard.kill()
                
        for lapin in self._lapins_sprites :
            lapin._energie -= Etres_vivants.energie_deplacement_lapin
            if lapin._energie <= 0 :
                lapin.kill()
        

        self.__compteur_actions += 1

        Animaux.predateur_mange_proie(self, self._renards_sprites, self._lapins_sprites) 
        Animaux.predateur_mange_proie(self, self._lapins_sprites, self._plantes_sprites)

        
        Animaux.reproduction(self, Renard, self._renards_sprites, self.__actors_sprites, self.__screen)
        Animaux.reproduction(self, Lapin, self._lapins_sprites, self.__actors_sprites, self.__screen)


        if self.__compteur_actions >= self.__longueur_cycle:
            if self.__cycle == 1 :
                print(f"Fin du {self.__cycle}er cycle.")
            else :
                print(f"Fin du {self.__cycle}ème cycle.")
            print(f"Il y a {len(self._renards_sprites)} renards et {len(self._lapins_sprites)} lapins")
            print("----------")

            self.__cycle += 1
            Plante.reset_plantes(self, self.__screen, self._plantes_sprites, self.__actors_sprites, nbre_initial_plantes)
            self.__compteur_actions = 0

            for renard in self._renards_sprites :
                renard._age += 1
                if renard._age >= Etres_vivants.age_max_renards :
                    renard.kill()

            for lapin in self._lapins_sprites :
                lapin._age += 1
                if lapin._age >= Etres_vivants.age_max_lapins :
                    lapin.kill()


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
