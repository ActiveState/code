import weakref

class EndOfStreamException(Exception):
  pass

class InvalidReaderException(Exception):
  pass

class BufferedStream:
  """A stream that supports multiple forward-only readers"""
  def __init__(self, generator):
      self.readers=[]
      self.generator=(item for item in generator)
      self.buffer=[]
      self.buffer_end=0
      self.buffer_start=0
      self.eof = False

  def read(self, reader, count):
      """Reads some values from the buffer"""
      indexBeforeRead = reader.index
      indexAfterRead = reader.index + count
      if indexBeforeRead < self.buffer_start:
          raise InvalidReaderException()
      if indexAfterRead > self.buffer_end:
          if self.eof:
              raise EndOfStreamException()
          else:
               self.populateBuffer(indexAfterRead)
      result = self.getBufferContents(indexBeforeRead, indexAfterRead)
      reader.index = indexAfterRead
      self.trimBuffer(indexBeforeRead)
      return result    

  def populateBuffer(self, targetIndex):
      """Ensures that all required values are in the buffer"""
      while self.buffer_end < targetIndex:
          try:
              nextValue = self.generator.next()
          except StopIteration:
              self.eof = True
              raise EndOfStreamException()
          self.buffer.append(nextValue)
          self.buffer_end += 1

  def trimBuffer(self, index):
      """Drops unneeded buffer contents"""
      if index!=self.buffer_start:
          return
      newBufferStart = self.buffer_end
      for readerRef in self.readers:
          reader = readerRef()
          if reader.index < newBufferStart:
              newBufferStart=reader.index
      dropSize = newBufferStart - self.buffer_start
      self.buffer = self.buffer[dropSize:]
      self.buffer_start = newBufferStart

  def getBufferContents(self, start, end):
      """Gets some values from the buffer"""
      start -= self.buffer_start
      end -= self.buffer_start
      return self.buffer[start:end]

  def createReader(self, index=0):
      reader = Reader(self, index)
      self.readers.append(weakref.ref(reader, self.removeReader))
      return reader

  def removeReader(self, ref):
      self.readers.remove(ref)


class Reader:
  def __init__(self, buffer, index=0):
      self.buffer = buffer
      self.index = index

  def read(self, count):
      return self.buffer.read(self, count)

  def readChar(self):
      return self.read(1)[0]

  def clone(self):
      return self.buffer.createReader(self.index)

  def __del__(self):
      self.buffer.trimBuffer(self.index)
