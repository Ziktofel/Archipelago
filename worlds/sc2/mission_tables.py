from typing import NamedTuple, Dict, List, Set, Union, Literal, Iterable, Callable, Optional
from enum import IntEnum, Enum, IntFlag, auto


class SC2Race(IntEnum):
    ANY = 0
    TERRAN = 1
    ZERG = 2
    PROTOSS = 3


class MissionPools(IntEnum):
    STARTER = 0
    EASY = 1
    MEDIUM = 2
    HARD = 3
    VERY_HARD = 4
    FINAL = 5


class MissionFlag(IntFlag):
    none          = 0
    Terran        = auto()
    Zerg          = auto()
    Protoss       = auto()
    NoBuild       = auto()
    Defense       = auto()
    AutoScroller  = auto()  # The mission is won by waiting out a timer or victory is gated behind a timer
    Countdown     = auto()  # Overall, the the mission must be beaten before a loss timer counts down
    Kerrigan      = auto()  # The player controls Kerrigan in the mission
    VanillaSoa    = auto()  # The player controls the Spear of Adun in the vanilla version of the mission
    Nova          = auto()  # The player controls NCO Nova in the mission
    AiTerranAlly  = auto()  # The mission has a Terran AI ally that can be taken over
    AiZergAlly    = auto()  # The mission has a Zerg AI ally that can be taken over
    AiProtossAlly = auto()  # The mission has a Protoss AI ally that can be taken over
    VsTerran      = auto()
    VsZerg        = auto()
    VsProtoss     = auto()
    HasRaceSwap   = auto()  # The mission has variants that use different factions from the vanilla experience.
    RaceSwap      = auto()  # The mission uses different factions from the vanilla experience.

    AiAlly        = AiTerranAlly|AiZergAlly|AiProtossAlly
    TimedDefense  = AutoScroller|Defense
    VsTZ          = VsTerran|VsZerg
    VsTP          = VsTerran|VsProtoss
    VsPZ          = VsProtoss|VsZerg
    VsAll         = VsTerran|VsProtoss|VsZerg

class SC2CampaignGoalPriority(IntEnum):
    """
    Campaign's priority to goal election
    """
    NONE = 0
    MINI_CAMPAIGN = 1  # A goal shouldn't be in a mini-campaign if there's at least one 'big' campaign
    HARD = 2  # A campaign ending with a hard mission
    VERY_HARD = 3  # A campaign ending with a very hard mission
    EPILOGUE = 4  # Epilogue shall be always preferred as the goal if present


class SC2Campaign(Enum):

    def __new__(cls, *args, **kwargs):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, campaign_id: int, name: str, goal_priority: SC2CampaignGoalPriority,  race: SC2Race):
        self.id = campaign_id
        self.campaign_name = name
        self.goal_priority = goal_priority
        self.race = race

    GLOBAL = 0, "Global", SC2CampaignGoalPriority.NONE, SC2Race.ANY
    WOL = 1, "Wings of Liberty", SC2CampaignGoalPriority.VERY_HARD, SC2Race.TERRAN
    PROPHECY = 2, "Prophecy", SC2CampaignGoalPriority.MINI_CAMPAIGN, SC2Race.PROTOSS
    HOTS = 3, "Heart of the Swarm", SC2CampaignGoalPriority.HARD, SC2Race.ZERG
    PROLOGUE = 4, "Whispers of Oblivion (Legacy of the Void: Prologue)", SC2CampaignGoalPriority.MINI_CAMPAIGN, SC2Race.PROTOSS
    LOTV = 5, "Legacy of the Void", SC2CampaignGoalPriority.VERY_HARD, SC2Race.PROTOSS
    EPILOGUE = 6, "Into the Void (Legacy of the Void: Epilogue)", SC2CampaignGoalPriority.EPILOGUE, SC2Race.ANY
    NCO = 7, "Nova Covert Ops", SC2CampaignGoalPriority.HARD, SC2Race.TERRAN


