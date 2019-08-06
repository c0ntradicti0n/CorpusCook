
Overall
=======

This is a server client pair, that allows multiple users to help me building a corpus.

The server does storing and doing stuff with AI on the text.
the app is for presenting results and collecting more information, that humans understand by reading the text.

To start the server
===================

    python server.py
    
The server serves as a very simple cloud service 

  * to store and send the text to be annotated, 
  
  * host the model to annotate the text snippets, the users made
  
  * to receive the annotations, the users also made
    
The server uses scraped webfiles from differncebetween.net 
and extracts the text from the pages.

that can be retrieved

To start the app
================

    python main.py
    
The app was built like this to run it on android and going by subways and tram.
For deploying, it must be androidized with buildozer from the kivy widget wizard.

So in the end, there is a APK file, that can be downloaded and run on Android Phones (at least).

