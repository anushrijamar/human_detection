from playsound import playsound
user_input = input("Enter 1 to play the alarm sound, or 0 to do nothing: ")
if user_input == '1':
    print("Playing alarm sound...")
    playsound('D:\human_detection_ui/flask_server/alarm/alarm_sound.mp3') 
else:
    print("No alarm triggered.")
