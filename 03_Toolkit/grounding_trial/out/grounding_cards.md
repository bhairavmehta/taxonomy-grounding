# Grounding cards – run-20261103-152542

Embedder: local-lsa (64 dims). Sample reports are synthetic.

## C1 Landing or takeoff on an unintended surface  –  GROUNDED

*Candidate definition:* The aircraft lands, lines up to land, or starts a takeoff on a surface other than the assigned runway: a taxiway, a closed or wrong runway, or the wrong airport.

**ICAO parent:** RI – Runway Incursion (proposed by discovery: RI; parent scores {'RI': 0.567, 'RE': 0.198, 'NAV': 0.113, 'ICE': 0.056}; agreement 75%)

*Reports given to a better-matching sibling:* SAMPLE-006 → C2, SAMPLE-007 → C2

**Industry definitions:**
- IND-03 – Wrong-surface event (FAA Runway Safety programme)
- IND-04 – Anomaly: Ground Incursion – Runway or Taxiway (NASA ASRS coding taxonomy)

**Supporting reports:**
- SAMPLE-001 [RI]: "During a night visual approach to Runway 27R the crew lined up on the parallel taxiway, mistaking the taxiway edge lights for runway lights."
- SAMPLE-002 [RI]: "Cleared for takeoff on Runway 4L, the crew taxied onto Runway 4R, which was closed for construction."
- SAMPLE-005 [RI, NAV]: "The crew landed at a nearby general aviation airport with a similar runway alignment instead of the destination airport."
- SAMPLE-003 [RI]: "After a late runway change the crew did not rebrief the approach and landed on Runway 35L instead of the assigned Runway 35R."
- SAMPLE-004 [RI]: "In low visibility the crew began a takeoff from taxiway Bravo, believing it was the runway."

**Checks:** G1 pass · G2 pass · G3 pass · G4 pass · G5 pass · G6 pass · G7 pass · G8 pass

## C2 Runway entry or crossing without clearance  –  GROUNDED

*Candidate definition:* An aircraft or vehicle crosses a hold-short line, stop bar or holding point and enters an active runway without a clearance.

**ICAO parent:** RI – Runway Incursion (proposed by discovery: RI; parent scores {'RI': 0.767, 'RE': 0.016, 'ARC': 0.005, 'SCF-NP': 0.004}; agreement 100%)

**Industry definitions:**
- IND-04 – Anomaly: Ground Incursion – Runway or Taxiway (NASA ASRS coding taxonomy)
- IND-01 – Runway incursion (ICAO Doc 9870, Manual on the Prevention of Runway Incursions)
- IND-03 – Wrong-surface event (FAA Runway Safety programme)

**Supporting reports:**
- SAMPLE-009 [RI]: "The stop bar lights were on, but the crew continued past the holding point onto the runway after mistaking a frequency change for a crossing clearance."
- SAMPLE-007 [RI]: "A readback error led the crew to hear cross Runway 9 instead of hold short of Runway 9, and the aircraft entered the active runway without a clearance."
- SAMPLE-006 [RI, ATM]: "Taxiing to Runway 16, the crew crossed the hold-short line for Runway 22 without a clearance while another aircraft was on its takeoff roll."
- SAMPLE-008 [RI]: "A snow removal vehicle entered the active runway without a clearance during clearing operations."

**Checks:** G1 pass · G2 pass · G3 pass · G4 pass · G5 pass · G6 pass · G7 pass · G8 pass

## C3 Overrun after a long or fast landing on a wet or contaminated runway  –  GROUNDED

*Candidate definition:* The aircraft touches down long or fast on a wet or contaminated runway, braking is poor, and it overruns the runway end.

**ICAO parent:** RE – Runway Excursion (proposed by discovery: RE; parent scores {'RE': 0.742, 'SCF-PP': 0.258, 'RI': 0.014, 'ARC': 0.011}; agreement 100%)

