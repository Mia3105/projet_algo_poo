from pygame_1 import *

class Etres_vivants(ActorSpriteDrivenBySpeed):

    def __init__(self, surface: pygame.Surface, position: pygame.Vector2, speed: pygame.Vector2, color = "red") -> None:
        super().__init__(surface, position, speed, color)

    def creer(self, classe, individus_sprites, actors_sprites, surface, nbre_initial_lapins: int , energie_initiale: int = None):
        
        for _ in range(nbre_initial_lapins) :
            actor_position = pygame.Vector2(randint(1, ((largeur-10)//10))*10, randint(1, ((hauteur-10)//10))*10)
            actor_speed = pygame.Vector2(randint(-1, 1), randint(-1, 1))
            liste_position_individus = []
            while actor_position in liste_position_individus :    
                    actor_position = pygame.Vector2(randint(1, ((largeur-10)//10))*10, randint(1, ((hauteur-10)//10))*10)
            liste_position_individus.append(actor_position)
            if energie_initiale == None :
                individu = classe(surface, actor_position, (0,0))
            else :
                individu = classe(energie_initiale, surface, actor_position, actor_speed)

            actors_sprites.add(individu)
            individus_sprites.add(individu)




class Animaux(ActorSpriteDrivenBySpeed):
    _energie : int

    def __init__(self, energie: int, surface: pygame.Surface, position: pygame.Vector2, speed: pygame.Vector2, color) -> None:
        super().__init__(surface, position, speed, color)
        self._energie = energie


    def predateur_mange_proie(predateurs_sprites: Etres_vivants, proies_sprites: Etres_vivants, energie_max: int):
        collision = pygame.sprite.groupcollide(predateurs_sprites, proies_sprites, False, True)
        for predateur, proies in collision.items():
            if predateur._energie < energie_max:  
                if type(predateur) == Lapin :
                    predateur._energie += 3 
                if type(predateur) == Renard :
                    for proie in proies :
                        predateur._energie += 0.75 * proie._energie
                


    def reproduction(individus_sprites, energie_perdue: int, taille_portee_max: int):
        collision = pygame.sprite.groupcollide(individus_sprites, individus_sprites, False, False)
        for individu1, individus_en_collision_avec_individu1 in collision.items():
            for individu2 in individus_en_collision_avec_individu1 :
                individu1._energie -= energie_perdue
                individu2._energie -= energie_perdue
                
                """for _ in range(randint(0,taille_portee_max)) :
                    actor_position = pygame.Vector2(randint(1, ((largeur-10)//10))*10, randint(1, ((hauteur-10)//10))*10)
                    actor_speed = pygame.Vector2(randint(-1, 1), randint(-1, 1))
                    plante = Plante(self.__screen, actor_position, actor_speed)            
                    while actor_position in list_position_plante :    # vérifier que les plantes ne spown pas les unes sur les autres
                            actor_position = pygame.Vector2(randint(1, ((largeur-10)//10))*10, randint(1, ((hauteur-10)//10))*10)
                    list_position_plante.append(actor_position)
                    self.__actors_sprites.add(plante)
                    self.__plantes_sprites.add(plante)"""
            

    
        
        
        

class Renard(Animaux):

    def __init__(self, energie: int, surface: pygame.Surface, position: pygame.Vector2, speed: pygame.Vector2, color = "red") -> None:
        super().__init__(energie, surface, position, speed, color)
        

class Lapin(Animaux):

    def __init__(self, energie: int, surface: pygame.Surface,position: pygame.Vector2, speed: pygame.Vector2, color="white") -> None:
        super().__init__(energie, surface, position, speed, color)   
                

class Plante(ActorSpriteDrivenBySpeed):

    def __init__(self, surface: pygame.Surface,position: pygame.Vector2, speed: pygame.Vector2, color="green" ) -> None:
        super().__init__(surface,position, speed, color)

      





