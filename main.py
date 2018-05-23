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

img = cv2.imread("farid.jpg");
img_height, img_width, img_channels = img.shape;
img = cv2.resize(img, (int(img_width/2),int(img_height/2)));

class TestBed:
	FILE_TYPES = (("",".jpg"),("",".jpeg"),("",".bmp"),("",".png"));
	image_label = [];
	fft_label = [];
	root = [];
	
	@staticmethod
	def compressionGraph():
		orig_size = os.path.getsize("farid.jpg")
		
		sizes = np.zeros(100);
		k = 0;
		
		for quality in range(0,100):
			ENCODE_PARAM = [int(cv2.IMWRITE_JPEG_QUALITY),quality];
			
			cv2.imwrite("code.jpg",img, ENCODE_PARAM);
			
			sizes[k] = orig_size/os.path.getsize("code.jpg");
			k += 1;
		
		plt.figure(1);
		plt.plot(sizes);
		plt.show();
	
	@staticmethod
	def frequency():
		ENCODE_PARAM = [int(cv2.IMWRITE_JPEG_QUALITY), 0];
		
		result, encoded_image = cv2.imencode(".jpg",img,ENCODE_PARAM);
		
		decoded_image = cv2.imdecode(encoded_image, 0);
		
		H2 = np.fft.fft2(cv2.cvtColor(img,cv2.COLOR_RGB2GRAY));
		fshift2 = np.fft.fftshift(H2);
		magnitude_spectrum2 = 20*np.log10(np.abs(fshift2));
		
		H = np.fft.fft2(decoded_image);
		fshift = np.fft.fftshift(H);
		magnitude_spectrum = 20*np.log10(np.abs(fshift));
		
		plt.figure(1);
		plt.subplot(121)
		plt.imshow(magnitude_spectrum2, cmap="gray");
		plt.title("Original");
		plt.subplot(122)
		plt.imshow(magnitude_spectrum, cmap="gray");
		plt.title("Decodificada");
	
	@staticmethod
	def onSliderChanged(q):
		ENCODE_PARAM = [int(cv2.IMWRITE_JPEG_QUALITY), int(float(q))];
		
		result, encoded_image = cv2.imencode(".jpg", img, ENCODE_PARAM);
		decoded_image = cv2.imdecode(encoded_image, 1);
		
		img_tk = TestBed.imageToTkinter(decoded_image)
		
		TestBed.image_label.configure(image=img_tk);
		TestBed.image_label.image = img_tk;
		
		magnitude_tk = TestBed.imageToTkinter(TestBed.computeMagnitude(decoded_image));
		
		TestBed.fft_label.configure(image=magnitude_tk);
		TestBed.fft_label.image = magnitude_tk;
		
		
		
	@staticmethod
	def computeMagnitude(image):
		H = np.fft.fft2(cv2.cvtColor(image,cv2.COLOR_RGB2GRAY),(512,512));
		fshift = np.fft.fftshift(H);
		magnitude = 20*np.log10(np.abs(fshift));
		
		return magnitude;
	
	@staticmethod
	def imageToTkinter(image):
		n_dims = len(image.shape);
		
		if(n_dims==3):
			b, g, r = cv2.split(image);
			img_rgb = cv2.merge((r, g, b));
			im = Image.fromarray(img_rgb);
		else:
			im = Image.fromarray(image);
		
		image_tk = ImageTk.PhotoImage(image=im);
		
		return image_tk;
		
	

if(__name__=="__main__"):
	TestBed.root = tk.Tk();
	
	scale_var = tk.DoubleVar();
	
	scale = ttk.Scale(TestBed.root,
							variable=scale_var,
							from_=0,
							to_=100,
							orient=tk.HORIZONTAL,
							command=TestBed.onSliderChanged,
							length=500,
							value = 100
							);
	
	
	image_tk = TestBed.imageToTkinter(img);
	
	
	TestBed.image_label = tk.Label(TestBed.root,
									image=image_tk
								  );
	
	magnitude = TestBed.computeMagnitude(img);
	
	magnitude_tk = TestBed.imageToTkinter(magnitude);
	
	TestBed.fft_label = tk.Label(TestBed.root,
										  image = magnitude_tk);
	
	scale.grid(row=0,column=1);
	TestBed.image_label.grid(row=1,column=0);
	
	#TestBed.fft_label.grid(row=1,column=1);
	
	f = plt.Figure(figsize=(5,5), dpi=100);
	axes = f.add_subplot(111);
	axes.imshow(magnitude);
	
	canvas = FigureCanvasTkAgg(f,TestBed.root);
	
	canvas.show();
	
	
	
	canvas.get_tk_widget().grid(row=1,column=1);
	
	
	
	
	
	
	
	
	
	
	
	TestBed.root.mainloop();
	
	