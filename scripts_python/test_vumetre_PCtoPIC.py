from ctypes import *
from pulseaudio import lib_pulseaudio

lib = cdll.LoadLibrary('libpulse-simple.so.0')

# pa_simple_new()
pa_simple_new = lib.pa_simple_new
pa_simple_new.restype = c_void_p
pa_simple_new.argstypes = [
    c_char_p,           # Server name or NULL for default
    c_char_p,           # Description for the client
    lib_pulseaudio.pa_stream_direction,             # Stream direction, record or playback
    c_char_p,           # Sink or source name, NULL for default
    c_char_p,           # Stream description

    POINTER(lib_pulseaudio.pa_sample_spec), # Sample type to use
    POINTER(lib_pulseaudio.pa_channel_map),         # Channel map to use or NULL for default
    POINTER(lib_pulseaudio.pa_buffer_attr),         # Buffer attributes or NULL for default
    POINTER(c_int),         # A pointer to the error code for when the routine returns NULL
]

# pa_simple_read()
pa_simple_read = lib.pa_simple_read
pa_simple_read.restype = c_int
pa_simple_read.argstypes = [ c_void_p, c_char_p, c_size_t, POINTER(c_int) ]


from pulseaudio import lib_pulseaudio
import pasimple
import ctypes

ss = lib_pulseaudio.pa_sample_spec(lib_pulseaudio.PA_SAMPLE_S16LE, 44100, 1)

buf = ctypes.create_string_buffer(4096)

s = pasimple.pa_simple_new(
        None, # server name NULL for default
        "avrvu", # program name
        2, # record
        "alsa_output.pci-0000_00_14.2.analog-stereo.monitor", #device
        "vu-record", 
        ctypes.byref(ss),
        None,
        None,
        None
)

while True:
    ret = pasimple.pa_simple_read(s, ctypes.byref(buf), 4096, None)
    #print ret
    data = buf.raw
    # your processing here