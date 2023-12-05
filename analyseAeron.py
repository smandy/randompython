import numpy as np
import time
from datetime import datetime

"""

aeron-common/src/main/java/uk/co/real_logic/aeron/common/CncFileDescriptor.java

/**
 * Description of the command and control file used between driver and clients
 *
 * File Layout
 * <pre>
 *  +----------------------------+
 *  |      Aeron CnC Version     |
 *  +----------------------------+
 *  |          Meta Data         |
 *  +----------------------------+
 *  |      to-driver Buffer      |
 *  +----------------------------+
 *  |      to-clients Buffer     |
 *  +----------------------------+
 *  |     Counter Labels Buffer  |
 *  +----------------------------+
 *  |     Counter Values Buffer  |
 *  +----------------------------+
 * </pre>
"""

metaData = [
    ('toDriversLength', np.int32),
    ('toClientsLength', np.int32),
    ('counterLabelsLength', np.int32),
    ('counterValuesLength', np.int32)
    ]

thaip = np.dtype([
    ('cncVersion', np.int32),
    ('metaData', metaData),
])

fn = '/dev/shm/aeron/conductor/cnc'

labelThaip = np.dtype([('length', np.uint32),
                       ('label', 'S1020')])

#orking around a bug

driverTrailer = np.dtype([
    ('tailCounter', np.int64),
    ('ign1', 'S56'),
    ('headCounter', np.int64),
    ('ign2', 'S56'),
    ('correlationCounter', np.int64),
    ('ign3', 'S56'),
    ('consumerHeartbeat', np.int64),
    ('ign4', 'S56')])

driverThaip = np.dtype([
    ('data', np.int8, 1024 * 1024),
    ('trailer', driverTrailer)])

mm = np.memmap(fn, dtype=thaip, mode='r', shape=(1,))[0]
md = mm['metaData']
numLabels = md['counterLabelsLength'] / labelThaip.itemsize
numValues = md['counterValuesLength'] / labelThaip.itemsize # Danger - w
toDriverOffset = thaip.itemsize
toClientOffset = toDriverOffset + md['toDriversLength']

labelOffset = thaip.itemsize + \
              md['toDriversLength'] + \
              md['toClientsLength']

valueOffset = labelOffset + md['counterLabelsLength']

driver = np.memmap(fn, dtype=driverThaip,
                   mode='readonly',
                   shape=1,
                   offset=toDriverOffset)[0]

labels = np.memmap(fn,
                   dtype=labelThaip,
                   mode='r',
                   shape=(numLabels,),
                   offset=labelOffset)

values = np.memmap(fn,
                   dtype=np.int64,
                   mode='r',
                   shape=(numValues,),
                   offset=valueOffset)


rbHeader = np.dtype([
    ('length', np.int32),
    ('thaip', np.int32)
    ])


for x,y in zip(labels[:35], values[:35]):
    print(x[1][:x[0]], y)


print(md)
print(driverThaip.itemsize)


while True:
    print(driver['trailer'])
    time.sleep(0.2)

"""
# Here's what I get 
## np.memmap([(1, (1048832, 1048704, 67108864, 67108864))], 
##       dtype=[('cncVersion', '<i4'), ('metaData', [('toDriversLength', '<i4'), ('toClientsLength', '<i4'), ('counterLabelsLength', '<i4'), ('counterValuesLength', '<i4')])])

First Field
===========
In [9]: 1024 * 1024 + 64 * 4    i.e. 1 meg + 4 cachelines
Out[9]: 1048832
RingBufferDescriptor
public static final int TAIL_COUNTER_OFFSET;
public static final int HEAD_COUNTER_OFFSET;
public static final int CORRELATION_COUNTER_OFFSET;
public static final int CONSUMER_HEARTBEAT_OFFSET;

Second Field
============
BroadcastBufferDescriptor
In [10]: 1024 * 1024 + 64 * 2    i.e. 1 meg + 2 cachelines
(tail counter + last counter)

Out[10]: 1048704

Third + Fourth
==============
67108864  = 1024 * 1024 * 64

"""