class SC2Mission(Enum):

    def __new__(cls, *args, **kwargs):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, mission_id: int, name: str, campaign: SC2Campaign, area: str, race: SC2Race, pool: MissionPools, map_file: str, flags: MissionFlag):
        self.id = mission_id
        self.mission_name = name
        self.campaign = campaign
        self.area = area
        self.race = race
        self.pool = pool
        self.map_file = map_file
        self.flags = flags

    # Wings of Liberty
    LIBERATION_DAY = 1, "Liberation Day", SC2Campaign.WOL, "Mar Sara", SC2Race.ANY, MissionPools.STARTER, "ap_liberation_day", MissionFlag.Terran|MissionFlag.NoBuild|MissionFlag.VsTerran
    THE_OUTLAWS = 2, "The Outlaws (Terran)", SC2Campaign.WOL, "Mar Sara", SC2Race.TERRAN, MissionPools.EASY, "ap_the_outlaws", MissionFlag.Terran|MissionFlag.VsTerran|MissionFlag.HasRaceSwap
    ZERO_HOUR = 3, "Zero Hour (Terran)", SC2Campaign.WOL, "Mar Sara", SC2Race.TERRAN, MissionPools.EASY, "ap_zero_hour", MissionFlag.Terran|MissionFlag.TimedDefense|MissionFlag.VsZerg|MissionFlag.HasRaceSwap
    EVACUATION = 4, "Evacuation (Terran)", SC2Campaign.WOL, "Colonist", SC2Race.TERRAN, MissionPools.EASY, "ap_evacuation", MissionFlag.Terran|MissionFlag.AutoScroller|MissionFlag.VsZerg|MissionFlag.HasRaceSwap
    OUTBREAK = 5, "Outbreak (Terran)", SC2Campaign.WOL, "Colonist", SC2Race.TERRAN, MissionPools.EASY, "ap_outbreak", MissionFlag.Terran|MissionFlag.Defense|MissionFlag.VsZerg|MissionFlag.HasRaceSwap
    SAFE_HAVEN = 6, "Safe Haven (Terran)", SC2Campaign.WOL, "Colonist", SC2Race.TERRAN, MissionPools.MEDIUM, "ap_safe_haven", MissionFlag.Terran|MissionFlag.Countdown|MissionFlag.VsProtoss|MissionFlag.HasRaceSwap
    HAVENS_FALL = 7, "Haven's Fall (Terran)", SC2Campaign.WOL, "Colonist", SC2Race.TERRAN, MissionPools.MEDIUM, "ap_havens_fall", MissionFlag.Terran|MissionFlag.VsZerg|MissionFlag.HasRaceSwap
    SMASH_AND_GRAB = 8, "Smash and Grab (Terran)", SC2Campaign.WOL, "Artifact", SC2Race.TERRAN, MissionPools.EASY, "ap_smash_and_grab", MissionFlag.Terran|MissionFlag.Countdown|MissionFlag.VsPZ|MissionFlag.HasRaceSwap
    THE_DIG = 9, "The Dig", SC2Campaign.WOL, "Artifact", SC2Race.TERRAN, MissionPools.MEDIUM, "ap_the_dig", MissionFlag.Terran|MissionFlag.TimedDefense|MissionFlag.VsProtoss
    THE_MOEBIUS_FACTOR = 10, "The Moebius Factor", SC2Campaign.WOL, "Artifact", SC2Race.TERRAN, MissionPools.MEDIUM, "ap_the_moebius_factor", MissionFlag.Terran|MissionFlag.Countdown|MissionFlag.VsZerg
    SUPERNOVA = 11, "Supernova", SC2Campaign.WOL, "Artifact", SC2Race.TERRAN, MissionPools.HARD, "ap_supernova", MissionFlag.Terran|MissionFlag.Countdown|MissionFlag.VsProtoss
    MAW_OF_THE_VOID = 12, "Maw of the Void", SC2Campaign.WOL, "Artifact", SC2Race.TERRAN, MissionPools.HARD, "ap_maw_of_the_void", MissionFlag.Terran|MissionFlag.VsProtoss
    DEVILS_PLAYGROUND = 13, "Devil's Playground (Terran)", SC2Campaign.WOL, "Covert", SC2Race.TERRAN, MissionPools.EASY, "ap_devils_playground", MissionFlag.Terran|MissionFlag.VsZerg|MissionFlag.HasRaceSwap
    WELCOME_TO_THE_JUNGLE = 14, "Welcome to the Jungle (Terran)", SC2Campaign.WOL, "Covert", SC2Race.TERRAN, MissionPools.MEDIUM, "ap_welcome_to_the_jungle", MissionFlag.Terran|MissionFlag.VsProtoss|MissionFlag.HasRaceSwap
    BREAKOUT = 15, "Breakout", SC2Campaign.WOL, "Covert", SC2Race.ANY, MissionPools.STARTER, "ap_breakout", MissionFlag.Terran|MissionFlag.NoBuild|MissionFlag.VsTerran
    GHOST_OF_A_CHANCE = 16, "Ghost of a Chance", SC2Campaign.WOL, "Covert", SC2Race.ANY, MissionPools.STARTER, "ap_ghost_of_a_chance", MissionFlag.Terran|MissionFlag.NoBuild|MissionFlag.VsTerran
    THE_GREAT_TRAIN_ROBBERY = 17, "The Great Train Robbery (Terran)", SC2Campaign.WOL, "Rebellion", SC2Race.TERRAN, MissionPools.MEDIUM, "ap_the_great_train_robbery", MissionFlag.Terran|MissionFlag.AutoScroller|MissionFlag.VsTerran|MissionFlag.HasRaceSwap
    CUTTHROAT = 18, "Cutthroat (Terran)", SC2Campaign.WOL, "Rebellion", SC2Race.TERRAN, MissionPools.MEDIUM, "ap_cutthroat", MissionFlag.Terran|MissionFlag.Countdown|MissionFlag.VsTerran|MissionFlag.HasRaceSwap
    ENGINE_OF_DESTRUCTION = 19, "Engine of Destruction (Terran)", SC2Campaign.WOL, "Rebellion", SC2Race.TERRAN, MissionPools.HARD, "ap_engine_of_destruction", MissionFlag.Terran|MissionFlag.AutoScroller|MissionFlag.VsTerran|MissionFlag.HasRaceSwap
    MEDIA_BLITZ = 20, "Media Blitz (Terran)", SC2Campaign.WOL, "Rebellion", SC2Race.TERRAN, MissionPools.MEDIUM, "ap_media_blitz", MissionFlag.Terran|MissionFlag.VsTerran|MissionFlag.HasRaceSwap
    PIERCING_OF_THE_SHROUD = 21, "Piercing the Shroud", SC2Campaign.WOL, "Rebellion", SC2Race.TERRAN, MissionPools.STARTER, "ap_piercing_the_shroud", MissionFlag.Terran|MissionFlag.NoBuild|MissionFlag.VsAll
    GATES_OF_HELL = 26, "Gates of Hell", SC2Campaign.WOL, "Char", SC2Race.TERRAN, MissionPools.HARD, "ap_gates_of_hell", MissionFlag.Terran|MissionFlag.VsZerg
    BELLY_OF_THE_BEAST = 27, "Belly of the Beast", SC2Campaign.WOL, "Char", SC2Race.ANY, MissionPools.STARTER, "ap_belly_of_the_beast", MissionFlag.Terran|MissionFlag.NoBuild|MissionFlag.VsZerg
    SHATTER_THE_SKY = 28, "Shatter the Sky (Terran)", SC2Campaign.WOL, "Char", SC2Race.TERRAN, MissionPools.HARD, "ap_shatter_the_sky", MissionFlag.Terran|MissionFlag.VsZerg|MissionFlag.HasRaceSwap
    ALL_IN = 29, "All-In (Terran)", SC2Campaign.WOL, "Char", SC2Race.TERRAN, MissionPools.VERY_HARD, "ap_all_in", MissionFlag.Terran|MissionFlag.TimedDefense|MissionFlag.VsZerg|MissionFlag.HasRaceSwap

    # Prophecy
    WHISPERS_OF_DOOM = 22, "Whispers of Doom", SC2Campaign.PROPHECY, "_1", SC2Race.ANY, MissionPools.STARTER, "ap_whispers_of_doom", MissionFlag.Protoss|MissionFlag.NoBuild|MissionFlag.VsZerg
    A_SINISTER_TURN = 23, "A Sinister Turn", SC2Campaign.PROPHECY, "_2", SC2Race.PROTOSS, MissionPools.MEDIUM, "ap_a_sinister_turn", MissionFlag.Protoss|MissionFlag.VsProtoss
    ECHOES_OF_THE_FUTURE = 24, "Echoes of the Future", SC2Campaign.PROPHECY, "_3", SC2Race.PROTOSS, MissionPools.MEDIUM, "ap_echoes_of_the_future", MissionFlag.Protoss|MissionFlag.VsZerg
    IN_UTTER_DARKNESS = 25, "In Utter Darkness", SC2Campaign.PROPHECY, "_4", SC2Race.PROTOSS, MissionPools.HARD, "ap_in_utter_darkness", MissionFlag.Protoss|MissionFlag.TimedDefense|MissionFlag.VsZerg

    # Heart of the Swarm
    LAB_RAT = 30, "Lab Rat", SC2Campaign.HOTS, "Umoja", SC2Race.ZERG, MissionPools.STARTER, "ap_lab_rat", MissionFlag.Zerg|MissionFlag.VsTerran
    BACK_IN_THE_SADDLE = 31, "Back in the Saddle", SC2Campaign.HOTS, "Umoja", SC2Race.ANY, MissionPools.STARTER, "ap_back_in_the_saddle", MissionFlag.Zerg|MissionFlag.Kerrigan|MissionFlag.NoBuild|MissionFlag.VsTZ
    RENDEZVOUS = 32, "Rendezvous", SC2Campaign.HOTS, "Umoja", SC2Race.ZERG, MissionPools.EASY, "ap_rendezvous", MissionFlag.Zerg|MissionFlag.Kerrigan|MissionFlag.AutoScroller|MissionFlag.VsTerran
    HARVEST_OF_SCREAMS = 33, "Harvest of Screams", SC2Campaign.HOTS, "Kaldir", SC2Race.ZERG, MissionPools.EASY, "ap_harvest_of_screams", MissionFlag.Zerg|MissionFlag.Kerrigan|MissionFlag.VsProtoss
    SHOOT_THE_MESSENGER = 34, "Shoot the Messenger", SC2Campaign.HOTS, "Kaldir", SC2Race.ZERG, MissionPools.EASY, "ap_shoot_the_messenger", MissionFlag.Zerg|MissionFlag.Kerrigan|MissionFlag.TimedDefense|MissionFlag.Countdown|MissionFlag.VsProtoss
    ENEMY_WITHIN = 35, "Enemy Within", SC2Campaign.HOTS, "Kaldir", SC2Race.ANY, MissionPools.EASY, "ap_enemy_within", MissionFlag.Zerg|MissionFlag.NoBuild|MissionFlag.VsProtoss
    DOMINATION = 36, "Domination", SC2Campaign.HOTS, "Char", SC2Race.ZERG, MissionPools.EASY, "ap_domination", MissionFlag.Zerg|MissionFlag.Kerrigan|MissionFlag.Countdown|MissionFlag.VsZerg
    FIRE_IN_THE_SKY = 37, "Fire in the Sky", SC2Campaign.HOTS, "Char", SC2Race.ZERG, MissionPools.MEDIUM, "ap_fire_in_the_sky", MissionFlag.Zerg|MissionFlag.Kerrigan|MissionFlag.Countdown|MissionFlag.VsTerran
    OLD_SOLDIERS = 38, "Old Soldiers", SC2Campaign.HOTS, "Char", SC2Race.ZERG, MissionPools.MEDIUM, "ap_old_soldiers", MissionFlag.Zerg|MissionFlag.Kerrigan|MissionFlag.VsTerran
    WAKING_THE_ANCIENT = 39, "Waking the Ancient", SC2Campaign.HOTS, "Zerus", SC2Race.ZERG, MissionPools.MEDIUM, "ap_waking_the_ancient", MissionFlag.Zerg|MissionFlag.Kerrigan|MissionFlag.VsZerg
    THE_CRUCIBLE = 40, "The Crucible", SC2Campaign.HOTS, "Zerus", SC2Race.ZERG, MissionPools.MEDIUM, "ap_the_crucible", MissionFlag.Zerg|MissionFlag.TimedDefense|MissionFlag.VsZerg
    SUPREME = 41, "Supreme", SC2Campaign.HOTS, "Zerus", SC2Race.ANY, MissionPools.MEDIUM, "ap_supreme", MissionFlag.Zerg|MissionFlag.Kerrigan|MissionFlag.NoBuild|MissionFlag.VsZerg
    INFESTED = 42, "Infested", SC2Campaign.HOTS, "Skygeirr Station", SC2Race.ZERG, MissionPools.MEDIUM, "ap_infested", MissionFlag.Zerg|MissionFlag.Kerrigan|MissionFlag.VsTerran
    HAND_OF_DARKNESS = 43, "Hand of Darkness", SC2Campaign.HOTS, "Skygeirr Station", SC2Race.ZERG, MissionPools.HARD, "ap_hand_of_darkness", MissionFlag.Zerg|MissionFlag.Kerrigan|MissionFlag.Countdown|MissionFlag.VsTerran
    PHANTOMS_OF_THE_VOID = 44, "Phantoms of the Void", SC2Campaign.HOTS, "Skygeirr Station", SC2Race.ZERG, MissionPools.HARD, "ap_phantoms_of_the_void", MissionFlag.Zerg|MissionFlag.Countdown|MissionFlag.VsProtoss
    WITH_FRIENDS_LIKE_THESE = 45, "With Friends Like These", SC2Campaign.HOTS, "Dominion Space", SC2Race.ANY, MissionPools.STARTER, "ap_with_friends_like_these", MissionFlag.Terran|MissionFlag.NoBuild|MissionFlag.VsTerran
    CONVICTION = 46, "Conviction", SC2Campaign.HOTS, "Dominion Space", SC2Race.ANY, MissionPools.MEDIUM, "ap_conviction", MissionFlag.Zerg|MissionFlag.Kerrigan|MissionFlag.NoBuild|MissionFlag.VsTerran
    PLANETFALL = 47, "Planetfall", SC2Campaign.HOTS, "Korhal", SC2Race.ZERG, MissionPools.HARD, "ap_planetfall", MissionFlag.Zerg|MissionFlag.Kerrigan|MissionFlag.AutoScroller|MissionFlag.VsTerran
    DEATH_FROM_ABOVE = 48, "Death From Above", SC2Campaign.HOTS, "Korhal", SC2Race.ZERG, MissionPools.HARD, "ap_death_from_above", MissionFlag.Zerg|MissionFlag.Kerrigan|MissionFlag.VsTerran
    THE_RECKONING = 49, "The Reckoning", SC2Campaign.HOTS, "Korhal", SC2Race.ZERG, MissionPools.VERY_HARD, "ap_the_reckoning", MissionFlag.Zerg|MissionFlag.Kerrigan|MissionFlag.VsTerran|MissionFlag.AiTerranAlly

    # Prologue
    DARK_WHISPERS = 50, "Dark Whispers", SC2Campaign.PROLOGUE, "_1", SC2Race.PROTOSS, MissionPools.EASY, "ap_dark_whispers", MissionFlag.Protoss|MissionFlag.Countdown|MissionFlag.VsTZ
    GHOSTS_IN_THE_FOG = 51, "Ghosts in the Fog", SC2Campaign.PROLOGUE, "_2", SC2Race.PROTOSS, MissionPools.MEDIUM, "ap_ghosts_in_the_fog", MissionFlag.Protoss|MissionFlag.VsProtoss
    EVIL_AWOKEN = 52, "Evil Awoken", SC2Campaign.PROLOGUE, "_3", SC2Race.PROTOSS, MissionPools.STARTER, "ap_evil_awoken", MissionFlag.Protoss|MissionFlag.NoBuild|MissionFlag.VsProtoss

    # LotV
    FOR_AIUR = 53, "For Aiur!", SC2Campaign.LOTV, "Aiur", SC2Race.ANY, MissionPools.STARTER, "ap_for_aiur", MissionFlag.Protoss|MissionFlag.NoBuild|MissionFlag.VsZerg
    THE_GROWING_SHADOW = 54, "The Growing Shadow", SC2Campaign.LOTV, "Aiur", SC2Race.PROTOSS, MissionPools.EASY, "ap_the_growing_shadow", MissionFlag.Protoss|MissionFlag.VsPZ
    THE_SPEAR_OF_ADUN = 55, "The Spear of Adun", SC2Campaign.LOTV, "Aiur", SC2Race.PROTOSS, MissionPools.EASY, "ap_the_spear_of_adun", MissionFlag.Protoss|MissionFlag.VanillaSoa|MissionFlag.VsPZ
    SKY_SHIELD = 56, "Sky Shield", SC2Campaign.LOTV, "Korhal", SC2Race.PROTOSS, MissionPools.EASY, "ap_sky_shield", MissionFlag.Protoss|MissionFlag.VanillaSoa|MissionFlag.Countdown|MissionFlag.VsTerran|MissionFlag.AiTerranAlly
    BROTHERS_IN_ARMS = 57, "Brothers in Arms", SC2Campaign.LOTV, "Korhal", SC2Race.PROTOSS, MissionPools.MEDIUM, "ap_brothers_in_arms", MissionFlag.Protoss|MissionFlag.VanillaSoa|MissionFlag.VsTerran|MissionFlag.AiTerranAlly
    AMON_S_REACH = 58, "Amon's Reach", SC2Campaign.LOTV, "Shakuras", SC2Race.PROTOSS, MissionPools.EASY, "ap_amon_s_reach", MissionFlag.Protoss|MissionFlag.VanillaSoa|MissionFlag.VsZerg
    LAST_STAND = 59, "Last Stand", SC2Campaign.LOTV, "Shakuras", SC2Race.PROTOSS, MissionPools.HARD, "ap_last_stand", MissionFlag.Protoss|MissionFlag.VanillaSoa|MissionFlag.TimedDefense|MissionFlag.VsZerg
    FORBIDDEN_WEAPON = 60, "Forbidden Weapon", SC2Campaign.LOTV, "Purifier", SC2Race.PROTOSS, MissionPools.MEDIUM, "ap_forbidden_weapon", MissionFlag.Protoss|MissionFlag.VanillaSoa|MissionFlag.Countdown|MissionFlag.VsProtoss
    TEMPLE_OF_UNIFICATION = 61, "Temple of Unification", SC2Campaign.LOTV, "Ulnar", SC2Race.PROTOSS, MissionPools.MEDIUM, "ap_temple_of_unification", MissionFlag.Protoss|MissionFlag.VanillaSoa|MissionFlag.VsTP
    THE_INFINITE_CYCLE = 62, "The Infinite Cycle", SC2Campaign.LOTV, "Ulnar", SC2Race.ANY, MissionPools.HARD, "ap_the_infinite_cycle", MissionFlag.Protoss|MissionFlag.Kerrigan|MissionFlag.NoBuild|MissionFlag.VsTP
    HARBINGER_OF_OBLIVION = 63, "Harbinger of Oblivion", SC2Campaign.LOTV, "Ulnar", SC2Race.PROTOSS, MissionPools.MEDIUM, "ap_harbinger_of_oblivion", MissionFlag.Protoss|MissionFlag.VanillaSoa|MissionFlag.Countdown|MissionFlag.VsTP|MissionFlag.AiZergAlly
    UNSEALING_THE_PAST = 64, "Unsealing the Past", SC2Campaign.LOTV, "Purifier", SC2Race.PROTOSS, MissionPools.MEDIUM, "ap_unsealing_the_past", MissionFlag.Protoss|MissionFlag.VanillaSoa|MissionFlag.AutoScroller|MissionFlag.VsZerg
    PURIFICATION = 65, "Purification", SC2Campaign.LOTV, "Purifier", SC2Race.PROTOSS, MissionPools.HARD, "ap_purification", MissionFlag.Protoss|MissionFlag.VanillaSoa|MissionFlag.VsZerg
    STEPS_OF_THE_RITE = 66, "Steps of the Rite", SC2Campaign.LOTV, "Tal'darim", SC2Race.PROTOSS, MissionPools.HARD, "ap_steps_of_the_rite", MissionFlag.Protoss|MissionFlag.VanillaSoa|MissionFlag.VsProtoss
    RAK_SHIR = 67, "Rak'Shir", SC2Campaign.LOTV, "Tal'darim", SC2Race.PROTOSS, MissionPools.HARD, "ap_rak_shir", MissionFlag.Protoss|MissionFlag.VanillaSoa|MissionFlag.VsProtoss
    TEMPLAR_S_CHARGE = 68, "Templar's Charge", SC2Campaign.LOTV, "Moebius", SC2Race.PROTOSS, MissionPools.HARD, "ap_templar_s_charge", MissionFlag.Protoss|MissionFlag.VanillaSoa|MissionFlag.VsTerran
    TEMPLAR_S_RETURN = 69, "Templar's Return", SC2Campaign.LOTV, "Return to Aiur", SC2Race.PROTOSS, MissionPools.EASY, "ap_templar_s_return", MissionFlag.Protoss|MissionFlag.NoBuild|MissionFlag.VsPZ
    THE_HOST = 70, "The Host", SC2Campaign.LOTV, "Return to Aiur", SC2Race.PROTOSS, MissionPools.HARD, "ap_the_host", MissionFlag.Protoss|MissionFlag.VanillaSoa|MissionFlag.VsAll
    SALVATION = 71, "Salvation", SC2Campaign.LOTV, "Return to Aiur", SC2Race.PROTOSS, MissionPools.VERY_HARD, "ap_salvation", MissionFlag.Protoss|MissionFlag.VanillaSoa|MissionFlag.TimedDefense|MissionFlag.VsPZ|MissionFlag.AiProtossAlly

    # Epilogue
    INTO_THE_VOID = 72, "Into the Void", SC2Campaign.EPILOGUE, "_1", SC2Race.PROTOSS, MissionPools.VERY_HARD, "ap_into_the_void", MissionFlag.Protoss|MissionFlag.VanillaSoa|MissionFlag.VsAll|MissionFlag.AiTerranAlly|MissionFlag.AiZergAlly
    THE_ESSENCE_OF_ETERNITY = 73, "The Essence of Eternity", SC2Campaign.EPILOGUE, "_2", SC2Race.TERRAN, MissionPools.VERY_HARD, "ap_the_essence_of_eternity", MissionFlag.Terran|MissionFlag.TimedDefense|MissionFlag.VsAll|MissionFlag.AiZergAlly|MissionFlag.AiProtossAlly
    AMON_S_FALL = 74, "Amon's Fall", SC2Campaign.EPILOGUE, "_3", SC2Race.ZERG, MissionPools.VERY_HARD, "ap_amon_s_fall", MissionFlag.Zerg|MissionFlag.Kerrigan|MissionFlag.AutoScroller|MissionFlag.VsAll|MissionFlag.AiTerranAlly|MissionFlag.AiProtossAlly

    # Nova Covert Ops
    THE_ESCAPE = 75, "The Escape", SC2Campaign.NCO, "_1", SC2Race.ANY, MissionPools.MEDIUM, "ap_the_escape", MissionFlag.Terran|MissionFlag.Nova|MissionFlag.NoBuild|MissionFlag.VsTerran
    SUDDEN_STRIKE = 76, "Sudden Strike", SC2Campaign.NCO, "_1", SC2Race.TERRAN, MissionPools.EASY, "ap_sudden_strike", MissionFlag.Terran|MissionFlag.Nova|MissionFlag.TimedDefense|MissionFlag.VsZerg
    ENEMY_INTELLIGENCE = 77, "Enemy Intelligence", SC2Campaign.NCO, "_1", SC2Race.TERRAN, MissionPools.MEDIUM, "ap_enemy_intelligence", MissionFlag.Terran|MissionFlag.Nova|MissionFlag.Defense|MissionFlag.VsZerg
    TROUBLE_IN_PARADISE = 78, "Trouble In Paradise", SC2Campaign.NCO, "_2", SC2Race.TERRAN, MissionPools.HARD, "ap_trouble_in_paradise", MissionFlag.Terran|MissionFlag.Nova|MissionFlag.Countdown|MissionFlag.VsPZ
    NIGHT_TERRORS = 79, "Night Terrors", SC2Campaign.NCO, "_2", SC2Race.TERRAN, MissionPools.MEDIUM, "ap_night_terrors", MissionFlag.Terran|MissionFlag.Nova|MissionFlag.VsPZ
    FLASHPOINT = 80, "Flashpoint", SC2Campaign.NCO, "_2", SC2Race.TERRAN, MissionPools.HARD, "ap_flashpoint", MissionFlag.Terran|MissionFlag.Nova|MissionFlag.VsZerg
    IN_THE_ENEMY_S_SHADOW = 81, "In the Enemy's Shadow", SC2Campaign.NCO, "_3", SC2Race.TERRAN, MissionPools.MEDIUM, "ap_in_the_enemy_s_shadow", MissionFlag.Terran|MissionFlag.Nova|MissionFlag.NoBuild|MissionFlag.VsTerran
    DARK_SKIES = 82, "Dark Skies", SC2Campaign.NCO, "_3", SC2Race.TERRAN, MissionPools.HARD, "ap_dark_skies", MissionFlag.Terran|MissionFlag.Nova|MissionFlag.TimedDefense|MissionFlag.VsProtoss
    END_GAME = 83, "End Game", SC2Campaign.NCO, "_3", SC2Race.TERRAN, MissionPools.VERY_HARD, "ap_end_game", MissionFlag.Terran|MissionFlag.Nova|MissionFlag.Defense|MissionFlag.VsTerran

    # Race-Swapped Variants
    # 84/85 - Liberation Day
    THE_OUTLAWS_Z = 86, "The Outlaws (Zerg)", SC2Campaign.WOL, "Mar Sara", SC2Race.ZERG, MissionPools.EASY, "ap_the_outlaws", MissionFlag.Zerg|MissionFlag.VsTerran|MissionFlag.RaceSwap
    THE_OUTLAWS_P = 87, "The Outlaws (Protoss)", SC2Campaign.WOL, "Mar Sara", SC2Race.PROTOSS, MissionPools.EASY, "ap_the_outlaws", MissionFlag.Protoss|MissionFlag.VsTerran|MissionFlag.RaceSwap
    ZERO_HOUR_Z = 88, "Zero Hour (Zerg)", SC2Campaign.WOL, "Mar Sara", SC2Race.ZERG, MissionPools.EASY, "ap_zero_hour", MissionFlag.Zerg|MissionFlag.TimedDefense|MissionFlag.VsZerg|MissionFlag.RaceSwap
    ZERO_HOUR_P = 89, "Zero Hour (Protoss)", SC2Campaign.WOL, "Mar Sara", SC2Race.PROTOSS, MissionPools.EASY, "ap_zero_hour", MissionFlag.Protoss|MissionFlag.TimedDefense|MissionFlag.VsZerg|MissionFlag.RaceSwap
    EVACUATION_Z = 90, "Evacuation (Zerg)", SC2Campaign.WOL, "Colonist", SC2Race.ZERG, MissionPools.EASY, "ap_evacuation", MissionFlag.Zerg|MissionFlag.AutoScroller|MissionFlag.VsZerg|MissionFlag.RaceSwap
    EVACUATION_P = 91, "Evacuation (Protoss)", SC2Campaign.WOL, "Colonist", SC2Race.PROTOSS, MissionPools.EASY, "ap_evacuation", MissionFlag.Protoss|MissionFlag.AutoScroller|MissionFlag.VsZerg|MissionFlag.RaceSwap
    OUTBREAK_Z = 92, "Outbreak (Zerg)", SC2Campaign.WOL, "Colonist", SC2Race.ZERG, MissionPools.EASY, "ap_outbreak", MissionFlag.Zerg|MissionFlag.Defense|MissionFlag.VsZerg|MissionFlag.RaceSwap
    OUTBREAK_P = 93, "Outbreak (Protoss)", SC2Campaign.WOL, "Colonist", SC2Race.PROTOSS, MissionPools.EASY, "ap_outbreak", MissionFlag.Protoss|MissionFlag.Defense|MissionFlag.VsZerg|MissionFlag.RaceSwap
    SAFE_HAVEN_Z = 94, "Safe Haven (Zerg)", SC2Campaign.WOL, "Colonist", SC2Race.ZERG, MissionPools.MEDIUM, "ap_safe_haven", MissionFlag.Zerg|MissionFlag.Countdown|MissionFlag.VsProtoss|MissionFlag.RaceSwap
    SAFE_HAVEN_P = 95, "Safe Haven (Protoss)", SC2Campaign.WOL, "Colonist", SC2Race.PROTOSS, MissionPools.MEDIUM, "ap_safe_haven", MissionFlag.Protoss|MissionFlag.Countdown|MissionFlag.VsProtoss|MissionFlag.RaceSwap
    HAVENS_FALL_Z = 96, "Haven's Fall (Zerg)", SC2Campaign.WOL, "Colonist", SC2Race.ZERG, MissionPools.MEDIUM, "ap_havens_fall", MissionFlag.Zerg|MissionFlag.VsZerg|MissionFlag.RaceSwap
    HAVENS_FALL_P = 97, "Haven's Fall (Protoss)", SC2Campaign.WOL, "Colonist", SC2Race.PROTOSS, MissionPools.MEDIUM, "ap_havens_fall", MissionFlag.Protoss|MissionFlag.VsZerg|MissionFlag.RaceSwap
    SMASH_AND_GRAB_Z = 98, "Smash and Grab (Zerg)", SC2Campaign.WOL, "Artifact", SC2Race.ZERG, MissionPools.EASY, "ap_smash_and_grab", MissionFlag.Zerg|MissionFlag.Countdown|MissionFlag.VsPZ|MissionFlag.RaceSwap
    SMASH_AND_GRAB_P = 99, "Smash and Grab (Protoss)", SC2Campaign.WOL, "Artifact", SC2Race.PROTOSS, MissionPools.EASY, "ap_smash_and_grab", MissionFlag.Protoss|MissionFlag.Countdown|MissionFlag.VsPZ|MissionFlag.RaceSwap
    # 100/101 - The Dig
    # 102/103 - Moebius Factor
    # 104/105 - Supernova
    # 106/107 - Maw of the Void
    DEVILS_PLAYGROUND_Z = 108, "Devil's Playground (Zerg)", SC2Campaign.WOL, "Covert", SC2Race.ZERG, MissionPools.EASY, "ap_devils_playground", MissionFlag.Zerg|MissionFlag.VsZerg|MissionFlag.RaceSwap
    DEVILS_PLAYGROUND_P = 109, "Devil's Playground (Protoss)", SC2Campaign.WOL, "Covert", SC2Race.PROTOSS, MissionPools.EASY, "ap_devils_playground", MissionFlag.Protoss|MissionFlag.VsZerg|MissionFlag.RaceSwap
    WELCOME_TO_THE_JUNGLE_Z = 110, "Welcome to the Jungle (Zerg)", SC2Campaign.WOL, "Covert", SC2Race.ZERG, MissionPools.MEDIUM, "ap_welcome_to_the_jungle", MissionFlag.Zerg|MissionFlag.VsProtoss|MissionFlag.RaceSwap
    WELCOME_TO_THE_JUNGLE_P = 111, "Welcome to the Jungle (Protoss)", SC2Campaign.WOL, "Covert", SC2Race.PROTOSS, MissionPools.MEDIUM, "ap_welcome_to_the_jungle", MissionFlag.Protoss|MissionFlag.VsProtoss|MissionFlag.RaceSwap
    # 112/113 - Breakout
    # 114/115 - Ghost of a Chance
    THE_GREAT_TRAIN_ROBBERY_Z = 116, "The Great Train Robbery (Zerg)", SC2Campaign.WOL, "Rebellion", SC2Race.ZERG, MissionPools.MEDIUM, "ap_the_great_train_robbery", MissionFlag.Zerg|MissionFlag.AutoScroller|MissionFlag.VsTerran|MissionFlag.RaceSwap
    THE_GREAT_TRAIN_ROBBERY_P = 117, "The Great Train Robbery (Protoss)", SC2Campaign.WOL, "Rebellion", SC2Race.PROTOSS, MissionPools.MEDIUM, "ap_the_great_train_robbery", MissionFlag.Protoss|MissionFlag.AutoScroller|MissionFlag.VsTerran|MissionFlag.RaceSwap
    CUTTHROAT_Z = 118, "Cutthroat (Zerg)", SC2Campaign.WOL, "Rebellion", SC2Race.ZERG, MissionPools.MEDIUM, "ap_cutthroat", MissionFlag.Zerg|MissionFlag.Countdown|MissionFlag.VsTerran|MissionFlag.RaceSwap
    CUTTHROAT_P = 119, "Cutthroat (Protoss)", SC2Campaign.WOL, "Rebellion", SC2Race.PROTOSS, MissionPools.MEDIUM, "ap_cutthroat", MissionFlag.Protoss|MissionFlag.Countdown|MissionFlag.VsTerran|MissionFlag.RaceSwap
    ENGINE_OF_DESTRUCTION_Z = 120, "Engine of Destruction (Zerg)", SC2Campaign.WOL, "Rebellion", SC2Race.ZERG, MissionPools.HARD, "ap_engine_of_destruction", MissionFlag.Zerg|MissionFlag.AutoScroller|MissionFlag.VsTerran|MissionFlag.RaceSwap
    ENGINE_OF_DESTRUCTION_P = 121, "Engine of Destruction (Protoss)", SC2Campaign.WOL, "Rebellion", SC2Race.PROTOSS, MissionPools.HARD, "ap_engine_of_destruction", MissionFlag.Protoss|MissionFlag.AutoScroller|MissionFlag.VsTerran|MissionFlag.RaceSwap
    MEDIA_BLITZ_Z = 122, "Media Blitz (Zerg)", SC2Campaign.WOL, "Rebellion", SC2Race.ZERG, MissionPools.MEDIUM, "ap_media_blitz", MissionFlag.Zerg|MissionFlag.VsTerran|MissionFlag.RaceSwap
    MEDIA_BLITZ_P = 123, "Media Blitz (Protoss)", SC2Campaign.WOL, "Rebellion", SC2Race.PROTOSS, MissionPools.MEDIUM, "ap_media_blitz", MissionFlag.Protoss|MissionFlag.VsTerran|MissionFlag.RaceSwap
    # 124/125 - Piercing the Shroud
    # 126/127 - Whispers of Doom
    # 128/129 - A Sinister Turn
    # 130/131 - Echoes of the Future
    # 132/133 - In Utter Darkness
    # 134/135 - Gates of Hell
    # 136/137 - Belly of the Beast
    SHATTER_THE_SKY_Z = 138, "Shatter the Sky (Zerg)", SC2Campaign.WOL, "Char", SC2Race.ZERG, MissionPools.HARD, "ap_shatter_the_sky", MissionFlag.Zerg|MissionFlag.VsZerg|MissionFlag.RaceSwap
    SHATTER_THE_SKY_P = 139, "Shatter the Sky (Protoss)", SC2Campaign.WOL, "Char", SC2Race.PROTOSS, MissionPools.HARD, "ap_shatter_the_sky", MissionFlag.Protoss|MissionFlag.VsZerg|MissionFlag.RaceSwap
    ALL_IN_Z = 140, "All-In (Zerg)", SC2Campaign.WOL, "Char", SC2Race.ZERG, MissionPools.VERY_HARD, "ap_all_in", MissionFlag.Zerg|MissionFlag.TimedDefense|MissionFlag.VsZerg|MissionFlag.RaceSwap
    ALL_IN_P = 141, "All-In (Protoss)", SC2Campaign.WOL, "Char", SC2Race.PROTOSS, MissionPools.VERY_HARD, "ap_all_in", MissionFlag.Protoss|MissionFlag.TimedDefense|MissionFlag.VsZerg|MissionFlag.RaceSwap
    # 142/143 - Lab Rat
    # 144/145 - Back in the Saddle
    # 146/147 - Rendezvous
    # 148/149 - Harvest of Screams
    # 150/151 - Shoot the Messenger
    # 152/153 - Enemy Within
    # 154/155 - Fire in the Sky
    # 156/157 - Old Soldiers
    # 158/159 - Waking the Ancient
    # 160/161 - The Crucible
    # 162/163 - Supreme
    # 164/165 - Infested
    # 166/167 - Hand of Darkness
    # 168/169 - Phantoms of the Void
    # 170/171 - With Friends Like These
    # 172/173 - Conviction
    # 174/175 - Planetfall
    # 176/177 - Death From Above
    # 178/179 - The Reckoning


