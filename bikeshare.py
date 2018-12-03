import time
import pandas as pd
import numpy as np

# Declaring Global Variables
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june']

days = { 'm' : 'monday', 
        'tu' : 'tuesday', 
         'w' : 'wednesday', 
        'th' : 'thursday', 
         'f' : 'friday', 
        'sa' : 'saturday', 
        'su' : 'sunday'}

filter_types = ['month','day','both','none']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) filter_type - type of filter among month, day, all, or none based on user's choice.
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Which city data would you like to explore? Chicago, New York, or Washington.\n').lower()
        if city in CITY_DATA:
            break
        print("Sorry, Couldn't process your request. Please check your input again.\n")
        
    # sub-function to get user input for month (all, january, february, ... , june)
    def get_months():
        '''
        Asks user to specify a month to explore.
        
        Returns:
            (str) month - name of the month to filter by. or "all" to apply no month filter
        '''
        
        while True:
            month = input('Which month? January, February, March, April, May, or June.\n').lower()
            if month in months:
                break
            print("Sorry, Couldn't process your request. Please check your input again.\n")  
        return month
    
        
    # sub-function to get user input for day of week (all, monday, tuesday, ... sunday)
    def get_days():
        '''
        Asks user to specify a day to explore.
        
        Returns:
            (str) day - name of the month to filter by. or "all" to apply no day filter
        '''
        while True:
            day = input('Which day? M, Tu, W, Th, F, Sa, or Su.\n').lower()
            if day in days:
                break
            print("Sorry, Couldn't process your request. Please check your input again.\n")
        return days[day]
    
    # Ask user for additional filter. Filter by month, day, both, or none.
    day = 'all'    # by default
    month = 'all'    # by default
    
    # get user input for filter type and get corresponding inputs from the user.
    while True:
        filter_type = input('Would you like to filter your data by month, day, both, or not at all? \nType "None" to see the data without any filters.\n').lower()
        if filter_type in filter_types:
            break
        print("Sorry, Couldn't process your request. Please check your input again.\n")
        
    if filter_type == 'both' or filter_type == 'month':
        month = get_months()
        
    if filter_type == 'both' or filter_type == 'day':
        day = get_days() 
            
    
    print('-'*40)
    return city,filter_type, month, day


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

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('Most common month is: {}. (Counts: {})'.format(months[popular_month - 1].title(),df['month'].value_counts()[popular_month]))

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most common day is: {}. (Counts: {})'.format(popular_day, df['day_of_week'].value_counts()[popular_day]))
    
    # display the most common start hour
    popular_hour = df['Start Time'].dt.hour.mode()[0]
    print('most common start hour is: {}. (Counts: {})'.format(popular_hour, df['Start Time'].dt.hour.value_counts()[popular_hour]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most commonly used start station is: {}. (Counts: {})'
          .format(popular_start_station, df['Start Station'].value_counts()[popular_start_station]))
    
    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most commmonly used end station is: {}. (Counts: {})'
          .format(popular_end_station, df['End Station'].value_counts()[popular_end_station]))
    
    # display most frequent combination of start station and end station trip
    df['Trip Combination'] = df['Start Station'] + ' to ' + df['End Station']
    popular_trip = df['Trip Combination'].mode()[0]
    print('Most frequent combination of start and end station trip is: {}. (Counts: {})'
          .format(popular_trip, df['Trip Combination'].value_counts()[popular_trip]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    seconds = df['Trip Duration'].sum()
    
    # converting seconds into day/hour/minutes/seconds format (rounded off to integers)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    
    print('Total travel time is: {} days {} hours {} minutes and {} seconds'
          .format(int(days), int(hours), int(minutes), int(seconds)))
    
    # display mean travel time (rounded to two decimal places)
    mean_trip = round(df['Trip Duration'].mean(), 2)
    print('Mean travel time is {} seconds'.format(mean_trip))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
def user_stats(df):
    """Displays statistics on bikeshare users."""
    
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Counts of User Types', df['User Type'].value_counts().to_frame(''),'\n')

    # Check if 'Gender' column exists in the dataframe and Display counts of gender if applicable
    if 'Gender' in df:
        print('Counts of Genders', df['Gender'].value_counts().to_frame(''))
        if df['Gender'].isnull().sum():
            print('Unknown  {}'.format(df['Gender'].isnull().sum()))
    else: 
        print('Oops.. Gender information doesn\'t exist in our dataframe. Skipping to next calculation.\n')

    
    # Check and Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        # most common year of birth
        popular_birth = df['Birth Year'].mode()[0]
        print('Most common year of birth is:', popular_birth,'\n')
        
        # Find unique set of birth year and sort them in order.
        birth_arr = df['Birth Year'].unique()
        birth_arr.sort()
        
        # dropping NaN values
        birth_arr = birth_arr[np.isnan(birth_arr) == False]
    
        print('Earliest year of birth is:', birth_arr[0],'\n')
        print('Most recent year of birth is:', birth_arr[-1],'\n')
         
    else:
        print('Oops.. Birth year information doesn\'t exist in our dataframe.')

    print("\nThis took %s seconds." % (time.time() - start_time))    
    print('-'*40)


def display_raw_data(df):
    """
    Asks users if they want to see the raw data, if "yes", display first 5 lines of raw data. 
    And again it asks if they want to see more, if "yes" then you should display further 5 lines of raw data. 
    This continues until the user enters "no" or data reaches the end.
    """
    # Validating user's first input, "yes" or "no"
    while True:
        user_input = input('Would you like to see the raw data? Type "Yes" or "No".').lower()
        if user_input in ['yes','no']:
            break
        print('Sorry, couldn\'t process your request. Please check your input again.')    
    
    # If "yes", shows first 5 lines of data, then asks again, "yes" or "no".
    # If "yes" again, shows futher 5 lines of data, until user inputs "no" or data reaches the end. 
    start = 0    
    while user_input == 'yes':
        if (start+5) >= len(df):
            print(df.iloc[start:])
            print('This is the end of the dataframe')
            break
        print(df.iloc[start:start+5])

        while True:
            user_input = input('Would you like to see more? Type "Yes" or "No".').lower()
            if user_input in ['yes','no']:
                break
            print('Sorry, couldn\'t process your request. Please check your input again.')
    
        if user_input == 'yes':
            start += 5


def main():
    while True:
        city, filter_type, month, day = get_filters()
        df = load_data(city, month, day)
        
        input('Please press ENTER to continue ...')
        time_stats(df)
        input('Please press ENTER to continue ...')
        station_stats(df)
        input('Please press ENTER to continue ...')
        trip_duration_stats(df)
        input('Please press ENTER to continue ...')
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

            
if __name__ == "__main__":
	main()
