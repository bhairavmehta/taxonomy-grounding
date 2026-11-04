"""
generate_sample_b.py – synthetic "Sample B" dataset for the grounding trial and the viewer's Load results.

All reports are SYNTHETIC (template-generated, not real events). The dataset is built to exercise the
grounding checks: sibling categories, multi-label co-codes, a wrong proposed parent, a thin category,
an emerging category split across NAV and the OTHR holding pool, stage-2 labelling errors, and
background reports that belong to no candidate.

  python tools/generate_sample_b.py                 # writes data_sample_b/
  python tools/generate_sample_b.py --seed 11 --out data_sample_c
"""
import argparse
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# ---------------------------------------------------------------- vocabulary
TYPES = ["B737-800", "B737 MAX 8", "B787-9", "B777-300ER", "A320", "A321neo", "E175", "CRJ900", "B767-300F", "A330-300"]
ARPTS = ["a large hub airport", "a regional airport", "a coastal airport", "a high-elevation airport", "a busy international airport"]
RWYS = ["09L", "27R", "16", "34L", "04R", "22", "13", "31L", "18R", "36"]
TWYS = ["Alpha", "Bravo", "Charlie", "Delta", "Echo", "Kilo"]
TIMES = ["at night", "at dusk", "in daylight", "shortly after sunrise", "late in the evening"]
WX = ["in light rain", "with gusty winds", "in low visibility", "in clear conditions", "with a low overcast", "in light snow"]
FL = [180, 210, 240, 280, 310, 330, 350, 370]
CREW = ["The crew", "We", "The flight crew", "The captain and first officer"]


def P(rng, seq):
    return rng.choice(seq)


def abbreviate(text, rng, rate):
    """ASRS-style shorthand on a share of reports."""
    if rng.random() > rate:
        return text
    for a, b in [("runway", "rwy"), ("Runway", "Rwy"), ("taxiway", "twy"), ("approximately", "approx"),
                 ("feet", "ft"), ("air traffic control", "ATC"), ("first officer", "FO"), ("captain", "CAPT")]:
        text = text.replace(a, b)
    return text


# ---------------------------------------------------------------- candidates: (id, proposed parent, true parent, name, definition, codes, n, templates)
# each template is a function of rng returning a list of sentences
def t(*parts):
    return list(parts)


