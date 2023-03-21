#
# Name: Becca Nika
# This is console-based Python program that inputs commands from the user
# and outputs data from the CTA2 L daily ridership database. There are nine 
# different commands that can be utilized to find information like the top
# ten busiest stations or can compare two stations during a specific year.
# This program utilizes SQL queries to gather the information from the database.
#

import sqlite3
import matplotlib.pyplot as plt


##################################################################
#
# print_stats
#
# Given a connection to the CTA database, executes various
# SQL queries to retrieve and output basic stats.
#
def print_stats(dbConn):
  dbCursor = dbConn.cursor()

  print("General stats:")
  
  # Number of stations
  dbCursor.execute("Select count(*) From Stations;")
  stations = dbCursor.fetchone()
  print("  # of stations:", f"{stations[0]:,}")

  # Number of stops
  dbCursor.execute("Select count(*) From Stops;")
  stops = dbCursor.fetchone()
  print("  # of stops:", f"{stops[0]:,}")

  # Number of ride entries
  dbCursor.execute("Select count(Num_Riders) From Ridership;")
  ride_entries = dbCursor.fetchone()
  print("  # of ride entries:", f"{ride_entries[0]:,}")

  # The date range of the database
  dbCursor.execute("Select MIN(strftime('%Y-%m-%d', Ride_Date)),MAX(strftime('%Y-%m-%d',Ride_Date)) From Ridership;")
  dates = dbCursor.fetchall()
  for r in dates:
    print("  date range:", r[0], "-", r[1])

  # Total ridership
  dbCursor.execute("Select SUM (Num_Riders) From Ridership;")
  total_riders = dbCursor.fetchone()
  total = 0
  for r in total_riders:
    total = r
  print("  Total ridership:", f"{total_riders[0]:,}")

  # Total ridership during the weekdays
  dbCursor.execute("Select SUM(Num_Riders) From Ridership Where Type_of_Day = 'W';")
  weekday_sum = dbCursor.fetchone()
  percentage = 0
  for r in weekday_sum:
    percentage = (r/ total) *100
  print("  Weekday ridership:", f"{weekday_sum[0]:,}", f"({percentage:.2f}%)")

  # Total ridership on Saturdays
  dbCursor.execute(
    "Select SUM(Num_Riders) From Ridership Where Type_of_Day = 'A';")
  saturday_sum = dbCursor.fetchone()
  for r in saturday_sum:
    percentage = (r/total)*100
  print("  Saturday ridership:", f"{saturday_sum[0]:,}", f"({percentage:.2f}%)")

  # Total ridership on Sundays or holiday
  dbCursor.execute(
    "Select SUM(Num_Riders) From Ridership Where Type_of_Day = 'U';")
  sun_hol_sum = dbCursor.fetchone()
  for r in sun_hol_sum:
    percentage = (r/total)*100
  print("  Sunday/holiday ridership:", f"{sun_hol_sum[0]:,}", f"({percentage:.2f}%)")

  # begin asking for input
  inp = input("\nPlease enter a command (1-9, x to exit): ").strip()
  command(inp, dbConn)
  dbCursor.close()


def command(inp, dbConn):

  dbCursor = dbConn.cursor()
  while (inp != "x"):

    if inp == "1":
      print("")
      commandOne(dbCursor)
      print("")

    elif inp == "2":
      print("** ridership all stations **")
      commandTwo(dbCursor)
      print("")      

    elif inp == "3":
      print("** top-10 stations **")
      commandThree(dbCursor)
      print("")      
      
    elif inp == "4":
      print("** least-10 stations **")
      commandFour(dbCursor)
      print("")
      
    elif inp == "5":
      print("")
      commandFive(dbCursor)      
      print("")
      
    elif inp == "6":
      print("** ridership by month **")
      commandSix(dbCursor)     
      print("")
      
    elif inp == "7":
      print("** ridership by year **")
      commandSeven(dbCursor)
      print("")
      
    elif inp == "8":
      print("")
      commandEight(dbCursor)
      print("")
      
    elif inp == "9":
      print("")
      commandNine(dbCursor)
      print("")
      
    else:
      print("**Error, unknown command, try again...\n")
    
    inp = input("Please enter a command (1-9, x to exit): ").strip()