class MissionConnection:
    campaign: SC2Campaign
    connect_to: int  # -1 connects to Menu

    def __init__(self, connect_to, campaign = SC2Campaign.GLOBAL):
        self.campaign = campaign
        self.connect_to = connect_to

    def _asdict(self):
        return {
            "campaign": self.campaign.id,
            "connect_to": self.connect_to
        }


class MissionInfo(NamedTuple):
    mission: SC2Mission
    required_world: List[Union[MissionConnection, Dict[Literal["campaign", "connect_to"], int]]]
    category: str
    number: int = 0  # number of worlds need beaten
    completion_critical: bool = False  # missions needed to beat game
    or_requirements: bool = False  # true if the requirements should be or-ed instead of and-ed
    ui_vertical_padding: int = 0   # How many blank padding tiles go above this mission in the launcher



lookup_id_to_mission: Dict[int, SC2Mission] = {
    mission.id: mission for mission in SC2Mission
}

lookup_name_to_mission: Dict[str, SC2Mission] = {
    mission.mission_name: mission for mission in SC2Mission
}
for mission in SC2Mission:
    if MissionFlag.HasRaceSwap in mission.flags and ' (' in mission.mission_name:
        # Short names for non-race-swapped missions for client compatibility
        short_name = mission.mission_name[:mission.mission_name.find(' (')]
        lookup_name_to_mission[short_name] = mission

