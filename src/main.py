import sentiment_analysis
import re


def file_extension(tweet_file, keyword_file):  # checks whether a file extension is given using regular expressions
    file_ext = re.compile(r".txt")  # This is the variable which will search for the .txt extension

    tweet_extension = file_ext.findall(tweet_file)  # Searches for the .txt extension on this file
    keyword_extension = file_ext.findall(keyword_file)  # Searches for the .txt extension

    if len(tweet_extension) == 0 and len(keyword_extension) == 0:  # If their is no extension on either file
        return tweet_file + ".txt", keyword_file + ".txt"  # Return the files with the extensions
    elif len(tweet_extension) >= 1 and len(keyword_extension) == 0:  # If their is no extension on the keyword file
        return tweet_file, keyword_file + ".txt"  # Returns the keyword file with an extension and the tweet the same
    elif len(tweet_extension) == 0 and len(keyword_extension) >= 1:  # If their is no extension on the tweet file
        return tweet_file + ".txt", keyword_file  # Returns the tweet file with an extension and the keyword the same
    elif len(tweet_extension) >= 1 and len(keyword_extension) >= 1:  # If there are extensions on both files
        return tweet_file, keyword_file  # Returns both files the same


def main():
    tweet_file_name = str(input("Please submit the file with the tweets: "))  # Get's the file with the tweets
    keyword_file_name = str(input("Please submit the file with the keywords: "))  # Get's the file with the keywords

    files = file_extension(tweet_file_name, keyword_file_name)  # Checks the extensions on the file names

    sentiments = sentiment_analysis.compute_tweets(files[0], files[1])
    print("Eastern tweet results: Average: " + str(sentiments[0][0]) + ", number of keyword tweets: " +
          str(sentiments[0][1]) + ", number of tweets in region: " + str(sentiments[0][2]))  # Prints the value compute tweets returns

    print("Central tweet results: Average: " + str(sentiments[1][0]) + ", number of keyword tweets: " +
          str(sentiments[1][1]) + ", number of tweets in region: " + str(
        sentiments[1][2]))  # Prints the value compute tweets returns

    print("Mountain tweet results: Average: " + str(sentiments[2][0]) + ", number of keyword tweets: " +
          str(sentiments[2][1]) + ", number of tweets in region: " + str(
        sentiments[2][2]))  # Prints the value compute tweets returns

    print("Pacific tweet results: Average: " + str(sentiments[3][0]) + ", number of keyword tweets: " +
          str(sentiments[3][1]) + ", number of tweets in region: " + str(
        sentiments[3][2]))  # Prints the value compute tweets returns


main()
