This document provides a structured, step-by-step technical procedure for **Qualified Personnel** to diagnose and verify the **Oil Tank Transfer Box (Program \#3201)**.

As a safety reminder: Ensure all Lockout/Tagout (LOTO) procedures are followed before opening the enclosure, and use appropriate PPE when working with the **240V AC supply (SR3B261FU module)**1.

# ---

**Step-by-Step Technical Verification Procedure**

## **Phase 1: Power & Hardware Integrity**

1. **Supply Voltage Check:** Verify that the main module (SR3B261FU) is receiving the correct voltage. This module is designed for 100-240V AC2.

2. **Expansion Connection:** Confirm the physical bus connection between the main module and the **SRXT141FU** extension3.

3. **Watchdog & Cycle Status:** Check the PLC screen (if available) to ensure the **Watchdog** is inactive and the cycle time is stable at **20ms**4.

4. **Date/Time Sync:** Ensure the system clock is accurate to the current date in **dd/mm/yyyy** format to ensure Daylight Saving logic does not interfere with timed operations5.

## **Phase 2: Input Signal Verification (Continuity & Voltage)**

Use a multimeter to verify that signals are reaching the PLC terminals.

1. **Verify Input IL (System Ready):** This input is used in multiple rungs (1/4, 3/3, 4/4, etc.)6. Without a high signal on **IL**, the system-ready relay **M1** cannot activate7777.  
   \+3

2. **Check Directional Inputs ID & IE:**  
   * Test continuity on **ID** (Rung 26/2) for "Tank A" logic8.

   * Test continuity on **IE** (Rung 26/3) for "Tank B" logic9.

3. **Confirm Input Filtering:** Note that the PLC is programmed with **3ms Slow Filtering**10. Rapidly flickering signals from a vibrating float switch may be filtered out and not registered by the logic.

## **Phase 3: Output & Timer Sequencing (The 1.5s Window)**

1. **Solenoid Valve Test (Q6, Q7, Q8):** \* In Auto mode, trigger a transfer and verify that **Q6** or **Q7** fires immediately11111111.  
   \+1

2. **Timer T9 & TA Observation:** \* The system utilizes a **1.5-second delay** (Function A)12121212.  
   \+1

   * **Step:** Measure the time between the valve opening and the pump (**Q1/Q2**) starting13131313. If the pump fails to start, the logic is likely timing out because it hasn't received a confirmation signal.  
     \+1

3. **Interlock M3 Check:** Verify that no conflicting outputs (**Q6, Q7, Q8**) are active simultaneously, as this will engage the **m1, q6, q7, q8** normally closed contacts, preventing **M3** from enabling the pumps14141414.  
   \+1

## **Phase 4: Final System Ready Logic (M1)**

1. **Monitor Auxiliary Relay M1:** This internal relay is the final "Gatekeeper" for **Q1** (Pump 1\) and **Q2** (Pump 2\)1515151515151515.  
   \+2

2. **Verify Fault Conditions:** Ensure that **M6** is not active, as it will break the circuit for both pump outputs16161616.  
   \+1

### ---

**Summary Checklist for Field Report**

* \[ \] Supply Voltage confirmed (100-240V AC).  
* \[ \] Input **IL** signal verified at terminal.  
* \[ \] **1.5s Timers** (T9/TA) firing correctly.  
* \[ \] **M3 Interlock** not blocked by stuck sensors.  
* \[ \] All LOTO devices removed and enclosure secured.

**Would you like me to create a specific "Fault Code" guide based on these relay behaviors to help your team document their findings?**