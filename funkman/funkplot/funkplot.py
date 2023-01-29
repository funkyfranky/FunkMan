"""
FunkPlot

This class uses matplotlib to create fancy images of trap sheets as well as bombing and strafing results.
"""

import matplotlib.pyplot as plt
from matplotlib.offsetbox import TextArea, AnnotationBbox
import matplotlib
import math
import numpy as np
from datetime import datetime
from enum import Enum
from ..utils.utils import _GetVal

class PlotColor(Enum):
    FACE      = '#404040'
    REFERENCE = '#A6A6A6'
    GRID      = '#585858'
    SPINE     = '#585858'
    LABEL     = '#BFBFBF'

class AircraftType(Enum):
    HORNET='FA-18C_hornet'
    TOMCATA="F-14A-135-GR"
    TOMCATB="F-14B"
    HARRIER="AV8BNA"
    HAWK="T-45"
    SKYHAWK="A-4E-C"
    RHINOE="FA-18E"
    RHINOF="FA-18F"
    GROWLER="EA-18G"

    @property
    def getAoA(self):
        if self.value==AircraftType.HORNET.value or self.value==AircraftType.RHINOE.value or self.value==AircraftType.RHINOF.value or self.value==AircraftType.GROWLER.value:
            return 7.4,8.1,8.8
        elif self.value==AircraftType.HAWK.value:
            return 6.75, 7.00, 7.25
        elif self.value==AircraftType.TOMCATA.value:
            return 9.5, 10.0, 10.5
        elif self.value==AircraftType.TOMCATB.value:
            return 9.5, 10.0, 10.5
        elif self.value==AircraftType.HARRIER.value:
            return 10, 11, 12
        elif self.value==AircraftType.SKYHAWK.value:
            return 8.5, 8.75, 9.0
        else:
            return 5, 10, 15


