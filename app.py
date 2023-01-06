#!/usr/bin/env python3.8

import pythonnet
from pythonnet import load

load("coreclr")

from utils import delay
from script import Script
from upper_gantry import UpperGantry
from meerstetter import Meerstetter
from fast_api_interface import FastAPIInterface
from uvicorn_server import UvicornServer

# Needed to do for pandas:
# python3.8 -m pip install openpyxl

import uvicorn
import pandas as pd
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

# Import Office365 for using SharePoint
#from office365.runtime.auth.authentication_context import AuthenticationContext
#from office365.sharepoint.client_context import ClientContext
#from office365.sharepoint.files.file import File

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
			'A': np.array([84,84, 50, 50, 84, 84]),
			'B': np.array([84,84, 50, 50, 84, 84]),
			'C': np.array([84,84, 50, 50, 84, 84]),
			'D': np.array([84,84, 50, 50, 84, 84]),
			},
		'times': {
			'A': {'denature': 3, 'anneal': 40, 'extension': 30},
			'B': {'denature': 3, 'anneal': 40, 'extension': 30},
			'C': {'denature': 3, 'anneal': 40, 'extension': 30},
			'D': {'denature': 3, 'anneal': 40, 'extension': 30},
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
			'A': 40,
			'B': 40,
			'C': 40,
			'D': 40,
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
		self.server = UvicornServer()
		self.server.start()
		self.script = Script()
		self.upper_gantry = UpperGantry()
		self.fast_api_interface = FastAPIInterface()

		# Copy/Paste
		self.clipboard = []

		self.use_z = tkinter.IntVar()
		self.use_z.set(1)
		self.slow_z = tkinter.IntVar()
		self.slow_z.set(1)
		self.pipette_tip_type = StringVar()
		self.pipette_tip_type.set(None)
		self.dx = StringVar()
		self.dx.set('500')
		self.dy = StringVar()
		self.dy.set('5000')
		self.dz = StringVar()
		self.dz.set('5000')
		self.image_dx_sv = StringVar()
		self.image_dx_sv.set('500')
		self.image_dy_sv = StringVar()
		self.image_dy_sv.set('500')
		self.image_dz_sv = StringVar()
		self.image_dz_sv.set('500')
		self.build_protocol_tips_tray_sv = StringVar('')
		self.bind('<Motion>', self.motion)
		self.clamp_A_max = StringVar()
		self.clamp_A_max.set('400000')
		self.clamp_B_max = StringVar()
		self.clamp_B_max.set('400000')
		self.clamp_C_max = StringVar()
		self.clamp_C_max.set('400000')
		self.clamp_D_max = StringVar()
		self.clamp_D_max.set('400000')
		self.heater_shaker_rpm = StringVar()
		self.heater_shaker_rpm.set('1300')
		self.settings_unit_sv = StringVar()
		self.settings_unit_sv.set('A')
		self.settings_unit_sv.trace('w', self.callback_settings_unit_sv_changed)
		self.use_thermocycler_A = tkinter.IntVar()
		self.use_thermocycler_A.set(1)
		self.use_thermocycler_B = tkinter.IntVar()
		self.use_thermocycler_B.set(1)
		self.use_thermocycler_C = tkinter.IntVar()
		self.use_thermocycler_C.set(0)
		self.use_thermocycler_D = tkinter.IntVar()
		self.use_thermocycler_D.set(1)
		self.service_topic_sv = StringVar()
		self.service_topic_sv.set('')
		self.image_filter_sv = StringVar()
		self.image_filter_sv.set('')
		self.image_led_sv = StringVar()
		self.image_led_sv.set('Off')
		self.brightfield_on = False
		self.thermocycler_cycles_sv = StringVar()
		self.thermocycler_cycles_sv.set(str(self.thermocyclers['cycles']['A']))
		self.settings_tip_tray_1_sv = StringVar()
		self.settings_tip_tray_1_sv.set('1000')
		self.settings_tip_tray_2_sv = StringVar()
		self.settings_tip_tray_2_sv.set('1000')
		self.settings_tip_tray_3_sv = StringVar()
		self.settings_tip_tray_3_sv.set('1000')
		self.settings_tip_tray_4_sv = StringVar()
		self.settings_tip_tray_4_sv.set('1000')
		self.settings_tip_tray_5_sv = StringVar()
		self.settings_tip_tray_5_sv.set('50')
		self.settings_tip_tray_6_sv = StringVar()
		self.settings_tip_tray_6_sv.set('50')
		self.settings_tip_tray_7_sv = StringVar()
		self.settings_tip_tray_7_sv.set('50')
		self.settings_tip_tray_8_sv = StringVar()
		self.settings_tip_tray_8_sv.set('50')
		self.settings_tip_tray_9_sv = StringVar()
		self.settings_tip_tray_9_sv.set('50')
		self.settings_tip_tray_10_sv = StringVar()
		self.settings_tip_tray_10_sv.set('50')
		self.settings_tip_tray_11_sv = StringVar()
		self.settings_tip_tray_11_sv.set('50')
		self.settings_tip_tray_12_sv = StringVar()
		self.settings_tip_tray_12_sv.set('50')

		# Volume in tips
		self.pipettor_current_volume = 0

		# Build Protocol
		self.build_protocol_action_list = []

		self.build_protocol_treeview_row_index = 0
		self.status_treeview_row_index = 0
		
		self.title("CDP 2.0 GUI")
		self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
		self.protocol("WM_DELETE_WINDOW", self.on_closing)

		# Treeview style.
		self.style_treeview = tkinter.ttk.Style(self)
		self.style_treeview.theme_use('clam')
		self.style_treeview.configure("Treeview", background='#2b2b2b', fieldbackground='#2b2b2b', foreground='#2b2b2b')
		
		# Create two frames.
		self.grid_columnconfigure(1, weight=1)
		self.grid_rowconfigure(0, weight=1)
		
		self.frame_left = ctk.CTkFrame(master=self, width=180, corner_radius=0)
		self.frame_left.grid(row=0, column=0, sticky='nswe')

		self.frame_right = ctk.CTkFrame(master=self)
		self.frame_right.grid(row=0, column=1, sticky='nswe', padx=20, pady=10, columnspan=3)

		# Left Frame.
		self.label_image = ctk.CTkLabel(master=self.frame_left, text="CDP 2.0", font=("Roboto Medium", -16))
		self.label_image.grid(row=1, column=0, pady=10, padx=10)
		self.button_image = ctk.CTkButton(master=self.frame_left, text='Image', command=lambda button_text='Image': self.on_button_click(button_text))
		self.button_image.grid(row=2, column=0, pady=10, padx=20)
		self.button_thermocycle = ctk.CTkButton(master=self.frame_left, text='Thermocycle', command=lambda button_text='Thermocycle': self.on_button_click(button_text))
		self.button_thermocycle.grid(row=3, column=0, pady=10, padx=20)
		self.button_build_protocol = ctk.CTkButton(master=self.frame_left, text="Build Protocol", command=lambda button_text="Build Protocol": self.on_button_click(button_text))
		self.button_build_protocol.grid(row=4, column=0, pady=10, padx=20)
		self.button_optimize = ctk.CTkButton(master=self.frame_left, text='Optimize', command=lambda button_text='Optimize': self.on_button_click(button_text))
		self.button_optimize.grid(row=5, column=0, pady=10, padx=20)
		self.button_service = ctk.CTkButton(master=self.frame_left, text='Service', command=lambda button_text='Service': self.on_button_click(button_text))
		self.button_service.grid(row=6, column=0, pady=10, padx=20)
		self.button_status = ctk.CTkButton(master=self.frame_left, text='Status', command=lambda button_text='Status': self.on_button_click(button_text))
		self.button_status.grid(row=7, column=0, pady=10, padx=20)
		self.button_configure = ctk.CTkButton(master=self.frame_left, text='Configure', command=lambda button_text='Configure': self.on_button_click(button_text))
		self.button_configure.grid(row=8, column=0, pady=10, padx=20)

	def __toggle_frame_left_button_background(self, button_text):
		self.button_image.configure(border_width=0)
		self.button_thermocycle.configure(border_width=0)
		self.button_build_protocol.configure(border_width=0)
		self.button_optimize.configure(border_width=0)
		self.button_service.configure(border_width=0)
		self.button_status.configure(border_width=0)
		self.button_configure.configure(border_width=0)
		if button_text == 'Image':
			self.button_image.configure(border_color='#ffffff', border_width=2)
		elif button_text == 'Thermocycle':
			self.button_thermocycle.configure(border_color='#ffffff', border_width=2)
		elif button_text == "Build Protocol":
			self.button_build_protocol.configure(border_color='#ffffff', border_width=2)
		elif button_text == 'Optimize':
			self.button_optimize.configure(border_color='#ffffff', border_width=2)
		elif button_text == 'Service':
			self.button_service.configure(border_color='#ffffff', border_width=2)
			self.service_topic_sv.set('')
		elif button_text == 'Status':
			self.button_status.configure(border_color='#ffffff', border_width=2)
		elif button_text == 'Configure':
			self.button_configure.configure(border_color='#ffffff', border_width=2)

	def on_button_click(self, button_text):
		# Clean up the Right Frame for updating
		for widget in self.frame_right.winfo_children():
			widget.destroy()
		self.__toggle_frame_left_button_background(button_text)
		if button_text == 'Image':
			# Image: View
			self.textbox_image_view = ctk.CTkTextbox(master=self.frame_right, width=400, height=400, font=("Roboto Medium", -12), state='disabled')
			self.textbox_image_view.place(x=10,y=10)
			# Image: Relative Moves
			self.label_image_relative_moves = ctk.CTkLabel(master=self.frame_right, text="Relative Moves", font=("Roboto Medium", -16))
			self.label_image_relative_moves.place(x=150,y=420)
			# Image: Relative Moves (dx)
			self.label_image_dx = ctk.CTkLabel(master=self.frame_right, text='dx', font=("Roboto Medium", -14))
			self.label_image_dx.place(x=30, y=455)
			self.entry_image_dx = ctk.CTkEntry(master=self.frame_right, textvariable=self.image_dx_sv, font=("Roboto Medium", -14), width=80)
			self.entry_image_dx.place(x=60,y=455)
			# Image: Relative Moves (dy)
			self.label_image_dy = ctk.CTkLabel(master=self.frame_right, text='dy', font=("Roboto Medium", -14))
			self.label_image_dy.place(x=150, y=455)
			self.entry_image_dy = ctk.CTkEntry(master=self.frame_right, textvariable=self.image_dy_sv, font=("Roboto Medium", -14), width=80)
			self.entry_image_dy.place(x=180,y=455)
			# Image: Relative Moves (dz)
			self.label_image_dz = ctk.CTkLabel(master=self.frame_right, text='dz', font=("Roboto Medium", -14))
			self.label_image_dz.place(x=270, y=455)
			self.entry_image_dz = ctk.CTkEntry(master=self.frame_right, textvariable=self.image_dz_sv, font=("Roboto Medium", -14), width=80)
			self.entry_image_dz.place(x=300,y=455)
			# Image: Filters
			self.label_image_filter = ctk.CTkLabel(master=self.frame_right, text='Filter', font=("Roboto Medium", -16))
			self.label_image_filter.place(x=470,y=10)
			self.optionmenu_image_filter = ctk.CTkOptionMenu(master=self.frame_right, variable=self.image_filter_sv, values=('HEX', 'FAM', 'ATTO590', 'ALEXA405', 'CY5', 'CY5.5', 'Home'))
			self.optionmenu_image_filter.place(x=425,y=40, width=120)
			# Image: LED
			self.label_image_led = ctk.CTkLabel(master=self.frame_right, text='LED', font=("Roboto Medium", -16))
			self.label_image_led.place(x=475, y=70)
			self.optionmenu_image_led = ctk.CTkOptionMenu(master=self.frame_right, variable=self.image_led_sv, values=('HEX', 'FAM', 'ATTO590', 'ALEXA405', 'CY5', 'CY5.5', 'Off'))
			self.image_led_sv.trace('w', self.callback_image_led_sv)
			self.optionmenu_image_led.place(x=425, y=100, width=120)
			# Image: Options
			self.label_image_options = ctk.CTkLabel(master=self.frame_right, text='Options', font=("Roboto Medium", -16))
			self.label_image_options.place(x=460, y=130)
			# Image: Brightfield
			self.button_image_brightfield = ctk.CTkButton(master=self.frame_right, text='Brightfield', font=("Roboto Medium", -16), width=120, command=self.brightfield, height=30)
			self.button_image_brightfield.place(x=425, y=160)
			# Image: Auto-Focus
			self.button_image_auto_focus = ctk.CTkButton(master=self.frame_right, text='Auto-Focus', font=("Roboto Medium", -16), width=120, command=self.auto_focus, height=30)
			self.button_image_auto_focus.place(x=425, y=200)
			# Image: Save View
			self.button_image_save_view = ctk.CTkButton(master=self.frame_right, text="Save View", font=("Roboto Medium", -16), width=120, command=self.save_view, height=30)
			self.button_image_save_view.place(x=425, y=240)
			# Image: Load View
			self.button_image_load_view = ctk.CTkButton(master=self.frame_right, text="Load View", font=("Roboto Medium", -16), width=120, command=self.load_view, height=30)
			self.button_image_load_view.place(x=425, y=280)
			# Image: Scan Chip
			self.button_image_scan_chip = ctk.CTkButton(master=self.frame_right, text="Scan Chip", font=("Roboto Medium", -16), width=120, command=self.scan_chip, height=30)
			self.button_image_scan_chip.place(x=425, y=320)
			# Image: Home Imager
			self.button_image_home_imager = ctk.CTkButton(master=self.frame_right, text="Home Imager", font=("Roboto Medium", -16), width=120, command=self.home_imager, height=30)
			self.button_image_home_imager.place(x=425, y=360)
			# Image: LED Intensity
			self.label_image_led_intensity = ctk.CTkLabel(master=self.frame_right, text="LED Intensity", font=("Roboto Medium", -16))
			self.label_image_led_intensity.place(x=435,y=400)
			self.slider_image_led_intensity = ctk.CTkSlider(master=self.frame_right, from_=0, to=100, number_of_steps=10, progress_color='green', command=self.slider_image_led_intensity_event, width=120, height=20)
			self.slider_image_led_intensity.set(0)
			self.slider_image_led_intensity.configure(state='disabled')
			self.slider_image_led_intensity.place(x=420,y=440)
		elif button_text == 'Thermocycle':
			# Thermocycle
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
			#self.thermocycler_cycles_sv = StringVar()
			#thermocycler_cycles_sv.set(str(self.thermocyclers['cycles'][thermocycler]))
			self.entry_thermocycler_cycles = ctk.CTkEntry(master=self.frame_right, textvariable=self.thermocycler_cycles_sv)
			self.entry_thermocycler_cycles.bind('<FocusOut>', self.callback_thermocycler_cycles)
			self.entry_thermocycler_cycles.place(x=150, y=80)
			image = Image.open(self.thermocycler_png_name).resize((250, 470))
			self.img_thermocycler = ImageTk.PhotoImage(image)
			self.label_thermocycler = ctk.CTkLabel(master=self.frame_right, text='thermocycler', font=("Roboto Light", -1), image=self.img_thermocycler)
			self.label_thermocycler.place(x=310, y=5) 
			self.label_thermocycler.bind('<Button-1>', self.on_click)
			self.button_start_thermocyclers = ctk.CTkButton(master=self.frame_right, text='Start', command=self.start_thermocyclers, fg_color='#4C7BD3')
			self.button_start_thermocyclers.place(x=45, y=465, width=55)
			self.button_import = ctk.CTkButton(master=self.frame_right, text='Load', command=self.import_thermocyclers)
			self.button_import.place(x=105, y=465, width=55)
			self.button_export = ctk.CTkButton(master=self.frame_right, text='Save', command=self.export_thermocyclers)
			self.button_export.place(x=165, y=465, width=55) 
			self.button_home_thermocyclers = ctk.CTkButton(master=self.frame_right, text='Home', command=self.home_thermocyclers)
			self.button_home_thermocyclers.place(x=225, y=465, width=55)
			# Progress Bar
			self.progressbar_thermocyclers = ctk.CTkProgressBar(master=self.frame_right, orientation='horizontal', mode='determinate', progress_color='green', height=25, corner_radius=0, width=260)
			self.progressbar_thermocyclers.set(0)
			self.progressbar_thermocyclers.place(x=30,y=432)
			self.plot_thermocycler(self.thermocyclers['temperatures']['A'])
			self.label_thermocycler_denature = ctk.CTkLabel(master=self.frame_right, text_color='white', text='1st Denature', font=("Roboto Light",-12))
			self.label_thermocycler_denature.place(x=35, y=120, width=100)
			self.label_thermocycler_anneal = ctk.CTkLabel(master=self.frame_right, text_color='white', text='Anneal', font=("Roboto Light", -12))
			self.label_thermocycler_anneal.place(x=135, y=120, width=60)
			self.label_thermocycler_extension = ctk.CTkLabel(master=self.frame_right, text_color='white', text='2nd Denature', font=("Roboto Light", -12))
			self.label_thermocycler_extension.place(x=195, y=120, width=100)
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
			# Thermocycler Checkboxes
			self.label_thermocycler_A = ctk.CTkLabel(master=self.frame_right, text='A', font=("Roboto Medium", -12))
			self.label_thermocycler_A.place(x=320, y=475)
			self.checkbox_thermocycler_A = ctk.CTkCheckBox(master=self.frame_right, variable=self.use_thermocycler_A, onvalue=1, offvalue=0, text='')
			self.checkbox_thermocycler_A.place(x=340, y=475)
			self.label_thermocycler_B = ctk.CTkLabel(master=self.frame_right, text='B', font=("Roboto Medium", -12))
			self.label_thermocycler_B.place(x=380, y=475)
			self.checkbox_thermocycler_B = ctk.CTkCheckBox(master=self.frame_right, variable=self.use_thermocycler_B, onvalue=1, offvalue=0, text='')
			self.checkbox_thermocycler_B.place(x=400, y=475)
			self.label_thermocycler_C = ctk.CTkLabel(master=self.frame_right, text='C', font=("Roboto Medium", -12))
			self.label_thermocycler_C.place(x=440, y=475)
			self.checkbox_thermocycler_C = ctk.CTkCheckBox(master=self.frame_right, variable=self.use_thermocycler_C, onvalue=1, offvalue=0, text='')
			self.checkbox_thermocycler_C.place(x=460, y=475)
			self.label_thermocycler_D = ctk.CTkLabel(master=self.frame_right, text='D', font=("Roboto Medium", -12))
			self.label_thermocycler_D.place(x=500, y=475)
			self.checkbox_thermocycler_D = ctk.CTkCheckBox(master=self.frame_right, variable=self.use_thermocycler_D, onvalue=1, offvalue=0, text='')
			self.checkbox_thermocycler_D.place(x=520, y=475)
		elif button_text == "Build Protocol":
			# Script builder defaults
			# Tips: 
			self.label_build_protocol_tips = ctk.CTkLabel(master=self.frame_right, text='Tips', font=("Roboto Medium", -16))
			self.label_build_protocol_tips.place(x=5, y=40)
			# Tips: Tray
			self.label_build_protocol_tips_tray = ctk.CTkLabel(master=self.frame_right, text='Tray', font=("Roboto Light", -14))
			self.label_build_protocol_tips_tray.place(x=190, y=10)
			self.build_protocol_tips_tray_sv = StringVar('')
			self.optionmenu_build_protocol_tips_tray = ctk.CTkOptionMenu(master=self.frame_right, variable=self.build_protocol_tips_tray_sv, values=('A', 'B', 'C', 'D', "Tip Transfer Tray", ''), font=("Roboto Light", -14)) 
			self.optionmenu_build_protocol_tips_tray.place(x=80, y=40, width=250)
			# Tips: Column
			self.label_build_protocol_tips_column = ctk.CTkLabel(master=self.frame_right, text='Column', font=("Roboto Light", -14))
			self.label_build_protocol_tips_column.place(x=345, y=10)
			self.build_protocol_tips_column_sv = StringVar('')
			self.optionmenu_build_protocol_tips_column = ctk.CTkOptionMenu(master=self.frame_right, variable=self.build_protocol_tips_column_sv, values=('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', ''), font=("Roboto Light", -14))
			self.optionmenu_build_protocol_tips_column.place(x=335, y=40, width=65)
			# Tips: Action
			self.label_build_protocol_tips_action = ctk.CTkLabel(master=self.frame_right, text='Action', font=("Roboto Medium", -14))
			self.label_build_protocol_tips_action.place(x=435, y=10)
			self.build_protocol_tips_action_sv = StringVar()
			self.build_protocol_tips_action_sv.set('Eject')
			self.optionmenu_build_protocol_tips_action = ctk.CTkOptionMenu(master=self.frame_right, variable=self.build_protocol_tips_action_sv, values=('Eject', 'Pickup'), font=("Roboto Light", -14))
			self.optionmenu_build_protocol_tips_action.place(x=405, y=40, width=100)
			# Tips: Add
			self.label_build_protocol_tips_add = ctk.CTkLabel(master=self.frame_right, text='Add', font=("Roboto Light", -14))
			self.label_build_protocol_tips_add.place(x=517, y=10)
			self.button_build_protocol_tips_add = ctk.CTkButton(master=self.frame_right, text='', command=self.build_protocol_tips_add, fg_color='#4C7BD3') 
			self.button_build_protocol_tips_add.place(x=510, y=40, width=40)
			# Motion:
			self.label_build_protocol_motion = ctk.CTkLabel(master=self.frame_right, text='Motion', font=("Roboto Medium", -16))
			self.label_build_protocol_motion.place(x=5, y=100)
			# Motion: Consumable
			self.label_build_protocol_motion_consumable = ctk.CTkLabel(master=self.frame_right, text='Consumable', font=("Roboto Light", -14))
			self.label_build_protocol_motion_consumable.place(x=163, y=70) #30,150
			self.build_protocol_motion_consumable_sv = StringVar('')
			self.optionmenu_build_protocol_motion_consumable = ctk.CTkOptionMenu(master=self.frame_right, variable=self.build_protocol_motion_consumable_sv, values=("Reagent Cartridge", "Sample Rack", "Heater/Shaker", "Mag Separator", "Assay Strip", "Chiller", "Pre-Amp Thermocycler", "Quant Strip", "Aux Heater", "Tray CD NIPT", "Tray CD FF", "Tray CD Quant", "DG8 1000"), font=("Roboto Light", -14)) 
			self.optionmenu_build_protocol_motion_consumable.place(x=80, y=100, width=235)
			# Motion: Tray
			self.label_build_protocol_motion_tray = ctk.CTkLabel(master=self.frame_right, text='Tray', font=("Roboto Light", -14))
			self.label_build_protocol_motion_tray.place(x=330, y=70)
			self.build_protocol_motion_tray_sv = StringVar('')
			self.optionmenu_build_protocol_motion_tray = ctk.CTkOptionMenu(master=self.frame_right, variable=self.build_protocol_motion_tray_sv, values=('A', 'B', 'C', 'D', ''))
			self.optionmenu_build_protocol_motion_tray.place(x=320,y=100,width=50)
			# Motion: Column
			self.label_build_protocol_motion_column = ctk.CTkLabel(master=self.frame_right, text='Column', font=("Roboto Light", -14))
			self.label_build_protocol_motion_column.place(x=375, y=70)
			self.build_protocol_motion_column_sv = StringVar('')
			self.optionmenu_build_protocol_motion_column = ctk.CTkOptionMenu(master=self.frame_right, variable=self.build_protocol_motion_column_sv, values=('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', ''), font=("Roboto Light", -14))
			self.optionmenu_build_protocol_motion_column.place(x=375, y=100, width=55)
			# Motion: Tip
			self.label_build_protocol_motion_tip = ctk.CTkLabel(master=self.frame_right, text='Tip (uL)', font=("Roboto Light", -14))
			self.label_build_protocol_motion_tip.place(x=445, y=70)
			self.build_protocol_motion_tip_sv = StringVar()
			self.build_protocol_motion_tip_sv.set('1000')
			self.optionmenu_build_protocol_motion_tip = ctk.CTkOptionMenu(master=self.frame_right, variable=self.build_protocol_motion_tip_sv, values=('1000', '50', '200', 'None'), font=("Roboto Light", -14)) 
			self.optionmenu_build_protocol_motion_tip.place(x=435,y=100,width=70)
			# Motion: Add
			self.label_build_protocol_motion_add = ctk.CTkLabel(master=self.frame_right, text='Add', font=("Roboto Light", -14))
			self.label_build_protocol_motion_add.place(x=517, y=70)
			self.button_build_protocol_motion_add = ctk.CTkButton(master=self.frame_right, text='', command=self.build_protocol_motion_add, fg_color='#4C7BD3') 
			self.button_build_protocol_motion_add.place(x=510, y=100, width=40)
			# Pipettor:
			self.label_build_protocol_pipettor = ctk.CTkLabel(master=self.frame_right, text='Pipettor', font=("Roboto Medium", -16))
			self.label_build_protocol_pipettor.place(x=5, y=160)
			# Pipettor: Volume
			self.label_build_protocol_pipettor_volume = ctk.CTkLabel(master=self.frame_right, text='Volume (uL)', font=("Roboto Medium", -14))
			self.label_build_protocol_pipettor_volume.place(x=92, y=130)
			self.entry_build_protocol_pipettor_volume = ctk.CTkEntry(master=self.frame_right)
			self.entry_build_protocol_pipettor_volume.place(x=85, y=160, width=95)
			# Pipettor: Tip
			self.label_build_protocol_pipettor_tip = ctk.CTkLabel(master=self.frame_right, text='Tip (uL)', font=("Roboto Medium", -14))
			self.label_build_protocol_pipettor_tip.place(x=200, y=130)
			self.build_protocol_pipettor_tip = StringVar()
			self.build_protocol_pipettor_tip.set('1000')
			self.optionmenu_build_protocol_pipettor_tip = ctk.CTkOptionMenu(master=self.frame_right, variable=self.build_protocol_pipettor_tip, values=('1000', '50', '200'))
			self.optionmenu_build_protocol_pipettor_tip.place(x=185, y=160, width=70)
			# Pipettor: Action
			self.label_build_protocol_pipettor_action = ctk.CTkLabel(master=self.frame_right, text='Action', font=("Roboto Medium", -14))
			self.label_build_protocol_pipettor_action.place(x=295,y=130)
			self.build_protocol_pipettor_action_sv = StringVar()
			self.build_protocol_pipettor_action_sv.set('Aspirate')
			self.optionmenu_build_protocol_pipettor_action = ctk.CTkOptionMenu(master=self.frame_right, variable=self.build_protocol_pipettor_action_sv, values=('Aspirate', 'Dispense', 'Mix'))
			self.optionmenu_build_protocol_pipettor_action.place(x=260, y=160, width=120)
			# Pipettor: Pressure
			self.label_build_protocol_pipettor_pressure = ctk.CTkLabel(master=self.frame_right, text='Pressure', font=("Roboto Medium", -14))
			self.label_build_protocol_pipettor_pressure.place(x=420, y=130)
			self.build_protocol_pipettor_pressure_sv = StringVar()
			self.build_protocol_pipettor_pressure_sv.set('High')
			self.optionmenu_build_protocol_pipettor_pressure = ctk.CTkOptionMenu(master=self.frame_right, variable=self.build_protocol_pipettor_pressure_sv, values=('High', 'Low'))
			self.optionmenu_build_protocol_pipettor_pressure.place(x=385, y=160, width=120)
			# Pipettor: Add
			self.label_build_protocol_pipettor_add = ctk.CTkLabel(master=self.frame_right, text='Add', font=("Roboto Light", -14))
			self.label_build_protocol_pipettor_add.place(x=517, y=130)
			self.button_build_protocol_pipettor_add = ctk.CTkButton(master=self.frame_right, text='', command=self.build_protocol_pipettor_add, fg_color='#4C7BD3') 
			self.button_build_protocol_pipettor_add.place(x=510, y=160, width=40)
			# Time:
			self.label_build_protocol_time = ctk.CTkLabel(master=self.frame_right, text='Time', font=("Roboto Medium", -16))
			self.label_build_protocol_time.place(x=5, y=220)
			# Time: Delay
			self.label_build_protocol_time_delay = ctk.CTkLabel(master=self.frame_right, text='Delay', font=("Roboto Medium", -14))
			self.label_build_protocol_time_delay.place(x=100,y=190)
			self.entry_build_protocol_time_delay = ctk.CTkEntry(master=self.frame_right)
			self.entry_build_protocol_time_delay.place(x=80, y=220, width=80)
			# Time: Units
			self.label_build_protocol_time_units = ctk.CTkLabel(master=self.frame_right, text='Units', font=("Roboto Medium", -14))
			self.label_build_protocol_time_units.place(x=215,y=190)
			self.build_protocol_time_units_sv = StringVar()
			self.build_protocol_time_units_sv.set('seconds')
			self.optionmenu_build_protocol_time_units = ctk.CTkOptionMenu(master=self.frame_right, variable=self.build_protocol_time_units_sv, values=('seconds', 'minutes'))
			self.optionmenu_build_protocol_time_units.place(x=165, y=220, width=120)
			# Time: Add
			self.label_build_protocol_time_add = ctk.CTkLabel(master=self.frame_right, text='Add', font=("Roboto Light", -14))
			self.label_build_protocol_time_add.place(x=297, y=190)
			self.button_build_protocol_time_add = ctk.CTkButton(master=self.frame_right, text='', command=self.build_protocol_time_add, fg_color='#4C7BD3') 
			self.button_build_protocol_time_add.place(x=290, y=220, width=40)
			# Other:
			self.label_build_protocol_other = ctk.CTkLabel(master=self.frame_right, text='Other', font=("Roboto Medium", -16))
			self.label_build_protocol_other.place(x=5, y=280)
			# Other: Options
			self.label_build_protocol_other_options = ctk.CTkLabel(master=self.frame_right, text='Options', font=("Roboto Medium", -16))
			self.label_build_protocol_other_options.place(x=150, y=250)
			self.build_protocol_other_sv = StringVar()
			self.build_protocol_other_sv.set("Home Pipettor")
			self.optionmenu_build_protocol_other = ctk.CTkOptionMenu(master=self.frame_right, variable=self.build_protocol_other_sv, values=("Home Pipettor", "Tip Press for 50 uL tips", "Tip Press for 1000 uL tips", "Move Relative Left", "Move Relative Right", "Move Relative Backwards", "Move Relative Forwards", "Move Relative Down", "Move Relative Up", 'Generate Standard Droplets', 'Generate Pico Droplets', 'Extraction', 'Transfer Plasma', 'Binding', 'Pooling', 'Wash 1', 'Wash 2', 'Pre-Elution', 'Elution', 'Assay Prep', 'Pre-Amp', 'Shake On', 'Shake Off', 'Engage Magnet', 'Disengage Magnet', "Pre-Amp Thermocycle (Not Functional)", "Move Lid (Not Functional)", "Move Chip (Not Functional)"))
			self.optionmenu_build_protocol_other.place(x=85, y=280, width=200)
			# Other: Add
			self.label_build_protocol_time_add = ctk.CTkLabel(master=self.frame_right, text='Add', font=("Roboto Light", -14))
			self.label_build_protocol_time_add.place(x=297, y=250)
			self.button_build_protocol_other_add = ctk.CTkButton(master=self.frame_right, text='', command=self.build_protocol_other_add, fg_color='#4C7BD3') 
			self.button_build_protocol_other_add.place(x=290, y=280, width=40)
			# Estimated time
			self.label_estimated_time = ctk.CTkLabel(master=self.frame_right, text="Estimated Time: 0 minutes", font=("Roboto Light", -14))
			self.label_estimated_time.place(x=360,y=215)
			# Action Progress
			self.label_action_progress = ctk.CTkLabel(master=self.frame_right, text="Action Progress: 0 of 0", font=("Roboto Light", -14))
			self.label_action_progress.place(x=360,y=235)
			# Progress Bar
			#self.progressbar_build_protocol = tkinter.ttk.Progressbar(master=self.frame_right, orient='horizontal', length=195, mode = 'determinate')
			self.progressbar_build_protocol = ctk.CTkProgressBar(master=self.frame_right, orientation='horizontal', mode='determinate', width=195, progress_color='green', height=25, corner_radius=0)
			self.progressbar_build_protocol.set(0)
			self.progressbar_build_protocol.place(x=350,y=265)
			# Start
			self.button_build_protocol_start = ctk.CTkButton(master=self.frame_right, text='Start', command=self.build_protocol_start, fg_color='#4C7BD3')
			self.button_build_protocol_start.place(x=460, y=330, width=85)
			# Import
			self.button_build_protocol_import = ctk.CTkButton(master=self.frame_right, text='Load', command=self.build_protocol_import)
			self.button_build_protocol_import.place(x=460, y=360, width=85)
			# Export
			self.button_build_protocol_export = ctk.CTkButton(master=self.frame_right, text='Save', command=self.build_protocol_export)
			self.button_build_protocol_export.place(x=460, y=390, width=85)
			# Delete 
			self.button_build_protocol_delete = ctk.CTkButton(master=self.frame_right, text='Delete', command=self.build_protocol_delete, fg_color='#b81414')
			self.button_build_protocol_delete.place(x=460, y=420, width=85)
			# Treeview
			self.scrollbar_treeview_build_protocol = tkinter.Scrollbar(self.frame_right, orient='horizontal')
			self.treeview_build_protocol = tkinter.ttk.Treeview(self.frame_right, columns=('Action'), show='headings', xscrollcommand=self.scrollbar_treeview_build_protocol.set)
			self.scrollbar_treeview_build_protocol.config(command=self.treeview_build_protocol.xview)
			self.treeview_build_protocol.column('Action', width=440, stretch=False)
			self.treeview_build_protocol.heading('Action', text='Action')
			self.treeview_build_protocol.place(x=5,y=320, width=440, height=160)
			self.scrollbar_treeview_build_protocol.place(x=5, y=480, width=440)
			self.treeview_build_protocol.bind('<Double-Button-1>', self.on_click)
			self.treeview_build_protocol.bind('<Control-c>', self.copy)
			self.treeview_build_protocol.bind('<Control-v>', self.paste)
			self.__fill_build_protocol_treeview()
		elif button_text == 'Optimize':
			image = Image.open('deck_plate.png').resize((560, 430))
			self.img_deck_plate = ImageTk.PhotoImage(image)
			self.label_deck_plate = ctk.CTkLabel(master=self.frame_right, text='deck_plate', font=("Roboto Medium", -1), image=self.img_deck_plate)
			self.label_deck_plate.bind('<ButtonPress-1>', self.on_click)
			self.label_deck_plate.bind('<ButtonRelease-1>', self.on_release)
			self.label_deck_plate.bind('<MouseWheel>', self.mouse_wheel)
			self.label_deck_plate.place(x=0, y=40) 
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
			# Checkboxes: Use Z
			self.checkbox_use_z = ctk.CTkCheckBox(master=self.frame_right, text="Use Z", variable=self.use_z, onvalue=1, offvalue=0) 
			self.checkbox_use_z.place(x=210, y=40, width=100)
			# Checkboxes: Slow z
			self.checkbox_slow_z = ctk.CTkCheckBox(master=self.frame_right, text="Slow Z", variable=self.slow_z, onvalue=1, offvalue=0)
			self.checkbox_slow_z.place(x=210, y=70, width=100)
			# Home buttons
			self.button_home = ctk.CTkButton(master=self.frame_right, text='Home', font=("Roboto Medium", -16), width=60, command=self.home_pipettor, height=45)
			self.button_home.place(x=340, y=45)
			self.button_home_z = ctk.CTkButton(master=self.frame_right, text="Home Z", font=("Roboto Medium", -12), width=60, command=self.home_pipettor_z)
			self.button_home_z.place(x=120, y=470)
			self.button_home_y = ctk.CTkButton(master=self.frame_right, text="Home Y", font=("Roboto Medium", -12), width=60, command=self.home_pipettor_y)
			self.button_home_y.place(x=185, y=470)
			self.button_home_x = ctk.CTkButton(master=self.frame_right, text="Home X", font=("Roboto Medium", -12), width=60, command=self.home_pipettor_x)
			self.button_home_x.place(x=250, y=470)
			# Move Button
			self.button_move = ctk.CTkButton(master=self.frame_right, text='Move', font=("Roboto Medium", -16), width=60, command=self.optimize_move_pipettor, height=45)
			self.button_move.place(x=410, y=45)
			# Update button
			self.button_update = ctk.CTkButton(master=self.frame_right, text='Update', font=("Roboto Medium", -16), width=60, command=self.update_coordinate, height=45, fg_color='#4C7BD3') 
			self.button_update.place(x=480, y=45)
			# Print button
			self.button_print = ctk.CTkButton(master=self.frame_right, text='Print', font=("Roboto Medium", -14), width=60, command=self.print_coordinate, height=25, fg_color='#4C7BD3')
			self.button_print.place(x=5, y=470)
		elif button_text == 'Service':
			# Service Topic
			self.label_service_topic = ctk.CTkLabel(master=self.frame_right, text='Service Topic', font=("Roboto Medium", -16))
			self.label_service_topic.place(x=10,y=10)
			self.optionmenu_service_topic = ctk.CTkOptionMenu(master=self.frame_right, variable=self.service_topic_sv, values=('Aspirate', 'Dispense', 'Air Valve', 'Motion', 'Tip Eject', 'Suction Cups', 'Coordinates', 'Pipette Tip Leak', 'Loose Pipettor Mandrels', 'LEDs Turn Off'), command=self.callback_service_topic)
			self.optionmenu_service_topic.place(x=130,y=10,width=200)
			# Service Tips
			self.textbox_service_tips = ctk.CTkTextbox(master=self.frame_right, width=540, height=300, font=("Roboto Medium", -12), state='disabled')
			self.textbox_service_tips.place(x=10, y=45)
			# Service Functions
			self.label_service_functions = ctk.CTkLabel(master=self.frame_right, text="Service Functions", font=("Roboto Medium", -16))
			self.label_service_functions.place(x=205, y=350)
		elif button_text == 'Status':
			# Unit A Status
			self.radiobutton_status_unit_A_iv = tkinter.IntVar(0)
			self.radiobutton_status_unit_A = ctk.CTkRadioButton(master=self.frame_right, text="Unit A", variable=self.radiobutton_status_unit_A_iv, command=self.unit_A_status_radiobutton_event)
			self.radiobutton_status_unit_A.place(x=5, y=10)
			# Unit B Status
			self.radiobutton_status_unit_B_iv = tkinter.IntVar()
			self.radiobutton_status_unit_B_iv.set(1)
			self.radiobutton_status_unit_B = ctk.CTkRadioButton(master=self.frame_right, text="Unit B", variable=self.radiobutton_status_unit_B_iv, command=self.unit_B_status_radiobutton_event)
			self.radiobutton_status_unit_B.place(x=85,y=10)
			# Unit C Status
			self.radiobutton_status_unit_C_iv = tkinter.IntVar()
			self.radiobutton_status_unit_C_iv.set(1)
			self.radiobutton_status_unit_C = ctk.CTkRadioButton(master=self.frame_right, text="Unit C", variable=self.radiobutton_status_unit_C_iv, command=self.unit_C_status_radiobutton_event)
			self.radiobutton_status_unit_C.place(x=165,y=10)
			# Unit D Status
			# Unit E Status
			# Unit F Status
			# Treeview
			self.scrollbar_treeview_status = tkinter.Scrollbar(self.frame_right, orient='horizontal')
			self.treeview_status = tkinter.ttk.Treeview(self.frame_right, columns=('Component', "Parent Module", 'Status', 'Priority', 'Note', "Fix By Date", 'Contact', "FW Version"), show='headings', xscrollcommand=self.scrollbar_treeview_status.set)
			self.scrollbar_treeview_status.config(command=self.treeview_status.xview)
			self.treeview_status.column('Component', width=200, stretch=False)
			self.treeview_status.heading('Component', text='Component')
			self.treeview_status.column("Parent Module", width=100, stretch=False)
			self.treeview_status.heading("Parent Module", text="Parent Module")
			self.treeview_status.column('Status', width=60, stretch=False)
			self.treeview_status.heading('Status', text='Status')
			self.treeview_status.column('Priority', width=80, stretch=False)
			self.treeview_status.heading('Priority', text='Priority')
			self.treeview_status.column('Note', width=300, stretch=False)
			self.treeview_status.heading('Note', text='Note')
			#self.treeview_status.column("Fix By", width=60, stretch=False)
			#self.treeview_status.heading("Fix By", text="Fix By")
			self.treeview_status.column("Fix By Date", width=100, stretch=False)
			self.treeview_status.heading("Fix By Date", text="Fix By Date")
			self.treeview_status.column('Contact', width=60, stretch=False)
			self.treeview_status.heading('Contact', text='Contact')
			self.treeview_status.column("FW Version", width=80, stretch=False)
			self.treeview_status.heading("FW Version", text="FW Version")
			self.treeview_status.place(x=5,y=40, width=550, height=440)
			self.scrollbar_treeview_status.place(x=5, y=485, width=550)
			self.load_status_xlsx()
		elif button_text == 'Configure':
			self.label_configure = ctk.CTkLabel(master=self.frame_right, text="Configuration Settings", font=("Roboto Medium", -18))
			self.label_configure.place(x=185,y=5)
			# Unit Settings.
			self.label_settings_unit = ctk.CTkLabel(master=self.frame_right, text="Unit Settings:", font=("Roboto Medium", -14))
			self.label_settings_unit.place(x=115, y=35)
			self.optionmenu_settings_unit = ctk.CTkOptionMenu(master=self.frame_right, variable=self.settings_unit_sv, values=('A', 'B', 'C', 'D', 'E', 'F'), anchor='center', state='disabled')
			self.optionmenu_settings_unit.place(x=225, y=35, width=80)
			# Relative Move Settings
			self.label_settings_relative_move = ctk.CTkLabel(master=self.frame_right, text="Relative Move Settings:", font=("Roboto Medium", -14))
			self.label_settings_relative_move.place(x=50, y=75)
			self.label_settings_dx = ctk.CTkLabel(master=self.frame_right, text='dx', font=("Roboto Medium", -14))
			self.label_settings_dx.place(x=205, y=75)
			self.entry_settings_dx = ctk.CTkEntry(master=self.frame_right, width=70, textvariable=self.dx, font=("Roboto Medium", -12))
			self.entry_settings_dx.bind('<FocusOut>', self.callback_dx)
			self.entry_settings_dx.place(x=225, y=75)
			self.label_settings_dy = ctk.CTkLabel(master=self.frame_right, text='dy', font=("Roboto Medium", -14))
			self.label_settings_dy.place(x=300, y=75)
			self.entry_settings_dy = ctk.CTkEntry(master=self.frame_right, width=70, textvariable=self.dy, font=("Roboto Medium", -12))
			self.entry_settings_dy.bind('<FocusOut>', self.callback_dy)
			self.entry_settings_dy.place(x=320, y=75)
			self.label_settings_dz = ctk.CTkLabel(master=self.frame_right, text='dz', font=("Roboto Medium", -14))
			self.label_settings_dz.place(x=395, y=75)
			self.entry_settings_dz = ctk.CTkEntry(master=self.frame_right, width=70, textvariable=self.dz, font=("Roboto Medium", -12))
			self.entry_settings_dz.bind('<FocusOut>', self.callback_dz)
			self.entry_settings_dz.place(x=415, y=75)
			# Thermocycler Clamp Settings.
			self.label_settings_thermocycler_clamp = ctk.CTkLabel(master=self.frame_right, text="Thermocycler Clamp Settings:", font=("Roboto Medium", -14))
			self.label_settings_thermocycler_clamp.place(x=5, y=115)
			self.label_settings_clamp_A = ctk.CTkLabel(master=self.frame_right, text='A', font=("Roboto Medium", -14))
			self.label_settings_clamp_A.place(x=205, y=115)
			self.entry_settings_clamp_A = ctk.CTkEntry(master=self.frame_right, width=60, textvariable=self.clamp_A_max, font=("Roboto Medium", -12))
			self.entry_settings_clamp_A.bind('<FocusOut>', self.callback_clamp_A_max)
			self.entry_settings_clamp_A.place(x=225, y=115)
			self.label_settings_clamp_B = ctk.CTkLabel(master=self.frame_right, text='B', font=("Roboto Medium", -14))
			self.label_settings_clamp_B.place(x=295, y=115)
			self.entry_settings_clamp_B = ctk.CTkEntry(master=self.frame_right, width=60, textvariable=self.clamp_B_max, font=("Roboto Medium", -12))
			self.entry_settings_clamp_B.bind('<FocusOut>', self.callback_clamp_B_max)
			self.entry_settings_clamp_B.place(x=315, y=115)
			self.label_settings_clamp_C = ctk.CTkLabel(master=self.frame_right, text='C', font=("Roboto Medium", -14))
			self.label_settings_clamp_C.place(x=385, y=115)
			self.entry_settings_clamp_C = ctk.CTkEntry(master=self.frame_right, width=60, textvariable=self.clamp_C_max, font=("Roboto Medium", -12))
			self.entry_settings_clamp_C.bind('<FocusOut>', self.callback_clamp_C_max)
			self.entry_settings_clamp_C.place(x=405, y=115)
			self.label_settings_clamp_D = ctk.CTkLabel(master=self.frame_right, text='D', font=("Roboto Medium", -14))
			self.label_settings_clamp_D.place(x=475, y=115)
			self.entry_settings_clamp_D = ctk.CTkEntry(master=self.frame_right, width=60, textvariable=self.clamp_D_max, font=("Roboto Medium", -12))
			self.entry_settings_clamp_D.bind('<FocusOut>', self.callback_clamp_D_max)
			self.entry_settings_clamp_D.place(x=495, y=115)
			# Heater/Shaker RPM Settings.
			self.label_settings_heater_shaker_rpm = ctk.CTkLabel(master=self.frame_right, text="Heater/Shaker RPM Settings:", font=("Roboto Bold", -14))
			self.label_settings_heater_shaker_rpm.place(x=10, y=155)
			self.entry_settings_heater_shaker_rpm = ctk.CTkEntry(master=self.frame_right, width=60, textvariable=self.heater_shaker_rpm, font=("Roboto Medium", -12))
			self.entry_settings_heater_shaker_rpm.bind('<FocusOut>', self.callback_heater_shaker_rpm)
			self.entry_settings_heater_shaker_rpm.place(x=225, y=155)
			# Tip Tray Box Settings.
			self.label_settings_tip_tray = ctk.CTkLabel(master=self.frame_right, text="Tip Tray Box Settings:", font=("Roboto Bold", -14))
			self.label_settings_tip_tray.place(x=55, y=195)
			# Tip Tray Box Settings #1.
			self.label_settings_tip_tray_1 = ctk.CTkLabel(master=self.frame_right, text='1', font=("Roboto Bold", -14))
			self.label_settings_tip_tray_1.place(x=205, y=195)
			self.optionmenu_settings_tip_tray_1 = ctk.CTkOptionMenu(master=self.frame_right, variable=self.settings_tip_tray_1_sv, values=('1000', '50', '200'), font=("Roboto Bold", -9))
			self.optionmenu_settings_tip_tray_1.place(x=225, y=195, width=60)
			# Tip Tray Box Settings #2.
			self.label_settings_tip_tray_2 = ctk.CTkLabel(master=self.frame_right, text='2', font=("Roboto Bold", -14))
			self.label_settings_tip_tray_2.place(x=295, y=195)
			self.optionmenu_settings_tip_tray_2 = ctk.CTkOptionMenu(master=self.frame_right, variable=self.settings_tip_tray_2_sv, values=('1000', '50', '200'), font=("Roboto Bold", -9))
			self.optionmenu_settings_tip_tray_2.place(x=315, y=195, width=60)
			# Tip Tray Box Settings #3.
			self.label_settings_tip_tray_3 = ctk.CTkLabel(master=self.frame_right, text='3', font=("Roboto Bold", -14))
			self.label_settings_tip_tray_3.place(x=385, y=195)
			self.optionmenu_settings_tip_tray_3 = ctk.CTkOptionMenu(master=self.frame_right, variable=self.settings_tip_tray_3_sv, values=('1000', '50', '200'), font=("Roboto Bold", -9))
			self.optionmenu_settings_tip_tray_3.place(x=405, y=195, width=60)
			# Tip Tray Box Settings #4.
			self.label_settings_tip_tray_4 = ctk.CTkLabel(master=self.frame_right, text='4', font=("Roboto Bold", -14))
			self.label_settings_tip_tray_4.place(x=475, y=195)
			self.optionmenu_settings_tip_tray_4 = ctk.CTkOptionMenu(master=self.frame_right, variable=self.settings_tip_tray_4_sv, values=('1000', '50', '200'), font=("Roboto Bold", -9))
			self.optionmenu_settings_tip_tray_4.place(x=495, y=195, width=60)
			# Tip Tray Box Settings #5.
			self.label_settings_tip_tray_5 = ctk.CTkLabel(master=self.frame_right, text='5', font=("Roboto Bold", -14))
			self.label_settings_tip_tray_5.place(x=205, y=235)
			self.optionmenu_settings_tip_tray_5 = ctk.CTkOptionMenu(master=self.frame_right, variable=self.settings_tip_tray_5_sv, values=('1000', '50', '200'), font=("Roboto Bold", -9))
			self.optionmenu_settings_tip_tray_5.place(x=225, y=235, width=60)
			# Tip Tray Box Settings #6.
			self.label_settings_tip_tray_6 = ctk.CTkLabel(master=self.frame_right, text='6', font=("Roboto Bold", -14))
			self.label_settings_tip_tray_6.place(x=295, y=235)
			self.optionmenu_settings_tip_tray_6 = ctk.CTkOptionMenu(master=self.frame_right, variable=self.settings_tip_tray_6_sv, values=('1000', '50', '200'), font=("Roboto Bold", -9))
			self.optionmenu_settings_tip_tray_6.place(x=315, y=235, width=60)
			# Tip Tray Box Settings #7.
			self.label_settings_tip_tray_7 = ctk.CTkLabel(master=self.frame_right, text='7', font=("Roboto Bold", -14))
			self.label_settings_tip_tray_7.place(x=385, y=235)
			self.optionmenu_settings_tip_tray_7 = ctk.CTkOptionMenu(master=self.frame_right, variable=self.settings_tip_tray_7_sv, values=('1000', '50', '200'), font=("Roboto Bold", -9))
			self.optionmenu_settings_tip_tray_7.place(x=405, y=235, width=60)
			# Tip Tray Box Settings #8.
			self.label_settings_tip_tray_8 = ctk.CTkLabel(master=self.frame_right, text='8', font=("Roboto Bold", -14))
			self.label_settings_tip_tray_8.place(x=475, y=235)
			self.optionmenu_settings_tip_tray_8 = ctk.CTkOptionMenu(master=self.frame_right, variable=self.settings_tip_tray_8_sv, values=('1000', '50', '200'), font=("Roboto Bold", -9))
			self.optionmenu_settings_tip_tray_8.place(x=495, y=235, width=60)
			# Tip Tray Box Settings #9.
			self.label_settings_tip_tray_9 = ctk.CTkLabel(master=self.frame_right, text='9', font=("Roboto Bold", -14))
			self.label_settings_tip_tray_9.place(x=205, y=275)
			self.optionmenu_settings_tip_tray_9 = ctk.CTkOptionMenu(master=self.frame_right, variable=self.settings_tip_tray_9_sv, values=('1000', '50', '200'), font=("Roboto Bold", -9))
			self.optionmenu_settings_tip_tray_9.place(x=225, y=275, width=60)
			# Tip Tray Box Settings #10.
			self.label_settings_tip_tray_10 = ctk.CTkLabel(master=self.frame_right, text='10', font=("Roboto Bold", -14))
			self.label_settings_tip_tray_10.place(x=295, y=275)
			self.optionmenu_settings_tip_tray_10 = ctk.CTkOptionMenu(master=self.frame_right, variable=self.settings_tip_tray_10_sv, values=('1000', '50', '200'), font=("Roboto Bold", -9))
			self.optionmenu_settings_tip_tray_10.place(x=315, y=275, width=60)
			# Tip Tray Box Settings #11.
			self.label_settings_tip_tray_11 = ctk.CTkLabel(master=self.frame_right, text='11', font=("Roboto Bold", -14))
			self.label_settings_tip_tray_11.place(x=385, y=275)
			self.optionmenu_settings_tip_tray_11 = ctk.CTkOptionMenu(master=self.frame_right, variable=self.settings_tip_tray_11_sv, values=('1000', '50', '200'), font=("Roboto Bold", -9))
			self.optionmenu_settings_tip_tray_11.place(x=405, y=275, width=60)
			# Tip Tray Box Settings #12.
			self.label_settings_tip_tray_12 = ctk.CTkLabel(master=self.frame_right, text='12', font=("Roboto Bold", -14))
			self.label_settings_tip_tray_12.place(x=475, y=275)
			self.optionmenu_settings_tip_tray_12 = ctk.CTkOptionMenu(master=self.frame_right, variable=self.settings_tip_tray_12_sv, values=('1000', '50', '200'), font=("Roboto Bold", -9))
			self.optionmenu_settings_tip_tray_12.place(x=495, y=275, width=60)
		#self.update()

	def slider_image_led_intensity_event(self, value):
		print(value)

	def callback_image_led_sv(self, *args):
		colors = {
			'HEX': 6,
			'FAM': 2,
			'ATTO590': 1,
			'ALEXA405': 4,
			'CY5.5': 3,
			'CY5': 5,
			}
		if self.image_led_sv.get() != 'Off':
			self.slider_image_led_intensity.set(100)
			self.slider_image_led_intensity.configure(state='normal')
			for color, channel in colors.items():
				self.fast_api_interface.reader.led.off(5, channel)
			self.fast_api_interface.reader.led.on(5, colors[self.image_led_sv.get()])
		else:
			for color, channel in colors.items():
				self.fast_api_interface.reader.led.off(5, channel)
			self.slider_image_led_intensity.set(0)
			self.slider_image_led_intensity.configure(state='disabled')
		if self.image_led_sv.get() != 'FAM':
			self.brightfield_on = False
		elif self.image_led_sv.get() == 'FAM':
			self.brightfield_on = True

	def auto_focus(self):
		print("HERE")

	def brightfield(self):
		if self.brightfield_on:
			self.image_filter_sv.set('HEX')
			self.image_led_sv.set('Off')
			self.brightfield_on = False
		else:
			self.image_filter_sv.set('HEX')
			self.image_led_sv.set('FAM')
			self.brightfield_on = True

	def save_view(self):
		print("HERE")

	def load_view(self):
		print("HERE")

	def scan_chip(self):
		print("HERE")

	def home_imager(self):
		print("HERE")

	def callback_service_topic(self, event):
		if self.service_topic_sv.get() == 'Aspirate':
			self.textbox_service_tips.configure(state='normal')
			self.textbox_service_tips.delete('0.0', 'end')
			msg = """If Aspiration does not work please check the following:
   - Valve 2
       - Turn on Valve 2 (should hear a click)
       - Turn off Valve 2 (should hear a click)
   - Pneumatic Tubing
       - Disconnect the pneumatic tubing (blue) from Valve 2 and run the aspirate service function to check if there is air flow, if so, put the tubing back in.
       - Disconnect the pneumatic tubing (blue) from the Seyonic Pipettor head and run the aspirate service function to check if there is air flow, if so, put the tubing back in.
       - Make sure that the pneumatic tubing (blue) going into and out of Valve 2 is securely set.
       - Make sure that the pneumatic tubing (blue) going into the Seyonic Pipettor head is securely set
   - Tip Blockage
       - If aspiration takes longer than antisipated the tips may be blocked due to the creation of a vacuum between the pipette tips and the deck plate consumable, to fix this, modify the coordinates z positioning upwards to stop blockage.
   - Seyonic Dispense Controller Software
   - Pipette Filtered Tips Reached
       - If the filters in the pipette tips come in contact with solution the pipette tip may stop apirating as expected and may need to be replaced
			"""
			self.textbox_service_tips.insert("0.0", msg)
			self.textbox_service_tips.configure(state='disabled')
		elif self.service_topic_sv.get() == 'Motion':
			self.textbox_service_tips.configure(state='normal')
			self.textbox_service_tips.delete('0.0', 'end')
			msg = """If motion is not working check the following:
   - Motors Are Engaged
       - Motors are not engaged if relatively little effort is necessary to move the Seyonic Pipettor head freely along the upper gantry, the reader trays are easy to move, the imager is easily shifted by hand, etc.
       - Motors are engaged if relatively little effort is used and motor modules are fixed
   - E-Stop
       - Check that the E-Stop is not pressed but is released
       - Check that the E-Stop is securely connected to the unit
   - Motor Relay
       - Check that the relay labeled 'Motor' is either mechanically switched on or a green LED is lit up indicating it is on
       - Use the Service Function to turn on and off the motor relay (should hear a click)
   - Motor 36V Power Supply
       - Check that the green LED on the 36V Motor Power Supply is on
       - Check that there is a voltage close to 36V on the Motor Power Supply
   - Door Lock 
       - Check that the door lock mechanism is not inhibiting motor motion
   - Local Uvicorn Server Running
       - Ensure that the local Uvicorn Server is running by going to http.
   - Chassis Controller Connected 
       - Ensure that the USB for the Chassis Controller is connected to your PC
   - Other
       - Unplug the grey and teal ethernet cables from the Chassis Controller board, replug them in, and retest motor enagement after you hear a hum
			"""
			self.textbox_service_tips.insert("0.0", msg)
			self.textbox_service_tips.configure(state='disabled')

	def unit_A_status_radiobutton_event(self):
		self.radiobutton_status_unit_B_iv.set(1)
		self.radiobutton_status_unit_C_iv.set(1)
		self.radiobutton_status_unit_A_iv.set(0)

	def unit_B_status_radiobutton_event(self):
		self.radiobutton_status_unit_A_iv.set(1)
		self.radiobutton_status_unit_C_iv.set(1)
		self.radiobutton_status_unit_B_iv.set(0)

	def unit_C_status_radiobutton_event(self):
		self.radiobutton_status_unit_A_iv.set(1)
		self.radiobutton_status_unit_B_iv.set(1)
		self.radiobutton_status_unit_C_iv.set(0)

	def build_protocol_start(self):
		self.button_build_protocol_start.configure(state=tkinter.DISABLED)
		thread = threading.Thread(target=self.start_protocol)
		thread.start()

	def start_protocol(self):
		self.progressbar_build_protocol.set(0)
		self.__update_build_protocol_action_list()
		n_tasks = len(self.build_protocol_action_list)
		i = 0
		for row in self.treeview_build_protocol.get_children():
			self.treeview_build_protocol.selection_set(row)
			action_msg = self.treeview_build_protocol.item(row)['values'][0]
			action_progress_index = int(self.label_action_progress.cget('text').split()[-3]) + 1
			action_progress_text = self.label_action_progress.cget('text').split()
			action_progress_text[-3] = str(action_progress_index)
			action_progress_text = ' '.join(action_progress_text)
			self.label_action_progress.configure(text=action_progress_text)
			
			# Parse the action message to determine which command to run.
			if "Eject" in action_msg:
				if "Tray" not in action_msg:
					self.upper_gantry.tip_eject()
				if "Column" in action_msg:
					split = action_msg.split()
					tray = split[3]
					if tray == 'Tip':
						tray = 'tip_transfer_tray'
					column = int(split[-1])
					self.upper_gantry.tip_eject(tray, column)
			elif "Pickup" in action_msg:
				if "Column" in action_msg:
					split = action_msg.split()
					tray = split[3]
					if tray == 'Tip':
						tray = 'tip_transfer_tray'
					column = int(split[-1])
					self.upper_gantry.tip_pickup(tray, column)
			elif "Move" in action_msg:
				split = action_msg.split()
				consumable = split[2]
				tray = None
				column = None
				pipette_tip_type = None
				if consumable == 'Reagent':
					consumable = "Reagent Cartridge"
				elif consumable == 'Sample':
					consumable = "Sample Rack"
				elif consumable == 'Mag':
					consumable = "Mag Separator"
				elif consumable == 'Assay':
					consumable = "Assay Strip"
				elif consumable == "Pre-Amp":
					consumable = "Pre-Amp Thermocycler"
				elif consumable == 'Qaunt':
					consumable = "Quant Strip"
				elif consumable == 'Aux':
					consumable = "Aux Heater"
				elif consumable == "Tray" and split[3] == 'CD':
					if split[4] == 'NIPT':
						consumable = 'Tray CD NIPT'
					elif split[4] == 'Quant':
						consumable = 'Tray CD Quant'
					elif split[4] == 'FF':
						consumable = 'Tray CD FF'
					split = action_msg.split()
					split = split[3:]
				elif consumable == 'DG8' and split[3] == '1000':
					consumable = "DG8 1000"
				else:
					consumable = consumable
				# Check if a tray is specified
				if 'Tray' in split:
					index = split.index('Tray')
					tray = split[index+1]
				if 'Column' in split:
					index = split.index('Column')
					column = int(split[index+1])
				try:
					pipette_tip_type = int(split[-3])
					if pipette_tip_type == 'None':
						pipette_tip_type = None
				except:
					pipette_tip_type = None
				if consumable.split()[0] == 'DG8' and column == 3 and pipette_tip_type == None:
					from coordinate import coordinates
					dz = coordinates['deck_plate']['dg8']['dz']
					self.upper_gantry.move_pipettor_new(consumable=consumable, tray=tray, row=column, pipette_tip_type=1000, use_drip_plate=False, relative_moves=[0,0,-dz,0])
				else:
					self.upper_gantry.move_pipettor_new(consumable=consumable, tray=tray, row=column, pipette_tip_type=pipette_tip_type, use_drip_plate=False)
			elif "Aspirate" in action_msg:
				split = action_msg.split()
				vol = int(split[1])
				tip = int(split[4])
				pressure = split[8].lower()
				self.upper_gantry.aspirate(vol, pressure=pressure, pipette_tip_type=tip)
			elif "Dispense" in action_msg:
				split = action_msg.split()
				vol = int(split[1])
				tip = int(split[4])
				pressure = split[8].lower()
				self.upper_gantry.dispense(vol, pressure=pressure)
			elif "Mix" in action_msg:
				split = action_msg.split()
				vol = int(split[1])
				tip = int(split[4])
				pressure = split[8].lower()
				self.upper_gantry.aspirate(vol, pressure=pressure, pipette_tip_type=tip)
				self.upper_gantry.dispense(vol, pressure=pressure)
			elif "Delay" in action_msg:
				split = action_msg.split()
				time_value = int(split[2])
				time_unit = split[-1]
				delay(time_value, time_unit)
			elif "Home Pipettor" in action_msg:
				self.upper_gantry.move_pipettor('home', use_drip_plate=False)
				self.upper_gantry.home_pipettor()
			elif "Transfer Plasma" in action_msg:
				self.script.transfer_plasma(self.upper_gantry, full_protocol=False)
			elif "Binding" in action_msg:
				self.script.binding(self.upper_gantry, full_protocol=False)
			elif "Pooling" in action_msg:
				self.script.pooling(self.upper_gantry, full_protocol=False)
			elif "Wash 1" in action_msg:
				self.script.wash(self.upper_gantry, wash_number=1, wash_rounds=2, full_protocol=False)
			elif "Wash 2" in action_msg:
				self.script.wash(self.upper_gantry, wash_number=2, wash_rounds=1, full_protocol=False)
			elif "Pre-Elution" in action_msg:
				self.script.pre_elution(self.upper_gantry, full_protocol=False)
			elif "Elution" in action_msg:
				self.script.elution(self.upper_gantry, full_protocol=False)
			elif "Extraction" in action_msg:
				self.script.extraction(self.upper_gantry, full_protocol=False)
			elif "Generate Standard Droplets" in action_msg:
				self.upper_gantry.generate_droplets('standard')
			elif "Generate Pico Droplets" in action_msg:
				self.upper_gantry.generate_droplets('pico')
			elif "Assay Prep" in action_msg:
				self.script.assay_prep(self.upper_gantry)
			elif "Engage Magnet" in action_msg:
				self.upper_gantry.engage_magnet()
			elif "Disengage Magnet" in action_msg:
				self.upper_gantry.disengage_magnet()
			elif "Move Relative Up" in action_msg:
				delta = int(action_msg.split()[-2])
				self.upper_gantry.move_relative('up', delta, velocity='fast')
			elif "Move Relative Down" in action_msg:
				delta = int(action_msg.split()[-2])
				self.upper_gantry.move_relative('down', delta, velocity='fast')
			elif "Move Relative Left" in action_msg:
				delta = int(action_msg.split()[-2])
				self.upper_gantry.move_relative('left', delta, velocity='fast')
			elif "Move Relative Right" in action_msg:
				delta = int(action_msg.split()[-2])
				self.upper_gantry.move_relative('right', delta, velocity='fast')
			elif "Move Relative Backwards" in action_msg:
				delta = int(action_msg.split()[-2])
				self.upper_gantry.move_relative('backwards', delta, velocity='fast')
			elif "Move Relative Forwards" in action_msg:
				delta = int(action_msg.split()[-2])
				self.upper_gantry.move_relative('forwards', delta, velocity='fast')
			elif "Pre-Amp Thermocycle" in action_msg:
				print('thermocycle')
			elif "Tip Press for 50 uL tips" in action_msg:
				a = [-427900, -1435000, -840000]
			# Update the progress bar for the protocol
			#self.progressbar_build_protocol['value'] = int((i+1) / (n_tasks)) * 100
			self.progressbar_build_protocol.set((i+1) / (n_tasks))
			i = i + 1
		self.button_build_protocol_start.configure(state=tkinter.NORMAL)
		#self.progressbar_build_protocol.set(0)

	def build_protocol_import(self):
		# Write the Build Protocol from a txt file to the Build Protocol Treeview
		file = tkinter.filedialog.askopenfile(initialfile='protocol.txt', initialdir = './', title="Open Protocol to File")
		lines = [line.rstrip('n') for line in file]
		for row in self.treeview_build_protocol.get_children():
			self.treeview_build_protocol.delete(row)
		for line in lines:
			action_msg = line
			self.treeview_build_protocol.insert('', 'end', 'row{0}'.format(self.build_protocol_treeview_row_index), values=(action_msg,))
			self.build_protocol_treeview_row_index = self.build_protocol_treeview_row_index + 1

	def build_protocol_export(self):
		# Write the Build Protocol Treeview to a txt file.
		file = self.browse_files('protocol.txt')
		for row in self.treeview_build_protocol.get_children():
			file.write(f"{self.treeview_build_protocol.item(row)['values'][0]}\n")
		file.close()

	def build_protocol_delete(self):
		try:
			#selected_row = self.treeview_build_protocol.selection()[0]
			for selected_row in self.treeview_build_protocol.selection():
				self.treeview_build_protocol.delete(selected_row)
			self.__update_build_protocol_action_list()
		except:
			pass

	def home_pipettor(self):
		thread = threading.Thread(target=self.upper_gantry.home_pipettor)
		thread.start()
	def home_pipettor_z(self):
		self.fast_api_interface.pipettor_gantry.axis.home('pipettor_gantry', 3, False, True)
	def home_pipettor_y(self):
		self.fast_api_interface.pipettor_gantry.axis.home('pipettor_gantry', 2, False, True)
	def home_pipettor_x(self):
		self.fast_api_interface.pipettor_gantry.axis.home('pipettor_gantry', 1, False, True)

	def optimize_move_pipettor(self):
		# Get the name of the coordinate.
		consumable = self.optionmenu_consumable.get()
		tray = self.optionmenu_tray.get()
		if tray == '':
			tray = None
		column = self.optionmenu_column.get()
		if column == '':
			column = None
		use_z = self.checkbox_use_z.get()
		use_drip_plate = False
		slow_z = self.checkbox_slow_z.get()
		pipette_tip_type = self.optionmenu_tip.get()
		if pipette_tip_type == 'None':
			pipette_tip_type = None
		elif pipette_tip_type != 'None':
			pipette_tip_type = int(pipette_tip_type)
		# Move the pipettor.
		if len(consumable) > 0:
			print(consumable)
			self.upper_gantry.move_pipettor_new(consumable=consumable, tray=tray, row=column, use_z=use_z, use_drip_plate=use_drip_plate, slow_z=slow_z, pipette_tip_type=pipette_tip_type)

	def script_builder_radiobutton_event(self):
		self.radiobutton_drag_tool_iv.set(1)
		self.radiobutton_script_builder_iv.set(0)

	def drag_tool_radiobutton_event(self):
		self.radiobutton_script_builder_iv.set(1)
		self.radiobutton_drag_tool_iv.set(0)

	def __reorder_treeview_build_protocol_rows(self):
		selected_row = self.treeview_build_protocol.selection()[0]
		self.build_protocol_action_list = []
		for row in self.treeview_build_protocol.get_children():
			self.build_protocol_action_list.append(self.treeview_build_protocol.item(row)['values'][0])
			self.treeview_build_protocol.delete(row)
		for i in range(len(self.build_protocol_action_list)):
			self.treeview_build_protocol.insert('','end',f'row{i}',values=(self.build_protocol_action_list[i],))

	def __update_build_protocol_action_list(self):
		self.build_protocol_action_list = []
		for row in self.treeview_build_protocol.get_children():
			self.build_protocol_action_list.append(self.treeview_build_protocol.item(row)['values'][0])
		self.label_action_progress.configure(text=f"Action Progress: 0 of {len(self.build_protocol_action_list)}")

	def __fill_build_protocol_treeview(self):
		for i in range(len(self.build_protocol_action_list)):
			self.treeview_build_protocol.insert('','end',f'row{i}',values=(self.build_protocol_action_list[i],))

	def build_protocol_add(self, action_msg: str):
		try:
			# Get the selected row.
			selected_row = self.treeview_build_protocol.selection()[0]
			print(self.treeview_build_protocol.focus())
			# Insert the data below the selected row
			self.treeview_build_protocol.insert('', int(selected_row.replace('row', ''))+1, iid='row{0}'.format(self.build_protocol_treeview_row_index), values=(action_msg,))
			self.build_protocol_treeview_row_index = self.build_protocol_treeview_row_index + 1
			self.__reorder_treeview_build_protocol_rows()
		except:
			# Insert the data at the bottom
			self.treeview_build_protocol.insert('', 'end', iid='row{0}'.format(self.build_protocol_treeview_row_index), values=(action_msg,))
			self.build_protocol_treeview_row_index = self.build_protocol_treeview_row_index + 1
		self.__update_build_protocol_action_list()

	def build_protocol_tips_add(self):
		action_msg = f"{self.build_protocol_tips_action_sv.get()} tips"# + self.build_protocol_tips_tray_sv.get() + " Column " + self.build_protocol_tips_column_sv.get()
		if self.build_protocol_tips_tray_sv.get() != '':
			action_msg = action_msg + f" Tray {self.build_protocol_tips_tray_sv.get()}"
		if self.build_protocol_tips_column_sv.get() != '':
			action_msg = action_msg + f" Column {self.build_protocol_tips_column_sv.get()}"
		self.build_protocol_add(action_msg)

	def build_protocol_motion_add(self):
		action_msg = f"Move to {self.build_protocol_motion_consumable_sv.get()}"#" Tray {self.build_protocol_motion_tray_sv.get()} Column {self.build_protocol_motion_column_sv.get()} with {self.build_protocol_motion_tip_sv.get()} uL tips"
		if self.build_protocol_motion_tray_sv.get() != '':
			action_msg = action_msg + f" Tray {self.build_protocol_motion_tray_sv.get()}"
		if self.build_protocol_motion_column_sv.get() != '':
			action_msg = action_msg + f" Column {self.build_protocol_motion_column_sv.get()}"
		if self.build_protocol_motion_tip_sv.get() != None:
			action_msg = action_msg + f" with {self.build_protocol_motion_tip_sv.get()} uL tips"
		self.build_protocol_add(action_msg)

	def build_protocol_pipettor_add(self):
		try:
			vol = int(self.entry_build_protocol_pipettor_volume.get())
			tip = int(self.optionmenu_build_protocol_pipettor_tip.get())
			pressure = self.optionmenu_build_protocol_pipettor_pressure.get()
			action_msg = f"{self.build_protocol_pipettor_action_sv.get()} {vol} uL with {tip} uL tips at {pressure.lower()} pressure"
			self.build_protocol_add(action_msg)
		except:
			pass

	def build_protocol_time_add(self):
		if int(self.entry_build_protocol_time_delay.get()) == 1:
			units = self.build_protocol_time_units_sv.get()[:-1]
		else:
			units = self.build_protocol_time_units_sv.get()
		action_msg = f"Delay for {self.entry_build_protocol_time_delay.get()} {units}"
		self.build_protocol_add(action_msg)

	def build_protocol_other_add(self):
		action_msg = self.build_protocol_other_sv.get()
		if 'Up' in action_msg:
			action_msg = action_msg + f" by {self.dz.get()} usteps"
		elif 'Down' in action_msg:
			action_msg = action_msg + f" by {self.dz.get()} usteps"
		elif 'Left' in action_msg:
			action_msg = action_msg + f" by {self.dx.get()} usteps"
		elif 'Right' in action_msg:
			action_msg = action_msg + f" by {self.dx.get()} usteps"
		elif 'Backwards' in action_msg:
			action_msg = action_msg + f" by {self.dy.get()} usteps"
		elif 'Forwards' in action_msg:
			action_msg = action_msg + f" by {self.dy.get()} usteps"
		self.build_protocol_add(action_msg)

	def update_coordinate(self):
		print("Update Coordinate")
		x,y,z,dp = self.upper_gantry.get_position()
		print(x)
		print(y)
		print(z)
		print(dp)
		unit = self.settings_unit_sv.get()
		# Write this to both coordinate.py and to coordinate_{unit}.py

	def print_coordinate(self):
		self.upper_gantry.print_position()

	def callback_dx(self, event):
		self.dx.set(self.entry_settings_dx.get())

	def callback_dy(self, event):
		self.dy.set(self.entry_settings_dy.get())

	def callback_dz(self, event):
		self.dz.set(self.entry_settings_dz.get())

	def __home_thermocyclers(self):
		self.fast_api_interface.reader.axis.home('reader', 8, False)
		self.fast_api_interface.reader.axis.home('reader', 9, False)
		self.fast_api_interface.reader.axis.home('reader', 10, False)
		self.fast_api_interface.reader.axis.home('reader', 11, True)
		self.fast_api_interface.reader.axis.home('reader', 6, False)
		self.fast_api_interface.reader.axis.home('reader', 7, False)
		image = Image.open('thermocycler.png').resize((250, 470))
		self.img_thermocycler = ImageTk.PhotoImage(image)
		self.label_thermocycler.configure(image=self.img_thermocycler)

	def home_thermocyclers(self) -> None:
		thread = threading.Thread(target=self.__home_thermocyclers)
		thread.start()

	def start_thermocyclers(self) -> None:
		# Create a file for logging.\
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
		self.button_start_thermocyclers.configure(state='disabled')
		self.progressbar_thermocyclers.set(0)
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
		self.progressbar_thermocyclers.set(0.1)
		if self.checkbox_thermocycler_A.get():
			meersetter.change_temperature(1, denature_temperature_A, False)
		if self.checkbox_thermocycler_B.get():
			meersetter.change_temperature(2, denature_temperature_B, False)
		if self.checkbox_thermocycler_C.get():
			meersetter.change_temperature(3, denature_temperature_C, False)
		if self.checkbox_thermocycler_D.get():
			meersetter.change_temperature(4, denature_temperature_D, False)
		for sec in range(int(denature_time_A * 60)):
			print(f"Second {sec}")
			time.sleep(1)
		# Thermocycle
		cycles = [i for i in range(self.thermocyclers['cycles']['A'])]
		self.thermocycler_cycles_sv.set(f"0/{len(cycles)}")
		for cycle in cycles:
			#print(f"Cycle Number: {cycle+1}/{len(cycles)}")
			self.thermocycler_cycles_sv.set(f"{cycle+1}/{len(cycles)}")
			#self.progressbar_thermocyclers['value'] = 100 * (cycle+1) / len(cycles) - 10
			self.progressbar_thermocyclers.set((cycle+1) / len(cycles))
			if self.checkbox_thermocycler_A.get():
				meersetter.change_temperature(1, extension_temperature_A, False)
			if self.checkbox_thermocycler_B.get():
				meersetter.change_temperature(2, extension_temperature_B, False)
			if self.checkbox_thermocycler_C.get():
				meersetter.change_temperature(3, extension_temperature_C, False)
			if self.checkbox_thermocycler_D.get():
				meersetter.change_temperature(4, extension_temperature_D, False)
			for sec in range(int(extension_time_A)):
				print(f"Second {sec} for cycle {cycle+1} high")
				time.sleep(1)
			if self.checkbox_thermocycler_A.get():
				meersetter.change_temperature(1, anneal_temperature_A, False)
			if self.checkbox_thermocycler_B.get():
				meersetter.change_temperature(2, anneal_temperature_B, False)
			if self.checkbox_thermocycler_C.get():
				meersetter.change_temperature(3, anneal_temperature_C, False)
			if self.checkbox_thermocycler_D.get():
				meersetter.change_temperature(4, anneal_temperature_D, False)
			for sec in range(int(anneal_time_A)):
				print(f"Second {sec} for cycle {cycle+1} low")
				time.sleep(1)
		# End temperatue
		if self.checkbox_thermocycler_A.get():
			meersetter.change_temperature(1, 30, False)
		if self.checkbox_thermocycler_B.get():
			meersetter.change_temperature(2, 30, False)
		if self.checkbox_thermocycler_C.get():
			meersetter.change_temperature(3, 30, False)
		if self.checkbox_thermocycler_D.get():
			meersetter.change_temperature(4, 30, False)
		# Thermocycling is done.
		self.progressbar_thermocyclers.set(1)
		self.button_start_thermocyclers.configure(state='normal')



	def browse_files(self, default_file_name='thermocycler_protocol.txt'):
		file = tkinter.filedialog.asksaveasfile(initialfile=default_file_name, initialdir = './', title="Save Protocol to File")
		return file

	def import_thermocyclers(self) -> None:
		a = 1

	def export_thermocyclers(self):
		t1 = threading.Thread(target=self.test1)
		t2 = threading.Thread(target=self.test2)
		t1.run()
		t2.run()

	def plot_thermocycler(self, data) -> None:
		fig = Figure(figsize=(3,2.4))
		fig.set_facecolor((43/255, 43/255, 43/255))
		a = fig.add_subplot(111)
		x = np.array([1,2,3,4,5,6])
		a.set_yticks([data[0],data[2],data[4]])
		a.set_xticks([])
		a.axvline(x=2.5)
		a.axvline(x=4.5)
		a.set_facecolor((43/255,43/255, 43/255))
		a.tick_params(color='white', labelcolor='white')
		for pos in ['top', 'bottom', 'left', 'right']:
			a.spines[pos].set_edgecolor('white')
		a.plot(x, data, color=(156/255, 61/255, 56/255))
		canvas = FigureCanvasTkAgg(fig, master=self.frame_right)
		canvas.flush_events()
		canvas.get_tk_widget().place(x=10, y=120)
		canvas.draw()
		self.label_thermocycler_denature = ctk.CTkLabel(master=self.frame_right, text_color='white', text='1st Denature', font=("Roboto Light",-12))
		self.label_thermocycler_denature.place(x=35, y=120, width=100)
		self.label_thermocycler_anneal = ctk.CTkLabel(master=self.frame_right, text_color='white', text='Anneal', font=("Roboto Light", -12))
		self.label_thermocycler_anneal.place(x=135, y=120, width=60)
		self.label_thermocycler_extension = ctk.CTkLabel(master=self.frame_right, text_color='white', text='2nd Denature', font=("Roboto Light", -12))
		self.label_thermocycler_extension.place(x=195, y=120, width=100)

	def on_click(self, event):
		x,y = event.x, event.y
		#print(f"{x}, {y}")
		if type(event.widget) == tkinter.ttk.Treeview:
			selected_row = self.treeview_build_protocol.selection()[0]
			#self.treeview_build_protocol.delete(selected_row)
		elif type(event.widget) == tkinter.Label:
			# Get label text.
			label_text = event.widget.cget('text')
			if label_text == 'thermocycler':
				# Check what the user is hovering over and toggle the component on click.
				if x >= 130 and x <= 238:
					if y >= 30 and y <= 124:
						if self.thermocyclers['clamps']['A']['homed']:
							self.fast_api_interface.reader.axis.move('reader', 8, -1 * int(self.clamp_A_max.get()), 80000, False, True)
							self.thermocyclers['clamps']['A']['homed'] = False
						else:
							self.fast_api_interface.reader.axis.home('reader', 8, False, True)
							self.thermocyclers['clamps']['A']['homed'] = True
					elif y >= 128 and y <= 222:
						if self.thermocyclers['clamps']['B']['homed']:
							self.fast_api_interface.reader.axis.move('reader', 9, -1 * int(self.clamp_B_max.get()), 80000, False, True)
							self.thermocyclers['clamps']['B']['homed'] = False
						else:
							self.fast_api_interface.reader.axis.home('reader', 9, False, True)
							self.thermocyclers['clamps']['B']['homed'] = True
					elif y >= 248 and y <= 345:
						if self.thermocyclers['clamps']['C']['homed']:
							self.fast_api_interface.reader.axis.move('reader', 10, -1 * int(self.clamp_C_max.get()), 80000, False, True)
							self.thermocyclers['clamps']['C']['homed'] = False
						else:
							self.fast_api_interface.reader.axis.home('reader', 10, False, True)
							self.thermocyclers['clamps']['C']['homed'] = True
					elif y >= 348 and y <= 446:
						if self.thermocyclers['clamps']['D']['homed']:
							self.fast_api_interface.reader.axis.move('reader', 11, -1 * int(self.clamp_D_max.get()), 80000, False, True)
							self.thermocyclers['clamps']['D']['homed'] = False
						else:
							self.fast_api_interface.reader.axis.home('reader', 11, False, True)
							self.thermocyclers['clamps']['D']['homed'] = True
				elif x >= 7	and x <= 118:
					if y >= 8 and y <= 234:
						if self.thermocyclers['clamps']['A']['homed'] and self.thermocyclers['clamps']['B']['homed']:
							if self.thermocyclers['trays']['AB']['homed']:
								self.fast_api_interface.reader.axis.move('reader', 6, -790000, 200000, False, True)
								self.thermocyclers['trays']['AB']['homed'] = False
							else:
								self.fast_api_interface.reader.axis.home('reader', 6, False, True)
								self.thermocyclers['trays']['AB']['homed'] = True
					elif y >= 238 and y <= 464:
						if self.thermocyclers['clamps']['C']['homed'] and self.thermocyclers['clamps']['D']['homed']:
							if self.thermocyclers['trays']['CD']['homed']:
								self.fast_api_interface.reader.axis.move('reader', 7, -790000, 200000, False, True)
								self.thermocyclers['trays']['CD']['homed'] = False
							else:
								self.fast_api_interface.reader.axis.home('reader', 7, False, True)
								self.thermocyclers['trays']['CD']['homed']  = True
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
				if x >= 305 and x <= 425:
					consumable_options.set('Reagent Cartridge')
					print(f'{x},{y}')
					if y >= 61 and y <= 146:
						tray_options.set('A')
					elif y >= 154 and y <= 240:
						tray_options.set('B')
					elif y >= 246 and y <= 331:
						tray_options.set('C')
					elif y >= 338 and y <= 423:
						tray_options.set('D')
					if x >= 305 and x <= 316:
						column_options.set('1')
					elif x >= 317 and x <= 324:
						column_options.set('2')
					elif x >= 325 and x <= 335:
						column_options.set('3')
					elif x >= 336 and x <= 345:
						column_options.set('4')
					elif x >= 346 and x <= 355:
						column_options.set('5')
					elif x >= 356 and x <= 365:
						column_options.set('6')
					elif x >= 366 and x <= 374:
						column_options.set('7')
					elif x >= 375 and x <= 384:
						column_options.set('8')
					elif x >= 385 and x <= 394:
						column_options.set('9')
					elif x >= 395 and x <= 403:
						column_options.set('10')
					elif x >= 404 and x <= 413:
						column_options.set('11')
					elif x >= 414 and x <= 425:
						column_options.set('12')
				# Sample Rack
				if x >= 266 and x <= 298:
					consumable_options.set('Sample Rack')
					column_options.set('')
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
					column_options.set('')
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
				if x >= 39 and x <= 158 and y >= 34 and y <= 119:
					consumable_options.set("Pre-Amp Thermocycler")
					tray_options.set('')
					if x >= 39 and x <= 50:
						column_options.set('1')
					elif x >= 51 and x <= 60:
						column_options.set('2')
					elif x >= 61 and x <= 69:
						column_options.set('3')
					elif x >= 70 and x <= 78:
						column_options.set('4')
					elif x >= 79 and x <= 89:
						column_options.set('5')
					elif x >= 90 and x <= 97:
						column_options.set('6')
					elif x >= 98 and x <= 107:
						column_options.set('7')
					elif x >= 108 and x <= 118:
						column_options.set('8')
					elif x >= 119 and x <= 127:
						column_options.set('9')
					elif x >= 128 and x <= 136:
						column_options.set('10')
					elif x >= 136 and x <= 146:
						column_options.set('11')
					elif x >= 147 and x <= 158:
						column_options.set('12')
				# Lid Tray
				# Tip Transfer Tray
				# Assay Strip
				if x >= 7 and x <= 98 and y >= 346 and y <= 424:
					consumable_options.set("Assay Strip")
					tray_options.set('')
					if x >= 7 and x <= 16:
						column_options.set('1')
					elif x >= 17 and x <= 25:
						column_options.set('2')
					elif x >= 31 and x <= 41:
						column_options.set('3')
					elif x >= 42 and x <= 50:
						column_options.set('4')
					elif x >= 56 and x <= 66:
						column_options.set('5')
					elif x >= 67 and x <= 74:
						column_options.set('6')
					elif x >= 80 and x <= 89:
						column_options.set('7')
					elif x >= 90 and x <= 99:
						column_options.set('8')
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
		thermocyclers = ['A', 'B', 'C', 'D']
		for thermocycler in thermocyclers:
			self.thermocyclers['times'][thermocycler]['denature'] = time_denature
			self.thermocyclers['times'][thermocycler]['anneal'] = time_anneal
			self.thermocyclers['times'][thermocycler]['extension'] = time_extension

	def callback_thermocycler_cycles(self, event):
		thermocycler = self.optionmenu_thermocycler.cget('variable').get()
		cycles = int(self.entry_thermocycler_cycles.get())
		thermocyclers = ['A', 'B', 'C', 'D']
		for thermocycler in thermocyclers:
			self.thermocyclers['cycles'][thermocycler] = cycles

	def callback_clamp_A_max(self, event):
		self.clamp_A_max.set(self.entry_settings_clamp_A.get())
	def callback_clamp_B_max(self, event):
		self.clamp_B_max.set(self.entry_settings_clamp_B.get())
	def callback_clamp_C_max(self, event):
		self.clamp_C_max.set(self.entry_settings_clamp_C.get())
	def callback_clamp_D_max(self, event):
		self.clamp_D_max.set(self.entry_settings_clamp_D.get())

	def callback_heater_shaker_rpm(self, event):
		self.heater_shaker_rpm.set(self.entry_settings_heater_shaker_rpm.get())

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
		self.server.stop()
		self.destroy()


	def backwards(self, event):
		if self.button_optimize.cget('border_width') != 0:
			dy = int(self.dy.get())
			thread = threading.Thread(target=self.upper_gantry.move_relative, args=('backwards', dy,))
			thread.start()


	def forwards(self, event):
		if self.button_optimize.cget('border_width') != 0:
			dy = int(self.dy.get())
			thread = threading.Thread(target=self.upper_gantry.move_relative, args=('forwards', dy,))
			thread.start()

	def left(self, event):
		if self.button_optimize.cget('border_width') != 0:
			dx = int(self.dx.get())
			thread = threading.Thread(target=self.upper_gantry.move_relative, args=('left', dx,))
			thread.start()

	def right(self, event):
		if self.button_optimize.cget('border_width') != 0:
			dx = int(self.dx.get())
			thread = threading.Thread(target=self.upper_gantry.move_relative, args=('right', dx,))
			thread.start()

	def up(self, event):
		if self.button_optimize.cget('border_width') != 0:
			dz = int(self.dz.get())
			thread = threading.Thread(target=self.upper_gantry.move_relative, args=('up', dz,))
			thread.start()

	def down(self, event):
		if self.button_optimize.cget('border_width') != 0:
			dz = int(self.dz.get())
			thread = threading.Thread(target=self.upper_gantry.move_relative, args=('down', dz,))
			thread.start()

	def copy(self, event):
		self.clipboard = []
		for row in self.treeview_build_protocol.selection():
			self.clipboard.append(self.treeview_build_protocol.item(row)['values'][0])
		self.clipboard.reverse()

	def paste(self, event):
		try:
			selected_row = self.treeview_build_protocol.selection()[0]
			for action_msg in self.clipboard:
				self.treeview_build_protocol.insert('', int(selected_row.replace('row', ''))+1, iid='row{0}'.format(self.build_protocol_treeview_row_index), values=(action_msg,))
				self.build_protocol_treeview_row_index = self.build_protocol_treeview_row_index + 1
		except:
			for action_msg in self.clipboard:
				self.treeview_build_protocol.insert('', 'end', iid='row{0}'.format(self.build_protocol_treeview_row_index), values=(action_msg,))
				self.build_protocol_treeview_row_index = self.build_protocol_treeview_row_index + 1
		self.__update_build_protocol_action_list()

	def load_status_xlsx(self):
		import math
		#status_url = r'https://biorad-my.sharepoint.com/:x:/r/personal/u112958_global_bio-rad_com/_layouts/15/Doc.aspx?sourcedoc=%7B0F23CBA7-8FD0-4246-B5F1-F3D53E68AAED%7D&file=unit_component_statuses.xlsx&action=default&mobileredirect=true'
		#ctx_auth = AuthenticationContext(status_url)
		#ctx_auth.acquire_token_for_user('u112958@bio-rad.com', 'G7aa-2x4-8')
		#ctx = ClientContext(status_url, ctx_auth)
		#response = File.open_binary(ctx, "")
		unit = f"Unit {self.settings_unit_sv.get()}"
		df = pd.read_excel('unit_component_statuses.xlsx', sheet_name=unit)
		for index, row in df.iterrows():
			cmpt = row['Component']
			pm = row["Parent Module"]
			s = row['Status']
			p = row['Priority']
			try:
				if math.isnan(p):
					p = ''
			except:
				pass
			n = row['Note']
			try:
				if math.isnan(n):
					n = ''
			except:
				pass
			fbd = row["Fix By Date"]
			c = row['Contact']
			try:
				if math.isnan(c):
					c = ''
			except:
				pass
			self.treeview_status.insert('', 'end', 'row{0}'.format(self.status_treeview_row_index), values=(cmpt, pm, s, p, n, fbd, c,))
			self.status_treeview_row_index = self.status_treeview_row_index + 1
	
	def callback_settings_unit_sv_changed(self, *args):
		#import os
		unit = self.settings_unit_sv.get()
		# Copy the unit coordinate file to coordinate.py
		#coordinate_file_name = 'coordinate.py'
		# Remove old backup.
		#os.system("del coordinate_backup.py")
		# Make a backup of this file if it exists.
		#os.system(f"copy {coordinate_file_name} coordinate_backup.py")
		# Remove it if it exists.
		#os.system(f"del {coordinate_file_name}")
		# Copy the correct coordinate file for the unit.
		#os.system(f"copy coordinate_{unit}.py {coordinate_file_name}")


if __name__ == '__main__':
	app = App()
	unit = 'D'
	app.settings_unit_sv.set(unit)
	# Copy the unit coordinate file to coordinate.py
	coordinate_file_name = 'coordinate.py'
	# Remove old backup.
	os.system("del coordinate_backup.py")
	# Make a backup of this file if it exists.
	os.system(f"copy {coordinate_file_name} coordinate_backup.py")
	# Remove it if it exists.
	os.system(f"del {coordinate_file_name}")
	# Copy the correct coordinate file for the unit.
	os.system(f"copy coordinate_{unit}.py {coordinate_file_name}")
	app.iconbitmap('bio-rad-logo.ico')
	app.bind('<Return>', app.enter)
	app.bind('<Up>', app.backwards)
	app.bind('<Left>', app.left)
	app.bind('<Down>', app.forwards)
	app.bind('<Right>', app.right)
	app.bind('<Shift Up>', app.up)
	app.bind('<Shift Down>', app.down)
	app.maxsize(780,520)
	app.minsize(780,520)
	app.mainloop()