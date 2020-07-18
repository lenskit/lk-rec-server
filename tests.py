import os
import time
 
os.system('docker-compose up -d')
time.sleep(5) # Wait for 5 seconds
os.system('pytest')
