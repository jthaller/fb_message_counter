## fb_message_counter
Facebook allows users to download their data in the format of html files. This python program takes a given friend's name as well as the directory in which the html file or files are located, and returns several interesting graphics and statistics.

## Message Count Per Day Barplot
![alt text](https://github.com/jthaller/fb_message_counter/blob/master/example_images/David Thaller_barplot.png "Example Barplot")


## Message Count Per Day Comparison Barplot
![alt text](https://github.com/jthaller/fb_message_counter/blob/master/exampe_images/David Thaller_friendship_comparison.png "Example Barplot Comparison")


## Cumulative Sum Plot
![alt text](https://github.com/jthaller/fb_message_counter/blob/master/example_images/David_Thaller_cumsum.png "Example Cumsum Plot")


## Cumulative Sum Comparison Plot
![alt text](https://github.com/jthaller/fb_message_counter/blob/master/example_images/David_Thaller_comparison_cumsum.png "Example Cumsum Plot")

## Further Implimentaions
The following features are things I'm interested in added when I have time
- rewrite the program for the JSON file instead. Should be way easier than scraping the garbage html file facebook gives you
- Redo all the graphs but with word count. I believe this is actually the best feature for understanding conversations. People tend to break up there messages in different ways. Some people send blocks of text instead of 5 separate messages for example.
- Include word count and character count measurements. Perhaps this can be used in conjunction with machine learning to predict users based on speech patterns. I haven't done much language ML yet, but I know there are packages and implimentations that would be nice to look into at some point.
- It's kind of a pain to locate the file directory and copy paste it in. Might be worth adding a little gui to run to just navigate there and select it. It might also be possible to auto-locate it based of the name, but it's tricky because there's no way to know the exact folder title. The folders are formatted like FistnameLastnameRandomNumbers and group chats might also start with their name.
