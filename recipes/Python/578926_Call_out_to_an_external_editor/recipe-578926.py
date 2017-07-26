import os, tempfile

def edit(editor, content=''):
    f = tempfile.NamedTemporaryFile(mode='w+')
    if content:
        f.write(content)
        f.flush()
    command = editor + " " + f.name
    status = os.system(command)
    f.seek(0, 0)
    text = f.read()
    f.close()
    assert not os.path.exists(f.name)
    return (status, text)