# Uses an inputed partial station name to output all the stations similar to it
def commandOne(dbCursor):
  station_name = input("Enter partial station name (wildcards _ and %): ")
  
  query = "Select Station_ID, Station_Name From Stations Where Station_Name like (?) Order By Station_Name asc;"
  
  dbCursor.execute(query, [station_name])
  row = dbCursor.fetchall()
  
  if row:
    for r in row:
      print(r[0], ":", r[1])
  else:
    print("**No stations found...")

# outputs the ridership at each station in ascending order
def commandTwo(dbCursor):
  query1 = "SELECT Station_Name, SUM(Num_Riders) AS Total_Riders FROM Ridership INNER JOIN Stations ON Ridership.Station_ID = Stations.Station_ID GROUP BY Station_Name ORDER BY Station_Name asc;"
  
  dbCursor.execute(query1)
  row = dbCursor.fetchall()
  
  query2 = "Select SUM(Num_Riders) From Ridership;"
  dbCursor.execute(query2)

  # will use for percentages
  total_ridership = dbCursor.fetchone()
  total = ""
  for t in total_ridership:
    total += str(t)

  # calculates percentage from total ridership and outputs information
  for r in row:
    percentage = (r[1] / float(total)) * 100
    print(
      r[0],
      ":",
      f"{r[1]:,}",
      f"({percentage:.2f}%)"
    )

# Outputs the top-10 busiest stations in terms of ridership in descending order
def commandThree(dbCursor):
  query1 = "SELECT Station_Name, SUM(Num_Riders) AS Total_Riders FROM Ridership INNER JOIN Stations ON Ridership.Station_ID = Stations.Station_ID GROUP BY Station_Name ORDER BY SUM(Num_Riders) desc limit 10;"
  
  dbCursor.execute(query1)
  row = dbCursor.fetchall()
  
  query2 = "Select SUM(Num_Riders) From Ridership;"
  dbCursor.execute(query2)

  # used for percentages
  total_ridership = dbCursor.fetchone()
  total = ""
  for t in total_ridership:
    total += str(t)

  # calculates percentages and outputs information
  for r in row:
    percentage = (r[1] / float(total)) * 100
    print(
      r[0],
      ":",
      f"{r[1]:,}",
      f"({percentage:.2f}%)"
    )

# Outputs the least-10 busiest stations in terms of ridership in ascending order
def commandFour(dbCursor):
  query1 = "SELECT Station_Name, SUM(Num_Riders) AS Total_Riders FROM Ridership INNER JOIN Stations ON Ridership.Station_ID = Stations.Station_ID GROUP BY Station_Name ORDER BY SUM(Num_Riders) asc limit 10;"
  
  dbCursor.execute(query1)
  row = dbCursor.fetchall()
  
  query2 = "Select SUM(Num_Riders) From Ridership;"
  dbCursor.execute(query2)

  # used for percentages
  total_ridership = dbCursor.fetchone()
  total = ""
  for t in total_ridership:
    total += str(t)

  # calculates percentage and outputs information
  for r in row:
    percentage = (r[1] / float(total)) * 100
    print(
      r[0],
      ":",
      f"{r[1]:,}",
      f"({percentage:.2f}%)"
    )

# Uses inputed line color to output all station names associated in ascending order
def commandFive(dbCursor):
  line_color = input("Enter a line color (e.g. Red or Yellow): ")
  
  query = "SELECT Stop_Name, Direction, ADA FROM Stops INNER JOIN StopDetails ON Stops.Stop_ID = StopDetails.Stop_ID INNER JOIN Lines ON StopDetails.Line_ID = Lines.Line_ID WHERE Color Like (?) Order By Stop_Name asc;"
  
  dbCursor.execute(query, [line_color])
  row = dbCursor.fetchall()
  
  # if color is valid
  if row:  
    for r in row:
      accessible = "no"  # initial accessibility
      if r[2] == 1:      # changes accessbility if needed
        accessible = "yes"
      # outputs information
      print(r[0], ": direction =", r[1], "(accessible? ", f"{accessible})")
  else:
    print("**No such line...")

