# -*- coding: utf-8 -*-

import requests
import json

url = 'https://hooks.slack.com/services/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'

requests.post(url,data = json.dumps({
    'text':u'test @d_minami 来客 @here'
    }))
