import tkinter as tk
from ctypes import windll
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import showerror
import tkinter.scrolledtext as scrolledtext
import gdle_to_ace
import pcap_to_gdle
import os


# output console
class Console:

    def __init__(self, parent, cont):
        self.frame = tk.Frame(parent)

        self.text_area = tk.scrolledtext.ScrolledText(self.frame, height=5, width=50, undo=True)
        self.text_area.configure(state='disabled')

        self.text_area.grid(row=0, column=0, padx=5, pady=5)


# panel where you select monsters and items
class SelectionPanel:

    def __init__(self, parent, cont):
        self.frame = tk.Frame(parent)

        norm_font = ("Arial", 12)

        # monster generator wcid combo boxe
        mgen_combo_label = tk.Label(self.frame, text="Monster generator WCID")
        self.mgen_combo = ttk.Combobox(self.frame, values=["7924"], font=norm_font)
        self.mgen_combo.current(0)

        # monster generator loc entry
        mgen_loc_label = tk.Label(self.frame, text="Monster generator /myloc paste")
        self.mgen_loc_entry = tk.Entry(self.frame, bg="white", font=norm_font)

        # item generator wcid combo box
        igen_entry_label = tk.Label(self.frame, text="Item generator WCID")
        self.igen_combo = ttk.Combobox(self.frame, values=["5085"], font=norm_font)
        self.igen_combo.current(0)

        # set the font of the dropdown list of the combo boxes
        self.frame.option_add('*TCombobox*Listbox.font', norm_font)

        # item generator loc entry
        igen_loc_label = tk.Label(self.frame, text="Item generator /myloc paste")
        self.igen_loc_entry = tk.Entry(self.frame, bg="white", font=norm_font)

        # monster selection listbox
        mob_listbox_label = tk.Label(self.frame, text="Select Monsters", font=norm_font)
        my_tuple = self.make_listbox(self.frame, norm_font, "extended")
        mob_frame = my_tuple[0]
        self.mob_listbox = my_tuple[1]

        # item selection listbox
        item_listbox_label = tk.Label(self.frame, text="Select Items", font=norm_font)
        my_tuple = self.make_listbox(self.frame, norm_font, "extended")
        item_frame = my_tuple[0]
        self.item_listbox = my_tuple[1]

        # ignore listbox
        ignore_listbox_label = tk.Label(self.frame, text="Select Ignore", font=norm_font)
        my_tuple = self.make_listbox(self.frame, norm_font, "extended")
        ignore_frame = my_tuple[0]
        self.ignore_listbox = my_tuple[1]

        # layout
        mgen_combo_label.grid(row=0, column=0, padx=5, pady=5)
        self.mgen_combo.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        mgen_loc_label.grid(row=2, column=0, padx=5, pady=5)
        self.mgen_loc_entry.grid(row=3, column=0, padx=5, pady=5, sticky="ew")
        mob_listbox_label.grid(row=4, column=0, padx=5, pady=5)
        mob_frame.grid(row=5, column=0, padx=5, pady=5)

        igen_entry_label.grid(row=0, column=1, padx=5, pady=5)
        self.igen_combo.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        igen_loc_label.grid(row=2, column=1, padx=5, pady=5)
        self.igen_loc_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        item_listbox_label.grid(row=4, column=1, padx=5, pady=5)
        item_frame.grid(row=5, column=1, padx=5, pady=5)

        ignore_listbox_label.grid(row=4, column=2, padx=5, pady=5)
        ignore_frame.grid(row=5, column=2, padx=5, pady=5)

    def make_listbox(self, parent, my_font, selection_mode):
        """Returns a frame and a listbox with a vertical scrollbar."""
        frame = tk.Frame(parent)

        listbox = tk.Listbox(frame, selectmode=selection_mode, font=my_font, exportselection=0)
        listbox['width'] = 30
        listbox.pack(side="left", fill="y")

        scrollbar = tk.Scrollbar(frame, orient="vertical")
        scrollbar.config(command=listbox.yview)
        scrollbar.pack(side="right", fill="y")
        listbox.config(yscrollcommand=scrollbar.set)

        return frame, listbox

    def get_list_boxes(self):
        return [self.mob_listbox, self.item_listbox, self.ignore_listbox]

    def get_selected(self, listbox):
        wcids = []

        selection = listbox.curselection()
        for i in selection:
            entry = listbox.get(i)
            split = entry.split(",")
            wcid = int(split[0])
            wcids.append(wcid)

        return wcids


