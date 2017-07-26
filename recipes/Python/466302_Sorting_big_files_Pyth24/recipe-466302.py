from heapq import heapify, heappop, heappush
from itertools import islice, cycle
from tempfile import gettempdir
import os

def merge(chunks,key=None):
    if key is None:
        key = lambda x : x

    values = []

    for index, chunk in enumerate(chunks):
        try:
            iterator = iter(chunk)
            value = iterator.next()
        except StopIteration:
            try:
                chunk.close()
                os.remove(chunk.name)
                chunks.remove(chunk)
            except:
                pass
        else:
            heappush(values,((key(value),index,value,iterator,chunk)))

    while values:
        k, index, value, iterator, chunk = heappop(values)
        yield value
        try:
            value = iterator.next()
        except StopIteration:
            try:
                chunk.close()
                os.remove(chunk.name)
                chunks.remove(chunk)
            except:
                pass
        else:
            heappush(values,(key(value),index,value,iterator,chunk))

def batch_sort(input,output,key=None,buffer_size=32000,tempdirs=[]):
    if not tempdirs:
        tempdirs.append(gettempdir())
    
    input_file = file(input,'rb',64*1024)
    try:
        input_iterator = iter(input_file)
        
        chunks = []
        try:
            for tempdir in cycle(tempdirs):
                current_chunk = list(islice(input_iterator,buffer_size))
                if current_chunk:
                    current_chunk.sort(key=key)
                    output_chunk = file(os.path.join(tempdir,'%06i'%len(chunks)),'w+b',64*1024)
                    output_chunk.writelines(current_chunk)
                    output_chunk.flush()
                    output_chunk.seek(0)
                    chunks.append(output_chunk)
                else:
                    break
        except:
            for chunk in chunks:
                try:
                    chunk.close()
                    os.remove(chunk.name)
                except:
                    pass
            if output_chunk not in chunks:
                try:
                    output_chunk.close()
                    os.remove(output_chunk.name)
                except:
                    pass
            return
    finally:
        input_file.close()
    
    output_file = file(output,'wb',64*1024)
    try:
        output_file.writelines(merge(chunks,key))
    finally:
        for chunk in chunks:
            try:
                chunk.close()
                os.remove(chunk.name)
            except:
                pass
        output_file.close()

if __name__ == '__main__':
    import optparse
    parser = optparse.OptionParser()
    parser.add_option(
        '-b','--buffer',
        dest='buffer_size',
        type='int',default=32000,
        help='''Size of the line buffer. The file to sort is
            divided into chunks of that many lines. Default : 32,000 lines.'''
    )
    parser.add_option(
        '-k','--key',
        dest='key',
        help='''Python expression used to compute the key for each
            line, "lambda line:" is prepended.\n
            Example : -k "line[5:10]". By default, the whole line is the key.'''
    )
    parser.add_option(
        '-t','--tempdir',
        dest='tempdirs',
        action='append',
        default=[],
        help='''Temporary directory to use. You might get performance
            improvements if the temporary directory is not on the same physical
            disk than the input and output directories. You can even try
            providing multiples directories on differents physical disks.
            Use multiple -t options to do that.'''
    )
    parser.add_option(
        '-p','--psyco',
        dest='psyco',
        action='store_true',
        default=False,
        help='''Use Psyco.'''
    )
    options,args = parser.parse_args()
    
    if options.key:
        options.key = eval('lambda line : (%s)'%options.key)
    
    if options.psyco:
        import psyco
        psyco.full()
    
    batch_sort(args[0],args[1],options.key,options.buffer_size,options.tempdirs) 
