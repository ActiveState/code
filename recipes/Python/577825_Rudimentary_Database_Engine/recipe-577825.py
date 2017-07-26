"""Module written to learn and understand more about databases.

The code in this module provides support for running a simple database engine
that runs completely in memory and allows usage of various concepts available
in a structured query language to get and set data that may be saved to file."""

################################################################################

import bz2
import copy
import datetime
import decimal
import pickle
import re
import sys
import types
import _thread

################################################################################

def _slots(names=''):
    "Returns the private version of names for __slots__ on a class."
    return tuple('__' + name for name in names.split())

################################################################################

class Database:

    "Database() -> Database"

    @classmethod
    def load(cls, path):
        "Loads database from path and tests identity."
        with open(path, 'rb') as file:
            obj = pickle.loads(bz2.decompress(file.read()))
        assert isinstance(obj, cls), 'Could not load a database object!'
        obj.__path = path
        return obj

    ########################################################################

    __slots__ = _slots('path data type view')

    def __init__(self):
        "Initializes database object void of tables or views."
        self.__path = None
        self.__setstate__(Table(('name', str),
                                ('type', type),
                                ('data', (Table, _View))))

    def __repr__(self):
        "Returns the representation of the database."
        return repr(self.__view.value)

    def __iter__(self):
        "Iterates over the names of the tables and views in the database."
        for row in rows(self.__data('name')):
            yield self[row[0]]

    def __getattr__(self, name):
        "Allows getting table or view via attribute lookup or index notation."
        t = tuple(self.__data.where(ROW.name == name)('data'))
        assert len(t) < 3, 'Name is ambiguous!'
        assert len(t) > 1, 'Object was not found!'
        data = t[1][0]
        if isinstance(data, _View):
            return data.value
        return data

    __getitem__ = __getattr__

    def __getstate__(self):
        "Provides support for pickling and saving the database."
        return self.__data

    def __setstate__(self, state):
        "Helps with unpickling and adding needed instance variables."
        self.__data = state
        self.__type = Table(('type', type), ('name', str))
        self.__type.insert(Table, 'table')
        self.__type.insert(_View, 'view')
        self.__view = _View(None, lambda _: self.__data.left_join(self.__type, \
            'Types', ROW.type == ROW.Types.type) \
            .select('name', 'Types.name', (lambda obj: \
            float(len(obj) if isinstance(obj, Table) else 'nan'), 'data')),
            ('Types.name', 'type'), ('<lambda>(data)', 'size'))

    ########################################################################

    def save(self, path=None):
        "Saves the database to path or most recently known path."
        if path is None:
            assert self.__path is not None, 'Path must be provided!'
            path = self.__path
        with open(path, 'wb') as file:
            file.write(bz2.compress(pickle.dumps(self)))
        self.__path = path

    def create(self, name, schema_or_table_or_query, *name_changes):
        "Creates either a table or view for use in the database."
        assert not self.__data.where(ROW.name == name), \
               'Name is already used and may not be overloaded!'
        if isinstance(schema_or_table_or_query, (tuple, list)):
            assert not name_changes, 'Name changes not allowed with schema!'
            data = Table(*schema_or_table_or_query)
        elif isinstance(schema_or_table_or_query, Table):
            assert not name_changes, 'Name changes not allowed with table!'
            data = schema_or_table_or_query
        else:
            data = _View(self, schema_or_table_or_query, *name_changes)
        self.__data.insert(name=name, type=type(data), data=data)
        return data

    def drop(self, name):
        "Deletes a table or view from the database."
        self.__data.delete(ROW.name == name)

    def print(self, end='\n\n', file=None):
        "Provides a simple way of showing a representation of the database."
        self.__view.value.print(end, file)

    def create_or_replace(self, name, schema_or_table_or_query, *name_changes):
        "Drops table or view before creating one with the same name."
        self.drop(name)
        self.create(name, schema_or_table_or_query, *name_changes)

    def inner_join(self, table_a, table_b, test):
        "Inner joins tables and views by name using test."
        return inner_join(test, **{table_a: self[table_a],
                                   table_b: self[table_b]})

    def full_join(self, table_a, table_b, test):
        "Full joins tables and views by name using test."
        return full_join(test, **{table_a: self[table_a],
                                  table_b: self[table_b]})

################################################################################

class Database2(Database):

    "Database2() -> Database2"

    @classmethod
    def upgrade(cls, db_old):
        "Upgrades the base version of a database into the child version."
        assert isinstance(db_old, cls.__base__), \
            'Can only upgrade Database objects!'
        db_new = cls()
        db_new.__setstate__(db_old.__getstate__())
        db_new.save(db_old._Database__path)
        db_old.__init__()
        return db_new

    ########################################################################

    __slots__ = _slots('lock locked view')

    def __repr__(self):
        "Returns an updated representation of the database."
        return repr(self.__view.value)

    def __setstate__(self, state):
        "Sets up remaining attributes and prepares for transactions."
        super().__setstate__(state)
        self.__add_transaction_support()

    def __getstate__(self):
        "Reduces internal table to required columns and returns copy."
        self.__del_transaction_support()
        data = self.__data.copy()
        self.__extend_data()
        return data

    def __getattr__(self, name):
        "Allows contents to be accessed only if not in transaction."
        table = self.__data.where(name=name)
        assert len(table) < 2, 'Name is abmiguous!'
        assert len(table) > 0, 'Object was not found!'
        assert not table.first('lock').locked, 'A transaction is in place!'
        if table.first('type') is _View:
            return table.first('data').value
        return table.first('data')

    __getitem__ = __getattr__

    ########################################################################

    def begin_transaction(self, table, wait=False):
        "Locks and copies table while optionally waiting for unlock."
        table = self.__data.where(name=table)
        assert table.first('type') is not _View, 'Views are not supported!'
        lock = table.first('lock')
        if wait:
            lock.acquire()
            with self.__lock:   # Protects Critical Section
                data = table.first('data')
                table.update(copy=copy.deepcopy(data))
        else:
            with self.__lock:
                assert lock.acquire(False), 'Table is locked in a transaction!'
                data = table.first('data')
                table.update(copy=copy.deepcopy(data))
        return data

    def commit_transaction(self, table):
        "Deletes reserve copy and unlocks the table."
        self.__close_transaction(table, self.__commit)

    def rollback_transaction(self, table):
        "Restores table with copy, removes copy, and unlocks the table."
        self.__close_transaction(table, self.__rollback)

    ######################################################################## 

    def __add_transaction_support(self):
        "Add attributes so database can support transactions."
        self.__lock = _thread.allocate_lock()
        self.__extend_data()
        self.__locked = _View(None, lambda _: self.__data \
            .select('name', (lambda lock: lock.locked, 'lock')) \
            .as_(('<lambda>(lock)', 'locked')))
        self.__view = _View(None, lambda _: self._Database__view.value \
            .left_join(self.__locked.value, 'Lock', ROW.name == ROW.Lock.name) \
            .select('name', 'type', 'size', 'Lock.locked'), \
            ('Lock.locked', 'locked'))

    def __extend_data(self):
        "Adds columns to internal table as necessary."
        if ('type', type) not in self.__data.schema:
            self.__data.alter_add('type', type)
            for name, data in rows(self.__data('name', 'data')):
                self.__data.where(name=name).update(type=type(data))
        self.__data.alter_add('lock', _Lock)
        self.__data.alter_add('copy', object)

    def __del_transaction_support(self):
        "Ensures no pending transactions and removes unsaved columns."
        assert not self.__locked.value.where(locked=True), \
            'You must commit all transactions before pickling!'
        self.__data.alter_drop('type')
        self.__data.alter_drop('lock')
        self.__data.alter_drop('copy')

    def __close_transaction(self, table, action):
        "Finishes taking care of a transaction's end."
        table = self.__data.where(name=table)
        assert table.first('type') is not _View, 'Views are not supported!'
        lock = table.first('lock')
        # Begin Critical Section
        with self.__lock:
            try:
                lock.release()
            except _thread.error:
                raise ValueError('Table was not in a transaction!')
            action(table)
        # End Critical Section

    ########################################################################

    @staticmethod
    def __commit(table):
        "Deletes the reserve copy of a table."
        table.update(copy=object())

    @staticmethod
    def __rollback(table):
        "Restores table from copy and deletes the copy."
        table.update(data=table.first('copy'), copy=object())

    ########################################################################

    @property
    def __data(self):
        "Aliases internal table from Database class."
        return self._Database__data

