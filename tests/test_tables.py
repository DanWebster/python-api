import os
from random import randint
import time
from quilt import Connection
import pandas as pd


username = os.environ.get('QUILT_USERNAME')
url = os.environ.get('QUILT_URL')
conn = Connection(username=username, url=url)


def test_tables():
    """ Test tables. """
    results = conn.tables
    assert isinstance(results, list)


def test_search_tables():
    results = conn.search('term')
    assert isinstance(results, list)


def test_get_table_with_bad_ids():
    # with pytest.raises(TableNotFoundError):
    result = conn.get_table(10000000000)
    assert isinstance(result, type(None))  # hack
    result = conn.get_table('test string')
    assert isinstance(result, type(None))


def test_create_empty_table():
    t1 = conn.create_table(name='test', description='test empty')
    t2 = conn.get_table(t1.id)
    assert t1 == t2


def test_create_table_with_duplicate_attributes():
    t1 = conn.create_table(name='test', description='test empty')
    t2 = conn.create_table(name='test', description='test empty')
    assert t2.id == t1.id + 1
    assert t1.sqlname != t2.sqlname


def test_create_table_from_file():
    seed = str(randint(10000, 99999))
    test_name = 'test' + seed
    test_file = test_name + '.csv'
    data = 'col1,col2\n1,a\n2,b\n'
    with open(test_file, 'w') as f:
        f.write(data)
    test_description = 'test file ' + test_name
    t1 = conn.create_table(name=test_name, description=test_description,
                           inputfile=test_file)
    time.sleep(10)
    assert ['col1', 'col2'] == [col.name for col in t1.columns]
    fields = [col.field for col in t1.columns]
    rows = [row for row in t1]
    assert len(rows) == 2
    assert len(fields) == 2
    assert rows[0][fields[0]] == 1
    assert rows[0][fields[1]] == 'a'
    assert rows[1][fields[0]] == 2
    assert rows[1][fields[1]] == 'b'
    t2 = conn.get_table(t1.id)
    assert t1 == t2
    os.remove(test_file)


def test_create_table_from_df():
    cols = ['col1', 'col2']
    data = {1: 'a', 2: 'b'}
    df = pd.DataFrame(list(data.iteritems()), columns=cols)
    t1 = conn.save_df(df, name='testDataFrame', description="test")
    t2 = conn.get_table(t1.id)
    assert ['col1', 'col2'] == [col.name for col in t2.columns]
    fields = [col.field for col in t2.columns]
    rows = [row for row in t2]
    assert rows[0][fields[0]] == 1
    assert rows[0][fields[1]] == 'a'
    assert rows[1][fields[0]] == 2
    assert rows[1][fields[1]] == 'b'
