from datetime import timedelta
from math import floor
from typing import Dict

import numpy

from simfantasy.enums import Attribute, Job, Race, RefreshBehavior, Slot
from simfantasy.events import CastEvent, ConsumeAuraEvent
from simfantasy.simulator import Actor, Aura, Item, Simulation


class Bard(Actor):
    job = Job.BARD

    def __init__(self, sim: Simulation,
                 race: Race,
                 level: int = None,
                 target: Actor = None,
                 name: str = None,
                 equipment: Dict[Slot, Item] = None):
        super().__init__(sim, race, level, target, name, equipment)

        self.straight_shot = StraightShotBuff()
        self.straighter_shot = StraighterShotBuff()
        self.raging_strikes = RagingStrikesBuff()

        self.windbite = WindbiteDebuff(source=self)
        self.venomous_bite = VenomousBiteDebuff(source=self)

    def calculate_base_stats(self) -> Dict[Attribute, int]:
        base_stats = super().calculate_base_stats()

        if self.level >= 20:
            base_stats[Attribute.DEXTERITY] += 8

        if self.level >= 40:
            base_stats[Attribute.DEXTERITY] += 16

        if self.level >= 60:
            base_stats[Attribute.DEXTERITY] += 24

        return base_stats

    def decide(self):
        if not self.on_cooldown(RagingStrikesCast):
            return self.cast(RagingStrikesCast, target=self)

        if self.target.has_aura(self.windbite) and self.target.has_aura(self.venomous_bite):
            if self.windbite.remains < timedelta(seconds=3) or self.venomous_bite.remains < timedelta(seconds=3):
                return self.cast(IronJawsCast)

            if not self.on_cooldown(SidewinderCast):
                return self.cast(SidewinderCast)

        if self.has_aura(self.straighter_shot):
            return self.cast(RefulgentArrowCast)

        if not self.has_aura(self.straight_shot):
            return self.cast(StraightShotCast)

        if not self.target.has_aura(self.windbite):
            return self.cast(WindbiteCast)

        if not self.target.has_aura(self.venomous_bite):
            return self.cast(VenomousBiteCast)

        return self.cast(HeavyShotCast)


class BardCastEvent(CastEvent):
    source: Bard

    affected_by = Attribute.ATTACK_POWER
    hastened_by = Attribute.SKILL_SPEED

    @property
    def direct_damage(self) -> int:
        direct_damage = super().direct_damage

        if self.source.level >= 20:
            direct_damage = floor(direct_damage * 1.1)

        if self.source.level >= 40:
            direct_damage = floor(direct_damage * 1.2)

        if self.source.raging_strikes in self.source.auras:
            direct_damage = floor(direct_damage * 1.1)

        return direct_damage


class StraighterShotBuff(Aura):
    duration = timedelta(seconds=10)
    refresh_behavior = RefreshBehavior.RESET


class StraightShotBuff(Aura):
    duration = timedelta(seconds=30)
    refresh_behavior = RefreshBehavior.RESET

    def apply(self, target: Bard):
        target.stats[Attribute.CRITICAL_HIT] *= 1.1

    def expire(self, target: Bard):
        target.stats[Attribute.CRITICAL_HIT] /= 1.1


class StraightShotCast(BardCastEvent):
    potency = 140

    @property
    def critical_hit_chance(self):
        return 100.0 if self.source.straighter_shot in self.source.auras else super().critical_hit_chance

    def execute(self):
        super().execute()

        self.schedule_aura_events(aura=self.source.straight_shot, target=self.source)

        if self.source.straighter_shot in self.source.auras:
            self.sim.schedule_in(ConsumeAuraEvent(sim=self.sim, target=self.source, aura=self.source.straighter_shot))


class WindbiteDebuff(Aura):
    def __init__(self, source: Bard):
        super().__init__()

        self.source = source

    @property
    def duration(self):
        return timedelta(seconds=15 if self.source.level < 64 else 30)


class WindbiteCast(BardCastEvent):
    @property
    def potency(self):
        return 60 if self.source.level < 64 else 120

    def execute(self):
        super().execute()

        self.schedule_aura_events(aura=self.source.windbite, target=self.target)


class VenomousBiteDebuff(Aura):
    def __init__(self, source: Bard):
        super().__init__()

        self.source = source

    @property
    def duration(self):
        return timedelta(seconds=15 if self.source.level < 64 else 30)


class VenomousBiteCast(BardCastEvent):
    @property
    def potency(self):
        return 100 if self.source.level < 64 else 120

    def execute(self):
        super().execute()

        self.schedule_aura_events(aura=self.source.venomous_bite, target=self.target)


class HeavyShotCast(BardCastEvent):
    potency = 150

    def execute(self):
        super().execute()

        if numpy.random.uniform() <= 0.2:
            self.schedule_aura_events(aura=self.source.straighter_shot, target=self.source)


class RagingStrikesBuff(Aura):
    duration = timedelta(seconds=20)


class RagingStrikesCast(BardCastEvent):
    is_off_gcd = True
    recast_time = timedelta(seconds=80)

    @property
    def critical_hit_chance(self):
        return 0.0

    @property
    def direct_hit_chance(self):
        return 0.0

    def execute(self):
        super().execute()

        self.schedule_aura_events(aura=self.source.raging_strikes, target=self.source)


class RefulgentArrowCast(BardCastEvent):
    potency = 300

    def execute(self):
        super().execute()

        self.sim.schedule_in(ConsumeAuraEvent(sim=self.sim, target=self.source, aura=self.source.straighter_shot))


class SidewinderCast(BardCastEvent):
    recast_time = timedelta(seconds=60)

    @property
    def potency(self):
        if self.source.level < 64:
            return 100

        if self.target.has_aura(self.source.windbite) and self.target.has_aura(self.source.venomous_bite):
            return 260

        if self.target.has_aura(self.source.windbite) or self.target.has_aura(self.source.venomous_bite):
            return 175

        return 100


class IronJawsCast(BardCastEvent):
    @property
    def potency(self):
        if self.source.level < 64:
            return 100

        if self.target.has_aura(self.source.windbite) and self.target.has_aura(self.source.venomous_bite):
            return 260

        if self.target.has_aura(self.source.windbite) or self.target.has_aura(self.source.venomous_bite):
            return 175

        return 100

    def execute(self):
        super().execute()

        if self.target.has_aura(self.source.windbite):
            self.schedule_aura_events(self.source.windbite)

        if self.target.has_aura(self.source.venomous_bite):
            self.schedule_aura_events(self.source.venomous_bite)
