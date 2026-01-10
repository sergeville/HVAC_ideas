I cannot directly generate a downloadable PDF file for you to save to your computer, but I have organized all our findings, technical data, and logic analysis into a structured format below. You can easily convert this into a PDF by copying the text into a document editor (like Word or Google Docs) and selecting **File > Export as PDF**.

---

# Technical Analysis Report: Oil Tank Transfer Box

**Project:** PROGRAM #3201 **System Date:** 2026 Reference (Original Program: 09/06/08) **Author:** FRED 

## 1. Hardware Specification

* 
**Controller:** Schneider Electric Zelio Logic SR3B261FU.


* 
**Expansion Module:** SR3XT141FU (XT2).


* 
**Cycle Time:** 20 ms ( ms).


* 
**Hardware Input Filtering:** Slow (3ms).


* 
**Time Zone:** Europe with Daylight Saving enabled.



## 2. Input/Output Mapping

| Type | ID | Description / Function | Location in Logic |
| --- | --- | --- | --- |
| **Input** | **IL** | Master discrete input / System Ready | (1/4), (3/3), (4/4), (6/3), (7/4), (19/2) 

 |
| **Input** | **ID** | Transfer Initiation / Directional Logic | (26/2), (27/1), (28/3) 

 |
| **Input** | **IE** | Transfer Initiation / Directional Logic | (26/3), (28/2), (29/1) 

 |
| **Output** | **Q1** | Primary Pump/Transfer Output | (30/6), (36/1) 

 |
| **Output** | **Q2** | Secondary Pump/Transfer Output | (33/6), (37/1) 

 |
| **Output** | **Q6-Q7** | Solenoid Valves for Transfer | (10/6), (13/6), (22/1), (23/1) 

 |

## 3. Logic & Timer Configuration

* 
**Timer T9:** 1.5-second delay, Function A (Active, control held down).


* 
**Timer TA:** 1.5-second delay, Function A (Active, control held down).


* **Auxiliary Relay M3:** Acts as a safety interlock; prevents operation if Q6, Q7, or Q8 are active.
* **Directional Relays (M4/M5):** Store the state of the transfer request based on ID and IE.

## 4. Troubleshooting: Why the System Fails to Pump

Based on the provided program diagram and your observation that it only works in **Manual Mode**, the following logic conflicts are likely:

1. 
**Sensor Signal Drop (Input IL):** Since **IL** is required for the system-ready state (**M1**), any flicker in this sensor will immediately drop the pump outputs (**Q1/Q2**).


2. 
**Valve Feedback Delay:** The 1.5s timers (**T9/TA**)  act as a window. If the valves (**Q6/Q7**) do not actuate fast enough, the PLC logic assumes a hardware failure and prevents the pumps from running to avoid pressure build-up.


3. **Safety Interlock Block:** Relay **M3** checks if other valves/pumps are already active. If a valve sensor is stuck "ON," **M3** will remain "OFF," preventing any new transfer from starting.

---

### Visualization of the System Flow

*(You can include the previously generated system diagrams here in your final document.)*

1. **Sensors (I)** detect levels and send a request to **M2**.
2. **Safety Interlock (M3)** verifies no collisions.
3. **Timers (T9/TA)** provide a **1.5s delay** for valves to open.
4. **Pumps (Q1/Q2)** activate once all conditions are met.

---

**Would you like me to create a step-by-step Maintenance Checklist for your technicians to use while checking these specific sensors?**