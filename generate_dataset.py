import pandas as pd
import numpy as np

data = []

for i in range(2000):
    v = np.random.normal(230, 15)
    c = np.random.normal(10, 6)
    pf = np.random.uniform(0.5, 1.0)
    f = np.random.normal(50, 1)

    # ================= ENGINEERING-BASED FAULT LOGIC =================

    # POWER FACTOR IS NOW IMPORTANT
    if pf < 0.65:
        fault = "PowerFactor Fault"

    elif c < 0.5:
        fault = "OpenCircuit"

    elif v > 260:
        fault = "OverVoltage"

    elif v < 180:
        fault = "UnderVoltage"

    elif c > 25:
        fault = "Overload"

    elif v < 200 and pf < 0.8:
        fault = "VoltageImbalance"

    elif pf < 0.75 and c > 15:
        fault = "GroundFault"

    elif np.random.rand() < 0.03:
        fault = "LineToLineFault"

    else:
        fault = "Normal"

    data.append([v, c, pf, f, fault])

df = pd.DataFrame(data, columns=[
    "Voltage", "Current", "PowerFactor", "Frequency", "Fault"
])

df.to_csv("dataset/fault_data.csv", index=False)

print("✅ ENGINEERING-BASED DATASET CREATED")