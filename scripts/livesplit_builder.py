TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<Run version="1.7.0">
  <GameIcon />
  <GameName>Path of Exile</GameName>
  <CategoryName>
  </CategoryName>
  <Metadata>
    <Run id="" />
    <Platform usesEmulator="False">
    </Platform>
    <Region>
    </Region>
    <Variables />
  </Metadata>
  <Offset>00:00:00</Offset>
  <AttemptCount>0</AttemptCount>
  <AttemptHistory />
  <Segments>
    {segments}
  </Segments>
  <AutoSplitterSettings />
</Run>
"""

SEGMENT_TEMPLATE = """<Segment>
  <Name>{name}</Name>
  <Icon/>
  <SplitTimes>
    <SplitTime name="Personal Best" />
  </SplitTimes>
  <BestSegmentTime />
  <SegmentHistory />
</Segment>"""


def _build_splits(items):
    for s in items:
        yield SEGMENT_TEMPLATE.format(name=s)


def build_splits(splits):
    segments = "".join(list(_build_splits(splits)))
    return TEMPLATE.format(segments=segments)
