from typing import List, Set, Dict, Tuple, Optional, Callable, Union
import math
from BaseClasses import MultiWorld, Region, Entrance, Location, CollectionState
from .Locations import LocationData
from .Options import get_option_value, MissionOrder
from .MissionTables import (MissionInfo, MissionInfoUiFlags, mission_orders,
    vanilla_mission_req_table, alt_final_mission_locations,
    MissionPools, mission_pool_names, vanilla_shuffle_order)
from .PoolFilter import filter_missions

# Allows for backward compatibility.
# Can be changed independently of the Archipelago version for asynchronous release
MISSION_GENERATOR_VERSION = 1

PROPHECY_CHAIN_MISSION_COUNT = 4

VANILLA_SHUFFLED_FIRST_PROPHECY_MISSION = 21


def create_regions(
    multiworld: MultiWorld,
    player: int,
    locations: Tuple[LocationData, ...],
    location_cache: List[Location]
) -> Tuple[Dict[str, MissionInfo], int, str]:
    """
    Creates region connections by calling the multiworld's `connect()` methods
    Returns a 3-tuple containing:
    * dict[str, MissionInfo] mapping a mission name to its data
    * int The number of missions in the world
    * str The name of the goal location
    """
    mission_order_type: int = multiworld.mission_order[player]

    if mission_order_type == MissionOrder.option_vanilla:
        return create_vanilla_regions(multiworld, player, locations, location_cache)
    elif mission_order_type == MissionOrder.option_grid:
        return create_grid_regions(multiworld, player, locations, location_cache)
    else:
        return create_structured_regions(multiworld, player, locations, location_cache, mission_order_type)


