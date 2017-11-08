#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    This is (kind of) a port of https://github.com/SaschaWillems/Vulkan

    @author: Gabriel Dubé
"""
import platform, vk, weakref
from ctypes import cast, c_char_p, c_uint, c_ubyte, c_ulonglong, pointer, POINTER, byref, c_float, Structure, sizeof, memmove
from itertools import chain

system_name = platform.system()

class Application(object):

    def create_instance(self):
        """
            Setup the vulkan instance
        """
        print("create_instance 000")
        app_info = vk.ApplicationInfo(
            s_type=vk.STRUCTURE_TYPE_APPLICATION_INFO,
            next=None,
            application_name=b'PythonText',
            application_version=0,
            engine_name=b'test',
            engine_version=0,
            api_version=vk.API_VERSION_1_0
        )

        layer_count = 0
        _layer_names = None

        create_info = vk.InstanceCreateInfo(
            s_type=vk.STRUCTURE_TYPE_INSTANCE_CREATE_INFO,
            next=None,
            flags=0,
            application_info=pointer(app_info),
            enabled_layer_count=layer_count,
            enabled_layer_names=_layer_names,
            enabled_extension_count=0,
            enabled_extension_names=None
        )

        instance = vk.Instance(0)
        result = vk.CreateInstance(byref(create_info), None, byref(instance))
        print("create_instance 900")
        if result == vk.SUCCESS:
            # For simplicity, all vulkan functions are saved in the application object
            functions = chain(vk.load_functions(instance, vk.InstanceFunctions, vk.GetInstanceProcAddr),
                              vk.load_functions(instance, vk.PhysicalDeviceFunctions, vk.GetInstanceProcAddr))
            for name, function in functions:
                setattr(self, name, function)

            self.instance = instance

        else:
            raise RuntimeError('Instance creation failed. Error code: {}'.format(result))

    def create_device(self):
        self.gpu = None

        # Enumerate the physical devices
        gpu_count = c_uint(0)
        result = self.EnumeratePhysicalDevices(self.instance, byref(gpu_count), None )
        if result != vk.SUCCESS or gpu_count.value == 0:
            raise RuntimeError('Could not fetch the physical devices or there are no devices available')

        buf = (vk.PhysicalDevice*gpu_count.value)()
        self.EnumeratePhysicalDevices(self.instance, byref(gpu_count), cast(buf, POINTER(vk.PhysicalDevice)))


        # For this example use the first available device
        self.gpu = vk.PhysicalDevice(buf[0])

        # Find a graphic queue that supports graphic operation and presentation into
        # the surface previously created
        queue_families_count = c_uint(0)
        self.GetPhysicalDeviceQueueFamilyProperties(
            self.gpu,
            byref(queue_families_count),
            None
        )

        if queue_families_count.value == 0:
            raise RuntimeError('No queues families found for the default GPU')

        queue_families = (vk.QueueFamilyProperties*queue_families_count.value)()
        self.GetPhysicalDeviceQueueFamilyProperties(
            self.gpu,
            byref(queue_families_count),
            cast(queue_families, POINTER(vk.QueueFamilyProperties))
        )

        # Get the physical device memory properties.
        self.gpu_mem = vk.PhysicalDeviceMemoryProperties()
        self.GetPhysicalDeviceMemoryProperties(self.gpu, byref(self.gpu_mem))





    def __init__(self):
        # Vulkan objets
        self.instance = None
        self.gpu = None
        self.gpu_mem = None
        self.device = None

        # Vulkan objets initialization
        self.create_instance()
        self.create_device()

    def __del__(self):
        if self.instance is None:
            return

        dev = self.device
        if dev is not None:
            self.DestroyDevice(dev, None)

        self.DestroyInstance(self.instance, None)
        print('Application freed!')


def main():
    app = Application()

if __name__ == '__main__':
    main()
