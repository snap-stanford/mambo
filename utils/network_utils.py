import snap

DELIMITER  = "\t"


def get_num_elem_per_mode(Graph):
    mode_num_elem = {}
    modeneti = Graph.BegModeNetI()
    while modeneti < Graph.EndModeNetI():
        name = Graph.GetModeName(modeneti.GetModeId())
        modeNet = modeneti.GetModeNet()
        mode_num_elem[name] = modeNet.GetNodes()
        modeneti.Next()
    return mode_num_elem
      

def get_num_elem_per_link(Graph):
    link_num_elem = {}
    crossnetids = snap.TIntV()
    crossneti = Graph.BegCrossNetI()
    while crossneti < Graph.EndCrossNetI():
        crossnetids.Add(crossneti.GetCrossId())
        name = Graph.GetCrossName(crossneti.GetCrossId())
        crossnet = crossneti.GetCrossNet()
        link_num_elem[name] = crossnet.GetEdges()
        crossneti.Next()
    return link_num_elem


def load_mode_to_graph(mode, filename, Graph, context):
    modeId = mode + 'Id'
    schema = snap.Schema()
    schema.Add(snap.TStrTAttrPr(modeId, snap.atStr))
    schema.Add(snap.TStrTAttrPr("datasetId", snap.atStr))
    modenet = snap.TTable.LoadSS(schema, filename, context, "\t", snap.TBool(False))
    snap.LoadModeNetToNet(Graph, mode, modenet, modeId, snap.TStrV())


def load_crossnet_to_graph(context, edgeId, srcName, dstName, filepath, Graph, prefix="miner"):
    srcId = srcName + "SrcId"
    dstId = dstName + "DstId"
    schema = snap.Schema()
    schema.Add(snap.TStrTAttrPr(edgeId, snap.atStr))
    schema.Add(snap.TStrTAttrPr("datasetId", snap.atStr))
    schema.Add(snap.TStrTAttrPr(srcId, snap.atStr))
    schema.Add(snap.TStrTAttrPr(dstId, snap.atStr))
    crossnet = snap.TTable.LoadSS(schema, filepath, context, DELIMITER, snap.TBool(False))
    crossName = prefix + "-" + dstName + "-" + srcName
    Graph.AddCrossNet(srcName, dstName, crossName, False)
    snap.LoadCrossNetToNet(Graph, srcName, dstName, crossName, crossnet, srcId, dstId, snap.TStrV())
