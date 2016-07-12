"""
    Thin wrapper over the vulkan API using ctypes.
    This wrapper is incomplete and should'nt be used outside this demo
"""

from ctypes import *
from sys import modules

### NON VULKAN VALUES ###

NULL = c_void_p(0)
NULL_LAYERS = cast(NULL, POINTER(c_char_p))
NULL_HANDLE = c_size_t(0)

### HANDLES ###

Instance = c_size_t
PhysicalDevice = c_size_t
Device = c_size_t
Queue = c_size_t
CommandBuffer = c_size_t
DeviceMemory = c_size_t
CommandPool = c_size_t
Buffer = c_size_t
BufferView = c_size_t
Image = c_size_t
ImageView = c_size_t
ShaderModule = c_size_t
Pipeline = c_size_t
PipelineLayout = c_size_t
Sampler = c_size_t
DescriptorSet = c_size_t
DescriptorSetLayout = c_size_t
DescriptorPool = c_size_t
Fence = c_size_t
Semaphore = c_size_t
Event = c_size_t
QueryPool = c_size_t
Framebuffer = c_size_t
RenderPass = c_size_t
PipelineCache = c_size_t
DisplayKHR = c_size_t
DisplayModeKHR = c_size_t
SurfaceKHR = c_size_t
SwapchainKHR = c_size_t
DebugReportCallbackEXT = c_size_t

### ENUMS ###

# VkImageLayout
IMAGE_LAYOUT_UNDEFINED = 0
IMAGE_LAYOUT_GENERAL = 1
IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL = 2
IMAGE_LAYOUT_DEPTH_STENCIL_ATTACHMENT_OPTIMAL = 3
IMAGE_LAYOUT_DEPTH_STENCIL_READ_ONLY_OPTIMAL = 4
IMAGE_LAYOUT_SHADER_READ_ONLY_OPTIMAL = 5
IMAGE_LAYOUT_TRANSFER_SRC_OPTIMAL = 6
IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL = 7
IMAGE_LAYOUT_PREINITIALIZED = 8

# VkAttachmentLoadOp
ATTACHMENT_LOAD_OP_LOAD = 0
ATTACHMENT_LOAD_OP_CLEAR = 1
ATTACHMENT_LOAD_OP_DONT_CARE = 2

# VkAttachmentStoreOp
ATTACHMENT_STORE_OP_STORE = 0
ATTACHMENT_STORE_OP_DONT_CARE = 1

# VkImageType
IMAGE_TYPE_1D = 0
IMAGE_TYPE_2D = 1
IMAGE_TYPE_3D = 2

# VkImageTiling
IMAGE_TILING_OPTIMAL = 0
IMAGE_TILING_LINEAR = 1

# VkImageViewType
IMAGE_VIEW_TYPE_1D = 0
IMAGE_VIEW_TYPE_2D = 1
IMAGE_VIEW_TYPE_3D = 2
IMAGE_VIEW_TYPE_CUBE = 3
IMAGE_VIEW_TYPE_1D_ARRAY = 4
IMAGE_VIEW_TYPE_2D_ARRAY = 5
IMAGE_VIEW_TYPE_CUBE_ARRAY = 6

# VkCommandBufferLevel
COMMAND_BUFFER_LEVEL_PRIMARY = 0
COMMAND_BUFFER_LEVEL_SECONDARY = 1

# VkComponentSwizzle
COMPONENT_SWIZZLE_IDENTITY = 0
COMPONENT_SWIZZLE_ZERO = 1
COMPONENT_SWIZZLE_ONE = 2
COMPONENT_SWIZZLE_R = 3
COMPONENT_SWIZZLE_G = 4
COMPONENT_SWIZZLE_B = 5
COMPONENT_SWIZZLE_A = 6

# VkDescriptorType
DESCRIPTOR_TYPE_SAMPLER = 0
DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER = 1
DESCRIPTOR_TYPE_SAMPLED_IMAGE = 2
DESCRIPTOR_TYPE_STORAGE_IMAGE = 3
DESCRIPTOR_TYPE_UNIFORM_TEXEL_BUFFER = 4
DESCRIPTOR_TYPE_STORAGE_TEXEL_BUFFER = 5
DESCRIPTOR_TYPE_UNIFORM_BUFFER = 6
DESCRIPTOR_TYPE_STORAGE_BUFFER = 7
DESCRIPTOR_TYPE_UNIFORM_BUFFER_DYNAMIC = 8
DESCRIPTOR_TYPE_STORAGE_BUFFER_DYNAMIC = 9
DESCRIPTOR_TYPE_INPUT_ATTACHMENT = 10

# VkQueryType
QUERY_TYPE_OCCLUSION = 0
QUERY_TYPE_PIPELINE_STATISTICS = 1
QUERY_TYPE_TIMESTAMP = 2

# VkBorderColor
BORDER_COLOR_FLOAT_TRANSPARENT_BLACK = 0
BORDER_COLOR_INT_TRANSPARENT_BLACK = 1
BORDER_COLOR_FLOAT_OPAQUE_BLACK = 2
BORDER_COLOR_INT_OPAQUE_BLACK = 3
BORDER_COLOR_FLOAT_OPAQUE_WHITE = 4
BORDER_COLOR_INT_OPAQUE_WHITE = 5

# VkPipelineBindPoint
PIPELINE_BIND_POINT_GRAPHICS = 0
PIPELINE_BIND_POINT_COMPUTE = 1

# VkPipelineCacheHeaderVersion
PIPELINE_CACHE_HEADER_VERSION_ONE = 1

# VkPrimitiveTopology
PRIMITIVE_TOPOLOGY_POINT_LIST = 0
PRIMITIVE_TOPOLOGY_LINE_LIST = 1
PRIMITIVE_TOPOLOGY_LINE_STRIP = 2
PRIMITIVE_TOPOLOGY_TRIANGLE_LIST = 3
PRIMITIVE_TOPOLOGY_TRIANGLE_STRIP = 4
PRIMITIVE_TOPOLOGY_TRIANGLE_FAN = 5
PRIMITIVE_TOPOLOGY_LINE_LIST_WITH_ADJACENCY = 6
PRIMITIVE_TOPOLOGY_LINE_STRIP_WITH_ADJACENCY = 7
PRIMITIVE_TOPOLOGY_TRIANGLE_LIST_WITH_ADJACENCY = 8
PRIMITIVE_TOPOLOGY_TRIANGLE_STRIP_WITH_ADJACENCY = 9
PRIMITIVE_TOPOLOGY_PATCH_LIST = 10