**Industry definitions:**
- IND-07 – Anomaly: Ground Excursion – Runway (NASA ASRS coding taxonomy)
- IND-06 – Runway condition code (RWYCC) (ICAO Global Reporting Format (GRF) for runway surface conditions)
- IND-05 – Runway excursion (veer-off and overrun) (SKYbrary – Runway Excursion)

**Supporting reports:**
- SAMPLE-010 [RE]: "Braking action was poor and the aircraft overran the runway end by 60 metres into the runway end safety area."
- SAMPLE-013 [RE, SCF-PP]: "With one thrust reverser unavailable, a long landing on a contaminated runway ended in a low-speed overrun past the runway end."
- SAMPLE-011 [RE]: "After an unstabilized, fast approach the aircraft touched down 2,500 feet beyond the threshold on a runway reported with standing water and came to a stop in the overrun area."

**Checks:** G1 pass · G2 pass · G3 pass · G4 pass · G5 pass · G6 pass · G7 pass · G8 pass

## C4 Upset or stall after unreliable airspeed  –  GROUNDED

*Candidate definition:* Disagreeing or erroneous airspeed indications, for example from icing or pitot failure, lead to a stall warning, overspeed or upset in flight.

**ICAO parent:** LOC-I – Loss of Control – Inflight (proposed by discovery: LOC-I; parent scores {'LOC-I': 0.57, 'ICE': 0.412, 'SCF-NP': 0.338, 'SCF-PP': 0.013}; agreement 80%)

**Industry definitions:**
- IND-09 – Unreliable airspeed (SKYbrary – Unreliable Airspeed)

**Supporting reports:**
- SAMPLE-015 [LOC-I, ICE]: "Climbing through FL280 in icing conditions, the captain and first officer airspeed indications disagreed."
- SAMPLE-018 [LOC-I, ICE]: "Ice crystals caused unreliable airspeed indications."
- SAMPLE-017 [LOC-I, SCF-NP]: "A pitot heat failure at cruise produced a falling airspeed indication."

**Checks:** G1 pass · G2 pass · G3 pass · G4 pass · G5 pass · G6 pass · G7 pass · G8 pass

## C5 TCAS resolution advisory after an altitude deviation  –  GROUNDED

*Candidate definition:* The aircraft deviates from its cleared altitude (level bust) and traffic receives a TCAS resolution advisory or separation is lost.

**ICAO parent:** MAC – Airprox / ACAS alert / loss of separation / near midair / midair collision (proposed by discovery: MAC; parent scores {'MAC': 0.71, 'NAV': 0.028, 'LOC-I': 0.007, 'SCF-NP': 0.007}; agreement 100%)

**Industry definitions:**
- IND-11 – Level bust (altitude deviation) (EUROCONTROL – Level bust)
- IND-10 – Resolution advisory (RA) (ICAO Annex 10 – Airborne Collision Avoidance System (ACAS))

**Supporting reports:**
- SAMPLE-021 [MAC, ATM]: "The resulting level bust triggered a TCAS climb resolution advisory and separation was lost."
- SAMPLE-019 [MAC]: "The climbing aircraft overshot its cleared altitude of FL240 by 400 feet, and opposite-direction traffic received a TCAS resolution advisory to descend."
- SAMPLE-020 [MAC]: "Autopilot mode confusion caused an altitude deviation, and the crew received a TCAS resolution advisory for traffic 600 feet below."
- SAMPLE-022 [MAC, ATM]: "The controller issued a descent clearance into conflicting traffic and both aircraft received TCAS resolution advisories."

**Checks:** G1 pass · G2 pass · G3 pass · G4 pass · G5 pass · G6 pass · G7 pass · G8 pass

## C6 Clear-air turbulence with cabin injuries  –  NEEDS REVIEW

*Candidate definition:* An unexpected encounter with turbulence in clear air injures passengers or cabin crew who are standing, unbelted or near unsecured carts.

**ICAO parent:** CABIN – Cabin Safety Events (proposed by discovery: TURB; parent scores {'CABIN': 0.871, 'TURB': 0.854, 'MAC': 0.026, 'BIRD': 0.018}; agreement 100%; suggested co-codes TURB)

