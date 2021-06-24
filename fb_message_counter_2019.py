## fb_message_counter_2019
## This takes the html file(s) that facebook gives you when you download your dataframe
## and creates several plots for it. To run it, you must do the following
## 1. Change the line me = friend('put your name here as shown on facebook')
## 2. yourfriendsname = friend('put your friend's name here as shown on facebook')
## 3. yourfriendsname.messages_file_dir = 'put the file path the the folder that contains the html files'
## 4. run analyze(yourfriendsname). It's at the bottom of this python script.

import pandas as pd
from bs4 import BeautifulSoup
import csv
import glob, os
pd.plotting.register_matplotlib_converters()
import matplotlib.pyplot as plt
from pylab import *
%matplotlib inline
import seaborn as sns
import numpy as np

## Class: friend.
## attributes:
#   name (exactly how their name appears in the chats. Case sensative)
#   total_messages_count (How many does this friend send)
#   message_stamps (a dataframe but only with the times (and name actually) of the friend)
#   messages (a dataframe with first column time stamps and the second column as the sender, i.e. either the friend or you)
#   messages_file_dir
class friend:
    def __init__(self,name, total_messages_count=0,message_stamps = pd.DataFrame({'A' : []}),messages=pd.DataFrame({'A' : []}),file_dir = ""):
        self.name = name
        self.total_messages_count = total_messages_count
        self.message_stamps = message_stamps #message stamps is a data frame with only their name
        self.messages = messages #sets a dataframe with al the chat data to be an attibute of the person. useful when you have several people
        self.messages_file_dir = file_dir #make sure you add an extra / or \\ after the file name. Otherwise when looking for the html file directory, it won't be like ~\message1.html


## FUNCTION: write_to_csv
## Params: filename, person
## returns: prints the total messages sent by me and the friend
# function takes an html file handed to it and creates a csv file populated with the two columns (date, sender)
# the dates of the file are give in the format of Dec 16, 2019, 10:38 PM
def write_to_csv(filename,person):
    # csvfile = csv.writer(open("chatdata.csv","a"))
    with open(filename, 'rb') as html:
        soup = BeautifulSoup(html)
    # get the dates
    dates = soup.find_all('div',{'class' : "_3-94 _2lem"})
    # get the senders
    senders = soup.find_all('div',{'class' : "_3-96 _2pio _2lek _2lel"})
    # print(senders[5].contents[0])
    i=0
    with open("chatdata.csv","a") as fp:
        # with open("chatdata.csv","a", encoding = "utf-8") as fp:
        # csvfile = csv.writer(open("chatdata.csv","w"))
        csvfile = csv.writer(fp)
        for date in dates:
            # date_data = date.contents[0].split(",", 1)
            # print(data)

            date_data = str(date.contents[0])
            date_data = date_data[:-9]        #get all but the three last character
            #add a try catch to see if a remove hours function exist
            sender_data = str(senders[i].contents[0]) #get the name of the sender at the same index of the bs4 element

            csvfile.writerow([date_data,sender_data])
            i=i+1
            # print([date_data,sender_data])
            if sender_data == me.name:
                me.total_messages_count +=1
            if sender_data == person.name:
                person.total_messages_count +=1
    print("total sent by me: " + str(me.total_messages_count))
    print("Total sent by " + str(person.name) + ": " + str(person.total_messages_count))


# #I'll keep this if the automation doesn't work for you. it mgiht have issues on linux, idk.
# # It's a real shame python doesn't allowed overloading. probably not worth importing @dispatch
# def extract_data_to_csv(person, num_files):
#     person.total_messages_count=0
#     me.total_messages_count=0
#     csvfile = open("chatdata.csv","w+")
#     csvfile.close() #clear the spreadsheet if it exists.
#
#     csvfile = csv.writer(open("chatdata.csv","w"))
#     csvfile.writerow(["date", "sender"])
#     for int in range(1,num_files+1):
#             write_to_csv(str(messages_file_dir + "message_" + str(int) + ".html"), rohan)




## Function: extract_data_to_csv_auto
## params: person
## Returns: just prints the files analizes and it calls the write_to_csv function
# the function checks the directory of the html files (person.messages_file_dir) and
# rather cleverly figures out how many there are and passes each to the
def extract_data_to_csv_auto(person):
    person.total_messages_count=0
    me.total_messages_count=0
    os.chdir(person.messages_file_dir) #possibly unecessary.
    csvfile = open("chatdata.csv","w+")
    csvfile.close() #clear the spreadsheet if it exists.

    with open("chatdata.csv","w") as fp:
        # with open("chatdata.csv","w", encoding = "utf-8") as fp:
        csvfile = csv.writer(fp)
        csvfile.writerow(["date", "sender"])

    for file in glob.glob("*.html"): #for each html file in the director...
        print(file)
        write_to_csv(str(person.messages_file_dir + file), person)
    print("---------DONE---------")


