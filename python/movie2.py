import mmap
import os
import struct
import sys

# Use a set for O(1) lookups instead of a list
CONTAINERS = {"moov", "udta", "trak", "edts", "mdia", "minf", "stbl", "dinf", "gmhd", "clip", "matt"}

def process_mp4(input_file):
    """Memory-maps the MP4 file and iteratively parses its box structure."""
    if not os.path.exists(input_file):
        print(f"Error: File {input_file} not found.", file=sys.stderr)
        return

    with open(input_file, 'rb') as f:
        file_size = os.path.getsize(input_file)
        if file_size < 8:
            return
            
        with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mmapped_file:
            # Stack stores tuples of: (start_offset, end_offset, current_prefix)
            stack = [(0, file_size, "")]
            
            while stack:
                offset, end_offset, prefix = stack.pop()
                
                while offset + 8 <= end_offset:
                    # Unpack directly from the mmap buffer without slicing memory
                    box_size, box_type_bytes = struct.unpack_from('>I4s', mmapped_file, offset)
                    
                    try:
                        box_type = box_type_bytes.decode("latin1")
                    except UnicodeDecodeError:
                        box_type = "????"

                    # Handle MP4 special box sizes
                    if box_size == 1:
                        # 64-bit large box size (comes after the type)
                        if offset + 16 > end_offset: break
                        box_size = struct.unpack_from('>Q', mmapped_file, offset + 8)[0]
                        header_size = 16
                    elif box_size == 0:
                        # Box extends to the end of the file
                        box_size = end_offset - offset
                        header_size = 8
                    else:
                        header_size = 8

                    # Guard against corrupted files with 0 or negative calculated sizes
                    if box_size < header_size:
                        break

                    content_offset = offset + header_size
                    content_size = box_size - header_size
                    
                    if box_type in CONTAINERS:
                        # Push the container content limits onto the stack to process next
                        # (Reverses order if you want strict top-down, but perfectly safe for tree dumps)
                        next_prefix = f"{prefix}/{box_type}@{content_offset}"
                        stack.append((content_offset, content_offset + content_size, next_prefix))
                    else:
                        print(f"{prefix}/{box_type}", content_offset, content_size)
                        
                    offset += box_size

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <input_file.mp4>")
        sys.exit(1)
    process_mp4(sys.argv[1])
