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
#
#       https://pypi.org/project/fuzzywuzzy/
#
from fuzzywuzzy import fuzz
# from fuzzywuzzy import process
import json


def read_filter_configuration(filename):
    """Read the input JSON file that defines the filter

    Args:
        filename (str): File name (or None) containing the JSON formatted filter
    Returns:
        None or the dictionary representing the filter
    """

    if not filename:
        return None
 
    try:
        f = open(filename)
    except (FileNotFoundError, IsADirectoryError) as e:
        print(f'FileNotFound: {e}')
        return None

    try:
        data = json.load(f)
    except:
        print(f'Error loading JSON data from {f.name}')
        return None

    return data


class Conditional(object):
    """Conditional definition to match against the data

    Args:
        filter_config: (dict): configuration of the filter, example
                                {
                                    "match": "any",
                                    "conditions": [
                                    {"key": "mac", "value": "26:f5:a2:3c:e4:70"},
                                    {"key": "os", "value": "PlayStation 4"}
                                    ]
                                }
        data: (dict) : Data returned from an API call, for example
                                {
                                    "os": "PlayStation 4",
                                    "ip6": null,
                                    "mac": "b0:05:94:24:0f:d7",
                                }
    Returns:
        None:  __init__ validates the input data via assertions
    """

    def __init__(self, filter_config, data):
        assert isinstance(filter_config, dict), "filter configuration must be type dict"
        assert isinstance(data, dict), "data must be type dict"
        self.ANY = 'any'
        self.ALL = 'all'

        self.match = filter_config.get('match')
        assert isinstance(self.match, str), f"'match' must be of type string"
        assert self.match in (self.ANY, self.ALL), f"'match' must be either 'any' or 'all', not '{self.match}'!"
        self.match = self.match.lower()

        self.conditions = filter_config.get('conditions')
        self.number_of_conditions = len(self.conditions)
        self.data = data  # a Dictionary, e.g. {"mac": "26:f5:a2:3c:e4:70", "os": "PlayStation 4"}

        return

    def compare(self):
        """Compare the two dictionaries to determine if there is a match, return True of False
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
    """Use Fuzzywuzzy to determine credibility

    Args: 
        a (str): first string
        b (str): second string

    Returns: Dictionary of the match confidence intervals
    """

    def __init__(self, a, b):
        self.result = dict(ratio=0, partial=0)   
        self.a = str(a)
        self.b = str(b)
        return

    def compare(self):
        """Execute ratio and partial matches

        Returns:
          Dictionary of the results
        """
        self.result['ratio'] = fuzz.ratio(self.a, self.b)
        self.result['partial'] = fuzz.partial_ratio(self.a, self.b)
        return dict(fuzzy=self.result)
    