# VkSharingMode
SHARING_MODE_EXCLUSIVE = 0
SHARING_MODE_CONCURRENT = 1

# VkIndexType
INDEX_TYPE_UINT16 = 0
INDEX_TYPE_UINT32 = 1

# VkFilter
FILTER_NEAREST = 0
FILTER_LINEAR = 1

# VkSamplerMipmapMode
SAMPLER_MIPMAP_MODE_NEAREST = 0
SAMPLER_MIPMAP_MODE_LINEAR = 1

# VkSamplerAddressMode
SAMPLER_ADDRESS_MODE_REPEAT = 0
SAMPLER_ADDRESS_MODE_MIRRORED_REPEAT = 1
SAMPLER_ADDRESS_MODE_CLAMP_TO_EDGE = 2
SAMPLER_ADDRESS_MODE_CLAMP_TO_BORDER = 3

# VkCompareOp
COMPARE_OP_NEVER = 0
COMPARE_OP_LESS = 1
COMPARE_OP_EQUAL = 2
COMPARE_OP_LESS_OR_EQUAL = 3
COMPARE_OP_GREATER = 4
COMPARE_OP_NOT_EQUAL = 5
COMPARE_OP_GREATER_OR_EQUAL = 6
COMPARE_OP_ALWAYS = 7

# VkPolygonMode
POLYGON_MODE_FILL = 0
POLYGON_MODE_LINE = 1
POLYGON_MODE_POINT = 2

# VkCullModeFlagBits
CULL_MODE_NONE = 0
CULL_MODE_FRONT_BIT = 1<<0
CULL_MODE_BACK_BIT = 1<<1
CULL_MODE_FRONT_AND_BACK = 0x00000003

# VkFrontFace
FRONT_FACE_COUNTER_CLOCKWISE = 0
FRONT_FACE_CLOCKWISE = 1

# VkBlendFactor
BLEND_FACTOR_ZERO = 0
BLEND_FACTOR_ONE = 1
BLEND_FACTOR_SRC_COLOR = 2
BLEND_FACTOR_ONE_MINUS_SRC_COLOR = 3
BLEND_FACTOR_DST_COLOR = 4
BLEND_FACTOR_ONE_MINUS_DST_COLOR = 5
BLEND_FACTOR_SRC_ALPHA = 6
BLEND_FACTOR_ONE_MINUS_SRC_ALPHA = 7
BLEND_FACTOR_DST_ALPHA = 8
BLEND_FACTOR_ONE_MINUS_DST_ALPHA = 9
BLEND_FACTOR_CONSTANT_COLOR = 10
BLEND_FACTOR_ONE_MINUS_CONSTANT_COLOR = 11
BLEND_FACTOR_CONSTANT_ALPHA = 12
BLEND_FACTOR_ONE_MINUS_CONSTANT_ALPHA = 13
BLEND_FACTOR_SRC_ALPHA_SATURATE = 14
BLEND_FACTOR_SRC1_COLOR = 15
BLEND_FACTOR_ONE_MINUS_SRC1_COLOR = 16
BLEND_FACTOR_SRC1_ALPHA = 17
BLEND_FACTOR_ONE_MINUS_SRC1_ALPHA = 18

# VkBlendOp
BLEND_OP_ADD = 0
BLEND_OP_SUBTRACT = 1
BLEND_OP_REVERSE_SUBTRACT = 2
BLEND_OP_MIN = 3
BLEND_OP_MAX = 4

# VkStencilOp
STENCIL_OP_KEEP = 0
STENCIL_OP_ZERO = 1
STENCIL_OP_REPLACE = 2
STENCIL_OP_INCREMENT_AND_CLAMP = 3
STENCIL_OP_DECREMENT_AND_CLAMP = 4
STENCIL_OP_INVERT = 5
STENCIL_OP_INCREMENT_AND_WRAP = 6
STENCIL_OP_DECREMENT_AND_WRAP = 7

# VkLogicOp
LOGIC_OP_CLEAR = 0
LOGIC_OP_AND = 1
LOGIC_OP_AND_REVERSE = 2
LOGIC_OP_COPY = 3
LOGIC_OP_AND_INVERTED = 4
LOGIC_OP_NO_OP = 5
LOGIC_OP_XOR = 6
LOGIC_OP_OR = 7
LOGIC_OP_NOR = 8
LOGIC_OP_EQUIVALENT = 9
LOGIC_OP_INVERT = 10
LOGIC_OP_OR_REVERSE = 11
LOGIC_OP_COPY_INVERTED = 12
LOGIC_OP_OR_INVERTED = 13
LOGIC_OP_NAND = 14
LOGIC_OP_SET = 15

# VkInternalAllocationType
INTERNAL_ALLOCATION_TYPE_EXECUTABLE = 0

# VkSystemAllocationScope
SYSTEM_ALLOCATION_SCOPE_COMMAND = 0
SYSTEM_ALLOCATION_SCOPE_OBJECT = 1
SYSTEM_ALLOCATION_SCOPE_CACHE = 2
SYSTEM_ALLOCATION_SCOPE_DEVICE = 3
SYSTEM_ALLOCATION_SCOPE_INSTANCE = 4

# VkPhysicalDeviceType
PHYSICAL_DEVICE_TYPE_OTHER = 0
PHYSICAL_DEVICE_TYPE_INTEGRATED_GPU = 1
PHYSICAL_DEVICE_TYPE_DISCRETE_GPU = 2
PHYSICAL_DEVICE_TYPE_VIRTUAL_GPU = 3
PHYSICAL_DEVICE_TYPE_CPU = 4

# VkVertexInputRate
VERTEX_INPUT_RATE_VERTEX = 0
VERTEX_INPUT_RATE_INSTANCE = 1

