from funkman.funkplot.funkplot import FunkPlot
from funkman.utils.tests import getResultStrafe, getResultTrap

fplot=FunkPlot()

#res=getResultStrafe()
#fplot.PlotStrafeRun(res)

res=getResultTrap("./testfiles/Trapsheet-AV8B_Tarawa-001.csv")
#res=getResultTrap("./testfiles/SH_unicorn_AIRBOSS-trapsheet-Yoda_FA-18C_hornet-0001.csv")
fplot.PlotTrapSheet(res)