lookup_id_to_campaign: Dict[int, SC2Campaign] = {
    campaign.id: campaign for campaign in SC2Campaign
}


campaign_mission_table: Dict[SC2Campaign, Set[SC2Mission]] = {
    campaign: set() for campaign in SC2Campaign
}
for mission in SC2Mission:
    campaign_mission_table[mission.campaign].add(mission)


def get_campaign_difficulty(campaign: SC2Campaign, excluded_missions: Iterable[SC2Mission] = ()) -> MissionPools:
    """

    :param campaign:
    :param excluded_missions:
    :return: Campaign's the most difficult non-excluded mission
    """
    excluded_mission_set = set(excluded_missions)
    included_missions = campaign_mission_table[campaign].difference(excluded_mission_set)
    return max([mission.pool for mission in included_missions])


def get_campaign_goal_priority(campaign: SC2Campaign, excluded_missions: Iterable[SC2Mission] = ()) -> SC2CampaignGoalPriority:
    """
    Gets a modified campaign goal priority.
    If all the campaign's goal missions are excluded, it's ineligible to have the goal
    If the campaign's very hard missions are excluded, the priority is lowered to hard
    :param campaign:
    :param excluded_missions:
    :return:
    """
    if excluded_missions is None:
        return campaign.goal_priority
    else:
        goal_missions = set(get_campaign_potential_goal_missions(campaign))
        excluded_mission_set = set(excluded_missions)
        remaining_goals = goal_missions.difference(excluded_mission_set)
        if remaining_goals == set():
            # All potential goals are excluded, the campaign can't be a goal
            return SC2CampaignGoalPriority.NONE
        elif campaign.goal_priority == SC2CampaignGoalPriority.VERY_HARD:
            # Check if a very hard campaign doesn't get rid of it's last very hard mission
            difficulty = get_campaign_difficulty(campaign, excluded_missions)
            if difficulty == MissionPools.VERY_HARD:
                return SC2CampaignGoalPriority.VERY_HARD
            else:
                return SC2CampaignGoalPriority.HARD
        else:
            return campaign.goal_priority


