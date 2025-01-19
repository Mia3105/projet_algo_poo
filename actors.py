from pygame_1 import *
from random import randint
from main import nbre_initial_plantes

class Etres_vivants(ActorSpriteDrivenBySpeed):
    energie_initiale_renards: int = 25
    energie_initiale_lapins: int = 10

    def __init__(self, surface: pygame.Surface, position: pygame.Vector2, speed: pygame.Vector2, color) -> None:
        super().__init__(surface, position, speed, color)

   

    def creer(self, classe, individus_sprites: pygame.sprite.Group, actors_sprites: pygame.sprite.Group, 
              surface: pygame.Surface, nbre_initial: int, liste_positions_all_individus: list = [],):
        
        if liste_positions_all_individus == []:
           liste_positions_all_individus = [individu.rect.topleft for individu in individus_sprites]

        if individus_sprites == self._lapins_sprites :
            energie_initiale = Etres_vivants.energie_initiale_lapins

        if individus_sprites == self._renards_sprites :
            energie_initiale = Etres_vivants.energie_initiale_renards

        if individus_sprites == self._plantes_sprites :
            energie_initiale = None


        for _ in range(nbre_initial) :
            actor_position = pygame.Vector2(randint(1, ((largeur-10)//10))*10, randint(1, ((hauteur-10)//10))*10)
            actor_speed = pygame.Vector2(randint(-1, 1), randint(-1, 1))
 
            while actor_position in liste_positions_all_individus :    # Vérifie que les individus ne spown pas les uns sur les autres (surtout pour les plantes)
                    actor_position = pygame.Vector2(randint(1, ((largeur-10)//10))*10, randint(1, ((hauteur-10)//10))*10)
            liste_positions_all_individus.append(actor_position)

            if energie_initiale == None :       # S'il n'y a pas d'argument energie, c'est une plante
                individu = classe(surface, actor_position, (0,0))

            else :                                       
                individu = classe(energie_initiale, surface, actor_position, actor_speed)

            actors_sprites.add(individu)
            individus_sprites.add(individu)




class Animaux(Etres_vivants):
    _energie : int

    def __init__(self, energie: int, surface: pygame.Surface, position: pygame.Vector2, speed: pygame.Vector2, color) -> None:
        super().__init__(surface, position, speed, color)
        self._energie = energie


    def predateur_mange_proie(predateurs_sprites: pygame.sprite.Group, proies_sprites: pygame.sprite.Group, energie_max: int):
        collision = pygame.sprite.groupcollide(predateurs_sprites, proies_sprites, False, True)
        for predateur, proies in collision.items():
            if predateur._energie < energie_max:  
                if type(predateur) == Lapin :
                    predateur._energie += 3 
                if type(predateur) == Renard :
                    for proie in proies :
                        predateur._energie += 0.75 * proie._energie
                

    def reproduction(self, classe, individus_sprites, actors_sprites, surface):
        collision = pygame.sprite.groupcollide(individus_sprites, individus_sprites, False, False)
        
        if individus_sprites == self._lapins_sprites :
            energie_perdue = 2
            taille_portee_max = 3

        if individus_sprites == self._renards_sprites :
            energie_perdue = 4
            taille_portee_max = 5
            

        for individu1, individus_en_collision_avec_individu1 in collision.items():
            for individu2 in individus_en_collision_avec_individu1 :
                individu1._energie -= energie_perdue
                individu2._energie -= energie_perdue        

        nbre_petits = randint(1, taille_portee_max)
        Animaux.creer(self, classe, individus_sprites, actors_sprites, surface, nbre_petits)
                
                

        

class Renard(Animaux):

    def __init__(self, energie: int, surface: pygame.Surface, position: pygame.Vector2, speed: pygame.Vector2, color = "red") -> None:
        super().__init__(energie, surface, position, speed, color)
        

class Lapin(Animaux):

    def __init__(self, energie: int, surface: pygame.Surface,position: pygame.Vector2, speed: pygame.Vector2, color="white") -> None:
        super().__init__(energie, surface, position, speed, color)   
                

class Plante(Etres_vivants):

    def __init__(self, surface: pygame.Surface, position: pygame.Vector2, speed: pygame.Vector2, color="green" ) -> None:
        super().__init__(surface,position, speed, color)

    def reset_plantes(self, surface, plantes_sprites, actors_sprites, nbre_initial_plantes) -> None :
        nbre_actuel_plantes = len(plantes_sprites)
        nbre_plantes_manquantes = nbre_initial_plantes - nbre_actuel_plantes 

        Plante.creer(self, Plante, plantes_sprites, actors_sprites, surface, nbre_plantes_manquantes, liste_positions_all_individus=[plante.rect.topleft for plante in plantes_sprites],)    





