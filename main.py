import logging
logging.basicConfig()

import av

container = av.open("./cute.mp4")
out = av.open("./outcat.mp4", "w")

in_stream = container.streams.video[0]
in_codec = in_stream.codec_context

framerate = in_stream.base_rate
time_base = in_stream.time_base
out_stream = out.add_stream("h264", rate=framerate)
out_codec = out_stream.codec_context
out_codec.width = in_codec.width
out_codec.height = in_codec.height

last_pts = 1
last_dts = 0

file_frames = {}
file_containers = {}

def get_file(key):
    return file_frames[key]

def get_container(key):
    return file_containers[key]

def get_stream(key):
    container = get_container(key)
    return container.streams.get(video=0)[0]

def load_file(path, key):
    global file_frames
    global file_containers
    file_key = key or path
    container = av.open(path)
    frames = container.decode(video=0)
    file_frames[file_key] = frames
    file_containers[file_key] = container
    return frames

def mux_packets(packets):
    global last_pts
    global last_dts
    if len(packets) > 0:
        for packet in packets:
            packet.dts = last_dts
            packet.pts = last_pts
            last_dts += 1
            last_pts += 1 
        out.mux(packets)

def mux_frames(frames):
    for frame in frames:
        mux_packets(out_stream.encode(frame))

def file_slice(key, fromFrame, toFrame):
    print(f"slice {key} from {fromFrame} to {toFrame}")
    frames = get_file(key)
    container = get_container(key)
    # print(container.duration)
    stream = get_stream(key)
    print(stream.time_base)
    container.seek(-1, any_frame=False, backward=True, stream=stream)
    i = 0
    for frame in container.decode(video=0):
        if i >= fromFrame+toFrame:
            print(f"end slice at {i}")
            break
        i += 1
        if i < fromFrame:
            continue
        mux_packets(out_stream.encode(frame))

def file_mux(key):
    print(f"mux {key} {last_pts}")
    mux_frames(get_file(key))

def out_close():
    mux_packets(out_stream.encode(None))
    out.close()


load_file("./cute.mp4", "cute")
load_file("./cat.mp4", "cat")
load_file("./bunny.webm", "bunny")
load_file("./korone_pizza.mp4", "korone")

print(framerate)
# file_mux("cute")
file_slice("cute", framerate*3, 10)
file_slice("cute", framerate, 10)
file_slice("cute", framerate, 10)
file_slice("cute", framerate*4, framerate)
file_slice("cute", framerate*4, 2)
file_slice("cute", framerate*5, 2)
file_slice("cute", framerate*3, 2)
file_slice("cute", framerate*1, 2)
file_slice("cute", framerate*2, 2)
file_slice("cute", framerate*4, 2)
file_slice("cute", framerate*5, 2)
file_slice("cute", framerate*3, 2)
file_slice("cute", framerate*1, 2)
file_slice("cute", framerate*2, 2)
file_slice("cute", framerate*4, 2)
file_slice("cute", framerate*5, 2)
file_slice("cute", framerate*3, 2)
file_slice("cute", framerate*1, 2)
file_slice("cute", framerate*4, 1)
file_slice("cute", framerate*4, 1)
file_slice("cute", framerate*4, 1)
file_slice("cute", framerate*4, 1)
file_slice("cute", framerate*4, 1)
file_slice("cute", framerate*4, 1)
file_slice("cute", framerate, 5)
file_slice("cute", framerate, 5)
file_slice("cute", framerate*2, 5)
file_slice("cute", framerate*2, 5)
file_slice("cute", framerate*6, 15)
file_slice("cute", framerate*6, 5)
file_slice("cute", framerate*6, 5)
file_slice("cute", framerate*6, 1)
file_slice("cute", framerate*6, 1)
file_slice("cute", framerate*6, 1)

out_close()

