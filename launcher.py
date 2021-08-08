import tkinter as tk
from ctypes import windll
from tkinter import filedialog
from tkinter.messagebox import showerror
import tkinter.scrolledtext as scrolledtext
import os
from pathlib import Path
import platform
import subprocess
import pcap_helper
import matplotlib.pyplot as plt
import numpy as np


# output console
class Console:

    def __init__(self, parent, cont):
        self.frame = tk.Frame(parent)

        self.text_area = tk.scrolledtext.ScrolledText(self.frame, height=10, width=50, undo=True)
        self.text_area.configure(state='disabled')

        clear_button = tk.Button(self.frame, text="Clear", command=self.clear)

        self.text_area.grid(row=0, column=0)
        clear_button.grid(row=1, column=0, padx=5, pady=5, sticky="e")

    def output(self, s):
        self.text_area.configure(state='normal')
        self.text_area.insert(tk.INSERT, s + "\n")
        self.text_area.yview(tk.END)
        self.text_area.configure(state='disabled')

    def clear(self):
        self.text_area.configure(state='normal')
        self.text_area.delete('1.0', tk.END)
        self.text_area.configure(state='disabled')


# panel where you select monsters and items
class SelectionPanel:

    def __init__(self, parent, cont):
        self.frame = tk.Frame(parent)

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
        mob_listbox_label.grid(row=0, column=0, padx=5, pady=5)
        mob_frame.grid(row=1, column=0, padx=5, pady=5)
        item_listbox_label.grid(row=0, column=1, padx=5, pady=5)
        item_frame.grid(row=1, column=1, padx=5, pady=5)

        ignore_listbox_label.grid(row=0, column=2, padx=5, pady=5)
        ignore_frame.grid(row=1, column=2, padx=5, pady=5)

    def make_listbox(self, parent, my_font, selection_mode):
        """Returns a tuple with a frame and a listbox with a vertical scrollbar."""
        frame = tk.Frame(parent)

        listbox = tk.Listbox(frame, selectmode=selection_mode, font=my_font, exportselection=0, height=20)
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
        """Returns a list of WCIDs for selected entries in a listbox."""
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
        self.cont = cont

        self.by_proximity = tk.IntVar(value=1)
        proximity_check_box = tk.Checkbutton(self.frame, text="Remove by Proximity",
                                             variable=self.by_proximity, font=norm_font)
        self.by_range = tk.IntVar(value=0)
        range_check_box = tk.Checkbutton(self.frame, text="Keep in Range (all fields required)",
                                         variable=self.by_range, font=norm_font)

        self.proximity_entry = tk.Entry(self.frame, bg="white", font=norm_font)
        self.proximity_entry.insert(0, 2)  # default of 2

        min_header = tk.Label(self.frame, text="min", font=norm_font)
        max_header = tk.Label(self.frame, text="max", font=norm_font)

        x_label = tk.Label(self.frame, text="x", font=norm_font)
        self.x_min_entry = tk.Entry(self.frame, bg="white", font=norm_font)
        self.x_max_entry = tk.Entry(self.frame, bg="white", font=norm_font)

        y_label = tk.Label(self.frame, text="y", font=norm_font)
        self.y_min_entry = tk.Entry(self.frame, bg="white", font=norm_font)
        self.y_max_entry = tk.Entry(self.frame, bg="white", font=norm_font)

        z_label = tk.Label(self.frame, text="z", font=norm_font)
        self.z_min_entry = tk.Entry(self.frame, bg="white", font=norm_font)
        self.z_max_entry = tk.Entry(self.frame, bg="white", font=norm_font)

        filter_button = tk.Button(self.frame, text="Apply", command=self.apply_filter)

        # layout
        proximity_check_box.grid(row=0, column=0, padx=5, pady=5, columnspan=2, sticky="w")
        self.proximity_entry.grid(row=0, column=2, padx=5, pady=5)
        range_check_box.grid(row=2, column=0, padx=5, pady=5, columnspan=2, sticky="w")
        min_header.grid(row=3, column=1, padx=5, pady=5)
        max_header.grid(row=3, column=2, padx=5, pady=5)
        x_label.grid(row=4, column=0, padx=5, pady=5)
        self.x_min_entry.grid(row=4, column=1, padx=5, pady=5)
        self.x_max_entry.grid(row=4, column=2, padx=5, pady=5)
        y_label.grid(row=5, column=0, padx=5, pady=5)
        self.y_min_entry.grid(row=5, column=1, padx=5, pady=5)
        self.y_max_entry.grid(row=5, column=2, padx=5, pady=5)
        z_label.grid(row=6, column=0, padx=5, pady=5)
        self.z_min_entry.grid(row=6, column=1, padx=5, pady=5)
        self.z_max_entry.grid(row=6, column=2, padx=5, pady=5)
        filter_button.grid(row=7, column=2, padx=5, pady=5, sticky="e")

    def apply_filter(self):

        if self.by_proximity.get() == 1:

            proximity = self.proximity_entry.get().strip()
            if self.is_number(proximity):
                self.cont.filter_by_proximity(self.cont.filtered_list, int(proximity))

        if self.by_range.get() == 1:

            x_min = self.x_min_entry.get().strip()
            x_max = self.x_max_entry.get().strip()
            if x_min == "" or x_max == "":
                self.cont.x_min = None
                self.cont.x_max = None
            else:
                if self.is_number(x_min) and self.is_number(x_max):
                    self.cont.x_min = int(x_min)
                    self.cont.x_max = int(x_max)

            y_min = self.y_min_entry.get().strip()
            y_max = self.y_max_entry.get().strip()
            if y_min == "" or y_max == "":
                self.cont.y_min = None
                self.cont.y_max = None
            else:
                if self.is_number(y_min) and self.is_number(y_max):
                    self.cont.y_min = int(y_min)
                    self.cont.y_max = int(y_max)

            z_min = self.z_min_entry.get().strip()
            z_max = self.z_max_entry.get().strip()
            if z_min == "" or z_max == "":
                self.cont.z_min = None
                self.cont.z_max = None
            else:
                if self.is_number(z_min) and self.is_number(z_max):
                    self.cont.z_min = int(z_min)
                    self.cont.z_max = int(z_max)

            self.cont.filter_by_range(self.cont.filtered_list)

    def is_number(self, val):
        try:
            float(val)
            return True
        except ValueError:
            return False


