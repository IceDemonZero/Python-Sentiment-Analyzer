import re


# The below are coordinates are used for estimating timezones
p1 = (49.189787, -67.444574)
p2 = (24.660845, -67.444574)
p3 = (49.189787, -87.518395)
p4 = (24.660845, -87.518395)
p5 = (49.189787, -101.998892)
p6 = (24.660845, -101.998892)
p7 = (49.189787, -115.236428)
p8 = (24.660845, -115.236428)
p9 = (49.189787, -125.242264)
p10 = (24.660845, -125.242264)


def average(lst):  # Calculates the average of the timezone
    try:
        return sum(lst) / len(lst)  # Return the average of the timezone
    except ZeroDivisionError:  # If there are no tweets in the region it causes a zero division error
        return 0  # Return a zero in this case


def keyword_dictionary(keyword_file):  # Creates a dictionary which will store the keywords and the value they represent
    keywords = {}
    for line in keyword_file:  # for each line in the file
        values = line.split(",")  # Create a list by splitting the line based on the comma
        keywords.update({values[0]: int(values[1])})  # add the keyword and its associated value to the dictionary

    return keywords  # Return the dictionary


def reformat_tweet(tweet_file):  # Puts the tweet into a format the program can use
    coordinates = []  # Holds the coordinates for the tweets
    tweet_text = []  # Holds the tweet text

    tweet_regex = re.compile(r"\d\d:\d\d:\d\d ")  # Search for a pattern in the tweet like the one in the compile block
    for line in tweet_file:  # The code in this for loop will find and take the location and text form the tweets
        time = tweet_regex.search(line)  # Searches the tweet for the pattern indicating a time stamp
        text = line.split(time.group())  # Splits the line at the time stamp
        tweet_text.append(text[1].replace('\n', ""))  # Adds the text to the list and removes the new line character

        first_split = line.split("]")  # Splits the text for to isolate the coordinates and the first bracket
        text_coord = first_split[0].split("[")  # Isolates for just the str coordinates by removing bracket at the front
        coordinates.append((float(text_coord[1].split(",")[0]), float(text_coord[1].split(",")[1])))  # Adds coordinate

    punctuation_regex = re.compile(r"[\\[!@#$%^&*?.,\-_=+/:;{}()`~\"']")  # A regular expression which searches for punc
    for tweet in tweet_text:  # for each tweet in the list
        line = punctuation_regex.sub("", tweet)  # Replace the punctuation at the start with empty space
        tweet_text.insert(tweet_text.index(tweet), line)  # insert the new version of tweet in its proper index
        tweet_text.remove(tweet)  # Remove the old version of the tweet

    return tweet_text, coordinates  # Returns the lists


def determine_timezone(tweets, coordinates):
    eastern, central, mountain, pacific = [], [], [], []  # The lists divides tweets into timezones

    for i in range(len(tweets)):
        lowered_tweet = tweets[i].lower()
        if p1[0] >= coordinates[i][0] >= p2[0] and p1[1] >= coordinates[i][1] >= p3[1]:  # if the tweet is Eastern
            eastern.append(lowered_tweet)  # Adds the lower case version of the tweet to the list
        elif p3[0] >= coordinates[i][0] >= p4[0] and p3[1] >= coordinates[i][1] >= p5[1]:  # if the tweet is Central
            central.append(lowered_tweet)  # Adds the lower case version of the tweet to the list
        elif p5[0] >= coordinates[i][0] >= p6[0] and p6[1] >= coordinates[i][1] >= p8[1]:  # if the tweet is Mountain
            mountain.append(lowered_tweet)  # Adds the lower case version of the tweet to the list
        elif p7[0] >= coordinates[i][0] >= p10[0] and p7[1] >= coordinates[i][1] >= p9[1]:  # if the tweet Pacific
            pacific.append(lowered_tweet)  # Adds the lower case version of the tweet to the list

    return eastern, central, mountain, pacific


def compute_tweets(tweet_file_name, keyword_file_name):  # Computes the happiness scores for the timezones
    eastern_tweets, central_tweets, mountain_tweets, pacific_tweets = {}, {}, {}, {}  # The dictionaries for timezones
    keyword_num, total = 0, 0  # The variables which count the number of keywords in a tweet and the total sentiment of a tweet

    try:
        tweet_file = open(tweet_file_name, "r", encoding="utf-8")  # opens file
        keyword_file = open(keyword_file_name, "r", encoding="utf-8")  # opens file

        keyword = keyword_dictionary(keyword_file)  # Returns a dictionary with the keywords and their corresponding values
        tweets = reformat_tweet(tweet_file)   # reformats tweets
        regions = determine_timezone(tweets[0], tweets[1])  # takes the values of the timezones

        for i in regions[0]:  # Check for all numbers in range of eastern
            eastern_word = i.split()  # Splits up the words into a list based on spaces
            for word in eastern_word:  # Iterates through all the words in the list
                for key, value in keyword.items():  # Checks each and every keyword and value
                    if word == key:  # If the word is a key value
                        total += value  # Add the value to the total
                        keyword_num += 1  # Increase the number of keywords found in the tweet
            if keyword_num != 0:  # If there are keywords in the tweet
                eastern_tweets.update({i: total / keyword_num})   # Add tweet and its happiness score if it is a keyword
                total = 0  # Reset the total
                keyword_num = 0  # Reset the keyword number

        east_avg = average(eastern_tweets.values())  # Calculate the average for eastern tweets
        # Create a tuple with the average, the num of keyword tweets and the number of tweets in the region
        eastern = (east_avg, len(eastern_tweets), len(regions[0]))

        for i in regions[1]:  # Check for all numbers in range of central
            central_word = i.split()
            for word in central_word:
                for key, value in keyword.items():
                    if word == key:
                        total += value
                        keyword_num += 1
            if keyword_num != 0:
                central_tweets.update({i: total/keyword_num})
                total = 0
                keyword_num = 0

        central_avg = average(central_tweets.values())  # Calculate the average for central tweets
        # Create a tuple with the average, the num of keyword tweets and the number of tweets in the region
        central = (central_avg, len(central_tweets), len(regions[1]))

        for i in regions[2]:  # Check for all numbers in range of mountain
            mountain_word = i.split()
            for word in mountain_word:
                for key, value in keyword.items():
                    if word == key:
                        total += value
                        keyword_num += 1
            if keyword_num != 0:
                mountain_tweets.update({i: total/keyword_num})
                total = 0
                keyword_num = 0

        mountain_avg = average(mountain_tweets.values())  # Calculate the average for mountain tweets
        # Create a tuple with the average, the num of keyword tweets and the number of tweets in the region
        mountain = (mountain_avg, len(mountain_tweets), len(regions[2]))

        for i in regions[3]:  # Check for all numbers in range of pacific
            pacific_word = i.split()
            for word in pacific_word:
                for key, value in keyword.items():
                    if word == key:
                        total += value
                        keyword_num += 1
            if keyword_num != 0:
                pacific_tweets.update({i: total/keyword_num})
                total = 0
                keyword_num = 0
        pacific_avg = average(pacific_tweets.values())  # Calculate the average for pacific tweets
        # Create a tuple with the average, the num of keyword tweets and the number of tweets in the region
        pacific = (pacific_avg, len(pacific_tweets), len(regions[3]))

        return eastern, central, mountain, pacific  # Returns the tuples
    except FileNotFoundError:  # If their is no file of said name
        return []  # Return empty list