################################################################################

class _Lock:

    "_Lock(immediate=False, silent=False) -> _Lock"

    __slots__ = _slots('lock verbose')

    def __init__(self, immediate=False, silent=False):
        "Initializes _Lock instance with internal mechanism."
        self.__lock = _thread.allocate_lock()
        self.__verbose = silent
        if immediate:
            self.acquire()

    ########################################################################

    def acquire(self, wait=True):
        "Acquires lock with an optional wait."
        return self.__lock.acquire(wait)

    def release(self, exc_type=None, exc_value=None, traceback=None):
        "Release lock if locked or possibly throws error."
        try:
            self.__lock.release()
        except _thread.error:
            if self.__verbose:
                raise

    ########################################################################

    __enter__ = acquire

    __exit__ = release

    ########################################################################

    @property
    def locked(self):
        "Returns whether or not lock is currently locked."
        return self.__lock.locked()

################################################################################

class Table:

    "Table(*columns) -> Table"

    @classmethod
    def from_iter(cls, iterator):
        "Generates a table from a column / rows iterator."
        title, test_row, *rows = iterator
        table = cls(*zip(title, map(type, test_row)))
        table.insert(*test_row)
        for row in rows:
            table.insert(*row)
        return table

    ########################################################################

    __slots__ = _slots('columns data_area row_index')

    def __init__(self, *columns):
        "Initializes Table with columns and row storage area."
        self.__columns = _Columns(columns)
        self.__data_area = {}
        self.__row_index = 1

    def __len__(self):
        "Returns the number of rows in the table."
        return len(self.__data_area)

    def __repr__(self):
        "Creates a complete representation of the table."
        buffer = [list(map(repr, ['ROW_ID'] + [name for index, name, data_type \
                                               in self.__columns]))]
        width = [0] * len(buffer[0])
        for row in sorted(self.__data_area):
            buffer.append(list(map(repr, [row] + [self.__data_area[row][index] \
                                                  for index, name, data_type \
                                                  in self.__columns])))
        for row in buffer:
            for index, string in enumerate(row):
                width[index] = max(width[index], len(string))
        string = ''
        for index, value in enumerate(buffer[0]):
            string += value.ljust(width[index]) + ' | '
        string = string[:-3] + '\n'
        for index in range(len(buffer[0])):
            string += '-' * width[index] + '-+-'
        string = string[:-3] + '\n'
        for row in buffer[1:]:
            for index, value in enumerate(row):
                string += value.ljust(width[index]) + ' | '
            string = string[:-3] + '\n'
        return string[:-1]

    def __str__(self):
        names, *rows = self
        columns = {name: [] for name in names}
        for row in rows:
            for key, value in zip(names, row):
                columns[key].append(value)
        lengths = tuple(max(len(str(value)) for value in columns[key] + [key])
                       for key in names)
        template = ' '.join(map('{{:{}}}'.format, lengths))
        lines = [template.format(*map(str.upper, names)),
                 ' '.join(map('-'.__mul__, lengths))]
        for row in zip(*map(columns.__getitem__, names)):
            lines.append(template.format(*row))
        return '\n'.join(lines)

    def __iter__(self):
        "Returns an iterator over the table's columns."
        return self(*self.columns)

    def __call__(self, *columns):
        "Returns an iterator over the specified columns."
        indexs = tuple(self.__columns[name][1] for name in columns)
        yield columns
        for row in sorted(self.__data_area):
            yield tuple(self.__data_area[row][index] for index in indexs)

    ########################################################################

    def first(self, column=None):
        "Returns the first row or column of specified row."
        return self.__get_location(min, column)

    def last(self, column=None):
        "Returns the last row or column of specified row."
        return self.__get_location(max, column)

    def print(self, end='\n\n', file=None):
        "Provides a convenient way of printing representation of the table."
        print(repr(self), end=end, file=sys.stdout if file is None else file)

    def top(self, amount):
        "Iterates over the top rows specified by amount."
        if amount == -1:
            amount = len(self.__data_area)
        elif 0 <= amount < 1:
            amount = round(amount * len(self.__data_area))
        assert isinstance(amount, int), 'Amount was not understood!'
        for row, count in zip(self, range(amount + 1)):
            yield row

    def insert(self, *values, **columns):
        "Inserts provided data into a new row of the database."
        if values:
            assert len(values) == len(self.__columns), 'Bad number of columns!'
            assert not columns, 'Mixed syntax is not accepted!'
            row = self.__insert_across(values)
        else:
            assert columns, 'There is nothing to insert!'
            row = self.__insert_select(columns)
        self.__data_area[self.__row_index] = row
        self.__row_index += 1

    def alter_add(self, name, data_type):
        "Adds a column to the table and populates it."
        index = self.__columns.add(name, data_type)
        started = False
        try:
            for row in self.__data_area.values():
                row[index] = data_type()
                started = True
        except TypeError:
            if started:
                raise
            for row in self.__data_area.values():
                row[index] = data_type

    def alter_drop(self, name):
        "Removes a column from the table and frees memory."
        index = self.__columns.drop(name)
        for row in self.__data_area.values():
            del row[index]

    def alter_column(self, name, data_type):
        "Changes the data-type of a column and refreshes it."
        index = self.__columns.alter(name, data_type)
        for row in self.__data_area.values():
            row[index] = data_type()

    def alter_name(self, old, new):
        "Renames a column without altering the rows."
        self.__columns.rename(old, new)

    def as_(self, *pairs):
        "Changes the name of multiple columns at a time."
        for old, new in pairs:
            self.alter_name(old, new)
        return self

    def copy(self):
        "Copies a table while sharing cell instances."
        copy = type(self)()
        copy.__columns = self.__columns.copy()
        copy.__data_area = {}
        for key, value in self.__data_area.items():
            copy.__data_area[key] = value.copy()
        copy.__row_index = self.__row_index
        return copy

    def select(self, *column_names):
        "Select columns and process them with any given functions."
        if not column_names:
            return self
        columns, functions = [], []
        for item in column_names:
            if isinstance(item, str):
                columns.append(item)
            elif isinstance(item, tuple):
                functions.append(item)
            else:
                raise TypeError(type(item))
        original = {name for index, name, data_type in self.__columns}
        excess = original - set(columns)
        if functions:
            return self.__select_with_function(excess, functions)
        copy = type(self)()
        copy.__columns = self.__columns.copy()
        copy.__data_area = self.__data_area
        copy.__row_index = self.__row_index
        for column in excess:
            copy.__columns.drop(column)
        return copy

    def distinct(self):
        "Return copy of table having only distinct rows."
        copy = type(self)()
        copy.__columns = self.__columns
        copy.__data_area = self.__data_area.copy()
        copy.__row_index = self.__row_index
        valid_indexs = set()
        distinct_rows = set()
        for row in copy.__data_area:
            array = pickle.dumps(tuple(copy.__data_area[row][index] \
                                       for index, name, data_type \
                                       in self.__columns))
            if array not in distinct_rows:
                valid_indexs.add(row)
                distinct_rows.add(array)
        for row in tuple(copy.__data_area):
            if row not in valid_indexs:
                del copy.__data_area[row]
        return copy

    def update(self, **assignments):
        "Changes all present rows with given assignments."
        assign = []
        for name, value in assignments.items():
            data_type, index = self.__columns[name]
            assert isinstance(value, data_type), \
            'Wrong datatype: {} ({!r}, {!r})'.format(name, value, data_type)
            assign.append((index, value))
        for row in self.__data_area.values():
            for index, value in assign:
                row[index] = value

    def where(self, test='and', **kw):
        "Select rows that fit criteria given by the test."
        test = self.__process_test(test, kw)
        copy = type(self)()
        copy.__columns = self.__columns
        copy.__data_area = self.__data_area.copy()
        copy.__row_index = self.__row_index
        self.__remove(copy.__data_area, False, test)
        return copy

    def delete(self, test='and', **kw):
        "Delete rows that fit criteria given by the test."
        test = self.__process_test(test, kw)
        self.__remove(self.__data_area, True, test)
        return self

    def truncate(self):
        "Deletes all of the rows in the table."
        self.__data_area.clear()
        return self

    def order_by(self, column, desc=False):
        "Returns a sorted result of the table."
        return _SortedResults(self, column, desc)

    def into(self, table):
        "Inserts external table into this table by column name."
        self_iter = iter(self)
        self_colu = next(self_iter)
        for row in self_iter:
            table.insert(**{name: data for name, data in zip(self_colu, row)})

    def left_join(self, table, name, test):
        "Returns result of a left join on the given table using test."
        return left_join(self, (table, name), test)

    def sum_(self, column):
        "Adds up all of the cells in a particular column of the table."
        data_type, index = self.__columns[column]
        total = data_type()
        for row in self.__data_area:
            total += self.__data_area[row][index]
        return total

    def avg(self, column):
        "Averages the cells in the given column of the table."
        size = len(self.__data_area)
        return self.sum_(column) / size if size else size

    def max_(self, column):
        "Finds the largest cell value from the column in the table."
        index = self.__columns[column][1]
        return max(map(ROW[index], self.__data_area.values()))

    def min_(self, column):
        "Finds the smallest cell value from the column in the table."
        index = self.__columns[column][1]
        return min(map(ROW[index], self.__data_area.values()))

    def count(self, column=None):
        "Counts the total number of 'non-null' cells in the given column."
        if column is None:
            return len(self.__data_area)
        data_type, index = self.__columns[column]
        null, total = data_type(), 0
        for row in self.__data_area.values():
            if row[index] != null:
                total += 1
        return total

    def group_by(self, *columns):
        "Creates new tables from this table on matching columns."
        column_map = {name: index for index, name, data_type in self.__columns}
        index_list = tuple(sorted(column_map.values()))
        schema = list(self.schema)
        tables = {}
        first = True
        for row_dict in self.__data_area.values():
            interest = []
            row = list(row_dict[index] for index in index_list)
            for name in columns:
                if isinstance(name, str):
                    interest.append(row_dict[column_map[name]])
                else:
                    interest.append(name(_RowAdapter(row_dict, column_map)))
                    name = name.name
                    if name is not None:
                        data = interest[-1]
                        row.append(data)
                        if first:
                            signature = name, type(data)
                            if signature not in schema:
                                schema.append(signature)
            first = False
            key = tuple(interest)
            if key not in tables:
                tables[key] = type(self)(*schema)
            tables[key].insert(*row)
        return tables.values()

    ########################################################################

    def __get_location(self, function, column):
        "Returns a row or cell based on function and column."
        row = self.__data_area[function(self.__data_area)]
        if column is None:
            return tuple(row[index] for index in sorted(row))
        return row[self.__columns[column][1]]

    def __insert_across(self, values):
        "Inserts values into new row while checking data types."
        row = {}
        for value, (index, name, data_type) in zip(values, self.__columns):
            assert isinstance(value, data_type), \
                'Wrong datatype: {} ({!r}, {!r})'.format(name, value, data_type)
            row[index] = value
        return row

    def __insert_select(self, values):
        "Inserts values into new row and fills in blank cells."
        row = {}
        for name, value in values.items():
            data_type, index = self.__columns[name]
            assert isinstance(value, data_type), \
            'Wrong datatype: {} ({!r}, {!r})'.format(name, value, data_type)
            row[index] = value
        for index, name, data_type in self.__columns:
            if index not in row:
                row[index] = data_type()
        return row

    def __remove(self, data_area, delete, test):
        "Removes rows from data area according to criteria."
        column_map = {name: index for index, name, data_type in self.__columns}
        for row in tuple(data_area):
            value = test(_RowAdapter(data_area[row], column_map))
            assert not isinstance(value, _RowAdapter), 'Test improperly formed!'
            if bool(value) == delete:
                del data_area[row]

    def __select_with_function(self, excess, functions):
        "Creates virtual rows formed by calling functions on columns."
        table = self.copy()
        for code, data in functions:
            if data in table.__columns:
                data_name = '{}({})'.format(code.__name__, data)
                data_type = type(code(next(rows(table(data)))[0]))
                table.alter_add(data_name, data_type)
                dest = table.__columns[data_name][1]
                sour = table.__columns[data][1]
                for row in table.__data_area.values():
                    row[dest] = code(row[sour])
            else:
                sour = code()
                table.alter_add(data, type(sour))
                dest = table.__columns[data][1]
                for row in table.__data_area.values():
                    row[dest] = copy.deepcopy(sour)
        for column in excess:
            table.alter_drop(column)
        return table

    ########################################################################

    @staticmethod
    def __process_test(test, kw):
        "Ensures that test has been properly formed as necessary."
        if kw:
            test = _Where(test, kw)
        else:
            assert callable(test), 'Test must be callable!'
        return test

    ########################################################################

    @property
    def columns(self):
        "Returns a list of column names from the table."
        columns = sorted(self.__columns, key=lambda info: info[0])
        return tuple(map(lambda info: info[1], columns))

    @property
    def schema(self):
        "Returns table's schema that can be used to create another table."
        return tuple((name, self.__columns[name][0]) for name in self.columns)

