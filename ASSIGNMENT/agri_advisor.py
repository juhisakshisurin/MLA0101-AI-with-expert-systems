"""
AgriAdvisor: Rule-Based Expert System for Crop Disease Diagnosis
and Farm Resource Advisory (Irrigation + Pest Alerts)

Implements:
  - A Knowledge Base of IF-THEN production rules
  - A Forward-Chaining inference engine (data -> conclusions), used by the
    Irrigation Agent and Pest-Alert Agent (sensor readings drive action)
  - A Backward-Chaining inference engine (goal -> evidence needed), used by
    the Diagnosis Agent (hypothesis-driven, asks only for missing symptoms)

Author: MLA0101 - AI & Expert Systems Assignment (AgriAdvisor)
"""

from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# 1. KNOWLEDGE BASE
# ---------------------------------------------------------------------------

@dataclass
class Rule:
    name: str
    conditions: list          # list of facts (strings) that must all be true
    conclusion: str           # fact/action asserted when conditions hold
    explanation: str = ""


# --- 1a. Disease diagnosis rules (used by backward chaining) ---------------
DIAGNOSIS_RULES = [
    Rule("R1",
         ["leaf_yellowing", "leaf_curling", "whitefly_present"],
         "disease_leaf_curl_virus",
         "Yellowing + curling + whitefly vector => Leaf Curl Virus"),
    Rule("R2",
         ["brown_leaf_spots", "high_humidity", "warm_temperature"],
         "disease_early_blight",
         "Brown concentric spots under warm/humid conditions => Early Blight"),
    Rule("R3",
         ["white_powdery_coating", "low_humidity"],
         "disease_powdery_mildew",
         "White powdery coating in dry weather => Powdery Mildew"),
    Rule("R4",
         ["water_soaked_lesions", "high_humidity", "cool_temperature"],
         "disease_late_blight",
         "Water-soaked lesions in cool/humid weather => Late Blight"),
    Rule("R5",
         ["wilting", "yellowing_lower_leaves", "waterlogged_soil"],
         "disease_root_rot",
         "Wilting + lower leaf yellowing + waterlogging => Root Rot"),
    # Treatment rules chain off a diagnosis fact
    Rule("T1", ["disease_leaf_curl_virus"], "action_remove_infected_plants_control_whitefly",
         "Remove infected plants; apply neem/insecticide for whitefly control"),
    Rule("T2", ["disease_early_blight"], "action_apply_fungicide_chlorothalonil",
         "Apply chlorothalonil/mancozeb fungicide; improve air circulation"),
    Rule("T3", ["disease_powdery_mildew"], "action_apply_sulfur_fungicide",
         "Apply sulfur-based fungicide; avoid overhead irrigation"),
    Rule("T4", ["disease_late_blight"], "action_apply_copper_fungicide_destroy_debris",
         "Apply copper-based fungicide; destroy crop debris immediately"),
    Rule("T5", ["disease_root_rot"], "action_improve_drainage_apply_fungicide",
         "Improve field drainage; apply trichoderma/fungicide drench"),
]

# --- 1b. Irrigation rules (used by forward chaining) -----------------------
IRRIGATION_RULES = [
    Rule("I1", ["soil_moisture_low", "no_rain_forecast"], "action_irrigate_now",
         "Low soil moisture and no rain expected => irrigate immediately"),
    Rule("I2", ["soil_moisture_low", "rain_forecast"], "action_delay_irrigation",
         "Low moisture but rain expected => delay irrigation to save water"),
    Rule("I3", ["soil_moisture_adequate"], "action_no_irrigation_needed",
         "Adequate soil moisture => no irrigation needed"),
    Rule("I4", ["soil_moisture_high", "rain_forecast"], "action_check_drainage",
         "High moisture with more rain expected => check field drainage"),
]

# --- 1c. Pest/environment alert rules (used by forward chaining) ----------
PEST_RULES = [
    Rule("P1", ["pest_count_high", "temperature_favorable_for_pest"], "action_alert_pest_outbreak",
         "High pest count under favourable temperature => raise outbreak alert"),
    Rule("P2", ["pest_count_moderate"], "action_advise_monitoring",
         "Moderate pest presence => advise continued field monitoring"),
    Rule("P3", ["humidity_high", "temperature_high"], "action_alert_fungal_risk",
         "Hot & humid conditions => raise fungal-disease risk alert"),
]

ALL_RULES = DIAGNOSIS_RULES + IRRIGATION_RULES + PEST_RULES


# ---------------------------------------------------------------------------
# 2. FORWARD-CHAINING INFERENCE ENGINE  (data-driven: sensors -> action)
# ---------------------------------------------------------------------------

