import pygame

# Родительский Класс для всех Спрайтов
class Sprite:
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
    coords = (0, 0) # Позиция
    sheet = None    # Моделька Спрайта
    orientation = 0 # То в какую сторону смотрит спрайт, всего 8 направлений

    def __init__(self, image: object, hp: int, k_hp: int, armor: float, k_armor: int, speed: int, view_range: int,
                 level: int, live: bool, hand: bool, bullets: int, damage: int, k_damage: int, range: int, p_speed: int,
                 proj_img: str):
        self.sheet = image
        self.hp = hp + (hp * level // k_hp)
        self.armor = armor + (armor * level / k_armor)
        self.speed = speed
        self.view_range = view_range
        self.level = level
        self.live = live
        self.hand = hand
        self.bullets = bullets
        self.xp_need = level * 200
        # Выбор оружия в зависимости от типа боя
        if hand is True:
            self.weapon = Simple_Weapon(damage + (damage * level // k_damage), range)
        else:
            self.weapon = []
            for i in range(self.bullets):
                self.weapon.append(Projectile_Weapon(range, p_speed, damage + (damage * level // k_damage),
                                                     self.coords, self.orientation, proj_img, False))

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
        if self.orientation == 0:
            self.get_image(0, 0, 32, 32, 3, (255, 255, 255))
            self.get_image(1, 0, 32, 32, 3, (255, 255, 255))
        elif self.orientation == 1:
            self.get_image(0, 1, 32, 32, 3, (255, 255, 255))
            self.get_image(1, 1, 32, 32, 3, (255, 255, 255))
        elif self.orientation == 2:
            self.get_image(0, 2, 32, 32, 3, (255, 255, 255))
            self.get_image(1, 2, 32, 32, 3, (255, 255, 255))
        elif self.orientation == 3:
            self.get_image(0, 3, 32, 32, 3, (255, 255, 255))
            self.get_image(1, 3, 32, 32, 3, (255, 255, 255))
        elif self.orientation == 4:
            self.get_image(0, 4, 32, 32, 3, (255, 255, 255))
            self.get_image(1, 4, 32, 32, 3, (255, 255, 255))
        elif self.orientation == 5:
            self.get_image(0, 5, 32, 32, 3, (255, 255, 255))
            self.get_image(1, 5, 32, 32, 3, (255, 255, 255))
        elif self.orientation == 6:
            self.get_image(0, 6, 32, 32, 3, (255, 255, 255))
            self.get_image(1, 6, 32, 32, 3, (255, 255, 255))
        elif self.orientation == 7:
            self.get_image(0, 7, 32, 32, 3, (255, 255, 255))
            self.get_image(1, 7, 32, 32, 3, (255, 255, 255))

    # Анимация атаки
    def animation_atack(self):

        if self.orientation == 0:
            self.get_image(4, 0, 32, 32, 3, (255, 255, 255))
            self.get_image(5, 0, 32, 32, 3, (255, 255, 255))
            self.get_image(6, 0, 32, 32, 3, (255, 255, 255))
        if self.orientation == 1:
            self.get_image(4, 1, 32, 32, 3, (255, 255, 255))
            self.get_image(5, 1, 32, 32, 3, (255, 255, 255))
            self.get_image(6, 1, 32, 32, 3, (255, 255, 255))
        if self.orientation == 2:
            self.get_image(4, 2, 32, 32, 3, (255, 255, 255))
            self.get_image(5, 2, 32, 32, 3, (255, 255, 255))
            self.get_image(6, 2, 32, 32, 3, (255, 255, 255))
        if self.orientation == 3:
            self.get_image(4, 3, 32, 32, 3, (255, 255, 255))
            self.get_image(5, 3, 32, 32, 3, (255, 255, 255))
            self.get_image(6, 3, 32, 32, 3, (255, 255, 255))
        if self.orientation == 4:
            self.get_image(4, 4, 32, 32, 3, (255, 255, 255))
            self.get_image(5, 4, 32, 32, 3, (255, 255, 255))
            self.get_image(6, 4, 32, 32, 3, (255, 255, 255))
        if self.orientation == 5:
            self.get_image(4, 5, 32, 32, 3, (255, 255, 255))
            self.get_image(5, 5, 32, 32, 3, (255, 255, 255))
            self.get_image(6, 5, 32, 32, 3, (255, 255, 255))
        if self.orientation == 6:
            self.get_image(4, 6, 32, 32, 3, (255, 255, 255))
            self.get_image(5, 6, 32, 32, 3, (255, 255, 255))
            self.get_image(6, 6, 32, 32, 3, (255, 255, 255))
        if self.orientation == 7:
            self.get_image(4, 7, 32, 32, 3, (255, 255, 255))
            self.get_image(5, 7, 32, 32, 3, (255, 255, 255))
            self.get_image(6, 7, 32, 32, 3, (255, 255, 255))

        # Анимация ходьбы
        def animation_walk(self):
            if self.orientation == 0:
                self.get_image(2, 0, 32, 32, 3, (255, 255, 255))
                self.get_image(3, 0, 32, 32, 3, (255, 255, 255))
            if self.orientation == 1:
                self.get_image(2, 1, 32, 32, 3, (255, 255, 255))
                self.get_image(3, 1, 32, 32, 3, (255, 255, 255))
            if self.orientation == 2:
                self.get_image(2, 2, 32, 32, 3, (255, 255, 255))
                self.get_image(3, 2, 32, 32, 3, (255, 255, 255))
            if self.orientation == 3:
                self.get_image(2, 3, 32, 32, 3, (255, 255, 255))
                self.get_image(3, 3, 32, 32, 3, (255, 255, 255))
            if self.orientation == 4:
                self.get_image(2, 4, 32, 32, 3, (255, 255, 255))
                self.get_image(3, 4, 32, 32, 3, (255, 255, 255))
            if self.orientation == 5:
                self.get_image(2, 5, 32, 32, 3, (255, 255, 255))
                self.get_image(3, 5, 32, 32, 3, (255, 255, 255))
            if self.orientation == 6:
                self.get_image(2, 6, 32, 32, 3, (255, 255, 255))
                self.get_image(3, 6, 32, 32, 3, (255, 255, 255))
            if self.orientation == 7:
                self.get_image(2, 7, 32, 32, 3, (255, 255, 255))
                self.get_image(3, 7, 32, 32, 3, (255, 255, 255))

        # Анимация стрельбы
        def animation_fire(self, **kwargs):
            if self.orientation == 0:
                self.get_image(8, 0, 32, 32, 3, (255, 255, 255))
                self.get_image(9, 0, 32, 32, 3, (255, 255, 255))
                self.get_image(10, 0, 32, 32, 3, (255, 255, 255))
                self.get_image(11, 0, 32, 32, 3, (255, 255, 255))
            if self.orientation == 1:
                self.get_image(8, 1, 32, 32, 3, (255, 255, 255))
                self.get_image(9, 1, 32, 32, 3, (255, 255, 255))
                self.get_image(10, 1, 32, 32, 3, (255, 255, 255))
                self.get_image(11, 1, 32, 32, 3, (255, 255, 255))
            if self.orientation == 2:
                self.get_image(8, 2, 32, 32, 3, (255, 255, 255))
                self.get_image(9, 2, 32, 32, 3, (255, 255, 255))
                self.get_image(10, 2, 32, 32, 3, (255, 255, 255))
                self.get_image(11, 2, 32, 32, 3, (255, 255, 255))
            if self.orientation == 3:
                self.get_image(8, 3, 32, 32, 3, (255, 255, 255))
                self.get_image(9, 3, 32, 32, 3, (255, 255, 255))
                self.get_image(10, 3, 32, 32, 3, (255, 255, 255))
                self.get_image(11, 3, 32, 32, 3, (255, 255, 255))
            if self.orientation == 4:
                self.get_image(8, 4, 32, 32, 3, (255, 255, 255))
                self.get_image(9, 4, 32, 32, 3, (255, 255, 255))
                self.get_image(10, 4, 32, 32, 3, (255, 255, 255))
                self.get_image(11, 4, 32, 32, 3, (255, 255, 255))
            if self.orientation == 5:
                self.get_image(8, 5, 32, 32, 3, (255, 255, 255))
                self.get_image(9, 5, 32, 32, 3, (255, 255, 255))
                self.get_image(10, 5, 32, 32, 3, (255, 255, 255))
                self.get_image(11, 5, 32, 32, 3, (255, 255, 255))
            if self.orientation == 6:
                self.get_image(8, 6, 32, 32, 3, (255, 255, 255))
                self.get_image(9, 6, 32, 32, 3, (255, 255, 255))
                self.get_image(10, 6, 32, 32, 3, (255, 255, 255))
                self.get_image(11, 6, 32, 32, 3, (255, 255, 255))
            if self.orientation == 7:
                self.get_image(8, 7, 32, 32, 3, (255, 255, 255))
                self.get_image(9, 7, 32, 32, 3, (255, 255, 255))
                self.get_image(10, 7, 32, 32, 3, (255, 255, 255))
                self.get_image(11, 7, 32, 32, 3, (255, 255, 255))

        # Анимация смерти
        def animation_death(self, **kwargs):
            if self.orientation == 0:
                self.get_image(12, 0, 32, 32, 3, (255, 255, 255))
                self.get_image(13, 0, 32, 32, 3, (255, 255, 255))
                self.get_image(14, 0, 32, 32, 3, (255, 255, 255))
                self.get_image(15, 0, 32, 32, 3, (255, 255, 255))
            if self.orientation == 1:
                self.get_image(12, 1, 32, 32, 3, (255, 255, 255))
                self.get_image(13, 1, 32, 32, 3, (255, 255, 255))
                self.get_image(14, 1, 32, 32, 3, (255, 255, 255))
                self.get_image(15, 1, 32, 32, 3, (255, 255, 255))
            if self.orientation == 2:
                self.get_image(12, 2, 32, 32, 3, (255, 255, 255))
                self.get_image(13, 2, 32, 32, 3, (255, 255, 255))
                self.get_image(14, 2, 32, 32, 3, (255, 255, 255))
                self.get_image(15, 2, 32, 32, 3, (255, 255, 255))
            if self.orientation == 3:
                self.get_image(12, 3, 32, 32, 3, (255, 255, 255))
                self.get_image(13, 3, 32, 32, 3, (255, 255, 255))
                self.get_image(14, 3, 32, 32, 3, (255, 255, 255))
                self.get_image(15, 3, 32, 32, 3, (255, 255, 255))
            if self.orientation == 4:
                self.get_image(12, 4, 32, 32, 3, (255, 255, 255))
                self.get_image(13, 4, 32, 32, 3, (255, 255, 255))
                self.get_image(14, 4, 32, 32, 3, (255, 255, 255))
                self.get_image(15, 4, 32, 32, 3, (255, 255, 255))
            if self.orientation == 5:
                self.get_image(12, 5, 32, 32, 3, (255, 255, 255))
                self.get_image(13, 5, 32, 32, 3, (255, 255, 255))
                self.get_image(14, 5, 32, 32, 3, (255, 255, 255))
                self.get_image(15, 5, 32, 32, 3, (255, 255, 255))
            if self.orientation == 6:
                self.get_image(12, 6, 32, 32, 3, (255, 255, 255))
                self.get_image(13, 6, 32, 32, 3, (255, 255, 255))
                self.get_image(14, 6, 32, 32, 3, (255, 255, 255))
                self.get_image(15, 6, 32, 32, 3, (255, 255, 255))
            if self.orientation == 7:
                self.get_image(12, 7, 32, 32, 3, (255, 255, 255))
                self.get_image(13, 7, 32, 32, 3, (255, 255, 255))
                self.get_image(14, 7, 32, 32, 3, (255, 255, 255))
                self.get_image(15, 7, 32, 32, 3, (255, 255, 255))

        # Анимация победы
        def animation_win(self, **kwargs):
            if self.orientation == 0:
                self.get_image(17, 0, 32, 32, 3, (255, 255, 255))
                self.get_image(18, 0, 32, 32, 3, (255, 255, 255))
                self.get_image(19, 0, 32, 32, 3, (255, 255, 255))
                self.get_image(20, 0, 32, 32, 3, (255, 255, 255))
            if self.orientation == 1:
                self.get_image(17, 1, 32, 32, 3, (255, 255, 255))
                self.get_image(18, 1, 32, 32, 3, (255, 255, 255))
                self.get_image(19, 1, 32, 32, 3, (255, 255, 255))
                self.get_image(20, 1, 32, 32, 3, (255, 255, 255))
            if self.orientation == 2:
                self.get_image(17, 2, 32, 32, 3, (255, 255, 255))
                self.get_image(18, 2, 32, 32, 3, (255, 255, 255))
                self.get_image(19, 2, 32, 32, 3, (255, 255, 255))
                self.get_image(20, 2, 32, 32, 3, (255, 255, 255))
            if self.orientation == 3:
                self.get_image(17, 3, 32, 32, 3, (255, 255, 255))
                self.get_image(18, 3, 32, 32, 3, (255, 255, 255))
                self.get_image(19, 3, 32, 32, 3, (255, 255, 255))
                self.get_image(20, 3, 32, 32, 3, (255, 255, 255))
            if self.orientation == 4:
                self.get_image(17, 4, 32, 32, 3, (255, 255, 255))
                self.get_image(18, 4, 32, 32, 3, (255, 255, 255))
                self.get_image(19, 4, 32, 32, 3, (255, 255, 255))
                self.get_image(20, 4, 32, 32, 3, (255, 255, 255))
            if self.orientation == 5:
                self.get_image(17, 5, 32, 32, 3, (255, 255, 255))
                self.get_image(18, 5, 32, 32, 3, (255, 255, 255))
                self.get_image(19, 5, 32, 32, 3, (255, 255, 255))
                self.get_image(20, 5, 32, 32, 3, (255, 255, 255))
            if self.orientation == 6:
                self.get_image(17, 6, 32, 32, 3, (255, 255, 255))
                self.get_image(18, 6, 32, 32, 3, (255, 255, 255))
                self.get_image(19, 6, 32, 32, 3, (255, 255, 255))
                self.get_image(20, 6, 32, 32, 3, (255, 255, 255))
            if self.orientation == 7:
                self.get_image(17, 7, 32, 32, 3, (255, 255, 255))
                self.get_image(18, 7, 32, 32, 3, (255, 255, 255))
                self.get_image(19, 7, 32, 32, 3, (255, 255, 255))
                self.get_image(20, 7, 32, 32, 3, (255, 255, 255))

    """
    Методы отвечающие за движение
    """
    def move_bullets(self):
        for i in self.weapon:
            if i.on_fly is False:
                i.coords = self.coords
                i.f_coords = self.coords
                i.orientation = self.orientation

    def move_front(self):
        self.animation_walk()
        self.coords[1] += self.speed
        self.orientation = 0
        if self.hand is False:
            self.move_bullets()

    def move_back(self):
        self.animation_walk()
        self.coords[1] -= self.speed
        self.orientation = 4
        if self.hand is False:
            self.move_bullets()

    def move_right(self):
        self.animation_walk()
        self.coords[0] += self.speed
        self.orientation = 2
        if self.hand is False:
            self.move_bullets()

    def move_left(self):
        self.animation_walk()
        self.coords[0] -= self.speed
        self.orientation = 6
        if self.hand is False:
            self.move_bullets()

    def move_diag(self, x: str, y: str):
        self.animation_walk()
        """
        :param x: принимает +-
        :param y: принимает +-
        если один из параметров положительный, то спрайт движется в положительную сторону по этой оси,
        если отрицательный, то наоборот
        """
        if x == '+':
            if y == '+':
                self.coords[0] += self.speed
                self.coords[1] += self.speed
                self.orientation = 1
            else:
                self.coords[0] += self.speed
                self.coords[1] -= self.speed
                self.orientation = 3
        else:
            if y == '+':
                self.coords[0] -= self.speed
                self.coords[1] += self.speed
                self.orientation = 7
            else:
                self.coords[0] -= self.speed
                self.coords[1] -= self.speed
                self.orientation = 5
        if self.hand is False:
            self.move_bullets()

    """
    Атака и получение урона
    """
    # Получение урона
    def get_damage(self, damage: int):
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            self.animation_death()
            self.live = False
            return 1
        return 0

    # Атака в ближнем бою
    def attack(self, goal: object):
        self.animation_atack()
        if goal is not None:
            self.kills += goal.get_damage(self.weapon.damage)

    # Стрельба
    def fire(self, goal: list, walls: list):
        self.animation_fire()
        """
        :param goal: Для героя передается список всех врагов на карте
                     Для врагов передается список из одного элемента - героя
        :param walls: Передается список с координатами всех стен
        """
        self.weapon[-1].on_fly = True

        # Проверка не попал ли снаряд на край экрана
        if self.weapon[-1].coords[0] >= 520 or self.weapon[-1].coords[0] <= 0:
            d = self.weapon.pop(self.weapon.index(self.weapon[-1]))
            self.weapon.append(Projectile_Weapon(d.range, d.speed, d.damage,
                                                     self.coords, self.orientation, d.image, False))

        # Проверка не попал ли снаряд на край экрана
        if self.weapon[-1].coords[1] >= 800 or self.weapon[-1].coords[1] <= 0:
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
            if self.weapon[-1].coords == wall:
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

    def draw(self, screen: object):
        screen.blit(self.animation_stay(), self.coords)



# Родительский Класс для всех видов оружия ближнего боя
class Simple_Weapon:
    def __init__(self, damage: int, range: int):
        self.damage = damage      # Урон
        self.range = range        # Дальность

# Родительский Класс для всех видов оружия дальнего боя
class Projectile_Weapon:
    def __init__(self, range: int, speed: int, damage: int, coords: tuple, orientation: int, image: str, on_fly: bool):
        self.range = range              # Дальность полета
        self.speed = speed              # Скорость полета
        self.damage = damage            # Урон
        self.f_coords = coords          # Координаты на момент выстрела
        self.coords = coords            # Координаты снаряда
        self.orientation = orientation  # Ориентация в пространстве
        self.image = image              # Изображение снаряда
        self.on_fly = on_fly            # Снаряд выпущен