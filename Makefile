rptest:
	cd bench && python3 driver.py

clean:
	cd bench && $(RM) *.png *.txt