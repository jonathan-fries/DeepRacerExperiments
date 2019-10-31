prev_track_direction = None
last_first_waypoint = None
on_straight_away = None
progress75 = False
progress100 = False

def reward_function(params):

    import math
    global prev_track_direction
    global last_first_waypoint
    global on_straight_away
    global progress75
    global progress100

    reward = 0

    # Read input parameters
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    speed = params['speed']
    heading = params['heading']
    progress = params['progress']
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']

    if progress < 5:
        progress75 = False
        progress100 = False

    # Calculate 3 markers that are at varying distances away from the center line
    marker_3 = 0.5 * track_width

    if closest_waypoints[1]+2 < len(waypoints):
        waypoint1 = waypoints[closest_waypoints[0]+2]
        waypoint2 = waypoints[closest_waypoints[1]+2]
    else:
        waypoint1 = waypoints[closest_waypoints[0]]
        waypoint2 = waypoints[closest_waypoints[1]]

    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
    track_direction = math.atan2(waypoint2[1] - waypoint1[1], waypoint2[0] - waypoint1[0])
    # Convert to degree
    track_direction = math.degrees(track_direction)


    if distance_from_center <= marker_3:
        print("Mostly on track, things are OK.")
        DIRECTION_THRESHOLD = 15.0

        if progress > 75.0 and not progress75:
            reward += 25
            progress75 = True

        if progress >= 100 and not progress100:
            reward += 250
            progress100 = True

        if prev_track_direction is not None:

            direction_change = abs(track_direction - prev_track_direction)
            print("Prev_track_direction {0}".format(prev_track_direction))
            print("track_direction: {0}".format(track_direction))
            print("speed: {0}".format(speed))

            if last_first_waypoint is not None:
                if waypoint1 != last_first_waypoint:
                    print("New way point, determine if we are in corner or straight away.")
                    if direction_change > 10:
                        on_straight_away = False
                        print("We are coming to/on a corner.")
                    else:
                        on_straight_away = True
                        print("We are coming to/on straight away.")

                if on_straight_away is not None:
                    print("We can now tell if we are on a straight away or not.")
                    if not on_straight_away:
                        if speed <= 2:
                            print("Slow cornering rewarded.")
                            reward += 3.0
                        else:
                            print("Fast cornering, no reward.")
                    else:
                        if speed > 2:
                            print("Fast straight away rewarded.")
                            reward +=3.0
                        else:
                            print("Slow straight, no reward.")



    else:
        print("We are off track, things are bad.")
        reward -= 1

    prev_track_direction = track_direction
    last_first_waypoint = waypoint1

    return float(reward) 
