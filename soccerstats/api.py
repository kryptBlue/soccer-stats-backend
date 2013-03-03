"""
Blueprint implementing the API wrapper.

:author: 2013, Pascal Hartig <phartig@weluse.de>
:license: BSD
"""

import json
from flask import Blueprint, request, abort
from .utils import JSONError
from .calc import calculate_scores


api = Blueprint('api', __name__, url_prefix='/v1')


class ScoresResponse(object):
    def __init__(self, scores):
        self.scores = scores

    def to_json(self):
        return {'scores': self.scores}


@api.route('/score', methods=['POST'])
def score():
    """Calculate the score for a given result set."""

    try:
        results = json.loads(request.data)['results']
    except (ValueError, KeyError):
        abort(400)

    if not isinstance(results, list):
        abort(400)

    try:
        scores = calculate_scores(results)
    except Exception as err:
        return JSONError('CALCULATION_ERROR', code=-1, message=err).to_error()

    return ScoresResponse(scores)
