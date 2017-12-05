#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    This is (kind of) a port of https://github.com/SaschaWillems/Vulkan

    @author: Gabriel Dubé
"""
import platform, vk
from ctypes import cast, c_char_p, c_uint, c_ubyte, c_ulonglong, pointer, POINTER, byref, c_float, Structure, sizeof, memmove

#system_name = platform.system()

class Application(object):

    def create_instance(self):
        print("create_instance")
        app_info = vk.ApplicationInfo(
            s_type=vk.STRUCTURE_TYPE_APPLICATION_INFO,
            next=None,
            application_name=b'PythonText',
            application_version=0,
            engine_name=b'test',
            engine_version=0,
            api_version=vk.API_VERSION_1_0
        )

        create_info = vk.InstanceCreateInfo(
            s_type=vk.STRUCTURE_TYPE_INSTANCE_CREATE_INFO,
            next=None,
            flags=0,
            application_info=pointer(app_info),
            enabled_layer_count=0,
            enabled_layer_names=None,
            enabled_extension_count=0,
            enabled_extension_names=None
        )

        instance = vk.Instance(0)
        print("CreateInstance");
        result = vk.CreateInstance(byref(create_info), None, byref(instance))
        if result != vk.SUCCESS:
            raise RuntimeError('CreateInstance failed. Error code: {}'.format(result))

        for name, function in vk.load_functions(instance, vk.InstanceFunctions, vk.GetInstanceProcAddr):
            setattr(self, name, function)
        #for name, function in vk.load_functions(instance, vk.PhysicalDeviceFunctions, vk.GetInstanceProcAddr):
            #setattr(self, name, function)

        self.instance = instance


    def enumerate_devices(self):
        print("enumerate_devices")
        self.gpu = None

        # Enumerate the physical devices
        gpu_count = c_uint(0)
        result = self.EnumeratePhysicalDevices(self.instance, byref(gpu_count), None )
        if result != vk.SUCCESS or gpu_count.value == 0:
            raise RuntimeError('EnumeratePhysicalDevices failed or zero.')

        buf = (vk.PhysicalDevice*gpu_count.value)()
        self.EnumeratePhysicalDevices(self.instance, byref(gpu_count), cast(buf, POINTER(vk.PhysicalDevice)))

        # For this example use the first available device
        self.gpu = vk.PhysicalDevice(buf[0])

    def get_queue_families(self):
        print("get_queue_families")
        queue_families_count = c_uint(0)
        self.GetPhysicalDeviceQueueFamilyProperties( self.gpu, byref(queue_families_count), None)
        if queue_families_count.value == 0:
            raise RuntimeError('queue_families_count = 0.')

        queue_families = (vk.QueueFamilyProperties*queue_families_count.value)()
        self.GetPhysicalDeviceQueueFamilyProperties(
            self.gpu,
            byref(queue_families_count),
            cast(queue_families, POINTER(vk.QueueFamilyProperties))
        )

    def get_memory_properties(self):
        print("get_memory_properties")
        self.memory_properties = vk.PhysicalDeviceMemoryProperties()
        self.GetPhysicalDeviceMemoryProperties(self.gpu, byref(self.memory_properties))


    def __init__(self):
        print("__init__")
        self.instance = None
        self.gpu = None
        self.memory_properties = None

    def __del__(self):
        print("__del__")
        if self.instance is not None:
            print("DestroyInstance")
            self.DestroyInstance(self.instance, None)


def main():
    app = Application()
    app.create_instance()
    app.enumerate_devices()
    #app.get_queue_families()
    #app.get_memory_properties()


if __name__ == '__main__':
    main()
