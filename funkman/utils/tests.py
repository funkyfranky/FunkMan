"""
Test cases.
"""

from random import randint
import matplotlib.pyplot as plt
from ..funkplot.funkplot import FunkPlot

def testStrafe(funkplot: FunkPlot):

    Nfired=randint(1, 500)
    Nhit=randint(0, Nfired)

    # Strafe result.
    resultStrave = {
    "type": "Strafe Result",
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
    }

    print("Testing StrafeRun plot")

    # Create figuire.
    fig, ax=funkplot.PlotStrafeRun(resultStrave)

    return fig, ax

def testBomb(funkplot: FunkPlot):

    # Bomb run result
    resultBomb = {
    "type": "Bomb Result",
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
    "theater": "Caucasus"
    }     

    # Debug info.
    print("Testing BombRun plot")

    # Create figure.
    fig, ax=funkplot.PlotBombRun(resultBomb)

    return fig, ax

def testTrap(funkplot: FunkPlot):

    # Test template file.
    trapfile="D:/AIRBOSS-CVN-71_Trapsheet-New callsign_FA-18C_hornet-0006.csv"

    # Read trapsheet from disk for testing.
    trapsheet=funkplot.ReadTrapsheet(trapfile)

    result={
        "name":"funkyfranky",
        "trapsheet": trapsheet,
        "airframe": 'FA-18C_hornet',
        "mitime": "05:00:01",
        "midate":"2022-04-01",
        "wind": 25,
        "carriertype": "CVN-74",
        "carriername": "USS Stennis",
        "carrierrwy": -9,
        "theatre": "Kola",
        "Tgroove": randint(10, 20),
        "wire": randint(1,4),
        "case": randint(1,3),
        "finalscore": "OK",
        "points": 3,
        "details": "LUL"
    }
    
    # Debug info.
    print("Testing TrapSheet plot")

    # Create figure.
    fig, axs=funkplot.PlotTrapSheet(result)

    return fig, axs
