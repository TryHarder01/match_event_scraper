# match_event_scraper

This Python3 script takes as input an API key, match url from sportradar.us of a futbol game, and a destination file.

It uses the urllib library to download the XML response from the API.
The XML library to parse the response for key information.
The output is a csv in the same folder as the script. 

I noticed that while some match 'facts' have teamid and (x, y) values, not all events do. I addressed this by creating a dictionary for the teamid first and then adding a check for the teamid, x and y values or using 'NA' as a value. 

