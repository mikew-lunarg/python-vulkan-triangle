# vk.py
# mikew@lunarg.com
# Derived (long long ago) from https://github.com/gabdube/python-vulkan-triangle

from ctypes import (c_void_p, c_float, c_uint8, c_uint, c_uint64, c_int, c_size_t, c_char, c_char_p, cast, Structure, POINTER)
import platform

# platform-specific library initialization
system_name = platform.system()
if system_name == 'Windows':
    from ctypes import WINFUNCTYPE, windll
    FUNCTYPE = WINFUNCTYPE
    vk = windll.LoadLibrary('vulkan-1')
elif system_name == 'Linux':
    from ctypes import CFUNCTYPE, cdll
    FUNCTYPE = CFUNCTYPE
    vk = cdll.LoadLibrary('libvulkan.so.1')

def MAKE_VERSION(major, minor, patch):
    return (major<<22) | (minor<<12) | patch
API_VERSION_1_0 = MAKE_VERSION(1,0,0)
API_VERSION_1_1 = MAKE_VERSION(1,1,0)

def define_structure(name, *args):
    return type(name, (Structure,), {'_fields_': args})

def load_functions(vk_object, functions_list, load_func):
    functions = []
    for name, return_type, *args in functions_list:
        py_name = name.decode()[2::]
        fn_ptr = load_func(vk_object, name)
        fn_ptr = cast(fn_ptr, c_void_p)
        if fn_ptr:
            fn = (FUNCTYPE(return_type, *args))(fn_ptr.value)
            functions.append((py_name, fn))
        else:
            print('Function {} not found.'.format(py_name))
    return functions

# HANDLES
Instance = c_size_t

# FLAGS
InstanceCreateFlags = c_uint

# ENUMS
StructureType = c_uint
STRUCTURE_TYPE_APPLICATION_INFO = 0
STRUCTURE_TYPE_INSTANCE_CREATE_INFO = 1

Result = c_uint
SUCCESS = 0

# STRUCTURES
ApplicationInfo = define_structure('ApplicationInfo',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('application_name', c_char_p),
    ('application_version', c_uint),
    ('engine_name', c_char_p),
    ('engine_version', c_uint),
    ('api_version', c_uint),
)

InstanceCreateInfo = define_structure('InstanceCreateInfo',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('flags', InstanceCreateFlags),
    ('application_info', POINTER(ApplicationInfo)),
    ('enabled_layer_count', c_uint),
    ('enabled_layer_names', POINTER(c_char_p)),
    ('enabled_extension_count', c_uint),
    ('enabled_extension_names', POINTER(c_char_p)),
)

# FUNCTIONS

LoaderFunctions = (
    (b'vkCreateInstance', Result, POINTER(InstanceCreateInfo), c_void_p, POINTER(Instance), ),
)

InstanceFunctions = (
    (b'vkDestroyInstance', None, Instance, c_void_p ),
)

GetInstanceProcAddr = vk.vkGetInstanceProcAddr
GetInstanceProcAddr.restype = FUNCTYPE( None, )
GetInstanceProcAddr.argtypes = (Instance, c_char_p, )

