# Grounding cards – run-20261103-143214

Embedder: local-lsa (64 dims). Sample reports are synthetic.

## B01 Vehicle or pedestrian on the runway without clearance  –  GROUNDED

*Candidate definition:* A ground vehicle, tug or person enters an active runway or its protected area without an ATC clearance.

**ICAO parent:** RI – Runway Incursion (proposed by discovery: RI; parent scores {'RI': 0.779, 'RE': 0.212, 'ARC': 0.085, 'RAMP': 0.075}; agreement 74%)

*Reports given to a better-matching sibling:* SYNB-208 → B27, SYNB-210 → B27, SYNB-012 → B02, SYNB-206 → B27, SYNB-205 → B27

**Industry definitions:**
- IND-19 – Vehicle or pedestrian deviation (FAA Runway Safety programme)
- IND-04 – Anomaly: Ground Incursion – Runway or Taxiway (NASA ASRS coding taxonomy)
- IND-40 – Pilot deviation (runway incursion) (FAA Runway Safety programme – Pilot deviation)

**Supporting reports:**
- SYNB-010 [RI]: "A airport operations vehicle entered Runway 18R without a clearance shortly after sunrise."
- SYNB-005 [RI]: "A fuel truck entered Runway 36 without a clearance at night."
- SYNB-007 [RI]: "A maintenance worker on foot entered Runway 27R without a clearance late in the evening."
- SYNB-002 [RI]: "A maintenance worker on foot entered Runway 27R without a clearance in daylight."
- SYNB-009 [RI]: "A snow removal truck entered Runway 18R without a clearance at night."
- SYNB-001 [RI]: "A tug towing an aircraft entered Rwy 16 without a clearance shortly after sunrise."
- SYNB-006 [RI]: "A fuel truck entered Runway 09L without a clearance late in the evening."

**Checks:** G1 pass · G2 pass · G3 pass · G4 pass · G5 pass · G6 pass · G7 pass · G8 pass

## B02 Landing on a taxiway or the wrong runway at night  –  GROUNDED

*Candidate definition:* At night or in low light the crew lines up on and lands, or nearly lands, on a taxiway or a runway other than the one assigned.

**ICAO parent:** RI – Runway Incursion (proposed by discovery: RI; parent scores {'RI': 0.725, 'RE': 0.183, 'USOS': 0.127, 'ARC': 0.118}; agreement 93%)

*Reports given to a better-matching sibling:* SYNB-206 → B27, SYNB-210 → B27, SYNB-209 → B27, SYNB-205 → B27, SYNB-208 → B27

**Industry definitions:**
- IND-03 – Wrong-surface event (FAA Runway Safety programme)
- IND-04 – Anomaly: Ground Incursion – Runway or Taxiway (NASA ASRS coding taxonomy)

**Supporting reports:**
- SYNB-012 [RI]: "The crew lined up on taxiway Echo in darkness, mistaking its lights for Runway 18R."
- SYNB-016 [RI]: "The captain and first officer lined up on taxiway Alpha at night, mistaking its lights for Runway 04R."
- SYNB-017 [RI]: "The crew lined up on taxiway Kilo at dusk, mistaking its lights for Runway 04R."
- SYNB-015 [RI]: "The flight crew lined up on taxiway Charlie at dusk, mistaking its lights for Runway 22."
- SYNB-011 [RI]: "The captain and first officer lined up on taxiway Charlie in darkness, mistaking its lights for Runway 34L."
- SYNB-013 [RI]: "The flight crew lined up on twy Echo at night, mistaking its lights for Rwy 27R."
- SYNB-014 [RI]: "The flight crew lined up on twy Bravo in darkness, mistaking its lights for Rwy 13."

**Checks:** G1 pass · G2 pass · G3 pass · G4 pass · G5 pass · G6 pass · G7 pass · G8 pass

## B03 Veer-off during landing in a strong or gusty crosswind  –  GROUNDED

*Candidate definition:* In a strong or gusty crosswind the aircraft drifts and veers off the side of the runway during the landing roll.

**ICAO parent:** RE – Runway Excursion (proposed by discovery: RE; parent scores {'RE': 0.944, 'USOS': 0.25, 'ARC': 0.217, 'RAMP': 0.054}; agreement 100%)

**Industry definitions:**
- IND-20 – Crosswind landing (SKYbrary – Crosswind Landings)
- IND-05 – Runway excursion (veer-off and overrun) (SKYbrary – Runway Excursion)
- IND-07 – Anomaly: Ground Excursion – Runway (NASA ASRS coding taxonomy)

**Supporting reports:**
- SYNB-025 [RE]: "Landing on Runway 18R with a crosswind near the limit, the A330-300 drifted toward the edge."
- SYNB-026 [RE]: "Landing on Runway 36 in strong gusts from the left, the B737-800 drifted toward the edge."
- SYNB-021 [RE]: "Landing on Runway 31L with a crosswind near the limit, the B767-300F drifted toward the edge."
- SYNB-022 [RE]: "Landing on Runway 04R in strong gusts from the left, the E175 drifted toward the edge."
- SYNB-028 [RE]: "Landing on Runway 27R with a 30-knot gusting crosswind, the CRJ900 drifted toward the edge."
- SYNB-027 [RE]: "Landing on Rwy 13 with a crosswind near the limit, the B737 MAX 8 drifted toward the edge."
- SYNB-024 [RE, ARC]: "Landing on Rwy 31L in strong gusts from the left, the B787-9 drifted toward the edge."
- SYNB-019 [RE]: "Landing on Rwy 31L with a crosswind near the limit, the B787-9 drifted toward the edge."
- SYNB-023 [RE]: "Landing on Rwy 16 with a 30-knot gusting crosswind, the B787-9 drifted toward the edge."
- SYNB-020 [RE]: "Landing on Rwy 04R with a 30-knot gusting crosswind, the B777-300ER drifted toward the edge."

