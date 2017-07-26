class auto_dict(dict):
    def __getitem__(self, key):
        return self.setdefault(key, self.__class__())


if __name__ == "__main__":
    d = auto_dict()
    d["foo"]["bar"]["baz"] = 42
    print d
