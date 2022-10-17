-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Settings
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------

local socket=SOCKET:New(10042) --Utilities.Socket#SOCKET
socket:SendText("Hello World!")

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Bombing Ranges
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------

  
-- Some range
local range=RANGE:New("Practice Range")  --Functional.Range#RANGE

-- Enable funkman
range:SetFunkManOn()


--- Function called when a weapon impacts at the Range.
function range:OnAfterImpact(From, Event, To, Result, Player)
  local player=Player --Functional.Range#RANGE.PlayerData
  local result=Result --Functional.Range#RANGE.BombResult
  local Text=string.format("Player %s dropped ordnance at range %s in airframe %s", player.playername, result.rangename, result.airframe)
  env.info(Text)       
end

--- Function called when a player finished a straing run.    
function range:OnAfterStrafeResult(From, Event, To, Player, Result)
  local player=Player --Functional.Range#RANGE.PlayerData
  local result=Result --Functional.Range#RANGE.BombResult  
  local Text=string.format("Player %s strafed at range %s in airframe %s", player.playername, result.rangename, result.airframe)
  env.info(Text)
end

local function testBomb()

  local result = {} -- --Functional.Range#RANGE.BombResult
  result.command = SOCKET.DataType.BOMBRESULT
  result.name = "My Target"
  result.distance = math.random(1,150)
  result.radial = math.random(1,360)
  result.weapon = "Mk 82"
  result.quality = "INEFFECTIVE"
  result.player = "funkyfranky"
  result.time = timer.getAbsTime()
  result.clock = UTILS.SecondsToClock(result.time, true)
  result.midate=UTILS.GetDCSMissionDate()
  result.airframe = "F/A 18 Hornet"
  result.roundsFired = 0 -- Rangeboss Edit
  result.roundsHit = 0 -- Rangeboss Edit
  result.roundsQuality = "N/A" -- Rangeboss Edit
  result.rangename = "My Test Range"
  result.attackHdg = math.random(360)
  result.attackAlt = math.random(5000, 10000)
  result.attackVel = math.random(300, 500)
  result.theatre = env.mission.theatre
  
  env.info("FF Test bomb! Expect impact in 1 seconds..")
  
  local player={}--Functional.Range#RANGE.PlayerData
  player.playername="funkyfranky"
  player.airframe="F/A 18 Hornet"
  player.unitname="My Unit"
  
  range:__Impact(1, result, player)
  
end
  
testBomb()

local function testStrafe()

  local result = {} -- --Functional.Range#RANGE.BombResult
  result.command = SOCKET.DataType.STRAFERESULT
  result.name = "My Target"
  result.roundsFired=math.random(10, 300)
  result.roundsHit=math.random(result.roundsFired)
  result.strafeAccuracy=result.roundsHit/result.roundsFired*100
  result.roundsQuality = "Some Quality"
  result.player = "funkyfranky"
  result.time = timer.getAbsTime()
  result.clock = UTILS.SecondsToClock(result.time, true)
  result.midate=UTILS.GetDCSMissionDate()
  result.airframe = "F/A 18 Hornet"
  result.rangename = "My Test Range"
  result.theatre = env.mission.theatre

  env.info("FF Test bomb! Expect impact in 1 seconds..")
  
  local player={}--Functional.Range#RANGE.PlayerData
  player.playername="funkyfranky"
  player.airframe="F/A 18 Hornet"
  player.unitname="My Unit"
  
  range:__StrafeResult(1, player, result)
  
end

testStrafe()

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- AIRBOSS
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------

-- Create AIRBOSS object.
local airboss=AIRBOSS:New("CVN-74")

-- Enable FunkMan.
airboss:SetFunkManOn()

-- Start airboss class.
airboss:Start()

--- Function called when a player receives and LSO grade.
function airboss:OnAfterLSOGrade(From, Event, To, PlayerData, Grade)
  local playerData=PlayerData--Ops.Airboss#AIRBOSS.PlayerData
  local grade=Grade --Ops.Airboss#AIRBOSS.LSOGrade
  env.info("FF LSO grade incoming!")
end


local function testtrap()

  local playerData = {} --Ops.Airboss#AIRBOSS.PlayerData
  
  playerData.name="funkyfranky"
  playerData.airframe="FA-18C_hornet"
  playerData.callsign="My Callsign"
  playerData.Tgroove=15
  playerData.trapsheet={}
  playerData.wire=3
  playerData.case=1
  playerData.flag=1
  
  env.info("Trap sheet data")
  for i=1,150 do
    local ts={} --Ops.Airboss#AIRBOSS.GrooveData
    ts.Alt=170-i
    ts.AoA=math.random(7,10)
    ts.Gamma=50-i/10
    ts.Grade="Ok"
    ts.GSE=1.0
    ts.LUE=0.0+i/10
    ts.Z=200+i/2
    ts.X=-2700+i*25
    --BASE:I(ts)
    table.insert(playerData.trapsheet, ts)
  end
  
  local grade={} --Ops.Airboss#AIRBOSS.LSOgrade
  grade.airframe="FA-18C_hornet"
  grade.carriername="USS Stennis"
  grade.carriertype="CVN-74"
  grade.theatre=env.mission.theatre
  grade.carrierrwy=-9
  grade.case=1
  grade.points=2.5
  grade.details="(LUL)X (F)IM  LOLULIC LOLULAR"
  grade.grade="(OK)"
  grade.finalscore=2
  grade.Tgroove=15.1042432342334
  grade.midate=UTILS.GetDCSMissionDate()
  grade.mitime=UTILS.SecondsToClock(timer.getAbsTime(), true)
  grade.wire=3
  grade.wind=25.343421
  
  playerData.grade=grade
  
  env.info("FF Sending AIRBOSS LSO grade in 3 seconds!")
  
  airboss:__LSOGrade(3, playerData, grade)
  
end

testtrap()
