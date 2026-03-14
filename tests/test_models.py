import unittest
from typing import cast

from pydantic import ValidationError

from models import Downtime, Folder, Host, HostTagGroup, Service, Tag


def make_host_data(**extensions):
    return {"id": "myhost", "extensions": extensions}


def make_service_data(**extensions):
    return {"id": "svc_1", "title": "CPU utilization", "extensions": extensions}


def make_downtime_data(**overrides):
    extensions = {
        "comment": "Maintenance",
        "host_name": "myhost",
        "is_service": "no",
        "author": "admin",
        "start_time": "2024-01-01T00:00:00Z",
        "end_time": "2024-01-02T00:00:00Z",
        "recurring": "no",
    }
    extensions.update(overrides)
    return {"id": "123", "title": "My Downtime", "extensions": extensions}


def make_folder_data():
    return {
        "title": "Linux Servers",
        "extensions": {
            "path": "/linux/servers",
            "attributes": {
                "meta_data": {
                    "created_at": "2024-01-01T00:00:00Z",
                    "updated_at": "2024-01-02T00:00:00Z",
                }
            },
        },
    }


# ---------------------------------------------------------------------------
# Host
# ---------------------------------------------------------------------------


class TestHostModel(unittest.TestCase):
    def test_minimal_host_is_parsed(self):
        host = Host.model_validate(make_host_data())
        self.assertEqual(host.name, "myhost")

    def test_host_state_zero_is_up(self):
        host = Host.model_validate(make_host_data(state=0))
        self.assertEqual(host.state, "up")

    def test_host_state_one_is_down(self):
        host = Host.model_validate(make_host_data(state=1))
        self.assertEqual(host.state, "down")

    def test_host_state_two_is_unreachable(self):
        host = Host.model_validate(make_host_data(state=2))
        self.assertEqual(host.state, "unreachable")

    def test_host_ip_address_is_mapped(self):
        host = Host.model_validate(make_host_data(address="192.168.1.1"))
        self.assertEqual(host.ip_address, "192.168.1.1")

    def test_host_alias_is_mapped(self):
        host = Host.model_validate(make_host_data(alias="My Server"))
        self.assertEqual(host.alias, "My Server")

    def test_host_num_services_is_mapped(self):
        host = Host.model_validate(make_host_data(num_services=5))
        self.assertEqual(host.number_services, 5)

    def test_host_num_services_crit_is_mapped(self):
        host = Host.model_validate(make_host_data(num_services_crit=2))
        self.assertEqual(host.number_services_critical, 2)

    def test_host_last_time_up_zero_returns_dash(self):
        host = Host.model_validate(make_host_data(last_time_up=0))
        self.assertEqual(host.last_time_up, "-")

    def test_host_last_time_up_with_timestamp_returns_string(self):
        host = Host.model_validate(make_host_data(last_time_up=1700000000))
        self.assertNotEqual(host.last_time_up, "-")
        self.assertIsInstance(host.last_time_up, str)

    def test_host_optional_fields_default_to_none(self):
        host = Host.model_validate(make_host_data())
        self.assertIsNone(host.ip_address)
        self.assertIsNone(host.alias)
        self.assertIsNone(host.state)

    def test_host_missing_id_raises(self):
        with self.assertRaises(ValidationError):
            Host.model_validate({"extensions": {}})


# ---------------------------------------------------------------------------
# Service
# ---------------------------------------------------------------------------


class TestServiceModel(unittest.TestCase):
    def test_minimal_service_is_parsed(self):
        service = Service.model_validate(make_service_data())
        self.assertEqual(service.id, "svc_1")
        self.assertEqual(service.title, "CPU utilization")

    def test_service_state_zero_is_ok(self):
        service = Service.model_validate(make_service_data(state=0))
        self.assertEqual(service.state, "ok")

    def test_service_state_two_is_critical(self):
        service = Service.model_validate(make_service_data(state=2))
        self.assertEqual(service.state, "critical")

    def test_service_description_is_mapped(self):
        service = Service.model_validate(make_service_data(description="CPU usage"))
        self.assertEqual(service.description, "CPU usage")

    def test_service_last_time_ok_zero_returns_dash(self):
        service = Service.model_validate(make_service_data(last_time_ok=0))
        self.assertEqual(service.last_time_ok, "-")

    def test_service_optional_fields_default_to_none(self):
        service = Service.model_validate(make_service_data())
        self.assertIsNone(service.state)
        self.assertIsNone(service.description)

    def test_service_missing_title_raises(self):
        with self.assertRaises(ValidationError):
            Service.model_validate({"id": "svc_1", "extensions": {}})


