The program takes the following inputs:

1) the type of cache “d”, for direct-mapped

2) the total cache size in bytes (max. for testing 256 bytes, must be a power of 2). This does not include valid and tag bits

3) the size of a block in bytes (max. for testing 64 bytes, must be a power of 2). This does not include valid and tag bits

4) an input text that contains the sequence of memory accesses.


Example use:
python3 cache.py --type=d --cache_size=256 --block_size=64 --memfile=mem1.txt


The output is broken down with the diagram shown below
accessed memory address in hexadecimal | tag bits (binary) | index bits (binary) |  hit (h) or miss (m) or unaligned (u)

There will also be a calculation for the Hit/Miss ratio

