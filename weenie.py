class LandblockEntry:

    def __init__(self, guid, wcid, desc, origin_list, angles_list, cell):
        self.guid = guid
        self.wcid = wcid

        self.desc = desc.replace("\"", " ")

        self.origin_list = origin_list

        origin_split = origin_list.split(',')
        self.ox = float(origin_split[0])
        self.oy = float(origin_split[1])
        self.oz = float(origin_split[2])

        self.angles_list = angles_list
        angles_split = angles_list.split(',')
        self.aw = angles_split[0]
        self.ax = angles_split[1]
        self.ay = angles_split[2]
        self.az = angles_split[3]

        self.cell = cell

        self.name = self.get_name()

    def get_name(self):
        split1 = self.desc.split(',')
        return split1[0]

    def fix_cell(self):
        split1 = self.desc.split(',')
        split2 = split1[2].split(' ')
        self.cell = int(split2[7], 16)

    def get_hits(self):
        split1 = self.desc.split(',')
        split2 = split1[2].split(' ')
        hits = int(split2[2])
        return hits

    def get_json_entry(self):
        entry = '{"id": ' + str(self.guid) + ', "wcid": ' + str(
            self.wcid) + ', "desc": "' + self.desc + '", ' + '"pos": { "frame": { "origin": { "x": ' + str(
            self.ox) + ', "y": ' + str(self.oy) + ', "z": ' + str(self.oz) + '}, ' + '"angles": { ' + '"w": ' + str(
            self.aw) + ', "x": ' + str(self.ax) + ', "y": ' + str(self.ay) + ', "z": ' + str(
            self.az) + '}}, ' + '"objcell_id": ' + str(self.cell) + ' }}'
        return entry


class GeneratorLink:

    def __init__(self, parent, child, desc):
        self.parent = parent
        self.child = child
        self.desc = desc

    def get_json_entry(self):
        # the target is the parent, the source is the child
        entry = '{"_linkinfo": "' + self.desc + '", "source": ' + str(self.child) + ', "target": ' + str(
            self.parent) + ' }'
        return entry


class LandblockLoc:

    def __init__(self, ox, oy, oz, aw, ax, ay, az, cell):
        self.origin = ox + "," + oy + "," + oz
        self.angles = aw + "," + ax + "," + ay + "," + az
        self.cell = cell
