import pygame

#helper
def ray_vs_rect(ray_origin, ray_dir, target):
    if ray_dir.x == 0 or ray_dir.y == 0:
        raise ZeroDivisionError
    t_near = (pygame.Vector2(target.topleft) - ray_origin).elementwise() / ray_dir
    t_far = (pygame.Vector2(target.topleft) + target.size - ray_origin).elementwise() / ray_dir

    if t_near.x > t_far.x:
        (t_near.x, t_far.x) = (t_far.x, t_near.x)
    if t_near.y > t_far.y:
        (t_near.y, t_far.y) = (t_far.y, t_near.y)
    
    if t_near.x > t_far.y or t_near.y > t_far.x:
        return (False, None, None, None)
    
    t_hit_near = max(t_near.x, t_near.y)
    t_hit_far = min(t_far.x, t_far.y)

    if t_hit_far < 0 :
        return (False, None, None, None)
    contact_point = ray_origin + t_hit_near * ray_dir

    if t_near.x >= t_near.y:
        if ray_dir.x < 0:
            contact_normal = (1, 0)
        else: 
            contact_normal = (-1, 0)
    elif t_near.x < t_near.y:
        if ray_dir.y < 0:
            contact_normal = (0, 1)
        else: 
            contact_normal = (0, -1)

    return (True, contact_point, contact_normal, t_hit_near)

    
class Player:
    def __init__(self):
        self.position: pygame.Vector2 = pygame.Vector2(0,0)
        self.velocity: pygame.Vector2 = pygame.Vector2(0,0)
        self.width = 16
        self.height = 16
        self.rect = pygame.Rect((240,240), (self.width, self.height))
        self.is_grounded = False
        self.jump_count = 0
        self.spawned = False
        self.wall_surface_normal = 0 
        self.can_dash = False
        self.can_wall_jump = False
    
    def jump(self):
        if self.can_wall_jump and not self.is_grounded:
            self.velocity.y = -350
            self.velocity.x += self.wall_surface_normal * 500
            self.can_wall_jump = False
        elif self.jump_count < 2:
            self.jump_count += 1
            if self.jump_count == 1:
                self.velocity.y = -250
            elif self.jump_count == 2:
                self.velocity.y = -250
            
    def update(self, dt, level):    
        self.is_grounded = False
        if not self.spawned:
            self.position = level.spawn_point.copy()
            self.velocity = pygame.Vector2(0,0)
            self.spawned = True
        GRAVITY = 980
        keys = pygame.key.get_pressed()
        self.velocity.x *= 0.9

        #Basic Controls: WASD or arrow keys
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity.x += -25
            
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity.x += 25 
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.jump()
        self.velocity.y += GRAVITY  * dt 
        
        #detect and resolve collision against each platform
        for p in level.platforms:
            (collision, point, normal, time) = self._vs_rect(p, dt)
            if collision:
                self.velocity -= self.velocity.dot(normal) * pygame.Vector2(normal)
                #if the surface normal of the collided object is up, we're on the ground
                if normal[1] == -1:
                    self.is_grounded = True

                #If we have collided with an object on it's left or right side and we're not grounded,
                # we can wall jump
                if normal[0] != 0 and not self.is_grounded:
                    self.can_wall_jump = True
                    self.wall_surface_normal = normal[0]
     
        if self.is_grounded:
            self.jump_count = 0
            self.can_wall_jump = False
        
        self.position += self.velocity * dt      
        self.rect.topleft = self.position
     
        for i in level.items:
            if self.rect.colliderect(i.rect):
                i.behaviour(self, level)
        
        if keys[pygame.K_r] or level.finished:
            self.spawned = False 

    #Swept AABB collision
    def _vs_rect(self, other, dt):
        if self.velocity.x == 0 and self.velocity.y == 0:
            return (False, None, None, None)
        epsilon = 1e-8
        vel = pygame.Vector2(
            self.velocity.x if self.velocity.x != 0 else epsilon,
            self.velocity.y if self.velocity.y != 0 else epsilon
        )
        
        expanded_target = pygame.Rect(0, 0, 0, 0)
        expanded_target.topleft = pygame.Vector2(other.topleft) - pygame.Vector2(self.rect.size) / 2
        expanded_target.size = pygame.Vector2(other.size) + pygame.Vector2(self.rect.size)

        try:
            (collision, point, normal, time) = ray_vs_rect(pygame.Vector2(self.rect.center), vel * dt, expanded_target)
        except:
            pass
        else:
            if collision and 0 <= time < 1:
                return (collision, point, normal, time)
        return (False, None, None, None)
              
    def render(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)
    
        
