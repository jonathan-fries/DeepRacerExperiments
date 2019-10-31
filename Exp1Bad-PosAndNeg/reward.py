prev_track_direction = None
last_first_waypoint = None
on_straight_away = None

def reward_function(params):

    import math
    global prev_track_direction
    global last_first_waypoint
    global on_straight_away

    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    speed = params['speed']
    heading = params['heading']
    all_wheels_on_track = params['all_wheels_on_track']


    # Calculate 3 markers that are at varying distances away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width

    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_1:
        reward = 3.0
    elif distance_from_center <= marker_2:
        reward = 1.5
    elif distance_from_center <= marker_3:
        reward = 0.5
    else:
        reward = 1e3  # likely crashed/ close to off track

    waypoint1 = waypoints[closest_waypoints[0]]
    waypoint2 = waypoints[closest_waypoints[1]]

    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
    track_direction = math.atan2(waypoint2[1] - waypoint1[1], waypoint2[0] - waypoint1[0])
    # Convert to degree
    track_direction = math.degrees(track_direction)

    # Calculate the difference between the track direction and the heading direction of the car
    direction_diff = abs(track_direction - heading)

    if all_wheels_on_track:
        print("All wheels on track, things are looking good.")
        DIRECTION_THRESHOLD = 15.0

        if prev_track_direction is not None:

            direction_change = abs(track_direction - prev_track_direction)
            print("Prev_track_direction {0}".format(prev_track_direction))
            print("track_direction: {0}".format(track_direction))
            print("direction_change: {0}".format(direction_change))
            print("speed: {0}".format(speed))

            if last_first_waypoint is not None:
                if waypoint1 != last_first_waypoint:
                    print("New way point, determine if we are in corner or straight away.")
                    if direction_change > 10:
                        on_straight_away = False
                        print("We are in a corner.")
                    else:
                        on_straight_away = True
                        print("We are on straight away.")

                if on_straight_away is not None:
                    print("We can now tell if we are on a straight away or not.")
                    if not on_straight_away:
                        if speed <= 2:
                            print("Slow cornering rewarded.")
                            reward += 3.0
                        else:
                            print("Fast cornering penalized.")
                            reward -= 2.0
                    else:
                        if speed > 2:
                            print("Fast straight away rewarded.")
                            reward +=3.0
                        else:
                            print("Slow straight away penalized.")
                            reward -=2.0


        print("Heading: {0}".format(heading))
        print("track_direction: {0}".format(track_direction))
        print("direction_diff: {0}".format(direction_diff))

        if direction_diff > DIRECTION_THRESHOLD:
            reward -= 2.0
            print("Direction difference penalized.")
        elif direction_diff < 5.0:
            reward += 3.0
            print("Direction convergence rewarded.")

    else:
        print("We are off track, things are bad.")
        reward -= 6.0

    prev_track_direction = track_direction
    last_first_waypoint = waypoint1

    return float(reward)
 