class FunkPlot():

    def __init__(self, ImagePath="./funkpics/") -> None:

        # Info message.
        print(f"Init FunkPlot: Reading images from {ImagePath}...")

        # Append / if necessary.
        if not ImagePath.endswith("/") or ImagePath.endswith("\\"):
            ImagePath=ImagePath+"/"

        # Read images:
        self.imageBombCircle = plt.imread(ImagePath+"BombCircle.png")
        self.imageStrafePit  = plt.imread(ImagePath+"StrafePit.png")

        self.imageCVNside    = plt.imread(ImagePath+'CarrierCVN_Side.png')
        self.imageCVNtop     = plt.imread(ImagePath+'CarrierCVN_TopDown.png')

        self.imageLHAside    = plt.imread(ImagePath+'CarrierLHA_Side.png')
        self.imageLHAtop     = plt.imread(ImagePath+'CarrierLHA_TopDown.png')

        self.imageCrater     = plt.imread(ImagePath+"Crater.png")
        self.imageNorthUp    = plt.imread(ImagePath+"NorthUp.png")
        self.imageBullet     = plt.imread(ImagePath+"BulletHole.png")

        self.imageUnicorn1   = plt.imread(ImagePath+"Unicorn1.png")
        self.imageUnicorn2   = plt.imread(ImagePath+"Unicorn2.png")
        #self.imageUnicorn3   = plt.imread(ImagePath+"Unicorn3.png")


    def _GetAoA(self, actype: str):
        """
        Returns the angle of attack (AoA) for a given aircraft type.
        """
        if actype==AircraftType.HARRIER.value:
            return AircraftType.HARRIER.getAoA
        elif actype==AircraftType.HAWK.value:
            return AircraftType.HAWK.getAoA
        elif actype==AircraftType.HORNET.value:
            return AircraftType.HORNET.getAoA
        elif actype==AircraftType.RHINOE.value:
            return AircraftType.RHINOE.getAoA
        elif actype==AircraftType.RHINOF.value:
            return AircraftType.RHINOF.getAoA
        elif actype==AircraftType.GROWLER.value:
            return AircraftType.GROWLER.getAoA
        elif actype==AircraftType.SKYHAWK.value:
            return AircraftType.SKYHAWK.getAoA
        elif actype==AircraftType.TOMCATA.value:
            return AircraftType.TOMCATA.getAoA
        elif actype==AircraftType.TOMCATB.value:
            return AircraftType.TOMCATB.getAoA
        else:
            print("WARNING: Unknown aircraft type! Taking generic AoA values")
            return 5,10,15

    def _Polar2Cart(self, r, phi):
        """
        Convert from polar to cartesian coordinates.
        """
        phi=math.radians(90-phi)
        x=r*math.cos(phi)
        y=r*math.sin(phi)
        return x, y

    def _SetSpine(self, ax, color):
        ax.spines['bottom'].set_color(color)
        ax.spines['top'].set_color(color)
        ax.spines['left'].set_color(color)
        ax.spines['right'].set_color(color)

    def PlotBombRun(self, result):
        """
        Creates a bomb run figure for a given result table.
        """

        # Set matplotlib backend.
        matplotlib.use('Agg')
        plt.ioff()

        # Length of axes.
        zmax=195

        # Define distance.
        distance=float(_GetVal(result, "distance", 500,  0))
        radial=float(_GetVal(result, "radial", 0, 0))

        # Attack parameters.
        attackHdg=float(_GetVal(result, "attackHdg", 0, 0))
        attackAlt=_GetVal(result, "attackAlt", "?", 0)
        attackVel=_GetVal(result, "attackVel", "?", 0)

        # Mission info.
        theatre=_GetVal(result, "theatre", "Unknown Map")
        missiontime=_GetVal(result, "clock", "?")
        missiondate=_GetVal(result, "midate", "?")
        
        # Try to figure out if the impact was long, short, left, right.
        dphi=float(radial)-float(attackHdg)
        if dphi>=-45 and dphi<45:
            pass
        elif dphi>=45 and dphi<90:            
            pass

        # Convert from polar to cartesian coordinates.
        x,y=self._Polar2Cart(min(distance, zmax), float(radial))

        # Create figure and axis objects.
        fig, ax = plt.subplots(1, 1, facecolor=PlotColor.FACE.value, sharex=True, dpi=150)

        # Set tick label color.
        plt.setp(ax.get_xticklabels(), color=PlotColor.LABEL.value)
        plt.setp(ax.get_yticklabels(), color=PlotColor.LABEL.value)

        # Set label color.
        ax.xaxis.label.set_color(PlotColor.LABEL.value)

        # Create title.
        title=str(f'Bombing result of {_GetVal(result, "player", "Ghostrider")}\n')
        title+=str(f'{_GetVal(result, "rangename", "Unknown Range")}: {_GetVal(result, "name", "Unknown Target")}\n')

        # Set title.
        fig.suptitle(title, fontsize=12, color=PlotColor.LABEL.value)

        # Set figure size.
        fig.set_size_inches(8, 6)

        # Set background color.
        ax.set_facecolor(PlotColor.FACE.value)

        # Set x-label.
        ax.set_xlabel("Distance [Meters]")

        # Show bomb circle.
        plt.imshow(self.imageBombCircle, interpolation='none', origin='upper', extent=[-zmax, zmax, -zmax, zmax], clip_on=True)

        # North Up image.
        north=150
        plt.imshow(self.imageNorthUp, interpolation='none', origin='upper', extent=[north-30, north+30, north-23, north+37], clip_on=True, zorder=17)

        # Plot impact point.
        plt.plot([x], [y], 'ro', markersize=3)
        
        # Crater image.
        scrater=20
        plt.imshow(self.imageCrater, interpolation='none', origin='upper', extent=[x-scrater, x+scrater, y-scrater, y+scrater], clip_on=True)

        # Attack heading arrow in North Up image.
        xa,ya=self._Polar2Cart(30, float(attackHdg))
        ax.arrow(north, north, xa, ya, head_width=5, head_length=5, zorder=501, length_includes_head=True, color="green")

        # Attack heading arrow.
        xa,ya=self._Polar2Cart(30, float(radial))
        ax.arrow(north, north, xa, ya, head_width=5, head_length=5, zorder=500, length_includes_head=True, color="red")

        # Plot grid.
        plt.grid(axis='both', color='red', alpha=0.3)

        # Annotation box with attack data.
        offsetbox = TextArea(f'{_GetVal(result, "airframe", "Unknown AC")}\nh={attackAlt} ft\n$v$={attackVel} kts\n$\psi$={attackHdg}°',
        textprops=dict(color="green", backgroundcolor=PlotColor.FACE.value))
        ab = AnnotationBbox(offsetbox, (x, y),
                            xybox=(0.9, 0.8),
                            xycoords='figure fraction',
                            boxcoords="figure fraction", #, box_alignment=(1.1, 1.1))
                            bboxprops =dict(boxstyle="round, pad=0.6", fc=PlotColor.FACE.value, ec="green", lw=1.2))
        ax.add_artist(ab)

        # Annotation box with weapon data.
        offsetbox = TextArea(f'{_GetVal(result, "weapon")}\nr={distance} m\n$\phi$={radial}°\n{_GetVal(result, "quality", "?")}',
        textprops=dict(color="crimson", backgroundcolor=PlotColor.FACE.value))
        ab = AnnotationBbox(offsetbox, (x, y),
                            xybox=(0.9, 0.3),
                            xycoords='data',
                            boxcoords="figure fraction",
                            bboxprops =dict(boxstyle="round, pad=0.6", fc=PlotColor.FACE.value, ec="crimson", lw=1.2),
                            arrowprops=dict(arrowstyle="->"))
        ax.add_artist(ab)

        # Mission date at left bottom
        timestamp=str(f"{theatre}: {missiondate} ({missiontime})")
        plt.annotate(timestamp, xy=(0, 0), xycoords='figure fraction', alpha=0.5, color="grey", horizontalalignment='left', verticalalignment="bottom")

        # Real date at right bottom.
        timestamp = datetime.now().strftime(f"%Y-%b-%d (%H:%M:%S)")
        plt.annotate(timestamp, xy=(1, 0.0), xycoords='figure fraction', alpha=0.5, color="grey", horizontalalignment='right', verticalalignment="bottom")

        return fig, ax


    def PlotStrafeRun(self, result):
        """
        Creates a strafe run figure for a given result table.
        """

        # Set matplotlib backend.
        matplotlib.use('Agg')
        plt.ioff()

        # Get info from result table.
        player=_GetVal(result, "player", "GhostRider")
        actype=_GetVal(result, "airframe", "Unknown AC")

        roundsFired=_GetVal(result, "roundsFired", 1)
        roundsHit=_GetVal(result, "roundsHit", 0)
        invalid=_GetVal(result, "invalid", False)

        # Mission info.
        theatre=_GetVal(result, "theatre", "Unknown Map")
        missiontime=_GetVal(result, "clock", "?")
        missiondate=_GetVal(result, "midate", "?")

        # Debug info.
        print(f"Plotting Strafe Run for player {player}!")

        # Create subplot figure.
        fig, ax = plt.subplots(1, 1, facecolor=PlotColor.FACE.value, sharex=True, dpi=150)

        # Set face color.
        ax.set_facecolor(PlotColor.FACE.value)

        # Set size of figure.
        fig.set_size_inches(8, 6)

        #nx = int(fig.get_figwidth() * fig.dpi)
        #ny = int(fig.get_figheight() * fig.dpi) 
        #pos1 = ax.get_position() 

        # Create title.
        title=str(f"Strafing result of {player} [{actype}]")
        title+=str(f'\n{_GetVal(result, "rangename", "Unknown Range")}: {_GetVal(result, "name", "Unknown Target")}')

        # Set title.
        fig.suptitle(title, fontsize=12, color=PlotColor.LABEL.value)

        # Remove all axes and tics.
        ax.spines['top'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_xticks([])
        ax.set_yticks([])

        zmax=195

        # Read strafe pit image.        
        plt.imshow(self.imageStrafePit, interpolation='none', origin='upper', extent=[-zmax, zmax, -zmax, zmax], clip_on=True)

        for _ in range(1): #(roundsHit):

            r=np.random.randint(0,100)
            p=np.random.randint(0,360)

            # Convert from polar to cartesian coordinates.
            x,y=self._Polar2Cart(r, p)
            
            # Plot red "x" inside.
            #ax.plot(0, 0, "rX", zorder=15, alpha=0.5)

            # Bullet image.
            bullet=10
            plt.imshow(self.imageBullet, interpolation='none', origin='upper', extent=[x-bullet, x+bullet, y-bullet, y+bullet], clip_on=True)
            #fig.figimage(self.imageBullet,  0, 0, alpha=0.45, zorder=100, clip_on=True)

        for _ in range(roundsFired-roundsHit):
            r=np.random.randint(150,200)
            p=np.random.randint(0,360)

            # Convert from polar to cartesian coordinates.
            x,y=self._Polar2Cart(r, p)
            
            # Plot blue "X" outside.
            ax.plot(x, y, "bX", zorder=15, alpha=0.5)

        # Plot something outside to have the bullet image right.
        ax.plot(-zmax, -zmax, "rX", zorder=15, alpha=0.0)
        ax.plot(-zmax, +zmax, "rX", zorder=15, alpha=0.0)
        ax.plot(+zmax, -zmax, "rX", zorder=15, alpha=0.0)
        ax.plot(+zmax, +zmax, "rX", zorder=15, alpha=0.0)

        Nfired=_GetVal(result, "roundsFired", "?")
        Nhits=_GetVal(result, "roundsHit", "?")
        Accu=Nhits/max(Nfired,1)*100
        Qual=_GetVal(result, "roundsQuality", "?")

        # Annotation box with weapon data.
        text=str(f'Fired: {Nfired}\nHits: {Nhits}\nAccu={Accu:.1f}%\n{Qual}')
        offsetbox = TextArea(text, textprops=dict(color="green", backgroundcolor=PlotColor.FACE.value))
        ab = AnnotationBbox(offsetbox,
                            (x, y),
                            xybox=(zmax, -zmax/2),
                            xycoords='data',
                            boxcoords="data",
                            bboxprops =dict(boxstyle="round, pad=0.6", fc=PlotColor.FACE.value, ec="green", lw=1.2),
                            zorder=1000)
        ax.add_artist(ab)

        # Invalid runs.
        if invalid:
            ax.text(0.5, 0.35, '*** INVALID ***', va='bottom', ha='center', transform=ax.transAxes, color='red', fontsize=25, zorder=5000,
            bbox=dict(boxstyle="round", ec="red", fc="red", alpha=0.5,), rotation=30)

        #ax.text(0.6, 0.7, "Invalid", size=50, rotation=30., ha="center", va="center", bbox=dict(boxstyle="round", ec=(1., 0.5, 0.5), fc=(1., 0.8, 0.8),))

        # Mission date at left bottom
        timestamp=str(f"{theatre}: {missiondate} ({missiontime})")
        plt.annotate(timestamp, xy=(0, 0), xycoords='figure fraction', alpha=0.5, color="grey", horizontalalignment='left', verticalalignment="bottom")

        # Real date at right bottom.
        timestamp = datetime.now().strftime(f"%Y-%b-%d (%H:%M:%S)")
        plt.annotate(timestamp, xy=(1, 0.0), xycoords='figure fraction', alpha=0.5, color="grey", horizontalalignment='right', verticalalignment="bottom")

        return fig, ax


    def PlotTrapSheet(self, result, filename=None):
        """
        Creates trapsheet figure for a given player data table.
        """

        # Set matplotlib backend.
        matplotlib.use('Agg')
        plt.ioff()

        # Trapsheet data.
        try:
            trapsheet=result["trapsheet"]
        except:
            print("ERROR: Trap sheet data does not exist!")
            return

        # Length of trap sheet.
        lts=len(trapsheet)

        if lts==0:
            print("ERROR: Trap sheet is empty!")
            return

        # Conversion factor NM to feet.
        nm2feet = 6076.12
        nm2meter = 1852
        meter2nm = 1.0/1852.0
        meter2feet = 3.28084
        feet2meter = 0.3048

        # Get arrays.
        X=-np.array(trapsheet["X"])               # X in meters. Take care of minus sign!
        Y=np.array(trapsheet["Z"])                # Y in meters.
        AOA=np.array(trapsheet["AoA"])            # Angle of attack in AU.
        ALT=np.array(trapsheet["Alt"])*meter2feet # Altitude in feet.

        # Get other info from result.
        actype=_GetVal(result, "airframe", "Unkown")
        Tgroove=_GetVal(result, "Tgroove", "?", 1)

        player=_GetVal(result, "name", "Ghostrider")
        grade=_GetVal(result, "grade", "?")
        points=_GetVal(result, "points", "?")
        details=_GetVal(result, "details")
        case=_GetVal(result, "case", "?")
        wire=_GetVal(result, "wire", "?")

        carriertype=_GetVal(result, "carriertype", "?")
        carriername=_GetVal(result, "carriername", "?")
        landingdist=_GetVal(result, "landingdist", -86)
        windondeck=_GetVal(result, "wind", "?", 1)
        missiontime=_GetVal(result, "mitime", "?")
        missiondate=_GetVal(result, "midate", "?")
        theatre=_GetVal(result, "theatre", "Unknown Map")

        # Angled runway.
        theta=_GetVal(result, "carrierrwy", -9)

        if abs(theta)>0.1:
            angledRunway=True
        else:
            angledRunway=False

        # Convert ange to radians.
        theta = math.radians(theta)

        # Position and font parameters.
        xpoint=0.195
        xpointsize=9

        # Skip last AoA values as they are to inaccurate.    
        num_aoa = 3

        # Rotation matrix.
        rotMatrix = np.array([[np.cos(theta), -np.sin(theta)],
                              [np.sin(theta),  np.cos(theta)]])

        # X-Y array in NM
        dx = landingdist
        if angledRunway:
            dy = 9.5 # Translate perpendicular so that the y=0 corresponds to the stern coordinate.
        else:
            dy = 8 #35
        xy = np.array([X+dx, Y+dy])*meter2nm # convert to NM

        # Rotate grid
        xy = np.dot(rotMatrix, xy)

        X=xy[0]  # X in NM
        Y=xy[1]  # Y in NM

        # Create subplot figure and axes.
        fig, axs = plt.subplots(3, 1, sharex=True, facecolor=PlotColor.FACE.value, dpi=150)

        # Set figure size. Needed to have the carrier images in the right place!
        fig.set_size_inches(8, 6)

        # second annotation relative to the axis limits
        bbox_props = dict(boxstyle="round, pad=0.5", fc=PlotColor.FACE.value, ec="lightsteelblue", lw=1)

        if angledRunway:
            carrierinfo=str(f"{carriername}\n{carriertype}\nCase {case}\nWind {windondeck}\n{wire} wire\nT$_G$={Tgroove}")
        else:
            carrierinfo=str(f"{carriername}\n{carriertype}\nCase {case}\nWind {windondeck}\nT$_G$={Tgroove}")
        plt.annotate(carrierinfo, xy=(0.99, 0.98), xycoords='figure fraction', alpha=0.6, color="lightsteelblue", horizontalalignment='right', verticalalignment="top", bbox=bbox_props)

        # Mission date at left bottom
        timestamp=str(f"{theatre}: {missiondate} ({missiontime})")
        plt.annotate(timestamp, xy=(0, 0), xycoords='figure fraction', alpha=0.5, color="grey", horizontalalignment='left', verticalalignment="bottom")

        # Real date at right bottom.
        timestamp = datetime.now().strftime(f"%Y-%b-%d (%H:%M:%S)")
        plt.annotate(timestamp, xy=(1, 0.0), xycoords='figure fraction', alpha=0.5, color="grey", horizontalalignment='right', verticalalignment="bottom")

        if angledRunway:
            # These are the CVN images:

            # Side view.
            axs[0].figure.figimage(self.imageCVNside, 930, 557, alpha=0.45, zorder=1, clip_on=True)

            # Top-down view.
            axs[0].figure.figimage(self.imageCVNtop,  930, 347, alpha=0.45, zorder=1, clip_on=True)
        else:
            # These are the LHA images:

            # Side view for the glideslope plot.
            axs[0].figure.figimage(self.imageLHAside,  910, 560, alpha=0.75, zorder=1, clip_on=True)

            # Top-down view.
            axs[0].figure.figimage(self.imageLHAtop,   910, 340, alpha=0.75, zorder=1, clip_on=True)

        if grade=="_OK_":
            fig.figimage(self.imageUnicorn2, 550, 450)
        elif grade=="OK":
            fig.figimage(self.imageUnicorn1, 550, 450)

        """
        Glide Slope
        """
        # Set axis.
        ax = axs[0]

        # Y-axis limit.
        ax.set_ylim([-20,580])  #Glideslope Reference scale from 0 to 650 feet

        # No bottom line.
        ax.spines['bottom'].set_visible(False)        

        if angledRunway:
            gs=math.radians(3.5) # Glide slope [rad]
            y0=2*meter2feet
        else:
            gs=math.radians(3.0) # Glide slope [rad]
            y0=50#50+2*meter2feet

        # Glide Slope Reference line
        _X=np.linspace(0, 1.2)
        _Y=nm2feet*_X*np.tan(gs)+y0
        ax.plot(_X,_Y, PlotColor.REFERENCE.value, linewidth=1.0, alpha=0.8)

        # Actual data with glow.
        ax.plot(X, ALT, 'b',  linewidth=8, alpha=0.1)   #"glow" effect arond the glideslope line
        ax.plot(X, ALT, 'b',  linewidth=5, alpha=0.1)   #"glow" effect arond the glideslope line
        ax.plot(X, ALT, 'b',  linewidth=3, alpha=0.15)  #"glow" effect arond the glideslope line
        ax.plot(X, ALT, 'w-', linewidth=1, alpha=0.45)  #"glow" effect arond the glideslope line

        # Add text.
        ax.text(xpoint, 410, "Glide Slope", color=PlotColor.LABEL.value, fontsize=xpointsize, alpha=0.5)

        """
        Line Up
        """    

        # Set axis.
        ax = axs[1]

        # y-axis limit.
        if angledRunway:
            ax.set_ylim([-501,901])
        else:
            ax.set_ylim([-301,601])

        # Line up referece line.
        if angledRunway:
            y0=0
        else:
            y0=35*meter2feet #*feet2meter # 100 ft abeam

        # Glide Slope Reference line
        _X=np.linspace(0, 1.2)
        _Y=np.array([y0]*_X.shape[0])
        ax.plot(_X, _Y, PlotColor.REFERENCE.value, linewidth=2, alpha=0.8)

        # Plot lineup with glow.
        ax.plot(X, -nm2feet*Y, 'g',  linewidth=16, alpha=0.10)
        ax.plot(X, -nm2feet*Y, 'g',  linewidth=10, alpha=0.10)
        ax.plot(X, -nm2feet*Y, 'g',  linewidth=6,  alpha=0.15)
        ax.plot(X, -nm2feet*Y, 'w-', linewidth=1,  alpha=0.45)

        # Add text "Lineup"
        ax.text(xpoint, 510, "Lineup", color=PlotColor.LABEL.value, fontsize=xpointsize, alpha=0.5)

        """
        AoA
        """
        # Set axis.
        ax = axs[2]

        # Set x label.
        ax.set_xlabel("Distance [Nautical Miles]")

        # AoA values. We skip the last values before the landing.
        AoA=AOA[:-num_aoa]

        # Get AC specific AoA values.
        AoAmin, AoAopt, AoAmax=self._GetAoA(actype)

        # Plot limit.
        xmax=ax.get_xlim()[1]

        # Plot AoA limits.
        ax.plot([0,xmax], [AoAmax,AoAmax], 'r--', linewidth=1.2, alpha=0.6)
        ax.plot([0,xmax], [AoAmin,AoAmin], 'r--', linewidth=1.2, alpha=0.6)
        ax.plot([0,xmax], [AoAopt,AoAopt], 'g--', linewidth=1.2, alpha=0.6)

        AoAmin=min(AoAmin, np.min(AoA))
        AoAmax=max(AoAmax, np.max(AoA))

        # Y-axis limit.
        ax.set_ylim([0.9*AoAmin, 1.1*AoAmax])

        # Add AoA text.
        ax.text(xpoint, AoAmax*1.05, "AoA", color=PlotColor.LABEL.value, fontsize=xpointsize, alpha=0.5)

        # Plot AoA line with glow effect.
        ax.plot(X[:-num_aoa], AoA, 'g-', linewidth=8, alpha=0.10)
        ax.plot(X[:-num_aoa], AoA, 'g-', linewidth=5, alpha=0.10)
        ax.plot(X[:-num_aoa], AoA, 'g-', linewidth=3, alpha=0.15)
        ax.plot(X[:-num_aoa], AoA, 'w-', linewidth=1, alpha=0.45)


        """
        Axes Settings
        """

        # Common axes settings.
        for ax in axs:
            # Set background color
            ax.set_facecolor(PlotColor.FACE.value)
            # Set x-axis limit.
            #ax.set_xlim([0.001, 1.2])
            ax.set_xlim([-0.1, 1.01])
            # Set grid.
            ax.grid(linestyle='-', linewidth='0.5', color=PlotColor.GRID.value)
            # Set tick parameters.
            ax.tick_params(axis=u'both', which=u'both', length=0)
            # Set spines.
            self._SetSpine(ax, PlotColor.SPINE.value)
            # Set tick label color.
            plt.setp(ax.get_xticklabels(), color=PlotColor.LABEL.value)
            plt.setp(ax.get_yticklabels(), color=PlotColor.LABEL.value)
            # Set label color.
            ax.xaxis.label.set_color(PlotColor.LABEL.value)
            # Invert x-axis
            ax.invert_xaxis()

        """
        Title
        """
        # Create title.
        title = str(f'Trapsheet of {player} [{actype}]')
        title+= str(f"\n{grade} {points}PT - {details}")

        # Set title.
        fig.suptitle(title, fontsize=12, color=PlotColor.LABEL.value)

        # Show plot.
        if filename:
            plt.savefig(filename)

        return fig, axs