def create_vanilla_regions(
    multiworld: MultiWorld,
    player: int,
    locations: Tuple[LocationData, ...],
    location_cache: List[Location],
) -> Tuple[Dict[str, MissionInfo], int, str]:
    
    locations_per_region = initialize_locations_per_region(locations)
    regions = [create_region(multiworld, player, locations_per_region, location_cache, "Menu")]

    # Generating all regions and locations
    names: Dict[str, int] = {}
    for region_name in vanilla_mission_req_table.keys():
        regions.append(create_region(multiworld, player, locations_per_region, location_cache, region_name))
    multiworld.regions += regions

    connect(multiworld, player, names, 'Menu', 'Liberation Day'),
    connect(multiworld, player, names, 'Liberation Day', 'The Outlaws',
            lambda state: state.has("Beat Liberation Day", player)),
    connect(multiworld, player, names, 'The Outlaws', 'Zero Hour',
            lambda state: state.has("Beat The Outlaws", player)),
    connect(multiworld, player, names, 'Zero Hour', 'Evacuation',
            lambda state: state.has("Beat Zero Hour", player)),
    connect(multiworld, player, names, 'Evacuation', 'Outbreak',
            lambda state: state.has("Beat Evacuation", player)),
    connect(multiworld, player, names, "Outbreak", "Safe Haven",
            lambda state: state._sc2wol_cleared_missions(multiworld, player, 7) and
                            state.has("Beat Outbreak", player)),
    connect(multiworld, player, names, "Outbreak", "Haven's Fall",
            lambda state: state._sc2wol_cleared_missions(multiworld, player, 7) and
                            state.has("Beat Outbreak", player)),
    connect(multiworld, player, names, 'Zero Hour', 'Smash and Grab',
            lambda state: state.has("Beat Zero Hour", player)),
    connect(multiworld, player, names, 'Smash and Grab', 'The Dig',
            lambda state: state._sc2wol_cleared_missions(multiworld, player, 8) and
                            state.has("Beat Smash and Grab", player)),
    connect(multiworld, player, names, 'The Dig', 'The Moebius Factor',
            lambda state: state._sc2wol_cleared_missions(multiworld, player, 11) and
                            state.has("Beat The Dig", player)),
    connect(multiworld, player, names, 'The Moebius Factor', 'Supernova',
            lambda state: state._sc2wol_cleared_missions(multiworld, player, 14) and
                            state.has("Beat The Moebius Factor", player)),
    connect(multiworld, player, names, 'Supernova', 'Maw of the Void',
            lambda state: state.has("Beat Supernova", player)),
    connect(multiworld, player, names, 'Zero Hour', "Devil's Playground",
            lambda state: state._sc2wol_cleared_missions(multiworld, player, 4) and
                            state.has("Beat Zero Hour", player)),
    connect(multiworld, player, names, "Devil's Playground", 'Welcome to the Jungle',
            lambda state: state.has("Beat Devil's Playground", player)),
    connect(multiworld, player, names, "Welcome to the Jungle", 'Breakout',
            lambda state: state._sc2wol_cleared_missions(multiworld, player, 8) and
                            state.has("Beat Welcome to the Jungle", player)),
    connect(multiworld, player, names, "Welcome to the Jungle", 'Ghost of a Chance',
            lambda state: state._sc2wol_cleared_missions(multiworld, player, 8) and
                            state.has("Beat Welcome to the Jungle", player)),
    connect(multiworld, player, names, "Zero Hour", 'The Great Train Robbery',
            lambda state: state._sc2wol_cleared_missions(multiworld, player, 6) and
                            state.has("Beat Zero Hour", player)),
    connect(multiworld, player, names, 'The Great Train Robbery', 'Cutthroat',
            lambda state: state.has("Beat The Great Train Robbery", player)),
    connect(multiworld, player, names, 'Cutthroat', 'Engine of Destruction',
            lambda state: state.has("Beat Cutthroat", player)),
    connect(multiworld, player, names, 'Engine of Destruction', 'Media Blitz',
            lambda state: state.has("Beat Engine of Destruction", player)),
    connect(multiworld, player, names, 'Media Blitz', 'Piercing the Shroud',
            lambda state: state.has("Beat Media Blitz", player)),
    connect(multiworld, player, names, 'The Dig', 'Whispers of Doom',
            lambda state: state.has("Beat The Dig", player)),
    connect(multiworld, player, names, 'Whispers of Doom', 'A Sinister Turn',
            lambda state: state.has("Beat Whispers of Doom", player)),
    connect(multiworld, player, names, 'A Sinister Turn', 'Echoes of the Future',
            lambda state: state.has("Beat A Sinister Turn", player)),
    connect(multiworld, player, names, 'Echoes of the Future', 'In Utter Darkness',
            lambda state: state.has("Beat Echoes of the Future", player)),
    connect(multiworld, player, names, 'Maw of the Void', 'Gates of Hell',
            lambda state: state.has("Beat Maw of the Void", player)),
    connect(multiworld, player, names, 'Gates of Hell', 'Belly of the Beast',
            lambda state: state.has("Beat Gates of Hell", player)),
    connect(multiworld, player, names, 'Gates of Hell', 'Shatter the Sky',
            lambda state: state.has("Beat Gates of Hell", player)),
    connect(multiworld, player, names, 'Gates of Hell', 'All-In',
            lambda state: state.has('Beat Gates of Hell', player) and (
                    state.has('Beat Shatter the Sky', player) or state.has('Beat Belly of the Beast', player)))

    return vanilla_mission_req_table, 29, 'All-In: Victory'


