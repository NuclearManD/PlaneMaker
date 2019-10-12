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
Lf = None # fuselage length

Cv = None # Vertical tail volume coefficient
Ch = None # Horizontal tail volume coefficient

Aw = None # area of the wing
Af = None # fuselage cross-sectional area
Aht = None # horizontal tail, area of a single side
Avt = None # vertical tail area

Tw = None # thickness of the wing
Tt = None # thickness of the tail

Vw = None # wing volume
Vt = None # tail volume
Vf = None # fuselage volume

Dw = None # wing density (kg/m3)
Dt = None # density of the tail
Df = None # density of the fuselage

Mc = None  # payload mass (kg)
Mw = None  # wing mass
Mf = None  # fuselage mass
Mt = None  # tail mass

v = None # plane velocity
cl = None # lift constant
cd = None # drag constant
theta = None # angle of flat wing

wing_shape_coef = None

# QUESTIONS

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
        print('\n'+question)
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
# COEFS

def get_tail_v_coef():
    global Cv
    if Cv==None:
        options = {
            'Glider':.02,
            '1 Engine':.04,
            '2 Engine':.07,
            'Fighter Jet':.07,
            'Jet':.09
            }
        Cv = get_float_options('Vertical Tail Volume Coef?', options)
    return Cv

def get_tail_h_coef():
    global Ch
    if Ch==None:
        options = {
            'Glider':.50,
            '1 Engine':.70,
            '2 Engine':.80,
            'Fighter Jet':.40,
            'Jet':1
            }
        Ch = get_float_options('Horizontal Tail Volume Coef?', options)
    return Ch
# FORCES

def calc_lift_force(surface_area = None):
    'calculates for changes due to optimization'
    if surface_area==None:
        surface_area = get_wing_area()
    
    # 1.2 is roughly the density of air in kg/m3
    return (get_lift_constant()*(get_plane_velocity()**2)*surface_area*1.2)/2
def calc_drag_force():
    'calculates for changes due to optimization'
    # 1.2 is roughly the density of air in kg/m3
    return (get_drag_constant()*(get_plane_velocity()**2)*get_wing_area()*1.2)/2
def calc_gravity_force():
    return get_plane_mass()*9.81

# DENSITIES

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
def get_fuselage_density():
    global Df
    if Df==None:
        Df = ask_density_of('fuselage')
    return Df

# THICKNESSES

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

# AREAS

def get_fuselage_area():
    global Af
    if Af==None:
        Af = get_float('Cross-sectional area of fuselage (in cm2)?')/10000
    return Af
def get_wing_area():
    'returns area of BOTH wings together'
    global Aw
    if Aw==None:
        # we assume that the wing has a parabolic shape for now
        # 2/3*wingspan*wing chord
        Aw = get_wingspan()*get_wing_chord()*get_wing_shape_coef()
    return Aw
def get_tail_area_v():
    if Avt==None:
        raise Exception("Requested tail vertical area before value was calculated.")
    return Avt
def get_tail_area_h():
    if Aht==None:
        raise Exception("Requested tail vertical area before value was calculated.")
    return Aht

# VOLUMES

def get_wing_volume():
    global Vw
    if Vw==None:
        Vw = get_wing_thickness()*get_wing_area()
    return Vw
def get_tail_volume():
    global Vt
    if Vt==None:
        Vt = get_tail_thickness()*(get_tail_area_v()+get_tail_area_h()*2)
    return Vt
def get_fuselage_volume():
    global Vf
    if Vf==None:
        if Lf==None:
            raise Exception("Fuselage length not yet calculated!")
        Vf = Lf*get_fuselage_area()
    return Vf


# MASSES

def get_wing_mass():
    global Mw
    if Mw==None:
        Mw = get_wing_volume()*get_wing_density()
    return Mw
def get_tail_mass():
    global Mt
    if Mt==None:
        Mt = get_tail_volume()*get_tail_density()
    return Mt