################################################################################

class _Columns:

    "_Columns(columns) -> _Columns"

    __slots__ = _slots('column_index column_names')

    def __init__(self, columns):
        "Initializes Columns instance with names and data types."
        self.__column_index = 1
        self.__column_names = UniqueDict()
        for name, data_type in columns:
            self.add(name, data_type)

    def __contains__(self, name):
        "Checks if the named column already exists."
        return name in self.__column_names

    def __len__(self):
        "Returns the number of columns recognizes."
        return len(self.__column_names)

    def __iter__(self):
        "Iterates over columns in sorted order."
        cache = []
        for name, (data_type, index) in self.__column_names.items():
            cache.append((index, name, data_type))
        for item in sorted(cache):
            yield item

    def __getitem__(self, name):
        "Returns requested information on the given column name."
        return self.__column_names[name]

    def __getstate__(self):
        "Provides support for class instances to be pickled."
        return self.__column_index, self.__column_names

    def __setstate__(self, state):
        "Sets the state while object in being unpickled."
        self.__column_index, self.__column_names = state

    ########################################################################

    def copy(self):
        "Creates a copy of the known columns."
        copy = type(self)([])
        copy.__column_index = self.__column_index
        copy.__column_names = self.__column_names.copy()
        return copy

    def add(self, name, data_type):
        "Adds a column name with data type and assigns an index."
        index = self.__column_index
        self.__column_names[name] = data_type, index
        self.__column_index += 1
        return index

    def drop(self, name):
        "Removes all information regarding the named column."
        index = self.__column_names[name][1]
        del self.__column_names[name]
        return index

    def alter(self, name, data_type):
        "Changes the data type of the named column."
        index = self.__column_names[name][1]
        self.__column_names.replace(name, (data_type, index))
        return index

    def rename(self, old, new):
        "Renames a column from old name to new name."
        self.__column_names[new] = self.__column_names[old]
        del self.__column_names[old]