CANDIDATES = [
 ("B01", "RI", "RI", "Vehicle or pedestrian on the runway without clearance",
  "A ground vehicle, tug or person enters an active runway or its protected area without an ATC clearance.", ["RI"], 6,
  lambda r: t(f"A {P(r, ['snow removal truck', 'fuel truck', 'tug towing an aircraft', 'airport operations vehicle', 'maintenance worker on foot'])} entered Runway {P(r, RWYS)} without a clearance {P(r, TIMES)}.",
              f"{P(r, ['Landing traffic was sent around', 'An aircraft on its takeoff roll was told to stop', 'Departing traffic was held in position'])}.",
              f"The driver {P(r, ['said the radio was on the wrong frequency', 'misunderstood a hold-short instruction', 'did not see the runway guard lights'])}.")),
 ("B02", "RI", "RI", "Landing on a taxiway or the wrong runway at night",
  "At night or in low light the crew lines up on and lands, or nearly lands, on a taxiway or a runway other than the one assigned.", ["RI"], 5,
  lambda r: t(f"{P(r, CREW)} lined up on taxiway {P(r, TWYS)} {P(r, ['at night', 'in darkness', 'at dusk'])}, mistaking its lights for Runway {P(r, RWYS)}.",
              f"{P(r, ['Tower called a go-around at 300 feet', 'The aircraft landed on the taxiway, which was clear of traffic', 'The crew went around at about 150 feet after seeing aircraft on the taxiway'])}.",
              f"The approach lighting for the assigned runway was {P(r, ['partly out of service', 'set to a low intensity', 'hidden by a NOTAM nobody had briefed'])}.")),
 ("B03", "RE", "RE", "Veer-off during landing in a strong or gusty crosswind",
  "In a strong or gusty crosswind the aircraft drifts and veers off the side of the runway during the landing roll.", ["RE"], 6,
  lambda r: t(f"Landing on Runway {P(r, RWYS)} {P(r, ['with a 30-knot gusting crosswind', 'with a crosswind near the limit', 'in strong gusts from the left'])}, the {P(r, TYPES)} drifted toward the edge.",
              f"The aircraft veered off the {P(r, ['left', 'right'])} side of the runway {P(r, ['and stopped on the grass', 'and struck an edge light', 'before returning to the pavement'])}.",
              f"{P(r, ['There were no injuries', 'The nose gear was damaged', 'The runway was closed for two hours'])}.")),
 ("B04", "RE", "RE", "Overrun on a contaminated runway",
  "On a wet, slushy, snowy or icy runway braking is poor and the aircraft overruns the end of the runway.", ["RE"], 5,
  lambda r: t(f"The runway condition code was {P(r, ['2', '3', '1'])} {P(r, ['after freezing rain', 'with standing water', 'with compacted snow', 'with slush'])}.",
              f"Braking action was poor and the {P(r, TYPES)} overran the end of Runway {P(r, RWYS)} {P(r, ['by 40 metres', 'into the safety area', 'onto the grass'])}.",
              f"{P(r, ['The crew had not recomputed the landing distance', 'Autobrakes were set to a low setting', 'The touchdown was 1,500 feet long'])}.")),
 ("B05", "LOC-I", "LOC-I", "Stall warning or upset during a go-around",
  "During a go-around or missed approach the aircraft pitches up with high thrust, energy is mismanaged, and a stall warning or upset follows.", ["LOC-I"], 5,
  lambda r: t(f"{P(r, CREW)} initiated a go-around at {P(r, ['200', '500', '1,000'])} feet {P(r, WX)}.",
              f"With full thrust the pitch rose to {P(r, ['20', '25', '28'])} degrees and the speed decayed until the stick shaker activated.",
              f"{P(r, ['The captain lowered the nose and recovered', 'The aircraft rolled to 35 degrees of bank before recovery', 'The autopilot had disconnected without the crew noticing'])}.")),
 ("B06", "TURB", "TURB", "Wake turbulence upset on approach",
  "Wake vortices from a preceding heavier aircraft cause a sudden roll or pitch upset on approach or departure.", ["TURB"], 5,
  lambda r: t(f"On final approach {P(r, ['3 miles', '5 miles', '6 miles'])} behind a {P(r, ['B777', 'A380', 'B747', 'heavy aircraft'])}, the {P(r, TYPES)} encountered wake turbulence.",
              f"The aircraft rolled {P(r, ['25', '30', '40'])} degrees to the {P(r, ['left', 'right'])} before the crew recovered.",
              f"{P(r, ['Spacing had been reduced by ATC', 'Winds were light and calm', 'The crew had flown below the glide path of the heavy aircraft'])}.")),
 ("B07", "MAC", "MAC", "Loss of separation caused by an ATC clearance",
  "A controller clearance or instruction puts two aircraft into conflict, leading to loss of separation or a TCAS alert.", ["MAC", "ATM"], 5,
  lambda r: t(f"The controller cleared the {P(r, TYPES)} to {P(r, ['descend', 'climb', 'turn left'])} into conflicting traffic at FL{P(r, FL)}.",
              f"{P(r, ['Separation was lost', 'Both aircraft received TCAS resolution advisories', 'The closest point was 1.2 miles and 400 feet'])}.",
              f"{P(r, ['The sector was very busy', 'There was a handover between controllers', 'A similar call sign was on the frequency'])}.")),
 ("B08", "MAC", "MAC", "TCAS resolution advisory after a level bust",
  "The aircraft climbs or descends through its cleared altitude (level bust) and a TCAS resolution advisory follows.", ["MAC"], 5,
  lambda r: t(f"{P(r, CREW)} climbed through the cleared altitude of FL{P(r, FL)} by {P(r, ['300', '500', '700'])} feet.",
              f"Traffic {P(r, ['above', 'ahead', 'crossing'])} triggered a TCAS resolution advisory to {P(r, ['descend', 'level off', 'climb'])}.",
              f"{P(r, ['The wrong altitude had been set in the mode control panel', 'The autopilot did not capture the altitude', 'The FO was busy with a checklist'])}.")),
 ("B09", "SCF-NP", "SCF-NP", "Hydraulic system failure in flight",
  "Loss of fluid or pressure in a hydraulic system in flight degrades flight controls, brakes or landing gear.", ["SCF-NP"], 6,
  lambda r: t(f"At FL{P(r, FL)} the {P(r, ['A', 'B', 'green', 'left'])} hydraulic system quantity dropped to zero.",
              f"{P(r, CREW)} ran the hydraulic loss checklist and {P(r, ['diverted', 'returned to the departure airport', 'continued to the destination'])}.",
              f"{P(r, ['The gear was extended by gravity', 'Landing distance was longer because of reduced braking', 'A hydraulic line had chafed through'])}.")),
 ("B10", "SCF-NP", "SCF-NP", "Landing gear did not extend",
  "One or more landing gear legs fail to extend or lock down, requiring alternate extension or a gear-up landing.", ["SCF-NP"], 5,
  lambda r: t(f"On approach the {P(r, ['nose gear', 'left main gear', 'right main gear'])} showed unsafe with no green light.",
              f"The alternate gear extension {P(r, ['worked on the second attempt', 'did not lock the gear', 'was used and the gear locked down'])}.",
              f"{P(r, ['A tower flyby confirmed the gear position', 'The aircraft landed with emergency services standing by', 'A damaged downlock actuator was found'])}.")),
 ("B11", "CFIT", "CFIT", "Terrain warning on a non-precision approach",
  "During a non-precision or visual approach the aircraft descends too low and the terrain awareness system warns of terrain or obstacles.", ["CFIT"], 5,
  lambda r: t(f"Flying a {P(r, ['VOR', 'RNAV', 'NDB', 'visual'])} approach {P(r, TIMES)} {P(r, WX)}, the aircraft descended below the minimum altitude.",
              f"The terrain awareness system called {P(r, ['TERRAIN, PULL UP', 'TOO LOW TERRAIN', 'SINK RATE'])} and the crew climbed away.",
              f"{P(r, ['The altimeter setting had been entered wrongly', 'The crew had started the descent too early', 'The final approach fix was misidentified'])}.")),
 ("B12", "NAV", "NAV", "GNSS interference or spoofing",
  "Satellite navigation signals are jammed or spoofed, giving false position, lost RNP capability or incorrect time, often near conflict zones.", ["NAV"], 5,
  lambda r: t(f"{P(r, ['Over the eastern Mediterranean', 'Near the Black Sea', 'On a route near a conflict area', 'Approaching the region'])} both GPS receivers {P(r, ['lost signal', 'showed a position 40 miles in error', 'reported a different time'])}.",
              f"{P(r, ['RNP approaches were no longer available', 'A false terrain warning followed', 'ATC provided radar vectors'])}.",
              f"{P(r, ['The crew reverted to conventional navigation', 'Several other aircraft reported the same problem', 'The position errors stopped after 20 minutes'])}.")),
 ("B13", "SCF-NP", "SCF-PP", "Engine shutdown after loss of oil pressure",
  "Low oil pressure or oil loss in flight leads the crew to shut an engine down as a precaution.", ["SCF-PP"], 4,
  lambda r: t(f"At FL{P(r, FL)} the {P(r, ['left', 'right', 'number 2'])} engine oil pressure fell below the limit.",
              f"{P(r, CREW)} shut the engine down and {P(r, ['diverted', 'declared an emergency', 'returned'])}.",
              f"{P(r, ['A loose oil line fitting was found', 'The oil filter was found clogged', 'Oil had leaked from a cracked seal'])}.")),
 ("B14", "ICE", "ICE", "Takeoff with frost or ice not removed",
  "The aircraft departs or begins to depart with frost, snow or ice on its wings because it was not removed or the fluid failed.", ["ICE"], 2,
  lambda r: t(f"After a long taxi in {P(r, ['freezing fog', 'light snow'])}, a passenger reported ice on the wing.",
              f"{P(r, CREW)} {P(r, ['returned for de-icing', 'had already started the takeoff roll and rejected the takeoff'])}.")),
 # ---- added set: B15-B28
 ("B15", "BIRD", "BIRD", "Bird ingestion damaging an engine on takeoff or climb",
  "One or more birds are ingested into an engine during takeoff or initial climb, causing vibration, surging or loss of thrust.", ["BIRD", "SCF-PP"], 5,
  lambda r: t(f"Passing {P(r, ['400', '800', '1,500'])} feet after takeoff from {P(r, ARPTS)}, the {P(r, TYPES)} flew through a flock of {P(r, ['geese', 'gulls', 'starlings'])}.",
              f"The {P(r, ['left', 'right', 'number 1'])} engine {P(r, ['surged with loud bangs', 'showed high vibration', 'lost thrust'])} after ingesting birds.",
              f"{P(r, CREW)} {P(r, ['returned to land', 'shut the engine down and returned', 'declared an emergency and landed overweight'])}.",
              f"{P(r, ['Several fan blades were bent', 'Bird remains were found in the engine core', 'The engine was replaced'])}.")),
 ("B16", "BIRD", "BIRD", "Bird strike damaging the windshield or nose on approach",
  "A large bird or flock strikes the windshield, radome or nose on approach or descent and causes visible damage.", ["BIRD"], 5,
  lambda r: t(f"On descent through {P(r, ['3,000', '5,000', '7,000'])} feet a large {P(r, ['eagle', 'goose', 'vulture', 'pelican'])} struck the {P(r, ['windshield', 'radome', 'nose'])}.",
              f"{P(r, ['The outer windshield pane cracked', 'The radome was dented and holed', 'Blood and feathers covered the windshield'])}.",
              f"{P(r, CREW)} continued the approach {P(r, ['and landed without further problems', 'with the FO flying', 'after declaring an emergency'])}.")),
 ("B17", "F-NI", "F-NI", "Lithium battery fire from a passenger device",
  "A phone, laptop, power bank or other lithium battery device overheats, smokes or catches fire in the cabin.", ["F-NI", "CABIN"], 5,
  lambda r: t(f"A passenger's {P(r, ['power bank', 'phone', 'laptop', 'e-cigarette'])} {P(r, ['caught fire', 'began smoking', 'overheated'])} {P(r, ['in a seat pocket', 'in the overhead bin', 'after being crushed in a seat mechanism'])}.",
              f"Cabin crew {P(r, ['used a halon extinguisher and then water', 'put the device in a containment bag', 'cooled the device with water'])}.",
              f"{P(r, ['The aircraft diverted', 'Two passengers were treated for smoke inhalation', 'The flight continued after the device cooled'])}.")),
 ("B18", "F-NI", "F-NI", "Electrical smoke or burning smell in the flight deck",
  "Smoke, fumes or a burning electrical smell appears in the flight deck, often traced to wiring, a display or a window heater.", ["F-NI", "SCF-NP"], 5,
  lambda r: t(f"During {P(r, ['cruise', 'climb', 'descent'])} at FL{P(r, FL)} {P(r, CREW).lower()} noticed {P(r, ['smoke', 'an electrical burning smell', 'haze'])} in the flight deck.",
              f"{P(r, CREW)} donned oxygen masks and ran the smoke checklist.",
              f"The source was {P(r, ['an overheated window heat connector', 'a failed display unit', 'chafed wiring behind a panel'])}.",
              f"{P(r, ['The aircraft diverted', 'The smoke cleared after the bus was isolated', 'An emergency landing was made'])}.")),
 ("B19", "FUEL", "FUEL", "Low fuel after holding or a diversion",
  "Extended holding, a missed approach or a diversion leaves the aircraft close to or below final reserve fuel, and the crew declares minimum fuel or a fuel emergency.", ["FUEL"], 5,
  lambda r: t(f"After {P(r, ['40 minutes of holding', 'two missed approaches', 'a diversion to a busy alternate'])} {P(r, WX)}, fuel dropped toward final reserve.",
              f"{P(r, CREW)} declared {P(r, ['minimum fuel', 'MAYDAY FUEL', 'a fuel emergency'])} and received priority.",
              f"The aircraft landed with {P(r, ['1,100', '1,400', '900'])} kg remaining, {P(r, ['below final reserve', 'just above final reserve'])}.")),
 ("B20", "RAMP", "RAMP", "Pushback or towing collision",
  "During pushback or towing the tug, towbar or aircraft strikes another aircraft, a vehicle or a fixed object.", ["RAMP"], 5,
  lambda r: t(f"During pushback from the gate the {P(r, TYPES)} {P(r, ['wing tip struck a parked aircraft', 'tail struck a light pole', 'struck a baggage cart'])}.",
              f"{P(r, ['The wing walker was not in position', 'The tug driver could not see the wing tip', 'The towbar shear pin failed'])}.",
              f"{P(r, ['The flight was cancelled', 'The aircraft was inspected and found damaged', 'Both aircraft were taken out of service'])}.")),
 ("B21", "CABIN", "CABIN", "Disruptive or unruly passenger",
  "A passenger is aggressive, intoxicated or refuses crew instructions, interfering with the crew or other passengers.", ["CABIN"], 5,
  lambda r: t(f"A {P(r, ['intoxicated', 'aggressive', 'agitated'])} passenger {P(r, ['refused to follow crew instructions', 'shouted at cabin crew', 'tried to open a door'])} during the flight.",
              f"Cabin crew {P(r, ['restrained the passenger with help from others', 'moved the passenger to another seat', 'informed the captain'])}.",
              f"{P(r, ['Police met the aircraft on arrival', 'The aircraft diverted to offload the passenger', 'A report was filed with the authorities'])}.")),
 ("B22", "ARC", "ARC", "Tail strike on takeoff",
  "The tail strikes the runway during takeoff rotation, often after early or fast rotation or a wrong takeoff speed or weight.", ["ARC"], 5,
  lambda r: t(f"During rotation on Runway {P(r, RWYS)} the tail of the {P(r, TYPES)} struck the runway.",
              f"{P(r, ['The takeoff speeds had been computed with the wrong weight', 'The pilot flying rotated early and fast', 'A gust raised the pitch rate'])}.",
              f"{P(r, CREW)} {P(r, ['returned to land', 'did not pressurize and returned', 'continued after the tail strike light went out'])}.")),
 ("B23", "TURB", "WSTRW", "Windshear on final approach",
  "A sudden change in wind speed or direction on approach, often near a thunderstorm or microburst, causes loss of airspeed and a windshear warning.", ["WSTRW"], 5,
  lambda r: t(f"On short final {P(r, ['near a thunderstorm', 'with a microburst reported', 'in gusty conditions'])} the airspeed dropped by {P(r, ['20', '25', '30'])} knots.",
              f"The {P(r, ['predictive windshear', 'reactive windshear'])} warning sounded and {P(r, CREW).lower()} flew the windshear escape manoeuvre.",
              f"{P(r, ['The aircraft lost 300 feet before climbing', 'The crew diverted to the alternate', 'A second approach was flown after the storm passed'])}.")),
 ("B24", "USOS", "USOS", "Landing short of the runway",
  "The aircraft touches down before the runway threshold, on the approach lights or in the undershoot area.", ["USOS"], 4,
  lambda r: t(f"On a {P(r, ['visual', 'RNAV', 'non-precision'])} approach {P(r, TIMES)} the {P(r, TYPES)} touched down {P(r, ['in the grass', 'on the approach lights', '50 metres'])} short of the threshold of Runway {P(r, RWYS)}.",
              f"{P(r, ['The aircraft was below the glide path for the last mile', 'A black-hole illusion made the approach look high', 'The crew misjudged the flare in a tailwind'])}.",
              f"{P(r, ['The main gear was damaged', 'Several approach lights were broken', 'There were no injuries'])}.")),
 ("B25", "ICE", "ICE", "Airframe icing in flight",
  "Ice builds on the wings, tail or windshield in flight in icing conditions, degrading performance or handling.", ["ICE"], 4,
  lambda r: t(f"Holding at {P(r, ['8,000', '10,000', '12,000'])} feet in {P(r, ['freezing drizzle', 'icing conditions', 'supercooled cloud'])}, ice built up on the wings faster than expected.",
              f"{P(r, ['The anti-ice system could not keep up', 'Airspeed decayed and more power was needed', 'The windshield iced over'])}.",
              f"{P(r, CREW)} {P(r, ['requested a lower altitude', 'left the icing area', 'increased the approach speed'])}.")),
 ("B26", "SCF-NP", "SCF-NP", "Unreliable airspeed from blocked pitot probes",
  "Pitot probes blocked by ice, insects or covers give wrong airspeed indications, leading to warnings and autopilot disconnection.", ["SCF-NP"], 5,
  lambda r: t(f"{P(r, ['During the takeoff roll', 'In cruise at FL350', 'On climb-out'])} the captain's and first officer's airspeeds disagreed by {P(r, ['30', '40', '60'])} knots.",
              f"{P(r, ['The autopilot disconnected', 'An IAS DISAGREE alert appeared', 'The stall warning sounded falsely'])} and {P(r, CREW).lower()} flew pitch and power.",
              f"{P(r, ['A wasp nest was found in a pitot probe', 'A pitot cover had been left on', 'Ice crystals had blocked the probes'])}.")),
 ("B27", "RI", "RI", "Crew crossed a hold-short line without clearance",
  "The flight crew taxis past a runway hold-short line without a clearance to enter or cross the runway (pilot deviation).", ["RI"], 5,
  lambda r: t(f"Taxiing on taxiway {P(r, TWYS)} {P(r, TIMES)}, {P(r, CREW).lower()} crossed the hold-short line for Runway {P(r, RWYS)} without a clearance.",
              f"{P(r, ['The FO was head-down programming the FMS', 'The crew read back hold short but did not stop', 'The airport diagram had not been briefed'])}.",
              f"{P(r, ['An aircraft on approach went around', 'Tower told the crew to stop', 'No conflict occurred'])}.")),
 ("B28", "NAV", "NAV", "Wrong route or waypoint loaded in the FMS",
  "The flight management system is loaded with the wrong route, waypoint or departure, and the aircraft deviates from its cleared route.", ["NAV"], 3,
  lambda r: t(f"After departure the aircraft turned toward the wrong waypoint because {P(r, ['an old route was loaded', 'a similar-named waypoint was selected', 'the wrong departure procedure was entered'])}.",
              f"ATC noticed the deviation and {P(r, ['gave a heading', 'asked the crew to check their route'])}.")),
]