# VkFormat
FORMAT_UNDEFINED = 0
FORMAT_R4G4_UNORM_PACK8 = 1
FORMAT_R4G4B4A4_UNORM_PACK16 = 2
FORMAT_B4G4R4A4_UNORM_PACK16 = 3
FORMAT_R5G6B5_UNORM_PACK16 = 4
FORMAT_B5G6R5_UNORM_PACK16 = 5
FORMAT_R5G5B5A1_UNORM_PACK16 = 6
FORMAT_B5G5R5A1_UNORM_PACK16 = 7
FORMAT_A1R5G5B5_UNORM_PACK16 = 8
FORMAT_R8_UNORM = 9
FORMAT_R8_SNORM = 10
FORMAT_R8_USCALED = 11
FORMAT_R8_SSCALED = 12
FORMAT_R8_UINT = 13
FORMAT_R8_SINT = 14
FORMAT_R8_SRGB = 15
FORMAT_R8G8_UNORM = 16
FORMAT_R8G8_SNORM = 17
FORMAT_R8G8_USCALED = 18
FORMAT_R8G8_SSCALED = 19
FORMAT_R8G8_UINT = 20
FORMAT_R8G8_SINT = 21
FORMAT_R8G8_SRGB = 22
FORMAT_R8G8B8_UNORM = 23
FORMAT_R8G8B8_SNORM = 24
FORMAT_R8G8B8_USCALED = 25
FORMAT_R8G8B8_SSCALED = 26
FORMAT_R8G8B8_UINT = 27
FORMAT_R8G8B8_SINT = 28
FORMAT_R8G8B8_SRGB = 29
FORMAT_B8G8R8_UNORM = 30
FORMAT_B8G8R8_SNORM = 31
FORMAT_B8G8R8_USCALED = 32
FORMAT_B8G8R8_SSCALED = 33
FORMAT_B8G8R8_UINT = 34
FORMAT_B8G8R8_SINT = 35
FORMAT_B8G8R8_SRGB = 36
FORMAT_R8G8B8A8_UNORM = 37
FORMAT_R8G8B8A8_SNORM = 38
FORMAT_R8G8B8A8_USCALED = 39
FORMAT_R8G8B8A8_SSCALED = 40
FORMAT_R8G8B8A8_UINT = 41
FORMAT_R8G8B8A8_SINT = 42
FORMAT_R8G8B8A8_SRGB = 43
FORMAT_B8G8R8A8_UNORM = 44
FORMAT_B8G8R8A8_SNORM = 45
FORMAT_B8G8R8A8_USCALED = 46
FORMAT_B8G8R8A8_SSCALED = 47
FORMAT_B8G8R8A8_UINT = 48
FORMAT_B8G8R8A8_SINT = 49
FORMAT_B8G8R8A8_SRGB = 50
FORMAT_A8B8G8R8_UNORM_PACK32 = 51
FORMAT_A8B8G8R8_SNORM_PACK32 = 52
FORMAT_A8B8G8R8_USCALED_PACK32 = 53
FORMAT_A8B8G8R8_SSCALED_PACK32 = 54
FORMAT_A8B8G8R8_UINT_PACK32 = 55
FORMAT_A8B8G8R8_SINT_PACK32 = 56
FORMAT_A8B8G8R8_SRGB_PACK32 = 57
FORMAT_A2R10G10B10_UNORM_PACK32 = 58
FORMAT_A2R10G10B10_SNORM_PACK32 = 59
FORMAT_A2R10G10B10_USCALED_PACK32 = 60
FORMAT_A2R10G10B10_SSCALED_PACK32 = 61
FORMAT_A2R10G10B10_UINT_PACK32 = 62
FORMAT_A2R10G10B10_SINT_PACK32 = 63
FORMAT_A2B10G10R10_UNORM_PACK32 = 64
FORMAT_A2B10G10R10_SNORM_PACK32 = 65
FORMAT_A2B10G10R10_USCALED_PACK32 = 66
FORMAT_A2B10G10R10_SSCALED_PACK32 = 67
FORMAT_A2B10G10R10_UINT_PACK32 = 68
FORMAT_A2B10G10R10_SINT_PACK32 = 69
FORMAT_R16_UNORM = 70
FORMAT_R16_SNORM = 71
FORMAT_R16_USCALED = 72
FORMAT_R16_SSCALED = 73
FORMAT_R16_UINT = 74
FORMAT_R16_SINT = 75
FORMAT_R16_SFLOAT = 76
FORMAT_R16G16_UNORM = 77
FORMAT_R16G16_SNORM = 78
FORMAT_R16G16_USCALED = 79
FORMAT_R16G16_SSCALED = 80
FORMAT_R16G16_UINT = 81
FORMAT_R16G16_SINT = 82
FORMAT_R16G16_SFLOAT = 83
FORMAT_R16G16B16_UNORM = 84
FORMAT_R16G16B16_SNORM = 85
FORMAT_R16G16B16_USCALED = 86
FORMAT_R16G16B16_SSCALED = 87
FORMAT_R16G16B16_UINT = 88
FORMAT_R16G16B16_SINT = 89
FORMAT_R16G16B16_SFLOAT = 90
FORMAT_R16G16B16A16_UNORM = 91
FORMAT_R16G16B16A16_SNORM = 92
FORMAT_R16G16B16A16_USCALED = 93
FORMAT_R16G16B16A16_SSCALED = 94
FORMAT_R16G16B16A16_UINT = 95
FORMAT_R16G16B16A16_SINT = 96
FORMAT_R16G16B16A16_SFLOAT = 97
FORMAT_R32_UINT = 98
FORMAT_R32_SINT = 99
FORMAT_R32_SFLOAT = 100
FORMAT_R32G32_UINT = 101
FORMAT_R32G32_SINT = 102
FORMAT_R32G32_SFLOAT = 103
FORMAT_R32G32B32_UINT = 104
FORMAT_R32G32B32_SINT = 105
FORMAT_R32G32B32_SFLOAT = 106
FORMAT_R32G32B32A32_UINT = 107
FORMAT_R32G32B32A32_SINT = 108
FORMAT_R32G32B32A32_SFLOAT = 109
FORMAT_R64_UINT = 110
FORMAT_R64_SINT = 111
FORMAT_R64_SFLOAT = 112
FORMAT_R64G64_UINT = 113
FORMAT_R64G64_SINT = 114
FORMAT_R64G64_SFLOAT = 115
FORMAT_R64G64B64_UINT = 116
FORMAT_R64G64B64_SINT = 117
FORMAT_R64G64B64_SFLOAT = 118
FORMAT_R64G64B64A64_UINT = 119
FORMAT_R64G64B64A64_SINT = 120
FORMAT_R64G64B64A64_SFLOAT = 121
FORMAT_B10G11R11_UFLOAT_PACK32 = 122
FORMAT_E5B9G9R9_UFLOAT_PACK32 = 123
FORMAT_D16_UNORM = 124
FORMAT_X8_D24_UNORM_PACK32 = 125
FORMAT_D32_SFLOAT = 126
FORMAT_S8_UINT = 127
FORMAT_D16_UNORM_S8_UINT = 128
FORMAT_D24_UNORM_S8_UINT = 129
FORMAT_D32_SFLOAT_S8_UINT = 130
FORMAT_BC1_RGB_UNORM_BLOCK = 131
FORMAT_BC1_RGB_SRGB_BLOCK = 132
FORMAT_BC1_RGBA_UNORM_BLOCK = 133
FORMAT_BC1_RGBA_SRGB_BLOCK = 134
FORMAT_BC2_UNORM_BLOCK = 135
FORMAT_BC2_SRGB_BLOCK = 136
FORMAT_BC3_UNORM_BLOCK = 137
FORMAT_BC3_SRGB_BLOCK = 138
FORMAT_BC4_UNORM_BLOCK = 139
FORMAT_BC4_SNORM_BLOCK = 140
FORMAT_BC5_UNORM_BLOCK = 141
FORMAT_BC5_SNORM_BLOCK = 142
FORMAT_BC6H_UFLOAT_BLOCK = 143
FORMAT_BC6H_SFLOAT_BLOCK = 144
FORMAT_BC7_UNORM_BLOCK = 145
FORMAT_BC7_SRGB_BLOCK = 146
FORMAT_ETC2_R8G8B8_UNORM_BLOCK = 147
FORMAT_ETC2_R8G8B8_SRGB_BLOCK = 148
FORMAT_ETC2_R8G8B8A1_UNORM_BLOCK = 149
FORMAT_ETC2_R8G8B8A1_SRGB_BLOCK = 150
FORMAT_ETC2_R8G8B8A8_UNORM_BLOCK = 151
FORMAT_ETC2_R8G8B8A8_SRGB_BLOCK = 152
FORMAT_EAC_R11_UNORM_BLOCK = 153
FORMAT_EAC_R11_SNORM_BLOCK = 154
FORMAT_EAC_R11G11_UNORM_BLOCK = 155
FORMAT_EAC_R11G11_SNORM_BLOCK = 156
FORMAT_ASTC_4x4_UNORM_BLOCK = 157
FORMAT_ASTC_4x4_SRGB_BLOCK = 158
FORMAT_ASTC_5x4_UNORM_BLOCK = 159
FORMAT_ASTC_5x4_SRGB_BLOCK = 160
FORMAT_ASTC_5x5_UNORM_BLOCK = 161
FORMAT_ASTC_5x5_SRGB_BLOCK = 162
FORMAT_ASTC_6x5_UNORM_BLOCK = 163
FORMAT_ASTC_6x5_SRGB_BLOCK = 164
FORMAT_ASTC_6x6_UNORM_BLOCK = 165
FORMAT_ASTC_6x6_SRGB_BLOCK = 166
FORMAT_ASTC_8x5_UNORM_BLOCK = 167
FORMAT_ASTC_8x5_SRGB_BLOCK = 168
FORMAT_ASTC_8x6_UNORM_BLOCK = 169
FORMAT_ASTC_8x6_SRGB_BLOCK = 170
FORMAT_ASTC_8x8_UNORM_BLOCK = 171
FORMAT_ASTC_8x8_SRGB_BLOCK = 172
FORMAT_ASTC_10x5_UNORM_BLOCK = 173
FORMAT_ASTC_10x5_SRGB_BLOCK = 174
FORMAT_ASTC_10x6_UNORM_BLOCK = 175
FORMAT_ASTC_10x6_SRGB_BLOCK = 176
FORMAT_ASTC_10x8_UNORM_BLOCK = 177
FORMAT_ASTC_10x8_SRGB_BLOCK = 178
FORMAT_ASTC_10x10_UNORM_BLOCK = 179
FORMAT_ASTC_10x10_SRGB_BLOCK = 180
FORMAT_ASTC_12x10_UNORM_BLOCK = 181
FORMAT_ASTC_12x10_SRGB_BLOCK = 182
FORMAT_ASTC_12x12_UNORM_BLOCK = 183
FORMAT_ASTC_12x12_SRGB_BLOCK = 184

