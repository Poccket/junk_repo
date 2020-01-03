from datetime import datetime
import time
import os
import signal
import sys


def signal_handler(sig, frame):
	f.close()
	print("")
	print("Prime #", primes, ":", n)
	print("Took", round(time.time() - start, 2), "seconds to calculate")
	sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


start = time.time()
filename = "primes " + str(datetime.now()) + ".txt"
f = open(filename, "a")
n = 2
primes = 0

print("Send SIGINT (Ctrl+C) to stop", end=" ", flush=True)

#while os.stat(filename).st_size < 1000000000:
#while primes < 1000:
while True:
	isPrime = True
	for num in range(2, int(n ** 0.5) + 1):
		if n % num == 0:
			isPrime = False
			break
	if isPrime:
		f.write(str(n) + ";")
		primes += 1
	n += 1

f.close()