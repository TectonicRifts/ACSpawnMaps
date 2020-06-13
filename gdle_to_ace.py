import json
import datetime
import os


def convert_spawn_map(file_folder, file_name):
    """Convert a GDLE spawn map to ACE sql format."""

    landblock_4 = ""
    output_file = ""
    landblock_dec = ""

    my_id_list = []
    my_wcid_list = []
    my_desc_list = []
    my_origin_list = []
    my_angles_list = []
    my_cell_list = []

    # links
    link_descriptions = []
    sources = []  # child
    targets = []  # parent

    with open(os.path.join(file_folder, file_name)) as file_object:
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
                landblock_4 = hex(landblock_dec)[2:6]
                if '00' in landblock_4:
                    landblock_4 = landblock_4[2:4] + landblock_4[0:2]
                output_file = landblock_4.upper() + '.sql'
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
                                                    my_origin_list.append(
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
                                                    my_angles_list.append(
                                                        str(angles_w) + ', ' + str(angles_x) + ', ' + str(
                                                            angles_y) + ', ' + str(angles_z))

                                        elif k5 == 'objcell_id':
                                            cell = v5
                                            my_cell_list.append(cell)
                    elif k2 == 'links':
                        for k8, v8 in enumerate(v2):
                            for k9, v9 in v8.items():
                                if k9 == '_linkinfo':
                                    link_descriptions.append(v9)
                                elif k9 == 'source':
                                    sources.append(v9)
                                elif k9 == 'target':
                                    targets.append(v9)

    with open(output_file, 'w') as file_object:

        today = str(datetime.date.today())

        file_object.write(
            "DELETE FROM `landblock_instance` WHERE `landblock` = 0x" + str(landblock_4).upper() + ";\n\n")

        for i, j, k, l, m, n in zip(my_wcid_list, my_cell_list, my_origin_list, my_angles_list, my_desc_list,
                                    my_id_list):

            guid = str(n)

            is_link_child = "False"
            if n in sources:
                is_link_child = "True"
            else:
                is_link_child = "False"

            file_object.write(
                "INSERT INTO `landblock_instance` (`guid`, `weenie_Class_Id`, `obj_Cell_Id`, `origin_X`, `origin_Y`, `origin_Z`, `angles_W`, `angles_X`, `angles_Y`, `angles_Z`, `is_Link_Child`, `last_Modified`)\n")
            file_object.write('VALUES (' + guid + ', ' + str(i) + ', ' + str(j) + ', ' + str(k) + ', ' + str(
                l) + ', ' + is_link_child + ", '" + today + " 00:00:00');\n")
            file_object.write("/* " + str(m) + " */\n\n")

        link_counter = 0

        # get unique targets (i.e. parents) in the list
        unique_targets = set(targets)

        for generator in unique_targets:
            file_object.write("DELETE FROM `landblock_instance_link` WHERE `parent_GUID` =" + str(generator) + ";\n\n")

        # this handles case of multiple generators (e.g., both monster and item)
        previous_target = 0
        current_target = 0

        counter_cutoffs = []

        for o, p, q in zip(targets, sources, link_descriptions):

            current_target = o
            if current_target == previous_target:
                pass
            else:
                if previous_target == 0:
                    pass
                else:
                    counter_cutoffs.append(link_counter - 1)

            previous_target = current_target
            link_counter += 1

        counter_cutoffs.append(len(targets) - 1)

        # reset counter
        link_counter = 0
        start_line = True

        for o, p, q in zip(targets, sources, link_descriptions):

            target = str(o)
            source = str(p)

            if start_line:
                file_object.write(
                    "INSERT INTO `landblock_instance_link` (`parent_GUID`, `child_GUID`, `last_Modified`)\n")
                file_object.write('VALUES (' + target + ", " + source + ", '" + today + " 00:00:00') ")
                start_line = False
            elif link_counter in counter_cutoffs:
                file_object.write('     , (' + target + ", " + source + ", '" + today + " 00:00:00'); ")
                start_line = True
            else:
                file_object.write('     , (' + target + ", " + source + ", '" + today + " 00:00:00') ")

            file_object.write("/* " + str(q) + " */\n")
            link_counter += 1
