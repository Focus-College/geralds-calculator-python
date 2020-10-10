import math

BEAM_WIDTH = 3.5
BOARD_LENGTH = ( 8 * 12 )
WASTE_MULTIPLIER = 0.1
STUDS_OFFSET = 16

BEAMS_REQUIRED_EVERY_INCHES = (20 * 12)
FULL_BOARDS_IN_SECTION = math.floor( BEAMS_REQUIRED_EVERY_INCHES / BOARD_LENGTH )
FULL_BOARD_SECTION_SIZE = FULL_BOARDS_IN_SECTION * BOARD_LENGTH

print({
    "name": "contants",
    "BEAM_WIDTH": BEAM_WIDTH,
    "BOARD_LENGTH": BOARD_LENGTH,
    "WASTE_MULTIPLIER": WASTE_MULTIPLIER,
    "BEAMS_REQUIRED_EVERY_INCHES": BEAMS_REQUIRED_EVERY_INCHES,
    "FULL_BOARD_SECTION_SIZE": FULL_BOARD_SECTION_SIZE
})

def convertFeetToInches( feet ):
    return feet * 12

def getPlatesInLength( inches ):
    # devide the length by 96 inches (8 feet) and round up
    # multiply by two because we're doing the top and bottom in one calculation
    return math.ceil( inches / BOARD_LENGTH ) * 2

def getStudsInLength( inches ):

    # calculate the studs across
    # round up to account for the last one
    studs = math.ceil( inches / STUDS_OFFSET )

    # make sure we add an end piece if we have a perfect multiple of 16
    isNotPerfectWidth = min( inches % STUDS_OFFSET, 1 )
    perfectWidthExtension = (isNotPerfectWidth * -1) + 1
    return studs + perfectWidthExtension

def getBoardsInLength( inches ):

    plates = getPlatesInLength( inches )
    studs = getStudsInLength( inches )

    print({
        "function": "getStudsInLength",
        "inches": inches,
        "plates": plates,
        "studs": studs
    })

    return plates + studs

def getRequiredBeamsInLength( inches ):

    # for every 20 feet, we need one beam
    # we know our wall is at least 20 feet, so calculate the required beams for the REST of the wall
    # if our wall is under 20 feet, this will return zero
    wallLengthOverMinRequired = getWallLengthOverMinimumRequiredBeforeBeam( inches )
    wallLengthPlusBeam = BEAMS_REQUIRED_EVERY_INCHES + BEAM_WIDTH
    requiredBeams = math.ceil( wallLengthOverMinRequired / wallLengthPlusBeam )

    return requiredBeams

def getWallLengthOverMinimumRequiredBeforeBeam( inches ):
    return max(inches - BEAMS_REQUIRED_EVERY_INCHES, 0)

# any number of inches past BEAMS_REQUIRED_EVERY_INCHES will return 1
# any number of inches below or equal to BEAMS_REQUIRED_EVERY_INCHES return 0
def isBeamRequired( inches ):
    
    # negative numbers are zero
    wallLengthOverMinRequired = max(inches - BEAMS_REQUIRED_EVERY_INCHES, 0)

    # remove decimals
    wholeNumber = math.ceil( wallLengthOverMinRequired )

    # returns 1 (at least one beam required ) or 0 (no beams required)
    isBeamRequired = min( wholeNumber, 1 )

    print({
        "function": "isBeamRequired",
        "inches": inches,
        "wallLengthOverMinRequired": wallLengthOverMinRequired,
        "wholeNumber": wholeNumber,
        "isBeamRequired": isBeamRequired
    })
    
    return isBeamRequired

def getFullSections( inches, beams ):

    # how many inches will we remove from a section between beams to get to the last full board
    inchesReducedPerSection = BEAMS_REQUIRED_EVERY_INCHES - FULL_BOARD_SECTION_SIZE

    # how big is the last section if all beams are at BEAMS_REQUIRED_EVERY_INCHES
    lastSectionSize = inches - ( beams * ( BEAMS_REQUIRED_EVERY_INCHES + BEAM_WIDTH ))

    # how many inches of boards can we add to the last section before it will add an additional beam to the structure
    remainingBeforeNewBeam = BEAMS_REQUIRED_EVERY_INCHES - lastSectionSize

    # how many complete portions of the inchesReducedPerSection can we move to the last section
    fullSections = math.floor( remainingBeforeNewBeam / inchesReducedPerSection )

    # even if we can FIT fullSections moved into the last portion, we might not HAVE them in our length
    fullSections = min( fullSections, beams )

    # safeguard inches not requiring a beam and return value
    fullSections = fullSections * isBeamRequired( inches )

    print({
        "function": "getFullSections",
        "inches": inches,
        "beams": beams,
        "inchesReducedPerSection": inchesReducedPerSection,
        "lastSectionSize": lastSectionSize,
        "remainingBeforeNewBeam": remainingBeforeNewBeam,
        "fullSections": fullSections
    })
    
    return fullSections

def getLastSectionSize( inches, beams ):

    fullSections = getFullSections( inches, beams )
    lastSectionSize = inches - ( beams * BEAM_WIDTH ) - ( fullSections * FULL_BOARD_SECTION_SIZE )

    print({
        "function": "getLastSectionSize",
        "inches":inches,
        "beams":beams,
        "fullSections":fullSections,
        "lastSectionSize":lastSectionSize
    })

    return lastSectionSize

def buildWall( inches ):

    # get required beams
    requiredBeams = getRequiredBeamsInLength( inches )
    fullSections = getFullSections( inches, requiredBeams )
    lastSectionSize =  getLastSectionSize( inches, requiredBeams )
    studs = getBoardsInLength( FULL_BOARD_SECTION_SIZE ) * fullSections + getBoardsInLength( lastSectionSize )

    wall = {
        "function": "buildWall",
        "inches": inches,
        "studs": studs,
        "beams": requiredBeams
    }

    print( wall )

    return wall

def accountForWaste( items ):

    waste = math.ceil( items * WASTE_MULTIPLIER )

    print({
        "function": "accountForWaste",
        "items": items,
        "waste": waste
    })
    
    return waste + items

def calculateHouseRequirements( outerWidthOfHouse, outerLengthOfHouse, isInches ):

    if isInches == False:
        # convert feet to inches
        outerWidthOfHouse = convertFeetToInches( outerWidthOfHouse )
        outerLengthOfHouse = convertFeetToInches( outerLengthOfHouse )
    
    # calculate the space inbetween corner beams
    innerWidthOfHouse = outerWidthOfHouse - ( BEAM_WIDTH * 2 )
    innerLengthOfHouse = outerLengthOfHouse - ( BEAM_WIDTH * 2 )

    wall1 = buildWall( innerWidthOfHouse )
    wall2 = buildWall( innerLengthOfHouse )

    studs = accountForWaste(( wall1['studs'] + wall2['studs'] ) * 2)
    beams = accountForWaste((( wall1['beams'] + wall2['beams'] ) * 2) + 4)

    return {
        "function": "calculateHouseRequirements",
        "width": {
            "outerWidthOfHouse": outerWidthOfHouse,
            "innerWidthOfHouse": innerWidthOfHouse
        },
        "length": {
            "outerLengthOfHouse": outerLengthOfHouse,
            "innerLengthOfHouse": innerLengthOfHouse
        },
        "studs": studs,
        "beams": beams
    }