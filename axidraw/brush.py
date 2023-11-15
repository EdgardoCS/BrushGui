import math
import random
import sys
import time
from array import array

import serial

# import axi

Debug_Mode = False


def distance(x, y):
    """
    distance where moving part will move
    :param x: target destination in x axis
    :param y: target destination in y axis
    :return (x^2 + y^2)
    """
    # Pythagorean theorem
    return math.sqrt(x * x + y * y)


def circle_perimeter(radius):
    """
    calculates the perimeter of the circumference, given the radius
    :param radius: radius of target circumference, in cm
    :return: circumference perimeter (2π * r)
    """
    # circumference perimeter
    return math.pi * 2 * radius


def print_info(*s):
    if Debug_Mode:
        print(*s)


def findPort():
    """
    Find a single EiBotBoard connected to a USB port.
    :return: port
    """
    try:
        from serial.tools.list_ports import comports
    except ImportError:
        return None
    if comports:
        com_ports_list = list(comports())
        ebb_port = None
        for port in com_ports_list:
            if port[1].startswith("EiBotBoard"):
                ebb_port = port[0]  # Success; EBB found by name match.
                break  # stop searching-- we are done.
        if ebb_port is None:
            for port in com_ports_list:
                if port[2].startswith("USB VID:PID=04D8:FD92"):
                    ebb_port = port[0]  # Success; EBB found by VID/PID match.
                    break  # stop searching-- we are done.
        return ebb_port


def openPort(com_port):
    """
    Open a given serial port, verify that it is an EiBotBoard,
    and return a SerialPort object that we can reference later.

    This routine only opens the port;
    it will need to be closed as well, for example with closePort( com_port ).
    You, who open the port, are responsible for closing it as well.
    :param com_port: serial port, EiBotBoard connected
    :return: serial_port, com_status
    """
    trials = 10
    for trial in range(0, trials):
        try:
            serial_port = serial.Serial(com_port, timeout=1.0)
            serial_port.reset_input_buffer()
            serial_port.write('v\r'.encode('ascii'))
            str_version = serial_port.readline()
            serial_port.write('qc\r'.encode('ascii'))
            pwr_state = serial_port.readline()
            value = pwr_state.decode('ascii').split(',')
            if int(value[1]) <= 100:  # check input current level https://evil-mad.github.io/EggBot/ebb.html#QC
                com_status = False
                return serial_port, com_status
        except serial.SerialException as se:
            if 'Device or resource busy:' in se.__str__():
                print('Waiting for the port to be ready ...')
            else:
                print('se: {0}'.format(se))
                return None
        else:
            if str_version and str_version.startswith("EBB".encode('ascii')):
                print('FW version:', str_version.decode('ascii'))
                com_status = True
                return serial_port, com_status
            serial_port.close()
            return None
    # time.sleep(1)


def closePort(com_port):
    """
    close port after use
    :param com_port: serial port, EiBotBoard connected
    :return: None
    """
    if com_port is not None:
        try:
            serial_port = serial.Serial(com_port, timeout=1.0)
            serial_port.close()
            print('Port', com_port, 'is now closed')
        except serial.SerialException:
            pass


def query(com_port, cmd):
    """

    :param com_port: serial port, EiBotBoard connected
    :param cmd: command encoded (EBB Command Set)
    :return: response from EiBotBoard
    """
    if com_port is not None and cmd is not None:
        response = ''
        try:
            com_port.write(cmd.encode('ascii'))
            response = com_port.readline().decode('ascii')
            n_retry_count = 0
            while len(response) == 0 and n_retry_count < 100:
                # get new response to replace null response if necessary
                response = com_port.readline()
                n_retry_count += 1
            if cmd.strip().lower() not in ["v", "i", "a", "mr", "pi", "qm"]:
                # Most queries return an "OK" after the data requested.
                # We skip this for those few queries that do not return an
                # extra line.
                unused_response = com_port.readline()  # read in extra blank/OK line
                n_retry_count = 0
                while len(unused_response) == 0 and n_retry_count < 100:
                    # get new response to replace null response if necessary
                    unused_response = com_port.readline()
                    n_retry_count += 1
        except Exception as e:
            print(e)
            print("Error reading serial data.")
        return response
    else:
        return None


def command(com_port, cmd):
    """
    same as query.
    :param com_port: serial port, EiBotBoard connected
    :param cmd: command encoded (EBB Command Set)
    :return: response from EiBotBoard
    """
    if com_port is not None and cmd is not None:
        try:
            com_port.write(cmd.encode('ascii'))
            response = com_port.readline().decode('ascii')
            n_retry_count = 0
            while len(response) == 0 and n_retry_count < 100:
                # get new response to replace null response if necessary
                response = com_port.readline()
                n_retry_count += 1
            if response.strip().startswith("OK"):
                pass  # inkex.errormsg( 'OK after command: ' + cmd ) #Debug option: indicate which command.
            else:
                if response:
                    print('Error: Unexpected response from EBB.')
                    print('   Command: {0}'.format(cmd.strip()))
                    print('   Response: {0}'.format(response.strip()))
                else:
                    print('EBB Serial Timeout after command: {0}'.format(cmd))
        except Exception as e:
            print(e)
            print('Failed after command: {0}'.format(cmd))
            pass