def get_fuselage_mass():
    global Mf
    if Mf==None:
        Mf = get_fuselage_volume()*get_fuselage_density()
    return Mf
def get_payload_mass():
    global Mc
    if Mc==None:
        Mc = get_float('What is your payload mass (kg)?', .01)
    return Mc
def get_plane_mass():
    return get_payload_mass()+get_tail_mass()+get_wing_mass()+get_fuselage_mass()

# OTHER
    
def get_wing_chord():
    if Cw==None:
        raise Exception("Requested wing chord before value was calculated.")
    return Cw
def get_wingspan():
    if Lw==None:
        raise Exception("Requested wing length before value was calculated.")
    return Lw
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
        cl = get_float("Lift coef? ")#2 * math.pi * get_angle_of_wing()
    return cl
def get_drag_constant():
    global cd
    if cd==None:
        cd = get_float("Drag coefficient?", 0.005)
    return cd
def get_wing_shape_coef():
    global wing_shape_coef
    if wing_shape_coef==None:
        options = {
            'Rectangle': 1,
            'Parabolic':.667,
            'Triangle' :.5
            }
        wing_shape_coef = get_float_options('Wing Area Coef?', options)
    return wing_shape_coef

def print_results():
    print("\n\nResults:")
    
    if Qw>1:
        # use meters
        print("Payload is at zero meters.")
        print("Wing location: {} m".format(Qw))
        print("Tail location: {} m".format(Qvc))
        print("Vertical stabilizer area: {} m2".format(get_tail_area_v()))
        print("Horizontal stabilizer area: {} m2".format(2*get_tail_area_h()))
    else:
        # use centimeters
        print("Payload is at zero cm.")
        print("Wing location: {} cm".format(Qw*100))
        print("Tail location: {} cm".format(Qvc*100))
        print("Vertical stabilizer area: {} cm2".format(get_tail_area_v()*10000))
        print("Horizontal stabilizer area: {} cm2".format(2*get_tail_area_h()*10000))
    print()
    print("Total plane mass: {} kg".format(get_plane_mass()))
    print("Lift force: {} kg*m/s3".format(calc_lift_force()))
    print("Drag force: {} kg*m/s3".format(calc_drag_force()))
    print("Grav force: {} kg*m/s3".format(calc_gravity_force()))
    if calc_gravity_force()>calc_lift_force():
        print("WARNING:  This plane will NOT fly at angle of attack<=0 degrees.  Caution!")



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

        Qtwd = math.sqrt(.4*get_wing_area()*get_wing_chord()*get_tail_thickness()/(2*get_fuselage_area()))

    else:
        # TODO: find best Qtwd with desired payload capacity instead
        Qtwd = -1
    # Now calculate the rest of the shape of the tail

    Aht = get_tail_h_coef()*get_wing_area()*get_wing_chord()/Qtwd
    Avt = get_tail_v_coef()*get_wing_area()*get_wingspan()/Qtwd

    if not has_wing_size:
        # TODO: optimize wing size here
        raise Exception("ModeNotSupported! (yet)")

    # Now make the center of gravity match the center of lift
    
    cw4 = get_wing_chord()/4 # cw4 is Cw/4

    # this calculation is very, very large.  So I'm breaking into 3 lines of code.
    numerator = ((get_wing_mass()*cw4)+((cw4+Qtwd)*get_tail_mass())+get_payload_mass()*cw4)
    denominator = (get_payload_mass() - (cw4+Qtwd)*get_fuselage_area()*get_fuselage_density()/2)
    Qw = numerator/denominator

    Qcl = Qw - cw4
    Qvc = Qw+Qtwd
    Lf = Qvc+math.sqrt(get_tail_area_h())/3

    # make sure we have all data we need loaded for the final results
    calc_lift_force()
    calc_drag_force()
    calc_gravity_force()
    get_plane_mass()
    
    print_results()
