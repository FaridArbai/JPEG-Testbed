import cv2
import os
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
from PIL import ImageTk
from PIL import Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog

class TestBed:
	FILE_TYPES = (("", ".jpg"), ("", ".jpeg"), ("", ".bmp"), ("", ".png"));
	image_label = [];
	fft_label = [];
	root = [];
	image = [];
	orig = [];
	scale_var = 0;
	dfft_button = [];
	image_button = [];
	
	#TODO: Adjust height and width so that it scales
	#to the available window size
	
	ROOT_HEIGHT = int(1080*0.9);
	ROOT_WIDTH = int(1920*0.9);
	
	FRAME_HEIGHT = int(0.8*(ROOT_HEIGHT));
	FRAME_WIDTH = int(0.5*ROOT_WIDTH);
	FRAME_RATIO = FRAME_WIDTH/FRAME_HEIGHT;
	
	SLIDER_WIDTH = FRAME_WIDTH*0.8;
	
	graph_figure = [];
	initial_fft_figure = [];
	matrix_figure = [];
	fft_figure = [];
	canvas = [];
	
	image_size = 0;
	
	Q50 = np.array([[16, 11, 10, 16, 24, 40, 51, 61],
											  [12, 12, 14, 19, 26, 58, 60, 55],
											  [14, 13, 16, 24, 40, 57, 69, 56],
											  [14, 17, 22, 29, 51, 87, 80, 62],
											  [18, 22, 37, 56, 68, 109, 103, 77],
											  [24, 35, 55, 64, 81, 104, 113, 92],
											  [49, 64, 78, 87, 103, 121, 120, 101],
											  [72, 92, 95, 98, 112, 100, 103, 99]])
	
	@staticmethod
	def init(image_path):
		image = cv2.imread(image_path);
		TestBed.image_size = os.path.getsize(image_path);
		b, g, r = cv2.split(image);
		image = cv2.merge((r, g, b));
		
		height, width, channels = image.shape;
		
		image_ratio = width/height;
		
		if(image_ratio > TestBed.FRAME_RATIO):
			image_width = TestBed.FRAME_WIDTH;
			image_height = TestBed.FRAME_HEIGHT/image_ratio;
		else:
			image_height = TestBed.FRAME_HEIGHT;
			image_width = TestBed.FRAME_WIDTH*image_ratio;
		
		image_width = int(image_width);
		image_height = int(image_height);
		
		TestBed.image = cv2.resize(image,(image_width,image_height));
		
		
	@staticmethod
	def plotQuantizationMatrix(q):
		if(q<0.15):
			q=0.15
		
		if(q<50):
			s = 5000/q;
		else:
			s = 200-2*q;
		
		Q = np.floor((s*TestBed.Q50+50)/100);
		Q[Q==0] = 1;
		
		
		TestBed.matrix_figure.clear();
		for i in range(8):
			for j in range(8):
				c = int(Q[i][j]);
				TestBed.matrix_figure.text((i),(j),str(c),va='center',ha="center");
		
		TestBed.matrix_figure.matshow(Q,cmap=plt.cm.Blues);
		
		var_rang = np.arange(-0.5, 8.5);
		TestBed.matrix_figure.set_xlim(-0.5,7.5);
		TestBed.matrix_figure.set_ylim(7.5, -0.5);
		TestBed.matrix_figure.set_xticks(var_rang);
		TestBed.matrix_figure.set_yticks(var_rang[::-1]);
		TestBed.matrix_figure.axis("off");
		
		TestBed.matrix_figure.grid(linewidth=0.5);
		str_title = "Matriz de cuantizacion para Q=%.2f"%(q);
		TestBed.matrix_figure.set_title(str_title);
		
	@staticmethod
	def initGraphs():
		vq = np.arange(0,100,0.5);
		v_size = np.zeros(len(vq));
		i = 0;
		
		for q in vq:
			ENCODE_PARAM = [int(cv2.IMWRITE_JPEG_QUALITY), q];
			cv2.imwrite('tmp.jpg', TestBed.image, ENCODE_PARAM);
			v_size[i] = TestBed.image_size/os.path.getsize("tmp.jpg");
			i+=1;
		
		TestBed.graph_figure.plot(vq,v_size,
										  "#168a9c");
		TestBed.graph_figure.grid(linewidth=0.5);
		TestBed.graph_figure.set_title("Factores de compresión");
		
		magnitude = TestBed.computeMagnitude(TestBed.image);
		
		TestBed.initial_fft_figure.imshow(magnitude);
		TestBed.initial_fft_figure.set_title("DFFT con Q=100.00");
		
		TestBed.fft_figure.imshow(magnitude);
		TestBed.fft_figure.set_title("DFFT con Q=100.00");
		
		TestBed.plotQuantizationMatrix(100);
		
		TestBed.canvas.show();
		
		return 0;
		
		
	@staticmethod
	def onSliderChanged(q):
		q = 100-(float(q));
		
		decoded_image = TestBed.getDecodedImage(q);
		
		img_tk = TestBed.imageToTkinter(decoded_image)
		
		TestBed.image_label.configure(image=img_tk);
		TestBed.image_label.image = img_tk;
		
		TestBed.plotQuantizationMatrix(q);
		
		TestBed.canvas.show();
		
	@staticmethod
	def getDecodedImage(q):
		ENCODE_PARAM = [int(cv2.IMWRITE_JPEG_QUALITY), q];
		result, encoded_image = cv2.imencode(".jpg", TestBed.image, ENCODE_PARAM);
		decoded_image = cv2.imdecode(encoded_image, 1);
		
		return decoded_image
		
		
	
	@staticmethod
	def computeMagnitude(image):
		H = np.fft.fft2(cv2.cvtColor(image, cv2.COLOR_RGB2GRAY),(2048,2048));
		fshift = np.fft.fftshift(H);
		magnitude = 20*np.log10(np.abs(fshift));
		
		return magnitude;
	
	@staticmethod
	def imageToTkinter(image):
		im = Image.fromarray(image);
		image_tk = ImageTk.PhotoImage(image=im);
		
		return image_tk;
	
	@staticmethod
	def onSizeChanged(event):
		TestBed.setSize(event.width/2, event.height);
		resized_ = cv2.resize(TestBed.image,(TestBed.width,TestBed.height));
		TestBed.image_label.config(image=TestBed.imageToTkinter(resized_));
		TestBed.image_label.image = resized_;
		
	
	@staticmethod
	def setSize(width, height):
		print("orig: (%d,%d)", width, height);
		new_ratio = width/height;
		if (TestBed.ratio > new_ratio):
			TestBed.width = int(width);
			TestBed.height = int(height/TestBed.ratio);
		else:
			TestBed.height = int(height);
			TestBed.width = int(width*TestBed.ratio);
		
		print("sizes: (%d,%d)", TestBed.width, TestBed.height);
		
	
	@staticmethod
	def onClick():
		q = 100 - TestBed.scale_var.get();
		decodificada = TestBed.getDecodedImage(q);
		magnitud = TestBed.computeMagnitude(decodificada);
		TestBed.fft_figure.clear();
		TestBed.fft_figure.imshow(magnitud);
		TestBed.fft_figure.set_title("DFFT para Q=%.2f"%(q));
		TestBed.canvas.show();
		
	
	@staticmethod
	def onChangeImage():
		print("Clicked");
		
		image_path = filedialog.askopenfilename();
		
		TestBed.init(image_path);
		
		image = TestBed.image;
		
		img_tk = TestBed.imageToTkinter(image);
		
		TestBed.image_label.configure(image=img_tk);
		TestBed.image_label.image = img_tk;
		
		TestBed.graph_figure.clear();
		TestBed.initGraphs();
		
		q = TestBed.scale_var.get();
		
		TestBed.plotQuantizationMatrix(q);
		TestBed.onSliderChanged(q);
	
	
	#TODO: Complete this function so that it
	#scales automatically
	@staticmethod
	def onSizeChanged(event):
		new_width = event.width;
		new_height = event.height;
		
		# Resize image and graphs
		# Resize current window
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
		