################################################################################

class UniqueDict(dict):

    "UniqueDict(iterable=None, **kwargs) -> UniqueDict"

    __slots__ = ()

    def __setitem__(self, key, value):
        "Sets key with value if key does not exist."
        assert key not in self, 'Key already exists!'
        super().__setitem__(key, value)

    def replace(self, key, value):
        "Sets key with value if key already exists."
        assert key in self, 'Key does not exist!'
        super().__setitem__(key, value)

################################################################################

class _RowAdapter:

    "_RowAdapter(row, column_map=None) -> _RowAdapter"

    __slots__ = _slots('row map')

    def __init__(self, row, column_map=None):
        "Initializes _RowAdapter with data and mapping information."
        self.__row = row
        self.__map = column_map

    def __getattr__(self, column):
        "Returns a column from the row this instance in adapting."
        if self.__map is None:
            return self.__unmapped(column)
        if column in self.__map:
            return self.__row[self.__map[column]]
        new_map = {}
        column += '.'
        for name in self.__map:
            if name.startswith(column):
                new_map[name[len(column):]] = self.__map[name]
        assert new_map, 'Name did not match any known column: ' + repr(column)
        return type(self)(self.__row, new_map)

    __getitem__ = __getattr__

    ########################################################################

    def __unmapped(self, column):
        "Processes a row with column names already filled in."
        if column in self.__row:
            return self.__row[column]
        row = {}
        column += '.'
        for name in self.__row:
            if name.startswith(column):
                row[name[len(column):]] = self.__row[name]
        assert row, 'Name did not match any known column: ' + repr(column)
        return type(self)(row)

################################################################################

class _SortedResults:

    "_SortedResults(iterable column, desc) -> _SortedResults"

    __slots__ = _slots('iter column direction')

    def __init__(self, iterable, column, desc):
        "Initializes sorting adapter with given data."
        self.__iter = iterable
        self.__column = column
        self.__direction = desc

    def __iter__(self):
        "Iterates over internal data in the order requested."
        title, *rows = tuple(self.__iter)
        index = title.index(self.__column)
        yield title
        for row in sorted(rows, key=ROW[index], reverse=self.__direction):
            yield row

    ########################################################################

    def order_by(self, column, desc=False):
        "Returns results that are sorted on an additional level."
        return type(self)(self, column, desc)

    def table(self):
        "Converts the sorted results into a table object."
        return Table.from_iter(self)

################################################################################

class _View:

    "_View(database, query, *name_changes) -> _View"

    __slots__ = _slots('database query name_changes')

    def __init__(self, database, query, *name_changes):
        "Initializes _View instance with details of saved query."
        self.__database = database
        self.__query = query
        self.__name_changes = name_changes
    
    def __getstate__(self):
        "Returns everything needed to pickle _View instance."
        return self.__database, self.__query.__code__, self.__name_changes

    def __setstate__(self, state):
        "Sets the state of the _View instance when unpickled."
        database, query, name_changes = state
        self.__database = database
        self.__query = types.LambdaType(query, sys.modules, '', (), ())
        self.__name_changes = name_changes

    ########################################################################

    @property
    def value(self):
        "Caculates and returns the value of view's query."
        data = self.__query(self.__database)
        table = data if isinstance(data, Table) else Table.from_iter(data)
        for old, new in self.__name_changes:
            table.alter_name(old, new)
        return table

################################################################################

class _Where:

    "_Where(mode, condition) -> _Where"

    __slots__ = _slots('call rows')

    def __init__(self, mode, condition):
        "Initializes _Where support object for simple selections."
        self.__call = {'and': all, 'or': any}[mode]
        self.__rows = condition

    def __call__(self, row):
        "Runs test on given row and validates against condition."
        return self.__call(row[k] == v for k, v in self.__rows.items())

################################################################################

class NotLike:

    "NotLike(column, pattern, flags=IGNORECASE, advanced=False) -> NotLike"

    __slots__ = _slots('column method')

    def __init__(self, column, pattern, flags=re.IGNORECASE, advanced=False):
        "Initializes comparison object for specified column."
        self.__column = column
        if not advanced:
            pattern = '^' + pattern + '$'
        self.__method = re.compile(pattern, flags).search

    def __call__(self, row):
        "Tests if column in row was like the given pattern."
        return self.__method(row[self.__column]) is None

################################################################################

class Like(NotLike):

    "Like(column, pattern, flags=IGNORECASE, advanced=False) -> Like"

    __slots__ = _slots()

    def __call__(self, row):
        "Reverses the result from calling a NotLike instance."
        return not super().__call__(row)

################################################################################

class date(datetime.date):

    "date(year=None, month=None, day=None) -> date"

    __slots__ = _slots()

    def __new__(cls, year=None, month=None, day=None):
        "Creates a customized date object that does not require arguments."
        if year is None:
            year, month, day = cls.max.year, cls.max.month, cls.max.day
        elif isinstance(year, bytes):
            year_high, year_low, month, day = year
            year = (year_high << 8) + year_low
        return super().__new__(cls, year, month, day)

    def __str__(self):
        return self.strftime('%d-%b-%Y').upper()

    def __format__(self, length):
        return str(self).ljust(int(length))