**Checks:** G1 pass · G2 pass · G3 pass · G4 pass · G5 pass · G6 pass · G7 pass · G8 pass

## B04 Overrun on a contaminated runway  –  GROUNDED

*Candidate definition:* On a wet, slushy, snowy or icy runway braking is poor and the aircraft overruns the end of the runway.

**ICAO parent:** RE – Runway Excursion (proposed by discovery: RE; parent scores {'RE': 0.895, 'USOS': 0.237, 'ARC': 0.104, 'RI': 0.089}; agreement 91%)

*Reports given to a better-matching sibling:* SYNB-025 → B03, SYNB-026 → B03, SYNB-022 → B03, SYNB-028 → B03

**Industry definitions:**
- IND-05 – Runway excursion (veer-off and overrun) (SKYbrary – Runway Excursion)
- IND-06 – Runway condition code (RWYCC) (ICAO Global Reporting Format (GRF) for runway surface conditions)
- IND-07 – Anomaly: Ground Excursion – Runway (NASA ASRS coding taxonomy)

**Supporting reports:**
- SYNB-033 [RE]: "Braking action was poor and the A320 overran the end of Runway 31L onto the grass."
- SYNB-029 [RE]: "Braking action was poor and the A330-300 overran the end of Runway 16 onto the grass."
- SYNB-036 [RE]: "Braking action was poor and the B777-300ER overran the end of Runway 36 by 40 metres."
- SYNB-035 [RE]: "Braking action was poor and the A320 overran the end of Runway 18R into the safety area."
- SYNB-031 [RE]: "Braking action was poor and the A330-300 overran the end of Rwy 22 into the safety area."
- SYNB-032 [RE]: "Braking action was poor and the CRJ900 overran the end of Rwy 31L into the safety area."
- SYNB-034 [RE]: "Braking action was poor and the B787-9 overran the end of Rwy 18R by 40 metres."
- SYNB-030 [RE]: "Braking action was poor and the B737 MAX 8 overran the end of Rwy 34L onto the grass."

**Checks:** G1 pass · G2 pass · G3 pass · G4 pass · G5 pass · G6 pass · G7 pass · G8 pass

## B05 Stall warning or upset during a go-around  –  NEEDS REVIEW

*Candidate definition:* During a go-around or missed approach the aircraft pitches up with high thrust, energy is mismanaged, and a stall warning or upset follows.

**ICAO parent:** LOC-I – Loss of Control – Inflight (proposed by discovery: LOC-I; parent scores {'LOC-I': 0.236, 'FUEL': 0.191, 'USOS': 0.177, 'WSTRW': 0.153}; agreement 28%)

**Industry definitions:**
- IND-21 – Stall prevention and recovery (FAA Advisory Circular 120-109A – Stall Prevention and Recovery Training)
- IND-08 – Loss of control in-flight (IATA – Loss of Control In-flight (LOC-I))
- IND-09 – Unreliable airspeed (SKYbrary – Unreliable Airspeed)

**Supporting reports:**
- SYNB-196 [LOC-I]: "The stall warning sounded falsely and the crew flew pitch and power."
- SYNB-042 [LOC-I]: "With full thrust the pitch rose to 20 degrees and the speed decayed until the stick shaker activated."
- SYNB-037 [LOC-I]: "With full thrust the pitch rose to 25 degrees and the speed decayed until the stick shaker activated."
- SYNB-040 [LOC-I]: "With full thrust the pitch rose to 20 degrees and the speed decayed until the stick shaker activated."
- SYNB-039 [LOC-I]: "With full thrust the pitch rose to 25 degrees and the speed decayed until the stick shaker activated."
- SYNB-043 [LOC-I]: "With full thrust the pitch rose to 20 degrees and the speed decayed until the stick shaker activated."
- SYNB-038 [LOC-I]: "With full thrust the pitch rose to 25 degrees and the speed decayed until the stick shaker activated."
- SYNB-041 [LOC-I]: "With full thrust the pitch rose to 25 degrees and the speed decayed until the stick shaker activated."
- SYNB-044 [LOC-I]: "With full thrust the pitch rose to 28 degrees and the speed decayed until the stick shaker activated."
- SYNB-049 [LOC-I]: "On final approach 6 miles behind a B747, the A320 encountered wake turbulence."

**Checks:** G1 pass · G2 pass · G3 pass · G4 pass · G5 pass · G6 FAIL · G7 FAIL · G8 pass

## B06 Wake turbulence upset on approach  –  GROUNDED

*Candidate definition:* Wake vortices from a preceding heavier aircraft cause a sudden roll or pitch upset on approach or departure.

**ICAO parent:** TURB – Turbulence Encounter (proposed by discovery: TURB; parent scores {'TURB': 0.737, 'WSTRW': 0.179, 'LOC-I': 0.111, 'RI': 0.043}; agreement 78%)

**Industry definitions:**
- IND-22 – Wake turbulence (FAA Advisory Circular 90-23G – Aircraft Wake Turbulence)

**Supporting reports:**
- SYNB-046 [TURB]: "On final approach 6 miles behind a heavy aircraft, the A321neo encountered wake turbulence."
- SYNB-045 [TURB]: "On final approach 3 miles behind a B777, the B787-9 encountered wake turbulence."
- SYNB-050 [TURB]: "On final approach 6 miles behind a B747, the CRJ900 encountered wake turbulence."
- SYNB-052 [TURB]: "On final approach 5 miles behind a B777, the B767-300F encountered wake turbulence."
- SYNB-051 [TURB]: "On final approach 3 miles behind a B777, the CRJ900 encountered wake turbulence."
- SYNB-047 [TURB]: "On final approach 6 miles behind a B777, the B767-300F encountered wake turbulence."
- SYNB-048 [TURB]: "On final approach 3 miles behind a A380, the B737-800 encountered wake turbulence."

**Checks:** G1 pass · G2 pass · G3 pass · G4 pass · G5 pass · G6 pass · G7 pass · G8 pass

