#!/usr/bin/env python3.8

from tkinter import StringVar
import tkinter
import customtkinter as ctk
from PIL import Image, ImageTk
import matplotlib
import numpy as np
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('green')

class App(ctk.CTk):
	WIDTH = 780
	HEIGHT = 520

	# Thermocycler Settings:
	thermocyclers = {
		'clamp': {
			'A': True, # True (Raised, homed), False (Lowered)
			'B': True,
			'C': True,
			'D': True,
			},
		'tray': {
			'AB': True, # True (Open, homed), False (Closed),
			'CD': True, # True (Open, homed), False (Closed),
			},
		'temperatures': {
			'A': np.array([92,92, 55, 55, 84, 84]),
			'B': np.array([92,92, 60, 60, 95, 95]),
			'C': np.array([92,92, 55, 55, 84, 84]),
			'D': np.array([92,92, 55, 55, 84, 84]),
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
		}

	def __init__(self):
		super().__init__()
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
		self.frame_right.grid(row=0, column=1, sticky='nswe', padx=20, pady=20, columnspan=3)

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
			self.optionmenu_thermocycler = ctk.CTkOptionMenu(master=self.frame_right, variable=thermocycler_options, values=('A', 'B', 'C', 'D'))
			self.optionmenu_thermocycler.place(x=150, y=40)
			self.label_thermocycler_cycles = ctk.CTkLabel(master=self.frame_right, text='Cycles', font=("Roboto Light", -16))
			self.label_thermocycler_cycles.place(x=0, y=80)
			self.entry_thermocycler_cycles = ctk.CTkEntry(master=self.frame_right)
			self.entry_thermocycler_cycles.place(x=150, y=80)
			image = Image.open('thermocycler.png').resize((250, 470))
			self.img_thermocycler = ImageTk.PhotoImage(image)
			self.label_thermocycler = ctk.CTkLabel(master=self.frame_right, text='thermocycler', font=("Roboto Light", -1), image=self.img_thermocycler)
			self.label_thermocycler.place(x=310, y=5) 
			self.label_thermocycler.bind('<Button-1>', self.on_click)
			self.button_start_thermocyclers = ctk.CTkButton(master=self.frame_right, text='Start', command=self.start_thermocyclers())
			self.button_start_thermocyclers.place(x=5, y=445, width=100)
			self.button_import = ctk.CTkButton(master=self.frame_right, text='Import', command=self.import_thermocyclers())
			self.button_import.place(x=115, y=445, width=95)
			self.button_export = ctk.CTkButton(master=self.frame_right, text='Export', command=self.export_thermocyclers())
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
			self.entry_clock_denature.place(x=65, y=395)
			clock_anneal_sv = StringVar()
			clock_anneal_sv.set(str(self.thermocyclers['times'][thermocycler]['anneal']))
			self.entry_clock_anneal = ctk.CTkEntry(master=self.frame_right, width=40, textvariable=clock_anneal_sv)
			self.entry_clock_anneal.place(x=145, y=395)
			clock_extension_sv = StringVar()
			clock_extension_sv.set(str(self.thermocyclers['times'][thermocycler]['extension']))
			self.entry_clock_extension = ctk.CTkEntry(master=self.frame_right, width=40, textvariable=clock_extension_sv)
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
			self.label_deck_plate = ctk.CTkLabel(master=self.frame_right, text='', image=self.img_deck_plate)
			self.label_deck_plate.place(x=0, y=40) 
			self.label_consumable = ctk.CTkLabel(master=self.frame_right, text='Consumable', font=("Roboto Medium", -16))
			self.label_consumable.place(x=5, y=5, width=90)
			consumable_options = StringVar()
			consumable_options.set('')
			self.optionmenu_consumable = ctk.CTkOptionMenu(master=self.frame_right, variable=consumable_options, values=("Tip Tray", "Reagent Cartridge", "Sample Rack", "Aux Heater", "Heater/Shaker", "Mag Separator", "Chiller", "Pre-Amp Thermocycler", "Lid Tray", "Tip Transfer Tray", "DNA Quant", "Assay Strip"))
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
			self.label_x = ctk.CTkLabel(master=self.frame_right, text='X', font=("Roboto Medium", -16))
			self.label_x.place(x=195, y=45, width=30)
		elif button_text == 'Service':
			self.label_service_1 = ctk.CTkLabel(master=self.frame_right, text='Service', font=("Roboto Medium", -16))
			self.label_service_1.grid(row=1, column=0, pady=10, padx=10)
		#self.update()

	def start_thermocyclers(self) -> None:
		print("HERE")

	def import_thermocyclers(self) -> None:
		print("HERE")

	def export_thermocyclers(self) -> None:
		print("HERE")

	def plot_thermocycler(self, data) -> None:
		fig = Figure(figsize=(3,2.4))
		a = fig.add_subplot(111)
		#data = np.array([92,92,55,55,84,84])
		x = np.array([1,2,3,4,5,6])
		print(f"{data[0]}")
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
				thermocycler_dict = {
						'A': self.thermocyclers['clamps']['A']['homed'],
						'B': self.thermocyclers['clamps']['B']['homed'],
						'C': self.thermocyclers['clamps']['C']['homed'],
						'D': self.thermocyclers['clamps']['D']['homed'],
						'AB': self.thermocyclers['trays']['AB']['homed'],
						'CD': self.thermocyclers['trays']['CD']['homed'],
					}						
				png_name = self.make_thermocycler_png_name(thermocycler_dict)
				print(png_name)
				image = Image.open(png_name).resize((250, 470))
				self.img_thermocycler = ImageTk.PhotoImage(image)
				self.label_thermocycler = ctk.CTkLabel(master=self.frame_right, text='thermocycler', font=("Roboto Light", -1), image=self.img_thermocycler)
				self.label_thermocycler.place(x=310, y=5) 
				self.label_thermocycler.bind('<Button-1>', self.on_click)

	def make_thermocycler_png_name(self, thermocycler_dict) -> str:
		d = thermocycler_dict
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
		return s

	def motion(self, event) -> None:
		x,y = event.x, event.y
		#print(f"{x}, {y}")

	def callback_denature_temperature(self, sv):
		print(sv.get())
		#thermocycler = self.optionmenu_thermocycler.cget('variable').get()
		# Update the data.
		#self.thermocyclers['temperatures'][thermocycler] = np.array([90,90,40,40,80,80])
		#self.plot_thermocycler(self.thermocyclers['temperatures'][thermocycler])

	def callback_thermocycler_temperatures(self, event):
		thermocycler = self.optionmenu_thermocycler.cget('variable').get()
		# Update the data in the Thermocycler plot.
		temp_denature = int(self.entry_thermostat_denature.get())
		temp_anneal = int(self.entry_thermostat_anneal.get())
		temp_extension = int(self.entry_thermostat_extension.get())
		self.thermocyclers['temperatures'][thermocycler] = np.array([temp_denature,temp_denature, temp_anneal,temp_anneal, temp_extension, temp_extension])
		print(self.thermocyclers['temperatures'][thermocycler])
		self.plot_thermocycler(self.thermocyclers['temperatures'][thermocycler])

	def callback_anneal_temperature(self, sv):
		print(sv.get())

	def callback_extension_temperature(self, sv):
		print(sv.get())

	def enter(self, event):
		# Get the entry name.
		a = 1

	def on_closing(self, event=0) -> None:
		self.destroy()

if __name__ == '__main__':
	app = App()
	app.iconbitmap('bio-rad-logo.ico')
	app.bind('<Return>', app.enter)
	app.maxsize(780,520)
	app.minsize(780,520)
	app.mainloop()
