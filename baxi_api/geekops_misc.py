import time


def GenerateReference():
    rawTime = (round(time.time()) * 19564)
    timestamp = int(rawTime)
    tx_ref = "Bremit-" + str(timestamp)
    return tx_ref
