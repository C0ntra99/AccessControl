# AccessControl

**Program has been updated, have not had time to update github** 

Rose State access control:
*meant to be ran on a Raspberry pi*

We had an incident at Rose State, to prvent any future incidents we wanted to implement a form of access control. Since every student had an ID with a mag stripe I used that as authentication. The GPIO pins are connected to a relay board that is also connected to a electric door strike and a 12v power supply. This system can be implemented on any door, and instead of using a door strike you can use anything that will open the door with a signal.

1.main.py
 - Waits on input from a card reader.
 - Hashes the card number and compares it to the allowed cards on DB.txt
 - If the card is on AdminDB.txt then it will ask for another cards input 3 times, then it will add it to DB.txt
  
 - If the card is allowed it will trigger GPIO pins on a raspberry pi to unlock the electric door strike.
  
2.hash.py
  - Simple script to hash all the raw numbers before the hashing funcion was implemented.
  
3.log.txt
  - Keeps a log of the cards that were either denied or granted access, along with the time and date.
  
4.DB.txt
  - Database of all the cards.
  - Only card in there right now is set to "1234"
  
5.AdminDB.txt:
  - Database of Administrator cards.
  - Only card in there is "4321"

