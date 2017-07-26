"""Utility functions to deal with HTTP stream: dechunking and decompressing
body etc.
"""

__author__ = 'vovanec@gmail.com'


import bz2
import functools
import types
import zlib


CHUNK_SIZE = 1024 * 16

GZIP = 'gzip'
DEFLATE = 'deflate'
BZIP2 = 'bzip2'
SUPPORTED_COMPRESSIONS = {GZIP, DEFLATE, BZIP2}

DECOMPRESSOR_FACTORIES = {
    DEFLATE: functools.partial(zlib.decompressobj, -zlib.MAX_WBITS),
    GZIP: functools.partial(zlib.decompressobj, 16 + zlib.MAX_WBITS),
    BZIP2: bz2.BZ2Decompressor
}


class BodyStreamError(Exception):

    """Exception of this class is raised when HTTP stream could not be read.
    """

    pass


class DechunkError(BodyStreamError):

    """Raised when could not de-chunk stream.
    """

    pass


class DecompressError(BodyStreamError):

    """Raised when could not decompress stream.
    """

    pass


def read_until(stream, delimiter, max_bytes=16):
    """Read until we have found the given delimiter.
    :param file stream: readable file-like object.
    :param bytes delimiter: delimiter string.
    :param int max_bytes: maximum bytes to read.
    :rtype: bytes|None
    """

    buf = bytearray()
    delim_len = len(delimiter)

    while len(buf) < max_bytes:
        c = stream.read(1)

        if not c:
            break

        buf += c
        if buf[-delim_len:] == delimiter:
            return bytes(buf[:-delim_len])


def dechunk(stream):
    """De-chunk HTTP body stream.
    :param file stream: readable file-like object.
    :rtype: __generator[bytes]
    :raise: DechunkError
    """

    # TODO(vovan): Add support for chunk extensions:
    # TODO(vovan): http://tools.ietf.org/html/rfc2616#section-3.6.1

    while True:
        chunk_len = read_until(stream, b'\r\n')

        if chunk_len is None:
            raise DechunkError(
                'Could not extract chunk size: unexpected end of data.')

        try:
            chunk_len = int(chunk_len.strip(), 16)
        except (ValueError, TypeError) as err:
            raise DechunkError('Could not parse chunk size: %s' % (err,))

        if chunk_len == 0:
            break

        bytes_to_read = chunk_len
        while bytes_to_read:
            chunk = stream.read(bytes_to_read)
            bytes_to_read -= len(chunk)
            yield chunk

        # chunk ends with \r\n
        crlf = stream.read(2)
        if crlf != b'\r\n':
            raise DechunkError('No CR+LF at the end of chunk!')


def to_chunks(stream_or_generator):
    """This generator function receives file-like or generator as input
    and returns generator.
    :param file|__generator[bytes] stream_or_generator: readable stream or
           generator.
    :rtype: __generator[bytes]
    :raise: TypeError
    """

    if isinstance(stream_or_generator, types.GeneratorType):
        yield from stream_or_generator
    elif hasattr(stream_or_generator, 'read'):
        while True:
            chunk = stream_or_generator.read(CHUNK_SIZE)
            if not chunk:
                break  # no more data

            yield chunk

    else:
        raise TypeError('Input must be either readable or generator.')


def decompress(chunks, compression):
    """Decompress
    :param __generator[bytes] chunks: compressed body chunks.
    :param str compression: compression constant.
    :rtype: __generator[bytes]
    :return: decompressed chunks.
    :raise: TypeError, DecompressError
    """

    if compression not in SUPPORTED_COMPRESSIONS:
        raise TypeError('Unsupported compression type: %s' % (compression,))

    try:
        de_compressor = DECOMPRESSOR_FACTORIES[compression]()

        for chunk in chunks:
            try:
                yield de_compressor.decompress(chunk)
            except OSError as err:
                # BZ2Decompressor: invalid data stream
                raise DecompressError(err) from None

        # BZ2Decompressor does not support flush() interface.
        if hasattr(de_compressor, 'flush'):
            yield de_compressor.flush()

    except zlib.error as err:
        raise DecompressError(err) from None


def read_body_stream(stream, chunked=False, compression=None):
    """Read HTTP body stream, yielding blocks of bytes. De-chunk and
    de-compress data if needed.
    :param file stream: readable stream.
    :param bool chunked: whether stream is chunked.
    :param str|None compression: compression type is stream is
           compressed, otherwise None.
    :rtype: __generator[bytes]
    :raise: TypeError, BodyStreamError
    """

    if not (chunked or compression):
        return to_chunks(stream)

    generator = stream
    if chunked:
        generator = dechunk(generator)

    if compression:
        generator = decompress(to_chunks(generator), compression)

    return generator