# VkStructureType
STRUCTURE_TYPE_APPLICATION_INFO = 0
STRUCTURE_TYPE_INSTANCE_CREATE_INFO = 1
STRUCTURE_TYPE_DEVICE_QUEUE_CREATE_INFO = 2
STRUCTURE_TYPE_DEVICE_CREATE_INFO = 3
STRUCTURE_TYPE_SUBMIT_INFO = 4
STRUCTURE_TYPE_MEMORY_ALLOCATE_INFO = 5
STRUCTURE_TYPE_MAPPED_MEMORY_RANGE = 6
STRUCTURE_TYPE_BIND_SPARSE_INFO = 7
STRUCTURE_TYPE_FENCE_CREATE_INFO = 8
STRUCTURE_TYPE_SEMAPHORE_CREATE_INFO = 9
STRUCTURE_TYPE_EVENT_CREATE_INFO = 10
STRUCTURE_TYPE_QUERY_POOL_CREATE_INFO = 11
STRUCTURE_TYPE_BUFFER_CREATE_INFO = 12
STRUCTURE_TYPE_BUFFER_VIEW_CREATE_INFO = 13
STRUCTURE_TYPE_IMAGE_CREATE_INFO = 14
STRUCTURE_TYPE_IMAGE_VIEW_CREATE_INFO = 15
STRUCTURE_TYPE_SHADER_MODULE_CREATE_INFO = 16
STRUCTURE_TYPE_PIPELINE_CACHE_CREATE_INFO = 17
STRUCTURE_TYPE_PIPELINE_SHADER_STAGE_CREATE_INFO = 18
STRUCTURE_TYPE_PIPELINE_VERTEX_INPUT_STATE_CREATE_INFO = 19
STRUCTURE_TYPE_PIPELINE_INPUT_ASSEMBLY_STATE_CREATE_INFO = 20
STRUCTURE_TYPE_PIPELINE_TESSELLATION_STATE_CREATE_INFO = 21
STRUCTURE_TYPE_PIPELINE_VIEWPORT_STATE_CREATE_INFO = 22
STRUCTURE_TYPE_PIPELINE_RASTERIZATION_STATE_CREATE_INFO = 23
STRUCTURE_TYPE_PIPELINE_MULTISAMPLE_STATE_CREATE_INFO = 24
STRUCTURE_TYPE_PIPELINE_DEPTH_STENCIL_STATE_CREATE_INFO = 25
STRUCTURE_TYPE_PIPELINE_COLOR_BLEND_STATE_CREATE_INFO = 26
STRUCTURE_TYPE_PIPELINE_DYNAMIC_STATE_CREATE_INFO = 27
STRUCTURE_TYPE_GRAPHICS_PIPELINE_CREATE_INFO = 28
STRUCTURE_TYPE_COMPUTE_PIPELINE_CREATE_INFO = 29
STRUCTURE_TYPE_PIPELINE_LAYOUT_CREATE_INFO = 30
STRUCTURE_TYPE_SAMPLER_CREATE_INFO = 31
STRUCTURE_TYPE_DESCRIPTOR_SET_LAYOUT_CREATE_INFO = 32
STRUCTURE_TYPE_DESCRIPTOR_POOL_CREATE_INFO = 33
STRUCTURE_TYPE_DESCRIPTOR_SET_ALLOCATE_INFO = 34
STRUCTURE_TYPE_WRITE_DESCRIPTOR_SET = 35
STRUCTURE_TYPE_COPY_DESCRIPTOR_SET = 36
STRUCTURE_TYPE_FRAMEBUFFER_CREATE_INFO = 37
STRUCTURE_TYPE_RENDER_PASS_CREATE_INFO = 38
STRUCTURE_TYPE_COMMAND_POOL_CREATE_INFO = 39
STRUCTURE_TYPE_COMMAND_BUFFER_ALLOCATE_INFO = 40
STRUCTURE_TYPE_COMMAND_BUFFER_INHERITANCE_INFO = 41
STRUCTURE_TYPE_COMMAND_BUFFER_BEGIN_INFO = 42
STRUCTURE_TYPE_RENDER_PASS_BEGIN_INFO = 43
STRUCTURE_TYPE_BUFFER_MEMORY_BARRIER = 44
STRUCTURE_TYPE_IMAGE_MEMORY_BARRIER = 45
STRUCTURE_TYPE_MEMORY_BARRIER = 46
STRUCTURE_TYPE_LOADER_INSTANCE_CREATE_INFO = 47
STRUCTURE_TYPE_LOADER_DEVICE_CREATE_INFO = 48
STRUCTURE_TYPE_WIN32_SURFACE_CREATE_INFO_KHR = 1000009000