def doLowLevelMove(port_name, ri1, steps1, delta_r1, ri2, steps2, delta_r2):
    """
    Execute low level movement from axidraw
    :param port_name: serial port
    :param ri1: Rate1. represent step rates for axis 1 and 2, and are added to each axis step
    :param steps1: Steps1. Each number gives the movement distance — the total number of steps — for the given axis
    :param delta_r1: Accel1. These values are added to their respective Rate values every 40 μs and control acceleration or deceleration during a move
    :param ri2: Rate2.
    :param steps2: Steps2.
    :param delta_r2: Accel2.
    :return: None
    """
    # A "pre-computed" XY movement of the form
    #  "LM,RateTerm1,AxisSteps1,DeltaR1,RateTerm2,AxisSteps2,DeltaR2<CR>"
    # See http://evil-mad.github.io/EggBot/ebb.html#LM for documentation.
    # Important: Requires firmware version 2.5.1 or higher.
    if port_name is not None:
        if ((ri1 == 0 and delta_r1 == 0) or steps1 == 0) and ((ri2 == 0 and delta_r2 == 0) or steps2 == 0):
            return
        str_output = 'LM,{0},{1},{2},{3},{4},{5}\r'.format(ri1, steps1, delta_r1, ri2, steps2, delta_r2)
        command(port_name, str_output)


def sendDisableMotors(port_name):
    """
    Execute command EM (Enable Motors) and signal 0, disable motors
    :param port_name: serial port
    :return: None
    """
    if port_name is not None:
        command(port_name, 'EM,0,0\r')


def sendEnableMotors(port_name, res):
    """
    Execute command EM (Enable Motors) and signal 1, enable motors
    :param port_name: serial port
    :param res: set global step mode to target resolution (2x, 4x, 8x, 16x)
    :return: None
    """
    if res < 0:
        res = 0
    if res > 5:
        res = 5
    if port_name is not None:
        command(port_name, 'EM,{0},{0}\r'.format(res))
        # If res == 0, -> Motor disabled
        # If res == 1, -> 16X microstepping
        # If res == 2, -> 8X microstepping
        # If res == 3, -> 4X microstepping
        # If res == 4, -> 2X microstepping
        # If res == 5, -> No microstepping


def doTimedPause(port_name, n_pause):
    """
    set the time for steps to execute, in miliseconds
    :param port_name: serial port
    :param n_pause: integer in the range from 1 to 16777215, giving time in milliseconds.
    :return: None
    """
    if port_name is not None:
        while n_pause > 0:
            if n_pause > 750:
                td = 750
            else:
                td = n_pause
                if td < 1:
                    td = 1  # don't allow zero-time moves
            command(port_name, 'SM,{0},0,0\r'.format(td))
            n_pause -= td


def sendPenDown(port_name, pen_delay):
    """
    Execute command SP (set pen state), signal 0, lower the pen
    :param port_name: serial port
    :param pen_delay: duration (optional) is an integer from 1 to 65535, which gives a delay in milliseconds.
    :return: None
    """
    if port_name is not None:
        str_output = 'SP,0,{0}\r'.format(pen_delay)
        command(port_name, str_output)


def sendPenUp(port_name, pen_delay):
    """
    Execute command SP (set pen state), signal 1, raise the pen
    :param port_name: serial port
    :param pen_delay: duration (optional) is an integer from 1 to 65535, which gives a delay in milliseconds.
    :return: None
    """
    if port_name is not None:
        str_output = 'SP,1,{0}\r'.format(pen_delay)
        command(port_name, str_output)


def doXYMove(port_name, delta_x, delta_y, duration):
    """
    Move X/Y axes as: "SM,<move_duration>,<axis1>,<axis2><CR>"
    Typically, this is wired up such that axis 1 is the Y axis and axis 2 is
    the X axis of motion.
    On EggBot, Axis 1 is the "pen" motor, and Axis 2 is the "egg" motor.
    :param port_name: serial port
    :param delta_x: AxisSteps1 as integers, in the range from -16777215 to 16777215, giving movement distance in steps.
    :param delta_y: AxisSteps2 as integers, in the range from -16777215 to 16777215, giving movement distance in steps.
    :param duration: duration is an integer in the range from 1 to 16777215, giving time in milliseconds.
    :return: None
    """
    if port_name is not None:
        str_output = 'SM,{0},{1},{2}\r'.format(duration, delta_y, delta_x)
        command(port_name, str_output)


