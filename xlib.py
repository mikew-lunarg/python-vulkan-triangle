"""
    Minimalistic wrapper over the XLIB window api
"""
import vk
import weakref, asyncio

from ctypes import *

# Extern libraries
try:
    xcb = cdll.LoadLibrary('libxcb.so')
    libc = cdll.LoadLibrary("libc.so.6")
except OSError:
    raise OSError("Failed to import libxcb.so or libc. Is it installed?")

# TYPES
xcb_connection_t = c_void_p
xcb_setup_t = c_void_p
xcb_window_t = c_uint
xcb_colormap_t = c_uint
xcb_visualid_t = c_uint
xcb_drawable_t = c_uint

# Structures
class xcb_screen_t(Structure):
    _fields_ = (
        ('root', xcb_window_t),
        ('default_colormap', xcb_colormap_t),
        ('white_pixel', c_uint),
        ('black_pixel', c_uint),
        ('current_input_mask', c_uint),
        ('width_in_pixels', c_ushort), ('height_in_pixels', c_ushort),
        ('width_in_millimeters', c_ushort), ('height_in_millimeters', c_ushort),
        ('min_installed_maps', c_ushort), ('max_installed_maps', c_ushort),
        ('root_visual', xcb_visualid_t),
        ('backing_stores', c_ubyte), ('save_unders', c_ubyte),
        ('root_depth', c_ubyte), ('allowed_depths_len', c_ubyte)
    )

class xcb_get_geometry_reply_t(Structure):
    _fields_ = (
        ('response_type', c_ubyte),
        ('depth', c_ubyte),
        ('sequence', c_ushort),
        ('length', c_uint),
        ('root', xcb_window_t),
        ('x', c_short), ('y', c_short),
        ('width', c_ushort), ('height', c_ushort),
        ('border_width', c_ushort)
    )

class xcb_generic_event_t(Structure):
    _fields_ = (
        ('response_type', c_ubyte),
        ('pad0', c_ubyte),
        ('sequence', c_ushort),
        ('pad', c_uint*7),
        ('full_sequence', c_uint),
    )

class xcb_screen_iterator_t(Structure):
    _fields_ = (
        ('data', POINTER(xcb_screen_t)),
        ('rem', c_int),
        ('index', c_int)
    )

class xcb_void_cookie_t(Structure):
    _fields_ = (('sequence', c_uint),)

xcb_get_geometry_cookie_t = xcb_void_cookie_t

# CONSTS

NULL = c_void_p(0)
NULL_STR = cast(NULL, POINTER(c_char))

XCB_CW_BACK_PIXEL = 2
XCB_CW_EVENT_MASK = 2048

XCB_EVENT_MASK_KEY_RELEASE = 2
XCB_EVENT_MASK_EXPOSURE = 32768
XCB_EVENT_MASK_STRUCTURE_NOTIFY = 131072
XCB_EVENT_MASK_POINTER_MOTION = 64
XCB_EVENT_MASK_BUTTON_PRESS = 4
XCB_EVENT_MASK_BUTTON_RELEASE = 2

XCB_COPY_FROM_PARENT = 0

XCB_WINDOW_CLASS_INPUT_OUTPUT = 1

XCB_DESTROY_NOTIFY = 17

# Functions

xcb_connect = xcb.xcb_connect
xcb_connect.restype = xcb_connection_t
xcb_connect.argtypes = (c_char_p, POINTER(c_int))

xcb_get_setup = xcb.xcb_get_setup
xcb_get_setup.restype = xcb_setup_t
xcb_get_setup.argtypes = (xcb_connection_t,)

xcb_setup_roots_iterator = xcb.xcb_setup_roots_iterator
xcb_setup_roots_iterator.restype = xcb_screen_iterator_t
xcb_setup_roots_iterator.argtypes = (xcb_setup_t,)

xcb_setup_next = xcb.xcb_setup_next
xcb_setup_next.restype = None
xcb_setup_next.argtypes = (POINTER(xcb_screen_iterator_t),)

xcb_disconnect = xcb.xcb_disconnect
xcb_disconnect.restype = None
xcb_disconnect.argtypes = (xcb_connection_t,)

xcb_generate_id = xcb.xcb_generate_id
xcb_generate_id.restype = c_uint
xcb_generate_id.argtypes = (xcb_connection_t, )

xcb_create_window = xcb.xcb_create_window
xcb_create_window.restype = xcb_void_cookie_t
xcb_create_window.argtypes = (
    xcb_connection_t, c_ubyte, xcb_window_t, xcb_window_t, c_short, c_short,
    c_short, c_short, c_short, c_short, xcb_visualid_t, c_uint, c_void_p
)

