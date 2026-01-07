# HVAC Wiring Diagram Analysis: Outdoor Heat Pump Unit

This document provides a breakdown of the electrical wiring for a Heat Pump outdoor unit based on the provided technical schematic. It includes a physical **Connection Diagram** and a logical **Schematic Diagram**.

---

## 1. Key Components & Abbreviations
These are the primary "loads" (work-performing parts) and "switches" (control parts) identified in the system:

| Abbreviation | Component | Function |
| :--- | :--- | :--- |
| **COMP** | Compressor | Pumps refrigerant through the system. |
| **OFM** | Outdoor Fan Motor | Blows air over the outdoor coils. |
| **CB** | Control Board | The "brain" that manages timing, defrost, and safety. |
| **CONT** | Contactor | A heavy-duty relay that sends 230V power to the compressor. |
| **CAP** | Dual Capacitor | Helps the compressor and fan motor start and run. |
| **TRAN** | Transformer | Steps high voltage down to 24V for the control system. |
| **CCH** | Crankcase Heater | Keeps compressor oil warm during the off-cycle. |
| **RVS** | Reversing Valve | Swaps the unit between Heating and Cooling modes. |

---

## 2. System Logic & Power Flow
The **Schematic Diagram** (Ladder Form) illustrates how electricity moves through the unit:

* **High Voltage:** Power enters at **L1 and L2** (230V) and stays at the **CONT** (Contactor) contacts. When the contactor closes, power flows to the **COMP** and **OFM**.
* **Low Voltage:** The **CB** (Control Board) receives 24V signals from the indoor thermostat via terminals like **Y** (heating/cooling) and **O** (reversing valve).
* **Defrost Cycle:** The board uses "DEFROST TIME" pins (selectable at 30, 60, 90, or 120 minutes) to determine how often to check for ice. During defrost, the board switches to cooling mode to melt ice and shuts off the outdoor fan.

---

## 3. Safety Switches & Sensors
The Control Board monitors several safety devices to protect the equipment:

* **HPS (High Pressure Switch):** Shuts down the system if refrigerant pressure is dangerously high.
* **LPS (Low Pressure Switch):** Protects the compressor if refrigerant is lost.
* **DTS (Defrost Thermostat Sensor):** Monitors coil temperature to determine when to stop the defrost cycle.

---

## 4. Standard Wire Color Guide
The diagram follows industry-standard coloring for troubleshooting:

* **Red (R):** 24V Power.
* **Yellow (Y):** Compressor call signal.
* **Blue (C/VS):** Common/Neutral side of the 24V circuit.
* **Black/Red:** Typically indicates High Voltage (230V) lines.
