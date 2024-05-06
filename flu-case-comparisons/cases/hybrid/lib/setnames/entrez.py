# setLeafName :: (JsonObj, Clade) -> Str
def setLeafName(meta):
    (jsonObj, clade) = meta
    return ( clade + "|" +
             jsonObj["GBSeq_primary-accession"] + "|" +
             jsonObj["GBSeq_length"]
           )