## B07 Loss of separation caused by an ATC clearance  –  NEEDS REVIEW

*Candidate definition:* A controller clearance or instruction puts two aircraft into conflict, leading to loss of separation or a TCAS alert.

**ICAO parent:** MAC – Airprox / ACAS alert / loss of separation / near midair / midair collision (proposed by discovery: MAC; parent scores {'MAC': 0.651, 'RI': 0.201, 'LOC-I': 0.096, 'CFIT': 0.075}; agreement 57%)

*Reports given to a better-matching sibling:* SYNB-061 → B08

**Industry definitions:**
- IND-23 – Loss of separation (ICAO Doc 4444 – PANS-ATM (separation minima))
- IND-12 – Conflict: Airborne Conflict / NMAC (NASA ASRS coding taxonomy)
- IND-11 – Level bust (altitude deviation) (EUROCONTROL – Level bust)

**Supporting reports:**
- SYNB-058 [MAC, ATM]: "Both aircraft received TCAS resolution advisories."
- SYNB-056 [MAC, ATM]: "Both aircraft received TCAS resolution advisories."
- SYNB-060 [MAC, ATM]: "Separation was lost."
- SYNB-059 [MAC, ATM]: "Separation was lost."
- SYNB-054 [MAC, ATM]: "The controller cleared the A320 to descend into conflicting traffic at FL210."
- SYNB-057 [MAC, ATM]: "The controller cleared the CRJ900 to turn left into conflicting traffic at FL280."

**Checks:** G1 pass · G2 pass · G3 pass · G4 pass · G5 pass · G6 FAIL · G7 pass · G8 pass

## B08 TCAS resolution advisory after a level bust  –  GROUNDED

*Candidate definition:* The aircraft climbs or descends through its cleared altitude (level bust) and a TCAS resolution advisory follows.

**ICAO parent:** MAC – Airprox / ACAS alert / loss of separation / near midair / midair collision (proposed by discovery: MAC; parent scores {'MAC': 0.795, 'LOC-I': 0.047, 'WSTRW': 0.032, 'F-NI': 0.032}; agreement 100%)

*Reports given to a better-matching sibling:* SYNB-058 → B07

**Industry definitions:**
- IND-11 – Level bust (altitude deviation) (EUROCONTROL – Level bust)
- IND-10 – Resolution advisory (RA) (ICAO Annex 10 – Airborne Collision Avoidance System (ACAS))

**Supporting reports:**
- SYNB-066 [MAC]: "Traffic above triggered a TCAS resolution advisory to level off."
- SYNB-064 [MAC]: "Traffic crossing triggered a TCAS resolution advisory to level off."
- SYNB-061 [MAC]: "Traffic above triggered a TCAS resolution advisory to level off."
- SYNB-067 [MAC]: "Traffic ahead triggered a TCAS resolution advisory to climb."
- SYNB-062 [MAC]: "Traffic above triggered a TCAS resolution advisory to climb."
- SYNB-063 [MAC]: "Traffic ahead triggered a TCAS resolution advisory to descend."
- SYNB-065 [MAC]: "Traffic crossing triggered a TCAS resolution advisory to level off."
- SYNB-068 [MAC]: "Traffic ahead triggered a TCAS resolution advisory to descend."
- SYNB-226 [MAC]: "No resolution advisory followed and the traffic passed clear."
- SYNB-246 [MAC]: "No resolution advisory followed and the traffic passed clear."
- SYNB-266 [MAC]: "No resolution advisory followed and the traffic passed clear."

**Checks:** G1 pass · G2 pass · G3 pass · G4 pass · G5 pass · G6 pass · G7 pass · G8 pass

## B09 Hydraulic system failure in flight  –  GROUNDED

*Candidate definition:* Loss of fluid or pressure in a hydraulic system in flight degrades flight controls, brakes or landing gear.

**ICAO parent:** SCF-NP – System/Component Failure – Non-Powerplant (proposed by discovery: SCF-NP; parent scores {'SCF-NP': 0.778, 'F-NI': 0.078, 'LOC-I': 0.076, 'SCF-PP': 0.073}; agreement 100%)

*Reports given to a better-matching sibling:* SYNB-083 → B10, SYNB-085 → B10

**Industry definitions:**
- IND-24 – Hydraulic system failure (SKYbrary – Hydraulic System Failure)
- IND-25 – Landing gear malfunction (SKYbrary – Landing Gear Malfunction)

**Supporting reports:**
- SYNB-074 [SCF-NP]: "The flight crew ran the hydraulic loss checklist and diverted."
- SYNB-071 [SCF-NP]: "The flight crew ran the hydraulic loss checklist and continued to the destination."
- SYNB-073 [SCF-NP]: "We ran the hydraulic loss checklist and returned to the departure airport."
- SYNB-076 [SCF-NP]: "The captain and first officer ran the hydraulic loss checklist and continued to the destination."
- SYNB-072 [SCF-NP]: "We ran the hydraulic loss checklist and returned to the departure airport."
- SYNB-075 [SCF-NP]: "At FL180 the B hydraulic system quantity dropped to zero."
- SYNB-070 [SCF-NP]: "The crew ran the hydraulic loss checklist and returned to the departure airport."
- SYNB-078 [SCF-NP]: "The crew ran the hydraulic loss checklist and diverted."
- SYNB-069 [SCF-NP]: "The crew ran the hydraulic loss checklist and continued to the destination."
- SYNB-077 [SCF-NP]: "We ran the hydraulic loss checklist and continued to the destination."

**Checks:** G1 pass · G2 pass · G3 pass · G4 pass · G5 pass · G6 pass · G7 pass · G8 pass

## B10 Landing gear did not extend  –  GROUNDED

*Candidate definition:* One or more landing gear legs fail to extend or lock down, requiring alternate extension or a gear-up landing.

