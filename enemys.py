import pygame as pg
from sprites_obj import *
from random import randint, random, choice

class NPC(AnimatedSprite):
    def __init__(self, game, path='sprites/Enemys/1.png', pos=(7.5, 3.5), scale=0.6, shift=0.38, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.walk_images = self.get_images(self.path + '/walk')
        self.idle_images = self.get_images(self.path + '/idle')

        self.attack_dist = randint(3, 6)
        self.speed = 0.03
        self.size = 10
        self.health = 45
        self.attack_damage = 5
        self.accuracy = 0.15
        self.alive = True
        self.pain = False
        self.raycasting_value = False
        self.frame_counter = 0


    def update(self):
        self.check_animation_time()
        self.get_sprite()
        self.run_logic()

    def check_hit_in_enemy(self):
        if self.raycasting_value and self.game.player.shot:
            if HALF_WIDTH - self.sprite_half_width < self.screen_x < HALF_WIDTH + self.sprite_half_width:
                self.game.sound.npc_pain.play()
                self.game.player.shot = False
                self.pain = True
                self.health -= self.game.shotgun.damage
                self.check_healthPoints()

    

    def check_healthPoints(self):
        if self.health < 1:
            self.alive = False
            self.game.sound.npc_death.play()


    def run_logic(self):
        if self.alive:
            self.raycasting_value = self.ray_cast_player_npc()
            self.check_hit_in_enemy()
            self.animate(self.idle_images)
        


    @property
    def map_pos(self):
        return int(self.x), int(self.y)

    def ray_cast_player_npc(self):
        if self.game.player.map_pos == self.map_pos:
            return True
        
        wall_dist_v, wall_dist_h = 0, 0
        player_dist_v, player_dist_h = 0, 0

        self.ray_casting_result = []
        texture_vert, texture_hor = 1, 1
        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        ray_angle = self.theta
        
        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

            # horizontals
        y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)

        depth_hor = (y_hor - oy) / sin_a
        x_hor = ox + depth_hor * cos_a

        delta_depth = dy / sin_a
        dx = delta_depth * cos_a

        for i in range(MAX_DEPTH):
            tile_hor = int(x_hor), int(y_hor)
            if tile_hor == self.map_pos:
                player_dist_v = depth_hor
            if tile_hor in self.game.map.world_map:
                wall_dist_h = depth_hor
                break
            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth

            # verticals
            x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)

            depth_vert = (x_vert - ox) / cos_a
            y_vert = oy + depth_vert * sin_a

            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            for i in range(MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert == self.map_pos:
                    player_dist_v == depth_vert
                    break
                if tile_vert in self.game.map.world_map:
                    wall_dist_v = depth_vert
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth
        player_dist = max(player_dist_v, player_dist_h)
        wall_dist = max(wall_dist_v, wall_dist_h)

        if 0 < player_dist < wall_dist or not wall_dist:
            return True
        return False