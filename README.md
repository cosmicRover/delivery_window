# delivery_window
A little program to find a delivery slot for Amazon Fresh delivery during the covid-19 outbreak.

# How it works
This python program uses selenium to launch chrome, log-in to amazon, and wait for a delivery slot to open up on a given date. Once a slot is found, it will then send a text to the user to inform them. 

# Requirements
:reminder_ribbon: chrome 81 installed<br/>
:reminder_ribbon: python3 installed<br/>
:reminder_ribbon: selenium package installed (follow guide on user_creds.py)<br/>
:reminder_ribbon: :reminder_ribbon: followed the steps on user_creds.py<br/>

# Run
```cd``` into the ```delivery_window``` directory, then run: ```python3 driver.py```<br/>
:reminder_ribbon: be sure to exit all current chrome sessions first.
