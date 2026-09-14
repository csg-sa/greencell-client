# Copyright (c) 2025 csg-sa

import glob
import zipfile

whls = glob.glob("dist/*.whl")
assert whls, "No wheels in dist/"
with zipfile.ZipFile(whls[0]) as z:
    meta = next(n for n in z.namelist() if n.endswith(".dist-info/METADATA"))
    print(z.read(meta).decode().splitlines()[:12])
