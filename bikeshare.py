import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input(
            '\nChicago \nNew York City \nWashington DC \nKindly, tell us which of these 3 cities you want to learn more about it\'s Bikeshare data: \n').lower()
        if city in ['chicago', 'new york city', 'washington']:
            break
        else:
            print('\nPlease, choose only between the 3 cities: \n')

    # Get user input for month (all, january, february, ... , june)
    while True:
        month = input(
            '\nKindly, tell us which month...\n Type any month name between the first six months or type "all"\n').lower()
        if month in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            break
        else:
            print(
                '\nPlease, only type the correct month name between the 1st hulf year or type "all" to get the whole year\'s data\n')
    # Get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input(
            '\nKindly, tell us which day...\n Type any day name or type "all"\n').lower()
        if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
            break
        else:
            print('\nPlease, only type the correct day name or type "all" to get the whole week\'s data\n')

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
    # Loading data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Converting the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extracting month , day of week , and hours from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour


    # Filtering by month if applicable
    if month != 'all':
 	# Using the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1

    	# Filter by month to create the new dataframe
        df = df[df['month'] == month]

    # Filter by day of week if applicable
    if day != 'all':
        # Filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    #create the new dataframe
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    common_month = df['month'].mode()[0]
    print('The most common month is: ', common_month, '\n')
    # Display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('The most common day is: ', common_day, '\n')
    # Display the most common start hour
    common_hour = df['hour'].mode()[0]
    print('The most common hour is: ', common_hour, '\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    print('The most commonly used start station is: ',
          df['Start Station'].mode()[0], '\n')

    # Display most commonly used end station
    print('The most commonly used end station is: ',
          df['End Station'].mode()[0], '\n')

    # Display most frequent combination of start station and end station trip
    frequent_stations = df['Start Station'] + "*" + df['End Station']
    common_station = frequent_stations.value_counts().idxmax()
    print('The most frequent used combinations are:\n{} \nto\n{}'.format(
        common_station.split('*')[0], common_station.split('*')[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    print('The total travel time is: ', df['Trip Duration'].sum(), '\n')

    # Display mean travel time
    print('The total mean time is: ', df['Trip Duration'].mean(), '\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].value_counts()
    print('The counts of user type is: \n', user_type)
    print()

    # Display counts of gender
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print('The counts of gender is: \n', gender)
    else:
        print('The counts of gender is: \nSorry, there\'s no information available at this instance!\n')
    

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('\nThe earliest, most recent, and most common year of birth are:\n')
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common = int(df['Birth Year'].mode())
        print('The earliest year of birth is: ', earliest, '\n')
        print('The most recent year of birth is: ', recent, '\n')
        print('The most common year of birth is: ', common, '\n')
    else:
        print('earliest, most recent, and most common year of birth are: \nSorry, there\'s no information available at this instance!')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    start_loc = 1
    while True:
        view_data = input(
            'Would you like to view 5 rows of individual trip data? Enter yes or no?\n')
        if view_data.lower() == 'yes':
            print(df[start_loc:start_loc+5])
            start_loc = start_loc+5
        else:
            break

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
