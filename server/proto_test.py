from proto import Snet
proto = Snet()
meta = b"GETMETA ehlo\r\n\r\n"
assert proto.meta_header("ehlo") == meta, proto.header
range_ = b"GETRANGE ehlo\r\nstart : 0\r\nend : 1024\r\n\r\n"
assert proto.range_header("ehlo", 0, 1024) == range_, proto.header
dnload = b"DOWNLOADING ehlo\r\n\r\n"
assert proto.dnload_header("ehlo") == dnload, proto.header
accept = b"STAT1 ehlo\r\nlength : 1024\r\n\r\n"
assert proto.accept_header("ehlo", 1024) == accept, proto.header
reject = b"STAT0 ehlo\r\nfiles : ehlo, world\r\n\r\n"
assert proto.reject_header("ehlo", "ehlo, world") == reject, proto.header
upload = b"UPLOADING ehlo\r\nlength : 1024\r\n\r\n"
assert proto.upload_header("ehlo", 1024) == upload, proto.header
meta = {
    "status" : b"GETMETA",
    "name" : b"ehlo"
    }
assert proto.parse_header(proto.meta_header("ehlo")) == meta, proto.parsed
range_ = {
    "status" : b"GETRANGE",
    "name" : b"ehlo",
    "start" : 0,
    "end" : 1024
    }
assert proto.parse_header(proto.range_header("ehlo", 0, 1024)) == range_, proto.parsed
dnload = {
    "status" : b"DOWNLOADING",
    "name" : b"ehlo"
    }
assert proto.parse_header(proto.dnload_header("ehlo")) == dnload, proto.parsed
accept = {
    "status" : b"STAT1",
    "name" : b"ehlo",
    "length" : 1024
    }
assert proto.parse_header(proto.accept_header("ehlo", 1024)) == accept, proto.parsed
reject = {
    "status" : b"STAT0",
    "name" : b"ehlo",
    "files" : [b"ehlo", b"world"]
    }
assert proto.parse_header(proto.reject_header("ehlo", "ehlo, world")) == reject, proto.parsed
upload = {
    "status" : b"UPLOADING",
    "name" : b"ehlo",
    "length" : 1024
    }
assert proto.parse_header(proto.upload_header("ehlo", 1024)) == upload, proto.parsed
print("OK")
