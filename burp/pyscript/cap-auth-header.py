import sys

global get_token, inject_token

state["realm"] = "XXXX"


def get_token():
    url = messageInfo.getUrl()
    if (
        url
        and f"/realms/{state["realm"]}/protocol/openid-connect/token" in url.toString()
    ):
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
    is_found_header = False
    for h in headers:
        if h.startswith("Authorization:"):
            is_found_header = True
            headers.remove(h)
            break

    if not is_found_header:
        return

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
    if toolFlag in (
        callbacks.TOOL_REPEATER,
        callbacks.TOOL_SCANNER,
        callbacks.TOOL_INTRUDER,
    ) or (
        toolFlag == callbacks.TOOL_PROXY
        and any("Authorization: XXX" in i for i in headers)
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
