x86:
	cd bench-x86-64 && python3 driver.py

arm:
	cd bench-arm64 && python3 driver.py

clean:
	cd bench-x86-64 && $(RM) *.png *.txt
	cd bench-arm64 && $(RM) *.png *.txt
