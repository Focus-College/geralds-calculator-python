import sys
from calculators import gerald

def getFlag( flag ):
    try:
        sys.argv.index("--" + str(flag))
        return True
    except:
        return False 

def getFlagValue( flag ):
    return sys.argv[ sys.argv.index("--"+str(flag)) + 1 ]

width = float(getFlagValue("width"))
length = float(getFlagValue("length"))
inches = getFlag("inches")

house = gerald.calculateHouseRequirements( width, length, inches )

# print( sys.argv )
# print( width, length, inches )
print( house )