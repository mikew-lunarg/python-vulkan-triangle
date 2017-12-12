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

VkInstance = c_size_t

VkInstanceCreateFlags = c_uint

def VK_MAKE_VERSION(major, minor, patch):
    return (major<<22) | (minor<<12) | patch
VK_API_VERSION_1_0 = VK_MAKE_VERSION(1,0,0)
VK_API_VERSION_1_1 = VK_MAKE_VERSION(1,1,0)

VkStructureType = c_uint
VK_STRUCTURE_TYPE_APPLICATION_INFO = 0
VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO = 1

VkResult = c_int
VK_SUCCESS = 0

def define_struct(name, *args):
    return type(name, (Structure,), {'_fields_': args})

VkApplicationInfo = define_struct('ApplicationInfo',
    ('sType', VkStructureType),
    ('pNext', c_void_p),
    ('pApplicationName', c_char_p),
    ('applicationVersion', c_uint),
    ('pEngineName', c_char_p),
    ('engineVersion', c_uint),
    ('apiVersion', c_uint),
)

VkInstanceCreateInfo = define_struct('instancecreateinfo',
    ('sType', VkStructureType),
    ('pNext', c_void_p),
    ('flags', VkInstanceCreateFlags),
    ('pApplicationInfo', POINTER(VkApplicationInfo)),
    ('enabledLayerCount', c_uint),
    ('ppEnabledLayerNames', POINTER(c_char_p)),
    ('enabledExtensionCount', c_uint),
    ('ppEnabledExtensionNames', POINTER(c_char_p)),
)

LoaderFunctions = (
    (b'vkCreateInstance', VkResult, POINTER(VkInstanceCreateInfo), c_void_p, POINTER(VkInstance), ),
)

InstanceFunctions = (
    (b'vkDestroyInstance', None, VkInstance, c_void_p ),
)

GetInstanceProcAddr = vk.vkGetInstanceProcAddr
GetInstanceProcAddr.restype = FUNCTYPE( None, )
GetInstanceProcAddr.argtypes = (VkInstance, c_char_p, )

# Structure instances #######################################################

app_info = VkApplicationInfo(
    sType = VK_STRUCTURE_TYPE_APPLICATION_INFO,
    pNext = None,
    pApplicationName = b'CreateInstanceVersion.py',
    applicationVersion = 0,
    pEngineName = b'',
    engineVersion = 0,
    apiVersion = VK_API_VERSION_1_1
)

create_info = VkInstanceCreateInfo(
    sType = VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO,
    pNext                    = None,
    flags                   = 0,
    pApplicationInfo        = pointer(app_info),
    enabledLayerCount     = 0,
    ppEnabledLayerNames     = None,
    enabledExtensionCount = 0,
    ppEnabledExtensionNames = None
)

# main() ####################################################################

inst = VkInstance(0)

f=locals()
for name, fnptr in load_functions(inst, LoaderFunctions, GetInstanceProcAddr):
    f[name] = fnptr

result = vkCreateInstance(byref(create_info), None, byref(inst))
print('vkCreateInstance() returned {}'.format(result))
if result != VK_SUCCESS:
    raise RuntimeError('vkCreateInstance() failed')

f = locals()
for name, fnptr in load_functions(inst, InstanceFunctions, GetInstanceProcAddr):
    f[name] = fnptr

vkDestroyInstance(inst, None)

# eof

