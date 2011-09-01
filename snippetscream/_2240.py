"""
Serialize data to/from CSV

Since CSV deals only in string values, certain conventions must be
employed to represent other data types. The conventions used in this
serializer implementation are as follows:

- Boolean values are serialized as 'TRUE' and 'FALSE'
- The strings 'TRUE' and 'FALSE' are  serialized as "'TRUE'" and "'FALSE'"
- None is serialized as 'NULL'
- The string 'NULL' is serialized as "'NULL'"
- Lists are serialized as comma separated items surrounded by brackets,
  e.g. [foo, bar] becomes '[foo, bar]'
- Strings beginning with '[' and ending in ']' are serialized by being
  wrapped in single quotes, e.g. '[foo, bar]' becomes "'[foo, bar]'"

See also:
http://docs.djangoproject.com/en/1.2/topics/serialization/

"""
import codecs
import csv
import re
import StringIO

from itertools import groupby
from operator import itemgetter

from django.core.serializers.python import Serializer as PythonSerializer
from django.core.serializers.python import Deserializer as PythonDeserializer
from django.utils.encoding import smart_unicode


class Serializer(PythonSerializer):
    """
    Convert a queryset to CSV.
    """
    internal_use_only = False

    def end_serialization(self):

        def process_item(item):
            if isinstance(item, (list, tuple)):
                item = process_m2m(item)
            elif isinstance(item, bool):
                item = str(item).upper()
            elif isinstance(item, basestring):
                if item in ('TRUE', 'FALSE', 'NULL') or _LIST_RE.match(item):
                    # Wrap these in quotes, so as not to be confused with
                    # builtin types when deserialized
                    item = "'%s'" % item
            elif item is None:
                item = 'NULL'
            return smart_unicode(item)

        def process_m2m(seq):
            parts = []
            for item in seq:
                if isinstance(item, (list, tuple)):
                    parts.append(process_m2m(item))
                else:
                    parts.append(process_item(item))
            return '[%s]' % ', '.join(parts)

        writer = UnicodeWriter(self.stream)
        # Group objects by model and write out a header and rows for each.
        # Multiple models can be present when invoking from the command
        # line, e.g.: `python manage.py dumpdata --format csv auth`
        for k, g in groupby(self.objects, key=itemgetter('model')):
            write_header = True
            for d in g:
                # "flatten" the object. PK and model values come first,
                # then field values. Flat is better than nested, right? :-)
                pk, model, fields = d['pk'], d['model'], d['fields']
                pk, model = smart_unicode(pk), smart_unicode(model)
                row = [pk, model] + map(process_item, fields.values())
                if write_header:
                    header = ['pk', 'model'] + fields.keys()
                    writer.writerow(header)
                    write_header = False
                writer.writerow(row)

    def getvalue(self):
        if callable(getattr(self.stream, 'getvalue', None)):
            return self.stream.getvalue()


_QUOTED_BOOL_NULL = """ 'TRUE' 'FALSE' 'NULL' "TRUE" "FALSE" "NULL" """.split()

# regular expressions used in deserialization
_LIST_PATTERN = r'\[(.*)\]'
_LIST_RE = re.compile(r'\A%s\Z' % _LIST_PATTERN)
_QUOTED_LIST_RE = re.compile(r"""
    \A                 # beginning of string
    (['"])             # quote char
    %s                 # list
    \1                 # matching quote
    \Z                 # end of string""" % _LIST_PATTERN, re.VERBOSE)
_SPLIT_RE = re.compile(r', *')
_NK_LIST_RE = re.compile(r"""
    \A                 # beginning of string
    \[                 # opening bracket
    [^]]+              # one or more non brackets
    \]                 # closing bracket
    (?:, *\[[^]]+\])*  # zero or more of above, separated
                       #   by a comma and optional spaces
    \Z                 # end of string""", re.VERBOSE)
_NK_SPLIT_RE = re.compile(r"""
    (?<=\])            # closing bracket (lookbehind)
    , *                # comma and optional spaces
    (?=\[)             # opening bracket (lookahead)""", re.VERBOSE)


def Deserializer(stream_or_string, **options):
    """
    Deserialize a stream or string of CSV data.
    """
    def process_item(item):
        m = _LIST_RE.match(item)
        if m:
            contents = m.group(1)
            if not contents:
                item = []
            else:
                item = process_m2m(contents)
        else:
            if item == 'TRUE':
                item = True
            elif item == 'FALSE':
                item = False
            elif item == 'NULL':
                item = None
            elif (item in _QUOTED_BOOL_NULL or
                  _QUOTED_LIST_RE.match(item)):
                item = item.strip('\'"')
        return item

    def process_m2m(contents):
        li = []
        if _NK_LIST_RE.match(contents):
            for item in _NK_SPLIT_RE.split(contents):
                li.append(process_item(item))
        else:
            li = _SPLIT_RE.split(contents)
        return li

    if isinstance(stream_or_string, basestring):
        stream = StringIO.StringIO(stream_or_string)
    else:
        stream = stream_or_string

    reader = UnicodeReader(stream)
    header = next(reader)  # first line must be a header

    data = []
    for row in reader:
        # Need to account for the presence of multiple headers in
        # the stream since serialized data can contain them.
        if row[:2] == ['pk', 'model']:
            # Not the best check. Perhaps csv.Sniffer.has_header
            # would be better?
            header = row
            continue
        d = dict(zip(header[:2], row[:2]))
        d['fields'] = dict(zip(header[2:], map(process_item, row[2:])))
        data.append(d)

    for obj in PythonDeserializer(data, **options):
        yield obj


# The classes below taken from http://docs.python.org/library/csv.html

class UTF8Recoder(object):
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode('utf-8')


class UnicodeReader(object):
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding='utf-8', **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, 'utf-8') for s in row]

    def __iter__(self):
        return self


class UnicodeWriter(object):
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding='utf-8', **kwds):
        # Redirect output to a queue
        self.queue = StringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode('utf-8') for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode('utf-8')
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