################################################################################

class datetime(datetime.datetime):

    """datetime(year=None, month=None, day=None, hour=0,
         minute=0, second=0, microsecond=0, tzinfo=None) -> datetime"""

    __slots__ = _slots()

    def __new__(cls, year=None, month=None, day=None, hour=0,
                minute=0, second=0, microsecond=0, tzinfo=None):
        "Creates a customized datetime object that does not require arguments."
        if year is None:
            year, month, day = cls.max.year, cls.max.month, cls.max.day
        elif isinstance(year, bytes):
            year_high, year_low, _month, day, \
            hour, minute, second, a, b, c = year
            year = (year_high << 8) + year_low
            microsecond = (((a << 8) | b) << 8) | c
            if month is None or isinstance(month, datetime._tzinfo_class):
                tzinfo = month
            else:
                raise TypeError('bad tzinfo state arg {!r}'.format(month))
            month = _month
        return super().__new__(cls, year, month, day, hour,
                               minute, second, microsecond, tzinfo)

    def date(self):
        d = super().date()
        return date(d.year, d.month, d.day)

################################################################################

class _NamedInstance:

    "_NamedInstance(*args, **kwargs) -> _NamedInstance"

    __slots__ = _slots()

    def __init__(self, *args, **kwargs):
        "Raises an error since this is an abstract class."
        raise NotImplementedError('This is an abstract class!')

    @property
    def __name__(self):
        "Provides a way for callable instances to be identified."
        return type(self).__name__

################################################################################

class DatePart(_NamedInstance):

    "DatePart(part, column, name=None) -> DatePart"

    __slots__ = _slots('part column name')

    def __init__(self, part, column, name=None):
        "Initializes DatePart instance usable with 'group_by' method."
        self.__part = part.upper()
        self.__column = column
        self.__name = name

    def __call__(self, row):
        "Extract specified part of date from column in row."
        date = row[self.__column]
        if self.__part == 'Y':
            return date.year
        if self.__part == 'Q':
            return (date.month - 1) // 3 + 1
        if self.__part == 'M':
            return date.month
        if self.__part == 'D':
            return date.month
        raise ValueError('DatePart code cannot be processed!')

    ########################################################################

    @property
    def name(self):
        "Provides a name for us in the 'group_by' method."
        return self.__name

################################################################################

class MID(_NamedInstance):

    "MID(start, length=None) -> MID"

    __slots__ = _slots('start stop')

    def __init__(self, start, length=None):
        "Intializes MID instance with data to extract a sub-interval."
        self.__start = start - 1
        self.__stop = None if length is None else self.__start + length

    def __call__(self, data):
        "Returns sub-internal as specified upon instantiation."
        if self.__stop is None:
            return data[self.__start:]
        return data[self.__start:self.__stop]

################################################################################

class FORMAT(_NamedInstance):

    "FORMAT(spec) -> FORMAT"

    __slots__ = _slots('spec')

    def __init__(self, spec):
        "Initializes instance with 'spec' for the format function."
        self.__spec = spec

    def __call__(self, data):
        "Returns result from format function based on data and spec."
        return format(data, self.__spec)

################################################################################

del _slots
types.StringType = str
next_ = next
NOW = datetime.now

################################################################################

def inner_join(test, *table_arg, **table_kwarg):
    "Runs and returns result from inner joining two tables together."
    pa, pb, ta, tb = _join_args(table_arg, table_kwarg)
    table = _composite_table(pa, pb, ta, tb)
    _join_loop(table, test, pa, pb, ta, tb, True, False)
    return table

def full_join(test, *table_arg, **table_kwarg):
    "Runs and returns result from full joining two tables together."
    pa, pb, ta, tb = _join_args(table_arg, table_kwarg)
    table = _composite_table(pa, pb, ta, tb)
    _join_loop(table, test, pa, pb, ta, tb, False, True)
    return table

def left_join(table_a, table_b, test):
    "Runs and returns result from left joining two tables together."
    assert sum(isinstance(table, tuple) for table in (table_a, table_b)) > 0, \
        'At least one table must be given a name!'
    ta, pa = table_a if isinstance(table_a, tuple) else (table_a, '_')
    tb, pb = table_b if isinstance(table_b, tuple) else (table_b, '_')
    table = _composite_table(pa, pb, ta, tb)
    _join_loop(table, test, pa, pb, ta, tb, False, False)
    return table

def right_join(table_a, table_b, test):
    "Runs and returns result from right joining two tables together."
    return left_join(table_b, table_a, test)

def union(table_a, table_b, all_=False):
    "Creates a table from two tables that have been combined."
    table = Table.from_iter(table_a)
    for row in rows(table_b):
        table.insert(*row)
    if all_:
        return table
    return table.distinct()

def rows(iterable):
    "Skips the first row (column names) from a table-style iterator."
    iterator = iter(iterable)
    next(iterator)
    return iterator

################################################################################

def _join_args(table_arg, table_kwarg):
    "Determines tables and prefixes from given arguments."
    assert len(table_kwarg) > 0, 'At least one table name must be given!'
    assert sum(map(len, (table_arg, table_kwarg))) == 2, \
           'Two tables must be provided to join!'
    if len(table_kwarg) == 2:
        (pa, pb), (ta, tb) = zip(*table_kwarg.items())
    else:
        pa, ta = next(iter(table_kwarg.items()))
        pb, tb = '_', table_arg[0]
    return pa, pb, ta, tb

def _composite_table(pa, pb, ta, tb):
    "Create a new table based on information from tables and prefixes."
    columns = []
    for table_name, table_obj in zip((pa, pb), (ta, tb)):
        iterator = iter(table_obj)
        names = next(iterator)
        types = map(lambda item: item[1], table_obj.schema)
        for column_name, column_type in zip(names, types):
            if table_name != '_':
                column_name = '{}.{}'.format(table_name, column_name)
            columns.append((column_name, column_type))
    return Table(*columns)

def _join_loop(table, test, pa, pb, ta, tb, inner, full):
    "Joins two tables together into one table based on criteria."
    first = True
    second = dict()
    table_a = tuple(_pre_process(ta, pa))
    table_b = tuple(_pre_process(tb, pb))
    for row_cache in table_a:
        match = False
        for add in table_b:
            row = row_cache.copy()
            row.update(add)
            if test(_RowAdapter(row)):
                table.insert(**row)
                match = True
                if not first:
                    second.pop(id(add), None)
            elif first:
                second[id(add)] = add
        if not (inner or match):
            table.insert(**row_cache)
        first = False
    if full:
        for row in second.values():
            table.insert(**row)

def _pre_process(table, prefix):
    "Creates a table iterator that can cache results with optional prefix."
    iterator = iter(table)
    columns = next(iterator)
    if prefix == '_':
        for row in iterator:
            yield dict(zip(columns, row))
    else:
        for row in iterator:
            yield {'{}.{}'.format(prefix, column): \
                   value for column, value in zip(columns, row)}

################################################################################

