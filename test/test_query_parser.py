import pytest

from investmentcatbot.bot_engine.query_parser import get_numeric_part

def test_null_numeric_parse():
    query = "This has no numeric parts"
    (number, remaining_query) = get_numeric_part(query)
    assert number == None
    assert remaining_query == query

def test_simple_numeric_parse():
    query = "add valuation 123000000000 for GS"
    (number, remaining_query) = get_numeric_part(query)
    assert number == "123000000000"
    assert remaining_query == "add valuation  for GS"

def test_billion_encoded_numeric_parse():
    query = "add valuation 123B for GS"
    (number, remaining_query) = get_numeric_part(query)
    assert number == "123000000000"
    assert remaining_query == "add valuation  for GS"

def test_billion_encoded_numeric_parse():
    query = "add valuation 876M for IRBT"
    (number, remaining_query) = get_numeric_part(query)
    assert number == "876000000"
    assert remaining_query == "add valuation  for IRBT"
