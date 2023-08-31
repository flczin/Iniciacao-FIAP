import subprocess
import time

main_screen_cmd = "python ./../testCLI.py -g main_screen"
flappy_cmd = "python ./../testCLI.py -g flappy"
car_game_cmd = "python ./../testCLI.py -g car_game"

main_screen = subprocess.Popen(main_screen_cmd, shell=True, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
time.sleep(10)

print("finished")

subprocess.call(['taskkill', '/F', '/T', '/PID', str(main_screen.pid)])

time.sleep(5)
car_game = subprocess.Popen(car_game_cmd, shell=True, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
time.sleep(20)
print("finished")
subprocess.call(['taskkill', '/F', '/T', '/PID', str(car_game.pid)])