# VkSubpassContents
SUBPASS_CONTENTS_INLINE = 0
SUBPASS_CONTENTS_SECONDARY_COMMAND_BUFFERS = 1

# VkResult
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

# VkDynamicState
DYNAMIC_STATE_VIEWPORT = 0
DYNAMIC_STATE_SCISSOR = 1
DYNAMIC_STATE_LINE_WIDTH = 2
DYNAMIC_STATE_DEPTH_BIAS = 3
DYNAMIC_STATE_BLEND_CONSTANTS = 4
DYNAMIC_STATE_DEPTH_BOUNDS = 5
DYNAMIC_STATE_STENCIL_COMPARE_MASK = 6
DYNAMIC_STATE_STENCIL_WRITE_MASK = 7
DYNAMIC_STATE_STENCIL_REFERENCE = 8

# VkQueueFlagBits
QUEUE_GRAPHICS_BIT = 1<<0
QUEUE_COMPUTE_BIT = 1<<1
QUEUE_TRANSFER_BIT = 1<<2
QUEUE_SPARSE_BINDING_BIT = 1<<3

# VkMemoryPropertyFlagBits
MEMORY_PROPERTY_DEVICE_LOCAL_BIT = 1<<0
MEMORY_PROPERTY_HOST_VISIBLE_BIT = 1<<1
MEMORY_PROPERTY_HOST_COHERENT_BIT = 1<<2
MEMORY_PROPERTY_HOST_CACHED_BIT = 1<<3
MEMORY_PROPERTY_LAZILY_ALLOCATED_BIT = 1<<4

# VkMemoryHeapFlagBits
MEMORY_HEAP_DEVICE_LOCAL_BIT = 1<<0

# VkAccessFlagBits
ACCESS_INDIRECT_COMMAND_READ_BIT = 1<<0
ACCESS_INDEX_READ_BIT = 1<<1
ACCESS_VERTEX_ATTRIBUTE_READ_BIT = 1<<2
ACCESS_UNIFORM_READ_BIT = 1<<3
ACCESS_INPUT_ATTACHMENT_READ_BIT = 1<<4
ACCESS_SHADER_READ_BIT = 1<<5
ACCESS_SHADER_WRITE_BIT = 1<<6
ACCESS_COLOR_ATTACHMENT_READ_BIT = 1<<7
ACCESS_COLOR_ATTACHMENT_WRITE_BIT = 1<<8
ACCESS_DEPTH_STENCIL_ATTACHMENT_READ_BIT = 1<<9
ACCESS_DEPTH_STENCIL_ATTACHMENT_WRITE_BIT = 1<<10
ACCESS_TRANSFER_READ_BIT = 1<<11
ACCESS_TRANSFER_WRITE_BIT = 1<<12
ACCESS_HOST_READ_BIT = 1<<13
ACCESS_HOST_WRITE_BIT = 1<<14
ACCESS_MEMORY_READ_BIT = 1<<15
ACCESS_MEMORY_WRITE_BIT = 1<<16

# VkBufferUsageFlagBits
BUFFER_USAGE_TRANSFER_SRC_BIT = 1<<0
BUFFER_USAGE_TRANSFER_DST_BIT = 1<<1
BUFFER_USAGE_UNIFORM_TEXEL_BUFFER_BIT = 1<<2
BUFFER_USAGE_STORAGE_TEXEL_BUFFER_BIT = 1<<3
BUFFER_USAGE_UNIFORM_BUFFER_BIT = 1<<4
BUFFER_USAGE_STORAGE_BUFFER_BIT = 1<<5
BUFFER_USAGE_INDEX_BUFFER_BIT = 1<<6
BUFFER_USAGE_VERTEX_BUFFER_BIT = 1<<7
BUFFER_USAGE_INDIRECT_BUFFER_BIT = 1<<8

# VkBufferCreateFlagBits
BUFFER_CREATE_SPARSE_BINDING_BIT = 1<<0
BUFFER_CREATE_SPARSE_RESIDENCY_BIT = 1<<1
BUFFER_CREATE_SPARSE_ALIASED_BIT = 1<<2

# VkShaderStageFlagBits
SHADER_STAGE_VERTEX_BIT = 1<<0
SHADER_STAGE_TESSELLATION_CONTROL_BIT = 1<<1
SHADER_STAGE_TESSELLATION_EVALUATION_BIT = 1<<2
SHADER_STAGE_GEOMETRY_BIT = 1<<3
SHADER_STAGE_FRAGMENT_BIT = 1<<4
SHADER_STAGE_COMPUTE_BIT = 1<<5
SHADER_STAGE_ALL_GRAPHICS = 0x0000001F
SHADER_STAGE_ALL = 0x7FFFFFFF

