from pygame_structure import *
from random import randint
from main import nbre_initial_plantes

class Etres_vivants(ActorSpriteDrivenBySpeed):

    # Définition des variables concernant les lapins et les renards 
    energie_initiale_renards: int = 100        # Energie initiale
    energie_initiale_lapins: int = 80

    energie_deplacement_renard = 2              # Energie perdue par déplacement
    energie_deplacement_lapin = 1

    energie_reproduction_renards = 2            # Energie perdue pour la reproduction
    energie_reproduction_lapins = 1

    energie_max_renards = 50                     # Energie maximum
    energie_max_lapins = 20

    taille_portee_max_renards = 5               # Nombre de petits maximum par portée
    taille_portee_max_lapins = 3

    age_max_renards = 3                         # Age maximum 
    age_max_lapins = 5


    def __init__(self, surface: pygame.Surface, position: pygame.Vector2, speed: pygame.Vector2, color) -> None:
        super().__init__(surface, position, speed, color)

   

    def creer(self, classe, individus_sprites: pygame.sprite.Group, actors_sprites: pygame.sprite.Group, 
              surface: pygame.Surface, nbre_a_cree: int, liste_positions_all_individus: list = [],):
        
        if liste_positions_all_individus == []:
           liste_positions_all_individus = [individu.rect.topleft for individu in individus_sprites]

        if individus_sprites == self._lapins_sprites :
            energie_initiale = Etres_vivants.energie_initiale_lapins

        if individus_sprites == self._renards_sprites :
            energie_initiale = Etres_vivants.energie_initiale_renards
            

        if individus_sprites == self._plantes_sprites :
            energie_initiale = None


        for _ in range(nbre_a_cree) :
            actor_position = pygame.Vector2(randint(1, ((largeur-10)//10))*10, randint(1, ((hauteur-10)//10))*10)
            actor_speed = pygame.Vector2(randint(-1, 1), randint(-1, 1))
 
            while actor_position in liste_positions_all_individus :    # Vérifie que les individus ne spown pas les uns sur les autres (surtout pour les plantes)
                    actor_position = pygame.Vector2(randint(1, ((largeur-10)//10))*10, randint(1, ((hauteur-10)//10))*10)
            liste_positions_all_individus.append(actor_position)

            if energie_initiale == None :       # S'il n'y a pas d'argument energie, c'est une plante
                individu = classe(surface, pygame.Vector2(randint(0, ((largeur-10)//10))*10, randint(0, ((hauteur-10)//10))*10), (0,0))

            else :                                       
                individu = classe(energie_initiale, 0, surface, actor_position, actor_speed)

            actors_sprites.add(individu)
            individus_sprites.add(individu)




class Animaux(Etres_vivants):
    _energie : int
    _age : int

    def __init__(self, energie: int, age: int, surface: pygame.Surface, position: pygame.Vector2, speed: pygame.Vector2, color) -> None:
        super().__init__(surface, position, speed, color)
        self._energie = energie
        self._age = age


    def predateur_mange_proie(self, predateurs_sprites: pygame.sprite.Group, proies_sprites: pygame.sprite.Group) :
        collision = pygame.sprite.groupcollide(predateurs_sprites, proies_sprites, False, True)
        for predateur, proies in collision.items():
            if predateurs_sprites == self._renards_sprites :
                if predateur._energie < Etres_vivants.energie_max_renards:  
                    for proie in proies :
                        predateur._energie += (randint(10, 100)/100) * proie._energie
                        

            if predateurs_sprites == self._lapins_sprites :
                if predateur._energie < Etres_vivants.energie_max_lapins:  
                    predateur._energie += 3
       


    def reproduction(self, classe, individus_sprites, actors_sprites, surface):
        collision = pygame.sprite.groupcollide(individus_sprites, individus_sprites, False, False)
        
        if individus_sprites == self._renards_sprites :
            energie_perdue = Etres_vivants.energie_reproduction_renards
            taille_portee_max = Etres_vivants.taille_portee_max_renards

        if individus_sprites == self._lapins_sprites :
            energie_perdue = Etres_vivants.energie_reproduction_lapins
            taille_portee_max = Etres_vivants.taille_portee_max_lapins


        couples = []
        reproduction_max = 10      # Bloque le nombre de reproductions à 10 maximum pour éviter de surcharger la simulation

        for individu1, individus_en_collision_avec_individu1 in collision.items():
            for individu2 in individus_en_collision_avec_individu1 :
                if (individu1 != individu2 
                    and ((individu1,individu2) not in couples) and ((individu2,individu1) not in couples)
                    and individu1._age >=2 and individu2._age >=2
                    and individu1._energie > energie_perdue and individu2._energie > energie_perdue) :
                        
                        individu1._energie -= energie_perdue
                        individu2._energie -= energie_perdue        
                

                        couples.append((individu1, individu2))


        if len(couples) > reproduction_max:
            couples = couples[:reproduction_max]

        for _ in couples:
            nbre_petits = randint(1, taille_portee_max)
            Animaux.creer(self, classe, individus_sprites, actors_sprites, surface, nbre_petits)
                    
                
                

class Renard(Animaux):

    def __init__(self, energie: int, age: int, surface: pygame.Surface, position: pygame.Vector2, speed: pygame.Vector2, color = "red") -> None:
        super().__init__(energie, age, surface, position, speed, color)
        

class Lapin(Animaux):

    def __init__(self, energie: int, age: int, surface: pygame.Surface,position: pygame.Vector2, speed: pygame.Vector2, color="white") -> None:
        super().__init__(energie, age, surface, position, speed, color)   
                

class Plante(Etres_vivants):

    def __init__(self, surface: pygame.Surface, position: pygame.Vector2, speed: pygame.Vector2, color="green" ) -> None:
        super().__init__(surface,position, speed, color)

    def reset_plantes(self, surface, plantes_sprites, actors_sprites, nbre_initial_plantes) -> None :
        nbre_actuel_plantes = len(plantes_sprites)
        nbre_plantes_manquantes = nbre_initial_plantes - nbre_actuel_plantes 

        Plante.creer(self, Plante, plantes_sprites, actors_sprites, surface, nbre_plantes_manquantes, liste_positions_all_individus=[plante.rect.topleft for plante in plantes_sprites],)    





