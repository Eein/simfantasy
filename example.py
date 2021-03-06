import logging
from argparse import ArgumentParser
from sys import argv

from simfantasy.enums import Attribute, Race, Slot
from simfantasy.jobs.bard import Bard
from simfantasy.simulator import Actor, Item, Materia, Simulation, Weapon

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--log-event-filter', action='store')
    parser.add_argument('--iterations', action='store', type=int, default=100)
    parser.add_argument('--log-action-attempts', action='store_true', default=False, dest='log_action_attempts')

    heap_options = parser.add_mutually_exclusive_group()
    heap_options.add_argument('--log-pushes', action='store_false', default=True, dest='log_pops')
    heap_options.add_argument('--log-pops', action='store_false', default=True, dest='log_pushes')

    args = parser.parse_args(argv[1:])

    sim = Simulation(log_level=logging.DEBUG if args.debug else None,
                     log_event_filter=args.log_event_filter,
                     log_pushes=args.log_pushes,
                     log_pops=args.log_pops,
                     iterations=args.iterations,
                     log_action_attempts=args.log_action_attempts)

    enemy = Actor(sim=sim, race=Race.ENEMY)

    savage_aim_vi = Materia(Attribute.CRITICAL_HIT, 40)
    savage_might_vi = Materia(Attribute.DETERMINATION, 40)
    heavens_eye_vi = Materia(Attribute.DIRECT_HIT, 40)
    vitality_vi = Materia(Attribute.VITALITY, 25)

    kujakuo = Weapon(name='Kujakuo', physical_damage=102, magic_damage=69, auto_attack=103.36, delay=3.04,
                     stats=((Attribute.DEXTERITY, 330), (Attribute.CRITICAL_HIT, 209), (Attribute.VITALITY, 358),
                            (Attribute.DIRECT_HIT, 298)),
                     melds=(savage_aim_vi, savage_aim_vi))

    true_linen_cap = Item(name='True Linen Cap of Aiming', slot=Slot.HEAD,
                          stats=((Attribute.DEXTERITY, 180), (Attribute.CRITICAL_HIT, 114), (Attribute.VITALITY, 193),
                                 (Attribute.DIRECT_HIT, 163), (Attribute.DEFENSE, 428), (Attribute.MAGIC_DEFENSE, 428)),
                          melds=(savage_aim_vi, savage_might_vi))

    true_linen_jacket = Item(name='True Linen Jacket of Aiming', slot=Slot.BODY,
                             stats=((Attribute.DEXTERITY, 293), (Attribute.CRITICAL_HIT, 265),
                                    (Attribute.VITALITY, 314), (Attribute.DETERMINATION, 186), (Attribute.DEFENSE, 599),
                                    (Attribute.MAGIC_DEFENSE, 599)),
                             melds=(heavens_eye_vi, heavens_eye_vi))

    augmented_tomestone_gloves = Item(name='Augmented Lost Allagan Gloves of Aiming', slot=Slot.HANDS,
                                      stats=((Attribute.DEXTERITY, 172), (Attribute.CRITICAL_HIT, 156),
                                             (Attribute.VITALITY, 182), (Attribute.DIRECT_HIT, 109),
                                             (Attribute.DEFENSE, 418), (Attribute.MAGIC_DEFENSE, 418)),
                                      melds=(heavens_eye_vi, savage_might_vi))

    slothskin_belt = Item(name='Slothskin Belt of Aiming', slot=Slot.WAIST,
                          stats=((Attribute.DEXTERITY, 135), (Attribute.DETERMINATION, 122), (Attribute.VITALITY, 145),
                                 (Attribute.DIRECT_HIT, 86), (Attribute.DEFENSE, 371), (Attribute.MAGIC_DEFENSE, 371)),
                          melds=(savage_aim_vi,))

    true_linen_breeches = Item(name='True Linen Breeches of Aiming', slot=Slot.LEGS,
                               stats=(
                                   (Attribute.DEXTERITY, 293), (Attribute.SKILL_SPEED, 265), (Attribute.VITALITY, 314),
                                   (Attribute.DIRECT_HIT, 186), (Attribute.DEFENSE, 599),
                                   (Attribute.MAGIC_DEFENSE, 599)),
                               melds=(savage_aim_vi, savage_aim_vi))

    slothskin_boots = Item(name='Slothskin Boots of Aiming', slot=Slot.FEET,
                           stats=((Attribute.DEXTERITY, 180), (Attribute.CRITICAL_HIT, 114), (Attribute.VITALITY, 193),
                                  (Attribute.SKILL_SPEED, 163), (Attribute.DEFENSE, 428),
                                  (Attribute.MAGIC_DEFENSE, 428)),
                           melds=(savage_aim_vi, heavens_eye_vi))

    carborundum_earrings = Item(name='Carborundum Earring of Aiming', slot=Slot.EARRINGS,
                                stats=((Attribute.DEXTERITY, 135), (Attribute.SKILL_SPEED, 122),
                                       (Attribute.DETERMINATION, 86), (Attribute.DEFENSE, 1),
                                       (Attribute.MAGIC_DEFENSE, 1)),
                                melds=(savage_aim_vi,))

    diamond_necklace = Item(name='Diamond Necklace of Aiming', slot=Slot.NECKLACE,
                            stats=((Attribute.DEXTERITY, 149), (Attribute.DETERMINATION, 133),
                                   (Attribute.CRITICAL_HIT, 93), (Attribute.DEFENSE, 1), (Attribute.MAGIC_DEFENSE, 1)),
                            melds=(vitality_vi,))

    augmented_tomestone_bracelet = Item(name='Augmented Lost Allagan Bracelet of Aiming', slot=Slot.BRACELET,
                                        stats=((Attribute.DEXTERITY, 129), (Attribute.DIRECT_HIT, 82),
                                               (Attribute.CRITICAL_HIT, 117), (Attribute.DEFENSE, 1),
                                               (Attribute.MAGIC_DEFENSE, 1)),
                                        melds=(vitality_vi,))

    augmented_tomestone_ring = Item(name='Augmented Lost Allagan Ring of Aiming', slot=Slot.RING,
                                    stats=((Attribute.DEXTERITY, 129), (Attribute.DETERMINATION, 117),
                                           (Attribute.CRITICAL_HIT, 82), (Attribute.DEFENSE, 1),
                                           (Attribute.MAGIC_DEFENSE, 1)),
                                    melds=(vitality_vi,))

    carborundum_ring = Item(name='Carborundum Ring of Aiming', slot=Slot.RING,
                            stats=((Attribute.DEXTERITY, 135), (Attribute.DIRECT_HIT, 122),
                                   (Attribute.CRITICAL_HIT, 86), (Attribute.DEFENSE, 1), (Attribute.MAGIC_DEFENSE, 1)),
                            melds=(vitality_vi,))

    bard = Bard(sim, race=Race.HIGHLANDER, name='Dikembe', target=enemy,
                gear=((Slot.WEAPON, kujakuo), (Slot.HEAD, true_linen_cap), (Slot.BODY, true_linen_jacket),
                      (Slot.HANDS, augmented_tomestone_gloves), (Slot.WAIST, slothskin_belt),
                      (Slot.LEGS, true_linen_breeches), (Slot.FEET, slothskin_boots),
                      (Slot.EARRINGS, carborundum_earrings),
                      (Slot.NECKLACE, diamond_necklace), (Slot.BRACELET, augmented_tomestone_bracelet),
                      (Slot.LEFT_RING, augmented_tomestone_ring), (Slot.RIGHT_RING, carborundum_ring)))

    sim.run()
