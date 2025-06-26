import subprocess

config_file = "data/config.sumocfg"
cmd = f"sumo -c {config_file}"
print(f"Running: {cmd}")
subprocess.run(cmd, shell=True)
print("仿真完成。")
