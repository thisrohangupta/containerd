
# Make generated proto modules importable when they use absolute imports like
# "from github.com.containerd.containerd... import ..." by adding the protos
# root to sys.path so top-level package "github" resolves.
import os
import sys

_protos_root = os.path.join(os.path.dirname(__file__), "protos")
if _protos_root not in sys.path:
    sys.path.insert(0, _protos_root)


