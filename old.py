#!/usr/bin/env python3.8

import threading
import os
import getpass
import datetime
import time
#import fpdf
from tkinter import StringVar
import tkinter
import customtkinter as ctk
from PIL import Image, ImageTk
import matplotlib
import numpy as np
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from meerstetter import Meerstetter

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('green')

class App(ctk.CTk):
	WIDTH = 780
	HEIGHT = 520

	# Thermocycler Settings:
	thermocyclers = {
		'clamps': {
			'A': True, # True (Raised, homed), False (Lowered)
			'B': True,
			'C': True,
			'D': True,
			},
		'trays': {
			'AB': True, # True (Open, homed), False (Closed),
			'CD': True, # True (Open, homed), False (Closed),
			},
		'temperatures': {
			'A': np.array([84,84, 55, 55, 84, 84]),
			'B': np.array([84,84, 60, 60, 84, 84]),
			'C': np.array([84,84, 55, 55, 84, 84]),
			'D': np.array([84,84, 55, 55, 84, 84]),
			},
		'times': {
			'A': {'denature': 5, 'anneal': 80, 'extension': 40},
			'B': {'denature': 10, 'anneal': 80, 'extension': 40},
			'C': {'denature': 5, 'anneal': 80, 'extension': 40},
			'D': {'denature': 5, 'anneal': 80, 'extension': 40},
			},
		'trays': {
			'AB': {'homed': True},
			'CD': {'homed': True},
			},
		'clamps': {
			'A': {'homed': True},
			'B': {'homed': True},
			'C': {'homed': True},
			'D': {'homed': True},
			},
		'cycles': {
			'A': 45,
			'B': 45,
			'C': 45,
			'D': 45,
			},
		}
	thermocycler_dict = {
			'A': True,
			'B': True,
			'C': True,
			'D': True,
			'AB': True,
			'CD': True,
		}						
	thermocycler_png_name = 'thermocycler.png'

	def __init__(self):
		super().__init__()
		self.use_z = tkinter.IntVar()
		self.use_z.set(1)
		self.slow_z = tkinter.IntVar()
		self.slow_z.set(1)
		self.pipette_tip_type = StringVar()
		self.pipette_tip_type.set('None')
		self.dx = StringVar()
		self.dx.set('500')
		self.dy = StringVar()
		self.dy.set('5000')
		self.dz = StringVar()
		self.dz.set('5000')
		self.bind('<Motion>', self.motion)
		
		self.title("CDP 2.0 GUI")
		self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
		self.protocol("WM_DELETE_WINDOW", self.on_closing)
		
		# Create two frames.
		self.grid_columnconfigure(1, weight=1)
		self.grid_rowconfigure(0, weight=1)
		
		self.frame_left = ctk.CTkFrame(master=self, width=180, corner_radius=0)
		self.frame_left.grid(row=0, column=0, sticky='nswe')

		self.frame_right = ctk.CTkFrame(master=self)
		self.frame_right.grid(row=0, column=1, sticky='nswe', padx=20, pady=10, columnspan=3)

		# Left Frame.
		self.label_1 = ctk.CTkLabel(master=self.frame_left, text="CDP 2.0", font=("Roboto Medium", -16))
		self.label_1.grid(row=1, column=0, pady=10, padx=10)
		self.button_1 = ctk.CTkButton(master=self.frame_left, text='Image', command=lambda button_text='Image': self.on_button_click(button_text))
		self.button_1.grid(row=2, column=0, pady=10, padx=20)
		self.button_2 = ctk.CTkButton(master=self.frame_left, text='Thermocycle', command=lambda button_text='Thermocycle': self.on_button_click(button_text))
		self.button_2.grid(row=3, column=0, pady=10, padx=20)
		self.button_3 = ctk.CTkButton(master=self.frame_left, text="Build Protocol", command=lambda button_text="Build Protocol": self.on_button_click(button_text))
		self.button_3.grid(row=4, column=0, pady=10, padx=20)
		self.button_optimize = ctk.CTkButton(master=self.frame_left, text='Optimize', command=lambda button_text='Optimize': self.on_button_click(button_text))
		self.button_optimize.grid(row=5, column=0, pady=10, padx=20)
		self.button_4 = ctk.CTkButton(master=self.frame_left, text='Service', command=lambda button_text='Service': self.on_button_click(button_text))
		self.button_4.grid(row=6, column=0, pady=10, padx=20)

	def on_button_click(self, button_text):
		# Clean up the Right Frame for updating
		for widget in self.frame_right.winfo_children():
			widget.destroy()
		if button_text == 'Image':
			self.label_image_1 = ctk.CTkLabel(master=self.frame_right, text='Image', font=("Roboto Medium", -16))
			self.label_image_1.grid(row=1, column=0, pady=10, padx=10)
		elif button_text == 'Thermocycle':
			#self.label_thermocycle_1 = ctk.CTkLabel(master=self.frame_right, text="Denature Temperature (Celsius)", font=("Roboto Medium", -16))
			#self.label_thermocycle_1.grid(row=1, column=0, pady=10, padx=10)
			#self.entry_thermocycle_1 = ctk.CTkEntry(master=self.frame_right)
			#self.entry_thermocycle_1.grid(row=1, column=1, pady=20, padx=20)
			self.label_thermocycler_title = ctk.CTkLabel(master=self.frame_right, text="Thermocycle Protocol", font=("Roboto Bold", -20))
			self.label_thermocycler_title.place(x=50, y=0)
			self.label_thermocycler = ctk.CTkLabel(master=self.frame_right, text='Thermocycler', font=("Roboto Light", -16))
			self.label_thermocycler.place(x=0, y=40)
			thermocycler_options = StringVar()
			thermocycler_options.set('A')
			self.optionmenu_thermocycler = ctk.CTkOptionMenu(master=self.frame_right, variable=thermocycler_options, values=('A', 'B', 'C', 'D'), command=self.callback_update_thermocycler_protocol)
			thermocycler = str(self.optionmenu_thermocycler.cget('variable').get())
			self.optionmenu_thermocycler.place(x=150, y=40)
			self.label_thermocycler_cycles = ctk.CTkLabel(master=self.frame_right, text='Cycles', font=("Roboto Light", -16))
			self.label_thermocycler_cycles.place(x=0, y=80)
			thermocycler_cycles_sv = StringVar()
			thermocycler_cycles_sv.set(str(self.thermocyclers['cycles'][thermocycler]))
			self.entry_thermocycler_cycles = ctk.CTkEntry(master=self.frame_right, textvariable=thermocycler_cycles_sv)
			self.entry_thermocycler_cycles.bind('<FocusOut>', self.callback_thermocycler_cycles)
			self.entry_thermocycler_cycles.place(x=150, y=80)
			image = Image.open(self.thermocycler_png_name).resize((250, 470))
			self.img_thermocycler = ImageTk.PhotoImage(image)
			self.label_thermocycler = ctk.CTkLabel(master=self.frame_right, text='thermocycler', font=("Roboto Light", -1), image=self.img_thermocycler)
			self.label_thermocycler.place(x=310, y=5) 
			self.label_thermocycler.bind('<Button-1>', self.on_click)
			self.button_start_thermocyclers = ctk.CTkButton(master=self.frame_right, text='Start', command=self.start_thermocyclers)
			self.button_start_thermocyclers.place(x=5, y=445, width=100)
			self.button_import = ctk.CTkButton(master=self.frame_right, text='Import', command=self.import_thermocyclers)
			self.button_import.place(x=115, y=445, width=95)
			self.button_export = ctk.CTkButton(master=self.frame_right, text='Export', command=self.export_thermocyclers)
			self.button_export.place(x=215, y=445, width=95) 
			#fig = Figure(figsize=(3,2.4))
			#a = fig.add_subplot(111)
			#data = np.array([92,92,55,55,84,84])
			#x = np.array([1,2,3,4,5,6])
			#a.set_yticks([92,55,84])
			#a.set_xticks([])
			#a.axvline(x=2.5)
			#a.axvline(x=4.5)
			#a.plot(x, data, color='red')
			#canvas = FigureCanvasTkAgg(fig, master=self.frame_right)
			#canvas.get_tk_widget().place(x=10, y=120)
			#canvas.draw()
			self.plot_thermocycler(self.thermocyclers['temperatures']['A'])
			self.label_thermocycler_denature = ctk.CTkLabel(master=self.frame_right, bg_color="white", text_color='black', text='Denature', font=("Roboto Light",-16))
			self.label_thermocycler_denature.place(x=10, y=120, width=100)
			self.label_thermocycler_anneal = ctk.CTkLabel(master=self.frame_right, bg_color="white", text_color='black', text='Anneal', font=("Roboto Light", -16))
			self.label_thermocycler_anneal.place(x=110, y=120, width=100)
			self.label_thermocycler_extension = ctk.CTkLabel(master=self.frame_right, bg_color="white", text_color='black', text='Extension', font=("Roboto Light", -16))
			self.label_thermocycler_extension.place(x=210, y=120, width=100)
			image = Image.open('thermostat.png').resize((24,24))
			self.img_thermostat = ImageTk.PhotoImage(image)
			self.label_thermostat = ctk.CTkLabel(master=self.frame_right, text='', bg_color='white', image=self.img_thermostat)
			self.label_thermostat.place(x=15, y=365)
			thermocycler = str(self.optionmenu_thermocycler.cget('variable').get())
			thermostat_denature_sv = StringVar()
			thermostat_denature_sv.set(str(self.thermocyclers['temperatures'][thermocycler][0]))
			self.entry_thermostat_denature = ctk.CTkEntry(master=self.frame_right, width=40, textvariable=thermostat_denature_sv)
			self.entry_thermostat_denature.bind('<FocusOut>', self.callback_thermocycler_temperatures)
			self.entry_thermostat_denature.place(x=65, y=365)
			thermostat_anneal_sv = StringVar()
			thermostat_anneal_sv.set(str(self.thermocyclers['temperatures'][thermocycler][2]))
			self.entry_thermostat_anneal = ctk.CTkEntry(master=self.frame_right, width=40, textvariable=thermostat_anneal_sv)
			self.entry_thermostat_anneal.bind('<FocusOut>', self.callback_thermocycler_temperatures)
			self.entry_thermostat_anneal.place(x=145, y=365)
			thermostat_extension_sv = StringVar()
			thermostat_extension_sv.set(str(self.thermocyclers['temperatures'][thermocycler][4]))
			self.entry_thermostat_extension = ctk.CTkEntry(master=self.frame_right, width=40, textvariable=thermostat_extension_sv)
			self.entry_thermostat_extension.bind('<FocusOut>', self.callback_thermocycler_temperatures)
			self.entry_thermostat_extension.place(x=225, y=365)
			self.label_units_denature_C = ctk.CTkLabel(master=self.frame_right, text='C', font=("Roboto Light",-16))
			self.label_units_anneal_C = ctk.CTkLabel(master=self.frame_right, text='C', font=("Roboto Light",-16))
			self.label_units_extension_C = ctk.CTkLabel(master=self.frame_right, text='C', font=("Roboto Light",-16))
			self.label_units_denature_C.place(x=107, y=365)
			self.label_units_anneal_C.place(x=187, y=365)
			self.label_units_extension_C.place(x=267, y=365)
			image = Image.open('clock.png').resize((24,24))
			self.img_clock = ImageTk.PhotoImage(image)
			self.label_clock = ctk.CTkLabel(master=self.frame_right, text='', bg_color='white', image=self.img_clock)
			self.label_clock.place(x=15, y=395)
			clock_denature_sv = StringVar()
			clock_denature_sv.set(str(self.thermocyclers['times'][thermocycler]['denature']))
			self.entry_clock_denature = ctk.CTkEntry(master=self.frame_right, width=40, textvariable=clock_denature_sv)
			self.entry_clock_denature.bind('<FocusOut>', self.callback_thermocycler_times)
			self.entry_clock_denature.place(x=65, y=395)
			clock_anneal_sv = StringVar()
			clock_anneal_sv.set(str(self.thermocyclers['times'][thermocycler]['anneal']))
			self.entry_clock_anneal = ctk.CTkEntry(master=self.frame_right, width=40, textvariable=clock_anneal_sv)
			self.entry_clock_anneal.bind('<FocusOut>', self.callback_thermocycler_times)
			self.entry_clock_anneal.place(x=145, y=395)
			clock_extension_sv = StringVar()
			clock_extension_sv.set(str(self.thermocyclers['times'][thermocycler]['extension']))
			self.entry_clock_extension = ctk.CTkEntry(master=self.frame_right, width=40, textvariable=clock_extension_sv)
			self.entry_clock_extension.bind('<FocusOut>', self.callback_thermocycler_times)
			self.entry_clock_extension.place(x=225, y=395)
			self.label_units_denature_time = ctk.CTkLabel(master=self.frame_right, text='min', font=("Roboto Light",-16))
			self.label_units_anneal_time = ctk.CTkLabel(master=self.frame_right, text='sec', font=("Roboto Light",-16))
			self.label_units_extension_time = ctk.CTkLabel(master=self.frame_right, text='sec', font=("Roboto Light",-16))
			self.label_units_denature_time.place(x=107, y=395)
			self.label_units_anneal_time.place(x=187, y=395)
			self.label_units_extension_time.place(x=267, y=395)
		elif button_text == "Build Protocol":
			self.label_build_protocol_1 = ctk.CTkLabel(self.frame_right, text="Build Protocol", font=("Roboto Medium", -16))
			self.label_build_protocol_1.grid(row=1, column=0, pady=10, padx=10)
		elif button_text == 'Optimize':
			image = Image.open('deck_plate.png').resize((560, 430))
			self.img_deck_plate = ImageTk.PhotoImage(image)
			self.label_deck_plate = ctk.CTkLabel(master=self.frame_right, text='deck_plate', font=("Roboto Medium", -1), image=self.img_deck_plate)
			self.label_deck_plate.bind('<ButtonPress-1>', self.on_click)
			self.label_deck_plate.bind('<ButtonRelease-1>', self.on_release)
			self.label_deck_plate.bind('<MouseWheel>', self.mouse_wheel)
			self.label_deck_plate.place(x=0, y=40) 
			self.label_dx = ctk.CTkLabel(master=self.frame_right, text='dx', font=("Roboto Medium", -10))
			self.label_dx.place(x=195, y=35)
			self.entry_dx = ctk.CTkEntry(master=self.frame_right, width=70, textvariable=self.dx, font=("Roboto Medium", -10), height=10) 
			self.entry_dx.bind('<FocusOut>', self.callback_dx)
			self.entry_dx.place(x=220, y=40)
			self.label_dy = ctk.CTkLabel(master=self.frame_right, text='dy', font=("Roboto Medium", -10))
			self.label_dy.place(x=195, y=55)
			self.entry_dy = ctk.CTkEntry(master=self.frame_right, width=70, textvariable=self.dy, font=("Roboto Medium", -10), height=10) 
			self.entry_dy.bind('<FocusOut>', self.callback_dy)
			self.entry_dy.place(x=220, y=60)
			self.label_dz = ctk.CTkLabel(master=self.frame_right, text='dz', font=("Roboto Medium", -10))
			self.label_dz.place(x=195, y=75)
			self.entry_dz = ctk.CTkEntry(master=self.frame_right, width=70, textvariable=self.dz, font=("Roboto Medium", -10), height=10) 
			self.entry_dz.bind('<FocusOut>', self.callback_dz)
			self.entry_dz.place(x=220, y=80)
			self.label_consumable = ctk.CTkLabel(master=self.frame_right, text='Consumable', font=("Roboto Medium", -16))
			self.label_consumable.place(x=5, y=5, width=90)
			consumable_options = StringVar()
			consumable_options.set('')
			self.optionmenu_consumable = ctk.CTkOptionMenu(master=self.frame_right, variable=consumable_options, values=("Tip Tray", "Reagent Cartridge", "Sample Rack", "Aux Heater", "Heater/Shaker", "Mag Separator", "Chiller", "Pre-Amp Thermocycler", "Lid Tray", "Tip Transfer Tray", "Quant Strip", "Assay Strip"))
			self.optionmenu_consumable.place(x=100, y=5, width=190)
			self.label_tray = ctk.CTkLabel(master=self.frame_right, text='Tray', font=("Roboto Medium", -16))
			self.label_tray.place(x=295, y=5, width=40)
			tray_options = StringVar()
			tray_options.set('')
			self.optionmenu_tray = ctk.CTkOptionMenu(master=self.frame_right, variable=tray_options, values=('A', 'B', 'C', 'D'))
			self.optionmenu_tray.place(x=340, y=5, width=60)
			self.label_column = ctk.CTkLabel(master=self.frame_right, text='Column', font=("Roboto Medium", -16))
			self.label_column.place(x=400, y=5, width=80)
			column_options = StringVar()
			column_options.set('')
			self.optionmenu_column = ctk.CTkOptionMenu(master=self.frame_right, variable=column_options, values=('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'))
			self.optionmenu_column.place(x=480, y=5, width=60)
			self.label_tip = ctk.CTkLabel(master=self.frame_right, text='Tip Size (uL)', font=("Roboto Medium", -16))
			self.label_tip.place(x=330, y=470)
			self.optionmenu_tip = ctk.CTkOptionMenu(master=self.frame_right, variable=self.pipette_tip_type, values=('1000', '50', '200', 'None'))
			self.optionmenu_tip.place(x=435, y=470, width=100)
			self.checkbox_use_z = ctk.CTkCheckBox(master=self.frame_right, text="Use Z", variable=self.use_z, onvalue=1, offvalue=0) 
			self.checkbox_use_z.place(x=330, y=40, width=100)
			self.checkbox_slow_z = ctk.CTkCheckBox(master=self.frame_right, text="Slow Z", variable=self.slow_z, onvalue=1, offvalue=0)
			self.checkbox_slow_z.place(x=330, y=70, width=100)
			self.button_print = ctk.CTkButton(master=self.frame_right, text='Print', font=("Roboto Medium", -16), width=60, command=self.print_coordinate, height=45)
			self.button_print.place(x=410, y=45)
			self.button_update = ctk.CTkButton(master=self.frame_right, text='Update', font=("Roboto Medium", -16), width=60, command=self.update_coordinate, height=45, fg_color='#4C7BD3') 
			self.button_update.place(x=480, y=45)
		elif button_text == 'Service':
			self.label_service_1 = ctk.CTkLabel(master=self.frame_right, text='Service', font=("Roboto Medium", -16))
			self.label_service_1.grid(row=1, column=0, pady=10, padx=10)
		#self.update()

	def update_coordinate(self):
		print("Update Coordinate")

	def print_coordinate(self):
		print("Print Coordinate")

	def callback_dx(self, event):
		self.dx = self.entry_dx.get()

	def callback_dy(self, event):
		self.dy = self.entry_dy.get()

	def callback_dz(self, event):
		self.dz = self.entry_dz.get()

	def start_thermocyclers(self) -> None:
		# Create a file for logging.
		file = self.browse_files()
		file.write(f"""------------------------------------------------------
Thermocycler Protocol
------------------------------------------------------
Date: {datetime.date.today()}
User: {getpass.getuser()}

Thermocycler A:
---------------
Cycles: {int(self.thermocyclers['cycles']['A'])}
Temperatures:
	Denature: {int(self.thermocyclers['temperatures']['A'][0])} C
	Anneal: {int(self.thermocyclers['temperatures']['A'][2])} C
	Extension: {int(self.thermocyclers['temperatures']['A'][4])} C
Times:
	Denature: {int(self.thermocyclers['times']['A']['denature'])} min
	Anneal: {int(self.thermocyclers['times']['A']['anneal'])} sec
	Extension: {int(self.thermocyclers['times']['A']['extension'])} sec

Thermocycler B:
---------------
Cycles: {int(self.thermocyclers['cycles']['B'])}
Temperatures:
	Denature: {int(self.thermocyclers['temperatures']['B'][0])} C
	Anneal: {int(self.thermocyclers['temperatures']['B'][2])} C
	Extension: {int(self.thermocyclers['temperatures']['B'][4])} C
Times:
	Denature: {int(self.thermocyclers['times']['B']['denature'])} min
	Anneal: {int(self.thermocyclers['times']['B']['anneal'])} sec
	Extension: {int(self.thermocyclers['times']['B']['extension'])} sec

Thermocycler C:
---------------
Cycles: {int(self.thermocyclers['cycles']['C'])}
Temperatures:
	Denature: {int(self.thermocyclers['temperatures']['C'][0])} C
	Anneal: {int(self.thermocyclers['temperatures']['C'][2])} C
	Extension: {int(self.thermocyclers['temperatures']['C'][4])} C
Times:
	Denature: {int(self.thermocyclers['times']['C']['denature'])} min
	Anneal: {int(self.thermocyclers['times']['C']['anneal'])} sec
	Extension: {int(self.thermocyclers['times']['C']['extension'])} sec

Thermocycler D:
---------------
Cycles: {int(self.thermocyclers['cycles']['D'])}
Temperatures:
	Denature: {int(self.thermocyclers['temperatures']['D'][0])} C
	Anneal: {int(self.thermocyclers['temperatures']['D'][2])} C
	Extension: {int(self.thermocyclers['temperatures']['D'][4])} C
Times:
	Denature: {int(self.thermocyclers['times']['D']['denature'])} min
	Anneal: {int(self.thermocyclers['times']['D']['anneal'])} sec
	Extension: {int(self.thermocyclers['times']['D']['extension'])} sec

------------------------------------------------------""")
		# Start timers for the thermocyclers
		# Start a thread
		thread = threading.Thread(target=self.thermocycle)
		thread.start()

	def thermocycle(self):
		# Get the number of cycles for each thermocycler
		cycles_A = int(self.thermocyclers['cycles']['A'])
		cycles_B = int(self.thermocyclers['cycles']['B'])
		cycles_C = int(self.thermocyclers['cycles']['C'])
		cycles_D = int(self.thermocyclers['cycles']['D'])
		# Get the times for each thermocycler
		denature_time_A = int(self.thermocyclers['times']['A']['denature'])
		denature_time_B = int(self.thermocyclers['times']['B']['denature'])
		denature_time_C = int(self.thermocyclers['times']['C']['denature'])
		denature_time_D = int(self.thermocyclers['times']['D']['denature'])
		anneal_time_A = int(self.thermocyclers['times']['A']['anneal'])
		anneal_time_B = int(self.thermocyclers['times']['B']['anneal'])
		anneal_time_C = int(self.thermocyclers['times']['C']['anneal'])
		anneal_time_D = int(self.thermocyclers['times']['D']['anneal'])
		extension_time_A = int(self.thermocyclers['times']['A']['extension'])
		extension_time_B = int(self.thermocyclers['times']['B']['extension'])
		extension_time_C = int(self.thermocyclers['times']['C']['extension'])
		extension_time_D = int(self.thermocyclers['times']['D']['extension'])
		# Get the temperatures for each thermocycler
		denature_temperature_A = int(self.thermocyclers['temperatures']['A'][0])
		denature_temperature_B = int(self.thermocyclers['temperatures']['B'][0])
		denature_temperature_C = int(self.thermocyclers['temperatures']['C'][0])
		denature_temperature_D = int(self.thermocyclers['temperatures']['D'][0])
		anneal_temperature_A = int(self.thermocyclers['temperatures']['A'][2])
		anneal_temperature_B = int(self.thermocyclers['temperatures']['B'][2])
		anneal_temperature_C = int(self.thermocyclers['temperatures']['C'][2])
		anneal_temperature_D = int(self.thermocyclers['temperatures']['D'][2])
		extension_temperature_A = int(self.thermocyclers['temperatures']['A'][4])
		extension_temperature_B = int(self.thermocyclers['temperatures']['B'][4])
		extension_temperature_C = int(self.thermocyclers['temperatures']['C'][4])
		extension_temperature_D = int(self.thermocyclers['temperatures']['D'][4])
		# Denature
		time_start = time.time()
		meersetter = Meerstetter()
		meersetter.change_temperature(1, denature_temperature_A, False)
		meersetter.change_temperature(2, denature_temperature_B, False)
		#meersetter.change_temperature(3, denature_temperature_C, False)
		meersetter.change_temperature(4, denature_temperature_D, False)
		for sec in range(int(denature_time_A * 60)):
			time.sleep(1)
		print('done')
		# Thermocycle
		cycles = [i for i in range(self.thermocyclers['cycles']['A'])]
		for cycle in cycles:
			print(f"Cycle Number: {cycle}/{len(cycles)}")
			meersetter.change_temperature(1, extension_temperature_A, False)
			meersetter.change_temperature(2, extension_temperature_B, False)
			#meersetter.change_temperature(3, extension_temperature_C, False)
			meersetter.change_temperature(4, extension_temperature_D, False)
			for sec in range(int(denature_time_A * 60)):
				time.sleep(1)
			meersetter.change_temperature(1, anneal_temperature_A, False)
			meersetter.change_temperature(2, anneal_temperature_B, False)
			#meersetter.change_temperature(3, anneal_temperature_C, False)
			meersetter.change_temperature(4, anneal_temperature_D, False)
			for sec in range(int(denature_time_A * 60)):
				time.sleep(1)
		# End temperatue
		meersetter.change_temperature(1, 30, False)
		meersetter.change_temperature(2, 30, False)
		#meersetter.change_temperature(3, 30, False)
		meersetter.change_temperature(4, 30, False)


	def browse_files(self):
		file = tkinter.filedialog.asksaveasfile(initialfile='thermocycler_protocol.txt', initialdir = './', title="Save Protocol to File")
		return file

	def import_thermocyclers(self) -> None:
		a = 1

	def test1(self):
		payload = PeltierPayload('get', 1000)
		address = 1
		pcom = PeltierCommunication('#', 1, 1, payload,None)
		self.__controller.write(pcom.to_string())
		#self.__increase_sequence_number(address)
        # Get the response back.
		response = self.__controller.readline()
        # Compare the response.
        #pcom.compare_with_response(response, assert_checksum=False)
        # Get the object temperature from the response.
		temperature_hexidecimal = response[7:-4]
		temperature = convert_hexidecimal_to_float32_ieee_754(temperature_hexidecimal)
		print(temperature)

	def test2(self):
		payload = PeltierPayload('get', 1000)
		address = 2
		pcom = PeltierCommunication('#', 2, 1, payload,None)
		self.__controller.write(pcom.to_string())
		#self.__increase_sequence_number(address)
        # Get the response back.
		response = self.__controller.readline()
        # Compare the response.
        #pcom.compare_with_response(response, assert_checksum=False)
        # Get the object temperature from the response.
		temperature_hexidecimal = response[7:-4]
		temperature = convert_hexidecimal_to_float32_ieee_754(temperature_hexidecimal)
		print(temperature)

	def export_thermocyclers(self):
		t1 = threading.Thread(target=self.test1)
		t2 = threading.Thread(target=self.test2)
		t1.run()
		t2.run()

	def plot_thermocycler(self, data) -> None:
		fig = Figure(figsize=(3,2.4))
		a = fig.add_subplot(111)
		#data = np.array([92,92,55,55,84,84])
		x = np.array([1,2,3,4,5,6])
		a.set_yticks([data[0],data[2],data[4]])
		a.set_xticks([])
		a.axvline(x=2.5)
		a.axvline(x=4.5)
		a.plot(x, data, color='red')
		canvas = FigureCanvasTkAgg(fig, master=self.frame_right)
		canvas.flush_events()
		canvas.get_tk_widget().place(x=10, y=120)
		canvas.draw()
		#self.plot_thermocycler(self.thermocycler['temperatures']['A'])
		#self.label_thermocycler_denature = ctk.CTkLabel(master=self.frame_right, bg_color="white", text_color='black', text='Denature', font=("Roboto Light",-16))
		#self.label_thermocycler_denature.place(x=10, y=120, width=100)
		#self.label_thermocycler_anneal = ctk.CTkLabel(master=self.frame_right, bg_color="white", text_color='black', text='Anneal', font=("Roboto Light", -16))
		#self.label_thermocycler_anneal.place(x=110, y=120, width=100)
		#self.label_thermocycler_extension = ctk.CTkLabel(master=self.frame_right, bg_color="white", text_color='black', text='Extension', font=("Roboto Light", -16))
		#self.label_thermocycler_extension.place(x=210, y=120, width=100)

	def on_click(self, event):
		x,y = event.x, event.y
		#print(f"{x}, {y}")
		if type(event.widget) == tkinter.Label:
			# Get label text.
			label_text = event.widget.cget('text')
			if label_text == 'thermocycler':
				# Check what the user is hovering over and toggle the component on click.
				if x >= 130 and x <= 238:
					if y >= 30 and y <= 124:
						clicked_on = 'A'
						self.thermocyclers['clamps']['A']['homed'] = not self.thermocyclers['clamps']['A']['homed']
					elif y >= 128 and y <= 222:
						clicked_on = 'B'
						self.thermocyclers['clamps']['B']['homed'] = not self.thermocyclers['clamps']['B']['homed']
					elif y >= 248 and y <= 345:
						clicked_on = 'C'
						self.thermocyclers['clamps']['C']['homed'] = not self.thermocyclers['clamps']['C']['homed']
					elif y >= 348 and y <= 446:
						clicked_on = 'D'
						self.thermocyclers['clamps']['D']['homed'] = not self.thermocyclers['clamps']['D']['homed']
				elif x >= 7	and x <= 118:
					if y >= 8 and y <= 234:
						clicked_on = 'AB'
						if self.thermocyclers['clamps']['A']['homed'] and self.thermocyclers['clamps']['B']['homed']:
							self.thermocyclers['trays']['AB']['homed'] = not self.thermocyclers['trays']['AB']['homed']
					elif y >= 238 and y <= 464:
						clicked_on = 'CD'
						if self.thermocyclers['clamps']['C']['homed'] and self.thermocyclers['clamps']['D']['homed']:
							self.thermocyclers['trays']['CD']['homed'] = not self.thermocyclers['trays']['CD']['homed']
				# Change the thermocycler picture.
				self.thermocycler_dict = {
						'A': self.thermocyclers['clamps']['A']['homed'],
						'B': self.thermocyclers['clamps']['B']['homed'],
						'C': self.thermocyclers['clamps']['C']['homed'],
						'D': self.thermocyclers['clamps']['D']['homed'],
						'AB': self.thermocyclers['trays']['AB']['homed'],
						'CD': self.thermocyclers['trays']['CD']['homed'],
					}						
				self.make_thermocycler_png_name()
				image = Image.open(self.thermocycler_png_name).resize((250, 470))
				self.img_thermocycler = ImageTk.PhotoImage(image)
				self.label_thermocycler = ctk.CTkLabel(master=self.frame_right, text='thermocycler', font=("Roboto Light", -1), image=self.img_thermocycler)
				self.label_thermocycler.place(x=310, y=5) 
				self.label_thermocycler.bind('<Button-1>', self.on_click)
			if label_text == 'deck_plate':
				print(f"Clicked: {x}, {y}")
				consumable_options = StringVar()
				tray_options = StringVar()
				column_options = StringVar()
				# Quant Strips
				if x >= 531 and x <= 553:
					consumable_options.set('Quant Strip')
					column_options.set('1')
					if y >= 62 and y <= 148:
						tray_options.set('A')
					elif y >= 154 and y <= 241: 
						tray_options.set('B')
					elif y >= 247 and y <= 334:
						tray_options.set('C')
					elif y >= 338 and y <= 425:
						tray_options.set('D')
				# Tip Trays
				if x >= 433 and x <= 440:
					consumable_options.set('Tip Tray')
					column_options.set('1')
					if y >= 64 and y <= 150:
						tray_options.set('A')
					elif y >= 156 and y <= 241:
						tray_options.set('B')
					elif y >= 249 and y <= 334:
						tray_options.set('C')
					elif y >= 340 and y <= 426:
						tray_options.set('D')
				elif x >= 441 and x <= 448:
					consumable_options.set('Tip Tray')
					column_options.set('2')
					if y >= 64 and y <= 150:
						tray_options.set('A')
					elif y >= 156 and y <= 241:
						tray_options.set('B')
					elif y >= 249 and y <= 334:
						tray_options.set('C')
					elif y >= 340 and y <= 426:
						tray_options.set('D')
				elif x >= 442 and x <= 455:
					consumable_options.set('Tip Tray')
					column_options.set('3')
					if y >= 64 and y <= 150:
						tray_options.set('A')
					elif y >= 156 and y <= 241:
						tray_options.set('B')
					elif y >= 249 and y <= 334:
						tray_options.set('C')
					elif y >= 340 and y <= 426:
						tray_options.set('D')
				elif x >= 456 and x <= 464:
					consumable_options.set('Tip Tray')
					column_options.set('4')
					if y >= 64 and y <= 150:
						tray_options.set('A')
					elif y >= 156 and y <= 241:
						tray_options.set('B')
					elif y >= 249 and y <= 334:
						tray_options.set('C')
					elif y >= 340 and y <= 426:
						tray_options.set('D')
				elif x >= 465 and x <= 472:
					consumable_options.set('Tip Tray')
					column_options.set('5')
					if y >= 64 and y <= 150:
						tray_options.set('A')
					elif y >= 156 and y <= 241:
						tray_options.set('B')
					elif y >= 249 and y <= 334:
						tray_options.set('C')
					elif y >= 340 and y <= 426:
						tray_options.set('D')
				elif x >= 473 and x <= 479:
					consumable_options.set('Tip Tray')
					column_options.set('6')
					if y >= 64 and y <= 150:
						tray_options.set('A')
					elif y >= 156 and y <= 241:
						tray_options.set('B')
					elif y >= 249 and y <= 334:
						tray_options.set('C')
					elif y >= 340 and y <= 426:
						tray_options.set('D')
				elif x >= 480 and x <= 486:
					consumable_options.set('Tip Tray')
					column_options.set('7')
					if y >= 64 and y <= 150:
						tray_options.set('A')
					elif y >= 156 and y <= 241:
						tray_options.set('B')
					elif y >= 249 and y <= 334:
						tray_options.set('C')
					elif y >= 340 and y <= 426:
						tray_options.set('D')
				elif x >= 487 and x <= 495:
					consumable_options.set('Tip Tray')
					column_options.set('8')
					if y >= 64 and y <= 150:
						tray_options.set('A')
					elif y >= 156 and y <= 241:
						tray_options.set('B')
					elif y >= 249 and y <= 334:
						tray_options.set('C')
					elif y >= 340 and y <= 426:
						tray_options.set('D')
				elif x >= 496 and x <= 503:
					consumable_options.set('Tip Tray')
					column_options.set('9')
					if y >= 64 and y <= 150:
						tray_options.set('A')
					elif y >= 156 and y <= 241:
						tray_options.set('B')
					elif y >= 249 and y <= 334:
						tray_options.set('C')
					elif y >= 340 and y <= 426:
						tray_options.set('D')
				elif x >= 504 and x <= 510:
					consumable_options.set('Tip Tray')
					column_options.set('10')
					if y >= 64 and y <= 150:
						tray_options.set('A')
					elif y >= 156 and y <= 241:
						tray_options.set('B')
					elif y >= 249 and y <= 334:
						tray_options.set('C')
					elif y >= 340 and y <= 426:
						tray_options.set('D')
				elif x >= 511 and x <= 516:
					consumable_options.set('Tip Tray')
					column_options.set('11')
					if y >= 64 and y <= 150:
						tray_options.set('A')
					elif y >= 156 and y <= 241:
						tray_options.set('B')
					elif y >= 249 and y <= 334:
						tray_options.set('C')
					elif y >= 340 and y <= 426:
						tray_options.set('D')
				elif x >= 517 and x <= 527:
					consumable_options.set('Tip Tray')
					column_options.set('12')
					if y >= 64 and y <= 150:
						tray_options.set('A')
					elif y >= 156 and y <= 241:
						tray_options.set('B')
					elif y >= 249 and y <= 334:
						tray_options.set('C')
					elif y >= 340 and y <= 426:
						tray_options.set('D')
				# Reagent Cartridge
				# Sample Rack
				if x >= 266 and x <= 298:
					consumable_options.set('Sample Rack')
					column_options.set('1')
					if y >= 62 and y <= 150:
						tray_options.set('A')
					elif y >= 154 and y <= 243: 
						tray_options.set('B')
					elif y >= 247 and y <= 334:
						tray_options.set('C')
					elif y >= 338 and y <= 427:
						tray_options.set('D')
				# Aux Heater
				if x >= 232 and x <= 258:
					consumable_options.set('Aux Heater')
					column_options.set('1')
					if y >= 62 and y <= 150:
						tray_options.set('A')
					elif y >= 154 and y <= 243: 
						tray_options.set('B')
					elif y >= 247 and y <= 334:
						tray_options.set('C')
					elif y >= 338 and y <= 427:
						tray_options.set('D')
				# Heater/Shaker
				if x >= 113 and x <= 225 and y >= 157 and y <= 242:
					consumable_options.set('Heater/Shaker')
					tray_options.set('')
					if x >= 113 and x <= 138:
						column_options.set('1')
					elif x >= 144 and x <= 167:
						column_options.set('2')
					elif x >= 173 and x <= 195:
						column_options.set('3')
					elif x >= 199 and x <= 221:
						column_options.set('4')
				# Mag Separator
				if x >= 111 and x <= 224 and y >= 249 and y <= 333:
					consumable_options.set("Mag Separator")
					tray_options.set('')
					if x >= 111 and x <= 121:
						column_options.set('1')
					elif x >= 122 and x <= 130:
						column_options.set('2')
					elif x >= 131 and x <= 140:
						column_options.set('3')
					elif x >= 141 and x <= 148:
						column_options.set('4')
					elif x >= 149 and x <= 158:
						column_options.set('5')
					elif x >= 159 and x <= 167:
						column_options.set('6')
					elif x >= 168 and x <= 176:
						column_options.set('7')
					elif x >= 177 and x <= 186:
						column_options.set('8')
				# Chiller
				# Pre-Amp Thermocycler
				# Lid Tray
				# Tip Transfer Tray
				# Assay Strip
				# Update the option menus
				self.optionmenu_consumable.configure(variable=consumable_options)
				self.optionmenu_tray.configure(variable=tray_options)
				self.optionmenu_column.configure(variable=column_options)

	def on_release(self, event):
		x, y = event.x, event.y
		if type(event.widget) == tkinter.Label:
			# Get label text.
			label_text = event.widget.cget('text')
			if label_text == 'deck_plate':
				print(f"Released: {x}, {y}")

	def make_thermocycler_png_name(self) -> None:
		d = self.thermocycler_dict
		s = 'thermocycler'
		if not d['AB']:
			s = s + '_ab'
		if not d['CD']:
			s = s + '_cd'
		if not d['A']:
			s = s + '_a'
		if not d['B']:
			s = s + '_b'
		if not d['C']:
			s = s + '_c'
		if not d['D']:
			s = s + '_d'
		s = s + '.png'
		self.thermocycler_png_name = s

	def motion(self, event) -> None:
		x,y = event.x, event.y
		#print(f"{x}, {y}")

	def callback_update_thermocycler_protocol(self, event):
		# Fill in all the protocol data for the heater.
		thermocycler = self.optionmenu_thermocycler.get()
		thermocycler_cycles_sv = StringVar()
		thermocycler_cycles_sv.set(str(self.thermocyclers['cycles'][thermocycler]))
		self.entry_thermocycler_cycles.configure(textvariable=thermocycler_cycles_sv)
		thermostat_denature_sv = StringVar()
		thermostat_denature_sv.set(str(self.thermocyclers['temperatures'][thermocycler][0]))
		self.entry_thermostat_denature.configure(textvariable=thermostat_denature_sv)
		thermostat_anneal_sv = StringVar()
		thermostat_anneal_sv.set(str(self.thermocyclers['temperatures'][thermocycler][2]))
		self.entry_thermostat_anneal.configure(textvariable=thermostat_anneal_sv)
		thermostat_extension_sv = StringVar()
		thermostat_extension_sv.set(str(self.thermocyclers['temperatures'][thermocycler][4]))
		self.entry_thermostat_extension.configure(textvariable=thermostat_extension_sv)
		clock_denature_sv = StringVar()
		clock_denature_sv.set(str(self.thermocyclers['times'][thermocycler]['denature']))
		self.entry_clock_denature.configure(textvariable=clock_denature_sv)
		clock_anneal_sv = StringVar()
		clock_anneal_sv.set(str(self.thermocyclers['times'][thermocycler]['anneal']))
		self.entry_clock_anneal.configure(textvariable=clock_anneal_sv)
		clock_extension_sv = StringVar()
		clock_extension_sv.set(str(self.thermocyclers['times'][thermocycler]['extension']))
		self.entry_clock_extension.configure(textvariable=clock_extension_sv)
		self.plot_thermocycler(self.thermocyclers['temperatures'][thermocycler])

	def callback_thermocycler_temperatures(self, event):
		thermocycler = self.optionmenu_thermocycler.cget('variable').get()
		# Update the data in the Thermocycler plot.
		temp_denature = int(self.entry_thermostat_denature.get())
		temp_anneal = int(self.entry_thermostat_anneal.get())
		temp_extension = int(self.entry_thermostat_extension.get())
		self.thermocyclers['temperatures'][thermocycler] = np.array([temp_denature,temp_denature, temp_anneal,temp_anneal, temp_extension, temp_extension])
		self.plot_thermocycler(self.thermocyclers['temperatures'][thermocycler])

	def callback_thermocycler_times(self, event):
		thermocycler = self.optionmenu_thermocycler.cget('variable').get()
		time_denature = int(self.entry_clock_denature.get())
		time_anneal = int(self.entry_clock_anneal.get())
		time_extension = int(self.entry_clock_extension.get())
		self.thermocyclers['times'][thermocycler]['denature'] = time_denature
		self.thermocyclers['times'][thermocycler]['anneal'] = time_anneal
		self.thermocyclers['times'][thermocycler]['extension'] = time_extension

	def callback_thermocycler_cycles(self, event):
		thermocycler = self.optionmenu_thermocycler.cget('variable').get()
		cycles = int(self.entry_thermocycler_cycles.get())
		self.thermocyclers['cycles'][thermocycler] = cycles

	def enter(self, event):
		# Get the entry name.
		a = 1

	def mouse_wheel(self, event):
		if type(event.widget) == tkinter.Label:
			label_text = event.widget.cget('text')
			if event.delta == 1:
				print(f"{label_text}: down")
			elif event.delta == -1:
				print(f"{label_text}: up")

	def on_closing(self, event=0) -> None:
		self.destroy()

if __name__ == '__main__':
	app = App()
	app.iconbitmap('bio-rad-logo.ico')
	app.bind('<Return>', app.enter)
	app.maxsize(780,520)
	app.minsize(780,520)
	app.mainloop()