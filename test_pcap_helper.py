from unittest import TestCase
import pcap_helper


class Test(TestCase):

    def test_get_guid(self):
        command = (
            "`landblock_instance` (`guid`, `weenie_Class_Id`, `obj_Cell_Id`, `origin_X`, `origin_Y`, `origin_Z`, `angles_W`, `angles_X`, `angles_Y`, `angles_Z`, `is_Link_Child`, `last_Modified`)\n"
            "VALUES (0x72D3102B, 51669, 0x2D31003B, 188.051, 65.8611, 175.1155, -0.4930212, 0, 0, -0.8700173, False, '2019-02-10 00:00:00'); /* Rynthid Foundry */\n"
            "/* @teleloc 0x2D31003B [188.051000 65.861100 175.115500] -0.493021 0.000000 0.000000 -0.870017 */\n"
        )
        guid = pcap_helper.get_guid(command)
        self.assertEqual(guid, "0x72D3102B")

    def test_get_wcid(self):
        command = (
            "`landblock_instance` (`guid`, `weenie_Class_Id`, `obj_Cell_Id`, `origin_X`, `origin_Y`, `origin_Z`, `angles_W`, `angles_X`, `angles_Y`, `angles_Z`, `is_Link_Child`, `last_Modified`)\n"
            "VALUES (0x72D3102B, 51669, 0x2D31003B, 188.051, 65.8611, 175.1155, -0.4930212, 0, 0, -0.8700173, False, '2019-02-10 00:00:00'); /* Rynthid Foundry */\n"
            "/* @teleloc 0x2D31003B [188.051000 65.861100 175.115500] -0.493021 0.000000 0.000000 -0.870017 */\n"
        )
        wcid = pcap_helper.get_wcid(command)
        self.assertEqual(wcid, "51669")

    def test_get_name(self):
        command = (
            "`landblock_instance` (`guid`, `weenie_Class_Id`, `obj_Cell_Id`, `origin_X`, `origin_Y`, `origin_Z`, `angles_W`, `angles_X`, `angles_Y`, `angles_Z`, `is_Link_Child`, `last_Modified`)\n"
            "VALUES (0x72D3102B, 51669, 0x2D31003B, 188.051, 65.8611, 175.1155, -0.4930212, 0, 0, -0.8700173, False, '2019-02-10 00:00:00'); /* Rynthid Foundry */\n"
            "/* @teleloc 0x2D31003B [188.051000 65.861100 175.115500] -0.493021 0.000000 0.000000 -0.870017 */\n"
        )
        name = pcap_helper.get_name(command)
        self.assertEqual(name, "Rynthid Foundry")

    def test_get_cell_id(self):
        command = (
            "`landblock_instance` (`guid`, `weenie_Class_Id`, `obj_Cell_Id`, `origin_X`, `origin_Y`, `origin_Z`, `angles_W`, `angles_X`, `angles_Y`, `angles_Z`, `is_Link_Child`, `last_Modified`)\n"
            "VALUES (0x72D3102B, 51669, 0x2D31003B, 188.051, 65.8611, 175.1155, -0.4930212, 0, 0, -0.8700173, False, '2019-02-10 00:00:00'); /* Rynthid Foundry */\n"
            "/* @teleloc 0x2D31003B [188.051000 65.861100 175.115500] -0.493021 0.000000 0.000000 -0.870017 */\n"
        )
        name = pcap_helper.get_cell_id(command)
        self.assertEqual(name, "0x2D31003B")

    def test_get_origin_xyz(self):
        command = (
            "`landblock_instance` (`guid`, `weenie_Class_Id`, `obj_Cell_Id`, `origin_X`, `origin_Y`, `origin_Z`, `angles_W`, `angles_X`, `angles_Y`, `angles_Z`, `is_Link_Child`, `last_Modified`)\n"
            "VALUES (0x72D3102B, 51669, 0x2D31003B, 188.051, 65.8611, 175.1155, -0.4930212, 0, 0, -0.8700173, False, '2019-02-10 00:00:00'); /* Rynthid Foundry */\n"
            "/* @teleloc 0x2D31003B [188.051000 65.861100 175.115500] -0.493021 0.000000 0.000000 -0.870017 */\n"
        )
        origin = pcap_helper.get_origin_xyz(command)
        self.assertEqual(origin[0], 188.051)
        self.assertEqual(origin[1], 65.8611)
        self.assertEqual(origin[2], 175.1155)

    def test_get_angles_wxyz(self):
        command = (
            "`landblock_instance` (`guid`, `weenie_Class_Id`, `obj_Cell_Id`, `origin_X`, `origin_Y`, `origin_Z`, `angles_W`, `angles_X`, `angles_Y`, `angles_Z`, `is_Link_Child`, `last_Modified`)\n"
            "VALUES (0x72D3102B, 51669, 0x2D31003B, 188.051, 65.8611, 175.1155, -0.4930212, 0, 0, -0.8700173, False, '2019-02-10 00:00:00'); /* Rynthid Foundry */\n"
            "/* @teleloc 0x2D31003B [188.051000 65.861100 175.115500] -0.493021 0.000000 0.000000 -0.870017 */\n"
        )
        angles = pcap_helper.get_angles_wxyz(command)
        self.assertEqual(angles[0], -0.4930212)
        self.assertEqual(angles[1], 0)
        self.assertEqual(angles[2], 0)
        self.assertEqual(angles[3], -0.8700173)

    def test_get_is_link_child(self):
        command = (
            "`landblock_instance` (`guid`, `weenie_Class_Id`, `obj_Cell_Id`, `origin_X`, `origin_Y`, `origin_Z`, `angles_W`, `angles_X`, `angles_Y`, `angles_Z`, `is_Link_Child`, `last_Modified`)\n"
            "VALUES (0x72D3102B, 51669, 0x2D31003B, 188.051, 65.8611, 175.1155, -0.4930212, 0, 0, -0.8700173, False, '2019-02-10 00:00:00'); /* Rynthid Foundry */\n"
            "/* @teleloc 0x2D31003B [188.051000 65.861100 175.115500] -0.493021 0.000000 0.000000 -0.870017 */\n"
        )
        name = pcap_helper.get_is_link_child(command)
        self.assertEqual("False", name)

    def test_get_last_modified(self):
        command = (
            "`landblock_instance` (`guid`, `weenie_Class_Id`, `obj_Cell_Id`, `origin_X`, `origin_Y`, `origin_Z`, `angles_W`, `angles_X`, `angles_Y`, `angles_Z`, `is_Link_Child`, `last_Modified`)\n"
            "VALUES (0x72D3102B, 51669, 0x2D31003B, 188.051, 65.8611, 175.1155, -0.4930212, 0, 0, -0.8700173, False, '2019-02-10 00:00:00'); /* Rynthid Foundry */\n"
            "/* @teleloc 0x2D31003B [188.051000 65.861100 175.115500] -0.493021 0.000000 0.000000 -0.870017 */\n"
        )
        name = pcap_helper.get_last_modified(command)
        self.assertEqual("'2019-02-10 00:00:00'", name)