# ---------------------------------------------------------------------------
# Downtime
# ---------------------------------------------------------------------------


class TestDowntimeModel(unittest.TestCase):
    def test_downtime_is_parsed(self):
        downtime = Downtime.model_validate(make_downtime_data())
        self.assertEqual(downtime.id, "123")
        self.assertEqual(downtime.title, "My Downtime")
        self.assertEqual(downtime.host_name, "myhost")
        self.assertEqual(downtime.comment, "Maintenance")
        self.assertEqual(downtime.author, "admin")

    def test_downtime_is_service_field(self):
        downtime = Downtime.model_validate(make_downtime_data())
        self.assertEqual(downtime.is_service, "no")

    def test_downtime_missing_host_name_raises(self):
        data = {
            "id": "123",
            "title": "My Downtime",
            "extensions": {
                "comment": "Maintenance",
                "is_service": "no",
                "author": "admin",
                "start_time": "2024-01-01T00:00:00Z",
                "end_time": "2024-01-02T00:00:00Z",
                "recurring": "no",
            },
        }
        with self.assertRaises(ValidationError):
            Downtime.model_validate(data)


# ---------------------------------------------------------------------------
# Folder
# ---------------------------------------------------------------------------


class TestFolderModel(unittest.TestCase):
    def test_folder_is_parsed(self):
        folder = Folder.model_validate(make_folder_data())
        self.assertEqual(folder.name, "Linux Servers")
        self.assertEqual(folder.path, "/linux/servers")
        self.assertEqual(folder.created_at, "2024-01-01T00:00:00Z")
        self.assertEqual(folder.updated_at, "2024-01-02T00:00:00Z")

    def test_folder_name_comes_from_title(self):
        folder = Folder.model_validate(make_folder_data())
        self.assertEqual(folder.name, "Linux Servers")

    def test_folder_missing_path_raises(self):
        data = {
            "title": "Linux Servers",
            "extensions": {
                "attributes": {
                    "meta_data": {
                        "created_at": "2024-01-01T00:00:00Z",
                        "updated_at": "2024-01-02T00:00:00Z",
                    }
                }
            },
        }
        with self.assertRaises(ValidationError):
            Folder.model_validate(data)


# ---------------------------------------------------------------------------
# Tag
# ---------------------------------------------------------------------------


class TestTagModel(unittest.TestCase):
    def test_tag_is_parsed(self):
        tag = Tag.model_validate({"id": "prod", "title": "Production"})
        self.assertEqual(tag.name, "prod")
        self.assertEqual(tag.title, "Production")

    def test_tag_name_comes_from_id(self):
        tag = Tag.model_validate({"id": "dev", "title": "Development"})
        self.assertEqual(tag.name, "dev")

    def test_tag_missing_id_raises(self):
        with self.assertRaises(ValidationError):
            Tag.model_validate({"title": "Production"})


# ---------------------------------------------------------------------------
# HostTagGroup
# ---------------------------------------------------------------------------


class TestHostTagGroupModel(unittest.TestCase):
    def test_host_tag_group_is_parsed(self):
        data = {
            "id": "criticality",
            "title": "Criticality",
            "extensions": {
                "tags": [
                    {"id": "prod", "title": "Production"},
                    {"id": "test", "title": "Test"},
                ]
            },
        }
        group = HostTagGroup.model_validate(data)
        self.assertEqual(group.name, "criticality")
        self.assertEqual(group.title, "Criticality")
        self.assertEqual(len(group.tags), 2)
        self.assertEqual(group.tags[0].name, "prod")
        self.assertEqual(group.tags[1].name, "test")

    def test_host_tag_group_empty_tags(self):
        data = {
            "id": "criticality",
            "title": "Criticality",
            "extensions": {"tags": []},
        }
        group = HostTagGroup.model_validate(data)
        self.assertEqual(group.tags, [])

    def test_host_tag_group_missing_tags_raises(self):
        with self.assertRaises(ValidationError):
            HostTagGroup.model_validate(
                {
                    "id": "criticality",
                    "title": "Criticality",
                    "extensions": {},
                }
            )


if __name__ == "__main__":
    unittest.main()
