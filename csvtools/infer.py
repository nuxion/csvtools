from chardet.universaldetector import UniversalDetector



def bylines(lines):
    detector = UniversalDetector()
    for line in lines:
        line= bytearray(line)
        detector.feed(line)
        if detector.done: break
    detector.close()
    return detector.result

def chardetect(arch):
    with open(arch, "rb") as f:
        encoding = bylines(f)

    return encoding

if __name__=='__main__':
    pass


