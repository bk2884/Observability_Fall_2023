import uuid

def process_trace_context(header):

    datacat_identifier = "dc=.2"

    if 'traceparent' in header:
        traceparent_parts = header['traceparent'].split('-')
        traceparent_parts[2] = uuid.uuid4().hex[0:16]
        header['traceparent'] = '-'.join(traceparent_parts)
    else:
    	version = "00"
    	trace_id = uuid.uuid4().hex
    	parent_id = uuid.uuid4().hex[0:16]
    	trace_flags = "01"
    	new_traceparent = f"{version}-{trace_id}-{parent_id}-{trace_flags}"

    	# Add 'traceparent' before 'tracestate'
    	header['tracestate'] = f"{datacat_identifier},{header.get('tracestate', '')}"
    	header = {'traceparent': new_traceparent, 'tracestate': header['tracestate']}

    if 'tracestate' in header:
        tracestate_parts = header['tracestate'].split(',')
        tracestate_parts = [part for part in tracestate_parts if not part.startswith('dc=')]
        tracestate_parts.insert(0, datacat_identifier)
        header['tracestate'] = ','.join(tracestate_parts)
    else:
        header['tracestate'] = datacat_identifier

    return header

# run tests
input_headers = [
    {
        "traceparent": "00-0af7651916cd43dd8448eb211c80319c-b9c7c989f97918e1-01",
        "tracestate": "congo=ucfJifl5GOE,rojo=00f067aa0ba902b7"
     },{
        "traceparent": "00-0af7651916cd43dd8448eb211c80319c-b9c7c989f97918e1-01",
        "tracestate": "dc=.2,congo=ucfJifl5GOE"
    },{
        "traceparent": "00-0af7651916cd43dd8448eb211c80319c-b9c7c989f97918e1-01",
        "tracestate": "congo=ucfJifl5GOE,dc=1"
    },{
        "tracestate": "congo=ucfJifl5GOE,dc=1"
    },{
        "traceparent": "00-0af7651916cd43dd8448eb211c80319c-b9c7c989f97918e1-01"
    },
    { }
]

for header in input_headers:
    modified_header = process_trace_context(header)
    print(modified_header)
