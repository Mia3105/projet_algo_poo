from pygame_1 import *

class Animaux(ActorSpriteDrivenBySpeed):
    _energie : int

    def __init__(self, energie: int, surface: pygame.Surface, position: pygame.Vector2, speed: pygame.Vector2, color = "red") -> None:
        super().__init__(surface, position, speed, color)
        self._energie = energie


    def predateur_mange_proie(predateurs_sprites, proies_sprites, energie_max):
        collision = pygame.sprite.groupcollide(predateurs_sprites, proies_sprites, False, True)
        for predateur, proies in collision.items():
            if predateur._energie < energie_max:  
                if type(predateur) == Lapin :
                    predateur._energie += 3 
                if type(predateur) == Renard :
                    for proie in proies :
                        predateur._energie += 0.75 * proie._energie
                


    """def reproduction(especes_sprites):
        collision = pygame.sprite.groupcollide(especes_sprites, especes_sprites, False, False)
        for individu, individus_en_collision_avec_individu in collision.items():
            if renard._energie < 30: 
                renard._energie += 5  
                for lapin in lapins:
                    self.__lapins_sprites.remove(lapin) """

    
        
        
        

class Renard(Animaux):

    def __init__(self, energie: int, surface: pygame.Surface, position: pygame.Vector2, speed: pygame.Vector2, color = "red") -> None:
        super().__init__(energie, surface, position, speed, color)
        


class Lapin(Animaux):

    def __init__(self, energie: int, surface: pygame.Surface,position: pygame.Vector2, speed: pygame.Vector2, color="white") -> None:
        super().__init__(energie, surface, position, speed, color)
        
    
    
                



class Plante(ActorSpriteDrivenBySpeed):

    def __init__(self, surface: pygame.Surface,position: pygame.Vector2, speed: pygame.Vector2, color="green" ) -> None:
        super().__init__(surface,position, speed, color)

      





