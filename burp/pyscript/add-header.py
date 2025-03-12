import sys

global inject_token

def inject_token():
    print(callbacks.getToolName(toolFlag))
    request_info = helpers.analyzeRequest(messageInfo)
    body = messageInfo.getRequest()[request_info.getBodyOffset() :]

    headers = request_info.getHeaders()
    ticket = "X-Ya-Service-Ticket: 3:serv:CPf2ARC5o5i-BiIRCMTzehC06Hog2-_fkaXU_gE:EvsnRX2DPJuX6o4btUVlUXK_JOFrcUQD6njjBvOO0xX6DfyMj_KT9NVOINR2ZbSp8xfuid4iRf7gKayCQmbFhM1WOrVAaih724q7cpl7un5VpleLLJ6-Th7-EGj7fFr5qbzHJV1CRCY3C8E8-qu5uQo0IhJOCU2C5F7FkBVkxtzhbJfv5PIvwTrWtCkxhhEujqtkp8U_X62Wfkv9IlnrqemHN5XFcfNRP0FDAK26GJo5knmwpuTGdZCQ58V3nR3NcIPjUkDkijyOxSq1FVOnckpFfmPQYqEKTwvsfJgj5-yoSCwydoAzn_R58V1Hig9IqLJo0ChyukvsGl47Us9obA"
    headers.add(ticket)

    new_request = helpers.buildHttpMessage(headers, body)
    messageInfo.setRequest(new_request)
    print("[*] Ticket header".format(callbacks.getToolName(toolFlag)))


def process_request():
    global inject_token
    if toolFlag in (
        callbacks.TOOL_REPEATER,
        callbacks.TOOL_SCANNER,
        callbacks.TOOL_INTRUDER,
        callbacks.TOOL_EXTENDER,
    ):
        inject_token()


if messageIsRequest:
    process_request()