## Fucntion: sort_data_by_dates
## parameters: data frame df
## returns: a dataframe with the dates sorted in the format of a timeframe object. Also prints the first few sorted columns
# example: dates in the df before (Dec 16, 2019, 10:38 PM) --> (Timestamp('2019-12-16 22:38:00'))
#turns the dates from the previous function into YYY-MM-DD
#then sorts the dates from earliest to latest
def sort_data_by_dates(df,person):
    df['date'] = pd.to_datetime(df.date)
    df.head()
    # print(df.sort_values('date').head())
    person.messages = df.sort_values('date')
    return person.messages


## Function: message_stamps_for_friend
## params: person
## return: none
# just makes a dataframe with only the timestamps for that person.
# useful if you want to plot messages sent vs received for a friend.
def message_stamps_for_friend(person):
    person.message_stamps = person.messages.loc[(person.messages.sender == person.name)] #used to be df.sender
    return person.message_stamps

## Function: plot_for_friend
## params: person
## return: none
#Take a person instance as object and plots messages sent by them
# note, df.iloc[:,0].value_counts() gives number of messages on a given date
def plot_for_friend(person):
    # fig = plt.plot()
    matplotlib.rcParams.update({'font.size': 14, 'font.family': 'serif'})
    plt.figure(figsize=(15,5))
    plt.title('Messages sent per day by ' + person.name)
    x = person.messages.iloc[:,0].value_counts().index
    y = person.messages.iloc[:,0].value_counts().values
    plt.bar(x, y, align="center", width=4) #these params don't do shit
    plt.xticks(rotation=30)
    os.chdir(person.messages_file_dir)
    plt.savefig(str(person.name + "_barplot.png"), dpi=200)


## Function: plot_comparison
## params: person
## returns: plots
## plots the messages sent by each person on each day together
def plot_comparison(person):
    friend_x = message_stamps_for_friend(person).iloc[:,0].value_counts().index
    friend_y = person.message_stamps.iloc[:,0].value_counts().values
    #looks like a mess, but there's not a great way to store it.
    # I could maybe make message_stamps_for_friend take two params
    # But you only need to call it once. honestly making a new class called me might be cleaner, or
    # maybe add another parameter to each friend object, but but why bother
    # for just two lines of disgusting code.
    me_x = person.messages.loc[(person.messages.sender == me.name)].iloc[:,0].value_counts().index #first half says look in friend's messages, take only mine. second half says now how many are there for each time.
    me_y = person.messages.loc[(person.messages.sender == me.name)].iloc[:,0].value_counts().values

    matplotlib.rcParams.update({'font.size': 14, 'font.family': 'serif'})
    fig, ax = plt.subplots(figsize=(15,5))
    ax.bar(friend_x, friend_y, label = str(person.name),color="red", width=4,alpha=.5 )
    ax.bar(me_x,me_y, label= me.name,color="#1155dd", width=4,alpha=.5)
    ax.set_title('Friendship Comparison ')
    ax.legend(loc=0);
    os.chdir(person.messages_file_dir)
    plt.savefig(str(person.name + "_friendship_comparison.png"), dpi=200)



## Fucntion: cum_sum
## params: person
## return: none
## creates a figure for the cumulative sum of all the messages sent between you and your friend 
def cum_sum(person):
        df = pd.DataFrame({"dates": person.messages.iloc[:,0].value_counts().index,"counts":person.messages.iloc[:,0].value_counts().values})
        sorted_by_date = df.sort_values(by=['dates'])
        sorted_by_date['cum'] = sorted_by_date['counts'].cumsum()
        matplotlib.rcParams.update({'font.size': 14, 'font.family': 'serif'})
        plt.figure(figsize=(15,5))
        plt.title('Total Messages Exchanged Between Me and ' + person.name)
        ax = sns.lineplot(x=sorted_by_date['dates'],y=sorted_by_date['cum'])
        ax.set(ylabel='Total Messages')
        os.chdir(person.messages_file_dir)
        plt.savefig(str(person.name + "_cumsum.png"), dpi=200)