**ICAO parent:** SCF-NP – System/Component Failure – Non-Powerplant (proposed by discovery: SCF-NP; parent scores {'SCF-NP': 0.714, 'ARC': 0.091, 'USOS': 0.06, 'RE': 0.049}; agreement 100%)

**Industry definitions:**
- IND-25 – Landing gear malfunction (SKYbrary – Landing Gear Malfunction)
- IND-24 – Hydraulic system failure (SKYbrary – Hydraulic System Failure)

**Supporting reports:**
- SYNB-083 [SCF-NP]: "The alternate gear extension did not lock the gear."
- SYNB-085 [SCF-NP]: "The alternate gear extension was used and the gear locked down."
- SYNB-079 [SCF-NP]: "The alternate gear extension did not lock the gear."
- SYNB-081 [SCF-NP]: "The alternate gear extension did not lock the gear."
- SYNB-084 [SCF-NP]: "The alternate gear extension was used and the gear locked down."
- SYNB-080 [SCF-NP]: "The alternate gear extension was used and the gear locked down."
- SYNB-082 [SCF-NP]: "The alternate gear extension worked on the second attempt."
- SYNB-086 [SCF-NP]: "The alternate gear extension worked on the second attempt."

**Checks:** G1 pass · G2 pass · G3 pass · G4 pass · G5 pass · G6 pass · G7 pass · G8 pass

## B11 Terrain warning on a non-precision approach  –  GROUNDED

*Candidate definition:* During a non-precision or visual approach the aircraft descends too low and the terrain awareness system warns of terrain or obstacles.

**ICAO parent:** CFIT – Controlled Flight Into or Toward Terrain (proposed by discovery: CFIT; parent scores {'CFIT': 0.679, 'USOS': 0.104, 'SCF-NP': 0.097, 'SCF-PP': 0.091}; agreement 85%)

**Industry definitions:**
- IND-26 – Terrain awareness and warning system (TAWS) (14 CFR 121.354 – Terrain awareness and warning system)

**Supporting reports:**
- SYNB-087 [CFIT]: "The terrain awareness system called TERRAIN, PULL UP and the crew climbed away."
- SYNB-089 [CFIT]: "The terrain awareness system called TOO LOW TERRAIN and the crew climbed away."
- SYNB-093 [CFIT]: "The terrain awareness system called TERRAIN, PULL UP and the crew climbed away."
- SYNB-091 [CFIT]: "Flying a visual approach late in the evening with gusty winds, the aircraft descended below the minimum altitude."
- SYNB-088 [CFIT]: "The terrain awareness system called SINK RATE and the crew climbed away."
- SYNB-094 [CFIT]: "Flying a VOR approach shortly after sunrise in clear conditions, the aircraft descended below the minimum altitude."
- SYNB-090 [CFIT]: "The terrain awareness system called SINK RATE and the crew climbed away."
- SYNB-092 [CFIT]: "The terrain awareness system called SINK RATE and the crew climbed away."

**Checks:** G1 pass · G2 pass · G3 pass · G4 pass · G5 pass · G6 pass · G7 pass · G8 pass

## B12 GNSS interference or spoofing  –  GROUNDED

*Candidate definition:* Satellite navigation signals are jammed or spoofed, giving false position, lost RNP capability or incorrect time, often near conflict zones.

**ICAO parent:** NAV – Navigation Error (proposed by discovery: NAV; parent scores {'NAV': 0.689, 'MAC': 0.187, 'WSTRW': 0.107, 'CFIT': 0.066}; agreement 84%)

**Industry definitions:**
- IND-27 – GNSS jamming and spoofing (EASA Safety Information Bulletin 2022-02 – GNSS outages and alterations)

**Supporting reports:**
- SYNB-095 [NAV]: "Near the Black Sea both GPS receivers showed a position 40 miles in error."
- SYNB-101 [NAV]: "Near the Black Sea both GPS receivers showed a position 40 miles in error."
- SYNB-100 [NAV]: "Approaching the region both GPS receivers lost signal."
- SYNB-102 [NAV]: "On a route near a conflict area both GPS receivers reported a different time."
- SYNB-098 [NAV]: "Over the eastern Mediterranean both GPS receivers showed a position 40 miles in error."
- SYNB-253 [NAV]: "The FMS lost its navigation database during preflight and had to be reloaded."

**Checks:** G1 pass · G2 pass · G3 pass · G4 pass · G5 pass · G6 pass · G7 pass · G8 pass

## B13 Engine shutdown after loss of oil pressure  –  NEEDS REVIEW

*Candidate definition:* Low oil pressure or oil loss in flight leads the crew to shut an engine down as a precaution.

**ICAO parent:** SCF-PP – System/Component Failure – Powerplant (proposed by discovery: SCF-NP; parent scores {'SCF-PP': 0.833, 'BIRD': 0.157, 'SCF-NP': 0.098, 'LOC-I': 0.092}; agreement 100%)

**Industry definitions:**
- IND-28 – In-flight engine shutdown (IFSD) (SKYbrary – In-Flight Shutdown)

**Supporting reports:**
- SYNB-104 [SCF-PP]: "The flight crew shut the engine down and declared an emergency."
- SYNB-103 [SCF-PP]: "The flight crew shut the engine down and returned."
- SYNB-108 [SCF-PP]: "The flight crew shut the engine down and declared an emergency."
- SYNB-105 [SCF-PP]: "At FL210 the number 2 engine oil pressure fell below the limit."
- SYNB-106 [SCF-PP]: "At FL180 the right engine oil pressure fell below the limit."
- SYNB-107 [SCF-PP]: "At FL370 the right engine oil pressure fell below the limit."
- SYNB-117 [BIRD, SCF-PP]: "The flight crew shut the engine down and returned."
- SYNB-113 [BIRD, SCF-PP]: "The crew shut the engine down and returned."
- SYNB-116 [BIRD, SCF-PP]: "The flight crew shut the engine down and returned."

**Checks:** G1 pass · G2 pass · G3 pass · G4 pass · G5 pass · G6 pass · G7 pass · G8 FAIL

