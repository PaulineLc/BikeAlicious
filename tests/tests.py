from src import data_scrapping

def test_neatify_coord():
    test_string1 = "{[123.123,][}}}"
    test_string2 = "123.123,][}}}"
    test_string3 = "{[123.123"
    assert(data_scrapping.neatify_coord(test_string1) == 123.123)
    assert(data_scrapping.neatify_coord(test_string2) == 123.123)
    assert(data_scrapping.neatify_coord(test_string3) == 123.123)

test_neatify_coord()