def create_grid_regions(
    multiworld: MultiWorld,
    player: int,
    locations: Tuple[LocationData, ...],
    location_cache: List[Location],
) -> Tuple[Dict[str, MissionInfo], int, str]:
    
    locations_per_region = initialize_locations_per_region(locations)
    regions = [create_region(multiworld, player, locations_per_region, location_cache, "Menu")]
    mission_pools = filter_missions(multiworld, player)

    # Generating all regions and locations
    names: Dict[str, int] = {}
    num_missions = sum(len(pool) for _, pool in mission_pools.items())
    num_missions = min(num_missions, multiworld.maximum_campaign_size[player])
    remove_top_left: bool = multiworld.grid_two_start_positions[player]
    missions: Dict[Tuple[int, int], str] = {}
    final_mission = mission_pools[MissionPools.FINAL][0]

    grid_size_x, grid_size_y, num_corners_to_remove = get_grid_dimensions(num_missions + remove_top_left)
    # pick missions in order along concentric diagonals
    # each diagonal will have the same difficulty
    # this keeps long sides from possibly stealing lower-difficulty missions from future columns
    num_diagonals = grid_size_x + grid_size_y - 1
    diagonal_difficulty = MissionPools.STARTER
    missions_to_add = mission_pools[MissionPools.STARTER]
    for diagonal in range(num_diagonals):
        if diagonal == num_diagonals - 1:
            diagonal_difficulty = MissionPools.FINAL
            grid_coords = (grid_size_x-1, grid_size_y-1)
            missions[grid_coords] = mission_pools[MissionPools.FINAL][0]
            break
        if diagonal == 0 and remove_top_left:
            continue
        diagonal_length = min(diagonal + 1, num_diagonals - diagonal, grid_size_x, grid_size_y)
        if len(missions_to_add) < diagonal_length:
            raise Exception(f"There are not enough {mission_pool_names[diagonal_difficulty]} missions to fill the campaign.  Please exclude fewer missions.")
        for i in range(diagonal_length):
            # (0,0) + (0,1)*diagonal + (1,-1)*i + (1,-1)*max(diagonal - grid_size_y + 1, 0)
            grid_coords = (i + max(diagonal - grid_size_y + 1, 0), diagonal - i - max(diagonal - grid_size_y + 1, 0))
            if grid_coords == (grid_size_x - 1, 0) and num_corners_to_remove >= 2:
                missions[grid_coords] = ''
            elif grid_coords == (0, grid_size_y - 1) and num_corners_to_remove >= 1:
                missions[grid_coords] = ''
            else:
                mission_index = multiworld.random.randint(0, len(missions_to_add) - 1)
                missions[grid_coords] = missions_to_add.pop(mission_index)

        if diagonal_difficulty < MissionPools.HARD:
            diagonal_difficulty += 1
            missions_to_add.extend(mission_pools[diagonal_difficulty])

    # Generating regions and locations from selected missions
    mission_coords_to_id: Dict[Tuple[int, int], int] = {}
    for x in range(grid_size_x):
        for y in range(grid_size_y):
            if (missions.get((x, y))):
                mission_coords_to_id[(x, y)] = len(regions)
                regions.append(create_region(multiworld, player, locations_per_region, location_cache, missions[(x, y)]))
    multiworld.regions += regions

    mission_req_table: Dict[str, MissionInfo] = {}
    for coords, mission in missions.items():
        ui_flags: MissionInfoUiFlags = MissionInfoUiFlags(0)
        if not mission:
            continue
        connections: List[str] = []
        if coords == (0, 0) or (remove_top_left and sum(coords) == 1):
            # Connect to the "Menu" starting region
            connect(multiworld, player, names, "Menu", mission)
        else:
            for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                connected_coords = (coords[0] + dx, coords[1] + dy)
                if connected_coords in mission_coords_to_id:
                    connections.append(missions[connected_coords])
                    connect(multiworld, player, names, missions[connected_coords], mission,
                        make_grid_connect_rule(missions, connected_coords, player),
                    )
        if coords[1] == 1 and not missions.get((coords[0], 0)):
            ui_flags |= MissionInfoUiFlags.PrependSpacer
        mission_req_table[mission] = MissionInfo(
            vanilla_mission_req_table[mission].id,
            connections,
            category=f'_{coords[0] + 1}',
            or_requirements=True,
            ui_flags=ui_flags.value,
        )

    final_mission_id = vanilla_mission_req_table[final_mission].id
    final_location = set_up_final_location(final_mission, location_cache)

    return mission_req_table, final_mission_id, final_location


def make_grid_connect_rule(
    mission_names: Dict[Tuple[int, int], str],
    connected_coords: Tuple[int, int],
    player: int
) -> Callable[[CollectionState], bool]:
    return lambda state: state.has(f"Beat {mission_names[connected_coords]}", player)


