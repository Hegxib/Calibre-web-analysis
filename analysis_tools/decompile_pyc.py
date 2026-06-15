import marshal, struct

def analyze_pyc(path):
    with open(path, 'rb') as f:
        magic = f.read(4)
        flags = struct.unpack('<I', f.read(4))[0]

        print('Magic:', magic.hex())
        print('Flags: 0x{:08x}'.format(flags))

        if flags & 0x1:
            hash_val = f.read(8)
            print('Source hash:', hash_val.hex())

        size_data = f.read(4)
        if len(size_data) == 4:
            code_size = struct.unpack('<I', size_data)[0]
            print('Code size:', code_size)

        code_obj = marshal.load(f)
        print('Code type:', type(code_obj))
        print('Name:', code_obj.co_name)
        print('Filename:', code_obj.co_filename)
        print('Arg count:', code_obj.co_argcount)
        print('Constants ({}):'.format(len(code_obj.co_consts)))
        for i, c in enumerate(code_obj.co_consts[:15]):
            if isinstance(c, str):
                print("  [{}] str({}): {}".format(i, len(c), c[:120]))
            elif isinstance(c, type(None)):
                print("  [{}] None".format(i))
            elif isinstance(c, (int, float, bool)):
                print("  [{}] {}: {}".format(i, type(c).__name__, str(c)[:80]))
            else:
                print("  [{}] {}".format(i, type(c).__name__))

        print('Names ({}):'.format(len(code_obj.co_names)))
        for n in code_obj.co_names[:20]:
            print(' ', n)

        print('\nAll strings in consts:')
        def extract_strings(co, depth=0):
            if depth > 3:
                return
            for c in co.co_consts:
                if isinstance(c, str) and len(c) > 5:
                    prefix = "  " * depth
                    print("{}str({}): {}".format(prefix, len(c), c[:150]))
                elif hasattr(c, 'co_consts'):
                    extract_strings(c, depth + 1)
        extract_strings(code_obj)

analyze_pyc('D:/Analysis/calibreweb.exe_extracted/root.pyc')
