from ..scrap import (
    export_sources_accounts,
    divide_source_accounts_into_chunks,
)


def test_divide_source_accounts_into_chunks_with_zero_account(shared_datadir):
    sources_file = shared_datadir / "zero_sources.json"
    sources_accounts = export_sources_accounts(sources_file)
    chunks = divide_source_accounts_into_chunks(sources_accounts, 1)
    assert len(chunks) == 0
    assert chunks == []


def test_divide_source_accounts_into_chunks_with_one_account(shared_datadir):
    sources_file = shared_datadir / "one_sources.json"
    sources_accounts = export_sources_accounts(sources_file)
    chunks = divide_source_accounts_into_chunks(sources_accounts, 1)
    assert len(chunks) == 1
    assert chunks == [["account1"]]


def test_divide_source_accounts_into_chunks_with_several_account(shared_datadir):
    sources_file = shared_datadir / "several_sources.json"
    sources_accounts = export_sources_accounts(sources_file)
    chunks = divide_source_accounts_into_chunks(sources_accounts, 10)
    assert len(chunks) == 2
    assert chunks == [
        [
            "account1",
            "account2",
            "account3",
            "account4",
            "account5",
            "account6",
            "account7",
            "account8",
            "account9",
            "account10",
        ],
        ["account11"],
    ]
