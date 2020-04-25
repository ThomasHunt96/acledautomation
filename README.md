## Automation script for processing ACLED .csv files

## Getting Started:

### Prerequisites:
* Python 3.6+,
* Pandas 1.0,
* A csv file from [Acled Data](https://acleddata.com/data-export-tool/)
  
### Overview

Essentially this script performs the following: 
* Removes uncecessary columns, 
* Calculates a conflict date from "event_date", 
* Removes  duplicate admin2 rows by first occurence or highest fatalities, 
* Exports the processed data to a new csv file.

Run in command line, direct the program to enter the path to an ACLED.csv file.

You will be prompted to enter a 'start date' (in dd-mm-yyyy format), which will be used to calculate a conflict_date an integer calculated by days between the start date and 'event_date'. conflict_date replaces 'event_date' in the csv file.

Then you choose to filter out duplicate admin2s. Currently there are two filters: First occurence, which keeps the row of the first occurence of each admin2. Highest fatalities keeps the row with the highest fatalities for each admin2.


Data is exported to a csv file in the following format:
![image of table](https://i.ibb.co/nnp6kZz/Screenshot-2020-04-25-Tom-Automation-tasks.png)
'''

If you find any issues or have any improvements that can be made please raise them in the repo, and I'll see to them asap!








