# Top Ten Songs
Displays the top ten songs from an artist and which track on which album that song is on via text.
### Set-up
There are a few things that need to be done before this can be used:
1. You will need to create an account on Spotify for Developers in order to obtain a Client ID key as well as a Client Secret key. To do this, follow this link: https://developer.spotify.com/dashboard/. I put these in a database that I access in order to use them.
2. Create a Twilio account and obtain a Twilio phone number. They have a free trail you can take advantage of so you can play around with it. https://www.twilio.com/
3. Next, download ngrok. https://ngrok.com/
### How to use
Run the code. 

Then, you'll have to use ngrok by opening a terminal and typing in ``` ngrok http 5000 ```. Copy the https URL.

Then, sign in to Twilio, go to Phone Numbers, click on the phone number, and in the bottom, under Messaging, you'll paste the url in the "A MESSAGE COMES IN" section and end it with ```/sms``` and click save. Now, you can text the Twilio number the name of an artist, and you'll receive the results in a few seconds. If you are texting the number through a different number than what was used to create the Twilio account, you will need to verify the number with Twilio first.