def doXMMove(port_name, delta_x, delta_y, duration):
    """
    Stepper Move, for Mixed-axis Geometries
    :param port_name: serial port
    :param delta_x: AxisSteps1 as integers, in the range from -16777215 to 16777215, giving movement distance in steps.
    :param delta_y: AxisSteps2 as integers, in the range from -16777215 to 16777215, giving movement distance in steps.
    :param duration: duration is an integer in the range from 1 to 16777215, giving time in milliseconds.
    :return: None
    """
    if port_name is not None:
        str_output = 'XM,{0},{1},{2}\r'.format(duration, delta_y, delta_x)
        command(port_name, str_output)


def to_the_front(serial_port, steps, mtime):
    doXYMove(serial_port, -steps, steps, mtime)


def to_the_back(serial_port, steps, mtime):
    doXYMove(serial_port, steps, -steps, mtime)


def to_the_left(serial_port, steps, mtime):
    doXYMove(serial_port, -steps, -steps, mtime)


def to_the_right(serial_port, steps, mtime):
    doXYMove(serial_port, steps, steps, mtime)


def setup_servo(serial_port):
    print('Setting the servo...')
    command(serial_port, 'SC,4,20641\r')
    command(serial_port, 'SC,5,15248\r')
    command(serial_port, 'SC,11,2000\r')
    command(serial_port, 'SC,12,750\r')
    command(serial_port, 'SM,10,0,0\r')
    print('Done')


def pen_down(serial_port):
    command(serial_port, 'PD,B,3,0\r')  # Enable trigger
    command(serial_port, 'SC,4,20641\r')
    command(serial_port, 'SC,5,15248\r')
    command(serial_port, 'SC,11,2000\r')
    command(serial_port, 'SC,12,750\r')
    command(serial_port, 'SP,0,200\r')
    command(serial_port, 'SM,10,0,0\r')
    command(serial_port, 'PO,B,3,1\r')  # Trigger


def pen_up(serial_port):
    command(serial_port, 'PD,B,3,0\r')  # Enable trigger
    command(serial_port, 'SC,4,20641\r')
    command(serial_port, 'SC,5,15248\r')
    command(serial_port, 'SC,11,2000\r')
    command(serial_port, 'SC,12,750\r')
    command(serial_port, 'SP,1,200\r')
    command(serial_port, 'SM,10,0,0\r')
    command(serial_port, 'PO,B,3,0\r')  # Trigger