class View:

    def __init__(self, parent, cont):
        self.frame = tk.Frame(parent)
        self.cont = cont

        self.top_panel = TopPanel(self.frame, cont)
        self.toolbar = Toolbar(self.frame, cont)
        self.console = Console(self.frame, cont)
        self.selection_panel = SelectionPanel(self.frame, cont)

        # layout
        self.top_panel.frame.grid(row=0, column=0, padx=5, pady=5)
        self.console.frame.grid(row=0, column=1, padx=5, pady=5)
        self.toolbar.frame.grid(row=1, column=0, padx=5, pady=5)
        self.selection_panel.frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        self.frame.grid()


class Controller:

    def __init__(self, parent):

        self.view = View(parent, self)
        self.unfiltered_list = []
        self.filtered_list = []

        # this is the sql file (i.e., sql commands) currently being worked on
        self.sql_commands = []

        # this is the name of the output file
        self.sql_output = None

        self.wcid_list = None

        # delete from line
        self.delete_line = None

        self.mgen = None
        self.igen = None

        self.monster_links = None
        self.item_links = None

        self.x_min = None
        self.y_min = None
        self.z_min = None

        self.x_max = None
        self.y_max = None
        self.z_max = None

    def open_file(self):
        """Load a pcap landblock .sql file."""

        self.sql_commands.clear()
        self.filtered_list.clear()
        self.sql_output = None

        my_file = filedialog.askopenfilename(filetypes=[("sql files", "*.sql")])
        if my_file:
            with open(my_file) as file_object:
                sql_file = file_object.read()
                my_commands = sql_file.split("INSERT INTO")
                for command in my_commands:
                    if "landblock_instance" in command and "landblock_instance_link" not in command:
                        if "DELETE FROM" in command:
                            self.delete_line = command
                        else:
                            if command.strip() == "":
                                pass
                            else:
                                self.sql_commands.append(command.strip())

                # this is the output file name
                self.sql_output = os.path.split(my_file)[1]

                for command in self.sql_commands:
                    self.unfiltered_list.append(pcap_helper.get_landblock_entry(command))

                self.unfiltered_list.sort(key=lambda x: x.name, reverse=True)
                self.filtered_list = self.unfiltered_list

                self.landblock_stats()
                self.show_entries()

    def landblock_stats(self):

        self.view.console.clear()
        self.view.console.output("Loaded landblock: " + str(self.sql_output))
        total_entries = len(self.filtered_list)
        self.view.console.output("Total entries: " + str(total_entries))

        xs = []
        ys = []
        zs = []
        for entry in self.filtered_list:
            xs.append(entry.ox)
            ys.append(entry.oy)
            zs.append(entry.oz)

        self.view.console.output("x min: " + str(round(min(xs), 2)))
        self.view.console.output("x max: " + str(round(max(xs), 2)))
        self.view.console.output("y min: " + str(round(min(ys), 2)))
        self.view.console.output("y max: " + str(round(max(ys), 2)))
        self.view.console.output("z min: " + str(round(min(zs), 2)))
        self.view.console.output("z max: " + str(round(max(zs), 2)))

    def save_sql(self):

        Path("output/").mkdir(parents=True, exist_ok=True)

        if self.filtered_list:
            with open("output/" + self.sql_output, 'w') as file_object:
                file_object.write(self.delete_line)
                for entry in self.filtered_list:
                    command = entry.get_sql_entry()
                    if command.strip() != "":
                        if "Lifestoned Changelog" in command:
                            pass
                        else:
                            file_object.write(command)
                if self.monster_links:
                    file_object.write(self.monster_links)
                    self.mgen = None
                    self.monster_links = None
                if self.item_links:
                    file_object.write(self.item_links)
                    self.igen = None
                    self.item_links = None
                file_object.write("\n")
        else:
            tk.messagebox.showinfo("Info", "There was no file to save.")

    def reset_all_filters(self):
        self.filtered_list = self.unfiltered_list
        self.show_entries()
        self.view.console.output("All filters have been reset.")

    def filter_by_proximity(self, landblock_entries, proximity):
        filtered_entries = pcap_helper.filter_by_proximity(landblock_entries, proximity)
        total_removed = len(landblock_entries) - len(filtered_entries)
        self.view.console.output("Filter by proximity removed: " + str(total_removed))
        self.filtered_list = filtered_entries

    def filter_by_range(self, landblock_entries):

        filtered_entries = pcap_helper.filter_by_range(landblock_entries,
                                                       self.x_min, self.x_max,
                                                       self.y_min, self.y_max,
                                                       self.z_min, self.z_max)

        total_removed = len(landblock_entries) - len(filtered_entries)
        self.view.console.output("Filter by range removed: " + str(total_removed))
        self.filtered_list = filtered_entries

    def plot_landblock(self):

        unfiltered_len = len(self.unfiltered_list)
        filtered_len = len(self.filtered_list)

        if unfiltered_len > 0:
            fig = plt.figure(figsize=(8, 8))
            ax = fig.add_subplot(111, projection='3d')
            my_xs = []
            my_ys = []
            my_zs = []
            group = []
            for entry in self.unfiltered_list:
                my_xs.append(entry.ox)
                my_ys.append(entry.oy)
                my_zs.append(entry.oz)

                if unfiltered_len != filtered_len:
                    if entry in self.filtered_list:
                        group.append(1)
                    else:
                        group.append(0)

            if len(group) > 0:
                my_plot = ax.scatter(xs=my_xs, ys=my_ys, zs=my_zs, cmap="coolwarm", c=group)
                cb = plt.colorbar(my_plot, pad=0.2)
                cb.set_ticks([0, 1])
                cb.set_ticklabels(["Remove", "Keep"])
            else:
                ax.scatter(xs=my_xs, ys=my_ys, zs=my_zs)

            ax.set_title(str(self.sql_output))
            ax.set_xlabel("X")
            ax.set_ylabel("Y")
            ax.set_zlabel("Z")

            plt.show()
        else:
            self.view.console.output("There was nothing to plot.")

    def get_unique_entries(self):
        uniques = {}
        # return unique wcids with names for clarity, used for view
        for entry in self.filtered_list:
            uniques[entry.wcid] = entry
        return uniques

    def show_entries(self):
        uniques = self.get_unique_entries()
        listbox_list = self.view.selection_panel.get_list_boxes()

        # clear listboxes
        for listbox in listbox_list:
            listbox.delete(0, tk.END)

        # add entries
        i = 0
        for wcid, entry in sorted(uniques.items()):  # sort and output

            entry_formatted = str(wcid) + "," + str(entry.name)
            for listbox in listbox_list:
                listbox.insert(i, entry_formatted)
            i += 1

    def print_entries(self):
        uniques = self.get_unique_entries()
        i = 0
        for wcid, entry in sorted(uniques.items()):  # sort and output
            entry_formatted = str(wcid) + "," + str(entry.name)
            self.view.console.output(entry_formatted)

    def make_map(self):
        if self.filtered_list:

            mob_wcids = self.view.selection_panel.get_selected(self.view.selection_panel.mob_listbox)
            item_wcids = self.view.selection_panel.get_selected(self.view.selection_panel.item_listbox)
            ignore_wcids = self.view.selection_panel.get_selected(self.view.selection_panel.ignore_listbox)

            for entry in self.filtered_list:
                if "Linkable Monster" in entry.name and self.mgen is None:
                    self.mgen = entry

            for entry in self.filtered_list:
                if "Linkable Item" in entry.name and self.igen is None:
                    self.igen = entry

            wcid_list = []

            # make sure selected monsters and items don't get ignored
            for wcid in ignore_wcids:
                if wcid in mob_wcids or wcid in item_wcids:
                    pass
                else:
                    wcid_list.append(wcid)

            # remove whatever's in the ignore wcid list
            cleaned_list = pcap_helper.get_clean_list(self.filtered_list, wcid_list)

            # make links
            if self.mgen:
                self.monster_links = pcap_helper.get_links(cleaned_list, self.mgen.guid, mob_wcids)
            if self.igen:
                self.item_links = pcap_helper.get_links(cleaned_list, self.igen.guid, item_wcids)

            self.filtered_list = cleaned_list
            self.save_sql()
            self.view.console.output("Done.")

    def open_output_folder(self):
        Path("output/").mkdir(parents=True, exist_ok=True)
        path = "output"

        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])


# use to inspect a landblock
class Toolbar:

    def __init__(self, parent, cont):
        self.frame = tk.Frame(parent)

        open_button = tk.Button(self.frame, text="Open", command=cont.open_file)
        plot_button = tk.Button(self.frame, text="Plot", command=cont.plot_landblock)
        reset_button = tk.Button(self.frame, text="Reset", command=cont.reset_all_filters)
        print_button = tk.Button(self.frame, text="Print", command=cont.print_entries)
        save_button = tk.Button(self.frame, text="Save", command=cont.make_map)
        output_button = tk.Button(self.frame, text="Files", command=cont.open_output_folder)

        # layout
        open_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        plot_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        reset_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        print_button.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        save_button.grid(row=0, column=4, padx=5, pady=5, sticky="ew")
        output_button.grid(row=0, column=5, padx=5, pady=5, sticky="ew")


norm_font = ("Arial", 12)


def main():
    # if on Windows, fix blurry font
    if os.name == 'nt':
        windll.shcore.SetProcessDpiAwareness(1)

    version = 0.4
    root = tk.Tk()
    root.title("AC Spawn Maps " + str(version))
    Controller(root)
    root.mainloop()


if __name__ == '__main__':
    main()
