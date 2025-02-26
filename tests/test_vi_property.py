import os
import configparser
from unittest import TestCase

from pysphere import VIServer, VIProperty, VIMor

class VIPropertyTest(TestCase):

    @classmethod
    def setUpClass(cls):
        config_path = os.path.join(os.path.dirname(__file__), "config.ini")
        cls.config = configparser.ConfigParser()
        cls.config.read(config_path)
        
        host = cls.config.get("READ_ONLY_ENV", "host")
        user = cls.config.get("READ_ONLY_ENV", "user")
        pswd = cls.config.get("READ_ONLY_ENV", "password")
        
        cls.server = VIServer()
        cls.server.connect(host, user, pswd)

    @classmethod
    def tearDownClass(cls):
        cls.server.disconnect()

    def test_property_types(self):
        hosts = self.server.get_hosts()
        for hmor, hname in hosts.items():
            p = VIProperty(self.server, hmor)
            assert p.name == hname
            #string
            assert isinstance(p.name, str)
            #property mor
            assert VIMor.is_mor(p._obj)
            #nested properties
            assert isinstance(p.configManager, VIProperty)
            #bool
            assert isinstance(p.runtime.inMaintenanceMode, bool)
            #list
            assert isinstance(p.vm, list)
            #mor without traversing
            assert VIMor.is_mor(p.vm[0]._obj)
            #traversing
            assert isinstance(p.vm[0].name, str)
            #enum
            assert p.runtime.powerState in ['poweredOff', 'poweredOn',
                                            'standBy', 'unknown']
            #int
            assert isinstance(p.summary.config.port, int)
            #long
            assert isinstance(p.hardware.memorySize, int)
            #short as int
            assert isinstance(p.hardware.cpuInfo.numCpuCores, int)
            #date as tuple
            assert isinstance(p.runtime.bootTime, tuple)
            #check property cache
            assert "runtime" in list(p.__dict__.keys())
            assert "memorySize" in list(p.hardware.__dict__.keys())
            assert "numCpuCores" in list(p.hardware.cpuInfo.__dict__.keys())
            assert "name" in list(p.vm[0].__dict__.keys())
            #check cache flush
            p._flush_cache()
            assert "runtime" not in list(p.__dict__.keys())
            assert "memorySize" not in list(p.hardware.__dict__.keys())
            assert "numCpuCores" not in list(p.hardware.cpuInfo.__dict__.keys())
            assert "name" not in list(p.vm[0].__dict__.keys())
            #check unexistent property
            try:
                p.hoochiemama
            except AttributeError:
                pass
            except:
                raise AssertionError("Attribute Error expected")
            else:
                raise AssertionError("Attribute Error expected")