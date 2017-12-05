#!/usr/bin/env python3
# mikew@lunarg.com
# Inspired (long long ago) from https://github.com/gabdube/python-vulkan-triangle

import vk
from ctypes import cast, c_char_p, c_uint, c_ubyte, c_ulonglong, pointer, POINTER, byref, c_float, Structure, sizeof, memmove

class Application(object):

    def create_instance(self):
        print("create_instance")
        app_info = vk.ApplicationInfo(
            s_type = vk.STRUCTURE_TYPE_APPLICATION_INFO,
            next = None,
            application_name = b'PythonText',
            application_version = 0,
            engine_name = b'test',
            engine_version = 0,
            api_version = vk.API_VERSION_1_0
        )

        create_info = vk.InstanceCreateInfo(
            s_type = vk.STRUCTURE_TYPE_INSTANCE_CREATE_INFO,
            next = None,
            flags = 0,
            application_info = pointer(app_info),
            enabled_layer_count = 0,
            enabled_layer_names = None,
            enabled_extension_count = 0,
            enabled_extension_names = None
        )

        instance = vk.Instance(0)
        print("CreateInstance");
        result = vk.CreateInstance(byref(create_info), None, byref(instance))
        if result != vk.SUCCESS:
            raise RuntimeError('CreateInstance failed. result {}'.format(result))

        for name, function in vk.load_functions(instance, vk.InstanceFunctions, vk.GetInstanceProcAddr):
            setattr(self, name, function)
        for name, function in vk.load_functions(instance, vk.PhysicalDeviceFunctions, vk.GetInstanceProcAddr):
            setattr(self, name, function)

        self.instance = instance


    def enumerate_devices(self):
        print("enumerate_devices")
        dev_count = c_uint(0)
        result = self.EnumeratePhysicalDevices(self.instance, byref(dev_count), None)
        if result != vk.SUCCESS or dev_count.value == 0:
            raise RuntimeError('EnumeratePhysicalDevices failed. result {}'.format(result))

        dev_data = (vk.PhysicalDevice * dev_count.value)()
        self.EnumeratePhysicalDevices(self.instance, byref(dev_count), cast(dev_data, POINTER(vk.PhysicalDevice)))

        # just use the first available device
        self.physical_device = vk.PhysicalDevice(dev_data[0])

# dt->GetPhysicalDeviceProperties(physical_device, &pdd.physical_device_properties_);
    def get_device_properties(self):
        print("get_device_properties")
        self.device_properties = vk.PhysicalDeviceMemoryProperties()
        self.GetPhysicalDeviceMemoryProperties(self.physical_device, byref(self.device_properties))


    def get_queue_families(self, physical_device):
        print("get_queue_families")
        qf_count = c_uint(0)
        self.GetPhysicalDeviceQueueFamilyProperties(physical_device, byref(qf_count), None)
        if qf_count.value == 0:
            raise RuntimeError('GetPhysicalDeviceQueueFamilyProperties failed')

        qf_data = (vk.QueueFamilyProperties * qf_count.value)()
        self.GetPhysicalDeviceQueueFamilyProperties(physical_device, byref(qf_count),
            cast(qf_data, POINTER(vk.QueueFamilyProperties)))

    def get_memory_properties(self, physical_device):
        print("get_memory_properties")
        self.memory_properties = vk.PhysicalDeviceMemoryProperties()
        self.GetPhysicalDeviceMemoryProperties(physical_device, byref(self.memory_properties))


    def __init__(self):
        print("__init__")
        self.instance = None
        self.physical_device = None
        self.memory_properties = None
        self.device_properties = None

    def __del__(self):
        print("__del__")
        if self.instance is not None:
            print("DestroyInstance")
            self.DestroyInstance(self.instance, None)
            self.instance = None


def main():
    app = Application()
    app.create_instance()
    app.enumerate_devices()
    app.get_queue_families(app.physical_device)
    app.get_memory_properties(app.physical_device)


if __name__ == '__main__':
    main()
