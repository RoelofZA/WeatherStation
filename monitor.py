#!/usr/bin/env python

import sqlite3

import os
import time
import glob

import serial

ser = serial.Serial('/dev/ttyACM0',9600,timeout=3.0)

# global variables
speriod=(15*60)-1
dbname='/var/www/templog.db'

# store the temperature in the database
def log_temperature(temp1, temp2):

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    curs.execute("INSERT INTO temps2 values(datetime('now'), (?),(?))", (temp1,temp2))

    # commit the changes
#    curs.execute("DELETE FROM temps")
    conn.commit()
    conn.close()

# display the contents of the database
def display_data():
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    for row in curs.execute("SELECT * FROM temps2"):
        print str(row[0])+"	"+str(row[1])+"     "+str(row[2])

    conn.close()

def readlineCR(port):
    rv = ""
    while True:
        ch = port.read()
        rv += ch
        if ch=='\r' or ch=='':
            return rv

# get temerature
# returns None on error, or the temperature as a float
def get_temp(charval):

    try:
	read_serial="0"
	read_serial=ser.readline()
	ser.write(charval)
        read_serial=ser.readline()
        tempvalue=float(read_serial)
        if tempvalue > 100:
            return None

        if tempvalue < -10:
            return 0

        return tempvalue
    except:
	#print("Unexpected error:", sys.exc_info()[0])
        return None

# main function
# This is where the program starts 
def main():

#    while True:

#	ser.write('R')
        # get the temperature from the device file
        temperature = get_temp('R')
	temperature2 = get_temp('E')
#	print temperature

        if temperature != None:
            print "temperature="+"{:.2f}".format(temperature)
	    print "temp2","{:.2f}".format(temperature2)
        else:
 	    # Sometimes reads fail on the first attempt
            # so we need to retry
            temperature = get_temp()
#       print "temperature="+str(temperature)

        # Store the temperature in the database
        if temperature != None:
            log_temperature(temperature,temperature2)

#	print temperature

        # display the contents of the database
#        display_data()
#        time.sleep(5)

if __name__=="__main__":
    main()
