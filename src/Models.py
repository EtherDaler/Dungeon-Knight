import pygame

from . import settings
from pygame.math import Vector2 as vec


class Sprite:
    """
    Родительский Класс для всех Спрайтов
    """

    hp = 0          # Шкала здоровья
    armor = 0       # Броня
    speed = 0       # Скорость передвижения
    view_range = 0  # Дальность обзора
    level = 0       # Уровень
    xp = 0          # Опыт
    kills = 0       # Убийства
    xp_need = 0     # Необходимо опыта, чтобы перейти на следущий уровень
    hand = True     # Ближний бой
    weapon = None   # Оружие
    bullets = 0     # Патроны
    live = True     # Живой/Мертвый
    coords = [0, 0] # Позиция
    sheet = None    # Моделька Спрайта
    orientation = 0 # То в какую сторону смотрит спрайт, всего 8 направлений
    p_speed = 0
    an_or = {0: 4,
             1: 3,
             2: 2,
             3: 1,
             4: 0,
             5: 7,
             6: 6,
             7: 5} # Фрейм анимации для ориентации
    stanned = False # Состояние оглушения

    # Получение нужного фрейма спрайта с ассета
    def get_image(self, frame_x: int, frame_y: int, width: int, height: int, scale: int, colour: tuple):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0),
                   ((frame_x * width), (frame_y * height), (frame_x * width + width), (frame_y * height + height)))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(colour)

        return image

    """
    Анимации спрайта
    :param kwargs: сюда передаются все изображения для анимации
    Важно: Анимация должна работать для всех направлений
    """

    # Анимация стоячего спрайта
    def animation_stay(self):
        return [self.get_image(i, self.an_or[self.orientation], settings.PX, settings.PX, 2, settings.BLACK) for i in range(0, 2)]

    # Анимация атаки
    def animation_atack(self):
        return [self.get_image(i, self.an_or[self.orientation], settings.PX, settings.PX, 2, settings.BLACK) for i in range(4, 7)]

    # Анимация ходьбы
    def animation_walk(self):
        return [self.get_image(i, self.an_or[self.orientation], settings.PX, settings.PX, 2, settings.BLACK) for i in range(2, 4)]

    # Анимация стрельбы
    def animation_fire(self):
        return [self.get_image(i, self.an_or[self.orientation], settings.PX, settings.PX, 2, settings.BLACK) for i in range(8, 12)]

        # Анимация смерти

    def animation_death(self):
        return [self.get_image(i, self.an_or[self.orientation], settings.PX, settings.PX, 2, settings.BLACK) for i in range(20, 24)]

        # Анимация победы
    def animation_win(self):
        return [self.get_image(i, self.an_or[self.orientation], settings.PX, settings.PX, 2, settings.BLACK) for i in range(15, 19)]
    """
    Методы отвечающие за движение
    """
    def move_bullets(self):
        for i in self.weapon:
            if i.on_fly is False:
                i.coords = self.coords
                i.f_coords = self.coords
                i.orientation = self.orientation

    def move_front(self, walls: list):
        can_walk = True
        if self.stanned == True:
            can_wlk = False
        cell_width = settings.MAZE_WIDTH // 28
        cell_height = settings.MAZE_HEIGHT // 30
        for wall in walls:
            if (self.coords[0] // cell_width, (self.coords[1] - self.speed - 1) // cell_height) == wall:
                can_walk = False
        if can_walk:
            self.coords[1] -= self.speed
        self.orientation = 0
        if self.hand is False:
            self.move_bullets()

    def move_back(self, walls: list):
        can_walk = True
        if self.stanned == True:
            can_wlk = False
        cell_width = settings.MAZE_WIDTH // 28
        cell_height = settings.MAZE_HEIGHT // 30
        for wall in walls:
            if (self.coords[0] // cell_width, (self.coords[1] + self.speed + 1) // cell_height) == wall:
                can_walk = False
        if can_walk:
            self.coords[1] += self.speed
        self.orientation = 4
        if self.hand is False:
            self.move_bullets()

    def move_right(self, walls: list):
        can_walk = True
        if self.stanned == True:
            can_wlk = False
        cell_width = settings.MAZE_WIDTH // 28
        cell_height = settings.MAZE_HEIGHT // 30
        for wall in walls:
            if ((self.coords[0] + self.speed + 1) // cell_width, self.coords[1] // cell_height) == wall:
                can_walk = False
        if can_walk is True:
            self.coords[0] += self.speed
        self.orientation = 2
        if self.hand is False:
            self.move_bullets()

    def move_left(self, walls: list):
        can_walk = True
        if self.stanned == True:
            can_wlk = False
        cell_width = settings.MAZE_WIDTH // 28
        cell_height = settings.MAZE_HEIGHT // 30
        for wall in walls:
            if ((self.coords[0] - self.speed - 1) // cell_width, self.coords[1] // cell_height) == wall:
                can_walk = False
        if can_walk is True:
            self.coords[0] -= self.speed
        self.orientation = 6
        if self.hand is False:
            self.move_bullets()

    def move_diag(self, x: str, y: str):
        """
        :param x: принимает +-
        :param y: принимает +-
        если один из параметров положительный, то спрайт движется в положительную сторону по этой оси,
        если отрицательный, то наоборот
        """
        can_walk = True
        if x == '+':
            if y == '+':
                self.orientation = 1
            else:
                self.orientation = 3
        else:
            if y == '+':
                self.orientation = 7
            else:
                self.orientation = 5
        if self.hand is False:
            self.move_bullets()

    """
    Атака и получение урона
    """
    # Получение урона
    def get_damage(self, damage: int):
        self.hp -= damage - (self.armor / 10)
        if self.hp <= 0:
            self.hp = 0
            self.animation_death()
            self.live = False
            return 1
        return 0

    # Атака в ближнем бою
    def attack(self, goal: object):
        can_atack = True
        if self.stanned == True:
            can_atack = False
        if can_atack:
            self.animation_atack()
            if goal is not None:
                self.kills += goal.get_damage(self.weapon.damage)

    def fire(self, goal: list, walls: list):
        """
        Стрельба
        :param goal: Для героя передается список всех врагов на карте
                     Для врагов передается список из одного элемента - героя
        :param walls: Передается список с координатами всех стен

        """
        cell_width = settings.MAZE_WIDTH // 28
        cell_height = settings.MAZE_HEIGHT // 30
        can_atack = True
        if self.stanned == True:
            can_atack = False
        if can_atack:
            self.animation_fire()
            self.weapon[-1].on_fly = True

            # Проверка не попал ли снаряд на край экрана
            if self.weapon[-1].coords[0] >= settings.WIDTH or self.weapon[-1].coords[0] <= 0:
                d = self.weapon.pop(self.weapon.index(self.weapon[-1]))
                self.weapon.append(Projectile_Weapon(d.range, d.speed, d.damage,
                                                         self.coords, self.orientation, d.image, False))

            # Проверка не попал ли снаряд на край экрана
            if self.weapon[-1].coords[1] >= settings.HEIGHT or self.weapon[-1].coords[1] <= 0:
                d = self.weapon.pop(self.weapon.index(self.weapon[-1]))
                self.weapon.append(Projectile_Weapon(d.range, d.speed, d.damage,
                                                         self.coords, self.orientation, d.image, False))

            # Проверка на дальность полета
            if self.weapon[-1].coords[0] >= self.weapon[-1].f_coords[0] + self.weapon[-1].range or \
                    self.weapon[-1].coords[1] >= self.weapon[-1].f_coords[1] + self.weapon[-1].range:
                d = self.weapon.pop(self.weapon.index(self.weapon[-1]))
                self.weapon.append(Projectile_Weapon(d.range, d.speed, d.damage,
                                                     self.coords, self.orientation, d.image, False))

            # Проверка на попадание в стену
            for wall in walls:
                if (self.weapon[-1].coords[0] // cell_width, self.weapon[-1].coords[1] // cell_height) == wall:
                    d = self.weapon.pop(self.weapon.index(self.weapon[-1]))
                    self.weapon.append(Projectile_Weapon(d.range, d.speed, d.damage,
                                                         self.coords, self.orientation, d.image, False))

            # Проверка на попадание в спрайта
            for sprite in goal:
                if self.weapon[-1].coords == sprite.coords:
                    sprite.get_damage(self.weapon[-1].damage)
                    d = self.weapon.pop(self.weapon.index(self.weapon[-1]))
                    self.weapon.append(Projectile_Weapon(d.range, d.speed, d.damage,
                                                         self.coords, self.orientation, d.image, False))

            # Полет снаряда
            if self.weapon[-1].orientation == 0:
                self.weapon[-1].coords[1] += self.weapon[-1].speed
            elif self.weapon[-1].orientation == 1:
                self.weapon[-1].coords[0] += self.weapon[-1].speed
                self.weapon[-1].coords[1] += self.weapon[-1].speed
            elif self.weapon[-1].orientation == 2:
                self.weapon[-1].coords[0] += self.weapon[-1].speed
            elif self.weapon[-1].orientation == 3:
                self.weapon[-1].coords[0] += self.weapon[-1].speed
                self.weapon[-1].coords[1] -= self.weapon[-1].speed
            elif self.weapon[-1].orientation == 4:
                self.weapon[-1].coords[1] -= self.weapon[-1].speed
            elif self.weapon[-1].orientation == 5:
                self.weapon[-1].coords[0] -= self.weapon[-1].speed
                self.weapon[-1].coords[1] -= self.weapon[-1].speed
            elif self.weapon[-1].orientation == 6:
                self.weapon[-1].coords[0] -= self.weapon[-1].speed
            elif self.weapon[-1].orientation == 7:
                self.weapon[-1].coords[0] -= self.weapon[-1].speed
                self.weapon[-1].coords[1] += self.weapon[-1].speed

    def draw(self, animation: int):
        if animation == 1:
            return self.animation_stay()
        elif animation == 2:
            return self.animation_atack()
        elif animation == 3:
            return self.animation_walk()
        elif animation == 4:
            return self.animation_fire()
        elif animation == 5:
            return self.animation_death()
        elif animation == 6:
            return self.animation_win()
        return self.animation_stay()

class SpriteBuilder:
    """
        :image: моделька
        :coords: начальные координаты
        :hp: жизни
        :k_hp: коэфицент увеличения жизней
        :armor: броня
        :k_armor: коэфицент увеличения брони
        :speed: скорость передвижения
        :view_range: дальность обзора
        :level: уровень
        :live: состояние жив или мертв
        :hand: состояние ближнего боя
        :damage: урон
        :k_damage: коэфицент увеличений урона
        :range: дальность атаки
    """

    sprite = None

    def set_model(self, image):
        self.sprite.sheet = image
        return self

    def set_hp(self, hp, k_hp):
        self.sprite.hp = hp + (hp * self.sprite.level // k_hp)
        self.sprite.k_hp = k_hp
        return self

    def set_armor(self, armor, k_armor):
        self.sprite.armor = armor + (armor * self.sprite.level / k_armor)
        self.sprite.k_armor = k_armor
        return self

    def set_speed(self, speed):
        self.sprite.speed = speed 
        return self

    def set_damage(self, damage, k_damage):
        self.sprite.damage = damage
        self.sprite.k_damage = k_damage
        return self

    def set_coords(self, coords):
        self.sprite.coords = coords
        return self

    def set_xp(self, xp, xp_need, level):
        self.sprite.xp = xp 
        self.sprite.xp_need = xp_need
        self.sprite.level = level
        return self

    def set_sleeping(self, sleep):
        self.sprite.sleep = sleep
        return self

    def set_atack(self, hand, bullets, range_atack, p_speed, proj_img):
        self.sprite.hand = hand
        self.sprite.bullets = bullets
        self.sprite.range = range_atack
        self.sprite.p_speed = p_speed
        if hand is True:
            self.sprite.weapon = Simple_Weapon(
                self.sprite.damage + (self.sprite.damage * self.sprite.level // self.sprite.k_damage), 
                range_atack)
        else:
            self.sprite.weapon = []
            for i in range(self.sprite.bullets):
                self.sprite.weapon.append(Projectile_Weapon(range_atack, p_speed, 
                        self.sprite.damage + (self.sprite.damage * self.sprite.level // self.sprite.k_damage),
                        self.sprite.coords, self.sprite.orientation, proj_img, False))

        return self

    def set_no_level_depends(self, image, coords, speed, sleep):
        self.set_model(image)
        self.set_coords(coords)
        self.set_speed(speed)
        self.set_sleeping(sleep)

    def set_level_depends(self, xp, xp_need, level, hp, k_hp, armor, k_armor, damage, k_damage, 
        hand, bullets, range_atack, p_speed, prog_img):
        self.set_xp(xp, xp_need, leve)
        self.set_hp(hp, k_hp)
        self.set_armor(armor, k_armor)
        self.set_damage(damage, k_damage)
        self.set_atack(hand, bullets, range_atack, p_speed, prog_img)

    def spawn(self, Model) -> Sprite:
        self.sprite = Model()
        return self.sprite

    def full_spawn(self, Model, image, coords, speed, sleep,
        xp, xp_need, level, hp, k_hp, armor, k_armor, damage, k_damage, 
        hand, bullets=0, range_atack=20, p_speed=20, prog_img=""):
        self.sprite = Model()
        self.set_no_level_depends(image, coords, speed, sleep)
        self.set_level_depends(xp, xp_need, level, hp, k_hp, armor, k_armor, damage, k_damage, 
            hand, bullets, range_atack, p_speed, prog_img)
        return self.sprite
        


class Simple_Weapon:
    """
    Родительский Класс для всех видов оружия ближнего боя
    """

    def __init__(self, damage: int, range: int):
        self.damage = damage      # Урон
        self.range = range        # Дальность


class Projectile_Weapon:
    """
    Родительский Класс для всех видов оружия дальнего боя
    """

    def __init__(self, range: int, speed: int, damage: int, coords: list, orientation: int, image: str, on_fly: bool):
        self.range = range              # Дальность полета
        self.speed = speed              # Скорость полета
        self.damage = damage            # Урон
        self.f_coords = coords          # Координаты на момент выстрела
        self.coords = coords            # Координаты снаряда
        self.orientation = orientation  # Ориентация в пространстве
        self.image = image              # Изображение снаряда
        self.on_fly = on_fly            # Снаряд выпущен
