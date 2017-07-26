class Files(tuple):
  def __new__(cls, *filePaths):
    files = []
    try:
      for filePath in filePaths:
        files.append(open(filePath))
        files[-1].__enter__()
    except:
      for file in files:
        file.close()
      raise
    else:
      return super(Files, cls).__new__(cls, files)
  def __enter__(self):
    return self
  def __exit__(self, *args):
    for file in self:
      file.close()