## B14 Takeoff with frost or ice not removed  –  NOT GROUNDED

*Candidate definition:* The aircraft departs or begins to depart with frost, snow or ice on its wings because it was not removed or the fluid failed.

**ICAO parent:** ICE – Icing (proposed by discovery: ICE; parent scores {'ICE': 0.88, 'RAMP': 0.157, 'LOC-I': 0.109, 'CFIT': 0.087}; agreement 90%)

*Reports given to a better-matching sibling:* SYNB-194 → B25, SYNB-190 → B25, SYNB-193 → B25, SYNB-189 → B25

**Industry definitions:**
- IND-29 – Clean aircraft concept (FAA Advisory Circular 120-60B – Ground Deicing and Anti-icing Program)
- IND-17 – Holdover time (FAA holdover time guidelines (ground de-icing and anti-icing))
- IND-38 – In-flight airframe icing (FAA Advisory Circular 91-74B – Pilot Guide: Flight in Icing Conditions)

**Supporting reports:**
- SYNB-109 [ICE]: "After a long taxi in light snow, a passenger reported ice on the wing."
- SYNB-110 [ICE]: "After a long taxi in light snow, a passenger reported ice on the wing."

**Checks:** G1 pass · G2 pass · G3 pass · G4 pass · G5 FAIL · G6 pass · G7 pass · G8 pass

## B15 Bird ingestion damaging an engine on takeoff or climb  –  NEEDS REVIEW

*Candidate definition:* One or more birds are ingested into an engine during takeoff or initial climb, causing vibration, surging or loss of thrust.

**ICAO parent:** BIRD – Bird (proposed by discovery: BIRD; parent scores {'BIRD': 0.838, 'SCF-PP': 0.821, 'CFIT': 0.105, 'SCF-NP': 0.065}; agreement 88%; suggested co-codes SCF-PP)

**Industry definitions:**
- IND-16 – Engine bird ingestion (14 CFR 33.76 – Bird ingestion (engine certification))
- IND-39 – Damaging bird strike (FAA National Wildlife Strike Database – strike reporting)
- IND-15 – Wildlife strike (FAA National Wildlife Strike Database)

**Supporting reports:**
- SYNB-113 [BIRD, SCF-PP]: "The right engine showed high vibration after ingesting birds."
- SYNB-117 [BIRD, SCF-PP]: "The right engine showed high vibration after ingesting birds."
- SYNB-111 [BIRD, SCF-PP]: "The number 1 engine surged with loud bangs after ingesting birds."
- SYNB-114 [BIRD, SCF-PP]: "The number 1 engine showed high vibration after ingesting birds."
- SYNB-115 [BIRD, SCF-PP]: "The left engine lost thrust after ingesting birds."
- SYNB-116 [BIRD, SCF-PP]: "The number 1 engine surged with loud bangs after ingesting birds."
- SYNB-118 [BIRD, SCF-PP]: "The left engine showed high vibration after ingesting birds."
- SYNB-112 [BIRD, SCF-PP]: "The right engine surged with loud bangs after ingesting birds."

**Checks:** G1 pass · G2 pass · G3 pass · G4 pass · G5 pass · G6 pass · G7 FAIL · G8 pass

## B16 Bird strike damaging the windshield or nose on approach  –  GROUNDED

*Candidate definition:* A large bird or flock strikes the windshield, radome or nose on approach or descent and causes visible damage.

**ICAO parent:** BIRD – Bird (proposed by discovery: BIRD; parent scores {'BIRD': 0.831, 'CFIT': 0.087, 'ARC': 0.071, 'RAMP': 0.054}; agreement 91%)

*Reports given to a better-matching sibling:* SYNB-111 → B15, SYNB-112 → B15

**Industry definitions:**
- IND-39 – Damaging bird strike (FAA National Wildlife Strike Database – strike reporting)
- IND-16 – Engine bird ingestion (14 CFR 33.76 – Bird ingestion (engine certification))
- IND-15 – Wildlife strike (FAA National Wildlife Strike Database)

**Supporting reports:**
- SYNB-214 [BIRD]: "A bird struck the radome during the approach."
- SYNB-254 [BIRD]: "A bird struck the windshield during the approach."
- SYNB-126 [BIRD]: "On descent through 3,000 feet a large goose struck the windshield."
- SYNB-120 [BIRD]: "On descent through 5,000 ft a large pelican struck the radome."
- SYNB-124 [BIRD]: "On descent through 5,000 ft a large goose struck the nose."
- SYNB-119 [BIRD]: "On descent through 3,000 ft a large goose struck the windshield."
- SYNB-121 [BIRD]: "On descent through 5,000 feet a large eagle struck the radome."
- SYNB-123 [BIRD]: "On descent through 3,000 ft a large pelican struck the radome."
- SYNB-125 [BIRD]: "On descent through 3,000 feet a large pelican struck the radome."
- SYNB-234 [BIRD]: "A bird struck the left wing leading edge during the approach."

**Checks:** G1 pass · G2 pass · G3 pass · G4 pass · G5 pass · G6 pass · G7 pass · G8 pass

## B17 Lithium battery fire from a passenger device  –  NEEDS REVIEW

*Candidate definition:* A phone, laptop, power bank or other lithium battery device overheats, smokes or catches fire in the cabin.

**ICAO parent:** CABIN – Cabin Safety Events (proposed by discovery: F-NI; parent scores {'CABIN': 0.778, 'F-NI': 0.716, 'TURB': 0.036, 'WSTRW': 0.034}; agreement 100%; suggested co-codes F-NI)

*Reports given to a better-matching sibling:* SYNB-164 → B21

**Industry definitions:**
- IND-31 – Lithium battery fire (FAA SAFO – Fire risks from lithium batteries in the cabin)

