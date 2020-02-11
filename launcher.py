import tkinter as tk
from tkinter import filedialog
from tkinter import *
import tkinter.scrolledtext as scrolledtext
import gdle_to_ace
import pcap_to_gdle
import os

class Launcher():

	def __init__(self, root):
		self.root = root
		self.make_start_screen(root)
		
		self.pcap_converter = pcap_to_gdle.PcapConverter()
		
	def make_start_screen(self, root):
	
		self.page_one = Frame(root, width=800, height=800)
		self.page_one.grid(row=0, column=0, padx=20, pady=20)
		
		# convert landblock
		
		label1 = Label(self.page_one, text="1 - Print list of unique WCIDs", font="Arial 12")
		label1.grid(row=1, column=0, padx=5, pady=5)
		
		open_pcap_folder = Button(self.page_one, text="Open PCAP and Run", command = self.examine_landblock_pcap)
		open_pcap_folder.grid(row=1, column=1, padx=5, pady=5)
		
		label2 = Label(self.page_one, text="Seen more than")
		label2.grid(row=2, column=0, padx=5, pady=5)
		
		self.threshold_scale = Scale(self.page_one, from_=0, to=10, orient=HORIZONTAL)
		self.threshold_scale.set(1)
		self.threshold_scale.grid(row=2, column=1, padx=5, pady=5)
		
		label3 = Label(self.page_one, text="2 - Convert (PCAP to GDLE)", font="Arial 12")
		label3.grid(row=3, column=0, padx=5, pady=5)
		
		open_pcap_folder = Button(self.page_one, text="Open PCAP and Run", command = self.load_landblock_pcap)
		open_pcap_folder.grid(row=3, column=1, padx=5, pady=5)
		
		# monster wcid entry
		label4 = Label(self.page_one, text="Monster WCIDs (comma separated)")
		label4.grid(row=4, column=0, padx=5, pady=5)
		
		self.monster_entry = Entry(self.page_one, bg="white")
		self.monster_entry.grid(row=4, column=1, padx=5, pady=5, ipadx=50)
		
		# item wcid entry
		label5 = Label(self.page_one, text="Item WCIDs (comma separated)")
		label5.grid(row=5, column=0, padx=5, pady=5)
		
		self.item_entry = Entry(self.page_one, bg="white")
		self.item_entry.grid(row=5, column=1, padx=5, pady=5, ipadx=50)
		
		# ignore wcid entry
		label6 = Label(self.page_one, text="Ignore WCIDs (comma separated)")
		label6.grid(row=6, column=0, padx=5, pady=5)
		
		self.ignore_entry = Entry(self.page_one, bg="white")
		self.ignore_entry.grid(row=6, column=1, padx=5, pady=5, ipadx=50)
		
		# generator wcid entries
		label7 = Label(self.page_one, text="Monster generator WCID")
		label7.grid(row=7, column=0, padx=5, pady=5)
		
		self.mgen_entry = Entry(self.page_one, bg="white")
		self.mgen_entry.insert(END, "7924")
		self.mgen_entry.grid(row=7, column=1, padx=5, pady=5, ipadx=50)
		
		label8 = Label(self.page_one, text="Monster generator /myloc paste")
		label8.grid(row=8, column=0, padx=5, pady=5)
		
		self.mgen_loc_entry = Entry(self.page_one, bg="white")
		self.mgen_loc_entry.grid(row=8, column=1, padx=5, pady=5, ipadx=50)
		
		label9 = Label(self.page_one, text="Item generator WCID")
		label9.grid(row=9, column=0, padx=5, pady=5)
		
		self.igen_entry = Entry(self.page_one, bg="white")
		self.igen_entry.insert(END, "5085")
		self.igen_entry.grid(row=9, column=1, padx=5, pady=5, ipadx=50)
	
		label10 = Label(self.page_one, text="Item generator /myloc paste")
		label10.grid(row=10, column=0, padx=5, pady=5)
		
		self.igen_loc_entry = Entry(self.page_one, bg="white")
		self.igen_loc_entry.grid(row=10, column=1, padx=5, pady=5, ipadx=50)
		
		# landblock description
		label11 = Label(self.page_one, text="Landblock description")
		label11.grid(row=11, column=0, padx=5, pady=5)
		
		self.desc_entry = Entry(self.page_one, bg="white")
		self.desc_entry.insert(END, "A name goes here")
		self.desc_entry.grid(row=11, column=1, padx=5, pady=5, ipadx=50)
		
		# nickname
		label12 = Label(self.page_one, text="Nickname")
		label12.grid(row=12, column=0, padx=5, pady=5)
		
		self.nickname_entry = Entry(self.page_one, bg="white")
		self.nickname_entry.insert(END, "Asheron")
		self.nickname_entry.grid(row=12, column=1, padx=5, pady=5, ipadx=50)
		
		# convert spawn map
		label13 = Label(self.page_one, text="3 - Convert spawn map (GDLE to ACE)", font="Arial 12")
		label13.grid(row=13, column=0, padx=5, pady=5)
		
		open_landblock_folder = Button(self.page_one, text="Open Folder and Run", command = self.load_gdle_map)
		open_landblock_folder.grid(row=13, column=1, padx=5, pady=5)
		
		self.text = scrolledtext.ScrolledText(self.page_one, height=15, width=50, undo=True)
		self.text.configure(state='disabled')
		self.text.grid(row=14, column=0, padx=5, pady=5, columnspan=2)
		
	def examine_landblock_pcap(self):
		
		input_file =  filedialog.askopenfilename(filetypes=[("json files", "*.json")])
		
		if input_file:
			
			self.text.configure(state='normal')
			self.text.delete('1.0', END)
			
			self.text.insert('1.0', "Opening " + os.path.split(input_file)[1] + "...\n")
			filtered_list = self.pcap_converter.load_pcap(input_file, self.threshold_scale.get())
			
			uniques = {}
			
			for entry in filtered_list:
				uniques[entry.wcid] = entry.name
			
			for k, v in sorted(uniques.items()):
				self.text.insert(END, str(k) + ' ' + str(v) + '\n')
				
			self.text.configure(state='disabled')
	
	def load_landblock_pcap(self):
		
		input_file =  filedialog.askopenfilename(filetypes=[("json files", "*.json")])
		
		if input_file:
			
			print("Opening " + os.path.split(input_file)[1] + "...")
			filtered_list = self.pcap_converter.load_pcap(input_file, self.threshold_scale.get())
			
			ignore_wcids = []
			
			if len(self.ignore_entry.get()) > 0:
				entries = self.ignore_entry.get().replace(" ", "").split(',')
				ignore_wcids = self.get_wcid_set(entries)
				
			filtered_list = self.pcap_converter.clean_list(filtered_list, ignore_wcids)
			
			monster_wcids = []
			
			if len(self.monster_entry.get()) > 0:
				entries = self.monster_entry.get().replace(" ", "").split(',')
				monster_wcids = self.get_wcid_set(entries)		
			
			item_wcids = []
			
			if len(self.item_entry.get()) > 0:
				entries = self.item_entry.get().replace(" ", "").split(',')
				item_wcids = self.get_wcid_set(entries)
			
			mgen_wcid = self.mgen_entry.get().strip()
			igen_wcid = self.igen_entry.get().strip()
			
			mgen_loc = self.mgen_loc_entry.get().strip()
			igen_loc = self.igen_loc_entry.get().strip()
			
			monster_links = self.pcap_converter.get_links(filtered_list, mgen_wcid, "Monster Generator", monster_wcids, mgen_loc)
			item_links = self.pcap_converter.get_links(filtered_list, igen_wcid, "Item Generator", item_wcids, igen_loc)  
			
			landblock_desc = "A landblock"
			if len(self.desc_entry.get()) > 0:
				landblock_desc = self.desc_entry.get()
			
			nickname = "Asheron"
			if len(self.nickname_entry.get()) > 0:
				nickname = self.nickname_entry.get()
				
			self.pcap_converter.output_map(nickname, landblock_desc, filtered_list, monster_links, item_links)
			
			print("Done.")
	
	def get_wcid_set(self, entries):
		
		wcid_list = []
		
		for entry in entries:
			wcid_list.append(int(entry))
		
		return set(wcid_list)
	
	def load_gdle_map(self):
		"""Convert a batch of GDLE spawn maps to ACE format."""
		
		file_folder = filedialog.askdirectory()
		file_list = []
		
		for r, d, f in os.walk(file_folder):
			for file in f:
				if '.json' in file:
					file_list.append(file)
			
		for file_name in file_list:
			print("Working on " + file_name + "...")
			gdle_to_ace.convert_spawn_map(file_folder, file_name)
			print("Done.")
	
root = tk.Tk()
root.title("AC Spawn Maps")

launcher = Launcher(root)
root.mainloop()
