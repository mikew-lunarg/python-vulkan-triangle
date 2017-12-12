#! /usr/bin/python3
# mikew@lunarg.com
# Inspired by https://github.com/gabdube/python-vulkan-triangle

from ctypes import c_void_p, c_float, c_uint8, c_uint, c_uint64, c_int, c_size_t, c_char, c_char_p, cast, Structure, POINTER, pointer, byref
import platform

# Platform library handling #################################################

platform_name = platform.system()
if platform_name == 'Windows':
    from ctypes import WINFUNCTYPE, windll
    FUNCTYPE = WINFUNCTYPE
    vk = windll.LoadLibrary('vulkan-1')
elif platform_name == 'Linux':
    from ctypes import CFUNCTYPE, cdll
    FUNCTYPE = CFUNCTYPE
    vk = cdll.LoadLibrary('libvulkan.so.1')
else:
    raise RuntimeError('Unsupported platform "{}"'.format(platform_name))

def load_functions(vk_object, functions_list, load_func):
    functions = []
    for name, return_type, *args in functions_list:
        py_name = name.decode()
        fn_ptr = load_func(vk_object, name)
        fn_ptr = cast(fn_ptr, c_void_p)
        if not fn_ptr:
            raise RuntimeError('Function {} not found.'.format(py_name))

        fn = (FUNCTYPE(return_type, *args))(fn_ptr.value)
        functions.append((py_name, fn))
    return functions

# Vulkan declarations #######################################################

Instance = c_size_t

InstanceCreateFlags = c_uint

def MAKE_VERSION(major, minor, patch):
    return (major<<22) | (minor<<12) | patch
API_VERSION_1_0 = MAKE_VERSION(1,0,0)
API_VERSION_1_1 = MAKE_VERSION(1,1,0)

StructureType = c_uint
STRUCTURE_TYPE_APPLICATION_INFO = 0
STRUCTURE_TYPE_INSTANCE_CREATE_INFO = 1

Result = c_int
SUCCESS = 0

def define_structure(name, *args):
    return type(name, (Structure,), {'_fields_': args})

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

LoaderFunctions = (
    (b'vkCreateInstance', Result, POINTER(InstanceCreateInfo), c_void_p, POINTER(Instance), ),
)

InstanceFunctions = (
    (b'vkDestroyInstance', None, Instance, c_void_p ),
)

GetInstanceProcAddr = vk.vkGetInstanceProcAddr
GetInstanceProcAddr.restype = FUNCTYPE( None, )
GetInstanceProcAddr.argtypes = (Instance, c_char_p, )

# Structure instances #######################################################

app_info = ApplicationInfo(
    s_type = STRUCTURE_TYPE_APPLICATION_INFO,
    next = None,
    application_name = b'vkCreateInstance.py',
    application_version = 0,
    engine_name = b'',
    engine_version = 0,
    api_version = API_VERSION_1_0
)

create_info = InstanceCreateInfo(
    s_type = STRUCTURE_TYPE_INSTANCE_CREATE_INFO,
    next                    = None,
    flags                   = 0,
    application_info        = pointer(app_info),
    enabled_layer_count     = 0,
    enabled_layer_names     = None,
    enabled_extension_count = 0,
    enabled_extension_names = None
)

# main() ####################################################################

instance = Instance(0)

f=locals()
for name, fnptr in load_functions(instance, LoaderFunctions, GetInstanceProcAddr):
    f[name] = fnptr

result = vkCreateInstance(byref(create_info), None, byref(instance))
if result != SUCCESS:
    raise RuntimeError('CreateInstance() returned {}'.format(result))

f = locals()
for name, fnptr in load_functions(instance, InstanceFunctions, GetInstanceProcAddr):
    f[name] = fnptr

vkDestroyInstance(instance, None)

# eof

