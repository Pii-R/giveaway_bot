from ..process import add_new_users_to_sources
import json


def test_add_one_user_to_sources(shared_datadir):
    list_new_mentionned_users = [783214]
    test_result = add_new_users_to_sources(
        list_new_mentionned_users, shared_datadir / "sources.json"
    )

    with open(shared_datadir / "sources.json", "r", encoding="utf-8") as sources_file:
        with open(
            shared_datadir / "expected_one_more_user_sources.json",
            "r",
            encoding="utf-8",
        ) as expected_sources_file:
            expected_result = json.load(expected_sources_file)
            result = json.load(sources_file)
            assert result == expected_result


def test_add_one_user_already_in_sources(shared_datadir):
    list_new_mentionned_users = [106355755, 1225440114832281600]
    test_result = add_new_users_to_sources(
        list_new_mentionned_users, shared_datadir / "sources.json"
    )

    with open(shared_datadir / "sources.json", "r", encoding="utf-8") as sources_file:
        with open(
            shared_datadir / "expected_no_duplicate_sources.json",
            "r",
            encoding="utf-8",
        ) as expected_sources_file:
            expected_result = json.load(expected_sources_file)
            result = json.load(sources_file)
            assert result == expected_result


def test_add_no_user_to_sources(shared_datadir):
    list_new_mentionned_users = []
    test_result = add_new_users_to_sources(
        list_new_mentionned_users, shared_datadir / "sources.json"
    )

    with open(shared_datadir / "sources.json", "r", encoding="utf-8") as sources_file:
        with open(
            shared_datadir / "expected_no_more_user_sources.json", "r", encoding="utf-8"
        ) as expected_sources_file:
            expected_result = json.load(expected_sources_file)
            result = json.load(sources_file)
            assert result == expected_result
