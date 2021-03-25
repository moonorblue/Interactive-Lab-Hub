# You're a wizard, Kae-Jer

<img src="https://pbs.twimg.com/media/Cen7qkHWIAAdKsB.jpg" height="400">

In this lab, we want you to practice wizarding an interactive device as discussed in class. We will focus on audio as the main modality for interaction but there is no reason these general techniques can't extend to video, haptics or other interactive mechanisms. In fact, you are welcome to add those to your project if they enhance your design.


## Text to Speech and Speech to Text

In the home directory of your Pi there is a folder called `text2speech` containing some shell scripts.

```
pi@ixe00:~/text2speech $ ls
Download        festival_demo.sh  GoogleTTS_demo.sh  pico2text_demo.sh
espeak_demo.sh  flite_demo.sh     lookdave.wav

```

you can run these examples by typing 
`./espeakdeom.sh`. Take some time to look at each script and see how it works. You can see a script by typing `cat filename`

```
pi@ixe00:~/text2speech $ cat festival_demo.sh 
#from: https://elinux.org/RPi_Text_to_Speech_(Speech_Synthesis)#Festival_Text_to_Speech

echo "Just what do you think you're doing, Dave?" | festival --tts

```

You can also play audio files directly with `aplay filename`.

After looking through this folder do the same for the `speech2text` folder. In particular, look at `test_words.py` and make sure you understand how the vocab is defined. Then try `./vosk_demo_mic.sh`

## Serving Pages

In Lab 1 we served a webpage with flask. In this lab you may find it useful to serve a webpage for the controller on a remote device. Here is a simple example of a webserver.

```
pi@ixe00:~/$ python server.py
 * Serving Flask app "server" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 162-573-883
```
From a remote browser on the same network, check to make sure your webserver is working by going to [http://ixe00.local:5000]()


## Demo

In the [demo directory](./demo), you will find an example wizard of oz project you may use as a template. **You do not have to** feel free to get creative. In that project, you can see how audio and sensor data is streamed from the Pi to a wizard controller that runs in the browser. You can control what system says from the controller as well.

## Optional

There is an included [dspeech](./dspeech) demo that uses [Mozilla DeepSpeech](https://github.com/mozilla/DeepSpeech) for speech to text. If you're interested in trying it out we suggest you create a seperarate virutalenv. 



# Lab 3 Part 2

Create a system that runs on the Raspberry Pi that takes in one or more sensors and requires participants to speak to it. Document how the system works and include videos of both the system and the controller.

## Prep for Part 2

Idea: A mini crypto market helper, use voice to control the device to show data

<img src="https://github.com/moonorblue/Interactive-Lab-Hub/blob/Spring2021/Lab%203/Untitled%20(Draft)-1%203.jpg?raw=true">

## Share your idea sketches with Zoom Room mates and get feedback

*what was the feedback? Who did it come from?*

Justin Liu: This is so cool! Are these data real-time?

Jeff Lu: Very fancy feature, can you place order with it?

Cheng-Wei Hu: Wow, really amazing, can you use it to make money?

## Prototype your system

The system should:
* use the Raspberry Pi 
* use one or more sensors
* require participants to speak to it. 

*Document how the system works*

The system works in a very straightforward way; after the user asks the device to show the cryptocurrency market data, it will show the data on the screen. The user can ask the device to show more than one market data, (the default one is BTC), the user can ask the device to show other market data. Besides adding market data, the user can ask the device to speed up the data update frequency. Here I use the button pressing to act like how the device receives the voice command. 

*Include videos or screencaptures of both the system and the controller.*

[Video here](https://drive.google.com/file/d/1sp6yZdiph-kIt9fkr9pUq0Mwa2ep3U0G/view?usp=sharing)

## Test the system
Try to get at least two people to interact with your system. (Ideally, you would inform them that there is a wizard _after_ the interaction, but we recognize that can be hard.)

Answer the following:

### What worked well about the system and what didn't?

The device worked well with showing the data with the according "voice command", it can update the data immediately. For what didn't work well, normal user kind of don't know the purpose of the device, the numbers on the screen were not meaningful for people who're not interested in cryptocurrency

### What worked well about the controller and what didn't?

The controller works efficiently, can immediately respond to the "voice command" and show the corresponded function, but the buttons were quite simple controllers, it's hard to make complicated features with them. 


### What lessons can you take away from the WoZ interactions for designing a more autonomous version of the system?

We'll limit the functions or the features of the system if we only use the "WoZ" like interactions; if we let users try the device with more flexibility, it's possible to come up with more new ideas for the device  


### How could you use your system to create a dataset of interaction? What other sensing modalities would make sense to capture?

I can use my system to record how users talk to the device, with other related data, like time, sentence length, etc.
I think if we can capture the photos or videos of the user when they are using the device might be interesting; perhaps we can understand their mood or their reactions by their face or body language. 