**Supporting reports:**
- SYNB-127 [F-NI, CABIN]: "A passenger's power bank began smoking after being crushed in a seat mechanism."
- SYNB-129 [F-NI, CABIN]: "A passenger's power bank overheated after being crushed in a seat mechanism."
- SYNB-131 [F-NI, CABIN]: "A passenger's power bank caught fire in a seat pocket."
- SYNB-130 [F-NI, CABIN]: "A passenger's laptop caught fire after being crushed in a seat mechanism."
- SYNB-128 [F-NI, CABIN]: "A passenger's power bank caught fire in a seat pocket."
- SYNB-133 [F-NI, CABIN]: "A passenger's laptop began smoking in the overhead bin."
- SYNB-134 [F-NI, CABIN]: "A passenger's phone began smoking after being crushed in a seat mechanism."
- SYNB-132 [F-NI, CABIN]: "A passenger's phone began smoking in the overhead bin."

**Checks:** G1 pass · G2 pass · G3 pass · G4 pass · G5 pass · G6 pass · G7 FAIL · G8 FAIL

## B18 Electrical smoke or burning smell in the flight deck  –  GROUNDED

*Candidate definition:* Smoke, fumes or a burning electrical smell appears in the flight deck, often traced to wiring, a display or a window heater.

**ICAO parent:** F-NI – Fire/Smoke (Non-Impact) (proposed by discovery: F-NI; parent scores {'F-NI': 0.86, 'SCF-NP': 0.7, 'CFIT': 0.109, 'LOC-I': 0.097}; agreement 100%; suggested co-codes SCF-NP)

**Industry definitions:**
- IND-32 – Smoke or fumes in flight (SKYbrary – Smoke and Fumes)

**Supporting reports:**
- SYNB-137 [F-NI, SCF-NP]: "During descent at FL330 the captain and first officer noticed an electrical burning smell in the flight deck."
- SYNB-138 [F-NI, SCF-NP]: "During descent at FL210 we noticed an electrical burning smell in the flight deck."
- SYNB-141 [F-NI, SCF-NP]: "During descent at FL240 the captain and first officer noticed smoke in the flight deck."
- SYNB-139 [F-NI, SCF-NP]: "During cruise at FL310 the flight crew noticed smoke in the flight deck."
- SYNB-142 [F-NI, SCF-NP]: "During descent at FL330 the crew noticed smoke in the flight deck."
- SYNB-135 [F-NI, SCF-NP]: "During climb at FL310 the crew noticed smoke in the flight deck."
- SYNB-140 [F-NI, SCF-NP]: "During climb at FL350 the crew noticed haze in the flight deck."
- SYNB-136 [F-NI, SCF-NP]: "During cruise at FL310 we noticed haze in the flight deck."

**Checks:** G1 pass · G2 pass · G3 pass · G4 pass · G5 pass · G6 pass · G7 pass · G8 pass

## B19 Low fuel after holding or a diversion  –  GROUNDED

*Candidate definition:* Extended holding, a missed approach or a diversion leaves the aircraft close to or below final reserve fuel, and the crew declares minimum fuel or a fuel emergency.

**ICAO parent:** FUEL – Fuel Related (proposed by discovery: FUEL; parent scores {'FUEL': 0.832, 'SCF-NP': 0.057, 'SCF-PP': 0.052, 'CFIT': 0.037}; agreement 95%)

**Industry definitions:**
- IND-33 – Minimum fuel and fuel emergency (ICAO Annex 6 – Fuel planning and in-flight fuel management)

**Supporting reports:**
- SYNB-150 [FUEL]: "After two missed approaches with a low overcast, fuel dropped toward final reserve."
- SYNB-146 [FUEL]: "After two missed approaches in clear conditions, fuel dropped toward final reserve."
- SYNB-145 [FUEL]: "After two missed approaches in clear conditions, fuel dropped toward final reserve."
- SYNB-149 [FUEL]: "After 40 minutes of holding in low visibility, fuel dropped toward final reserve."
- SYNB-144 [FUEL]: "After two missed approaches in clear conditions, fuel dropped toward final reserve."
- SYNB-148 [FUEL]: "After two missed approaches with gusty winds, fuel dropped toward final reserve."
- SYNB-143 [FUEL]: "After a diversion to a busy alternate in light snow, fuel dropped toward final reserve."
- SYNB-147 [FUEL]: "After a diversion to a busy alternate in clear conditions, fuel dropped toward final reserve."

**Checks:** G1 pass · G2 pass · G3 pass · G4 pass · G5 pass · G6 pass · G7 pass · G8 pass

## B20 Pushback or towing collision  –  GROUNDED

*Candidate definition:* During pushback or towing the tug, towbar or aircraft strikes another aircraft, a vehicle or a fixed object.

**ICAO parent:** RAMP – Ground Handling (proposed by discovery: RAMP; parent scores {'RAMP': 0.641, 'RI': 0.263, 'BIRD': 0.129, 'MAC': 0.11}; agreement 80%)

**Industry definitions:**
- IND-34 – Pushback and towing (IATA Ground Operations Manual – Pushback and towing)

**Supporting reports:**
- SYNB-151 [RAMP]: "During pushback from the gate the A320 wing tip struck a parked aircraft."
- SYNB-153 [RAMP]: "The tug driver could not see the wing tip."
- SYNB-156 [RAMP]: "The tug driver could not see the wing tip."
- SYNB-158 [RAMP]: "The towbar shear pin failed."
- SYNB-155 [RAMP]: "During pushback from the gate the A320 struck a baggage cart."
- SYNB-152 [RAMP]: "During pushback from the gate the B737 MAX 8 wing tip struck a parked aircraft."

**Checks:** G1 pass · G2 pass · G3 pass · G4 pass · G5 pass · G6 pass · G7 pass · G8 pass

## B21 Disruptive or unruly passenger  –  GROUNDED

*Candidate definition:* A passenger is aggressive, intoxicated or refuses crew instructions, interfering with the crew or other passengers.

