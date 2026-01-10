This guide is designed for **Qualified Personnel** to interpret the internal state of the **Zelio Logic SR3B261FU**1. Since these "Fault Codes" refer to internal auxiliary relays (M) and timers (T), they should be verified using the PLC's integrated display or via Zelio Soft monitoring software.

# ---

**Fault Diagnosis & Logic Status Guide (Program \#3201)**

This guide translates the program's ladder logic into actionable diagnostic "codes" to identify why the system is failing in Automatic mode2.

## **1\. Primary Operation Faults**

| Code / Status | Logic Indicator | Technical Meaning | Probable Cause |
| :---- | :---- | :---- | :---- |
| **FAULT: NO-RDY** |  **M1 is OFF** 3  |  **System Ready Interlock is open.** Both Pump Q1 and Q2 are blocked4444.  | Missing signal on Input **IL**5. Verify terminal voltage at **IL**6.  |
| **FAULT: T-OUT 9** |  **T9 Expired** 777 \+2  |  **Pump 1 Start Timeout.** Timer T9 reached 1.5s without the sequence completing88. \+1  | Solenoid Valve **Q6** is slow to actuate or Feedback sensor IF is missing9999. \+1  |
| **FAULT: T-OUT A** |  **TA Expired** 101010 \+2  |  **Pump 2 Start Timeout.** Timer TA reached 1.5s without the sequence completing1111. \+1  | Solenoid Valve **Q7** is slow to actuate or Feedback sensor IG is missing12121212. \+1  |

## ---

**2\. Safety & Interlock Blocks**

| Code / Status | Logic Indicator | Technical Meaning | Probable Cause |
| :---- | :---- | :---- | :---- |
| **BLOCK: SAFE** |  **M3 is OFF** 13  |  **Safety Interlock active.** The system detects a "collision" or unsafe state14.  | One of the auxiliary relays (m1) or outputs (q6, q7, q8) is stuck in the ON position15.  |
| **BLOCK: DIR** |  **M4/M5 OFF** 1616 \+1  |  **No Direction Latched.** The system does not know which tank to pump to1717. \+1  | Inputs **ID** or **IE** failed to pulse high18. Check float switches for continuity19.  |

## ---

**3\. Step-by-Step Logic Documentation for Technicians**

When documenting a fault, Qualified Personnel should record the state of these specific contacts:

### **Step 1: Check the Master Gate (M1)**

* **Logic Check:** Is M1 active? 20202020

* **Significance:** M1 must be closed for Pump Q1 or Q2 to receive power21212121.

* **Hardware Link:** Check Input **IL** (Physical terminal)22.

### **Step 2: Check the Directional Memory (M4/M5)**

* **Logic Check:** Which relay is latched? 2323  
  \+1

* **Significance:** M4 controls Direction A 24, M5 controls Direction B25.  
  \+1

* **Hardware Link:** Verify inputs **ID** and **IE**26.

### **Step 3: Verify the "No-Fault" Bit (M6)**

* **Logic Check:** Is M6 ON? 27

* **Significance:** M6 is a normally closed contact (**m6**) in the pump line28. If M6 activates, it creates a "Break" in the circuit and stops the pumps29.

* **Hardware Link:** Often linked to an E-Stop or Thermal Overload.

## ---

**4\. Maintenance Recommendation**

* **Timer Adjustment:** If the oil is highly viscous (thick), it may take longer than **1.5s** for the pressure to stabilize or valves to open30303030.  
  \+1

* **Action:** Qualified Personnel should monitor the time it takes for solenoid **Q6/Q7** to fully open31313131. If it is consistently near 1.5s, the timers T9/TA may need to be increased slightly to prevent nuisance trips32.  
  \+2

**Would you like me to create a "Pass/Fail" log sheet that your technicians can print out and fill in during their inspection?**