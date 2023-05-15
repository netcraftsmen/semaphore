#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#     Copyright (c) 2023 Joel W. King
#     All rights reserved.
#
#     author: @joelwking)
#     written:  14 May 2023
#
#     description: Event filters
#
#     usage:
#       >>> from filter import filters
#       >>> result = filters.Fuzzy('ONE','ONE').match()
#       >>> result
#       {'ratio': 100, 'partial': 100}
#
#       test = filters.read_filter_configuration('../documentation/filter.json')
#       valid = None
#       valid = filters.Conditional(test, dict())
#       if not valid:
#          exit(1)
#       https://pypi.org/project/fuzzywuzzy/
#
from fuzzywuzzy import fuzz
# from fuzzywuzzy import process
import json

def read_filter_configuration(filename):
    """
        Read the input JSON file that defines the filter
        and return a dictionary to the caller
    """
    try:
        f = open(filename)
    except (FileNotFoundError, IsADirectoryError) as e:
        print(f'FileNotFound: {e}')
        return None

    try:
        data = json.load(f)
    except JSONDecoderError as e:
        print(f'{f.name} {e}')
        return None

    print(f'Using {f.name} as filter')
    return data


class Conditional(object):
    """

    Input: conditional to test against the data
        {
            "match": "any",
            "conditions": [
            {"key": "mac", "value": "26:f5:a2:3c:e4:70"},
            {"key": "os", "value": "PlayStation 4"}
            ]
        }
    >>> from filter import filters
    >>> test = dict(conditions=[{"key": "mac", "value": "26:f5:a2:3c:e4:70"}, {"key": "os", "value": "PlayStation 4"}])
    >>> test['match']='any'
    >>> data = {"mac": "26:f5:a2:3c:e4:70", "os": "PlayStation 4"}
    >>> filters.Conditional(test, data).match()
    """

    def __init__(self, filter, data):
        assert isinstance(test, dict), f"filter must be type dict"
        assert isinstance(data, dict), f"data must be type dict"
        self.ANY = 'any'
        self.ALL = 'all'

        self.match = filter.get('match')
        assert isinstance(self.match, str), f"'match' must be of type string"
        assert self.match in (self.ANY, self.ALL), f"'match' must be either 'any' or 'all', not '{self.match}'!"
        self.match = self.match.lower()

        self.conditions = filter.get('conditions')
        self.number_of_conditions = len(self.conditions)
        self.data = data  # a Dictionary, e.g. {"mac": "26:f5:a2:3c:e4:70", "os": "PlayStation 4"}

        return
    
    def compare(self):
        """
            Compare the two dictionaries to determine if there is a match, return True of False
        """
        hits = 0
        for condition in self.conditions:
            if self.data.get(condition['key']):
                if self.data[condition['key']] == condition['value']:
                    hits += 1

        if (self.match == self.ALL) and (hits == self.number_of_conditions):
            return True
    
        if (self.match == self.ANY) and (hits > 0):
            return True
       
        return False

class Fuzzy(object):
    """
        Use Fuzzywuzzy to determine credibility
        Input: two strings to be compared
        Returns: dict of the match confidence
    """

    def __init__(self, a, b):
        self.result = dict(ratio=0, partial=0)   
        self.a = a
        self.b = b
        return

    def compare(self):
        """
            Execute ratio and partial matches
        """
        self.result['ratio'] = fuzz.ratio(self.a, self.b)
        self.result['partial'] = fuzz.partial_ratio(self.a, self.b)
        return dict(fuzzy=self.result)
    