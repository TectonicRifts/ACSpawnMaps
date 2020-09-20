def get_landblock_entry(command):
    landblock_entry = LandblockEntry(
        get_guid(command),
        get_wcid(command),
        get_cell_id(command),
        get_origin_xyz(command),
        get_angles_wxyz(command),
        get_last_modified(command),
        get_name(command)
    )

    return landblock_entry


def get_links(filtered_list, parent_guid, wcid_set):
    if len(wcid_set) == 0:
        return None

    entry = None

    my_list = []

    for entry in filtered_list:
        if entry.wcid in wcid_set:
            my_list.append(entry)
            entry.is_link_child = True

    for i in range(len(my_list)):
        if i == 0:
            entry = """INSERT INTO `landblock_instance_link` (`parent_GUID`, `child_GUID`, `last_Modified`)\n"""
            entry += f"""VALUES ({parent_guid}, {my_list[i].guid}, '2019-02-10 00:00:00') /* {my_list[i].name} */"""
        else:
            entry += f"""\n     , ({parent_guid}, {my_list[i].guid}, '2019-02-10 00:00:00') /* {my_list[i].name} */"""

    entry += ";\n\n"

    return entry


def filter_by_distance(landblock_entries):
    filtered_list = landblock_entries.copy()
    to_remove = []

    groups = {}
    for entry in landblock_entries:
        groups.setdefault(entry.wcid, []).append(entry)

    nested_list = [groups[wcid] for wcid in sorted(groups.keys())]

    for my_list in nested_list:
        for i in my_list:
            for j in my_list:
                if i == j:
                    pass
                else:
                    d = calc_distance(i, j)
                    if d < 2:
                        if i in to_remove or j in to_remove:
                            pass
                        else:
                            to_remove.append(i)

    for entry in to_remove:
        filtered_list.remove(entry)

    return filtered_list


def calc_distance(p1, p2):
    """Calculate the distance between 2 weenies."""
    d = ((p2.ox - p1.ox) ** 2 + (p2.oy - p1.oy) ** 2 + (p2.oz - p1.oz) ** 2) ** 0.5
    return d


def filter_by_x(landblock_entries, x_min, x_max):
    """Keep only weenies with an origin x less than the threshold."""
    filtered_list = []

    for entry in landblock_entries:
        if x_min <= entry.ox <= x_max:
            filtered_list.append(entry)

    return filtered_list


def filter_by_y(landblock_entries, y_min, y_max):
    """Keep only weenies with an origin y less than the threshold."""
    filtered_list = []

    for entry in landblock_entries:
        if y_min <= entry.oy <= y_max:
            filtered_list.append(entry)

    return filtered_list


def filter_by_z(landblock_entries, z_min, z_max):
    """Keep only weenies with an origin z less than the threshold."""
    filtered_list = []

    for entry in landblock_entries:
        if z_min <= entry.oz <= z_max:
            filtered_list.append(entry)

    return filtered_list


def get_clean_list(filtered_list, ignore_wcids):
    my_list = []
    for entry in filtered_list:
        if entry.wcid in ignore_wcids:
            pass
        else:
            my_list.append(entry)

    return my_list


def get_guid(command):
    split_entry = command.split("\n")
    if "VALUES" in split_entry[1]:
        comma_split = split_entry[1].split(",")
        parentheses_split = comma_split[0].split("(")
        return parentheses_split[1].strip()


def get_wcid(command):
    split_entry = command.split("\n")
    if "VALUES" in split_entry[1]:
        comma_split = split_entry[1].split(",")
        return comma_split[1].strip()


def get_name(command):
    split_entry = command.split("\n")
    if "VALUES" in split_entry[1]:
        try:
            asterisk_split = split_entry[1].split("*")
            my_data = asterisk_split[1].strip()
        except IndexError:
            my_data = "Placeholder Name"

        return my_data


def get_cell_id(command):
    split_entry = command.split("\n")
    if "VALUES" in split_entry[1]:
        comma_split = split_entry[1].split(",")
        return comma_split[2].strip()


def get_origin_xyz(command):
    split_entry = command.split("\n")
    if "VALUES" in split_entry[1]:
        comma_split = split_entry[1].split(",")
        x = float(comma_split[3].strip())
        y = float(comma_split[4].strip())
        z = float(comma_split[5].strip())
        return x, y, z


def get_angles_wxyz(command):
    split_entry = command.split("\n")
    if "VALUES" in split_entry[1]:
        comma_split = split_entry[1].split(",")
        w = float(comma_split[6].strip())
        x = float(comma_split[7].strip())
        y = float(comma_split[8].strip())
        z = float(comma_split[9].strip())
        return w, x, y, z


def get_is_link_child(command):
    split_entry = command.split("\n")
    if "VALUES" in split_entry[1]:
        comma_split = split_entry[1].split(",")
        return comma_split[10].strip()


def get_last_modified(command):
    split_entry = command.split("\n")
    if "VALUES" in split_entry[1]:
        comma_split = split_entry[1].split(",")
        more_split = comma_split[11].split(")")
        return more_split[0].strip()


class LandblockEntry:

    def __init__(self, guid, wcid, cell, origin, angles, last_modified, name):
        self.guid = guid
        self.wcid = int(wcid)
        self.cell = cell

        self.ox = origin[0]
        self.oy = origin[1]
        self.oz = origin[2]

        if self.ox == 0.0:
            self.ox = 0
        if self.oy == 0.0:
            self.ox = 0
        if self.oz == 0.0:
            self.ox = 0

        self.aw = angles[0]
        self.ax = angles[1]
        self.ay = angles[2]
        self.az = angles[3]

        if self.aw == 0.0:
            self.aw = 0
        if self.ax == 0.0:
            self.ax = 0
        if self.ay == 0.0:
            self.ay = 0
        if self.az == 0.0:
            self.az = 0

        self.is_link_child = False
        self.last_modified = last_modified
        self.name = name

    def get_sql_entry(self):
        entry = """INSERT INTO `landblock_instance` (`guid`, `weenie_Class_Id`, `obj_Cell_Id`, `origin_X`, `origin_Y`, `origin_Z`, `angles_W`, `angles_X`, `angles_Y`, `angles_Z`, `is_Link_Child`, `last_Modified`)\n"""
        entry += f"""VALUES ({self.guid}, {self.wcid}, {self.cell}, {self.ox}, {self.oy}, {self.oz}, {self.aw}, {self.ax}, {self.ay}, {self.az}, {self.is_link_child}, {self.last_modified}); /* {self.name} */\n"""
        entry += f"""/* @teleloc {self.cell} [{self.ox} {self.oy} {self.oz}] {self.aw} {self.ax} {self.ay} {self.az} */\n\n"""

        return entry
