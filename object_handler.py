from sprites_obj import *

class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.static_sprite_path = 'sprites/'
        self.anim_sprite_path = 'animsprites/'
        add_sprite = self.Add_sprite

        add_sprite(SpriteObject(game))
        add_sprite(AnimatedSprite(game))
        
        
    def update(self):
        [sprite.update() for sprite in self.sprite_list]

    def Add_sprite(self, sprite):
        self.sprite_list.append(sprite)