import json

from weenie import GeneratorLink
from weenie import LandblockEntry
from weenie import LandblockLoc

import gdle_to_ace

class PcapConverter:

    def __init__(self):

        self.landblock_4 = ""

        self.origin_list = []
        self.angles_list = []
        self.cell_list = []

    def load_pcap(self, input_file, threshold):

        landblock_entries = []

        landblock_dec = ""

        my_id_list = []
        my_wcid_list = []
        my_desc_list = []

        # links
        link_descriptions = []
        sources = []  # child
        targets = []  # parent

        with open(input_file) as file_object:
            my_json = json.load(file_object)

            wcid = 0
            desc = ''
            cell = ''
            origin_x = ''
            origin_y = ''
            origin_z = ''

            angles_w = ''
            angles_x = ''
            angles_y = ''
            angles_z = ''

            for k1, v1 in my_json.items():
                if k1 == 'key':
                    landblock_dec = v1
                    self.landblock_4 = hex(landblock_dec)[2:6]
                    if '00' in self.landblock_4:
                        self.landblock_4 = self.landblock_4[2:4] + self.landblock_4[0:2]
                elif k1 == 'value':
                    for k2, v2 in v1.items():
                        if k2 == 'weenies':
                            for k3, v3 in enumerate(v2):
                                for k4, v4 in v3.items():
                                    if k4 == 'id':
                                        my_id_list.append(v4)
                                    if k4 == 'wcid':
                                        my_wcid_list.append(v4)
                                    if k4 == 'desc':
                                        my_desc_list.append(v4)
                                    if k4 == 'pos':
                                        for k5, v5 in v4.items():
                                            if k5 == 'frame':
                                                for k6, v6 in v5.items():
                                                    if k6 == 'origin':
                                                        for k7, v7 in v6.items():
                                                            if k7 == 'x':
                                                                origin_x = v7
                                                            elif k7 == 'y':
                                                                origin_y = v7
                                                            elif k7 == 'z':
                                                                origin_z = v7
                                                        self.origin_list.append(
                                                            str(origin_x) + ', ' + str(origin_y) + ', ' + str(origin_z))

                                                    elif k6 == 'angles':
                                                        for k7, v7 in v6.items():
                                                            if k7 == 'w':
                                                                angles_w = v7
                                                            elif k7 == 'x':
                                                                angles_x = v7
                                                            elif k7 == 'y':
                                                                angles_y = v7
                                                            elif k7 == 'z':
                                                                angles_z = v7
                                                        self.angles_list.append(
                                                            str(angles_w) + ', ' + str(angles_x) + ', ' + str(
                                                                angles_y) + ', ' + str(angles_z))

                                            elif k5 == 'objcell_id':
                                                cell = v5
                                                self.cell_list.append(cell)

        for i, j, k, l, m, n in zip(my_id_list, my_wcid_list, my_desc_list, self.origin_list, self.angles_list,
                                    self.cell_list):
            entry = LandblockEntry(i, j, k, l, m, n)
            landblock_entries.append(entry)

        # sort by name
        landblock_entries.sort(key=lambda x: x.name, reverse=True)

        # renumber
        hex_id = '7' + self.landblock_4 + '000'
        new_id = int(hex_id, 16)

        for entry in landblock_entries:
            entry.guid = new_id
            new_id += 1

        self.fix_cell(landblock_entries)

        # remove objects based on how many times they were seen
        filtered_list = self.filter_by_seen(landblock_entries, threshold)

        # remove objects too close in space
        filtered_list = self.filter_by_distance(filtered_list)

        return filtered_list

    def fix_cell(self, entries):
        """Correct the object cell ID for every weenie on the given list."""
        for entry in entries:
            entry.fix_cell()

    def filter_by_seen(self, entries, threshold):
        """Filter the given list of weenies by how many times they were seen."""
        filtered_list = []

        for entry in entries:
            if entry.get_hits() > threshold:
                filtered_list.append(entry)

        return filtered_list

    def filter_by_distance(self, entries):

        filtered_list = entries.copy()
        to_remove = []

        groups = {}
        for entry in entries:
            groups.setdefault(entry.wcid, []).append(entry)

        nested_list = [groups[wcid] for wcid in sorted(groups.keys())]

        for my_list in nested_list:
            for i in my_list:
                for j in my_list:
                    if i == j:
                        pass
                    else:
                        d = self.calc_distance(i, j)
                        if d < 2:
                            if i in to_remove or j in to_remove:
                                pass
                            else:
                                to_remove.append(i)

        for entry in to_remove:
            filtered_list.remove(entry)

        return filtered_list

    def calc_distance(self, p1, p2):
        """Calculate the distance between 2 weenies."""
        d = ((p2.ox - p1.ox) ** 2 + (p2.oy - p1.oy) ** 2 + (p2.oz - p1.oz) ** 2) ** 0.5
        return d

    def get_links(self, filtered_list, gen_wcid, gen_desc, wcid_set, gen_loc):
        """Return a list of links"""
        links = []

        if len(wcid_set) == 0:
            return links

        new_id = filtered_list[-1].guid + 1

        my_loc = self.extract_loc(gen_loc)
        generator = LandblockEntry(new_id, gen_wcid, gen_desc, my_loc.origin, my_loc.angles, my_loc.cell)

        filtered_list.append(generator)

        for entry in filtered_list:
            if entry.wcid in wcid_set:
                link = GeneratorLink(generator.guid, entry.guid, entry.name + ' -> ' + generator.desc)
                links.append(link)

        return links

    def extract_loc(self, loc_paste):
        """Returns location from a /myloc paste."""
        split_loc = loc_paste.split(" ")

        cell_hex = split_loc[0]
        cell_dec = int(cell_hex, 16)

        ox = split_loc[1].replace("[", "")
        oy = split_loc[2]
        oz = split_loc[3].replace("]", "")

        aw = split_loc[4]
        ax = split_loc[5]
        ay = split_loc[6]
        az = split_loc[7]

        return LandblockLoc(ox, oy, oz, aw, ax, ay, az, cell_dec)

    def get_clean_list(self, filtered_list, ignore_wcids):

        my_list = []
        for entry in filtered_list:
            if entry.wcid in ignore_wcids:
                pass
            else:
                my_list.append(entry)

        return my_list

    def output_map(self, nickname, land_desc, filtered_list, monster_links, item_links):

        # now do output, make a gdle spawn map file
        # use filtered_list for entries, also have monster_links and item_links

        # landblock id
        land_hex = self.landblock_4 + '0000'
        land_id = int(land_hex, 16)

        my_json = '{"key": ' + str(land_id) + ', "value": { "links": ['

        counter = 0
        for entry in monster_links:
            my_json = my_json + entry.get_json_entry()

            if counter < (len(monster_links) - 1):
                my_json = my_json + ','
            counter += 1

        counter = 0
        for entry in item_links:

            if counter == 0:
                my_json = my_json + ','

            my_json = my_json + entry.get_json_entry()

            if counter < (len(item_links) - 1):
                my_json = my_json + ','
            counter += 1

        my_json = my_json + '], "weenies": ['

        counter = 0
        for entry in filtered_list:
            my_json = my_json + entry.get_json_entry()

            if counter < (len(filtered_list) - 1):
                my_json = my_json + ','
            counter += 1

        my_json = my_json + ']},"desc": "' + land_desc + '", "modifiedBy": "' + nickname + '", "changeLog": [], "isDone": false }'

        file_name = str(self.landblock_4) + '.json'

        with open(file_name, 'w') as file_object:
            file_object.write(my_json)

        return file_name
