from funkman.funkplot.funkplot import FunkPlot
from funkman.utils.tests import getResultStrafe, getResultTrap

# Init funkplot.
fplot = FunkPlot()

testfiles = [
    {"filename": "./testfiles/Trapsheet-AV8B_Tarawa-001.csv", "savefile": "Tarawa-001.png"},
    {"filename": "./testfiles/SH_unicorn_AIRBOSS-trapsheet-Yoda_FA-18C_hornet-0001.csv", "savefile": "Hornet-001.png"},
]

for testcase in testfiles:
    filename = testcase.get("filename")
    savefile = testcase.get("savefile")
    result = getResultTrap(filename)
    fplot.PlotTrapSheet(result, savefile)

# res=getResultTrap("./testfiles/Trapsheet-AV8B_Tarawa-001.csv")
# res=getResultTrap("./testfiles/SH_unicorn_AIRBOSS-trapsheet-Yoda_FA-18C_hornet-0001.csv")
# fplot.PlotTrapSheet(res)