# form where you fill out basic information
class TopPanel:

    def __init__(self, parent, cont):
        self.frame = tk.Frame(parent)

        # landblock description
        label1 = tk.Label(self.frame, text="Landblock Description")
        self.desc_entry = tk.Entry(self.frame, bg="white")

        # nickname
        label2 = tk.Label(self.frame, text="Nickname")

        self.nickname_entry = tk.Entry(self.frame, bg="white")
        self.nickname_entry.insert(tk.END, "Asheron")

        # layout
        label1.grid(row=0, column=0, padx=5, pady=5)
        self.desc_entry.grid(row=0, column=1, padx=5, pady=5)
        label2.grid(row=1, column=0, padx=5, pady=5)
        self.nickname_entry.grid(row=1, column=1, padx=5, pady=5)


class View:

    def __init__(self, parent, cont):
        self.frame = tk.Frame(parent)
        self.cont = cont

        self.top_panel = TopPanel(self.frame, cont)
        self.toolbar = Toolbar(self.frame, cont)
        self.console = Console(self.frame, cont)
        self.selection_panel = SelectionPanel(self.frame, cont)
        self.bottom_panel = BottomPanel(self.frame, cont)

        # layout
        self.top_panel.frame.grid(row=0, column=0, padx=5, pady=5)
        self.toolbar.frame.grid(row=1, column=0, padx=5, pady=5)
        self.console.frame.grid(row=2, column=0, padx=5, pady=5)
        self.selection_panel.frame.grid(row=3, column=0, padx=5, pady=5)
        self.bottom_panel.frame.grid(row=4, column=0, padx=5, pady=5)

        self.frame.grid()


class Controller:

    def __init__(self, parent):

        self.view = View(parent, self)
        self.pcap_converter = pcap_to_gdle.PcapConverter()
        self.input_file = None
        self.filtered_list = []

    def open_landblock_pcap(self):

        self.input_file = filedialog.askopenfilename(filetypes=[("json files", "*.json")])

        if self.input_file:

            # output what it's opening to console
            self.view.console.text_area.configure(state='normal')
            self.view.console.text_area.delete('1.0', tk.END)
            self.view.console.text_area.insert('1.0', "Opening " + os.path.split(self.input_file)[1] + "...\n")
            self.view.console.text_area.configure(state='disabled')

            # get a list of wcids in the pcap
            self.filtered_list = self.pcap_converter.load_pcap(self.input_file, self.view.toolbar.threshold_scale.get())

            uniques = {}

            # only keep unique wcids for clarity, this is used for view only
            for entry in self.filtered_list:
                uniques[entry.wcid] = entry.name

            listbox_list = self.view.selection_panel.get_list_boxes()

            for k, v in sorted(uniques.items()):  # sort and output
                i = 0

                for listbox in listbox_list:
                    listbox.insert(i, str(k) + ',' + str(v))
                    i += 1

            self.view.toolbar.make_map_button["state"] = "normal"

    def make_gdle_spawn_map(self):
        """Make a gdle spawn map from a pcap landblock file."""

        if self.input_file:

            monster_wcids = self.view.selection_panel.get_selected(self.view.selection_panel.mob_listbox)
            item_wcids = self.view.selection_panel.get_selected(self.view.selection_panel.item_listbox)
            ignore_wcids = self.view.selection_panel.get_selected(self.view.selection_panel.ignore_listbox)

            # remove whatever's in the ignore wcid list
            cleaned_list = self.pcap_converter.get_clean_list(self.filtered_list, ignore_wcids)

            # get monster and item generator wcids
            mgen_wcid = self.view.selection_panel.mgen_combo.get().strip()
            igen_wcid = self.view.selection_panel.igen_combo.get().strip()

            # get monster and item generator locs
            mgen_loc = self.view.selection_panel.mgen_loc_entry.get().strip()
            igen_loc = self.view.selection_panel.igen_loc_entry.get().strip()

            if not mgen_loc or not igen_loc:
                showerror("Error", "The monster and item generator locations are required.")
                return

            # make links
            monster_links = self.pcap_converter.get_links(cleaned_list, mgen_wcid, "Monster Generator", monster_wcids,
                                                          mgen_loc)
            item_links = self.pcap_converter.get_links(cleaned_list, igen_wcid, "Item Generator", item_wcids, igen_loc)

            landblock_desc = None
            if len(self.view.top_panel.desc_entry.get()) > 0:
                landblock_desc = self.view.top_panel.desc_entry.get()
            else:
                showerror("Error", "The landblock description is required.")
                return

            nickname = "Asheron"
            if len(self.view.top_panel.nickname_entry.get()) > 0:
                nickname = self.view.top_panel.nickname_entry.get()

            self.pcap_converter.output_map(nickname, landblock_desc, cleaned_list, monster_links, item_links)

            # output what it's opening to console
            self.view.console.text_area.configure(state='normal')
            self.view.console.text_area.delete('1.0', tk.END)
            self.view.console.text_area.insert('1.0', "Done")
            self.view.console.text_area.configure(state='disabled')