**Industry definitions:**
- IND-14 – Turbulence-related injuries (FAA Advisory Circular 120-88A – Preventing Injuries Caused by Turbulence)

**Supporting reports:**
- SAMPLE-025 [TURB, CABIN]: "Moderate to severe clear-air turbulence over the mountains caught the cabin with carts not secured, and a flight attendant was struck by a cart."
- SAMPLE-026 [TURB, CABIN]: "Only light chop was expected, but the aircraft met sudden severe turbulence in clear air."
- SAMPLE-023 [TURB, CABIN]: "The aircraft encountered severe clear-air turbulence at FL350 with no weather shown on radar."
- SAMPLE-024 [TURB, CABIN]: "Unforecast turbulence near the jet stream occurred just after the seat belt sign was turned off."

**Checks:** G1 pass · G2 pass · G3 pass · G4 pass · G5 pass · G6 pass · G7 FAIL · G8 FAIL

## C7 Engine damage or shutdown after bird ingestion  –  GROUNDED

*Candidate definition:* Birds ingested into an engine cause vibration, surge, loss of thrust, fire warning or shutdown.

**ICAO parent:** SCF-PP – System/Component Failure – Powerplant (proposed by discovery: SCF-PP; parent scores {'SCF-PP': 0.824, 'BIRD': 0.722, 'CFIT': 0.02, 'MAC': 0.012}; agreement 100%; suggested co-codes BIRD)

**Industry definitions:**
- IND-16 – Engine bird ingestion (14 CFR 33.76 – Bird ingestion (engine certification))

**Supporting reports:**
- SAMPLE-031 [SCF-PP, BIRD]: "After ingesting a large bird at 3,000 feet the crew received an engine fire warning, shut the engine down and discharged the fire extinguisher."
- SAMPLE-028 [SCF-PP, BIRD]: "The engine vibrated and lost thrust, and the crew shut it down and returned."
- SAMPLE-029 [SCF-PP, BIRD]: "Multiple bird strikes during the takeoff roll caused the right engine to surge, and the crew rejected the takeoff."

**Checks:** G1 pass · G2 pass · G3 pass · G4 pass · G5 pass · G6 pass · G7 pass · G8 pass

## C8 Takeoff after de-icing holdover time exceeded  –  NOT GROUNDED

*Candidate definition:* The aircraft is delayed after ground de-icing and the fluid holdover time is exceeded before takeoff.

**ICAO parent:** ICE – Icing (proposed by discovery: ICE; parent scores {'ICE': 0.737, 'RE': 0.012, 'RI': 0.008, 'ARC': 0.006}; agreement 100%)

**Industry definitions:**
- IND-17 – Holdover time (FAA holdover time guidelines (ground de-icing and anti-icing))

**Supporting reports:**
- SAMPLE-032 [ICE]: "The takeoff was delayed beyond the de-icing fluid holdover time, and the crew returned to the pad for a second de-icing."

**Checks:** G1 pass · G2 pass · G3 pass · G4 pass · G5 FAIL · G6 pass · G7 pass · G8 pass

## C9 Hard landing or tail strike  –  NEEDS REVIEW

*Candidate definition:* A hard or bounced touchdown, or contact of the tail with the runway during rotation or flare.

**ICAO parent:** ARC – Abnormal Runway Contact (proposed by discovery: RE; parent scores {'ARC': 0.52, 'RE': 0.169, 'RI': 0.093, 'ICE': 0.079}; agreement 65%)

**Industry definitions:**
- IND-18 – Hard landing, tail strike (SKYbrary – Hard Landing and Tail Strike)

**Supporting reports:**
- SAMPLE-034 [ARC]: "A late flare in gusty winds led to a hard landing and a tail strike."
- SAMPLE-036 [ARC]: "A bounced landing was followed by a hard second touchdown that damaged the nose landing gear."
- SAMPLE-035 [ARC]: "An incorrect takeoff weight in the flight management computer led to early rotation and a tail strike on takeoff."

**Checks:** G1 pass · G2 pass · G3 pass · G4 pass · G5 pass · G6 pass · G7 pass · G8 FAIL