# label noise: (candidate id, index of report, wrong stage-2 codes)
LABEL_ERRORS = [("B06", 4, ["LOC-I"]), ("B03", 5, ["RE", "ARC"]), ("B12", 2, ["OTHR"]), ("B12", 4, ["OTHR"]),
                ("B23", 2, ["TURB"]), ("B26", 1, ["LOC-I"]), ("B28", 2, ["OTHR"]), ("B16", 3, ["OTHR"])]
THIN = {"B14", "B28"}   # kept small whatever --scale is

BACKGROUND = [
 (["BIRD"], lambda r: t(f"A bird struck the {P(r, ['radome', 'windshield', 'left wing leading edge'])} during the approach.", "No damage was found on inspection.")),
 (["RAMP"], lambda r: t(f"A {P(r, ['baggage loader', 'catering truck', 'belt loader'])} struck the {P(r, ['cargo door', 'fuselage', 'wing tip'])} at the gate.", "The aircraft was taken out of service for inspection.")),
 (["CABIN"], lambda r: t(f"A passenger {P(r, ['fainted', 'had a seizure', 'reported chest pain'])} during cruise.", "Cabin crew provided first aid and medical services met the aircraft.")),
 (["F-NI"], lambda r: t(f"Smoke came from a {P(r, ['galley oven', 'coffee maker', 'lavatory light'])} during cruise.", "Cabin crew turned off the power and the smoke cleared.")),
 (["ATM"], lambda r: t(f"Frequency congestion delayed the {P(r, ['descent clearance', 'handover', 'approach clearance'])}.", "The crew had to request the clearance several times.")),
 (["FUEL"], lambda r: t(f"A fuel imbalance of {P(r, ['900', '1,200', '1,500'])} kg developed during cruise.", "The crew followed the fuel imbalance checklist and found no leak.")),
 (["ARC"], lambda r: t(f"The {P(r, TYPES)} touched down hard after a late flare.", "A hard landing inspection was carried out.")),
 (["RE"], lambda r: t(f"A rejected takeoff at {P(r, ['80', '110', '125'])} knots was carried out for a {P(r, ['configuration warning', 'bird strike warning', 'master caution'])}.", "The aircraft stopped on the runway with hot brakes.")),
 (["RI", "ATM"], lambda r: t(f"An aircraft taxied across Runway {P(r, RWYS)} after being cleared to cross a different runway.", "No other aircraft were nearby.")),
 (["TURB", "CABIN"], lambda r: t(f"Moderate turbulence at FL{P(r, FL)} spilled drinks in the cabin.", "There were no injuries.")),
 (["SCF-NP"], lambda r: t(f"The cabin altitude rose to {P(r, ['9,000', '10,000'])} feet when a pressurization controller failed.", "The crew descended and the cabin altitude returned to normal.")),
 (["SCF-PP"], lambda r: t(f"An engine vibration advisory appeared at FL{P(r, FL)}.", "The vibration stayed within limits and the flight continued.")),
 (["MAC"], lambda r: t(f"A TCAS traffic advisory was received for VFR traffic {P(r, ['500', '700'])} feet below.", "No resolution advisory followed and the traffic passed clear.")),
 (["LOC-I"], lambda r: t(f"The autopilot disconnected briefly in light chop at FL{P(r, FL)}.", f"{P(r, CREW)} re-engaged it {P(r, ['without any deviation', 'within a few seconds', 'after checking the flight controls'])}.")),
 (["RAMP"], lambda r: t(f"Foreign object debris was found on the apron near gate {P(r, ['12', '21', '34'])}.", "The area was swept before the next arrival.")),
 (["FUEL", "RAMP"], lambda r: t(f"Fuel spilled from the {P(r, ['left', 'right'])} wing vent during refuelling at gate {P(r, ['5', '14', '22', '31'])}.", f"{P(r, ['The fire service covered the spill', 'Passengers were kept on the bridge', 'The refuelling was stopped'])} and the aircraft was refuelled again.")),
 (["ICE"], lambda r: t(f"De-icing took {P(r, ['35', '50'])} minutes because of a queue at the pad.", "The holdover time was checked again before departure.")),
 (["CABIN"], lambda r: t(f"A passenger was found smoking {P(r, ['in the forward lavatory', 'in the aft lavatory', 'an e-cigarette in the lavatory'])}.", f"Cabin crew {P(r, ['checked the waste bin and found no fire', 'reported it to the captain', 'gave a formal warning'])}.")),
 (["WSTRW"], lambda r: t(f"A windshear alert was broadcast by the tower for Runway {P(r, RWYS)}.", f"The approach was flown {P(r, ['normally with no windshear encountered', 'with extra speed but no windshear was met', 'to the other runway without problems'])}.")),
 (["NAV"], lambda r: t(f"The FMS {P(r, ['lost its navigation database', 'showed an expired database', 'froze'])} during preflight and had to be reloaded.", f"The departure was delayed by {P(r, ['15', '20', '40'])} minutes.")),
]