# Unsupported Features:
# =====================
#   Constraints:
#   ------------
#     NOT NULL [forced on all columns]
#     UNIQUE
#     PRIMARY KEY
#     FOREIGN KEY
#     CHECK
#     DEFAULT [constructed from type]
#   Indexes:
#   --------
#     CREATE
#     DROP
#   Increment:
#   ----------
#     AUTO INCREMENT
#     Starting Value
#     Increment by X
#       ["ROW_ID" starts at and increments by 1 but is not accessible]
#   Dates:
#   ------
#     NOW()
#     CURDATE()
#     CURTIME()
#     EXTRACT()
#     DATE_ADD()
#     DATE_SUB()
#     DATEDIFF()
#     DATE_FORMAT()
#     GETDATE()
#     CONVERT()
#       ["DatePart" and "date" are supported and may
#        be supplemented with the "datetime" module]
#   Nulls:
#   ------
#     ISNULL()
#     NVL()
#     IFNULL()
#     COALESCE()
#       [the NOT NULL constraint is forced on all columns]
#   Data Types:
#   -----------
#     Data types that cannot be initialized with a
#     parameterless call are not directly supported.
#   Functions:
#   ----------
#     max() [use "table.max_(column)" instead]
#     min() [use "table.min_(column)" instead]
#     sum() [use "table.sum_(column)" instead]
#     Having Statement
#     ucase() or upper() [use "(str.upper, 'column')" instead]
#     lcase() or lower() [use "(str.lower, 'column')" instead)
#     Virtual Columns [Function Based]
#     Materialized Views [Cached Functions]
#   Transactions:
#   -------------
#     Table Level Transactions
#       [database level transactions are supported;
#        table locks are supported in the same way]

################################################################################

import itertools
import operator

class _Repr:

    def __repr__(self):
        return '{}({})'.format(
            type(self).__name__,
            ', '.join(itertools.starmap('{!s}={!r}'.format,
                                        sorted(vars(self).items()))))

class _Row(_Repr):

    def __getattr__(self, name):
        return _Column(name)

    def __getitem__(self, key):
        return lambda row: row[key]

class _Column(_Row):

    def __init__(self, name):
        self.__name = name

    def __call__(self, row):
        return row[self.__name]

    def __getattr__(self, name):
        if name == 'NOT':
            return _Comparison(self, lambda a, b: (not a, b)[0], None)
        return super().__getattr__(self.__name + '.' + name)

    def __lt__(self, other):
        return _Comparison(self, operator.lt, other)

    def __le__(self, other):
        return _Comparison(self, operator.le, other)

    def __eq__(self, other):
        return _Comparison(self, operator.eq, other)

    def __ne__(self, other):
        return _Comparison(self, operator.ne, other)

    def __gt__(self, other):
        return _Comparison(self, operator.gt, other)

    def __ge__(self, other):
        return _Comparison(self, operator.ge, other)

    def in_(self, *items):
        return _Comparison(self, lambda a, b: a in b, items)

class _Comparison(_Repr):

    def __init__(self, column, op, other):
        self.__column, self.__op, self.__other = column, op, other

    def __call__(self, row):
        if isinstance(self.__other, _Column):
            return self.__op(self.__column(row), self.__other(row))
        return self.__op(self.__column(row), self.__other)

    def __lt__(self, other):
        return self & (self.__column < other)

    def __le__(self, other):
        return self & (self.__column <= other)

    def __eq__(self, other):
        return self & (self.__column == other)

    def __ne__(self, other):
        return self & (self.__column != other)

    def __gt__(self, other):
        return self & (self.__column > other)

    def __ge__(self, other):
        return self & (self.__column >= other)

    def __and__(self, other):
        return _Comparison(self, lambda a, b: a and b, other)

    def __or__(self, other):
        return _Comparison(self, lambda a, b: a or b, other)

ROW = _Row()

################################################################################

def test():
    "Runs several groups of tests of the database engine."
    # Test simple statements in SQL.
    persons = test_basic_sql()
    # Test various ways to select rows.
    test_row_selection(persons)
    # Test the four different types of joins in SQL.
    orders = test_all_joins(persons)
    # Test unstructured ways of joining tables together.
    test_table_addition(persons, orders)
    # Test creation and manipulation of databases.
    test_database_support()
    # Load and run some test on the sample Northwind database.
    northwind = test_northwind()
    # Test different date operations that can be performed.
    test_date_functionality()
    # Test various functions that operate on specified column.
    test_column_functions()
    if northwind:
        # Test ability to select columns with function processing.
        test_generic_column_functions(persons, northwind)
    # Test Database2 instances that support transactions.
    nw2 = test_transactional_database()
    # Allow for interaction at the end of the test.
    globals().update(locals())

def test_basic_sql():
    "Tests simple statements in SQL."
    # Test create table statement.
    persons = Table(('P_Id', int), ('LastName', str), ('FirstName', str),
                    ('Address', str), ('City', str))
    # Populate the table with rows.
    persons.insert(1, 'Hansen', 'Ola', 'Timoteivn 10', 'Sandnes')
    persons.insert(2, 'Svendson', 'Tove', 'Borgvn 23', 'Sandnes')
    persons.insert(3, 'Pettersen', 'Kari', 'Storgt 20', 'Stavanger')
    persons.print()
    # Test the select statement.
    persons.select('LastName', 'FirstName').print()
    persons.select().print()
    # Test the distinct statement.
    persons.select('City').distinct().print()
    # Test the where clause.
    persons.where(ROW.City == 'Sandnes').print()
    # Test the and operator.
    persons.where((ROW.FirstName == 'Tove') &
                  (ROW.LastName == 'Svendson')).print()
    # Test the or operator.
    persons.where((ROW.FirstName == 'Tove') | (ROW.FirstName == 'Ola')).print()
    # Test both and & or operators.
    persons.where((ROW.LastName == 'Svendson') &
                  ((ROW.FirstName == 'Tove') |
                   (ROW.FirstName == 'Ola'))).print()
    # Test order by statement.
    persons.insert(4, 'Nilsen', 'Tom', 'Vingvn 23', 'Stavanger')
    persons.order_by('LastName').table().print()
    persons.order_by('LastName', True).table().print()
    # Test insert statement.
    persons.insert(5, 'Nilsen', 'Johan', 'Bakken 2', 'Stavanger')
    persons.print()
    persons.insert(P_Id=6, LastName='Tjessem', FirstName='Jakob')
    persons.print()
    # Test update statement.
    persons.where((ROW.LastName == 'Tjessem') &
                  (ROW.FirstName == 'Jakob')).update(Address='Nissestien 67',
                                                     City='Sandnes')
    persons.print()
    copy = persons.order_by('P_Id').table()
    copy.update(Address='Nissestien 67', City='Sandnes')
    copy.print()
    # Test delete statement.
    copy = persons.order_by('P_Id').table()
    copy.delete((ROW.LastName == 'Tjessem') &
                (ROW.FirstName == 'Jakob')).print()
    copy.truncate().print()
    return persons