# VkImageUsageFlagBits
IMAGE_USAGE_TRANSFER_SRC_BIT = 1<<0
IMAGE_USAGE_TRANSFER_DST_BIT = 1<<1
IMAGE_USAGE_SAMPLED_BIT = 1<<2
IMAGE_USAGE_STORAGE_BIT = 1<<3
IMAGE_USAGE_COLOR_ATTACHMENT_BIT = 1<<4
IMAGE_USAGE_DEPTH_STENCIL_ATTACHMENT_BIT = 1<<5
IMAGE_USAGE_TRANSIENT_ATTACHMENT_BIT = 1<<6
IMAGE_USAGE_INPUT_ATTACHMENT_BIT = 1<<7

# VkImageCreateFlagBits
IMAGE_CREATE_SPARSE_BINDING_BIT = 1<<0
IMAGE_CREATE_SPARSE_RESIDENCY_BIT = 1<<1
IMAGE_CREATE_SPARSE_ALIASED_BIT = 1<<2
IMAGE_CREATE_MUTABLE_FORMAT_BIT = 1<<3
IMAGE_CREATE_CUBE_COMPATIBLE_BIT = 1<<4

# VkPipelineCreateFlagBits
PIPELINE_CREATE_DISABLE_OPTIMIZATION_BIT = 1<<0
PIPELINE_CREATE_ALLOW_DERIVATIVES_BIT = 1<<1
PIPELINE_CREATE_DERIVATIVE_BIT = 1<<2

# VkColorComponentFlagBits
COLOR_COMPONENT_R_BIT = 1<<0
COLOR_COMPONENT_G_BIT = 1<<1
COLOR_COMPONENT_B_BIT = 1<<2
COLOR_COMPONENT_A_BIT = 1<<3

# VkFenceCreateFlagBits
FENCE_CREATE_SIGNALED_BIT = 1<<0

# VkFormatFeatureFlagBits
FORMAT_FEATURE_SAMPLED_IMAGE_BIT = 1<<0
FORMAT_FEATURE_STORAGE_IMAGE_BIT = 1<<1
FORMAT_FEATURE_STORAGE_IMAGE_ATOMIC_BIT = 1<<2
FORMAT_FEATURE_UNIFORM_TEXEL_BUFFER_BIT = 1<<3
FORMAT_FEATURE_STORAGE_TEXEL_BUFFER_BIT = 1<<4
FORMAT_FEATURE_STORAGE_TEXEL_BUFFER_ATOMIC_BIT = 1<<5
FORMAT_FEATURE_VERTEX_BUFFER_BIT = 1<<6
FORMAT_FEATURE_COLOR_ATTACHMENT_BIT = 1<<7
FORMAT_FEATURE_COLOR_ATTACHMENT_BLEND_BIT = 1<<8
FORMAT_FEATURE_DEPTH_STENCIL_ATTACHMENT_BIT = 1<<9
FORMAT_FEATURE_BLIT_SRC_BIT = 1<<10
FORMAT_FEATURE_BLIT_DST_BIT = 1<<11
FORMAT_FEATURE_SAMPLED_IMAGE_FILTER_LINEAR_BIT = 1<<12

# VkQueryControlFlagBits
QUERY_CONTROL_PRECISE_BIT = 1<<0

# VkQueryResultFlagBits
QUERY_RESULT_64_BIT = 1<<0
QUERY_RESULT_WAIT_BIT = 1<<1
QUERY_RESULT_WITH_AVAILABILITY_BIT = 1<<2
QUERY_RESULT_PARTIAL_BIT = 1<<3

# VkCommandBufferUsageFlagBits
COMMAND_BUFFER_USAGE_ONE_TIME_SUBMIT_BIT = 1<<0
COMMAND_BUFFER_USAGE_RENDER_PASS_CONTINUE_BIT = 1<<1
COMMAND_BUFFER_USAGE_SIMULTANEOUS_USE_BIT = 1<<2

# VkQueryPipelineStatisticFlagBits
QUERY_PIPELINE_STATISTIC_INPUT_ASSEMBLY_VERTICES_BIT = 1<<0
QUERY_PIPELINE_STATISTIC_INPUT_ASSEMBLY_PRIMITIVES_BIT = 1<<1
QUERY_PIPELINE_STATISTIC_VERTEX_SHADER_INVOCATIONS_BIT = 1<<2
QUERY_PIPELINE_STATISTIC_GEOMETRY_SHADER_INVOCATIONS_BIT = 1<<3
QUERY_PIPELINE_STATISTIC_GEOMETRY_SHADER_PRIMITIVES_BIT = 1<<4
QUERY_PIPELINE_STATISTIC_CLIPPING_INVOCATIONS_BIT = 1<<5
QUERY_PIPELINE_STATISTIC_CLIPPING_PRIMITIVES_BIT = 1<<6
QUERY_PIPELINE_STATISTIC_FRAGMENT_SHADER_INVOCATIONS_BIT = 1<<7
QUERY_PIPELINE_STATISTIC_TESSELLATION_CONTROL_SHADER_PATCHES_BIT = 1<<8
QUERY_PIPELINE_STATISTIC_TESSELLATION_EVALUATION_SHADER_INVOCATIONS_BIT = 1<<9
QUERY_PIPELINE_STATISTIC_COMPUTE_SHADER_INVOCATIONS_BIT = 1<<10

# VkImageAspectFlagBits
IMAGE_ASPECT_COLOR_BIT = 1<<0
IMAGE_ASPECT_DEPTH_BIT = 1<<1
IMAGE_ASPECT_STENCIL_BIT = 1<<2
IMAGE_ASPECT_METADATA_BIT = 1<<3

# VkSparseImageFormatFlagBits
SPARSE_IMAGE_FORMAT_SINGLE_MIPTAIL_BIT = 1<<0
SPARSE_IMAGE_FORMAT_ALIGNED_MIP_SIZE_BIT = 1<<1
SPARSE_IMAGE_FORMAT_NONSTANDARD_BLOCK_SIZE_BIT = 1<<2

# VkSparseMemoryBindFlagBits
SPARSE_MEMORY_BIND_METADATA_BIT = 1<<0

