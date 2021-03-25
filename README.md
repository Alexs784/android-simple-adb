# Android simple adb

## Description

This is a simple pytthon desktop application that allows creating _scripts_ of `adb` commands.

What is a script in this case?
A database object with a group of commands chosen by the user.

## How to use
The first screen is the following one, where you need to add your Android SDK location (both full user path and abbreviate one (`~`) are supported).
<img width="912" alt="Screenshot 2021-03-21 at 21 13 50" src="https://user-images.githubusercontent.com/4242258/111919566-fa09d380-8a8a-11eb-9025-f22794996acf.png">

After that you get to the home screen: here you can bothj view saved scripts or create one.

Opening a script (both creating or opening an existing one) will show the current _steps_ (`adb` commands) added to it and give you a few options:
- Run the script
- Save the script (choose a name)
- Add steps to the scripts (enabled once you choose a device from the relative menu)
- Select a device (necessary to add steps, devices shown are the ones **currently** connected to the machine)

<img width="912" alt="Screenshot 2021-03-25 at 20 37 46" src="https://user-images.githubusercontent.com/4242258/112533313-1ae36900-8daa-11eb-9a0b-304064024318.png">

Once you select a device and click on "Add step", you will be able to choose trhe desired step(s):
<img width="912" alt="Screenshot 2021-03-21 at 21 22 34" src="https://user-images.githubusercontent.com/4242258/111919686-8fa56300-8a8b-11eb-851b-e17b179458fe.png">

Choosing a step may or may not ask extra parameters (depending on if they are required by the step). After choosing the desired one(s) and adding them, going back we will have an overview of what steps we did add
<img width="912" alt="Screenshot 2021-03-25 at 20 39 19" src="https://user-images.githubusercontent.com/4242258/112533426-38b0ce00-8daa-11eb-9485-42b10ca419f5.png">


From here we can run the script, save it or add more steps. We can also change device and add steps relative to that device.

## Currently supported (tested) platforms:

- MacOS Big Sur


## What's next
- [ ] Test Windows support
- [ ] Test Linux support
- [x] Improve step's parameter input UI by adding parameter descriptions
- [ ] Option to see each step's adb command(s)
- [ ] Option to delete a step from a script
- [x] Option to delete a script
- [ ] Option to search adb commands
- [ ] Support more adb commands
- [ ] Auto detect Android SDK
