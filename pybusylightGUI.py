import tkinter as tk
from pybusylight import pybusylight

class ExampleApp(tk.Frame):
    ''' An example application for TkInter.  Instantiate
        and call the run method to run. '''
    def __init__(self, master):
        
        try:
            print('Connect to the Busylight...')
            self.bl=pybusylight.busylight()
        except ValueError:
            print('\nBusylight not found, is it connected?...')
            exit(1)
    
        # Initialize window using the parent's constructor
        tk.Frame.__init__(self,
                          master,
                          width=300,
                          height=560)
        
    
        # Set the title
        self.master.title('BusyLight for Linux')
 
        # This allows the size specification to take effect
        self.pack_propagate(0)
 
        # We'll use the flexible pack layout manager
        self.pack()
 
        # The greeting selector
        # Use a StringVar to access the selector's value
#         self.greeting_var = tk.StringVar()
#         self.greeting = tk.OptionMenu(self,
#                                       self.greeting_var,
#                                       'hello',
#                                       'goodbye',
#                                       'heyo')
#         self.greeting_var.set('hello')
#  
#         # The recipient text entry control and its StringVar
#         self.recipient_var = tk.StringVar()
#         self.recipient = tk.Entry(self,
#                                   textvariable=self.recipient_var)
#         self.recipient_var.set('world')
 
        # Color buttons
        # RED, GREEN, BLUE, PINK, ORANGE, YELLOW, PURPLE
        self.color_label = tk.Label(self, text="COLORS", font='Roboto 14 bold')
        self.red_button = tk.Button(self, command=lambda: self.bl.setColor(0),bg="#FF0000")
        self.green_button = tk.Button(self, command=lambda: self.bl.setColor(1),bg="#00FF00")
        self.blue_button = tk.Button(self, command=lambda: self.bl.setColor(2),bg="#0000FF")        
        self.pink_button = tk.Button(self, command=lambda: self.bl.setColor(3),bg="pink")
        self.orange_button = tk.Button(self, command=lambda: self.bl.setColor(4),bg="orange")
        self.yellow_button = tk.Button(self, command=lambda: self.bl.setColor(5),bg="#FFFF00")        
        self.purple_button = tk.Button(self, command=lambda: self.bl.setColor(6),bg="#B400E1")
        
        # Sound buttons
        self.sound_label = tk.Label(self, text="SOUNDS", font='Roboto 14 bold')
        self.funky_button = tk.Button(self, text="FUNKY", command=lambda: self.bl.set_sound(0), bg="white")
        self.nordic_button = tk.Button(self, text="NORDIC", command=lambda: self.bl.set_sound(1), bg="white")
        self.quiet_button = tk.Button(self, text="QUIET", command=lambda: self.bl.set_sound(2), bg="white")
        self.open_button = tk.Button(self, text="OPEN OFFICE", command=lambda: self.bl.set_sound(3), bg="white")
        self.kuando_button = tk.Button(self, text="KUANDO", command=lambda: self.bl.set_sound(4), bg="white")
 
        # Control buttons
        # Blinking button
        self.control_label = tk.Label(self, text="CONTROL", font='Roboto 14 bold')        
        self.blinkOn = False       
        self.blink_button = tk.Button(self, text="Blink ON", command=lambda: self.toggleBlinking())
        
        self.close_button = tk.Button(self, command=self.bl.close, text="Close")
        self.off_button = tk.Button(self, command=self.bl.turn_off, text="Off")
                   
        # Put the controls on the form
        self.color_label.pack(fill=tk.X, side=tk.TOP)
        self.red_button.pack(fill=tk.X, side=tk.TOP)
        self.yellow_button.pack(fill=tk.X, side=tk.TOP)
        self.green_button.pack(fill=tk.X, side=tk.TOP)
        self.blue_button.pack(fill=tk.X, side=tk.TOP)
        self.pink_button.pack(fill=tk.X, side=tk.TOP)
        self.orange_button.pack(fill=tk.X, side=tk.TOP)
        self.purple_button.pack(fill=tk.X, side=tk.TOP)  
        self.sound_label.pack(fill=tk.X, side=tk.TOP)
        self.funky_button.pack(fill=tk.X, side=tk.TOP)
        self.nordic_button.pack(fill=tk.X, side=tk.TOP)
        self.quiet_button.pack(fill=tk.X, side=tk.TOP)
        self.open_button.pack(fill=tk.X, side=tk.TOP)
        self.kuando_button.pack(fill=tk.X, side=tk.TOP)      

        self.close_button.pack(fill=tk.X, side=tk.BOTTOM)       
        self.off_button.pack(fill=tk.X, side=tk.BOTTOM)
        self.blink_button.pack(fill=tk.X, side=tk.BOTTOM)               
        self.control_label.pack(fill=tk.X, side=tk.BOTTOM)
        
    def toggleBlinking(self):
        self.blinkOn = not self.blinkOn
        self.bl.setBlink(self.blinkOn)
        if self.blinkOn:
            self.blink_button.config(text="Blink OFF")
        else:
            self.blink_button.config(text="Blink ON")
 
    def run(self):
        ''' Run the app '''
        self.mainloop()

app = ExampleApp(tk.Tk())
app.run()