def test_row_selection(persons):
    "Tests various ways to select rows."
    # Test top clause.
    Table.from_iter(persons.top(2)).print()
    Table.from_iter(persons.top(0.5)).print()
    # Test like operator.
    persons.where(Like('City', 's.*')).print()
    persons.where(Like('City', '.*s')).print()
    persons.where(Like('City', '.*tav.*')).print()
    persons.where(NotLike('City', '.*tav.*')).print()
    # Test wildcard patterns.
    persons.where(Like('City', 'sa.*')).print()
    persons.where(Like('City', '.*nes.*')).print()
    persons.where(Like('FirstName', '.la')).print()
    persons.where(Like('LastName', 'S.end.on')).print()
    persons.where(Like('LastName', '[bsp].*')).print()
    persons.where(Like('LastName', '[^bsp].*')).print()
    # Test in operator.
    persons.where(ROW.LastName.in_('Hansen', 'Pettersen')).print()
    # Test manual between syntax.
    persons.where(('Hansen' < ROW.LastName) < 'Pettersen').print()
    persons.where(('Hansen' <= ROW.LastName) < 'Pettersen').print()
    persons.where(('Hansen' <= ROW.LastName) <= 'Pettersen').print()
    persons.where(('Hansen' < ROW.LastName) <= 'Pettersen').print()

def test_all_joins(persons):
    "Tests the four different types of joins in SQL."
    # Create and populate the Orders table.
    orders = Table(('O_Id', int), ('OrderNo', int), ('P_Id', int))
    orders.insert(1, 77895, 3)
    orders.insert(2, 44678, 3)
    orders.insert(3, 22456, 1)
    orders.insert(4, 24562, 1)
    orders.insert(5, 34764, 15)
    # Test the inner join function.
    inner_join(ROW.Persons.P_Id == ROW.Orders.P_Id,
               Persons=persons, Orders=orders) \
               .select('Persons.LastName',
                       'Persons.FirstName',
                       'Orders.OrderNo') \
                       .order_by('Persons.LastName').table().print()
    # Test inner join with alias.
    inner_join(ROW.p.P_Id == ROW.po.P_Id,
               p=persons, po=orders) \
               .select('po.OrderNo', 'p.LastName', 'p.FirstName') \
               .where((ROW.p.LastName == 'Hansen') &
                      (ROW.p.FirstName == 'Ola')).print()
    # Test left join with and without alias.
    left_join((persons, 'Persons'), (orders, 'Orders'),
              ROW.Persons.P_Id == ROW.Orders.P_Id) \
              .select('Persons.LastName',
                      'Persons.FirstName',
                      'Orders.OrderNo') \
                      .order_by('Persons.LastName').table().print()
    left_join((persons, 'p'), (orders, 'o'), ROW.p.P_Id == ROW.o.P_Id) \
              .select('p.LastName',
                      'p.FirstName',
                      'o.OrderNo') \
                      .order_by('p.LastName').table().print()
    # Test right join with and without alias.
    right_join((persons, 'Persons'), (orders, 'Orders'),
               ROW.Persons.P_Id == ROW.Orders.P_Id) \
               .select('Persons.LastName',
                       'Persons.FirstName',
                       'Orders.OrderNo') \
                       .order_by('Persons.LastName').table().print()
    right_join((persons, 'p'), (orders, 'o'), ROW.p.P_Id == ROW.o.P_Id) \
               .select('p.LastName', 'p.FirstName', 'o.OrderNo') \
               .order_by('p.LastName').table().print()
    # Test full join with and without alias.
    full_join(ROW.Persons.P_Id == ROW.Orders.P_Id,
              Persons=persons, Orders=orders) \
              .order_by('Persons.LastName').table().print()
    full_join(ROW.p.P_Id == ROW.o.P_Id,
              p=persons, o=orders) \
              .select('p.LastName', 'p.FirstName', 'o.OrderNo') \
              .order_by('p.LastName').table().print()
    return orders

def test_table_addition(persons, orders):
    "Tests unstructured ways of joining tables together."
    # Create two tables to union together.
    employees_norway = Table(('E_ID', str), ('E_Name', str))
    employees_norway.insert('01', 'Hansen, Ola')
    employees_norway.insert('02', 'Svendson, Tove')
    employees_norway.insert('03', 'Svendson, Stephen')
    employees_norway.insert('04', 'Pettersen, Kari')
    employees_usa = Table(('E_ID', str), ('E_Name', str))
    employees_usa.insert('01', 'Turner, Sally')
    employees_usa.insert('02', 'Kent, Clark')
    employees_usa.insert('03', 'Svendson, Stephen')
    employees_usa.insert('04', 'Scott, Stephen')
    # Test union function on tables.
    union(employees_norway('E_Name'), employees_usa('E_Name')).print()
    union(employees_norway('E_Name'), employees_usa('E_Name'), True).print()
    # Test select into functionality.
    backup = Table(*persons.schema)
    persons.into(backup)
    backup.print()
    backup.truncate()
    persons.select('LastName', 'FirstName').into(backup)
    backup.print()
    # Test select into with where and join clauses.
    backup = Table(('LastName', str), ('FirstName', str))
    persons.where(ROW.City == 'Sandnes') \
           .select('LastName', 'FirstName').into(backup)
    backup.print()
    person_orders = Table(('Persons.LastName', str), ('Orders.OrderNo', int))
    inner_join(ROW.Persons.P_Id == ROW.Orders.P_Id,
               Persons=persons, Orders=orders) \
               .select('Persons.LastName', 'Orders.OrderNo') \
               .into(person_orders)
    person_orders.print()

def test_database_support():
    "Tests creation and manipulation of databases."
    # Test ability to create database.
    db = Database()
    # Test creating and retrieving database tables.
    db.create('persons', Table(('Name', str), ('Credit', int)))
    db.create('mapdata', (('time', float), ('place', complex)))
    db.print()
    db.persons.insert('Marty', 7 ** 4)
    db.persons.insert(Name='Haddock')
    db.persons.print()

def test_northwind():
    "Loads and runs some test on the sample Northwind database."
    import os, imp
    # Patch the module namespace to recognize this file.
    name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    module = imp.new_module(name)
    vars(module).update(globals())
    sys.modules[name] = module
    # Load a Northwind database for various testing purposes.
    try:
        northwind = Database.load('northwind.db')
    except IOError:
        return
    # Create and test a current product list view.
    northwind.create('Current Product List', lambda db: db.Products.where(
        ROW.Discontinued.NOT).select('ProductID', 'ProductName'))
    northwind['Current Product List'].print()
    # Find all products having an above-average price.
    def above_average_price(db):
        return db.Products.where(ROW.UnitPrice > db.Products.avg('UnitPrice')) \
               .select('ProductName', 'UnitPrice')
    northwind.create('Products Above Average Price', above_average_price)
    northwind['Products Above Average Price'].print()
    # Calculate total sale per category in 1997.
    def category_sales_for_1997(db):
        result = Table(('CategoryName', str),
                       ('CategorySales', decimal.Decimal))
        for table in db['Product Sales For 1997'] \
            .group_by('Categories.CategoryName'):
            name = next(rows(table.select('Categories.CategoryName')))[0]
            total = table.sum_('ProductSales')
            result.insert(name, total)
        return result
    northwind.create('Category Sales For 1997', category_sales_for_1997)
    northwind['Category Sales For 1997'].print()
    # Show just the Beverages Category from the previous view.
    northwind['Category Sales For 1997'].where(
        ROW.CategoryName == 'Beverages').print()
    # Add the Category column to the Current Product List view.
    northwind.create_or_replace('Current Product List', lambda db: \
        db['Products View'].where(ROW.Discontinued.NOT) \
        .select('ProductID', 'ProductName', 'Category'))
    northwind['Current Product List'].print()
    # Drop the Category Sales For 1997 view.
    northwind.drop('Category Sales For 1997')
    return northwind

