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

def load_functions(vk_object, functions_list, loader):
    functions = []
    for name, return_type, *args in functions_list:
        py_name = name.decode()[2::]
        fn_ptr = loader(vk_object, name)
        fn_ptr = cast(fn_ptr, c_void_p)
        if fn_ptr:
            fn = (FUNCTYPE(return_type, *args))(fn_ptr.value)
            functions.append((py_name, fn))
        elif __debug__ == True:
            print('Function {} could not be loaded. (__debug__ == True)'.format(py_name))
    return functions

# HANDLES
Instance = c_size_t

# FLAGS
InstanceCreateFlags = c_uint

# ENUMS
API_Constants = c_uint
MAX_PHYSICAL_DEVICE_NAME_SIZE = 256
UUID_SIZE = 16
MAX_EXTENSION_NAME_SIZE = 256
MAX_DESCRIPTION_SIZE = 256
MAX_MEMORY_TYPES = 32
MAX_MEMORY_HEAPS = 16
LOD_CLAMP_NONE = c_float(1000.0)
REMAINING_MIP_LEVELS = c_uint(~0)
REMAINING_ARRAY_LAYERS = c_uint(~0)
WHOLE_SIZE = c_uint64(~0)
ATTACHMENT_UNUSED = c_uint(~0)
TRUE = 1
FALSE = 0

StructureType = c_uint
STRUCTURE_TYPE_APPLICATION_INFO = 0
STRUCTURE_TYPE_INSTANCE_CREATE_INFO = 1

Result = c_uint
SUCCESS = 0
NOT_READY = 1
TIMEOUT = 2
EVENT_SET = 3
EVENT_RESET = 4
INCOMPLETE = 5
ERROR_OUT_OF_HOST_MEMORY = -1
ERROR_OUT_OF_DEVICE_MEMORY = -2
ERROR_INITIALIZATION_FAILED = -3
ERROR_DEVICE_LOST = -4
ERROR_MEMORY_MAP_FAILED = -5
ERROR_LAYER_NOT_PRESENT = -6
ERROR_EXTENSION_NOT_PRESENT = -7
ERROR_FEATURE_NOT_PRESENT = -8
ERROR_INCOMPATIBLE_DRIVER = -9
ERROR_TOO_MANY_OBJECTS = -10
ERROR_FORMAT_NOT_SUPPORTED = -11
ERROR_FRAGMENTED_POOL = -12

# FUNC POINTERS
fn_VoidFunction = FUNCTYPE( None, )

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
GetInstanceProcAddr.restype = fn_VoidFunction
GetInstanceProcAddr.argtypes = (Instance, c_char_p, )

# Load the loader functions in the module namespace
loc = locals()
for name, fnptr in load_functions(Instance(0), LoaderFunctions, GetInstanceProcAddr):
    loc[name] = fnptr
del loc

