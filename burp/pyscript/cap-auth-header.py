import sys

global get_token, inject_token


def get_token():
    import re

    url = messageInfo.getUrl()
    paths = [".*/realms/.*/protocol/openid-connect/token"]
    if any(re.match(path, url.toString()) is not None for path in paths):
        print(url)
        response_bytes = messageInfo.getResponse()
        analyzed_response = helpers.analyzeResponse(response_bytes)
        body_offset = analyzed_response.getBodyOffset()
        body_bytes = response_bytes[body_offset:]
        body_str = helpers.bytesToString(body_bytes)

        try:
            import json

            data = json.loads(body_str)
            token = data.get("access_token", None)
            if token:
                state["last_token"] = token
                print("[+] New refresh_token captured: {}".format(token))
        except Exception as e:
            print(e)
            pass


def inject_token():
    if "last_token" not in state or not state["last_token"]:
        return

    last_token = state["last_token"]
    request_info = helpers.analyzeRequest(messageInfo)
    body = messageInfo.getRequest()[request_info.getBodyOffset() :]

    headers = request_info.getHeaders()
    for h in headers:
        if h.startswith("Authorization:"):
            headers.remove(h)
            break

    auth_header = "Authorization: Bearer {}".format(last_token)
    headers.add(auth_header)

    new_request = helpers.buildHttpMessage(headers, body)
    messageInfo.setRequest(new_request)
    print(
        "[*] Authorization header replaced with new refresh_token in {}".format(
            callbacks.getToolName(toolFlag)
        )
    )


def process_request():
    global inject_token
    request_info = helpers.analyzeRequest(messageInfo)
    headers = request_info.getHeaders()
    triggers = ("Authorization: XXX", "User-Agent: 13337")
    if toolFlag in (
        callbacks.TOOL_REPEATER,
        callbacks.TOOL_SCANNER,
        callbacks.TOOL_INTRUDER,
        callbacks.TOOL_EXTENDER,
    ) or (
        toolFlag == callbacks.TOOL_PROXY
        and any(j in i for j in triggers for i in headers)
    ):
        inject_token()


def process_response():
    global get_token
    if toolFlag == callbacks.TOOL_PROXY:
        get_token()


if messageIsRequest:
    process_request()
else:
    process_response()