def move_x(serial_port, x_dest, speed):
    """
    Move the pen in the x direction for a given distance and speed.
    Speed and distance in centimeters.
    :param serial_port: COM PORT
    :param x_dest: target distance (in cm)
    :param speed: target speed (in cm/s)
    """
    x_dest /= 2.54
    speed /= 2.54
    y_dest, v_i, v_f = 0, 0, 0
    print_info(f'Brushing to {x_dest} with speed {speed}')

    f_curr_x, f_curr_y = 0, 0
    delta_x_inches = x_dest - f_curr_x
    delta_y_inches = y_dest - f_curr_y

    # Velocity inputs; clarify units.
    vi_inches_per_sec = v_i
    vf_inches_per_sec = v_f

    # Distance in inches that the motor+belt must turn through at Motor 1 and 2
    motor_dist1 = delta_x_inches + delta_y_inches
    motor_dist2 = delta_x_inches - delta_y_inches

    # Look at distance to move along 45-degree axes, for native motor steps: Recall that StepScaleFactor gives a
    # scaling factor for converting from inches to steps. It is *not* the native resolution StepScaleFactor is Either
    # 1016 or 2032, for 8X or 16X microstepping, respectively.

    # resolution = 1 # 16x microstepping
    resolution = 2  # 8x microstepping
    print_info('Using resolution value of', resolution)

    if resolution == 2:
        StepScaleFactor = 1016.0
    else:
        StepScaleFactor = 1016.0 * 2  # Value from variable NativeResFactor in axidraw_conf.py

    # Round the requested motion to the nearest motor step.
    motor_steps1 = int(round(StepScaleFactor * motor_dist1))
    motor_steps2 = int(round(StepScaleFactor * motor_dist2))

    # Since we are rounding, we need to keep track of the actual distance moved,
    # not just the _requested_ distance to move.

    motor_dist1_rounded = float(motor_steps1) / (2.0 * StepScaleFactor)
    motor_dist2_rounded = float(motor_steps2) / (2.0 * StepScaleFactor)

    # Convert back to find the actual X & Y distances that will be moved:
    delta_x_inches_rounded = (motor_dist1_rounded + motor_dist2_rounded)
    delta_y_inches_rounded = (motor_dist1_rounded - motor_dist2_rounded)

    # If total movement is less than one step, skip this movement.
    if abs(motor_steps1) < 1 and abs(motor_steps2) < 1:
        print('Total movement less than one step, skipping this movement')

    segment_length_inches = distance(delta_x_inches_rounded, delta_y_inches_rounded)

    # From axidraw_conf
    PenUpSpeed = 100  # Default pen-up speed (%).   Range: 1 - 110 %
    PenDownSpeed = 100  # 25 # Default pen-down speed (%). Range: 1 - 110 %
    SpeedLimXY_LR = 1  # 12.000 # Maximum XY speed allowed when in Low Resolution
    #                        # mode, in inches per second. Default: 12.000 Max:
    #                        # 17.3958

    SpeedLimXY_HR = 3  # 8.6979 # Maximum XY speed allowed when in High Resolution
    #                        # mode, in inches per second. Default: 8.6979, Max:
    #                        # 8.6979 Do not increase these values above Max;
    #                        # they are derived from MaxStepRate and the
    #                        # resolution.
    # SpeedLimXY_LR = speed
    # SpeedLimXY_HR = speed
    # Acceleration & Deceleration rates:
    AccelRate = 100  # 40.0    # Standard acceleration rate, inches per second squared
    AccelRatePU = 60.0  # Pen-up acceleration rate, inches per second squared
    accel = 100  # 50              # Acceleration rate factor (1-100)
    TimeSlice = 0.025  # Interval, in seconds, of when to update the
    # motors. Default: TimeSlice = 0.025 (25 ms)
    MaxStepRate = 24.995  # Maximum allowed motor step rate, in steps per millisecond.
    # Note that 25 kHz is the absolute maximum step rate for the EBB.
    # Movement commands faster than this are ignored; may result in a crash (loss of position control).
    # We use a conservative value, to help prevent errors due to rounding.
    # This value is normally used _for speed limit checking only_.

    speed_pendown = PenDownSpeed * SpeedLimXY_HR / 110.0  # Speed given as
    # maximum inches/second
    # in XY plane
    speed_penup = PenUpSpeed * SpeedLimXY_HR / 110.0  # Speed given as
    # maximum
    # inches/second in XY
    # plane

    # Note: The value of `accel`, in the Inkscape extension, depends on the
    # timing parameter "Acceleration"

    # <param indent="1" name="accelFactor" type="optiongroup"
    # appearance="minimal" _gui-text="Acceleration :">
    # <_option value="50">Standard</_option>
    # <_option value="100">Maximum</_option>
    # <_option value="75">High</_option>
    # <_option value="35">Slow</_option>
    # <_option value="10">Very slow</_option>
    # </param>

    pen_up = False
    if pen_up:
        speed_limit = speed_penup
    else:
        speed_limit = speed_pendown

    # Acceleration/deceleration rates:
    if pen_up:
        accel_rate = AccelRatePU * accel / 100.0
    else:
        accel_rate = AccelRate * accel / 100.0

    # Maximum acceleration time: Time needed to accelerate from full stop to
    # maximum speed: v = a * t, so t_max = vMax / a
    t_max = speed_limit / accel_rate

    # Distance that is required to reach full speed, from zero speed:  x = 1/2 a t^2
    accel_dist = 0.5 * accel_rate * t_max * t_max

    if vi_inches_per_sec > speed_limit:
        vi_inches_per_sec = speed_limit
    if vf_inches_per_sec > speed_limit:
        vf_inches_per_sec = speed_limit

    # Times to reach maximum speed, from our initial velocity
    # vMax = vi + a*t  =>  t = (vMax - vi)/a
    # vf = vMax - a*t   =>  t = -(vf - vMax)/a = (vMax - vf)/a
    # -- These are _maximum_ values. We often do not have enough time/space to reach full speed.

    t_accel_max = (speed_limit - vi_inches_per_sec) / accel_rate
    t_decel_max = (speed_limit - vf_inches_per_sec) / accel_rate
    # Distance that is required to reach full speed, from our start at speed vi_inches_per_sec:
    # distance = vi * t + (1/2) a t^2
    accel_dist_max = (vi_inches_per_sec * t_accel_max) + (0.5 * accel_rate * t_accel_max * t_accel_max)
    # Use the same model for deceleration distance; modeling it with backwards motion:
    decel_dist_max = (vf_inches_per_sec * t_decel_max) + (0.5 * accel_rate * t_decel_max * t_decel_max)

    # time slices: Slice travel into intervals that are (say) 30 ms long.
    time_slice = TimeSlice  # Default slice intervals

    # Declare arrays: These are _normally_ 4-byte integers, but could
    # (theoretically) be 2-byte integers on some systems.  if so, this could
    # cause errors in rare cases (very large/long moves, etc.).  Set up an
    # alert system, just in case!

    duration_array = array('I')  # unsigned integer for duration -- up to
    # 65 seconds for a move if only 2 bytes.
    dist_array = array('f')  # float
    dest_array1 = array('i')  # signed integer
    dest_array2 = array('i')  # signed integer

    time_elapsed = 0.0
    position = 0.0
    velocity = vi_inches_per_sec
    speed_max = speed_limit  # We will reach _full cruising speed_!

    intervals = int(math.floor(t_accel_max / time_slice))  # Number of intervals during acceleration

    # If intervals == 0, then we are already at (or nearly at) full speed.
    if intervals > 0:
        time_per_interval = t_accel_max / intervals

        velocity_step_size = (speed_max - vi_inches_per_sec) / (intervals + 1.0)
        # For six time intervals of acceleration, first interval is at velocity (max/7)
        # 6th (last) time interval is at 6*max/7
        # after this interval, we are at full speed.

        for index in range(0, intervals):  # Calculate acceleration phase
            velocity += velocity_step_size
            time_elapsed += time_per_interval
            position += velocity * time_per_interval
            duration_array.append(int(round(time_elapsed * 1000.0)))
            dist_array.append(position)  # Estimated distance along direction of travel

            # Add a center "coasting" speed interval IF there is time for it.
        coasting_distance = segment_length_inches - (accel_dist_max + decel_dist_max)

        if coasting_distance > (time_slice * speed_max):
            # There is enough time for (at least) one interval at full cruising speed.
            velocity = speed  # speed_max
            cruising_time = coasting_distance / velocity
            time_elapsed += cruising_time
            duration_array.append(int(round(time_elapsed * 1000.0)))
            position += velocity * cruising_time
            dist_array.append(position)  # Estimated distance along direction of travel

        # Number of intervals during deceleration
        intervals = int(math.floor(t_decel_max / time_slice))

        time_per_interval = t_decel_max / intervals
        velocity_step_size = (speed_max - vf_inches_per_sec) / (intervals + 1.0)

        for index in range(0, intervals):  # Calculate deceleration phase
            velocity -= velocity_step_size
            time_elapsed += time_per_interval
            position += velocity * time_per_interval
            duration_array.append(int(round(time_elapsed * 1000.0)))
            dist_array.append(position)  # Estimated distance along direction of travel
        """
        The time & distance motion arrays for this path segment are now computed.
        Next: We scale to the correct intended travel distance,
        round into integer motor steps and manage the process
        of sending the output commands to the motors.
        """
        for index in range(0, len(dist_array)):
            # Scale our trajectory to the "actual" travel distance that we need:
            # Fractional position along the intended path
            fractional_distance = dist_array[index] / position
            dest_array1.append(int(round(fractional_distance * motor_steps1)))
            dest_array2.append(int(round(fractional_distance * motor_steps2)))

        sum(dest_array1)
        prev_motor1 = 0
        prev_motor2 = 0
        prev_time = 0

        for index in range(0, len(dest_array1)):
            move_steps1 = dest_array1[index] - prev_motor1
            move_steps2 = dest_array2[index] - prev_motor2
            move_time = duration_array[index] - prev_time
            prev_time = duration_array[index]

            if move_time < 1:
                move_time = 1  # don't allow zero-time moves.

            if abs(float(move_steps1) / float(move_time)) < 0.002:
                move_steps1 = 0  # don't allow too-slow movements of this axis
            if abs(float(move_steps2) / float(move_time)) < 0.002:
                move_steps2 = 0  # don't allow too-slow movements of this axis

            # Don't allow too fast movements of either axis: Catch rounding errors
            # that could cause an overspeed event
            while ((abs(float(move_steps1) / float(move_time)) >= MaxStepRate)
                   or (abs(float(move_steps2) / float(move_time)) >= MaxStepRate)):
                move_time += 1

            prev_motor1 += move_steps1
            prev_motor2 += move_steps2

            if move_steps1 != 0 or move_steps2 != 0:  # if at least one motor step
                # is required for this move.

                motor_dist1_temp = float(move_steps1) / (StepScaleFactor * 2.0)
                motor_dist2_temp = float(move_steps2) / (StepScaleFactor * 2.0)

                # Convert back to find the actual X & Y distances that will be moved:
                # X Distance moved in this subsegment, in inchse
                x_delta = (motor_dist1_temp + motor_dist2_temp)
                # Y Distance moved in this subsegment,
                y_delta = (motor_dist1_temp - motor_dist2_temp)

                f_new_x = f_curr_x + x_delta
                f_new_y = f_curr_y + y_delta
                print_info('Command:', move_steps2, move_steps1, move_time)
                doXYMove(serial_port, move_steps2, move_steps1, move_time)
                if move_time > 50:
                    # print('sleep time', float(move_time - 10) / 1000.0)
                    time.sleep(float(move_time - 10) / 1000.0)  # pause before issuing next command

                f_curr_x = f_new_x  # Update current position
                f_curr_y = f_new_y


