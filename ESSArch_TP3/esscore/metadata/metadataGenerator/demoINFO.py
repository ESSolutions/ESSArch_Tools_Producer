from xmlGenerator import createXML, calculateChecksum

inputData = {
        "agentname1":"amdSecID",
        "agentname2":"sadf",
        "agentname3":"sadf",
        "agentnote1":"sd",
        "agentnote2":"dsasdf",
        "agentnote3":"ds",
        "ID1":"sad",
        "ID2":"sdf",
        "ID3":"asdf",
        "SUBMISSIONAGREEMENT":"sdfsdf",
        "PREVIOUSSUBMISSIONAGREEMENT":"asdfds",
        "REFERENCECODE":"sadfd",
        "MetsHdrCREATEDATE": "sadf",
        "MetsOBJID":"sadf",
        "MetsType":"SIP",
        "MetsPROFILE": "asdf",
        "amdSecID": "asdf",
}

# print calculateChecksum('/SIP/tar.dmg')

createXML(inputData, {"info.xml":"templates/info.json"}, '/SIP')