**ICAO parent:** CABIN – Cabin Safety Events (proposed by discovery: CABIN; parent scores {'CABIN': 0.844, 'RAMP': 0.046, 'SCF-NP': 0.046, 'FUEL': 0.042}; agreement 100%)

**Industry definitions:**
- IND-30 – Unruly or disruptive passenger (ICAO Doc 10117 – Manual on the Legal Aspects of Unruly and Disruptive Passengers)

**Supporting reports:**
- SYNB-160 [CABIN]: "A intoxicated passenger refused to follow crew instructions during the flight."
- SYNB-159 [CABIN]: "A aggressive passenger refused to follow crew instructions during the flight."
- SYNB-163 [CABIN]: "A agitated passenger refused to follow crew instructions during the flight."
- SYNB-161 [CABIN]: "A aggressive passenger refused to follow crew instructions during the flight."
- SYNB-166 [CABIN]: "A aggressive passenger refused to follow crew instructions during the flight."
- SYNB-164 [CABIN]: "A aggressive passenger shouted at cabin crew during the flight."
- SYNB-165 [CABIN]: "Cabin crew restrained the passenger with help from others."
- SYNB-162 [CABIN]: "Cabin crew restrained the passenger with help from others."

**Checks:** G1 pass · G2 pass · G3 pass · G4 pass · G5 pass · G6 pass · G7 pass · G8 pass

## B22 Tail strike on takeoff  –  GROUNDED

*Candidate definition:* The tail strikes the runway during takeoff rotation, often after early or fast rotation or a wrong takeoff speed or weight.

**ICAO parent:** ARC – Abnormal Runway Contact (proposed by discovery: ARC; parent scores {'ARC': 0.894, 'RE': 0.105, 'BIRD': 0.039, 'USOS': 0.032}; agreement 100%)

**Industry definitions:**
- IND-35 – Tail strike (SKYbrary – Tailstrike)
- IND-18 – Hard landing, tail strike (SKYbrary – Hard Landing and Tail Strike)

**Supporting reports:**
- SYNB-173 [ARC]: "During rotation on Runway 34L the tail of the B737-800 struck the runway."
- SYNB-174 [ARC]: "During rotation on Runway 36 the tail of the A320 struck the runway."
- SYNB-167 [ARC]: "During rotation on Runway 27R the tail of the CRJ900 struck the runway."
- SYNB-172 [ARC]: "The takeoff speeds had been computed with the wrong weight."
- SYNB-168 [ARC]: "The pilot flying rotated early and fast."
- SYNB-170 [ARC]: "During rotation on Runway 16 the tail of the CRJ900 struck the runway."

**Checks:** G1 pass · G2 pass · G3 pass · G4 pass · G5 pass · G6 pass · G7 pass · G8 pass

## B23 Windshear on final approach  –  NEEDS REVIEW

*Candidate definition:* A sudden change in wind speed or direction on approach, often near a thunderstorm or microburst, causes loss of airspeed and a windshear warning.

**ICAO parent:** WSTRW – Windshear or Thunderstorm (proposed by discovery: TURB; parent scores {'WSTRW': 0.909, 'TURB': 0.218, 'MAC': 0.038, 'RAMP': 0.035}; agreement 90%)

**Industry definitions:**
- IND-36 – Low-level windshear (FAA Advisory Circular 00-54 – Pilot Windshear Guide)

**Supporting reports:**
- SYNB-178 [WSTRW]: "On short final near a thunderstorm the airspeed dropped by 25 knots."
- SYNB-180 [WSTRW]: "On short final near a thunderstorm the airspeed dropped by 25 knots."
- SYNB-182 [WSTRW]: "On short final near a thunderstorm the airspeed dropped by 30 knots."
- SYNB-179 [WSTRW]: "The predictive windshear warning sounded and the captain and first officer flew the windshear escape manoeuvre."
- SYNB-181 [WSTRW]: "The reactive windshear warning sounded and the CAPT and FO flew the windshear escape manoeuvre."
- SYNB-176 [WSTRW]: "The predictive windshear warning sounded and the crew flew the windshear escape manoeuvre."
- SYNB-175 [WSTRW]: "The predictive windshear warning sounded and the captain and first officer flew the windshear escape manoeuvre."
- SYNB-252 [WSTRW]: "The approach was flown with extra speed but no windshear was met."
- SYNB-232 [WSTRW]: "The approach was flown normally with no windshear encountered."

**Checks:** G1 pass · G2 pass · G3 pass · G4 pass · G5 pass · G6 pass · G7 pass · G8 FAIL

## B24 Landing short of the runway  –  GROUNDED

*Candidate definition:* The aircraft touches down before the runway threshold, on the approach lights or in the undershoot area.

**ICAO parent:** USOS – Undershoot/Overshoot (proposed by discovery: USOS; parent scores {'USOS': 0.739, 'RI': 0.254, 'RE': 0.2, 'ARC': 0.078}; agreement 70%)

**Industry definitions:**
- IND-37 – Undershoot (SKYbrary – Landing Short (Undershoot))

**Supporting reports:**
- SYNB-187 [USOS]: "On a visual approach shortly after sunrise the B787-9 touched down 50 metres short of the threshold of Runway 34L."
- SYNB-184 [USOS]: "On a visual approach at night the E175 touched down on the approach lights short of the threshold of Runway 34L."
- SYNB-186 [USOS]: "On a non-precision approach late in the evening the B787-9 touched down 50 metres short of the threshold of Runway 34L."
- SYNB-188 [USOS]: "On a visual approach shortly after sunrise the A321neo touched down in the grass short of the threshold of Runway 16."
- SYNB-185 [USOS]: "On a visual approach shortly after sunrise the A321neo touched down in the grass short of the threshold of Rwy 36."
- SYNB-183 [USOS]: "On a RNAV approach late in the evening the B787-9 touched down in the grass short of the threshold of Runway 22."

**Checks:** G1 pass · G2 pass · G3 pass · G4 pass · G5 pass · G6 pass · G7 pass · G8 pass

