import hlt
import logging

game = hlt.Game("ECBot-3")

logging.info("Starting ECBot-1")

turno = 0

while True:

    turno += 1

    command_queue = []

    game_map = game.update_map()

    my_ships = game_map.get_me().all_ships()

    logging.info(len(my_ships))

    for ship in my_ships:
        
        if len(my_ships) > 25:
            if ship.id % 2 == turno % 2:
                continue

        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            # Skip this ship
            continue

        entities_by_distance = game_map.nearby_entities_by_distance(ship)

        distances_list = sorted([key for key in entities_by_distance])

        planets_by_distance = []
        not_owned_planets_by_distance = []
        enemy_ships_by_distance = []

        for distance in distances_list:
            for entity in entities_by_distance[distance]:

                if isinstance(entity, hlt.entity.Planet):
                    planets_by_distance.append(entity)

                elif isinstance(entity, hlt.entity.Ship) and entity not in my_ships:
                    enemy_ships_by_distance.append(entity)

        not_owned_planets_by_distance = [planet for planet in planets_by_distance if not planet.is_owned()]

        for planet in planets_by_distance:

            if ship.can_dock(planet) and not planet.is_full():
                command_queue.append(ship.dock(planet))
                break

            if len(not_owned_planets_by_distance) > 0:
                navigate_command = ship.navigate(
                    ship.closest_point_to(not_owned_planets_by_distance[0]),
                    game_map,
                    speed=int(hlt.constants.MAX_SPEED),
                    ignore_ships=False)

                if navigate_command:
                    command_queue.append(navigate_command)

                break

            elif len(enemy_ships_by_distance) > 0:
                navigate_command = ship.navigate(
                    ship.closest_point_to(enemy_ships_by_distance[0]),
                    game_map,
                    speed=int(hlt.constants.MAX_SPEED),
                    ignore_ships=False)

                if navigate_command:
                    command_queue.append(navigate_command)

                break

            break


    game.send_command_queue(command_queue)
    #Fin del turno

#Fin del juego