class SC2CampaignGoal(NamedTuple):
    mission: SC2Mission
    location: str


campaign_final_mission_locations: Dict[SC2Campaign, Optional[SC2CampaignGoal]] = {
    SC2Campaign.WOL: SC2CampaignGoal(SC2Mission.ALL_IN, f'{SC2Mission.ALL_IN.mission_name}: Victory'),
    SC2Campaign.PROPHECY: SC2CampaignGoal(SC2Mission.IN_UTTER_DARKNESS, f'{SC2Mission.IN_UTTER_DARKNESS.mission_name}: Kills'),
    SC2Campaign.HOTS: SC2CampaignGoal(SC2Mission.THE_RECKONING, f'{SC2Mission.THE_RECKONING.mission_name}: Victory'),
    SC2Campaign.PROLOGUE: SC2CampaignGoal(SC2Mission.EVIL_AWOKEN, f'{SC2Mission.EVIL_AWOKEN.mission_name}: Victory'),
    SC2Campaign.LOTV: SC2CampaignGoal(SC2Mission.SALVATION, f'{SC2Mission.SALVATION.mission_name}: Victory'),
    SC2Campaign.EPILOGUE: None,
    SC2Campaign.NCO: SC2CampaignGoal(SC2Mission.END_GAME, f'{SC2Mission.END_GAME.mission_name}: Victory'),
}