## B25 Airframe icing in flight  –  GROUNDED

*Candidate definition:* Ice builds on the wings, tail or windshield in flight in icing conditions, degrading performance or handling.

**ICAO parent:** ICE – Icing (proposed by discovery: ICE; parent scores {'ICE': 0.847, 'LOC-I': 0.175, 'RAMP': 0.148, 'CFIT': 0.146}; agreement 86%)

*Reports given to a better-matching sibling:* SYNB-110 → B14, SYNB-109 → B14

**Industry definitions:**
- IND-38 – In-flight airframe icing (FAA Advisory Circular 91-74B – Pilot Guide: Flight in Icing Conditions)
- IND-17 – Holdover time (FAA holdover time guidelines (ground de-icing and anti-icing))
- IND-29 – Clean aircraft concept (FAA Advisory Circular 120-60B – Ground Deicing and Anti-icing Program)

**Supporting reports:**
- SYNB-194 [ICE]: "Holding at 12,000 ft in icing conditions, ice built up on the wings faster than expected."
- SYNB-190 [ICE]: "Holding at 8,000 feet in icing conditions, ice built up on the wings faster than expected."
- SYNB-193 [ICE]: "The windshield iced over."
- SYNB-189 [ICE]: "The windshield iced over."
- SYNB-191 [ICE]: "Holding at 10,000 ft in supercooled cloud, ice built up on the wings faster than expected."
- SYNB-192 [ICE]: "Holding at 10,000 feet in supercooled cloud, ice built up on the wings faster than expected."

**Checks:** G1 pass · G2 pass · G3 pass · G4 pass · G5 pass · G6 pass · G7 pass · G8 pass

## B26 Unreliable airspeed from blocked pitot probes  –  GROUNDED

*Candidate definition:* Pitot probes blocked by ice, insects or covers give wrong airspeed indications, leading to warnings and autopilot disconnection.

**ICAO parent:** SCF-NP – System/Component Failure – Non-Powerplant (proposed by discovery: SCF-NP; parent scores {'SCF-NP': 0.492, 'ICE': 0.245, 'LOC-I': 0.151, 'WSTRW': 0.14}; agreement 67%)

**Industry definitions:**
- IND-09 – Unreliable airspeed (SKYbrary – Unreliable Airspeed)

**Supporting reports:**
- SYNB-201 [SCF-NP]: "Ice crystals had blocked the probes."
- SYNB-199 [SCF-NP]: "The autopilot disconnected and we flew pitch and power."
- SYNB-200 [SCF-NP]: "The autopilot disconnected and we flew pitch and power."
- SYNB-198 [SCF-NP]: "The autopilot disconnected and the crew flew pitch and power."

**Checks:** G1 pass · G2 pass · G3 pass · G4 pass · G5 pass · G6 pass · G7 pass · G8 pass

## B27 Crew crossed a hold-short line without clearance  –  GROUNDED

*Candidate definition:* The flight crew taxis past a runway hold-short line without a clearance to enter or cross the runway (pilot deviation).

**ICAO parent:** RI – Runway Incursion (proposed by discovery: RI; parent scores {'RI': 0.736, 'LOC-I': 0.042, 'USOS': 0.039, 'RE': 0.027}; agreement 100%)

*Reports given to a better-matching sibling:* SYNB-015 → B02

**Industry definitions:**
- IND-40 – Pilot deviation (runway incursion) (FAA Runway Safety programme – Pilot deviation)
- IND-02 – Runway incursion types (FAA Runway Safety programme)
- IND-19 – Vehicle or pedestrian deviation (FAA Runway Safety programme)

**Supporting reports:**
- SYNB-204 [RI]: "Taxiing on taxiway Delta at dusk, the flight crew crossed the hold-short line for Runway 22 without a clearance."
- SYNB-206 [RI]: "Taxiing on taxiway Kilo at night, the flight crew crossed the hold-short line for Runway 18R without a clearance."
- SYNB-205 [RI]: "Taxiing on taxiway Charlie at night, the crew crossed the hold-short line for Runway 22 without a clearance."
- SYNB-210 [RI]: "Taxiing on taxiway Charlie at night, the crew crossed the hold-short line for Runway 34L without a clearance."
- SYNB-209 [RI]: "Taxiing on taxiway Charlie late in the evening, the flight crew crossed the hold-short line for Runway 04R without a clearance."
- SYNB-207 [RI]: "Taxiing on taxiway Charlie in daylight, the captain and first officer crossed the hold-short line for Runway 22 without a clearance."
- SYNB-203 [RI]: "Taxiing on twy Echo late in the evening, we crossed the hold-short line for Rwy 22 without a clearance."
- SYNB-208 [RI]: "Taxiing on taxiway Alpha shortly after sunrise, we crossed the hold-short line for Runway 16 without a clearance."

**Checks:** G1 pass · G2 pass · G3 pass · G4 pass · G5 pass · G6 pass · G7 pass · G8 pass

## B28 Wrong route or waypoint loaded in the FMS  –  NOT GROUNDED

*Candidate definition:* The flight management system is loaded with the wrong route, waypoint or departure, and the aircraft deviates from its cleared route.

**ICAO parent:** NAV – Navigation Error (proposed by discovery: NAV; parent scores {'NAV': 0.732, 'FUEL': 0.089, 'CABIN': 0.064, 'RAMP': 0.048}; agreement 68%)

**Industry definitions:**
- IND-41 – Lateral navigation error (SKYbrary – Lateral Navigation Error)

**Supporting reports:**
- SYNB-212 [NAV]: "After departure the aircraft turned toward the wrong waypoint because an old route was loaded."
- SYNB-211 [NAV]: "After departure the aircraft turned toward the wrong waypoint because a similar-named waypoint was selected."

**Checks:** G1 pass · G2 pass · G3 pass · G4 pass · G5 FAIL · G6 pass · G7 pass · G8 pass