# VkPipelineStageFlagBits
PIPELINE_STAGE_TOP_OF_PIPE_BIT = 1<<0
PIPELINE_STAGE_DRAW_INDIRECT_BIT = 1<<1
PIPELINE_STAGE_VERTEX_INPUT_BIT = 1<<2
PIPELINE_STAGE_VERTEX_SHADER_BIT = 1<<3
PIPELINE_STAGE_TESSELLATION_CONTROL_SHADER_BIT = 1<<4
PIPELINE_STAGE_TESSELLATION_EVALUATION_SHADER_BIT = 1<<5
PIPELINE_STAGE_GEOMETRY_SHADER_BIT = 1<<6
PIPELINE_STAGE_FRAGMENT_SHADER_BIT = 1<<7
PIPELINE_STAGE_EARLY_FRAGMENT_TESTS_BIT = 1<<8
PIPELINE_STAGE_LATE_FRAGMENT_TESTS_BIT = 1<<9
PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT = 1<<10
PIPELINE_STAGE_COMPUTE_SHADER_BIT = 1<<11
PIPELINE_STAGE_TRANSFER_BIT = 1<<12
PIPELINE_STAGE_BOTTOM_OF_PIPE_BIT = 1<<13
PIPELINE_STAGE_HOST_BIT = 1<<14
PIPELINE_STAGE_ALL_GRAPHICS_BIT = 1<<15
PIPELINE_STAGE_ALL_COMMANDS_BIT = 1<<16

# VkCommandPoolCreateFlagBits
COMMAND_POOL_CREATE_TRANSIENT_BIT = 1<<0
COMMAND_POOL_CREATE_RESET_COMMAND_BUFFER_BIT = 1<<1

# VkCommandPoolResetFlagBits
COMMAND_POOL_RESET_RELEASE_RESOURCES_BIT = 1<<0

# VkCommandBufferResetFlagBits
COMMAND_BUFFER_RESET_RELEASE_RESOURCES_BIT = 1<<0

# VkSampleCountFlagBits
SAMPLE_COUNT_1_BIT = 1<<0
SAMPLE_COUNT_2_BIT = 1<<1
SAMPLE_COUNT_4_BIT = 1<<2
SAMPLE_COUNT_8_BIT = 1<<3
SAMPLE_COUNT_16_BIT = 1<<4
SAMPLE_COUNT_32_BIT = 1<<5
SAMPLE_COUNT_64_BIT = 1<<6

# VkAttachmentDescriptionFlagBits
ATTACHMENT_DESCRIPTION_MAY_ALIAS_BIT = 1<<0

# VkStencilFaceFlagBits
STENCIL_FACE_FRONT_BIT = 1<<0
STENCIL_FACE_BACK_BIT = 1<<1
STENCIL_FRONT_AND_BACK = 0x00000003

# VkDescriptorPoolCreateFlagBits
DESCRIPTOR_POOL_CREATE_FREE_DESCRIPTOR_SET_BIT = 1<<0

# VkDependencyFlagBits
DEPENDENCY_BY_REGION_BIT = 1<<0

# VkPresentModeKHR
PRESENT_MODE_IMMEDIATE_KHR = 0
PRESENT_MODE_MAILBOX_KHR = 1
PRESENT_MODE_FIFO_KHR = 2
PRESENT_MODE_FIFO_RELAXED_KHR = 3

# VkColorSpaceKHR
COLOR_SPACE_SRGB_NONLINEAR_KHR = 0

# VkDisplayPlaneAlphaFlagBitsKHR
DISPLAY_PLANE_ALPHA_OPAQUE_BIT_KHR = 1<<0
DISPLAY_PLANE_ALPHA_GLOBAL_BIT_KHR = 1<<1
DISPLAY_PLANE_ALPHA_PER_PIXEL_BIT_KHR = 1<<2
DISPLAY_PLANE_ALPHA_PER_PIXEL_PREMULTIPLIED_BIT_KHR = 1<<3

# VkCompositeAlphaFlagBitsKHR
COMPOSITE_ALPHA_OPAQUE_BIT_KHR = 1<<0
COMPOSITE_ALPHA_PRE_MULTIPLIED_BIT_KHR = 1<<1
COMPOSITE_ALPHA_POST_MULTIPLIED_BIT_KHR = 1<<2
COMPOSITE_ALPHA_INHERIT_BIT_KHR = 1<<3

# VkSurfaceTransformFlagBitsKHR
SURFACE_TRANSFORM_IDENTITY_BIT_KHR = 1<<0
SURFACE_TRANSFORM_ROTATE_90_BIT_KHR = 1<<1
SURFACE_TRANSFORM_ROTATE_180_BIT_KHR = 1<<2
SURFACE_TRANSFORM_ROTATE_270_BIT_KHR = 1<<3
SURFACE_TRANSFORM_HORIZONTAL_MIRROR_BIT_KHR = 1<<4
SURFACE_TRANSFORM_HORIZONTAL_MIRROR_ROTATE_90_BIT_KHR = 1<<5
SURFACE_TRANSFORM_HORIZONTAL_MIRROR_ROTATE_180_BIT_KHR = 1<<6
SURFACE_TRANSFORM_HORIZONTAL_MIRROR_ROTATE_270_BIT_KHR = 1<<7
SURFACE_TRANSFORM_INHERIT_BIT_KHR = 1<<8

# VkDebugReportFlagBitsEXT
DEBUG_REPORT_INFORMATION_BIT_EXT = 1<<0
DEBUG_REPORT_WARNING_BIT_EXT = 1<<1
DEBUG_REPORT_PERFORMANCE_WARNING_BIT_EXT = 1<<2
DEBUG_REPORT_ERROR_BIT_EXT = 1<<3
DEBUG_REPORT_DEBUG_BIT_EXT = 1<<4

