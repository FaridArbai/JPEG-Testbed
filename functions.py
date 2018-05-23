import numpy as np
import matplotlib.pyplot as plt
from scipy import signal


class Functions:
	PLOT_COLOR = 'k';
	PLOT_LINEWIDTH = 0.75;
	PLOT_FACECOLOR = '#F0F0F0';
	GRID_STYLE = '--';
	GRID_LINEWIDTH = 0.5;
	
	@staticmethod
	def energia(x):
		return sum(x**2);
	
	@staticmethod
	def float2int16(x):
		return np.int16(x/np.max(np.abs(x))*(2**15-1));
	
	@staticmethod
	def respuesta(b, a, N_fft):
		delta = np.concatenate(([1], np.zeros(N_fft-1)), axis=0);
		denom = np.concatenate(([1], a), axis=0);
		ht = signal.lfilter(b, denom, delta);
		Hf = np.fft.fft(ht, 2*N_fft);
		Hf = Hf[0:N_fft];
		
		ffn = np.arange(0, 1, 1/N_fft);
		
		return ffn, Hf;
	
	@staticmethod
	def magnitud(Hf):
		Hf_abslog = 20*np.log10(np.abs(Hf));
		
		return Hf_abslog;
	
	@staticmethod
	def fase(Hf):
		phi = np.unwrap(np.angle(Hf));
		
		return phi;
	
	@staticmethod
	def plot(xx, yy, title="", plot_color=PLOT_COLOR, plot_linewidth=PLOT_LINEWIDTH, plot_label=""):
		plt.plot(xx, yy, plot_color, linewidth=plot_linewidth, label=plot_label);
		plt.title(title);
		plt.grid(linestyle=Functions.GRID_STYLE, linewidth=Functions.GRID_LINEWIDTH);
	
	@staticmethod
	def figure(n):
		plt.figure(n).patch.set_facecolor(Functions.PLOT_FACECOLOR);
	
	

