"""Flyweight pattern

Separate an object into two parts:
    1. an intrinsic, immutable part that can be shared across all instances
       (state-independent)
    2. an extrinsic, mutable part that is specific for each instance and cannot
       be shared (state-dependent)
"""
import random
from abc import ABC


class Model3D(object):
    pass


class OrkModel(Model3D):
    pass


class AlienModel(Model3D):
    pass


class Intelligence(object):
    pass


class HighIntelligence(Intelligence):
    pass


class Enemy(object):

    immutables = (Model3D, Intelligence)

    def __init__(self, position=(0, 0)):
        self.position = position


class Ork(Enemy):

    immutables = (OrkModel, Intelligence)


class Alien(Enemy):

    immutables = (AlienModel, Intelligence)


class Queen(Alien):

    immutables = (AlienModel, HighIntelligence)


class Factory(ABC):

    pool = dict()

    @classmethod
    def make_enemy(cls, enemy_type, position):
        this_module = __import__(__name__)
        enemy_class = getattr(this_module, enemy_type)

        # add immutable objects to the pool if they are not already there
        for imm in enemy_class.immutables:
            immutable_name = imm.__name__
            obj = cls.pool.get(immutable_name, None)
            if obj is None:
                obj = object.__new__(imm)
                cls.pool[immutable_name] = obj
                print("NEW IMMUTABLE in the pool: {}".format(immutable_name))

        return enemy_class(position=position)


if __name__ == "__main__":
    ork_model_identities = list()
    alien_model_identities = list()
    intelligence_identities = list()
    high_intelligence_identities = list()

    for i in range(10):
        x, y = (random.randint(0, 100), random.randint(0, 100))
        enemy = Factory.make_enemy("Ork", position=(x, y))
        ork_model_identities.append(id(enemy.immutables[0]))
        intelligence_identities.append(id(enemy.immutables[1]))
        print(enemy)

    print("")
    for i in range(10):
        x, y = (random.randint(0, 100), random.randint(0, 100))
        enemy = Factory.make_enemy("Alien", position=(x, y))
        alien_model_identities.append(id(enemy.immutables[0]))
        intelligence_identities.append(id(enemy.immutables[1]))
        print(enemy)

    print("")
    for i in range(2):
        x, y = (random.randint(0, 100), random.randint(0, 100))
        enemy = Factory.make_enemy("Queen", position=(x, y))
        alien_model_identities.append(id(enemy.immutables[0]))
        high_intelligence_identities.append(id(enemy.immutables[1]))
        print(enemy)

    print("\nImmutable parts of the same type share the same identity")
    print("ork_model_identities:\n{}".format(set(ork_model_identities)))
    print("alien_model_identities:\n{}".format(set(alien_model_identities)))
    print("intelligence_identities:\n{}".format(set(intelligence_identities)))
    print("high_intelligence_identities:\n{}".format(set(high_intelligence_identities)))
    assert len(set(ork_model_identities)) == 1
    assert len(set(alien_model_identities)) == 1
    assert len(set(intelligence_identities)) == 1
    assert len(set(high_intelligence_identities)) == 1
