# Android simple adb

## Description

This is a simple python desktop application that allows creating _scripts_ of `adb` commands.

What is a script in this case?
A database object with a group of commands chosen by the user.

## How to use
The first screen is the following one, where you need to add your Android SDK location (both full user path and abbreviate one (`~`) are supported).
<img width="912" alt="Screenshot 2021-03-21 at 21 13 50" src="https://user-images.githubusercontent.com/4242258/111919566-fa09d380-8a8a-11eb-9025-f22794996acf.png">

After that you get to the home screen: here you can both view saved scripts or create one.

Opening a script (both creating or opening an existing one) will show the current _steps_ (`adb` commands) added to it and give you a few options:
- Run the script on the currently selected device (devices shown are the ones **currently** connected to the machine)
- Save the script (choose a name)
- Duplicate the script (including its steps)
- Add steps to the scripts (enabled once you choose a device from the relative menu)
- Drag and drop steps added to a script to change order of execution
- View and delete a step of the script

<img width="912" alt="Screenshot 2021-06-13 at 23 20 07" src="https://user-images.githubusercontent.com/4242258/121822604-3f135f80-cca0-11eb-93af-1aa6e0988599.png">


Once you select a device and click on "Add step", you will be able to choose the desired step(s):
<img width="912" alt="Screenshot 2021-03-21 at 21 22 34" src="https://user-images.githubusercontent.com/4242258/111919686-8fa56300-8a8b-11eb-851b-e17b179458fe.png">

Choosing a step may or may not ask extra parameters (depending on if the step requires them). After choosing the desired one(s) and adding them, going back we will have an overview of what steps we did add
<img width="912" alt="Screenshot 2021-06-13 at 23 31 45" src="https://user-images.githubusercontent.com/4242258/121822619-52bec600-cca0-11eb-9135-92abf258f191.png">


From here we can run the script, save it, add more steps, reorder them or delete existing ones. We can also run the script on a different device by changing the target one.

Clicking on a step added to a script will show the adb commmand that that step executes and offers the option to delete the step from the current script:
<img width="912" alt="Screenshot 2021-03-28 at 20 05 56" src="https://user-images.githubusercontent.com/4242258/112762685-4318d500-9001-11eb-8fd8-eea5a18584a0.png">


## Currently supported (tested) platforms:

- MacOS Big Sur
- MacOS Sonoma


## What's next
- [ ] Test Windows support
- [ ] Test Linux support
- [x] Improve step's parameter input UI by adding parameter descriptions
- [x] Option to see each step's adb command(s)
- [x] Option to delete a step from a script
- [x] Option to delete a script
- [x] Option to duplicate a script
- [ ] Option to search adb commands
- [ ] Support more adb commands
- [ ] Auto detect Android SDK
