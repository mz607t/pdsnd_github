import time
import pandas as pd
import numpy as np

#dictionary for the cities and their files
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = {'january':1, 'february':2, 'march':3, 'april':4, 'may':5, 'june':6, 'all':7}
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

#Function for filtering user data preferences
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city
    city = ''
    while city not in CITY_DATA:
        city = input('Which city are you interested in - Chicago, New York City or Washington?  ').lower()
        if city not in CITY_DATA:
            print("I didn't get that... Please try again.")
    print("OK, we'll go with " + city.capitalize() + '.')

    # Get user input for month
    month = ''
    while month not in months:
        month = input('Which month are you interested in between January and June? You can also choose all.  ').lower()
        if month not in months:
            print("I didn't get that... Please try again.")
    print("OK, I'll show you " + month.capitalize() + '.')

    # Get user input for day of week
    day = ''
    while day not in days:
        day = input('Which day exactly are you interested in? You can also choose all.  ').lower()
        if day not in days:
            print("I didn't get that... Please try again.")
    print("OK, you want to see " + day.capitalize() + '.')

    print('-'*40)
    return city, month, day

#Function for loading the filtered data
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
    #Load the data for your city
    print("\nLoading data...")
    df = pd.read_csv(CITY_DATA[city])

    #Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    #Filter by month
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    #Filter by day of week
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

#Function to calculate all time-related statistics
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    common_month = df['month'].mode()[0]
    for name, number in months.items():
        if number == common_month:
            print('The month I see the most is ' + name.capitalize() + '.')

    # Display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('The day I see the most is ' + common_day + '.')

    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('Popular starting hour is ' + common_hour.astype(str) + '.')

    #Prints how much time it took for the calculation
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#Function to calculate all station related statistics
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station is ' + common_start_station + '.')

    # Display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('The most commonly used end station is ' + common_start_station + '.')

    # Display most frequent combination of start station and end station trip
    df['Start To End'] = df['Start Station'].str.cat(df['End Station'], sep=' to ')
    combo = df['Start To End'].mode()[0]
    print('The most frequent trip combination is from ' + combo + '.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#Function for trip duration statistics
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    # Refactor string formating
    total_duration = df['Trip Duration'].sum()
    minute, second = divmod(total_duration, 60)
    hour, minute = divmod(minute, 60)
    print(f'The total trip duration is {hour} hours, {minute} minutes and {second} seconds.')

    # Display mean travel time
    average_duration = round(df['Trip Duration'].mean())
    mins, sec = divmod(average_duration, 60)
    if mins > 60:
        hrs, mins = divmod(mins, 60)
        print(f'The average trip duration is {hrs} hours, {mins} minutes and {sec} seconds.')
    else:
        print(f'The average trip duration is {mins} minutes and {sec} seconds.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#Function to calculate user statistics
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].value_counts()
    print(f'\nHere are the types of users:\n\n{user_type}')

    # Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print(f'\nHere are the types of users by gender:\n\n{gender}')
    except:
        print("\nThere is no 'Gender' column in this file.")

    # Display earliest, most recent, and most common year of birth
    try:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print(f"\nThe earliest year of birth: {earliest}\n\nThe most recent year of birth: {recent}\n\nThe most common year of birth: {common_year}")
    except:
        print("There are no birth year details in this file.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    #Function to display the raw data
def display_data(df):
    """ Display raw data from the DF, if the user wants it. """

    BIN_RESPONSE_LIST = ['yes', 'no']
    rdata = ''
    counter = 0
    while rdata not in BIN_RESPONSE_LIST:
        rdata = input("\nDo you wish to view the raw data? (Yes/No)\n").lower()
        if rdata == "yes":
            print(df.head())
        elif rdata not in BIN_RESPONSE_LIST:
            print("I didn't get that... Please try again.\n")

    #Extra while loop here to ask user if they want to continue viewing data
    while rdata == 'yes':
        print("Do you wish to view more raw data?")
        counter += 5
        rdata = input().lower()
        if rdata == "yes":
             print(df[counter:counter+5])
        elif rdata != "yes":
             break

    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
