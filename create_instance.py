#! /usr/bin/env python
# mikew@lunarg.com
# Derived (long long ago) from https://github.com/gabdube/python-vulkan-triangle

import vk
from ctypes import cast, c_char_p, c_uint, c_int, c_ubyte, c_ulonglong, pointer, POINTER, byref, c_float, Structure, sizeof, memmove

def main():

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
            raise RuntimeError('CreateInstance failed. result {}'.format(c_int(result)))

        f = vars(vk)
        for name, fnptr in vk.load_functions(instance, vk.InstanceFunctions, vk.GetInstanceProcAddr):
            f[name] = fnptr

        print('CreateInstance result {}'.format(c_int(result)))
        print('DestroyInstance')
        vk.DestroyInstance(instance, None)
        instance = None

if __name__ == '__main__':
    main()