def create_structured_regions(
    multiworld: MultiWorld,
    player: int,
    locations: Tuple[LocationData, ...],
    location_cache: List[Location],
    mission_order_type: int,
) -> Tuple[Dict[str, MissionInfo], int, str]:
    locations_per_region = initialize_locations_per_region(locations)
    regions = [create_region(multiworld, player, locations_per_region, location_cache, "Menu")]
    mission_pools = filter_missions(multiworld, player)

    names: Dict[str, int] = {}
    mission_order = mission_orders[mission_order_type]
    missions: List[Union[str, int, None]] = []

    remove_prophecy = (
        mission_order_type == MissionOrder.option_vanilla_shuffled
        and not get_option_value(multiworld, player, "shuffle_protoss")
    )

    final_mission = mission_pools[MissionPools.FINAL][0]

    # Determining if missions must be removed
    mission_pool_size = sum(len(mission_pool) for mission_pool in mission_pools.values())
    removals = len(mission_order) - mission_pool_size
    # Removing entire Prophecy chain on vanilla shuffled when not shuffling protoss
    if remove_prophecy:
        removals -= PROPHECY_CHAIN_MISSION_COUNT

    # Initial fill out of mission list and marking all-in mission
    for mission in mission_order:
        # Removing extra missions if mission pool is too small
        # Also handle lower removal priority than Prophecy
        if 0 < mission.removal_priority <= removals or mission.category == 'Prophecy' and remove_prophecy \
                or (remove_prophecy and mission_order_type == MissionOrder.option_vanilla_shuffled
                    and mission.removal_priority > vanilla_shuffle_order[VANILLA_SHUFFLED_FIRST_PROPHECY_MISSION].removal_priority
                    and 0 < mission.removal_priority <= removals + PROPHECY_CHAIN_MISSION_COUNT):
            missions.append(None)
        elif mission.type == MissionPools.FINAL:
            missions.append(final_mission)
        else:
            missions.append(mission.type)

    no_build_slots = []
    easy_slots = []
    medium_slots = []
    hard_slots = []

    # Search through missions to find slots needed to fill
    for i in range(len(missions)):
        if missions[i] is None:
            continue
        if missions[i] == MissionPools.STARTER:
            no_build_slots.append(i)
        elif missions[i] == MissionPools.EASY:
            easy_slots.append(i)
        elif missions[i] == MissionPools.MEDIUM:
            medium_slots.append(i)
        elif missions[i] == MissionPools.HARD:
            hard_slots.append(i)

    # Add no_build missions to the pool and fill in no_build slots
    missions_to_add = mission_pools[MissionPools.STARTER]
    if len(no_build_slots) > len(missions_to_add):
        raise Exception("There are no valid No-Build missions.  Please exclude fewer missions.")
    for slot in no_build_slots:
        filler = multiworld.random.randint(0, len(missions_to_add) - 1)

        missions[slot] = missions_to_add.pop(filler)

    # Add easy missions into pool and fill in easy slots
    missions_to_add = missions_to_add + mission_pools[MissionPools.EASY]
    if len(easy_slots) > len(missions_to_add):
        raise Exception("There are not enough Easy missions to fill the campaign.  Please exclude fewer missions.")
    for slot in easy_slots:
        filler = multiworld.random.randint(0, len(missions_to_add) - 1)

        missions[slot] = missions_to_add.pop(filler)

    # Add medium missions into pool and fill in medium slots
    missions_to_add = missions_to_add + mission_pools[MissionPools.MEDIUM]
    if len(medium_slots) > len(missions_to_add):
        raise Exception("There are not enough Easy and Medium missions to fill the campaign.  Please exclude fewer missions.")
    for slot in medium_slots:
        filler = multiworld.random.randint(0, len(missions_to_add) - 1)

        missions[slot] = missions_to_add.pop(filler)

    # Add hard missions into pool and fill in hard slots
    missions_to_add = missions_to_add + mission_pools[MissionPools.HARD]
    if len(hard_slots) > len(missions_to_add):
        raise Exception("There are not enough missions to fill the campaign.  Please exclude fewer missions.")
    for slot in hard_slots:
        filler = multiworld.random.randint(0, len(missions_to_add) - 1)

        missions[slot] = missions_to_add.pop(filler)

    # Generating regions and locations from selected missions
    for region_name in missions:
        regions.append(create_region(multiworld, player, locations_per_region, location_cache, region_name))
    multiworld.regions += regions

    # Mapping original mission slots to shifted mission slots when missions are removed
    slot_map: List[int] = []
    slot_offset = 0
    for position, mission in enumerate(missions):
        slot_map.append(position - slot_offset + 1)
        if mission is None:
            slot_offset += 1

    # Loop through missions to create requirements table and connect regions
    # TODO: Handle 'and' connections
    mission_req_table: Dict[str, MissionInfo] = {}

    def build_connection_rule(mission_names: List[str], missions_req: int) -> Callable:
        if len(mission_names) > 1:
            return lambda state: state.has_all({f"Beat {name}" for name in mission_names}, player) and \
                                    state._sc2wol_cleared_missions(multiworld, player, missions_req)
        else:
            return lambda state: state.has(f"Beat {mission_names[0]}", player) and \
                                    state._sc2wol_cleared_missions(multiworld, player, missions_req)

    for i, mission in enumerate(missions):
        if mission is None:
            continue
        connections: List[int] = []
        all_connections: List[str] = []
        for connection in mission_order[i].connect_to:
            if connection == -1:
                continue
            while missions[connection] is None:
                connection -= 1
            all_connections.append(missions[connection])
        for connection in mission_order[i].connect_to:
            required_mission = missions[connection]
            if connection == -1:
                connect(multiworld, player, names, "Menu", mission)
            else:
                if required_mission is None and not mission_order[i].completion_critical:  # Drop non-critical null slots
                    continue
                while required_mission is None:  # Substituting null slot with prior slot
                    connection -= 1
                    required_mission = missions[connection]
                required_missions = [required_mission] if mission_order[i].or_requirements else all_connections
                connect(multiworld, player, names, required_mission, mission,
                        build_connection_rule(required_missions, mission_order[i].number))
                connections.append(slot_map[connection])

        mission_req_table.update({mission: MissionInfo(
            vanilla_mission_req_table[mission].id, connections, mission_order[i].category,
            number=mission_order[i].number,
            completion_critical=mission_order[i].completion_critical,
            or_requirements=mission_order[i].or_requirements)})

    final_mission_id = vanilla_mission_req_table[final_mission].id
    final_location = set_up_final_location(final_mission, location_cache)

    return mission_req_table, final_mission_id, final_location


