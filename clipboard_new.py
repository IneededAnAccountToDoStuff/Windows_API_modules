#New version of clipboard_api
import struct as _struct,ctypes as _ctypes;_windll=_ctypes.windll;_kernel32=_windll.kernel32;_user32=_windll.user32
def getformat(names:bool=False):'low level stuff';_user32.GetUpdatedClipboardFormats(None,0,_ctypes.pointer(q:=_ctypes.c_int()));buffer=bytearray((varco:=q.value)*4);_user32.GetUpdatedClipboardFormats((_ctypes.c_int*varco).from_buffer(buffer),varco,_ctypes.pointer(q));qq=[i for i in(i[0]for i in _struct.iter_unpack('H',buffer))if i];qq.sort();return(varco,{i:(buffer1:=bytearray(65*4),_user32.GetClipboardFormatNameA(i,(_ctypes.c_int*65).from_buffer(buffer1),255),buffer1[:buffer1.find(b'\x00')].decode())[2]for i in qq}if names else(*qq,))
def register(name:str):'low level stuff';return _user32.RegisterClipboardFormatW(name)
def clear_clipboard():'Clears clipboard';_user32.OpenClipboard(0);_user32.EmptyClipboard();_user32.CloseClipboard()
def set_format(formatname:int=1,bytedata:bytes=b'test')->bool:
    'low level stuff';_user32.OpenClipboard(0);GlobalLock=_kernel32.GlobalLock;GlobalLock.restype=_ctypes.c_void_p;GlobalAlloc=_kernel32.GlobalAlloc;GlobalAlloc.restype=_ctypes.c_void_p
    try:_user32.EmptyClipboard();handle=_kernel32.GlobalAlloc(66,len(bytedata)+2);pcontents=GlobalLock(_ctypes.c_void_p(handle));_ctypes.memmove(pcontents,bytedata,len(bytedata));_kernel32.GlobalUnlock(_ctypes.c_void_p(handle));_user32.SetClipboardData(_ctypes.c_ulong(formatname),_ctypes.c_void_p(handle))
    finally:_user32.CloseClipboard()
def get_format(formatname:int=1,hexout:bool=False)->bytes:
    'low level stuff'
    if formatname==2:return('Image')
    ty=_ctypes.c_void_p;_kernel32.GlobalLock.argtypes=[ty];_kernel32.GlobalLock.restype=ty;_kernel32.GlobalUnlock.argtypes=[ty];_user32.GetClipboardData.restype=ty;_user32.OpenClipboard(0)
    try:
        if _user32.IsClipboardFormatAvailable(formatname):
            data=_user32.GetClipboardData(formatname);
            if data is None:return None#actually null type
            data_locked=_kernel32.GlobalLock(data);
            if data_locked is None:return None
            text1=bytes((_ctypes.c_char*_kernel32.GlobalSize(_ctypes.c_int64(data_locked))).from_address(data_locked));_kernel32.GlobalUnlock(data_locked)
            if hexout:text1=text1.hex().upper();text1=' '.join(text1[i:i+2]for i in range(0,len(text1),2))
            return text1
    finally:_user32.CloseClipboard()
def get_clipboard(names:bool=False,hexout:bool=False)->dict[bytes|str]:
    'gets clipboard all data';q=getformat(names);v={}
    for i in q[1]:v[i]=(get_format(i,hexout),q[1][i])if names else get_format(i,hexout)
    return v
def set_clipboard(formdata:dict={}):
    'sets clipboard all data';_user32.OpenClipboard(0);GlobalLock=_kernel32.GlobalLock;GlobalLock.restype=_ctypes.c_void_p;GlobalAlloc=_kernel32.GlobalAlloc;GlobalAlloc.restype=_ctypes.c_void_p
    try:
        _user32.EmptyClipboard()
        for formatname,bytedata in formdata.items():
            if bytedata is None:_user32.SetClipboardData(0)
            handle=_kernel32.GlobalAlloc(66,len(bytedata)+2);pcontents=GlobalLock(_ctypes.c_void_p(handle));_ctypes.memmove(pcontents,bytedata,len(bytedata));_kernel32.GlobalUnlock(_ctypes.c_void_p(handle));_user32.SetClipboardData(_ctypes.c_ulong(formatname),_ctypes.c_void_p(handle))
    finally:_user32.CloseClipboard()
def decode13(dat:bytes)->str:'decodes entry 13';return dat.decode('utf-16')[:-1]


#legacy/convenience functions
def toclipboard(string:str):'Puts text in clipboard';set_clipboard({13:string.encode('utf-16-le')})
def getclipboard()->str:'Gets text in clipboard';return decode13(get_clipboard().get(13,b''))
emptyclipboard=clear_clipboard;Simples=type('simpleclipboard',(),{'get':getclipboard,'set':toclipboard})
if'__main__'==__name__:print(q:=get_clipboard());print(decode13(q.get(13,b'')),end='\n')
#1/7 normal channel, 13 unicode channel, 49489 html/gdocs channel
