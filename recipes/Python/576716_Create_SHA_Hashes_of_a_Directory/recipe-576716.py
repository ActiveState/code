import sha
import os
def createsha(directory):
    """Walk through a Directory creating Sha Hashes of each file path"""
    for root, dirs, files in os.walk(str(directory)):
        for name in files:
            filepath = os.path.join(root, name)
            value = sha.new(filepath).hexdigest()
            print value