PARENTS_EXTRA = [
 {"code": "RAMP", "name": "Ground Handling", "in_scope": True, "definition": "Occurrences during ground handling operations, such as servicing, loading and towing, including damage from ground equipment."},
 {"code": "F-NI", "name": "Fire/Smoke (Non-Impact)", "in_scope": True, "definition": "Fire or smoke in or on the aircraft, in flight or on the ground, not resulting from an impact."},
 {"code": "FUEL", "name": "Fuel Related", "in_scope": True, "definition": "Occurrences related to fuel quantity, imbalance, contamination or fuel system management."},
 {"code": "WSTRW", "name": "Windshear or Thunderstorm", "in_scope": True, "definition": "Flight into windshear or thunderstorm, including microbursts, sudden wind changes and associated loss of airspeed or altitude."},
 {"code": "USOS", "name": "Undershoot/Overshoot", "in_scope": True, "definition": "A touchdown off the runway surface before the threshold (undershoot) or a landing beyond the runway end that is not an excursion during the roll."},
 {"code": "OTHR", "name": "Other", "in_scope": False, "definition": "Occurrences that do not fit any other category; a holding pool for emerging issues."},
]

DEFS_EXTRA = [
 {"id": "IND-19", "source": "FAA Runway Safety programme", "term": "Vehicle or pedestrian deviation", "parents": ["RI"], "text": "A runway incursion caused by a ground vehicle or a person, such as a driver or pedestrian entering a runway without ATC authorization."},
 {"id": "IND-20", "source": "SKYbrary – Crosswind Landings", "term": "Crosswind landing", "parents": ["RE"], "text": "Landing with a wind component across the runway; strong or gusty crosswinds near the aircraft limit increase the risk of lateral runway excursion (veer-off)."},
 {"id": "IND-21", "source": "FAA Advisory Circular 120-109A – Stall Prevention and Recovery Training", "term": "Stall prevention and recovery", "parents": ["LOC-I"], "text": "Training to recognise and recover from approaches to stall and full stalls, including during go-arounds with high thrust and pitch."},
 {"id": "IND-22", "source": "FAA Advisory Circular 90-23G – Aircraft Wake Turbulence", "term": "Wake turbulence", "parents": ["TURB"], "text": "Vortices from a preceding aircraft, strongest behind heavy aircraft at slow speed, can cause sudden rolls on approach or departure; spacing reduces the risk."},
 {"id": "IND-23", "source": "ICAO Doc 4444 – PANS-ATM (separation minima)", "term": "Loss of separation", "parents": ["MAC", "ATM"], "text": "Two aircraft come closer than the prescribed separation minima, often after an ATC clearance or instruction puts them in conflict."},
 {"id": "IND-24", "source": "SKYbrary – Hydraulic System Failure", "term": "Hydraulic system failure", "parents": ["SCF-NP"], "text": "Loss of hydraulic fluid or pressure that degrades flight controls, brakes, steering or landing gear, handled with non-normal checklists."},
 {"id": "IND-25", "source": "SKYbrary – Landing Gear Malfunction", "term": "Landing gear malfunction", "parents": ["SCF-NP"], "text": "Failure of a landing gear leg to extend, retract or lock, requiring alternate extension or a landing with gear not fully down."},
 {"id": "IND-26", "source": "14 CFR 121.354 – Terrain awareness and warning system", "term": "Terrain awareness and warning system (TAWS)", "parents": ["CFIT"], "text": "Airliners must carry a system that warns the crew of terrain, obstacles and excessive descent so they can climb away before impact."},
 {"id": "IND-27", "source": "EASA Safety Information Bulletin 2022-02 – GNSS outages and alterations", "term": "GNSS jamming and spoofing", "parents": ["NAV"], "text": "Interference with satellite navigation signals, by jamming or spoofing, causes loss of GPS position, false positions or false terrain warnings, especially near conflict zones."},
 {"id": "IND-28", "source": "SKYbrary – In-Flight Shutdown", "term": "In-flight engine shutdown (IFSD)", "parents": ["SCF-PP"], "text": "An engine is shut down in flight because of a failure or a precautionary indication such as low oil pressure, high vibration or fire."},
 {"id": "IND-29", "source": "FAA Advisory Circular 120-60B – Ground Deicing and Anti-icing Program", "term": "Clean aircraft concept", "parents": ["ICE"], "text": "No takeoff may be made with frost, ice or snow adhering to wings or control surfaces; contamination must be removed before departure."},
 {"id": "IND-30", "source": "ICAO Doc 10117 – Manual on the Legal Aspects of Unruly and Disruptive Passengers", "term": "Unruly or disruptive passenger", "parents": ["CABIN"], "text": "A passenger who fails to respect rules of conduct or to follow crew instructions, disturbing good order and discipline on board."},
 {"id": "IND-31", "source": "FAA SAFO – Fire risks from lithium batteries in the cabin", "term": "Lithium battery fire", "parents": ["F-NI", "CABIN"], "text": "Portable electronic devices and power banks can overheat in thermal runaway, producing smoke and fire in the cabin; crew cool the device with water or non-alcoholic liquid."},
 {"id": "IND-32", "source": "SKYbrary – Smoke and Fumes", "term": "Smoke or fumes in flight", "parents": ["F-NI"], "text": "Smoke, fumes or burning smells in the flight deck or cabin, often electrical in origin, handled with oxygen masks and the smoke checklist."},
 {"id": "IND-33", "source": "ICAO Annex 6 – Fuel planning and in-flight fuel management", "term": "Minimum fuel and fuel emergency", "parents": ["FUEL"], "text": "The crew declares MINIMUM FUEL when any change may land them below final reserve, and MAYDAY FUEL when the landing fuel is expected to be below final reserve."},
 {"id": "IND-34", "source": "IATA Ground Operations Manual – Pushback and towing", "term": "Pushback and towing", "parents": ["RAMP"], "text": "Moving an aircraft with a tug or towbar, with wing walkers and headset communication, to prevent collisions with aircraft, vehicles and objects."},
 {"id": "IND-35", "source": "SKYbrary – Tailstrike", "term": "Tail strike", "parents": ["ARC"], "text": "The aft fuselage contacts the runway during takeoff rotation or landing, often after early rotation, wrong takeoff speeds or excessive pitch."},
 {"id": "IND-36", "source": "FAA Advisory Circular 00-54 – Pilot Windshear Guide", "term": "Low-level windshear", "parents": ["WSTRW"], "text": "Sudden changes in wind speed or direction near the ground, such as microbursts from thunderstorms, causing airspeed loss; crews fly the windshear escape manoeuvre."},
 {"id": "IND-37", "source": "SKYbrary – Landing Short (Undershoot)", "term": "Undershoot", "parents": ["USOS"], "text": "The aircraft touches down before the runway threshold, often after an unstable or low approach or a visual illusion."},
 {"id": "IND-38", "source": "FAA Advisory Circular 91-74B – Pilot Guide: Flight in Icing Conditions", "term": "In-flight airframe icing", "parents": ["ICE"], "text": "Ice accumulates on wings, tail and windshield in supercooled cloud or freezing drizzle, increasing drag and stall speed."},
 {"id": "IND-39", "source": "FAA National Wildlife Strike Database – strike reporting", "term": "Damaging bird strike", "parents": ["BIRD"], "text": "A collision with birds that damages the aircraft, such as a cracked windshield, dented radome or ingested engine, reported to the wildlife strike database."},
 {"id": "IND-40", "source": "FAA Runway Safety programme – Pilot deviation", "term": "Pilot deviation (runway incursion)", "parents": ["RI"], "text": "A runway incursion caused by a pilot, such as crossing a hold-short line or entering a runway without an ATC clearance."},
 {"id": "IND-41", "source": "SKYbrary – Lateral Navigation Error", "term": "Lateral navigation error", "parents": ["NAV"], "text": "The aircraft leaves its cleared route because of a wrong route, waypoint or procedure loaded in the flight management system."},
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--background", type=int, default=60)
    ap.add_argument("--scale", type=float, default=1.6, help="multiply the reports per candidate (thin candidates stay thin)")
    ap.add_argument("--abbrev-rate", type=float, default=0.3)
    ap.add_argument("--out", default=str(ROOT / "data_sample_b"))
    a = ap.parse_args()
    rng = random.Random(a.seed)
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)

    parents = json.loads((ROOT / "data" / "icao_categories.json").read_text())["categories"] + PARENTS_EXTRA
    defs = json.loads((ROOT / "data" / "industry_definitions.json").read_text())["definitions"] + DEFS_EXTRA

    reports, cands, n, seen = [], [], 0, set()
    phase = {"B01": "Taxi", "B02": "Approach", "B03": "Landing", "B04": "Landing", "B05": "Go-around", "B06": "Approach", "B07": "Cruise",
             "B08": "Climb", "B09": "Cruise", "B10": "Approach", "B11": "Approach", "B12": "Cruise", "B13": "Cruise", "B14": "Ground",
             "B15": "Climb", "B16": "Descent", "B17": "Cruise", "B18": "Cruise", "B19": "Approach", "B20": "Pushback", "B21": "Cruise",
             "B22": "Takeoff", "B23": "Approach", "B24": "Landing", "B25": "Approach", "B26": "Cruise", "B27": "Taxi", "B28": "Departure"}
    errs = {(c, i): codes for c, i, codes in LABEL_ERRORS}
    for cid, prop, true, name, definition, codes, k, tpl in CANDIDATES:
        keys = []
        if cid not in THIN:
            k = max(k, round(k * a.scale))
        for i in range(k):
            n += 1
            key = f"SYNB-{n:03d}"
            for _ in range(30):   # avoid word-for-word duplicates
                text = abbreviate(" ".join(tpl(rng)), rng, a.abbrev_rate)
                if text not in seen:
                    break
            seen.add(text)
            reports.append({"report_key": key, "source_id": "SYNTHETIC-B", "phase": phase[cid], "l1_codes": errs.get((cid, i), codes),
                            "source_codes": "", "narrative": text, "_truth": cid})
            keys.append(key)
        cands.append({"candidate_id": cid, "proposed_parent": prop, "expected_parent": true, "name": name, "definition": definition, "expected_reports": keys})
    for j in range(a.background):
        n += 1
        codes, tpl = BACKGROUND[j % len(BACKGROUND)]
        for _ in range(30):
            text = abbreviate(" ".join(tpl(rng)), rng, a.abbrev_rate)
            if text not in seen:
                break
        seen.add(text)
        reports.append({"report_key": f"SYNB-{n:03d}", "source_id": "SYNTHETIC-B", "phase": "Various", "l1_codes": codes,
                        "source_codes": "", "narrative": text, "_truth": "background"})
    rng.shuffle(reports)

    note = ("SYNTHETIC Sample B, template-generated for testing the grounding trial and viewer. Not real events. "
            "l1_codes are stage-2 assignments and include deliberate labelling errors; _truth is the generating candidate (answer key).")
    json.dump({"_note": note, "reports": reports}, open(out / "sample_reports.json", "w"), indent=1)
    json.dump({"_note": "Candidates for Sample B. B13 and B23 are proposed under the wrong parent; B14 and B28 are too thin; B12 is an emerging category; B15/B16 and B01/B02/B27 are siblings; B15, B17, B18 are multi-coded.", "candidates": cands},
              open(out / "candidates.json", "w"), indent=1)
    json.dump({"_note": "CICTT parents (paraphrased) plus RAMP, F-NI, FUEL, WSTRW, USOS and the OTHR holding pool.", "categories": parents}, open(out / "icao_categories.json", "w"), indent=1)
    json.dump({"_note": "Industry definitions (paraphrased) with crosswalk; IND-19 to IND-41 added for Sample B.", "definitions": defs}, open(out / "industry_definitions.json", "w"), indent=1)
    print(f"Sample B: {len(reports)} reports ({len(reports) - a.background} candidate reports, {a.background} background), "
          f"{len(cands)} candidates, {len(parents)} parents, {len(defs)} definitions -> {out}")


if __name__ == "__main__":
    main()