# Outputs total ridership by month in ascending order
def commandSix(dbCursor):
  query = "SELECT strftime('%m',Ride_Date) Month, SUM(Num_Riders) AS Total_Riders FROM Ridership GROUP BY Month ORDER BY Month asc;"
  
  dbCursor.execute(query)
  row = dbCursor.fetchall()

  # outputs monthly ridership
  for r in row:    
    print(r[0], ":", f"{r[1]:,}")
  print("")
  # does the user want the data plotted?
  plot = input("Plot? (y/n) ")
  
  # plots the monthly ridership
  if plot == "y":
    x = []
    y = []
    
    for r in row:      
      x.append(r[0])
      y.append(r[1]  * (10**8))

    plt.plot(x, y)
    plt.xlabel("month")
    plt.ylabel("number of riders (x * 10^8)")
    plt.title("monthly ridership") 
    plt.show(block=False)

# Outputs total ridership by year in ascending order
def commandSeven(dbCursor):
  query = "SELECT strftime('%Y',Ride_Date) as Month, SUM(Num_Riders) AS Total_Riders FROM Ridership GROUP BY Month ORDER BY Month asc;"
  
  dbCursor.execute(query)
  row = dbCursor.fetchall()

  # outputs yearly ridership
  for r in row:    
    print(r[0], ":", f"{r[1]:,}")
  print("")
  plot = input("Plot? (y/n) ")

  # plots yearly ridership
  if plot == "y":
    x = []
    y = []

    for r in row:      
      x.append(r[0])
      y.append(r[1]  * (10**8))

    plt.plot(x, y)
    plt.xlabel("year")
    plt.ylabel("number of riders (x * 10^8)")
    plt.title("yearly ridership") 
    plt.show(block=False)

# Inputs a year and the names of two stations and  outputs the daily ridership 
# at each station for that year
def commandEight(dbCursor):
  year = input("Year to compare against? ")
  print("")
  station1 = input("Enter station 1 (wildcards _ and %): ")

  q1 = f"Select Station_ID, Station_Name from Stations where Station_Name like '{station1}';"
  q1_result = dbCursor.execute(q1, []).fetchall()
  
  # checks if station1 input is valid
  if len(q1_result) == 0:
    print("**No station found...")
    return None
  if len(q1_result) > 1:
    print("**Multiple stations found...")
    return None
    
  print("")
  station2 = input("Enter station 2 (wildcards _ and %): ")
  
  q2 = f"Select Station_ID, Station_Name from Stations where Station_Name like '{station2}';"
  q2_result = dbCursor.execute(q2, []).fetchall()

  # checks if station2 input is valid
  if len(q2_result) == 0:
    print("**No station found...")
    return None
  if len(q2_result) > 1:
    print("**Multiple stations found...")
    return None

  # gathers the Ride_Date, sum of riders, Station_Name, and Station_ID for station1
  # with the inputed year
  q3 = f"SELECT strftime('%Y-%m-%d',Ride_Date) AS Date, SUM(Num_Riders), Station_Name, Ridership.Station_ID FROM Ridership INNER JOIN Stations WHERE Ridership.Station_ID = Stations.Station_ID AND Stations.Station_Name like '{station1}' AND Date like '{year}%' GROUP BY Date ORDER BY Date;"
  dbCursor.execute(q3, [])
  q3_result = dbCursor.fetchall()

  # parses the data and outputs the data in the correct format
  id1 = ""
  station_name1 = ""
  for r in q3_result:
    id1 = r[3]
    station_name1 = r[2]
  print("Station 1:", id1, station_name1)
  for row in list(q3_result)[0:5]: # first five days
    print(row[0], row[1])
  for row in list(q3_result)[-5:]: # last five days
    print(row[0], row[1])

  # gathers the Ride_Date, sum of riders, Station_Name, and Station_ID for station2
  # with the inputed year
  q4 = f"SELECT strftime('%Y-%m-%d',Ride_Date) AS Date, SUM(Num_Riders), Station_Name, Ridership.Station_ID FROM Ridership INNER JOIN Stations WHERE Ridership.Station_ID = Stations.Station_ID AND Stations.Station_Name like '{station2}' AND Date like '{year}%' GROUP BY Date ORDER BY Date asc;"
  dbCursor.execute(q4, [])
  q4_result = dbCursor.fetchall()

  # parses the data and outputs the data in the correct format
  id2 = ""
  station_name2 = ""
  for r in q4_result:
    station_name2 = r[2]
    id2 = r[3]
    
  print("Station 2:", id2, station_name2)
  for row in list(q4_result)[0:5]:
    print(row[0], row[1])
  for row in list(q4_result)[-5:]:
    print(row[0], row[1])

  q = f"Select strftime('%Y-%m-%d',Ride_Date) as Date from Ridership where Date like '{year}%' Group By Date Order By Date asc;"
  dbCursor.execute(q)
  q_res = dbCursor.fetchall()

  # makes a list of all the days in the inputed year from 1 to 365 or 366
  x_list = []
  counter = 0
  for i in q_res:
    counter = counter + 1
    x_list.append(counter)

  print("")
  plot = input("Plot? (y/n) ")

  # plotting of the data
  if plot == "y":
    y1 = []
    y2 = []
    
    for row in q3_result:
      y1.append(row[1])
    for row in q4_result:
      y2.append(row[1])
      
    plt.xlabel("day")
    plt.ylabel("number of riders")
    plt.title(f"riders each day of {year}")
    plt.plot(x_list, y1, label=f"{station_name1}")
    plt.plot(x_list, y2, label=f"{station_name2}")
    plt.legend()
    plt.show(block=False)

