import math


# I plan on fixing the bad variable
#   names later - this is the result of my whiteboard math!

# At Q=0 is the nose, and at Q=Lp is the end of the tail.
# Q is used as the location on the plane, on the axis from front to back.

Qw = None  # wing location
Qvc = None # tail location
Qcl = None # center of lift (equals Qcg, or center of gravity)
Cw = None # wing chord
Lw = None # wing length
Aw = None # area of the wing
Af = None # fuselage cross-sectional area
Tw = None # thickness of the wing
Tt = None # thickness of the tail
Vw = None # wing volume
Dw = None # wing density (kg/m3)

Mc = None  # payload mass (kg)
Mw = None  # wing mass
Mf = None  # fuselage mass

v = None # plane velocity
cl = None # lift constant
cd = None # drag constant
theta = None # angle of flat wing

def ask_yn(question):
    return input(question+'[Y/n]')=='Y'

def get_float(question, default=None):
    if default!=None:
        question+=" (default is {})".format(default)
    while True:
        inp=input(question)
        try:
            return float(inp)
        except:
            if default==None:
                print("Not a number!  Please enter the value again.")
            elif inp=='':
                return default
def get_float_options(question, options, units=''):
    while True:
        print(question)
        for i in options.keys():
            print('{} : {} {}'.format(i, options[i], units))
        inp = input("Enter a number or an option above >")
        try:
            return float(inp)
        except:
            if inp in options.keys():
                return options[inp]
            print("Not a number!  Please enter the value again.")
def ask_density_of(obj):
    options = {
        'Balsa':160,
        'PLA':1250,
        'ABS':1100
    }
    return get_float_options('Density of {} (kg/m3)?'.format(obj), options, 'kg/m3')
def get_payload_mass():
    global Mc
    if Mc==None:
        Mc = get_float('What is your payload mass (kg)?', .01)
    return Mc
def get_plane_velocity():
    global v
    if v==None:
        v = get_float("How fast do you want the plane to go (m/s)?")
    return v
def get_angle_of_wing():
    'asks user for wing angle'
    global theta
    if theta==None:
        while True:
            degrees = get_float("What is the angle of the wing (degrees)?")
            if degrees>15 or degrees<0:
                print("Cannot use that angle: pick a value between 0 and 15 degrees.")
                continue
            else:
                break
        theta = degrees/180 * math.pi
    return theta
def get_lift_constant():
    global cl
    if cl==None:
        cl = 2 * math.pi * get_angle_of_wing()
    return cl
def get_drag_constant():
    global cd
    if cd==None:
        cd = get_float("Drag coefficient?", 0.005)
    return cd
def calc_lift_force():
    'calculates for changes due to optimization'
    # 1.2 is roughly the density of air in kg/m3
    return (get_lift_constant()*(get_plane_velocity()**2)*get_wing_area()*1.2)/2
def calc_drag_force():
    'calculates for changes due to optimization'
    # 1.2 is roughly the density of air in kg/m3
    return (get_drag_constant()*(get_plane_velocity()**2)*get_wing_area()*1.2)/2
def get_wing_density():
    global Dw
    if Dw==None:
        # in kg/m3
        Dw = ask_density_of('wing')
    return Dw
def get_tail_density():
    global Dt
    if Dt==None:
        Dt = ask_density_of('tail')
    return Dt
def get_wing_thickness():
    global Tw
    if Tw==None:
        Tw = get_float("Wing thickness (in cm)?")/100 # convert to meters
    return Tw
def get_tail_thickness():
    global Tt
    if Tt==None:
        Tt = get_float("Tail thickness (in cm)?")/100 # convert to meters
    return Tt
def get_area_fuselage():
    global Af
    if Af==None:
        Af = get_float('Cross-sectional area of fuselage (in cm2)?')/10000
    return Af
def get_wing_mass():
    global Mw
    if Mw==None:
        Mw = get_wing_volume()*get_wing_density()
    return Mw
def get_wing_chord():
    if Cw==None:
        raise Exception("Requested wing chord before value was calculated.")
    return Cw
def get_wingspan():
    if Lw==None:
        raise Exception("Requested wing length before value was calculated.")
    return Lw
def get_wing_area():
    'returns area of BOTH wings together'
    global Aw
    if Aw==None:
        # we assume that the wing has a parabolic shape for now
        # 2*2/3*wing length*wing chord
        Aw = get_wingspan()*get_wing_chord()*2/3
    return Aw
def get_center_of_lift():
    global Qcl
    if Qcl==None:
        # value here should be from the center of mass, NOT the actual lift center.
        # this is because the computer has to calculate the position of the wing,
        # and that calculation affects the center of lift - that calculation
        # is based on the center of gravity.
        Qcl = 0
    return Qcl
def get_wing_location():
    global Qw
    if Qw==None:
        # Qw = Qcl + Cw/4   | center of lift is 1/4 the way into the wing
        # Qcg = Qcl         | center of gravity is at the center of lift
        Qw = get_center_of_lift() + get_wing_chord()
    
    return Qw

"""
steps:
1. determine tail shape
2. optimize wing size (if not given)
3. calculate position of all parts of the plane
"""

if __name__=='__main__':
    has_wing_size = ask_yn('Do you have the wing size?')
    if has_wing_size:
        Lw = get_float("Wingspan? (meters)")
        Cw = get_float("Chord of wing? (meters)")

        # optimize shape of tail with known wing shape
        # the distance from the center of gravity to the center of the tail (Qtwd) is best at roughly:
        #
        #   Qtwd = sqrt(.4AwCwTt/(Af*2))
        #
        # I did that with some calculus, it optimizes for low weight.
        #
        # Multiplies fuselage size by two to account for the increase in length in both directions away from the wing

        Qtwd = math.sqrt(.4*get_wing_area()*get_wing_chord()*get_tail_thickness()/(2*get_area_fuselage()))

    else:
        # TODO: find best Qtwd with desired payload capacity instead
        Qtwd = -1
    # Now calculate the rest of the shape of the tail

    Aht = .41*get_wing_area()*get_wing_chord()/Qtwd
    Avt = .25*get_wing_area()*get_wingspan()/Qtwd

    if not has_wing_size:
        # TODO: optimize wing size here
        raise Exception("ModeNotSupported! (yet)")

    
