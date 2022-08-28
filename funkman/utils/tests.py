"""
Test cases.
"""

from random              import randint
from ..funkplot.funkplot import FunkPlot
from ..utils.utils       import ReadTrapsheet

def getResultStrafe():

    Nfired=randint(1, 500)
    Nhit=randint(0, Nfired)

    # Result.
    resultStrave = {
        "dataType": "Strafe Result",
        "player": "funkyfranky",
        "name": "My Target",
        "clock": "9:45:01",
        "midate": "2022-04-01",
        "roundsFired": Nfired,
        "roundsHit": Nhit,
        "roundsQuality": "Some Quality",
        "strafeAccuracy": Nhit/Nfired*100,
        "rangename": "My Range",
        "airframe": "F/A-18C_hornet",
        "invalid": "false",
        "theatre": "Caucasus",
    }

    return resultStrave

def getResultBomb():

    # Result.
    result={
        "dataType": "Bomb Result",
        "name": "Target Name",
        "distance": randint(5,300),
        "radial": randint(1,360),
        "weapon": "Mk 82",
        "quality": "Ineffective",
        "player": "funkyfranky",
        "clock": "8:02",
        "airframe": "F/A-18C_hornet",
        "rangename": "My Range Name",
        "attackHdg": randint(1,360),
        "attackVel": randint(250, 400),
        "attackAlt": randint(6000, 12000),
        "theatre": "Caucasus",
    } 

    return result

def getResultTrap(trapfile: str):
    
    # Read trapsheet from disk for testing.
    trapsheet=ReadTrapsheet(trapfile)

    # Result.
    result={
        "dataType": "Trap Sheet",
        "name": "funkyfranky",
        "trapsheet": trapsheet,
        "airframe": 'FA-18C_hornet',
        "mitime": "05:00:01",
        "midate":"2022-04-01",
        "wind": 25.13432432432423,
        "carriertype": "CVN-74",
        "carriername": "USS Stennis",
        "carrierrwy": -9,
        "theatre": "Kola",
        "Tgroove": randint(10, 20),
        "wire": randint(1,4),
        "case": randint(1,3),
        "grade": "OK",
        "finalscore": 2,
        "points": 3,
        "details": "(LUL)X (F)IM  LOLULIC LOLULAR"
    }

    #print(result)

    return result

def testStrafe(funkplot: FunkPlot):

    # Debug info.
    print("Testing StrafeRun plot")

    # Get result.
    resultStrafe=getResultStrafe()

    # Create figuire.
    fig, ax=funkplot.PlotStrafeRun(resultStrafe)

    return fig, ax

def testBomb(funkplot: FunkPlot):

    # Debug info.
    print("Testing BombRun plot")

    # Get result.
    resultBomb=getResultBomb()

    # Create figure.
    fig, ax=funkplot.PlotBombRun(resultBomb)

    return fig, ax

def testTrap(funkplot: FunkPlot, trapfile: str):

    # Debug info.
    print(f"Testing TrapSheet plot from {trapfile}")

    # Get result.
    result=getResultTrap(trapfile)

    # Create figure.
    fig, axs=funkplot.PlotTrapSheet(result)

    return fig, axs