# use to inspect a landblock
class Toolbar:

    def __init__(self, parent, cont):
        self.frame = tk.Frame(parent)

        inspect_label = tk.Label(self.frame, text="Make GDLE Spawn Map", font="Arial 12")
        open_pcap_button = tk.Button(self.frame, text="Open PCAP", command=cont.open_landblock_pcap)

        threshold_label = tk.Label(self.frame, text="Seen more than")
        self.threshold_scale = tk.Scale(self.frame, from_=0, to=10, orient=tk.HORIZONTAL)
        self.threshold_scale.set(1)
        self.make_map_button = tk.Button(self.frame, text="Make Map", command=cont.make_gdle_spawn_map)
        self.make_map_button["state"] = "disabled"

        # layout
        inspect_label.grid(row=0, column=0, padx=5, pady=5)
        open_pcap_button.grid(row=0, column=1, padx=5, pady=5)
        self.make_map_button.grid(row=0, column=2, padx=5, pady=5)
        threshold_label.grid(row=1, column=0, padx=5, pady=5)
        self.threshold_scale.grid(row=1, column=1, padx=5, pady=5)


# use to convert spawn maps
class BottomPanel:

    def __init__(self, parent, cont):
        self.frame = tk.Frame(parent)
        self.cont = cont

        # convert a gdle spawn map json to an ace spawn map sql
        label2 = tk.Label(self.frame, text="Batch convert (GDLE to ACE)", font="Arial 12")
        open_landblock_folder = tk.Button(self.frame, text="Open Folder and Run",
                                          command=self.batch_convert_gdle_to_ace)

        label2.grid(row=0, column=0, padx=5, pady=5)
        open_landblock_folder.grid(row=0, column=1, padx=5, pady=5)

    def batch_convert_gdle_to_ace(self):
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

    def get_wcid_set(self, entries):
        # TODO revise this since no longer using entries, using listboxes instead

        wcid_list = []

        for entry in entries:
            wcid_list.append(int(entry))

        return set(wcid_list)


def main():
    # if on Windows, fix blurry font
    if os.name == 'nt':
        windll.shcore.SetProcessDpiAwareness(1)

    root = tk.Tk()
    root.title("AC Spawn Maps")
    Controller(root)
    root.mainloop()


if __name__ == '__main__':
    main()
