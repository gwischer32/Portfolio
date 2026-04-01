__kernel void conv_global(
    __global const float* image,
    const int width,
    const int height,
    __global const float* filter,
    const int fwidth,
    const int fheight,
    const int padx,
    const int pady,
    __global float* out)
{
    int x = get_global_id(0);
    int y = get_global_id(1);

    if (x >= width || y >= height) return;

    float sum = 0.0f;

    for (int fy = 0; fy < fheight; fy++) {
        for (int fx = 0; fx < fwidth; fx++) {

            int sx = x + fx - padx;
            int sy = y + fy - pady;

            if (sx >= 0 && sx < width && sy >= 0 && sy < height) {
                int sidx = sy * width + sx;
                int fidx = fy * fwidth + fx;
                sum += image[sidx] * filter[fidx];
            }
        }
    }

    out[y * width + x] = sum;
}