campaign_alt_final_mission_locations: Dict[SC2Campaign, Dict[SC2Mission, str]] = {
    SC2Campaign.WOL: {
        SC2Mission.MAW_OF_THE_VOID: f'{SC2Mission.MAW_OF_THE_VOID.mission_name}: Victory',
        SC2Mission.ENGINE_OF_DESTRUCTION: f'{SC2Mission.ENGINE_OF_DESTRUCTION.mission_name}: Victory',
        SC2Mission.SUPERNOVA: f'{SC2Mission.SUPERNOVA.mission_name}: Victory',
        SC2Mission.GATES_OF_HELL: f'{SC2Mission.GATES_OF_HELL.mission_name}: Victory',
        SC2Mission.SHATTER_THE_SKY: f'{SC2Mission.SHATTER_THE_SKY.mission_name}: Victory'
    },
    SC2Campaign.PROPHECY: None,
    SC2Campaign.HOTS: {
        SC2Mission.THE_CRUCIBLE: f'{SC2Mission.THE_CRUCIBLE.mission_name}: Victory',
        SC2Mission.HAND_OF_DARKNESS: f'{SC2Mission.HAND_OF_DARKNESS.mission_name}: Victory',
        SC2Mission.PHANTOMS_OF_THE_VOID: f'{SC2Mission.PHANTOMS_OF_THE_VOID.mission_name}: Victory',
        SC2Mission.PLANETFALL: f'{SC2Mission.PLANETFALL.mission_name}: Victory',
        SC2Mission.DEATH_FROM_ABOVE: f'{SC2Mission.DEATH_FROM_ABOVE.mission_name}: Victory'
    },
    SC2Campaign.PROLOGUE: {
        SC2Mission.GHOSTS_IN_THE_FOG: f'{SC2Mission.GHOSTS_IN_THE_FOG.mission_name}: Victory'
    },
    SC2Campaign.LOTV: {
        SC2Mission.THE_HOST: f'{SC2Mission.THE_HOST.mission_name}: Victory',
        SC2Mission.TEMPLAR_S_CHARGE: f'{SC2Mission.TEMPLAR_S_CHARGE.mission_name}: Victory'
    },
    SC2Campaign.EPILOGUE: {
        SC2Mission.AMON_S_FALL: f'{SC2Mission.AMON_S_FALL.mission_name}: Victory',
        SC2Mission.INTO_THE_VOID: f'{SC2Mission.INTO_THE_VOID.mission_name}: Victory',
        SC2Mission.THE_ESSENCE_OF_ETERNITY: f'{SC2Mission.THE_ESSENCE_OF_ETERNITY.mission_name}: Victory',
    },
    SC2Campaign.NCO: {
        SC2Mission.FLASHPOINT: f'{SC2Mission.FLASHPOINT.mission_name}: Victory',
        SC2Mission.DARK_SKIES: f'{SC2Mission.DARK_SKIES.mission_name}: Victory',
        SC2Mission.NIGHT_TERRORS: f'{SC2Mission.NIGHT_TERRORS.mission_name}: Victory',
        SC2Mission.TROUBLE_IN_PARADISE: f'{SC2Mission.TROUBLE_IN_PARADISE.mission_name}: Victory'
    }
}

