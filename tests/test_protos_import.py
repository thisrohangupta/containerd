def test_generated_protos_importable():
    # If imports succeed, our sys.path shim works
    import py_containerd.api.protos.github.com.containerd.containerd.api.services.images.v1.images_pb2 as _
    import py_containerd.api.protos.github.com.containerd.containerd.api.services.images.v1.images_pb2_grpc as _2
    import py_containerd.api.protos.github.com.containerd.containerd.api.types.descriptor_pb2 as _3