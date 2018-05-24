import matplotlib
matplotlib.use('TkAgg');

import cv2
import os
import matplotlib.pyplot as plt
from matplotlib import gridspec
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
from PIL import ImageTk
from PIL import Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from testbed import TestBed


TestBed.init("tyger.jpg");
image = TestBed.image;

if(__name__=="__main__"):
	TestBed.root = tk.Tk();
	TestBed.root.minsize(TestBed.ROOT_WIDTH,TestBed.ROOT_HEIGHT);
	
	
	TestBed.scale_var = tk.DoubleVar();
	
	scale = ttk.Scale(TestBed.root,
							variable=TestBed.scale_var,
							from_=100,
							to_=1,
							orient=tk.HORIZONTAL,
							command=TestBed.onSliderChanged,
							length=TestBed.SLIDER_WIDTH,
							value = 100
							);
	
	
	image_tk = TestBed.imageToTkinter(image);
	
	figure = plt.Figure(figsize=(TestBed.FRAME_WIDTH/100,TestBed.ROOT_HEIGHT/100),
							  dpi=100,
							  facecolor="#F0F0F0");
	
	TestBed.graph_figure = figure.add_subplot(222);
	TestBed.initial_fft_figure = figure.add_subplot(223);
	TestBed.matrix_figure = figure.add_subplot(221);
	TestBed.fft_figure = figure.add_subplot(224);
	
	TestBed.canvas = FigureCanvasTkAgg(figure,
										master=TestBed.root
										);
	TestBed.canvas.show();
	
	TestBed.initGraphs();
	
	
	TestBed.image_label = tk.Label(TestBed.root,
											 image=image_tk,
											 width = TestBed.FRAME_WIDTH,
											 height = TestBed.FRAME_HEIGHT);
	
	TestBed.dfft_button = ttk.Button(text="Calcular DFFT",
											  command = TestBed.onClick,
											  width = 0.4*TestBed.FRAME_WIDTH);
	
	TestBed.image_button = ttk.Button(text="Escoger imagen",
												command=TestBed.onChangeImage,
												width=0.4*TestBed.FRAME_WIDTH);
	
	TestBed.image_label.place(relx=0,rely=0.1);
	TestBed.canvas.get_tk_widget().place(relx=0.5,rely=0);
	scale.place(rely=0.075, relx=0.05);
	TestBed.dfft_button.place(rely=0.85, relx=0.225);
	TestBed.image_button.place(rely=0.15, relx=0.225);
	
	
	
	
	
	
	TestBed.root.mainloop();


	