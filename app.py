#!/usr/bin/env python3.8

from tkinter import StringVar
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

	def __init__(self):
		super().__init__()
		
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
			thermocycler_options.set('All')
			self.optionmenu_thermocycler = ctk.CTkOptionMenu(master=self.frame_right, variable=thermocycler_options, values=('A', 'B', 'C', 'D', 'All'))
			self.optionmenu_thermocycler.place(x=150, y=40)
			self.label_thermocycler_cycles = ctk.CTkLabel(master=self.frame_right, text='Cycles', font=("Roboto Light", -16))
			self.label_thermocycler_cycles.place(x=0, y=80)
			self.entry_thermocycler_cycles = ctk.CTkEntry(master=self.frame_right)
			self.entry_thermocycler_cycles.place(x=150, y=80)
			image = Image.open('thermocycler_homed.png').resize((250, 470))
			self.img_thermocycler_a = ImageTk.PhotoImage(image)
			self.label_thermocycler_a = ctk.CTkLabel(master=self.frame_right, text='', image=self.img_thermocycler_a)
			self.label_thermocycler_a.place(x=310, y=5) 
			self.button_start_thermocyclers = ctk.CTkButton(master=self.frame_right, text='Start', command=self.start_thermocyclers())
			self.button_start_thermocyclers.place(x=5, y=445, width=100)
			self.button_import = ctk.CTkButton(master=self.frame_right, text='Import', command=self.import_thermocyclers())
			self.button_import.place(x=115, y=445, width=95)
			self.button_export = ctk.CTkButton(master=self.frame_right, text='Export', command=self.export_thermocyclers())
			self.button_export.place(x=215, y=445, width=95)
			#image = Image.open('thermocycle_plot.png').resize((295, 310))
			#self.img_thermocycler_plot = ImageTk.PhotoImage(image)
			#self.label_thermocycler_plot = ctk.CTkLabel(master=self.frame_right, image=self.img_thermocycler_plot)
			#self.label_thermocycler_plot.place(x=10, y=120) 
			fig = Figure(figsize=(3,3))
			a = fig.add_subplot(111)
			data = np.array([92,92,55,55,84,84])
			x = np.array([1,2,3,4,5,6])
			a.set_yticks([92,55,84])
			a.set_xticks([])
			a.axvline(x=2.5)
			a.axvline(x=4.5)
			a.plot(x, data, color='red')
			canvas = FigureCanvasTkAgg(fig, master=self.frame_right)
			canvas.get_tk_widget().place(x=10, y=120)
			canvas.draw()
			self.label_thermocycler_denature = ctk.CTkLabel(master=self.frame_right, bg_color="white", text_color='black', text='Denature', font=("Roboto Light",-16))
			self.label_thermocycler_denature.place(x=10, y=120, width=100)
			self.label_thermocycler_anneal = ctk.CTkLabel(master=self.frame_right, bg_color="white", text_color='black', text='Anneal', font=("Roboto Light", -16))
			self.label_thermocycler_anneal.place(x=110, y=120, width=100)
			self.label_thermocycler_extension = ctk.CTkLabel(master=self.frame_right, bg_color="white", text_color='black', text='Extension', font=("Roboto Light", -16))
			self.label_thermocycler_extension.place(x=210, y=120, width=100)
		elif button_text == "Build Protocol":
			self.label_build_protocol_1 = ctk.CTkLabel(self.frame_right, text="Build Protocl", font=("Roboto Medium", -16))
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

	def on_closing(self, event=0) -> None:
		self.destroy()

if __name__ == '__main__':
	app = App()
	app.maxsize(780,520)
	app.minsize(780,520)
	app.mainloop()
