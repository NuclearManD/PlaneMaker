# I plan on fixing the bad variable
#   names later - this is the result of my whiteboard math!

# At Q=0 is the nose, and at Q=Lp is the end of the tail.
# Q is used as the location on the plane, on the axis from front to back.

Qw = None  # wing location
Qvc = None # tail location
Cw = None # wing chord
Lw = None # wing length
Qcl = None # center of lift (equals Qcg, or center of gravity)
Aw = None # area of the wing
Tw = None # thickness of the wing
Vw = None # wing volume
Dw = None # wing density (kg/m3)

Mc = None  # payload mass (kg)
Mw = None  # wing mass
Mt = None  # tail mass
Mf = None  # fuselage mass
Mp = None  # plane mass

def get_float(question):
    while True:
        try:
            return float(input(question))
        except:
            print("Not a number!  Please enter the value again.")
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
def get_wing_volume():
    global Vw
    if Vw==None:
        Vw = get_wing_area()*get_wing_thickness()
    return Vw
def get_wing_density():
    global Dw
    if Dw==None:
        # in kg/m3
        options = {
            'Balsa':160,
            'PLA':1250,
            'ABS':1100
            }
        Dw = get_float_options('Density of wing (kg/m3)?', options, 'kg/m3')
    return Dw
def get_wing_thickness():
    global Tw
    if Tw==None:
        Tw = get_float("Wing thickness (in cm)?")/100 # convert to meters
    return Tw
def get_wing_mass():
    global Mw
    if Mw==None:
        Mw = get_wing_volume()*get_wing_density()
    return Mw
def get_wing_chord():
    if Cw==None:
        Cw = 0
    return Cw
def get_wing_area():
    'returns area of BOTH wings together'
    global Aw
    if Aw==None:
        # we assume that the wing has a parabolic shape for now
        # 2*2/3*wing length*wing chord
        Aw = get_wing_length()*get_wing_chord()*4/3
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
