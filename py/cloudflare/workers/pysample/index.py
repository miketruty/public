def generateOutput(r):
    """
    This would usually generate more interesting output
    based on the request.

    Fields in the request: body, headers, json, method, text, url
    """
    output = [
            'Hello world 2020-07-30!',
            'request details (if I could):',
    ]
    output.append(dir(r))
    # for a in dir(r):
    #     output.append('%s: %s' % (a, getattr(r, a)))
    return output.join('\n')

def handleRequest(request):
    return __new__(Response(generateOutput(request), {
        'headers' : {'content-type' : 'text/plain' },
    }))

addEventListener('fetch', (lambda event: event.respondWith(handleRequest(event.request))))
