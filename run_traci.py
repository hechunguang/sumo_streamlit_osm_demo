import traci
import pandas as pd

sumo_binary = "sumo"
sumo_config = "data/config.sumocfg"

traci.start([sumo_binary, "-c", sumo_config])

records = []
step = 0
while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()
    for vid in traci.vehicle.getIDList():
        pos = traci.vehicle.getPosition(vid)
        speed = traci.vehicle.getSpeed(vid)
        records.append({
            "time": step,
            "id": vid,
            "x": pos[0],
            "y": pos[1],
            "speed": speed
        })
    step += 1

traci.close()
df = pd.DataFrame(records)
df.to_csv("fcd_output.csv", index=False)
print("轨迹数据已保存为 fcd_output.csv")