# VkDebugReportObjectTypeEXT
DEBUG_REPORT_OBJECT_TYPE_UNKNOWN_EXT = 0
DEBUG_REPORT_OBJECT_TYPE_INSTANCE_EXT = 1
DEBUG_REPORT_OBJECT_TYPE_PHYSICAL_DEVICE_EXT = 2
DEBUG_REPORT_OBJECT_TYPE_DEVICE_EXT = 3
DEBUG_REPORT_OBJECT_TYPE_QUEUE_EXT = 4
DEBUG_REPORT_OBJECT_TYPE_SEMAPHORE_EXT = 5
DEBUG_REPORT_OBJECT_TYPE_COMMAND_BUFFER_EXT = 6
DEBUG_REPORT_OBJECT_TYPE_FENCE_EXT = 7
DEBUG_REPORT_OBJECT_TYPE_DEVICE_MEMORY_EXT = 8
DEBUG_REPORT_OBJECT_TYPE_BUFFER_EXT = 9
DEBUG_REPORT_OBJECT_TYPE_IMAGE_EXT = 10
DEBUG_REPORT_OBJECT_TYPE_EVENT_EXT = 11
DEBUG_REPORT_OBJECT_TYPE_QUERY_POOL_EXT = 12
DEBUG_REPORT_OBJECT_TYPE_BUFFER_VIEW_EXT = 13
DEBUG_REPORT_OBJECT_TYPE_IMAGE_VIEW_EXT = 14
DEBUG_REPORT_OBJECT_TYPE_SHADER_MODULE_EXT = 15
DEBUG_REPORT_OBJECT_TYPE_PIPELINE_CACHE_EXT = 16
DEBUG_REPORT_OBJECT_TYPE_PIPELINE_LAYOUT_EXT = 17
DEBUG_REPORT_OBJECT_TYPE_RENDER_PASS_EXT = 18
DEBUG_REPORT_OBJECT_TYPE_PIPELINE_EXT = 19
DEBUG_REPORT_OBJECT_TYPE_DESCRIPTOR_SET_LAYOUT_EXT = 20
DEBUG_REPORT_OBJECT_TYPE_SAMPLER_EXT = 21
DEBUG_REPORT_OBJECT_TYPE_DESCRIPTOR_POOL_EXT = 22
DEBUG_REPORT_OBJECT_TYPE_DESCRIPTOR_SET_EXT = 23
DEBUG_REPORT_OBJECT_TYPE_FRAMEBUFFER_EXT = 24
DEBUG_REPORT_OBJECT_TYPE_COMMAND_POOL_EXT = 25
DEBUG_REPORT_OBJECT_TYPE_SURFACE_KHR_EXT = 26
DEBUG_REPORT_OBJECT_TYPE_SWAPCHAIN_KHR_EXT = 27
DEBUG_REPORT_OBJECT_TYPE_DEBUG_REPORT_EXT = 28

# VkDebugReportErrorEXT
DEBUG_REPORT_ERROR_NONE_EXT = 0
DEBUG_REPORT_ERROR_CALLBACK_REF_EXT = 1

# VkRasterizationOrderAMD
RASTERIZATION_ORDER_STRICT_AMD = 0
RASTERIZATION_ORDER_RELAXED_AMD = 1


### STRUCTS ###

mod = modules['vk']
def define_structure(name, *args):
    setattr(mod, name, type(name, (Structure,), {'_fields_': args}))

define_structure('ApplicationInfo',
 ('s_type', c_uint), ('next', c_void_p), ('application_name', c_char_p), ('application_version', c_uint),
 ('engine_name', c_char_p), ('engine_version', c_uint), ('api_version', c_uint))

define_structure('InstanceCreateInfo', 
 ('s_type', c_uint), ('next', c_void_p), ('flags', c_uint), ('application_info', POINTER(ApplicationInfo)),
 ('enabled_layer_count', c_uint), ('enabled_layer_names', POINTER(c_char_p)), ('enabled_extension_count', c_uint),
 ('enabled_extension_names', POINTER(c_char_p)))

define_structure('VkExtent3D', ('width', c_uint), ('height', c_uint), ('depth', c_uint))

define_structure('QueueFamilyProperties',
  ('queue_flags', c_uint), ('queue_count', c_uint), ('timestamp_valid_bits', c_uint),
  ('min_image_transfer_granularity', VkExtent3D)
)

define_structure('DeviceQueueCreateInfo',
    ('s_type', c_uint), ('next', c_void_p), ('flags', c_uint), ('queue_family_index', c_uint),
    ('queue_count', c_uint), ('queue_priorities', POINTER(c_float))    
)

define_structure('DeviceCreateInfo',
    ('s_type', c_uint), ('next', c_void_p), ('flags', c_uint), ('queue_create_info_count', c_uint),
    ('queue_create_infos', POINTER(DeviceQueueCreateInfo)), ('enabled_layer_count', c_uint),
    ('enabled_layer_names', POINTER(c_char_p)), ('enabled_extension_count', c_uint),
    ('enabled_extension_names', POINTER(c_char_p)), ('enabled_features', c_void_p),
)

define_structure('Win32SurfaceCreateInfoKHR',
    ('s_type', c_uint), ('next', c_void_p), ('flags', c_uint), ('hinstance', c_void_p),
    ('hwnd', c_void_p)
)

del mod

### INSTANCE FUNCTIONS ###

vk = cdll.LoadLibrary('vulkan-1')
GetInstanceProcAddr = vk.vkGetInstanceProcAddr
GetInstanceProcAddr.restype = c_void_p  # Note: using a function to check the return value will corrupt the function pointer.
GetInstanceProcAddr.argtypes = (Instance, c_char_p)

CreateInstance = (CFUNCTYPE(c_uint, POINTER(InstanceCreateInfo), c_void_p, POINTER(Instance)))(GetInstanceProcAddr(Instance(0), b'vkCreateInstance'))

INSTANCE_FUNCTIONS = (
    (b'vkDestroyInstance', None, Instance, c_void_p),
    (b'vkEnumeratePhysicalDevices', c_uint, Instance, POINTER(c_uint), POINTER(PhysicalDevice)),
    (b'vkGetPhysicalDeviceQueueFamilyProperties', None, PhysicalDevice, POINTER(c_uint), POINTER(QueueFamilyProperties)),
    (b'vkCreateDevice', c_uint, PhysicalDevice, POINTER(DeviceCreateInfo), c_void_p, POINTER(Device)),
    (b'vkGetDeviceProcAddr', c_void_p, Device, c_char_p),
    (b'vkCreateWin32SurfaceKHR', c_uint, Instance, POINTER(Win32SurfaceCreateInfoKHR), c_void_p, POINTER(SurfaceKHR)),
    (b'vkDestroySurfaceKHR', None, Instance, SurfaceKHR, c_void_p)
)

DEVICE_FUNCTIONS = (
    (b'vkDestroyDevice', None, Device, c_void_p),
    
)

def load_functions(owner, obj, functions_list, loader):
    """
        Not generated! Load the vulkan functions
    """
    for name, return_type, *args in functions_list:
        py_name = name.decode()[2::]
        fn = (CFUNCTYPE(return_type, *args))(loader(obj, name))
        setattr(owner, py_name, fn)

def load_instance_functions(owner, instance):
    load_functions(owner, instance, INSTANCE_FUNCTIONS, GetInstanceProcAddr)

def load_device_functions(owner, device, loader):
    load_functions(owner, device, DEVICE_FUNCTIONS, loader)