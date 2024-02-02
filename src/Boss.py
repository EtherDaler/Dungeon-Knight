import pygame
from Models import Sprite, Simple_Weapon, Projectile_Weapon
from Enemy import SimpleEnemy
from Hero import Knight
import threading
import time
from decorators import threadpool_decorator



class Boss_skills:
    """
    Класс, отвечающий за способности боссов в игре
    в нем реализованы все основные способности и ульты боссов в игре
    """

    def __init__(self, boss: object, skills_list: list, ult: int):
        """
        :boss: Принимает босса из класса Boss
        :skills_list: список скилов, они у нас пронумерованы
        :ult: номер ульты, которая будет у босса
        """

        self.boss = boss
        if len(skills_list) > 4:
            for i in range(5, len(skills_list)):
                del skills_list[i]
        self.skills_list = skills_list
        self.ult = ult

    def skill_0(self, percent: int):
        """
        Способность восстанавливает здоровье боссу
        """
        self.boss.hp += self.boss.hp * percent / 100
        if self.boss.hp > self.boss.max_hp:
            self.boss.hp = self.boss.hp

    @threadpool_decorator
    def stop_damage(self, damage: int, tm: int):
        time.sleep(time)
        self.boss.weapon.damage -= damage
        return True

    def skill_1(self, damage: int, tm: int):
        """
        Способность увеличивает урон босса на время
        """
        self.boss.weapon.damage += damage
        self.stop_damage(damage, tm)

    @threadpool_decorator
    def stop_slow(self, hero: Knight, speed: int, tm: int):
        time.sleep(time)
        hero.speed += speed
        return True

    def skill_2(self, hero: Knight, speed: int, tm: int):
        """
        Способность замедляет главного героя на время
        """
        hero.speed -= speed
        self.stop_slow(hero, speed, tm)

    def skill_3(self):
        """
        Способность выпускает сферу, которая наносит урон при попадании в героя
        """
        pass

    @threadpool_decorator
    def stop_stan(self, hero: Knight, tm: int):
        time.sleep(tm)
        hero.stanned = False
        return True

    def skill_4(self, hero: Knight, tm: int):
        """
        Способность оглушает главного героя на время
        """
        hero.stanned = True
        stop_stan(hero, tm)

    def skill_5(self):
        """
        Способность позволяет боссу перемещаться в пространстве
        """
        pass

    @threadpool_decorator
    def stop_fast(self, speed: int, tm: int):
        time.sleep(tm)
        self.boss.speed -= speed
        return True

    def skill_6(self, speed: int, tm: int):
        """
        Способность ускоряет скорость передвижения босса на время
        """
        self.boss.speed += speed
        self.stop_fast(speed, tm)

    def ult_0(self, screen, goal: list):
        """
        Ульта выпускает сферы, наносящие урон во все стороны
        """
        cell_width = settings.MAZE_WIDTH // 28
        cell_height = settings.MAZE_HEIGHT // 30
        blast = pygame.draw.circle(screen, (75, 0, 130), (100, 100), 50)
        sphere = Projectile_Weapon(500, 3, 10, self.boss.coords, self.boss.orientation, blast, True)
        # Проверка не попал ли снаряд на край экрана
        if sphere.coords[0] >= settings.WIDTH or sphere.coords[0] <= 0:
            del sphere
        if sphere.coords[1] >= settings.HEIGHT or sphere.coords[1] <= 0:
            del sphere

        # Проверка на дальность полета
        if sphere.coords[0] >= sphere.f_coords[0] + sphere.range or \
                sphere.coords[1] >= sphere.f_coords[1] + sphere.range:
            del sphere

        # Проверка на попадание в стену
        for wall in walls:
            if (sphere.coords[0] // cell_width, sphere.coords[1] // cell_height) == wall:
                del sphere

        # Проверка на попадание в спрайта
        for sprite in goal:
            if sphere.coords == sprite.coords:
                sprite.get_damage(sphere.damage)
                del sphere

        # Полет снаряда
        if sphere.orientation == 0:
            sphere.coords[1] += sphere.speed
        elif sphere.orientation == 1:
            sphere.coords[0] += sphere.speed
            sphere.coords[1] += sphere.speed
        elif sphere.orientation == 2:
            sphere.coords[0] += sphere.speed
        elif sphere.orientation == 3:
            sphere.coords[0] += sphere.speed
            sphere.coords[1] -= sphere.speed
        elif sphere.orientation == 4:
            sphere.coords[1] -= sphere.speed
        elif sphere.orientation == 5:
            sphere.coords[0] -= sphere.speed
            sphere.coords[1] -= sphere.speed
        elif sphere.orientation == 6:
            sphere.coords[0] -= sphere.speed
        elif sphere.orientation == 7:
            sphere.coords[0] -= sphere.speed
            sphere.coords[1] += sphere.speed

    def ult_1(self):
        """
        Ульта выпускает сферы, наносящие урон во все стороны
        """
        pass

    def ult_2(self):
        """
        Ульта позволяет боссу быстро побежать по прямой и наносить урон герою при попадании
        """
        pass

    @threadpool_decorator
    def ult_3(self, tm: int):
        """
        Ульта создает иллюзию босса на время
        """
        illusion = Boss(self.boss.sheet, [self.boss.coords[0] + 5, self.boss.coords[1] + 5], self.boss.hp // 2,
                        0, 0, 0, self.boss.speed, self.boss.view_range, self.boss.level, self.boss.live,
                        self.boss.hand, self.boss.bullets, self.boss.weapon.damage // 2, 0, self.boss.weapon.range,
                        self.boss.weapon.p_speed, self.boss.weapon.image)
        illusion.illusion = True
        time.sleep(tm)
        illusion.live = False
        del illusion
        return True



class Boss_fases:
    """
    Класс в котором будут реализованны фазы боссов
    """

    def __init__(self, boss: object, phase1: int, phase2: int):
        self.boss = boss
        if abs(phase1) > 2:
            ult = 2
        if abs(phase2) > 2:
            ult = 2
        self.phase1 = phase1
        self.phase2 = phase2

    def phase1_0(self):
        self.boss.weapon.damage += 5
        self.boss.speed += 2

    def phase1_1(self):
        self.boss.armor += 2
        self.boss.weapon.damage += 2

    def phase1_2(self):
        pass

    def phase2_0(self):
        pass

    def phase2_1(self):
        pass

    def phase2_2(self):
        pass



class Boss(SimpleEnemy):
    """
    Класс Босса
    тут мы уже непосредственно создаем нужного нам босса
    """

    max_hp = None
    illusion = False

    def call(self, name):
        """
        Дает имя боссу
        """

        self.name = name

    def fix_max_hp(self):
        """
        Зафиксировать максимальный запас здоровья босса, вызывается только вначале при создании объекта
        """

        if self.max_hp is None:
            self.max_hp = self.hp

    def set_skills(self, skills_list: list, ult: int):
        self.skills = Boss_skills(self, skills_list, ult)

    def set_fases(self, fas1: int, fas2: int):
        self.fases = Boss_fases(self, fas1=fas1, fas2=fas2)

    def activate_phase1(self):
        """
        Фаза 1 при битве с боссом
        """

        if self.hp * 100 / self.max_hp <= 50:
            self.fases.phase1_0()

    def activate_phase2(self):
        """
        Фаза 2 при битве с боссом
        """

        if self.hp * 100 / self.max_hp <= 30:
            self.fases.phase1_1()

    @threadpool_decorator
    def use_skill(self, skill: str, kd: int, **kwargs):
        time.sleep(kd)
        s = ""
        for i, j in kwrgs.items():
            s += f'{i}={j}'
        exec(f'self.skills.{skill}({s})')


    def use_skill(self, kd: list, **kwargs):
        for i, skill in enumirate(self.skills.skills_list):
            use_skill(skill, kd[i], kwargs[skill])

    @threadpool_decorator
    def use_ult(self, kd: int, **kwargs):
        time.sleep(kd)
        s = ""
        for i, j in kwrgs.items():
            s += f'{i}={j}'
        exec(f'self.skills.{self.skills.ult}({s})')
    
    def active(self):
        super().enemy_active(hero, walls, self.coords, self.coords + [20, 20])
        self.use_skill()
        self.use_ult()
        self.activate_fas1()
        self.activate_fas2()

