def generate_key(self, uid):
    import md5, os, base64, random
    m = md5.new()
    m.update(os.urandom(random.randint(15,25)))
    m.update(uid)
    return base64.standard_b64encode(m.digest())