## Fucntion: cum_sum_comparison
## params: person
## return: none
## creates a plot for the cumulative sum of the messages sent by you, and the cum sum of the messages sent by your friend
## To be clear, this creates one figure with two lineplots on it
def cum_sum_comparison(person):
    friend_messages = message_stamps_for_friend(person)
    my_messages = person.messages.loc[(person.messages.sender == me.name)]

    df_friend = pd.DataFrame({"dates": friend_messages.iloc[:,0].value_counts().index,"counts":friend_messages.iloc[:,0].value_counts().values})
    sorted_by_date_friend = df_friend.sort_values(by=['dates'])
    sorted_by_date_friend['cum'] = sorted_by_date_friend['counts'].cumsum()

    df_me = pd.DataFrame({"dates": my_messages.iloc[:,0].value_counts().index,"counts":my_messages.iloc[:,0].value_counts().values})
    sorted_by_date_me = df_me.sort_values(by=['dates'])
    sorted_by_date_me['cum'] = sorted_by_date_me['counts'].cumsum()

    matplotlib.rcParams.update({'font.size': 14, 'font.family': 'serif'})
    plt.subplots(figsize=(15,5))
    sns.lineplot(x=sorted_by_date_friend['dates'],y=sorted_by_date_friend['cum'], label = str(person.name),color="red")
    ax = sns.lineplot(x=sorted_by_date_me['dates'],y=sorted_by_date_me['cum'], label= me.name,color="#1155dd")
    plt.title('Friendship Comparison - Cumulative Messages')
    ax.set(ylabel='Total Messages')
    plt.legend(loc=0);
    os.chdir(person.messages_file_dir)
    plt.savefig(str(person.name + "_comparison_cumsum.png"), dpi=200)





## One method to rule them all.
## instanciate a person properly and this does everything.
def analyze(person):
    print('extracting data from html...')
    extract_data_to_csv_auto(person)
    print('turning into data frame....')
    df = pd.read_csv("chatdata.csv", encoding = "ISO-8859-1")
    print('Ordering by date...')
    sort_data_by_dates(df,person)
    plot_for_friend(person)
    plot_comparison(person)
    cum_sum(person)
    cum_sum_comparison(person)

if __name__ == "__main__":
    me = friend('Jeremy Thaller') #...maybe person would have been a more apt name for the class, but this is the only oddity

#friends to analize
    rohan = friend('Rohan Kadambi')
    rohan.messages_file_dir = 'C:\\Users\\jerem\\OneDrive\\Documents\\Python\\facebook_messanger_counter\\facebook-jeremythaller\\messages\\inbox\\RohanKadambi_NQvgRgwgtQ\\'

    sarah = friend('Sarah Ritzmann')
    sarah.messages_file_dir = "C:\\Users\\jerem\\OneDrive\\Documents\\Python\\facebook_messanger_counter\\facebook-jeremythaller\\messages\\inbox\\SarahRitzmann_qZoMJVMdAQ\\"

    s_early = friend('Sarah Early')
    s_early.messages_file_dir = 'C:\\Users\\jerem\\OneDrive\\Documents\\Python\\facebook_messanger_counter\\facebook-jeremythaller\\messages\\inbox\\SarahEarly_tW04iuKGdQ\\'

    karol = friend('Karol Regula')
    karol.messages_file_dir = "C:\\Users\\jerem\\OneDrive\\Documents\\Python\\facebook_messanger_counter\\facebook-jeremythaller\\messages\\inbox\\KarolRegula_4_fm6DtwTw\\"
    thomas = friend('Thomas Malchodi')
    thomas.messages_file_dir = 'C:\\Users\\jerem\\OneDrive\\Documents\\Python\\facebook_messanger_counter\\facebook-jeremythaller\\messages\\inbox\\ThomasMalchodi_PFq8d7gKmg\\'
    lucas = friend('Lucas Estrada')
    lucas.messages_file_dir = 'C:\\Users\\jerem\\OneDrive\\Documents\\Python\\facebook_messanger_counter\\facebook-jeremythaller\\messages\\inbox\\LucasEstrada_mKLuymR_pg\\'
    david = friend('David Thaller')
    david.messages_file_dir = "C:\\Users\\jerem\\OneDrive\\Documents\\Python\\facebook_messanger_counter\\facebook-jeremythaller\\messages\\inbox\\DavidThaller_tcugDXxZlg\\"
    
    
    
    ## If you have a friend with non-standard characters in their name (or in the messages)
## Karol is my polish friend, and his facebook name has a strange character in it. This deals with that
    os.chdir(karol.messages_file_dir)
    df = pd.read_csv("chatdata.csv", encoding = "ISO-8859-1")
    sort_data_by_dates(df,karol)
    plot_for_friend(karol)
    plot_comparison(karol)
    cum_sum(karol)
    cum_sum_comparison(karol)
    
    anayze(s_early)
    
# In this data set there's a strange dip in message frequencies. Upon investigation, I think this was my 10 day trip to the UK
    supervoid = sarah.messages.loc[(sarah.messages.date >= pd.to_datetime('Jan 21, 2018, 12:13 AM')) & (sarah.messages.date <= pd.to_datetime('May 21, 2018, 12:29 PM'))]
    supervoid.iloc[:,0].value_counts()