xcb_map_window = xcb.xcb_map_window
xcb_map_window.restype = xcb_void_cookie_t
xcb_map_window.argtypes = (xcb_connection_t, xcb_window_t)

xcb_destroy_window = xcb.xcb_destroy_window
xcb_destroy_window.restype = xcb_void_cookie_t
xcb_destroy_window.argtypes = (xcb_connection_t, xcb_window_t)

xcb_flush = xcb.xcb_flush
xcb_flush.restype = c_int
xcb_flush.argtypes = (xcb_connection_t,)

xcb_get_geometry = xcb.xcb_get_geometry
xcb_get_geometry.restype = xcb_get_geometry_cookie_t
xcb_get_geometry.argtypes = (xcb_connection_t, xcb_drawable_t)

xcb_get_geometry_reply = xcb.xcb_get_geometry_reply
xcb_get_geometry_reply.restype = POINTER(xcb_get_geometry_reply_t)
xcb_get_geometry_reply.argtypes = (xcb_connection_t, xcb_get_geometry_cookie_t, c_void_p)

xcb_poll_for_event = xcb.xcb_poll_for_event
xcb_poll_for_event.restype = POINTER(xcb_generic_event_t)
xcb_poll_for_event.argtypes = (xcb_connection_t,)

free = libc.free
free.restype = None
free.argtypes = (c_void_p,)

def handle_event(event):
    evt = event.response_type & 0x7f

    if evt == XCB_DESTROY_NOTIFY:
        return False

    return True

async def process_events(window):
    listen_events = True
    while listen_events:
        event = xcb_poll_for_event(window.connection)
        if event.value != 0:
            listen_events = handle_event(event.contents)
            free(event)

        await asyncio.sleep(1/30)

    asyncio.get_event_loop().stop()
    
class XlibWindow(object):
    
    def __init__(self, app):
        app = weakref.ref(app)

        # Setup a window using XCB
        screen = c_int(0)
        connection = xcb_connect(NULL_STR, byref(screen))
        setup = xcb_get_setup(connection);
        iter = xcb_setup_roots_iterator(setup);

        screen = screen.value
        while screen > 0:
            xcb_screen_next(byref(iter));
            screen -= 1

        screen = iter.data
        _screen = screen.contents

        # Create the window
        events_masks = XCB_EVENT_MASK_BUTTON_RELEASE | XCB_EVENT_MASK_BUTTON_PRESS |\
                        XCB_EVENT_MASK_POINTER_MOTION | XCB_EVENT_MASK_STRUCTURE_NOTIFY |\
                        XCB_EVENT_MASK_EXPOSURE | XCB_EVENT_MASK_KEY_RELEASE

        window = xcb_generate_id(connection)
        value_mask = XCB_CW_BACK_PIXEL | XCB_CW_EVENT_MASK
        value_list = (c_uint*32)(_screen.black_pixel, events_masks)

        
        xcb_create_window(
            connection, XCB_COPY_FROM_PARENT, window, _screen.root,
            0, 0, 1280, 720, 0, XCB_WINDOW_CLASS_INPUT_OUTPUT,
            _screen.root_visual, value_mask,
            cast(value_list, c_void_p)
        )

        self.window = window
        self.connection = connection

        asyncio.ensure_future(process_events(self))

    def __del__(self):
        xcb_destroy_window(self.connection, self.window)
        xcb_disconnect(self.connection)

    def dimensions(self):
        cookie = xcb_get_geometry(self.connection, self.window)
        geo = xcb_get_geometry_reply(self.connection, cookie, NULL)
        geo = geo.contents
        return (geo.width, geo.height)

    def show(self):
        xcb_map_window(self.connection, self.window)
        xcb_flush(self.connection)

    def set_title(self, title):
        return #TODO
        title = c_wchar_p(title)
        SetWindowTextW(self.__hwnd, title)



class XlibSwapchain(object):
    
    def create_surface(self):
        """
            Create a surface for the window
        """
        app = self.app()

        surface = vk.SurfaceKHR(0)
        surface_info = vk.XcbSurfaceCreateInfoKHR(
            s_type = vk.STRUCTURE_TYPE_XCB_SURFACE_CREATE_INFO_KHR,
            next= vk.NULL, flags=0, connection=app.window.connection,
            window=app.window.window
        )

        result = app.CreateXcbSurfaceKHR(app.instance, byref(surface_info), NULL, byref(surface))
        if result == vk.SUCCESS:
            self.surface = surface
        else:
            raise RuntimeError("Failed to create surface")
    
    def __init__(self, app):
        self.app = weakref.ref(app)
        self.surface = None
        self.swapchain = None
        self.images = None
        self.views = None
        self.create_surface()