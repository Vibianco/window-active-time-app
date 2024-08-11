from AppKit import NSWorkspace
import time, os, keyboard

print("Welcome! To track the active time of a window, you need to open a second Chrome window and rename it 'WORK'.")
print("To stop the application and see the total maximized time, press CTRL + C")
print("To clear the accumulated time, press SHIFT + F")
print("To pause or resume the application, press SHIFT + G")
print("To check the total accumulated time, press SHIFT + T")

# File to store the accumulated time
filename = 'accumulated_time.txt'

# Read the total accumulated time from the file
def read_total_time(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            total_time = float(file.read().strip())
    else:
        total_time = 0
    return total_time

# Write the total accumulated time to the file
def write_total_time(filename, total_time):
    with open(filename, 'w') as file:
        file.write(str(total_time))

# Clear the accumulated time in the file
def clear_total_time(filename):
    with open(filename, 'w') as file:
        file.write('0')

# Print the total accumulated time
def print_total_time(total_time):
    hours, minutes, seconds = seconds_to_hms(total_time)
    print(f'Total accumulated active time: {hours}:{minutes}:{seconds}')

# Handle the exit process: print and save the total accumulated time
def handle_exit(total_time):
    hours, minutes, seconds = seconds_to_hms(total_time)
    print('Application stopped by the user.')
    print_total_time(total_time)
    write_total_time(filename, total_time)

# Check if the 'WORK' window is active
def is_work_maximized():
    active_app = NSWorkspace.sharedWorkspace().activeApplication()
    if active_app and active_app['NSApplicationName'] == "Google Chrome":
        active_window_title = active_app['NSApplicationProcessIdentifier']
        windows = os.popen(f"osascript -e 'tell application \"Google Chrome\" to get the title of every window'").read().split(", ")
        for window in windows:
            if window == 'WORK':
                return True
    return False

# Convert seconds to hours, minutes and seconds
def seconds_to_hms(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return hours, minutes, seconds

start_time = None
total_time = read_total_time(filename)
is_paused = False

try:
    while True:
        if keyboard.is_pressed('shift+F'):
            clear_total_time(filename)
            total_time = 0
            print("Accumulated time has been cleared.")
            time.sleep(1)
        
        if keyboard.is_pressed('shift+G'):
            is_paused = not is_paused
            state = "paused" if is_paused else "resumed"
            print(f"Application is now {state}.")
            time.sleep(1)
        
        if keyboard.is_pressed('shift+T'):
            print_total_time(total_time)
            time.sleep(1)

        if not is_paused:
            if is_work_maximized():
                if start_time is None:
                    start_time = time.time()
            else:
                if start_time is not None:
                    elapsed_time = time.time() - start_time
                    total_time += elapsed_time
                    hours, minutes, seconds = seconds_to_hms(elapsed_time)
                    print(f'Active time: {hours}:{minutes}:{seconds}')
                    start_time = None
                    write_total_time(filename, total_time)
        time.sleep(1)

except KeyboardInterrupt:
    handle_exit(total_time)