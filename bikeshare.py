"""
Bikeshare script for exploring bikeshare usage and user profiles in major cities

An interactive program to allow users to ask questions about popular months,
days of the week, and time of day bikes are used. Also what are the popular 
starting and destination locations, ages of users, and other statistics about
bike sharing.

Functions:
        get_filters()
        load_data
        time_stats
        station_stats
        trip_duration_stats
        user_stats
Files:
        chicago.csv
        new_york_city.csv
        washington.csv
Version 1.0   16 Oct 2019
Ver 1.1
Last Updated 7 Nov 2019
"""

import time
import calendar as ca 
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" for no month filter
        (str) day - name of the day of week to filter by, or "all" for no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print("\nBikeshare data is available in the following cities:")
    
    city_list = ['chicago', 'new york city', 'washington']
    valid_months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    valid_days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 
    'friday', 'saturday', 'sunday']

    # get user input for city (chicago, new york city, washington).
    while True:
        try:
            city = input("\nEnter a city - Chicago, New York City, or Washington: ").lower().strip()
            if (city not in city_list):
                print ("Sorry, that entry is not in the list of available cities")
            else:
                break   
        except KeyboardInterrupt:
            print("\nDone - Program canceled by User\n")
            exit()
            
    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input('\nEnter a month (January thru June) or "all": ').lower().strip()
            if (month not in valid_months):
                print ("Sorry, that entry is not in the list of available months")
            else:
                break   
        except KeyboardInterrupt:
            print("\nDone - Program canceled by User\n")
            exit()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input('\nEnter a day of the week or "all": ').lower().strip()
            if (day not in valid_days):
                print ("Sorry, try again, Eg., Monday")
            else:
                break
        except KeyboardInterrupt:
            print("\nDone - Program canceled by User\n")
            exit()    
    

    print('-'*54)
    print("Stats for {}, Month: {}, Day of Week: {}".format(city.title(), month.title(), 
    day.title()))
    print('-'*54)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" for no month filter
        (str) day - name of the day of week to filter by, or "all" for no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.weekday_name
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['Month'] == month]
        
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['Day of Week'] == day.title()]
  
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    
    print("The most frequent month is {}".format(ca.month_name[df['Month'].mode()[0]]))

    # display the most common day of week
    print("The most frequent day of the week is {}".format(df['Day of Week'].mode()[0]))

    # display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    print("The most frequent start time of the day is {}:00".format(df['Hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most popular starting station is {}".format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print("The most popular destination is {}".format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    print("The most popular trip is {}"
    .format((df['Start Station'] + ' to ' + df['End Station']).mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Total travel time is {} hours".format(round(sum(df['Trip Duration'])/3600.,2)))
    
    # display mean travel time
    try:
        print("The mean trip duration is {} minutes".format(round(df['Trip Duration']
        .mean()/60.,2)))
    except:
        print("A mean cannot be calculated if 0 trips")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    # Display counts of user types
    print("\nNumber of users by type:")
    df_value_count = df['User Type'].value_counts().to_frame()
    print(df_value_count)

    # Display counts of gender
    try:
        print("\nNumber of users by gender:")
        df_value_count = df['Gender'].value_counts().to_frame()
        print(df_value_count)
    except:
        print("No gender data available for this city")

    # Display earliest, most recent, and most common year of birth
    try:
        print("\nAges of Users:")
        print("Oldest user birth year is {}".format(int(min(df['Birth Year']))))
        print("Youngest user birth year is {}".format(int(max(df['Birth Year']))))
        print("Most common birth year is {}".format(int(df['Birth Year'].mode()[0])))
    except:
        print("No birth year data available for this city\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # Check if user wants to see raw data
        view_raw = input('\nWould you like to see some raw data? Enter yes or no. ')
        if view_raw.lower() == 'yes':
            num_rows = len(df['Start Time'])
            for i in range(5, num_rows, 5):
                print(df.head(i))
                view_raw = input('\nWould you like to see more raw data? Enter yes or no. ')
                if view_raw.lower() != 'yes':
                    break
        
        # Check if user wants to restart with new entry data
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
        

if __name__ == "__main__":
	main()
