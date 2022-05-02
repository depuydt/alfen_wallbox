import logging

import requests
import time
from enum import Enum
from datetime import timedelta
import asyncio

from homeassistant.util import Throttle
from .const import DOMAIN

HEADER_JSON = {'content-type': 'application/json; charset=utf-8'}

_LOGGER = logging.getLogger(__name__)

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=30)

class AlfenDevice:

    def __init__(self, host, name, session, username, password):
        self.host = host
        self.name = name
        self._status = None
        self._session = session
        self.username = username
        if self.username is None:
            self.username = 'admin'
        self.password = password
    
    async def init(self):
        await self.async_get_info()
        self.id = 'alfen_{}'.format(self.info.identity)
        if self.name is None:
            self.name = f'{self.info.identity} ({self.host})'
        await self.async_update()

    @property
    def status(self):
        return self._status

    @property
    def device_info(self):
        """Return a device description for device registry."""
        return {
            "identifiers": { (DOMAIN, self.id) },
            "manufacturer": "Alfen",
            "model": self.info.model,
            "name": self.name,
            "firmware": self.info.firmware_version
        }

    def _request(self, parameter_list):
        pass
    
    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def async_update(self):
        await self._do_update()

    async def _do_update(self):
        await self._session.request(method='POST', url=self.__get_url('login'), json={'username': self.username, 'password': self.password})
        response = await self._session.request(method='GET', url=self.__get_url('prop?ids=2060_0,2056_0,2221_3,2221_4,2221_5,2221_A,2221_B,2221_C,2221_16,2201_0'))
        self._session.request(method='POST', url=self.__get_url('logout'))
        response_json = await response.json()
        self._status = AlfenStatus(response_json, self._status)

    async def async_get_info(self):
        response = await self._session.request(method='GET', url=self.__get_url('info'))
        _LOGGER.info(f'Response {response}')
                
        response_json = await response.json()
        self.info = AlfenDeviceInfo(response_json)

    async def reboot_wallbox(self):
        await self._session.post(self.__get_url('cmd'), headers = HEADER_JSON, json={'command': 'reboot'})

    def __get_url(self, action):
        return 'https://{}/servlet/api/{}'.format(self.host, action)

class AlfenStatus:

    def __init__(self,response, prev_status):
        self.uptime = 0
        self.bootups = 0
        self.voltage_l1 = 0
        self.voltage_l2 = 0
        self.voltage_l3 = 0
        self.current_l1 = 0
        self.current_l2 = 0
        self.current_l3 = 0
        self.active_power_total = 0
        self.temperature = 0

class AlfenDeviceInfo:

    def __init__(self,response):
        self.identity = response['Identity']
        self.firmware_version = response['FWVersion']
        self.model = response['Model']
        self.object_id = response['ObjectId']
        self.type = response['Type']