# ===== Helper methods =====


def set_up_final_location(final_mission_name: str, location_cache: List[Location]) -> str:
    """
    Changes the completion condition for alternate final missions into an event.
    Returns the name of the final location.
    """
    if final_mission_name != 'All-In':
        final_location = alt_final_mission_locations[final_mission_name]
        # Final location should be near the end of the cache
        for i in range(len(location_cache) - 1, -1, -1):
            if location_cache[i].name == final_location:
                location_cache[i].locked = True
                location_cache[i].event = True
                location_cache[i].address = None
                break
        return final_location
    else:
        return 'All-In: Victory'


def create_region(multiworld: MultiWorld, player: int, locations_per_region: Dict[str, List[LocationData]],
                  location_cache: List[Location], name: str) -> Region:
    region = Region(name, player, multiworld)

    if name in locations_per_region:
        for location_data in locations_per_region[name]:
            location = create_location(player, location_data, region, location_cache)
            region.locations.append(location)

    return region


def create_location(player: int, location_data: LocationData, region: Region,
                    location_cache: List[Location]) -> Location:
    location = Location(player, location_data.name, location_data.code, region)
    location.access_rule = location_data.rule

    if id is None:
        location.event = True
        location.locked = True

    location_cache.append(location)

    return location


def connect(world: MultiWorld, player: int, used_names: Dict[str, int], source: str, target: str,
            rule: Optional[Callable[[CollectionState], bool]] = None):
    sourceRegion = world.get_region(source, player)
    targetRegion = world.get_region(target, player)

    if target not in used_names:
        used_names[target] = 1
        name = target
    else:
        used_names[target] += 1
        name = target + (' ' * used_names[target])

    connection = Entrance(player, name, sourceRegion)

    if rule:
        connection.access_rule = rule

    sourceRegion.exits.append(connection)
    connection.connect(targetRegion)


def initialize_locations_per_region(locations: Tuple[LocationData, ...]) -> Dict[str, List[LocationData]]:
    per_region: Dict[str, List[LocationData]] = {}

    for location in locations:
        per_region.setdefault(location.region, []).append(location)

    return per_region


def get_factors(number: int) -> Tuple[int, int]:
    """
    Simple factorization into pairs of numbers (x, y) using a sieve method.
    Returns the factorization that is most square, i.e. where x + y is minimized.
    Factor order is such that x <= y.
    """
    assert number > 0
    for divisor in range(math.floor(math.sqrt(number)), 1, -1):
        quotient = number // divisor
        if quotient * divisor == number:
            return (divisor, quotient)
    return (1, number)


def get_grid_dimensions(size: int) -> Tuple[int, int, int]:
    """
    Get the dimensions of a grid mission order from the number of missions, int the format (x, y, error).
    * Error will always be 0, 1, or 2, so the missions can be removed from the corners that aren't the start or end.
    * Dimensions are chosen such that x <= y, as buttons in the UI are wider than they are tall.
    * Dimensions are chosen to be maximally square. That is, x + y + error is minimized.
    * If multiple options of the same rating are possible, the one with the larger error is chosen,
    as it will appear more square. Compare 3x11 to 5x7-2 for an example of this.
    """
    dimension_candidates = [(*get_factors(size+x), x) for x in (2, 1, 0)]
    best_dimension = min(dimension_candidates, key=sum)
    return best_dimension