def doOval(serial_port, theta, speed, radius_x, radius_y):
    """

    :param serial_port:
    :param theta:
    :param speed:
    :param radius_x:
    :param radius_y:
    :return:
    """
    radius_x = 1.0  # Radius along the x-axis
    radius_y = 5.0
    # Convert theta into radians
    delta = math.radians(theta)

    # Calculate the x and y coordinates for the oval shape
    x_dest = radius_x * math.cos(delta) / speed
    y_dest = radius_y * math.sin(delta) / speed
    print('x', x_dest)
    print('y', y_dest)


def demoMov(mov):
    """

    :param mov:
    :return:
    """
    p = findPort()
    if p is None:
        print('Could not find a port with an AxiDraw connected')
        sys.exit(-1)

    print('AxiDraw found at port', p)
    serial_port = openPort(p)
    if serial_port is None:
        print('Could not open the port.')
        sys.exit(-1)

    resolution = 2
    # print('Using resolution set to', resolution)

    time.sleep(5)  # for video recording

    print('Start')
    print('-----------------')

    circularMotion = False
    linearMotion = True

    if mov == 'circular':
        circularMotion = True
        linearMotion = False

    if circularMotion:
        speed = [5, 10, 2]
        radius = [2, 4, 1]
        direction = ['CW', 'ACW']

        for i in range(0, 8):
            sendEnableMotors(serial_port, resolution)
            pen_down(serial_port)

            target_speed = random.choice(speed)
            target_radius = random.choice(radius)
            target_direction = random.choice(direction)
            rep = 1

            print('trial', i + 1)
            print('speed', target_speed)
            print('radius', target_radius)
            print('direction', target_direction)
            print('-----------------')

            move_circular(serial_port, target_speed, target_radius, rep, target_direction)

            pen_up(serial_port)
            sendDisableMotors(serial_port)

            time.sleep(2)

    elif linearMotion:
        speed = [5, 10, 15]
        direction = [5, -5, 10, -10]

        for i in range(0, 8):
            sendEnableMotors(serial_port, resolution)
            pen_down(serial_port)

            target_speed = random.choice(speed)
            target_direction = random.choice(direction)
            rep = 1

            print('trial', i + 1)
            print('speed', target_speed)
            print('direction', target_direction)
            print('-----------------')

            move_x(serial_port, target_direction, target_speed)

            pen_up(serial_port)

            time.sleep(1)
            move_x(serial_port, -target_direction, 10)

            sendDisableMotors(serial_port)

            time.sleep(2)

    closePort(p)