def test_date_functionality():
    "Tests different date operations that can be performed."
    # Create an orderz table to test the date type.
    orderz = Table(('OrderId', int), ('ProductName', str), ('OrderDate', date))
    orderz.insert(1, 'Geitost', date(2008, 11, 11))
    orderz.insert(2, 'Camembert Pierrot', date(2008, 11, 9))
    orderz.insert(3, 'Mozzarella di Giovanni', date(2008, 11, 11))
    orderz.insert(4, 'Mascarpone Fabioloi', date(2008, 10, 29))
    # Query the table for a specific date.
    orderz.where(ROW.OrderDate == date(2008, 11, 11)).print()
    # Update the orderz table so that times are present with the dates.
    orderz.alter_column('OrderDate', datetime)
    orderz.where(ROW.OrderId == 1) \
                        .update(OrderDate=datetime(2008, 11, 11, 13, 23, 44))
    orderz.where(ROW.OrderId == 2) \
                        .update(OrderDate=datetime(2008, 11, 9, 15, 45, 21))
    orderz.where(ROW.OrderId == 3) \
                        .update(OrderDate=datetime(2008, 11, 11, 11, 12, 1))
    orderz.where(ROW.OrderId == 4) \
                        .update(OrderDate=datetime(2008, 10, 29, 14, 56, 59))
    # Query the table with a datetime object this time.
    orderz.where(ROW.OrderDate == datetime(2008, 11, 11)).print()

def test_column_functions():
    "Tests various functions that operate on specified column."
    # Create an order table to test various functions on.
    order = Table(('O_Id', int), ('OrderDate', date),
                  ('OrderPrice', int), ('Customer', str))
    order.insert(1, date(2008, 11, 12), 1000, 'Hansen')
    order.insert(2, date(2008, 10, 23), 1600, 'Nilsen')
    order.insert(3, date(2008, 9, 2), 700, 'Hansen')
    order.insert(4, date(2008, 9, 3), 300, 'Hansen')
    order.insert(5, date(2008, 9, 30), 2000, 'Jensen')
    order.insert(6, date(2008, 10, 4), 100, 'Nilsen')
    # Test the "avg" function.
    order_average = order.avg('OrderPrice')
    print('OrderAverage =', order_average, '\n')
    order.where(ROW.OrderPrice > order_average).select('Customer').print()
    # Test the "count" function.
    print('CustomerNilsen =', order.where(
        ROW.Customer == 'Nilsen').count('Customer'))
    print('NumberOfOrders =', order.count())
    print('NumberOfCustomers =', order.select('Customer') \
          .distinct().count('Customer'))
    # Test the "first" function.
    print('FirstOrderPrice =', order.first('OrderPrice'))
    # Test the "last" function.
    print('LastOrderPrice =', order.last('OrderPrice'))
    # Test the "max_" function.
    print('LargestOrderPrice =', order.max_('OrderPrice'))
    # Test the "min_" function.
    print('SmallestOrderPrice =', order.min_('OrderPrice'))
    # Test the "sum_" function.
    print('OrderTotal =', order.sum_('OrderPrice'), '\n')
    # Test the "group_by" statement.
    result = Table(('Customer', str), ('OrderPrice', int))
    for table in order.group_by('Customer'):
        result.insert(table.first('Customer'), table.sum_('OrderPrice'))
    result.print()
    # Add some more orders to the table.
    order.insert(7, date(2008, 11, 12), 950, 'Hansen')
    order.insert(8, date(2008, 10, 23), 1900, 'Nilsen')
    order.insert(9, date(2008, 9, 2), 2850, 'Hansen')
    order.insert(10, date(2008, 9, 3), 3800, 'Hansen')
    order.insert(11, date(2008, 9, 30), 4750, 'Jensen')
    order.insert(12, date(2008, 10, 4), 5700, 'Nilsen')
    # Test ability to group by several columns.
    result.truncate().alter_add('OrderDate', date)
    for table in order.group_by('Customer', 'OrderDate'):
        result.insert(table.first('Customer'),
                      table.sum_('OrderPrice'),
                      table.first('OrderDate'))
    result.print()

def test_generic_column_functions(persons, northwind):
    "Tests ability to select columns with function processing."
    # Test as_ and select with functions run on columns.
    persons.select((str.upper, 'LastName'), 'FirstName') \
        .as_(('upper(LastName)', 'LastName')).print()
    persons.select((str.lower, 'LastName'), 'FirstName') \
        .as_(('lower(LastName)', 'LastName')).print()
    persons.select((MID(1, 4), 'City')) \
        .as_(('MID(City)', 'SmallCity')).print()
    persons.select((len, 'Address')) \
        .as_(('len(Address)', 'LengthOfAddress')).print()
    northwind['Products'].select('ProductName', (round, 'UnitPrice')) \
        .as_(('round(UnitPrice)', 'UnitPrice')).print()
    current_products = northwind['Products'].select('ProductName',
                                                    'UnitPrice',
                                                    (NOW, 'PerDate'))
    current_products.print()
    current_products.select('ProductName', 'UnitPrice', (FORMAT('%Y-%m-%d'),
        'PerDate')).as_(('FORMAT(PerDate)', 'PerDate')).print()

def test_transactional_database():
    "Tests Database2 instances that support transactions."
    # Create a test database, tables, and dummy data.
    db2 = Database2()
    db2.create('test', Table(('id', int), ('name', str)))
    db2.test.insert(100, 'Adam')
    db2.test.print()
    # Test the rollback transaction support added in Database2.
    test = db2.begin_transaction('test')
    test.insert(101, 'Eve')
    test.print()
    db2.rollback_transaction('test')
    db2.test.print()
    # Test the commit transaction support added in Database2.
    test = db2.begin_transaction('test')
    test.insert(102, 'Seth')
    test.print()
    db2.commit_transaction('test')
    db2.test.print()
    # Prepare some supports for the test that follows.
    import time
    def delay(seconds, handler, table):
        time.sleep(seconds)
        handler(table)
    def async_commit(db, action, table, wait):
        _thread.start_new_thread(delay,
            (wait, getattr(db, action + '_transaction'), table))
    try:
        nw2 = Database2.load('northwind2.db')
    except IOError:
        return
    # Test waiting on a locked table before transaction.
    print('Starting transaction ...')
    categories = nw2.begin_transaction('Categories')
    print('Simulating processing ...')
    async_commit(nw2, 'commit', 'Categories', 2)
    print('Holding for release ...')
    categories = nw2.begin_transaction('Categories', True)
    print('Rolling back the table ...')
    nw2.rollback_transaction('Categories')
    return nw2

################################################################################

if __name__ == '__main__':
    test()
