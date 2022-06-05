from ..scrap import format_one_sources_chunck_for_query


def test_format_sources_query_one_sources():
    l = ["account1"]
    s = format_one_sources_chunck_for_query(l)
    assert s == "from:account1"


def test_format_sources_query_several_sources():
    l = ["account1", "account2"]
    s = format_one_sources_chunck_for_query(l)
    assert s == "(from:account1, OR from:account2)"
