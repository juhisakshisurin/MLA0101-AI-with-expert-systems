# AgriAdvisor: Rule-Based Expert System for Crop Disease Diagnosis & Farm Resource Advisory

**Course**: MLA0101 - AI & Expert Systems  
**Module**: Assignment - Rule-Based Expert Systems & Software Agents  

---

## 📌 Project Overview
**AgriAdvisor** is a hybrid rule-based expert system designed for precision agriculture. It assists farmers and automated agricultural management systems by offering:
1. **Crop Disease Diagnosis**: Hypothesis-driven disease detection based on observed field symptoms and vectors.
2. **Irrigation Advisory**: Sensor-driven soil moisture and weather forecast analysis for optimal watering decisions.
3. **Pest & Environment Alerts**: Real-time monitoring of pest density and atmospheric risk factors (e.g., fungal infection conditions).

The system integrates both **Data-Driven (Forward-Chaining)** and **Goal-Driven (Backward-Chaining)** reasoning engines with modular **Software Agents**.

---

## 🏗️ Architecture & Core Components

```
                     +-----------------------------------+
                     |           Knowledge Base          |
                     |  - Diagnosis Rules (R1-R5, T1-T5) |
                     |  - Irrigation Rules (I1-I4)       |
                     |  - Pest Risk Rules (P1-P3)        |
                     +-----------------------------------+
                                       |
           +---------------------------+---------------------------+
           |                                                       |
           v                                                       v
+-----------------------+                               +-----------------------+
|   Forward Chaining    |                               |   Backward Chaining   |
|   Inference Engine    |                               |   Inference Engine    |
| (Data-Driven: Sensors)|                               | (Goal-Driven: Hypoth) |
+-----------------------+                               +-----------------------+
           |                                                       |
     +-----+-----+                                                 |
     |           |                                                 |
     v           v                                                 v
+----------+ +-----------+                                  +----------------+
|Irrigation| | PestAlert |                                  | DiagnosisAgent |
|  Agent   | |   Agent   |                                  |  (Goal-Based)  |
+----------+ +-----------+                                  +----------------+
```

---

## 🔑 Key Modules

### 1. Knowledge Base (`Rule` Dataclass)
Defines IF-THEN production rules with:
- `name`: Unique identifier (e.g., `R1`, `I2`, `P3`).
- `conditions`: List of premise facts required for the rule to fire.
- `conclusion`: Consequent fact or action asserted.
- `explanation`: Human-readable explanation of the reasoning logic.

### 2. Forward-Chaining Inference Engine (`forward_chain`)
- **Type**: Data-driven (Sensor Data $\rightarrow$ Conclusions/Actions).
- **Mechanism**: Iteratively fires any rule whose conditions are satisfied by known facts until no further facts can be derived.
- **Used By**: `IrrigationAgent` and `PestAlertAgent`.

### 3. Backward-Chaining Inference Engine (`backward_chain` & `diagnose`)
- **Type**: Goal-driven (Hypothesis $\rightarrow$ Sub-goals $\rightarrow$ Evidence required).
- **Mechanism**: Recursively attempts to prove candidate disease hypotheses by evaluating required symptom premises.
- **Used By**: `DiagnosisAgent`.

### 4. Software Agents
- **`IrrigationAgent`**: Model-based reflex agent querying irrigation rules to advise `action_irrigate_now`, `action_delay_irrigation`, `action_no_irrigation_needed`, or `action_check_drainage`.
- **`PestAlertAgent`**: Model-based reflex agent evaluating environmental parameters for pest outbreak and fungal risk alerts.
- **`DiagnosisAgent`**: Goal-based agent identifying disease causes and linking them to recommended treatments (e.g., fungicide application, whitefly control).

---

## 🚀 How to Run

### Prerequisites
- Python 3.7+ (No external third-party dependencies required; uses Python standard library `dataclasses`).

### Execution
Run the main script directly from the terminal:

```bash
python agri_advisor.py
```

---

## 🧪 Test Scenarios & Output

The script executes 7 default test cases:

| Test Case | Agent / Target | Facts Provided | Output / Derived Action |
|---|---|---|---|
| **Test 1** | `IrrigationAgent` | `soil_moisture_low`, `no_rain_forecast` | `['action_irrigate_now']` |
| **Test 2** | `IrrigationAgent` | `soil_moisture_low`, `rain_forecast` | `['action_delay_irrigation']` |
| **Test 3** | `PestAlertAgent` | `pest_count_high`, `temperature_favorable_for_pest` | `['action_alert_pest_outbreak']` |
| **Test 4** | `PestAlertAgent` | `humidity_high`, `temperature_high` | `['action_alert_fungal_risk']` |
| **Test 5** | `DiagnosisAgent` | `leaf_yellowing`, `leaf_curling`, `whitefly_present` | `('disease_leaf_curl_virus', ['action_remove_infected_plants_control_whitefly'])` |
| **Test 6** | `DiagnosisAgent` | `water_soaked_lesions`, `high_humidity`, `cool_temperature` | `('disease_late_blight', ['action_apply_copper_fungicide_destroy_debris'])` |
| **Test 7** | `DiagnosisAgent` | `leaf_yellowing` (Insufficient) | `(None, [])` |

---

## 📄 File Structure
```text
ASSIGNMENT/
├── 192525148 AIES ASSIGNMENT.pdf                   # Assignment Specification Document
├── 192525148 Assignment Implementation output image 1.png # Output Screenshot
├── agri_advisor.py                                 # Core Python Implementation
└── README.md                                       # Documentation (This file)
```
