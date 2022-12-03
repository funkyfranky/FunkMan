"""
Test cases.
"""

from random import randint
from ..funkplot.funkplot import FunkPlot
from ..utils.utils import ReadTrapsheet

from logger import logger

log = logger.logging.getLogger(__name__)


def getResultStrafe():

    Nfired = randint(1, 500)
    Nhit = randint(0, Nfired)
    Nfired = 5
    Nhit = 5

    # Result.
    resultStrave = {
        "command": "moose_strafe_result",
        "player": "funkyfranky",
        "name": "My Target",
        "clock": "9:45:01",
        "midate": "2022-04-01",
        "roundsFired": Nfired,
        "roundsHit": Nhit,
        "roundsQuality": "Some Quality",
        "strafeAccuracy": Nhit / Nfired * 100,
        "rangename": "My Range",
        "airframe": "F/A-18C_hornet",
        "invalid": "false",
        "theatre": "Caucasus",
    }

    return resultStrave


def getResultBomb():

    # Result.
    result = {
        "command": "moose_bomb_result",
        "name": "Target Name",
        "distance": randint(5, 300),
        "radial": randint(1, 360),
        "weapon": "Mk 82",
        "quality": "Ineffective",
        "player": "funkyfranky",
        "clock": "8:02",
        "airframe": "F/A-18C_hornet",
        "rangename": "My Range Name",
        "attackHdg": randint(1, 360),
        "attackVel": randint(250, 400),
        "attackAlt": randint(6000, 12000),
        "theatre": "Caucasus",
    }

    return result


def getResultTrap(trapfile: str):

    # Read trapsheet from disk for testing.
    trapsheet = ReadTrapsheet(trapfile)

    # Debug info.
    log.debug(trapsheet)
    log.debug(trapsheet.keys())
    try:
        grade = trapsheet.get("Grade")[-1]
    except:
        grade = "N/A"
    try:
        details = trapsheet.get("Details")[-1]
    except:
        details = "N/A"
    try:
        points = trapsheet.get("Points")[-1]
    except:
        points = 0

    details.strip()
    if details.strip() == "":
        details = "Unicorn"

    rwyangle = -9
    wire = randint(1, 4)
    carriername = "USS Stennis"
    carriertype = "CVN-74"
    landingdist = -165 + 79  # sterndist+wire3
    if "Tarawa" in trapfile:
        rwyangle = 0
        wire = None
        carriername = "Tarawa"
        carriertype = "LHA"
        landingdist = -125 + 69  # sterndist+landingpos

    airframe = "FA-18C_hornet"
    if "AV8B" in trapfile:
        airframe = "AV8BNA"

    # Result.
    result = {
        "command": "moose_lso_grade",
        "name": "Ghostrider",
        "trapsheet": trapsheet,
        "airframe": airframe,
        "mitime": "05:00:01",
        "midate": "2022-04-01",
        "wind": 25.13432432432423,
        "carriertype": carriertype,
        "carriername": carriername,
        "carrierrwy": rwyangle,
        "landingdist": landingdist,
        "theatre": "Kola",
        "Tgroove": randint(10, 20),
        "case": randint(1, 3),
        "grade": grade or "OK",
        "finalscore": points or 2,
        "points": points or 3,
        "details": details or "(LUL)X (F)IM  LOLULIC LOLULAR",
    }
    if wire:
        result["wire"] = wire

    log.debug(result)

    return result


def testStrafe(funkplot: FunkPlot):

    # Debug info.
    log.debug("Testing StrafeRun plot")

    # Get result.
    resultStrafe = getResultStrafe()

    # Create figuire.
    fig, ax = funkplot.PlotStrafeRun(resultStrafe)

    return fig, ax


def testBomb(funkplot: FunkPlot):

    # Debug info.
    log.debug("Testing BombRun plot")

    # Get result.
    resultBomb = getResultBomb()

    # Create figure.
    fig, ax = funkplot.PlotBombRun(resultBomb)

    return fig, ax


def testTrap(funkplot: FunkPlot, trapfile: str):

    # Debug info.
    log.debug(f"Testing TrapSheet plot from {trapfile}")

    # Get result.
    result = getResultTrap(trapfile)

    # Create figure.
    fig, axs = funkplot.PlotTrapSheet(result)

    return fig, axs
