x86:
	cd bench-x86-64 && python3 driver.py

arm:
	cd bench-arm64 && python3 driver.py

clean:
	cd bench && $(RM) *.png *.txt
