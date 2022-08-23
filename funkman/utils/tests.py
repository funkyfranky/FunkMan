"""
Test cases.
"""

import matplotlib.pyplot as plt
from ..funkplot.funkplot import FunkPlot

def testStrafe(funkplot: FunkPlot):

    # Strafe result.
    resultStrave = {
    "type": "Strafe Result",
    "player": "funkyfranky",
    "name": "My Target",
    "clock": "9:45",
    "roundsFired": 500,
    "roundsHit": 100,
    "roundsQuality": "Quality",
    "strafeAccuracy": "10",
    "rangename": "My Range",
    "airframe": "F/A-18C_hornet",
    "invalid": "true",
    }

    print("Testing BombRun plot")

    fig, ax=funkplot.PlotStrafeRun(resultStrave)
    plt.show()

    return fig, ax

def testBomb(funkplot):

    # Bomb run result
    resultBomb = {
    "type": "Bomb Result",
    "name": "Target Name",
    "distance": 100,
    "radial": 37,
    "weapon": "Mk 82",
    "quality": "Ineffective",
    "player": "funkyfranky",
    "clock": "8:02",
    #"airframe": "F/A-18C_hornet",
    "rangename": "My Range Name",
    "attackHdg": 45,
    "attackVel": 300,
    "attackAlt": 16467,
    }     

    print("Testing BombRun plot")

    fig, ax=funkplot.PlotBombRun(resultBomb)
    plt.show()

    return fig, ax

def testTrap(funkplot):

    # Test template file.
    trapfile="D:/AIRBOSS-CVN-71_Trapsheet-New callsign_FA-18C_hornet-0006.csv"

    # Read trapsheet from disk for testing.
    ts = funkplot.ReadTrapsheet(trapfile)

    grade={
        "airframe": 'FA-18C_hornet',
        "carriername": "USS Stennis",
        "carrierType": "CVN-74",
        "case": 3,
        "finalscore": "OK",
        "points": 4,
        "details": "LUL",
        "wire": 3,
        "Tgroove": 15,
    }

        # Create playerData table. This will come from the FSM event.
    playerData={
        "trapsheet": ts,
        "airframe": 'FA-18C_hornet',
        "Tgroove": 15,
        "case": 1,
        "grade": grade,
        "carrierrwy": -9.0,
        "name": "funkyfranky",
    }

    print("Testing trapsheet plot")

    fig, axs=funkplot.PlotTrapSheet(playerData)
    plt.show()

    return fig, axs
