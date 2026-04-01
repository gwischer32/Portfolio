import os
import numpy as np
from time import time
from PIL import Image
import pyopencl as cl

# ----------------------------------------------------
# Image helpers

def read_image(file_path):
    """Read image from file and return grayscale float32 numpy array."""
    img = Image.open(file_path).convert('L')
    return np.array(img, dtype=np.float32)

def save_image(array, filename):
    """Save numpy array as an image."""
    img = Image.fromarray(np.uint8(np.clip(array, 0, 255)))
    img.save(filename)
    print(f"Saved: {filename}")

def display_image(array):
    """Show numpy array as image."""
    img = Image.fromarray(np.uint8(np.clip(array, 0, 255)))
    img.show()

# ----------------------------------------------------
# OpenCL global-memory convolution

def convolve2d_opencl(image, filter):
    """
    Perform 2D convolution using OpenCL (global memory only).
    """
    img = np.asarray(image, dtype=np.float32)
    filt = np.asarray(filter, dtype=np.float32)

    height, width = img.shape
    fheight, fwidth = filt.shape

    pad_y = fheight // 2
    pad_x = fwidth // 2

    # Flatten
    img_flat = img.ravel().astype(np.float32)
    filt_flat = filt.ravel().astype(np.float32)
    out_flat = np.empty_like(img_flat)

    # OpenCL platform
    try:
        platforms = cl.get_platforms()
        if not platforms:
            print("No OpenCL platforms found.")
            return image.copy()
    except Exception as e:
        print("OpenCL error:", e)
        return image.copy()

    platform = platforms[0]
    devices = platform.get_devices()
    if not devices:
        print("No devices on platform.")
        return image.copy()
    device = devices[0]

    ctx = cl.Context([device])
    queue = cl.CommandQueue(ctx, device)

    # Load kernel
    kernel_path = os.path.join(os.path.dirname(__file__), "convKernel.cl")
    if not os.path.exists(kernel_path):
        raise FileNotFoundError(f"Missing kernel file: {kernel_path}")

    with open(kernel_path, 'r') as f:
        kernel_src = f.read()

    program = cl.Program(ctx, kernel_src).build()

    mf = cl.mem_flags
    buf_image  = cl.Buffer(ctx, mf.READ_ONLY  | mf.COPY_HOST_PTR, hostbuf=img_flat)
    buf_filter = cl.Buffer(ctx, mf.READ_ONLY  | mf.COPY_HOST_PTR, hostbuf=filt_flat)
    buf_out    = cl.Buffer(ctx, mf.WRITE_ONLY, out_flat.nbytes)

    kernel = program.conv_global
    kernel.set_args(
        buf_image,
        np.int32(width),
        np.int32(height),
        buf_filter,
        np.int32(fwidth),
        np.int32(fheight),
        np.int32(pad_x),
        np.int32(pad_y),
        buf_out
    )

    global_size = (np.int32(width), np.int32(height))

    start = time()
    cl.enqueue_nd_range_kernel(queue, kernel, global_size, None)
    queue.finish()
    end = time()

    cl.enqueue_copy(queue, out_flat, buf_out)
    queue.finish()

    print(f"OpenCL convolution time: {end - start:.6f} seconds on device {device.name}")

    return out_flat.reshape((height, width))


# ----------------------------------------------------
# Main entry

if __name__ == "__main__":
    img = read_image("ecs.jpg").astype(np.float32)

    # 7×7 blur filter
    box = np.ones((7, 7), dtype=np.float32) / 49.0

    out = convolve2d_opencl(img, box)

    save_image(out, "convolved_opencl_global.png")
