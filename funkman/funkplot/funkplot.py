"""
FunkPlot

This class uses matplotlib to create fancy images of trap sheets as well as bombing and strafing results.
"""

import matplotlib.pyplot as plt
from matplotlib.offsetbox import TextArea, AnnotationBbox
import matplotlib
import math
import numpy as np
import csv
import datetime
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

    @property
    def getAoA(self):
        if self.value==AircraftType.HORNET.value:
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

    def __init__(self, ImagePath="./images/") -> None:

        # Info message.
        print("Init FunkPlot: Reading images...")

        path=ImagePath

        # Read images:
        self.imageBombCircle = plt.imread(path+"BombCircle.png")
        self.imageStrafePit  = plt.imread(path+"StrafePit.png")

        self.imageCVNside    = plt.imread(path+'CarrierCVN_Side.png')
        self.imageCVNtop     = plt.imread(path+'CarrierCVN_TopDown.png')

        self.imageLHAside    = plt.imread(path+'CarrierLHA_Side.png')
        self.imageLHAtop     = plt.imread(path+'CarrierLHA_Side.png')

        self.imageCrater     = plt.imread(path+"Crater.png")
        self.imageNorthUp    = plt.imread(path+"NorthUp.png")
        self.imageBullet     = plt.imread(path+"BulletHole.png")


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
        elif actype==AircraftType.SKYHAWK.value:
            return AircraftType.SKYHAWK.getAoA
        elif actype==AircraftType.TOMCATA.value:
            return AircraftType.TOMCATA.getAoA
        elif actype==AircraftType.TOMCATB.value:
            return AircraftType.TOMCATB.getAoA

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

        # Length of axes.
        zmax=195

        # Define distance.
        distance=_GetVal(result, "distance", 500)
        radial=_GetVal(result, "radial", 0)

        # Attack parameters.
        attackHdg=_GetVal(result, "attackHdg", 0)
        attackAlt=_GetVal(result, "attackAlt", "?")
        attackVel=_GetVal(result, "attackVel", "?")
        

        dphi=radial-attackHdg
        if dphi>=-45 and dphi<45:
            pass
        elif dphi>=45 and dphi<90:            
            pass

        # Convert from polar to cartesian coordinates.
        x,y=self._Polar2Cart(min(distance, zmax), radial)

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
        xa,ya=self._Polar2Cart(30, attackHdg)
        ax.arrow(north, north, xa, ya, head_width=5, head_length=5, zorder=501, length_includes_head=True, color="green")

        # Attack heading arrow.
        xa,ya=self._Polar2Cart(30, radial)
        ax.arrow(north, north, xa, ya, head_width=5, head_length=5, zorder=500, length_includes_head=True, color="red")

        # Plot grid.
        plt.grid(axis='both', color='red', alpha=0.3)

        # Annotation box with weapon data.
        offsetbox = TextArea(f'{_GetVal(result, "weapon")}\nr={distance} m\n$\phi$={radial}°\n{_GetVal(result, "quality", "?")}')
        ab = AnnotationBbox(offsetbox, (x, y),
                            xybox=(zmax+50, -zmax/2),
                            xycoords='data',
                            boxcoords="data",
                            arrowprops=dict(arrowstyle="->"))
        ax.add_artist(ab)

        # Annotation box with attack data.
        offsetbox = TextArea(f'{_GetVal(result, "airframe", "Unknown AC")}\nh={attackAlt} ft\n$v$={attackVel} kts\n$\psi$={attackHdg}°')
        ab = AnnotationBbox(offsetbox, (x, y),
                            xybox=(zmax+50, zmax-50),
                            xycoords='data',
                            boxcoords="data")
        ax.add_artist(ab)

        return fig, ax


    def PlotStrafeRun(self, result):
        """
        Creates a strafe run figure for a given result table.
        """

        # Get info from result table.
        player=_GetVal(result, "player", "GhostRider")
        actype=_GetVal(result, "airframe", "Unknown AC")

        roundsFired=_GetVal(result, "roundsFired", 1)
        roundsHit=_GetVal(result, "roundsHit", 0)

        print(f"Plotting Strafe Run for player {player}!")

        # Create subplot figure.
        fig, ax = plt.subplots(1, 1, facecolor=PlotColor.FACE.value, sharex=True, dpi=150)

        # Set face color.
        ax.set_facecolor(PlotColor.FACE.value)

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

        for _ in range(roundsHit):

            r=np.random.randint(0,100)
            p=np.random.randint(0,360)

            # Convert from polar to cartesian coordinates.
            x,y=self._Polar2Cart(r, p)
            
            # Plot red "x" inside.
            #ax.plot(x, y, "rX", zorder=15, alpha=0.5)

            # Crater image.
            bullet=10
            plt.imshow(self.imageBullet, interpolation='none', origin='upper', extent=[x-bullet, x+bullet, y-bullet, y+bullet], clip_on=True)

        for _ in range(roundsFired-roundsHit):
            r=np.random.randint(150,200)
            p=np.random.randint(0,360)

            # Convert from polar to cartesian coordinates.
            x,y=self._Polar2Cart(r, p)
            
            # Plot blue "X" outside.
            ax.plot(x, y, "bX", zorder=15, alpha=0.5)


        # Annotation box with weapon data.
        text=str(f'Fired: {_GetVal(result, "roundsFired", "?")}\nHits: {_GetVal(result, "roundsHit", "?")}\nAccu={_GetVal(result, "strafeAccuracy", "?")}%\n{_GetVal(result, "roundsQuality", "?")}')
        ab = AnnotationBbox(TextArea(text), 
                            (x, y),
                            xybox=(zmax, -zmax/2),
                            xycoords='data',
                            boxcoords="data", zorder=1000)
        ax.add_artist(ab)

        ax.text(0.5, 0.35, '*** INVALID ***', va='bottom', ha='center', transform=ax.transAxes, color='red', fontsize=25, zorder=5000,
        bbox=dict(boxstyle="round", ec="red", fc="red", alpha=0.5,), rotation=30)

        #ax.text(0.6, 0.7, "Invalid", size=50, rotation=30., ha="center", va="center", bbox=dict(boxstyle="round", ec=(1., 0.5, 0.5), fc=(1., 0.8, 0.8),))

        return fig, ax


    def PlotTrapSheet(self, playerData, Grade):
        """
        Creates trapsheet figure for a given player data table.
        """

        # Trapsheet data.
        trapsheet=playerData["trapsheet"]

        l=len(trapsheet)

        X=np.empty(l, dtype=float)
        Y=np.empty(l, dtype=float)
        AOA=np.empty(l, dtype=float)
        ALT=np.empty(l, dtype=float)

        for ts in trapsheet:
            np.append(X, ts["X"])
            np.append(Y, ts["Z"])
            np.append(AOA, ts["AoA"])
            np.append(ALT, ts["Alt"])

        actype=_GetVal(playerData, "airframe", "Unkown")
        Tgroove=_GetVal(playerData, "Tgroove", "?")

        print("FF actype")
        print(actype)

        carriertype=_GetVal(Grade, "Tgroove", "?")
        windondeck=_GetVal(Grade, "wind", "?")
        missiontime=_GetVal(Grade, "mitime", "?")
        missiondate=_GetVal(Grade, "midate", "?")
        theatre=_GetVal(Grade, "theatre", "?")

        # Angled runway.
        theta=_GetVal(Grade, "carrierrwy", -9)

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

        # Conversion factor.
        feet = 6076.12  # = -1 Nautical mile

        # Rotation matrix.
        rotMatrix = np.array([[np.cos(theta), -np.sin(theta)],
                              [np.sin(theta),  np.cos(theta)]])

        # X-Y array in NM
        dx = 20
        dy = 20
        xy = np.array([X+dx, Y+dy])/1852

        # Rotate grid
        xy = np.dot(rotMatrix, xy)

        X=xy[0]
        Y=xy[1]

        # Create subplot figure and axes.
        fig, axs = plt.subplots(3, 1, sharex=True, facecolor=PlotColor.FACE.value, dpi=150)

        # Set matplotlib backend.
        fig.set_size_inches(8, 6)

        #matplotlib.use('Agg')
        #plt.ioff()

        if angledRunway:
            # These are the CVN images:

            cx=1000
            cy=343

            # Top-down view.
            axs[0].figure.figimage(self.imageCVNtop, cx, cy, alpha=.45, zorder=1, clip_on=True)

            # Side view.
            axs[0].figure.figimage(self.imageCVNside, 1000, 567, alpha=.45, zorder=1)
        else:
            # These are the LHA images:

            # Top-down view.
            axs[0].figure.figimage(self.imageLHAtop, 940, 320, alpha=.75, zorder=1, clip_on=True)

            # side view for the glideslope plot
            axs[0].figure.figimage(self.imageLHAside, 930, 567, alpha=0.75, zorder=1)


        """
        Line Up
        """    

        # Set axis.
        ax = axs[1]

        # y-axis limit
        ax.set_ylim([-401,801])

        # Line up referece line.
        if angledRunway:
            m1 = np.array(ax.get_xlim())
            m1[0]=0
            m2=[0, 0]
        else:
            m1 = np.array(ax.get_xlim())
            m1[0]=0
            m2=[50, 50]

        ax.plot(m1, m2, PlotColor.REFERENCE.value, linewidth=2, alpha=0.8)

        # Plot lineup with glow.
        ax.plot(X, -feet*Y, 'g',  linewidth=16, alpha=0.10)
        ax.plot(X, -feet*Y, 'g',  linewidth=10, alpha=0.10)
        ax.plot(X, -feet*Y, 'g',  linewidth=6,  alpha=0.15) 
        ax.plot(X, -feet*Y, 'w-', linewidth=1,  alpha=0.45)

        # Add text "Lineup"
        ax.text(xpoint, 510, "Lineup", color=PlotColor.LABEL.value, fontsize=xpointsize, alpha=0.5)

        """
        Glide Slope
        """
        # Set axis.
        ax = axs[0]

        # Y-axis limit.
        ax.set_ylim([-1,650])  #Glideslope Reference scale from 0 to 650 feet

        if angledRunway:
            zt = feet*X*np.tan(math.radians(3.5))
            gx = 0
            gz = 40
        else:
            zt = feet*X*np.tan(math.radians(3.5))
            gx = 0
            gz = 40


        # Glide Slope Reference line
        ax.plot(X+gx, zt+gz, PlotColor.REFERENCE.value, linewidth=1.1, alpha=1)

        # Actual data with glow.
        ax.plot(X, ALT+gz+20, 'b',  linewidth=8, alpha=0.1)   #"glow" effect arond the glideslope line
        ax.plot(X, ALT+gz+20, 'b',  linewidth=5, alpha=0.1)   #"glow" effect arond the glideslope line
        ax.plot(X, ALT+gz+20, 'b',  linewidth=3, alpha=0.15)  #"glow" effect arond the glideslope line
        ax.plot(X, ALT+gz+20, 'w-', linewidth=1, alpha=0.45)  #"glow" effect arond the glideslope line

        # Add text.
        ax.text(xpoint, 410, "Glide Slope", color=PlotColor.LABEL.value, fontsize=xpointsize, alpha=0.5)

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
            ax.set_xlim([0.001, 1.2])
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
        player=_GetVal(playerData, "name", "Ghostrider")        
        grade=_GetVal(Grade, "finalscore", "?")
        points=_GetVal(Grade, "points", "?")
        details=_GetVal(Grade, "details")
        case=_GetVal(Grade, "case", "?")
        wire=_GetVal(Grade, "wire", "?")

        # Create title.
        title = str(f'Trapsheet of {player} [{actype}]')
        title+= str(f"\n Case {case}, {wire} wire: {grade} {points}PT - {details} - T$_G$={Tgroove} s")

        # Set title.
        fig.suptitle(title, fontsize=12, color=PlotColor.LABEL.value)

        """
        Save figure
        """

        # Save figure.
        #fig.savefig('D:/trapsheet.png', facecolor=PlotColor.FACE.value)

        return fig, axs


    def ReadTrapsheet(self, filename):
        """
        Read a trap sheet into a dictionary as numpy arrays.
        """        
        d={}
        try:
            with open(filename) as f:
                reader = csv.DictReader(f)

                for k in reader.fieldnames:
                    d[k]=np.array([])

                for row in reader:
                    for k in reader.fieldnames:
                        svalue = row[k]
                        try:
                            fvalue = float(svalue)
                            #print("float value: ", fvalue)
                            d[k] = np.append(d[k],fvalue)
                        except ValueError:
                            #print("Not a float", svalue)
                            d[k]=svalue
        except:
            print('ERROR!')

        return d