campaign_race_exceptions: Dict[SC2Mission, SC2Race] = {
    SC2Mission.WITH_FRIENDS_LIKE_THESE: SC2Race.TERRAN
}


def get_goal_location(mission: SC2Mission) -> Union[str, None]:
    """

    :param mission:
    :return: Goal location assigned to the goal mission
    """
    campaign = mission.campaign
    primary_campaign_goal = campaign_final_mission_locations[campaign]
    if primary_campaign_goal is not None:
        if primary_campaign_goal.mission == mission:
            return primary_campaign_goal.location

    campaign_alt_goals = campaign_alt_final_mission_locations[campaign]
    if campaign_alt_goals is not None and mission in campaign_alt_goals:
        return campaign_alt_goals.get(mission)

    return mission.mission_name + ": Victory"


def get_campaign_potential_goal_missions(campaign: SC2Campaign) -> List[SC2Mission]:
    """

    :param campaign:
    :return: All missions that can be the campaign's goal
    """
    missions: List[SC2Mission] = list()
    primary_goal_mission = campaign_final_mission_locations[campaign]
    if primary_goal_mission is not None:
        missions.append(primary_goal_mission.mission)
    alt_goal_locations = campaign_alt_final_mission_locations[campaign]
    if alt_goal_locations is not None:
        for mission in alt_goal_locations.keys():
            missions.append(mission)

    return missions


def get_missions_with_any_flags_in_list(flags: MissionFlag) -> List[SC2Mission]:
    return [mission for mission in SC2Mission if flags & mission.flags]
