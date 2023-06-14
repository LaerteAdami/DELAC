# import os
# os.system(' ')
import subprocess
print("Start")
list_files = subprocess.run(["turtleFSI", "-p", "test"])

print("Done")
