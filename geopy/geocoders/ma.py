#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals


from geopy.geocoders.base import (
    Geocoder,
    DEFAULT_FORMAT_STRING,
    DEFAULT_TIMEOUT,
)
from geopy.compat import urlencode
from geopy.location import Location
from geopy.util import logger

__all__ = ("MA", )


class MA(Geocoder):

    structured_query_params = {
        'types',
        'q'
    }
    def __init__(self, api, format_string=DEFAULT_FORMAT_STRING, timeout=DEFAULT_TIMEOUT, proxies=None): # pylint: disable=R0913
        super(MA, self).__init__(
            format_string, 'http', timeout, proxies
        )
        self.format_string = format_string
        self.api = api


    def geocode(self, query, exactly_one=True, timeout=None):  # pylint: disable=R0913,W0221
        params = {
            'q': self.format_string % query,
            'types': 'addresses'
        }
        url = "?".join((self.api, urlencode(params)))
        logger.debug("%s.geocode: %s", self.__class__.__name__, url)
        return self._parse_json(
            self._call_geocoder(url, timeout=timeout), exactly_one
        )

    @staticmethod
    def parse_code(place):
        """
        Parse each resource.
        """
        latitude = place.get('lat', None)
        longitude = place.get('lon', None)
        placename = place.get('title', None)
        if latitude and longitude:
            latitude = float(latitude)
            longitude = float(longitude)
        return Location(placename, (latitude, longitude), place)

    def _parse_json(self, place, exactly_one):
        """
        Internal class to handle json response
        """
        if place is None or not place.get('response'):
            return
        places = place['response']['places']
        if exactly_one is True:
            return self.parse_code(places[0])
        else:
            return[self.parse_code(p) for p in places]