def forward_chain(facts: set, rules: list, verbose=True) -> set:
    """Repeatedly fire any rule whose conditions are satisfied until no new
    fact can be derived (naive/exhaustive forward chaining)."""
    facts = set(facts)
    fired = set()
    changed = True
    while changed:
        changed = False
        for rule in rules:
            if rule.name in fired:
                continue
            if all(c in facts for c in rule.conditions) and rule.conclusion not in facts:
                facts.add(rule.conclusion)
                fired.add(rule.name)
                changed = True
                if verbose:
                    print(f"  [FIRED {rule.name}] {rule.explanation} -> {rule.conclusion}")
    return facts


# ---------------------------------------------------------------------------
# 3. BACKWARD-CHAINING INFERENCE ENGINE (goal-driven: hypothesis -> evidence)
# ---------------------------------------------------------------------------

def backward_chain(goal: str, facts: set, rules: list, trace=None, depth=0) -> bool:
    """Try to prove `goal` is true, either because it's already a known fact
    or because some rule's conditions can all be (recursively) proven."""
    if trace is None:
        trace = []
    indent = "  " * depth
    if goal in facts:
        trace.append(f"{indent}[KNOWN] {goal}")
        return True
    for rule in rules:
        if rule.conclusion == goal:
            trace.append(f"{indent}[TRY {rule.name}] proving {goal} via {rule.conditions}")
            if all(backward_chain(cond, facts, rules, trace, depth + 1) for cond in rule.conditions):
                trace.append(f"{indent}[PROVEN] {goal} by {rule.name} ({rule.explanation})")
                facts.add(goal)
                return True
    trace.append(f"{indent}[FAIL] cannot prove {goal}")
    return False


def diagnose(symptoms: set, candidate_diseases=None):
    """Backward-chain over each candidate disease hypothesis until one is
    proven true from the given symptom facts; also derives treatment."""
    if candidate_diseases is None:
        candidate_diseases = [r.conclusion for r in DIAGNOSIS_RULES if r.conclusion.startswith("disease_")]
    for disease in candidate_diseases:
        trace = []
        facts_copy = set(symptoms)
        if backward_chain(disease, facts_copy, DIAGNOSIS_RULES, trace):
            treatment_facts = forward_chain(facts_copy, DIAGNOSIS_RULES, verbose=False)
            treatments = [f for f in treatment_facts if f.startswith("action_")]
            return disease, treatments, trace
    return None, [], []


# ---------------------------------------------------------------------------
# 4. SOFTWARE AGENTS (percept -> expert system query -> action)
# ---------------------------------------------------------------------------

class IrrigationAgent:
    """Model-based reflex agent. Maintains internal state of recent moisture
    trend and queries the expert system (forward chaining) each cycle."""
    def __init__(self):
        self.moisture_history = []

    def percept_and_act(self, sensor_facts: set):
        self.moisture_history.append(sensor_facts)
        derived = forward_chain(sensor_facts, IRRIGATION_RULES, verbose=False)
        actions = [f for f in derived if f.startswith("action_")]
        return actions


class PestAlertAgent:
    """Model-based reflex agent monitoring pest counts & weather trend."""
    def percept_and_act(self, sensor_facts: set):
        derived = forward_chain(sensor_facts, PEST_RULES, verbose=False)
        actions = [f for f in derived if f.startswith("action_")]
        return actions


class DiagnosisAgent:
    """Goal-based agent: goal = identify the disease explaining the observed
    symptoms, then recommend treatment. Uses backward chaining."""
    def percept_and_act(self, symptom_facts: set):
        disease, treatments, trace = diagnose(symptom_facts)
        return disease, treatments


# ---------------------------------------------------------------------------
# 5. DEMO / TEST CASES
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 70)
    print("TEST CASE 1: Irrigation Agent - dry soil, no rain")
    ia = IrrigationAgent()
    print(ia.percept_and_act({"soil_moisture_low", "no_rain_forecast"}))

    print("\nTEST CASE 2: Irrigation Agent - dry soil, rain expected")
    print(ia.percept_and_act({"soil_moisture_low", "rain_forecast"}))

    print("\nTEST CASE 3: Pest Alert Agent - high pest count, favourable temp")
    pa = PestAlertAgent()
    print(pa.percept_and_act({"pest_count_high", "temperature_favorable_for_pest"}))

    print("\nTEST CASE 4: Pest Alert Agent - hot & humid (fungal risk)")
    print(pa.percept_and_act({"humidity_high", "temperature_high"}))

    print("\nTEST CASE 5: Diagnosis Agent - Leaf Curl Virus symptoms")
    da = DiagnosisAgent()
    print(da.percept_and_act({"leaf_yellowing", "leaf_curling", "whitefly_present"}))

    print("\nTEST CASE 6: Diagnosis Agent - Late Blight symptoms")
    print(da.percept_and_act({"water_soaked_lesions", "high_humidity", "cool_temperature"}))

    print("\nTEST CASE 7: Diagnosis Agent - insufficient/no matching symptoms")
    print(da.percept_and_act({"leaf_yellowing"}))
