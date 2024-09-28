from tkinter import *
import time
from tkcalendar import Calendar
from datetime import datetime, timedelta
from tkinter import messagebox
from PIL import Image, ImageTk

current_date = datetime.now()

def submit():
    if not empty_event():  # Program stops and displays an error if the 'Event' field is empty
        return
    
    if not negative_date():  # If the selected date is before todays date, the program does not start, and a warning is displayed
        return
    
    enteredTime = userTime.get() # Get time from optional time entrybox
    selected_period = var.get() # Get AM or PM selecting from radiobuttons
    #print(selected_period)

    if enteredTime == "":  # AM/PM time selection is optional, Get the time between now and the future date as proceed without adding time if not entered
        date_str = cal.get_date()
        future_date = datetime.strptime(date_str, "%m/%d/%y")
        global future_datetime
        future_datetime = datetime.combine(future_date, datetime.min.time())  #
        update_timer()  
    else:

        if len(enteredTime) == 5 and enteredTime[2] == ":": # Makes sure XX:XX has 5 characters and has colon at index 2
            try:
                hours, minutes = map(int, enteredTime.split(":")) # Splits XX:XX into XX,XX and applies int, unpacks list into hours:minutes
                #print(f"Parsed Hours: {hours}, Minutes: {minutes}")
                if 0 <= hours <= 12 and 0 <= minutes <= 59: # Validate 12 hour formart
                    if selected_period == "PM" and hours != 12: # If PM add 12 hours, if am add nothing
                        hours += 12
                    elif selected_period == "AM" and hours == 12:
                        hours = 0

                    #print(f"Parsed Hours (after conversion): {hours}, Minutes: {minutes}")    
                    date_str = cal.get_date()
                    future_date = datetime.strptime(date_str, "%m/%d/%y")
                    future_datetime = datetime.combine(future_date, datetime.min.time())  # Get the time between now and the future date
                    
                    future_datetime = future_datetime + timedelta(hours=hours, minutes=minutes) # Add the time entered by the user
                    
                    #print(f"Future DateTime: {future_datetime}")
                    
                    update_timer()  
                    return
                else:
                    messagebox.showerror("Error", "Invalid time format! Please enter time in 12-hour format!")
                    return 
            except ValueError:
                messagebox.showerror("Error", "Invalid time format! Please enter time as HH:MM.")
                return
        else:
            messagebox.showerror("Error", "Invalid time format! Please enter time as HH:MM.")
            return
    
    userTime.focus_set() # Set text curor to time entry box

    userEvent = EventName.get() # Get user entry for event 
    StartsIn.config(text=userEvent+" starts in:")  # Update the Label with the new text
    
    date_str = cal.get_date() # Get date on calendar picked by user
    future_date = datetime.strptime(date_str, "%m/%d/%y") # Converts 'date_str' in a datetime object in the format month day year
    future_datetime = datetime.combine(future_date, datetime.min.time()) # Combines future_date with a time of 00:00:00
    
    update_timer()

def update_timer():
    
    current_datetime = datetime.now() # Get the current date
    difference = future_datetime - current_datetime # Get the time difference between now and date selected by the user
    
    if difference.total_seconds() > 0:
        days, seconds = difference.days, difference.seconds
        hours = days * 24 + seconds // 3600 # Convert days and additonal seconds into hours
        minutes = (seconds % 3600) // 60 # Calculate minutes
        seconds = seconds % 60 # Remaining seconds
        
        timer.config(text=f"{hours:02}:{minutes:02}:{seconds:02}") # Display time, including zeros if the time would only be one digit
        timer.after(1000, update_timer) # Continually updates the timer
    else:
        timer.config(text="00:00:00") # When timer has reached zero, stop the timer
        messagebox.showinfo("Time's up!", "The countdown has finished!")

def update_time():
    current_time = time.strftime("%B %d, %Y %H:%M:%S")  
    RealTime.config(text="Current time: " + current_time) # Display current time in Month, Day, Year, Hours, Minutes, Seconds <- KEEPS THE TIME UPDATED
    RealTime.after(1000, update_time)  

window = Tk() # Start window
window.geometry("1280x720")
window.resizable(False,False)
window.title("Countdown Timer")
icon_path = 'images\\timer.png'
icon = Image.open(icon_path)
icon = ImageTk.PhotoImage(icon)
window.iconphoto(True,icon)

timer = Label(window,text="00:00:00", # Display 0 time before time actually starts
              font=("Bahnschrift",125))
timer.place(x=640,y=300,anchor="center")

StartsIn = Label(window,text=(" starts in:"), # Displays 'starts in:' for event is added
                font=("Bahnschrift",30))
StartsIn.place(x=640,y=200,anchor="center")

RealTime = Label(window,text="Current time: "+time.strftime("%B %d, %Y %H:%M:%S"), # Display current time in Month, Day, Year, Hours, Minutes, Seconds <- GETS THE TIME AS PROGRAM IS OPENED
                font=("Bahnschrift",20))
RealTime.place(x=5,y=0)
update_time() 

EventText = Label(window,font=("Bahnschrift", 14),text="Event Name:") # Event name entrybox
EventText.place(x=380,y=467,anchor="center")
EventName = Entry(window,font=("Arial", 14))
EventName.place(x=380,y=500,anchor="center")

var = StringVar(value="")

userTimeText = Label(window,font=("Bahnschrift", 14),text="(Optional) Enter Time:") # Optional enter time entrybox
userTimeText.place(x=640,y=467,anchor="center")
userTime = Entry(window,font=("Arial", 14))
userTime.place(x=640,y=500,anchor="center",)

amTime = Radiobutton(window,text="AM",font=("Bahnschrift", 12), variable=var, value="AM") #AM Radiobutton
amTime.place(x=610,y=535,anchor="center")

pmTime = Radiobutton(window,text="PM",font=("Bahnschrift", 12), variable=var, value="PM") #PM Radiobutton
pmTime.place(x=670,y=535,anchor="center")

cal = Calendar(window, selectmode = 'day', # Create calendar with the inital selected date as today
               year=current_date.year, 
               month=current_date.month,
               day=current_date.day)
 
cal.place(x=920,y=500,anchor="center") # Place calendar

SubmitButton = Button(window,text="Submit",font=("Bahnschrift", 14),command=submit) # Submit button
SubmitButton.place(x=640,y=600,anchor="center")

def empty_event(): # Function makes sure event field has some input
    eventSpace = EventName.get()
    if eventSpace == "":
        messagebox.showwarning("Warning","Please enter an event.")
        return False
    return True

def negative_date(): # Function checks if date is before todays date
    date_check = cal.get_date()
    selected_date = datetime.strptime(date_check, "%m/%d/%y").date()  
    if selected_date < current_date.date():  
        messagebox.showwarning("Warning", "Selected date is before today's date.")
        return False
    return True

window.mainloop()