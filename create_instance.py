#! /usr/bin/env python
# mikew@lunarg.com
# Derived (long long ago) from https://github.com/gabdube/python-vulkan-triangle

import vk
from ctypes import cast, c_char_p, c_uint, c_ubyte, c_ulonglong, pointer, POINTER, byref, c_float, Structure, sizeof, memmove

class Application(object):

    def create_instance(self):
        print('create_instance')
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
        print('CreateInstance');
        result = vk.CreateInstance(byref(create_info), None, byref(instance))
        if result != vk.SUCCESS:
            raise RuntimeError('CreateInstance failed. result {}'.format(result))

        for name, function in vk.load_functions(instance, vk.InstanceFunctions, vk.GetInstanceProcAddr):
            setattr(self, name, function)

        self.instance = instance

    def __init__(self):
        print('__init__')
        self.instance = None

    def __del__(self):
        print('__del__')
        if self.instance is not None:
            print('DestroyInstance')
            self.DestroyInstance(self.instance, None)
            self.instance = None


def main():
    app = Application()
    app.create_instance()

if __name__ == '__main__':
    main()