""" - Circular Motion - Author: Pablo V. """


def doCircle(serial_port, theta, speed, radius, direction):
    """

    :param serial_port:
    :param theta:
    :param speed:
    :param radius:
    :param direction:
    :return:
    """
    # distance /= 2.54
    speed /= 2.54

    delta = math.radians(theta)
    factor = radius * math.sin(math.radians(1))

    x_dest = factor * math.cos(delta) / 2.54
    y_dest = factor * math.sin(delta) / 2.54

    print('x', x_dest)
    print('y', y_dest)
    v_i, v_f = 0, 0

    # print_info(f'Brushing to {x_dest} with speed {speed}')

    f_curr_x, f_curr_y = 0, 0
    if direction == "ACW":
        x_dest = -x_dest
    """
    delta_x_inches = x_dest - f_curr_x
    delta_y_inches = y_dest - f_curr_y

    # Velocity inputs; clarify units.
    vi_inches_per_sec = v_i
    vf_inches_per_sec = v_f

    # Distance in inches that the motor+belt must turn through at Motor 1 and 2
    motor_dist1 = delta_x_inches + delta_y_inches
    motor_dist2 = delta_x_inches - delta_y_inches

    # resolution = 1 # 16x microstepping
    resolution = 2  # 8x microstepping
    print_info('Using resolution value of', resolution)

    if resolution == 2:
        StepScaleFactor = 1016.0
        StepScaleFactor = 1016.0
    else:
        StepScaleFactor = 1016.0 * 2  # Value from variable NativeResFactor in axidraw_conf.py

    # Round the requested motion to the nearest motor step.
    motor_steps1 = int(round(StepScaleFactor * motor_dist1))
    motor_steps2 = int(round(StepScaleFactor * motor_dist2))

    # Since we are rounding, we need to keep track of the actual distance moved,
    # not just the _requested_ distance to move.

    motor_dist1_rounded = float(motor_steps1) / (2.0 * StepScaleFactor)
    motor_dist2_rounded = float(motor_steps2) / (2.0 * StepScaleFactor)

    # Convert back to find the actual X & Y distances that will be moved:
    delta_x_inches_rounded = (motor_dist1_rounded + motor_dist2_rounded)
    delta_y_inches_rounded = (motor_dist1_rounded - motor_dist2_rounded)

    # If total movement is less than one step, skip this movement.
    if abs(motor_steps1) < 1 and abs(motor_steps2) < 1:
        print('Total movement less than one step, skipping this movement')

    segment_length_inches = distance(delta_x_inches_rounded, delta_y_inches_rounded)

    # From axidraw_conf
    PenUpSpeed = 100  # Default pen-up speed (%).   Range: 1 - 110 %
    PenDownSpeed = 100  # 25 # Default pen-down speed (%). Range: 1 - 110 %
    SpeedLimXY_LR = 1  # 12.000 # Maximum XY speed allowed when in Low Resolution
    #                        # mode, in inches per second. Default: 12.000 Max:
    #                        # 17.3958

    SpeedLimXY_HR = 3  # 8.6979 # Maximum XY speed allowed when in High Resolution
    #                        # mode, in inches per second. Default: 8.6979, Max:
    #                        # 8.6979 Do not increase these values above Max;
    #                        # they are derived from MaxStepRate and the
    #                        # resolution.
    # SpeedLimXY_LR = speed
    # SpeedLimXY_HR = speed
    # Acceleration & Deceleration rates:
    AccelRate = 100  # 40.0    # Standard acceleration rate, inches per second squared
    AccelRatePU = 60.0  # Pen-up acceleration rate, inches per second squared
    accel = 100  # 50              # Acceleration rate factor (1-100)
    TimeSlice = 0.025  # Interval, in seconds, of when to update the
    # motors. Default: TimeSlice = 0.025 (25 ms)
    MaxStepRate = 24.995  # Maximum allowed motor step rate, in steps per millisecond.

    speed_pendown = PenDownSpeed * SpeedLimXY_HR / 110.0  # Speed given as
    speed_penup = PenUpSpeed * SpeedLimXY_HR / 110.0  # Speed given as

    pen_up = False
    if pen_up:
        speed_limit = speed_penup
    else:
        speed_limit = speed_pendown

    # Acceleration/deceleration rates:
    if pen_up:
        accel_rate = AccelRatePU * accel / 100.0
    else:
        accel_rate = AccelRate * accel / 100.0

    # Maximum acceleration time: Time needed to accelerate from full stop to
    # maximum speed: v = a * t, so t_max = vMax / a
    t_max = speed_limit / accel_rate

    # Distance that is required to reach full speed, from zero speed:  x = 1/2 a t^2
    accel_dist = 0.5 * accel_rate * t_max * t_max

    if vi_inches_per_sec > speed_limit:
        vi_inches_per_sec = speed_limit
    if vf_inches_per_sec > speed_limit:
        vf_inches_per_sec = speed_limit

    # Times to reach maximum speed, from our initial velocity
    # vMax = vi + a*t  =>  t = (vMax - vi)/a
    # vf = vMax - a*t   =>  t = -(vf - vMax)/a = (vMax - vf)/a
    # -- These are _maximum_ values. We often do not have enough time/space to reach full speed.

    t_accel_max = (speed_limit - vi_inches_per_sec) / accel_rate
    t_decel_max = (speed_limit - vf_inches_per_sec) / accel_rate
    # Distance that is required to reach full speed, from our start at speed vi_inches_per_sec:
    # distance = vi * t + (1/2) a t^2
    accel_dist_max = (vi_inches_per_sec * t_accel_max) + (0.5 * accel_rate * t_accel_max * t_accel_max)
    # Use the same model for deceleration distance; modeling it with backwards motion:
    decel_dist_max = (vf_inches_per_sec * t_decel_max) + (0.5 * accel_rate * t_decel_max * t_decel_max)

    # time slices: Slice travel into intervals that are (say) 30 ms long.
    time_slice = TimeSlice  # Default slice intervals

    # Declare arrays: These are _normally_ 4-byte integers, but could
    # (theoretically) be 2-byte integers on some systems.  if so, this could
    # cause errors in rare cases (very large/long moves, etc.).  Set up an
    # alert system, just in case!

    duration_array = array('I')  # unsigned integer for duration -- up to
    # 65 seconds for a move if only 2 bytes.
    dist_array = array('f')  # float
    dest_array1 = array('i')  # signed integer
    dest_array2 = array('i')  # signed integer

    time_elapsed = 0.0
    position = 0.0
    velocity = vi_inches_per_sec
    speed_max = speed_limit  # We will reach _full cruising speed_!

    intervals = int(math.floor(t_accel_max / time_slice))  # Number of intervals during acceleration

    # If intervals == 0, then we are already at (or nearly at) full speed.
    if intervals > 0:
        time_per_interval = t_accel_max / intervals

        velocity_step_size = (speed_max - vi_inches_per_sec) / (intervals + 1.0)
        # For six time intervals of acceleration, first interval is at velocity (max/7)
        # 6th (last) time interval is at 6*max/7
        # after this interval, we are at full speed.

        for index in range(0, intervals):  # Calculate acceleration phase
            velocity += velocity_step_size
            time_elapsed += time_per_interval
            position += velocity * time_per_interval
            duration_array.append(int(round(time_elapsed * 1000.0)))
            dist_array.append(position)  # Estimated distance along direction of travel

            # Add a center "coasting" speed interval IF there is time for it.
        coasting_distance = segment_length_inches - (accel_dist_max + decel_dist_max)

        if coasting_distance > (time_slice * speed_max):
            # There is enough time for (at least) one interval at full cruising speed.
            velocity = speed  # speed_max
            cruising_time = coasting_distance / velocity
            time_elapsed += cruising_time
            duration_array.append(int(round(time_elapsed * 1000.0)))
            position += velocity * cruising_time
            dist_array.append(position)  # Estimated distance along direction of travel

        # Number of intervals during deceleration
        intervals = int(math.floor(t_decel_max / time_slice))

        time_per_interval = t_decel_max / intervals
        velocity_step_size = (speed_max - vf_inches_per_sec) / (intervals + 1.0)

        for index in range(0, intervals):  # Calculate deceleration phase
            velocity -= velocity_step_size
            time_elapsed += time_per_interval
            position += velocity * time_per_interval
            duration_array.append(int(round(time_elapsed * 1000.0)))
            dist_array.append(position)  # Estimated distance along direction of travel

        for index in range(0, len(dist_array)):
            # Scale our trajectory to the "actual" travel distance that we need:
            # Fractional position along the intended path
            fractional_distance = dist_array[index] / position
            dest_array1.append(int(round(fractional_distance * motor_steps1)))
            dest_array2.append(int(round(fractional_distance * motor_steps2)))

        sum(dest_array1)
        prev_motor1 = 0
        prev_motor2 = 0
        prev_time = 0

        for index in range(0, len(dest_array1)):
            move_steps1 = dest_array1[index] - prev_motor1
            move_steps2 = dest_array2[index] - prev_motor2
            move_time = duration_array[index] - prev_time
            prev_time = duration_array[index]

            if move_time < 1:
                move_time = 1  # don't allow zero-time moves.

            if abs(float(move_steps1) / float(move_time)) < 0.002:
                move_steps1 = 0  # don't allow too-slow movements of this axis
            if abs(float(move_steps2) / float(move_time)) < 0.002:
                move_steps2 = 0  # don't allow too-slow movements of this axis

            # Don't allow too fast movements of either axis: Catch rounding errors
            # that could cause an overspeed event
            while ((abs(float(move_steps1) / float(move_time)) >= MaxStepRate)
                   or (abs(float(move_steps2) / float(move_time)) >= MaxStepRate)):
                move_time += 1

            prev_motor1 += move_steps1
            prev_motor2 += move_steps2

            if move_steps1 != 0 or move_steps2 != 0:  # if at least one motor step
                # is required for this move.

                motor_dist1_temp = float(move_steps1) / (StepScaleFactor * 2.0)
                motor_dist2_temp = float(move_steps2) / (StepScaleFactor * 2.0)

                # Convert back to find the actual X & Y distances that will be moved:
                # X Distance moved in this subsegment, in inchse
                x_delta = (motor_dist1_temp + motor_dist2_temp)
                # Y Distance moved in this subsegment,
                y_delta = (motor_dist1_temp - motor_dist2_temp)

                f_new_x = f_curr_x + x_delta
                f_new_y = f_curr_y + y_delta

                # ------- new speed ------- #
                # TODO: adjust speed

                lapTime = round(circle_perimeter(radius) / speed)
                new_speed = circle_perimeter(radius) / lapTime
                # print("Time", lapTime/2.54)
                # print("Approx Speed (cm/s)", new_speed * 2.54)

                doXYMove(serial_port, move_steps2, move_steps1, lapTime)

                if move_time > 50:
                    # print('sleep time', float(move_time - 10) / 1000.0)
                    time.sleep(float(move_time - 10) / 1000.0)  # pause before issuing next command
                f_curr_x = f_new_x  # Update current position
                f_curr_y = f_new_y
    """


def move_circular(serial_port, speed, radius, rep, direction):
    """

    :param serial_port:
    :param speed:
    :param radius:
    :param rep:
    :param direction:
    :return:
    """
    n = 0
    while n < rep:
        k = 0
        while k < 360:
            doCircle(serial_port, k, speed, radius, direction)
            k += 1
        n += 1


if __name__ == '__main__':
    Debug_Mode = False

    demoMov('linear')

    print('We are done')
