To help your technicians resolve the issues with the **Oil Tank Transfer Box**, here is a comprehensive maintenance and troubleshooting checklist based on the logic found in **Program #3201**.

### 🛠️ Maintenance & Troubleshooting Checklist

This list focuses on why the system is failing in **Automatic Mode** while still functioning in **Manual Mode**.

#### 1. Power & PLC Health

* 
**Verify Module Model:** Ensure the main unit is a **SR3B261FU** and the extension is **SR3XT141FU**.


* 
**Check Cycle Status:** The PLC should be cycling at approximately **20ms**. If the "RUN" light is flashing or red, the program may have halted.


* 
**Input Filtering:** Be aware that inputs have a **3ms "Slow" filter**. If a sensor is flickering faster than this, the PLC will ignore the signal entirely.



#### 2. Critical Sensor Check (The "Gatekeepers")

* **Input IL (System Ready):** This is the most critical input. It appears in rungs 1, 3, 4, 6, 7, 9, and 19. If the sensor connected to **IL** is faulty, the system-ready relay (**M1**) will never engage, killing both pumps **Q1** and **Q2**.


* 
**Input ID & IE (Directional):** Check the physical float switches or buttons for **ID** and **IE**. These trigger the internal memory relays **M4** and **M5** which decide which way the oil flows.



#### 3. Valve & Timing Synchronization

* 
**Solenoid Outputs (Q6, Q7, Q8):** In Automatic mode, the PLC expects these valves to fire before or during pump operation.


* 
**The 1.5s Window:** Timers **T9** and **TA** are set to **1.5 seconds**.


* **Action:** Watch the physical valves when the system is in Auto. If they take longer than 1.5 seconds to open, the PLC logic for **Q1** or **Q2** may automatically reset to prevent pump cavitation.




* 
**Interlock M3:** Check if any of the "normally closed" contacts for **q6, q7, or q8** are stuck open in the logic. If the PLC *thinks* a valve is already on, **M3** will stay off and block the start sequence.



#### 4. Auxiliary Relay Status (Internal Logic)

If you have access to the Zelio Soft software, monitor these "Virtual" bits:

* 
**M1:** Must be **ON** for any pump to run.


* 
**M2:** Must be **ON** to signal that a transfer is actually requested.


* **M6:** Must be **OFF**. If **M6** is active, it acts as a "Stop" command for the pumps.



---

### Summary Table for Technicians

| Symptom | Likely Culprit | Source Reference |
| --- | --- | --- |
| **Pump won't start in Auto** | Input **IL** is open or flickering

 |  |
| **Pump starts then stops** | Timer **T9/TA** (1.5s) timing out

 |  |
| **No Direction Selected** | Inputs **ID** or **IE** failing

 |  |
| **System "Locked"** | Safety Interlock **M3** is blocked

 |  |

Would you like me to create a simplified **Wiring Diagram** that shows how these specific Inputs (IL, ID, IE) and Outputs (Q1, Q2) should be connected to the terminal blocks?