# Inputs a line color from the user and outputs all associated station names 
# in ascending order
def commandNine (dbCursor):
  color = input("Enter a line color (e.g. Red or Yellow): ")

  # selects the inputed color and gets the associated station name,
  # as well as the longtitude and latitude values
  query = f"Select distinct Color, Station_Name, Longitude, Latitude from Lines inner join StopDetails on Lines.Line_ID = StopDetails.Line_ID inner join Stops on StopDetails.Stop_ID = Stops.Stop_ID inner join Stations on Stops.Station_ID = Stations.Station_ID where Color like '{color}' Group By Station_Name Order By Station_Name asc;"
  
  dbCursor.execute(query)
  query_results = dbCursor.fetchall()

  # validity checking
  if len(query_results) == 0:
    print("**No such line...")
    return

  # outputing data in correct format: Station_Name, (Longitude, Latitude)
  for i in query_results:
    print(i[1], ":", f"({i[3]:,}, {i[2]:,})")

  print("")
  plot = input("Plot? (y/n) ")

  # plot the long and lat values onto the map of Chicagoland
  if plot == "y":
    x = []
    y = []

    for i in query_results:
      x.append(i[2])
      y.append(i[3])
      
    image = plt.imread("chicago.png")
    xydims = [-87.9277, -87.5569, 41.7012, 42.0868] # area covered by the map:
    plt.imshow(image, extent=xydims)
    plt.title(color + " line")
    
    # color is the value input by user, we can use that to plot the
    # figure *except* we need to map Purple-Express to Purple:
    if (color.lower() == "purple-express"):
      color="Purple" # color="#800080"
    plt.plot(x, y, "o", c=color)
    
    # annotate each (x, y) coordinate with its station name:    
    count = 0
    for r in query_results:
      plt.annotate(r[1], (float(x[count]), float(y[count])))
      count += 1
      
    plt.xlim([-87.9277, -87.5569])
    plt.ylim([41.7012, 42.0868])
    plt.show(block=False)
##################################################################
#
# main
#
def main():
  print('** Welcome to CTA L analysis app **')
  print()
  
  dbConn = sqlite3.connect('CTA2_L_daily_ridership.db')
  
  print_stats(dbConn)


if __name__ == '__main__':
  main()

#
# done
#
