import time
import pandas as pd
import numpy as np
import calendar as cl
import datetime as dt

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Welcome!\n This tool can be used to analyse the US bikeshare data!\n')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = ''
    city_select = ['chicago', 'new york city', 'washington']
                   
    while city not in city_select:
          city = input('For which city do you want to analyze the data? Please enter either Chicago, New York City, or Washington.\n').lower()
          if city not in city_select:
             print('This was an invalid input. Please enter either Chicago, New York, or Washington.\n')
          
    # TO DO: get user input for month (all, january, february, ... , june)

    month = ''
    month_select = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
                    
    while month not in month_select:
          month = input('\nFor which month do you want to analyze the data? Please enter January, February, March, April, May, June, or ALL to select all months.\n').lower()
          if month not in month_select:
             print('This was an invalid input. Please enter the respective month or ALL.\n') 

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
   
    day = ''
    day_select = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
                    
    while day not in day_select:
          day = input('\nFor which day do you want to analyze the data? Please enter Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or ALL to select all days.\n').lower()
          if day not in day_select:
             print('This was an invalid input. Please enter the respective day or ALL.\n') 
     
       
    
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
    # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating popular time of travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
  
    if df['month'].nunique() > 1:
        common_month = int(df['month'].mode()[0]) # find the most common month
        print('Most Common Month:', cl.month_name[common_month])

    # TO DO: display the most common day of week
    if df['day_of_week'].nunique() >1:
        common_day = df['day_of_week'].mode()[0] # find the most common day 
        print('Most Common Day of Week:', common_day)

    # TO DO: display the most common start hour
    
    df['hour'] = df['Start Time'].dt.hour # extract hour from the Start Time column to create an hour column
    common_hour = df['hour'].mode()[0]   # find the most common hour (from 0 to 23)
    print('Most Common Start Hour:', common_hour)
              
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating popular stations and trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()[0] # find the most common start station
    print('Most Common Start Station:', common_start_station)

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()[0] # find the most common end station
    print('Most Common End Station:', common_end_station)

    # TO DO: display most frequent combination of start station and end station trip    
    df['Trip'] = df['Start Station'] + ' - ' + df['End Station']
    most_frequent_trip = df['Trip'].mode()[0] # find the most frequent combination of start and end station
    print('The most frequent combination of start and end station is:', most_frequent_trip)

    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating trip duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum() # calculate total travel time
    print('Total Travel Time in Seconds:', int(total_travel_time))
    print('Total Travel Time in Minutes:', int(total_travel_time/60))
    print('Total Travel Time in Hours:', int(total_travel_time/3600))
    print('Total Travel Time in Days:', int(total_travel_time/86400))
    
        
    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean() # calculate mean travel time
    print('Mean Travel Time in Seconds:', int(mean_travel_time))
    print('Mean Travel Time in Minutes:', int(mean_travel_time/60))

    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating user info...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
        
    user_types = df['User Type'].value_counts() # calculate counts per user type
    print('Counts of User Types:\n', user_types)

    # TO DO: Display counts of gender
    try:
        gender = df['Gender'].value_counts() #calculate counts per gender
        print('\nCounts of Gender:\n', gender)
    except:
        print('No gender data available') 
        
    # TO DO: Display earliest, most recent, and most common year of birth
    try: 
        birth_year_min = int(df['Birth Year'].min()) # earliest year
        birth_year_max = int(df['Birth Year'].max()) # most recent year
        birth_year_common = int(df['Birth Year'].mode()[0]) # most common year
        print('\nEarliest year of birth:', birth_year_min)
        print('Most recent year of birth:', birth_year_max)
        print('Most common year of birth:', birth_year_common)
    
    except:
        print('No year of birth data available')
                                                
                                               
    print('-'*40)

    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break            
      
if __name__ == "__main__":
	main()
