import ctypes as _ctypes
ReadError=type('ReadError',(OSError,),{})
crashonerror=True
def _readerr(a=0):
    if not a and crashonerror:raise ReadError('Console incompatible - Windows API returned error')
class _COORD(_ctypes.Structure):_fields_=(("X",_ctypes.c_short),("Y",_ctypes.c_short))
class _SMALL_RECT(_ctypes.Structure):_fields_=(("Left",_ctypes.c_short),("Top",_ctypes.c_short),("Right",_ctypes.c_short),("Bottom",_ctypes.c_short))
class _CONSOLE_SCREEN_BUFFER_INFO(_ctypes.Structure):_fields_=(("dwSize",_COORD),("dwCursorPosition",_COORD),("wAttributes",_ctypes.c_ushort),("srWindow",_SMALL_RECT),("dwMaximumWindowSize",_COORD))
class _POINT(_ctypes.Structure):_fields_=(("x",_ctypes.c_long),("y",_ctypes.c_long))
_STDOUT_HANDLE=_ctypes.windll.kernel32.GetStdHandle(-11)
zFOREGROUND_BLACK=0x0000;zFOREGROUND_BLUE=0x0001;zFOREGROUND_GREEN=0x0002;zFOREGROUND_CYAN=0x0003;zFOREGROUND_RED=0x0004;zFOREGROUND_MAGENTA=0x0005;zFOREGROUND_YELLOW=0x0006;zFOREGROUND_WHITE=zFOREGROUND_GREY=0x0007;zFOREGROUND_INTENSITY=0x0008#foreground color is intensified.
zBACKGROUND_BLACK=0x0000;zBACKGROUND_BLUE=0x0010;zBACKGROUND_GREEN=0x0020;zBACKGROUND_CYAN=0x0030;zBACKGROUND_RED=0x0040;zBACKGROUND_MAGENTA=0x0050;zBACKGROUND_YELLOW=0x0060;zBACKGROUND_GREY=zBACKGROUND_WHITE=0x0070;zBACKGROUND_INTENSITY=0x0080#background color is intensified.
def colorto(color:str,fg:bool=True):x={'black':0x0000,'blue':0x0001,'green':0x0002,'cyan':0x0003,'red':0x0004,'magenta':0x0005,'yellow':0x0006,'white':0x0007,'grey':0x0007,'intensity':0x0008}if fg else{'black':0x0000,'blue':0x0010,'green':0x0020,'cyan':0x0030,'red':0x0040,'magenta':0x0050,'yellow':0x0060,'grey':0x0070,'intensity':0x0080};return x if color is None else x[color]
def colorfrom(number:int):
    number=f'{number:>02x}';dictionary='black','blue','green','cyan','red','magenta','yellow','white','grey','intensity'
    if number.endswith('0'):return'fg',dictionary[int(number[-2])]
    elif number[-2]=='0':return'bg',dictionary[int(number[-1])]
    return('fg',dictionary[int(number[-1])]),('bg',dictionary[int(number[-2])])
def getcolor()->int:csbi=_CONSOLE_SCREEN_BUFFER_INFO();_readerr(_ctypes.windll.kernel32.GetConsoleScreenBufferInfo(_STDOUT_HANDLE,_ctypes.byref(csbi)));return csbi.wAttributes
def getconsolesize()->tuple[int]:csbi=_CONSOLE_SCREEN_BUFFER_INFO();_readerr(_ctypes.windll.kernel32.GetConsoleScreenBufferInfo(_STDOUT_HANDLE,_ctypes.byref(csbi)));return csbi.dwSize.X,csbi.dwSize.Y,(csbi.srWindow.Left,csbi.srWindow.Top,csbi.srWindow.Right,csbi.srWindow.Bottom)
def setcolor(color:int):_readerr(_ctypes.windll.kernel32.SetConsoleTextAttribute(_STDOUT_HANDLE,color))
def colorclear():setcolor(zFOREGROUND_WHITE)
def concur_to(x:int,y:int):_readerr(_ctypes.windll.kernel32.SetConsoleCursorPosition(_STDOUT_HANDLE,_COORD(x,y)))
def concur_at()->tuple[int]:csbi=_CONSOLE_SCREEN_BUFFER_INFO();_readerr(_ctypes.windll.kernel32.GetConsoleScreenBufferInfo(_STDOUT_HANDLE,_ctypes.byref(csbi)));return csbi.dwCursorPosition.X,csbi.dwCursorPosition.Y
def conlinesclear(a:int,b:int):
    c=concur_at();d=getcolor();setcolor(0);q=' '*getconsolesize()[0]
    for i in range(b-a):concur_to(0,i+a);print(q)
    concur_to(*c);setcolor(d)
def getcursor()->tuple[int]:pt=_POINT();_ctypes.windll.user32.GetCursorPos(_ctypes.byref(pt));return pt.x,pt.y
def setcursor(x:int,y:int):_ctypes.windll.user32.SetCursorPos(x,y)
#def setter():import ctypes as _ctypes;_COORD=type('_COORD',(_ctypes.Structure,),{'_fields_':[("X",_ctypes.c_short),("Y",_ctypes.c_short)]});_CONSOLE_SCREEN_BUFFER_INFO=type('_CONSOLE_SCREEN_BUFFER_INFO',(_ctypes.Structure,),{'_fields_':[("dwSize",_COORD),("dwCursorPosition",_COORD),("wAttributes",_ctypes.c_ushort),("srWindow",type('_SMALL_RECT',(_ctypes.Structure,),{'_fields_':[("Left",_ctypes.c_short),("Top",_ctypes.c_short),("Right",_ctypes.c_short),("Bottom",_ctypes.c_short)]})),("dwMaximumWindowSize",_COORD)]});_STDOUT_HANDLE=_ctypes.windll.kernel32.GetStdHandle(-11);concur_to=lambda x,y:_ctypes.windll.kernel32.SetConsoleCursorPosition(_STDOUT_HANDLE,_COORD(x,y));concur_at=lambda:(_ctypes.windll.kernel32.GetConsoleScreenBufferInfo(_STDOUT_HANDLE,_ctypes.byref(csbi:=_CONSOLE_SCREEN_BUFFER_INFO())),csbi.dwCursorPosition.X,csbi.dwCursorPosition.Y)[1:];return concur_to,concur_at
def click(clicktime=0,right=0):from time import sleep;_ctypes.windll.user32.mouse_event((32 if right==2 else 8)if right else 2,0,0,0,0);sleep(clicktime);_ctypes.windll.user32.mouse_event((64 if right==2 else 16)if right else 4,0,0,0,0)

#---------------------------------------------------------------------------------------------

def getconsoletitle(original:bool=False)->str:buf=_ctypes.create_unicode_buffer(1);f=_ctypes.windll.kernel32.GetConsoleOriginalTitleW if original else _ctypes.windll.kernel32.GetConsoleTitleW;length=f(buf,1);buf=_ctypes.create_unicode_buffer(length+1);f(buf,length+1);return buf.value if buf.value else None
def setconsoletitle(text:str):_ctypes.windll.kernel32.SetConsoleTitleW(text)
class _CONSOLE_SELECTION_INFO(_ctypes.Structure):_fields_=(("dwFlags",_ctypes.c_ulong),("dwSelectionAnchor",_COORD),("srSelection",_SMALL_RECT))
def getconselection()->dict[int]:cssi=_CONSOLE_SELECTION_INFO();_ctypes.windll.kernel32.GetConsoleSelectionInfo(_ctypes.byref(cssi));cssi=cssi.srSelection;cssi={'Top':cssi.Top,'Left':cssi.Left,'Right':cssi.Right,'Bottom':cssi.Bottom};return None if{*cssi.values()}=={0}else cssi
getcolour=getcolor;setcolour=setcolor;colourclear=colorclear;colourto=colorto;colourfrom=colorfrom


class _CONSOLE_FONT_INFO(_ctypes.Structure):_fields_=(("cbSize",_ctypes.c_ulong),("nFont",_ctypes.c_ulong),("dwFontSize",_COORD),("FontFamily",_ctypes.c_uint),("FontWeight",_ctypes.c_uint),("FaceName",_ctypes.c_wchar*32))
def getconsolefontdata()->_CONSOLE_FONT_INFO:struct=_CONSOLE_FONT_INFO();struct.cbSize=_ctypes.sizeof(_CONSOLE_FONT_INFO);return'Fail'if not _ctypes.windll.kernel32.GetCurrentConsoleFontEx(_STDOUT_HANDLE,0,_ctypes.pointer(struct))else struct
class _CONSOLE_CURSOR_INFO(_ctypes.Structure):_fields_=(('dwSize',_ctypes.c_ulong),('bVisible',_ctypes.c_long))
def getconcurdata()->tuple[int]:a=_CONSOLE_CURSOR_INFO();return(a.dwSize,a.bVisible)if _ctypes.windll.kernel32.GetConsoleCursorInfo(_STDOUT_HANDLE,_ctypes.pointer(a))else _readerr()
def setconcurdata(size:int,visible:bool):a=_CONSOLE_CURSOR_INFO(size,visible);_readerr(_ctypes.windll.kernel32.SetConsoleCursorInfo(_STDOUT_HANDLE,_ctypes.pointer(a)))
def consolewrite(text:str,x:int,y:int)->int:c=_ctypes.c_ulong();_readerr(_ctypes.windll.kernel32.WriteConsoleOutputCharacterW(_STDOUT_HANDLE,text,len(text),_COORD(x,y),_ctypes.byref(c)));return c.value

#---------------------------------------------------------------------------------------------

def dumpCstruct(a):return f'{a.__class__.__name__}{repr({i:getattr(a,i)for i,v in a._fields_})}'
#for a in(_COORD,_SMALL_RECT,_CONSOLE_SCREEN_BUFFER_INFO,_POINT,_CONSOLE_SELECTION_INFO,_CONSOLE_FONT_INFO,_CONSOLE_CURSOR_INFO,_CHAR_INFO,_charunion):a.__repr__=dumpCstruct
#del a

#ReadConsoleOutput & ReadConsoleOutputAttribute uses a struct called CHAR_INFO, and I can't get them to work. So read/write text & color will have to be done seperately...
#TODO: CHAR_INFO
#Thanks to "Eryk Sun" https://stackoverflow.com/questions/38698383/executable-called-via-subprocess-check-output-prints-on-console-but-result-is-no
def read_screen(colour:bool=False)->list[tuple[str|int]]|str:
    start=_COORD(0,0);csbi=_CONSOLE_SCREEN_BUFFER_INFO();_ctypes.windll.kernel32.GetConsoleScreenBufferInfo(_STDOUT_HANDLE,_ctypes.byref(csbi));pos=csbi.dwCursorPosition;length=csbi.dwSize.X*pos.Y+pos.X+1;buf=_ctypes.create_unicode_buffer(length);n=(_ctypes.c_ulong*1)();_readerr(_ctypes.windll.kernel32.ReadConsoleOutputCharacterW(_STDOUT_HANDLE,buf,length,start,n))
    if colour:from ctypes import wintypes;b2=(_ctypes.c_wchar*length)();b2=(wintypes.WORD*length)();n=(_ctypes.c_ulong*1)();_readerr(_ctypes.windll.kernel32.ReadConsoleOutputAttribute(_STDOUT_HANDLE,b2,length,start,n));return[*zip(buf.value,b2)]
    return buf.value


#---------------------------------------------------------------------------------------------




class _CURSORINFO(_ctypes.Structure):_fields_=(('cbSize',_ctypes.c_uint),('flags',_ctypes.c_uint),('hCursor',_ctypes.c_void_p),('ptScreenPos',_POINT))
def getcursordat()->int:'Zero for hidden, 1 for showing, 2 for windows 8 stuff';b=_CURSORINFO();b.cbSize=_ctypes.sizeof(b);_ctypes.windll.user32.GetCursorInfo(_ctypes.byref(b));return b.flags#0 means hidden, 1 means showing, 2 means touch/pen hidden
def getDPI1()->int:'uses ctypes, has side effects';_ctypes.windll.shcore.SetProcessDpiAwareness(2-1);c=__import__('tkinter').Tk();a=round(c.winfo_fpixels('1i'));c.destroy();return a
#import ctypes,tkinter;ctypes.windll.shcore.SetProcessDpiAwareness(1);root=tkinter.Tk();dpi=ctypes.windll.user32.GetDpiForWindow(root.winfo_id());root.destroy()
def getDPI_safe()->int:'uses PowerShell to extract data, no side-effects.';import subprocess;silentstart=subprocess.STARTUPINFO();silentstart.dwFlags|=subprocess.STARTF_USESHOWWINDOW;return int(subprocess.run(r"PowerShell (Get-ItemProperty -Path 'HKCU:\Control Panel\Desktop').LogPixels",stdout=subprocess.PIPE,startupinfo=silentstart).stdout)
"PowerShell -Command  \"cd 'HKCU:\\Control Panel\\Desktop';(Get-ItemProperty -Path . -Name 'LogPixels').LogPixels\"\nPowerShell -Command  \"(Get-ItemProperty -Path 'HKCU:\\Control Panel\\Desktop' -Name 'LogPixels').LogPixels\"\nPowerShell -Command  \"(Get-ItemProperty -Path 'HKCU:\\Control Panel\\Desktop').LogPixels\"\nPowerShell \"(Get-ItemProperty -Path 'HKCU:\\Control Panel\\Desktop').LogPixels\"\nPowerShell (Get-ItemProperty -Path 'HKCU:\\Control Panel\\Desktop').LogPixels\n"
def DPI_to_scale(a:int)->float:return{'144':1.5,'120':1.25,'96':1}[f'{a}']# x/96
# def monitordatas(setDPIaware=False):
#     'warning: setting DPI Aware has side effects'
#     if setDPIaware:_ctypes.windll.shcore.SetProcessDpiAwareness(1)
#     user32=_ctypes.windll.user32;
#     moncount=user32.GetSystemMetrics(80)
#     yield('count',moncount)
#     yield('primary',user32.GetSystemMetrics(0),user32.GetSystemMetrics(1))
#     yield('sum',user32.GetSystemMetrics(78),user32.GetSystemMetrics(79))
def get_monitors_resolution(setDPIaware:bool=False)->list[tuple[int]]:
    'warning: setting DPI Aware has side effects - thanks to https://stackoverflow.com/questions/54271887/calculate-screen-dpi'
    if setDPIaware:_ctypes.windll.shcore.SetProcessDpiAwareness(1)
    user32=_ctypes.windll.user32;import ctypes.wintypes;monitors=[];monitor_enum_proc=_ctypes.WINFUNCTYPE(_ctypes.c_int,_ctypes.c_ulong,_ctypes.c_ulong,_ctypes.POINTER(ctypes.wintypes.RECT),_ctypes.c_double)
    def callback(hMonitor,hdcMonitor,lprcMonitor,dwData):monitors.append((lprcMonitor.contents.right-lprcMonitor.contents.left,lprcMonitor.contents.bottom-lprcMonitor.contents.top));return 1
    user32.EnumDisplayMonitors(None,None,monitor_enum_proc(callback),0);return monitors

# def _RECT():import ctypes.wintypes;return ctypes.wintypes.RECT
# _RECT=_RECT()
_console_handle=_ctypes.WinDLL('kernel32').GetConsoleWindow()
def get_window_dimensions(handle=_console_handle)->tuple[int]:import ctypes.wintypes;rect=ctypes.wintypes.RECT();_ctypes.windll.user32.GetWindowRect(handle,_ctypes.pointer(rect));return(rect.left,rect.top,rect.right,rect.bottom)
def get_window_handle_byname(name:str=None):return _ctypes.windll.user32.FindWindowW(None,name)
def get_window_handle_console():return _ctypes.WinDLL('kernel32').GetConsoleWindow()
def set_window_state(handle=_console_handle,state:int=11):
    '''State is between 0 and 11 with various effects. 11 forces minimise. 9 restores, https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-showwindow

    SW_HIDE 0	Hides the window and activates another window.
    SW_SHOWNORMAL   SW_NORMAL   1	Activates and displays a window. If the window is minimized, maximized, or arranged, the system restores it to its original size and position. An application should specify this flag when displaying the window for the first time.
    SW_SHOWMINIMIZED    2	Activates the window and displays it as a minimized window.
    SW_SHOWMAXIMIZED/SW_MAXIMIZE 3	Activates the window and displays it as a maximized window.
    SW_SHOWNOACTIVATE   4	Displays a window in its most recent size and position. This value is similar to SW_SHOWNORMAL, except that the window is not activated.
    SW_SHOW 5	Activates the window and displays it in its current size and position.
    SW_MINIMIZE 6	Minimizes the specified window and activates the next top-level window in the Z order.
    SW_SHOWMINNOACTIVE  7	Displays the window as a minimized window. This value is similar to SW_SHOWMINIMIZED, except the window is not activated.
    SW_SHOWNA   8	Displays the window in its current size and position. This value is similar to SW_SHOW, except that the window is not activated.
    SW_RESTORE  9	Activates and displays the window. If the window is minimized, maximized, or arranged, the system restores it to its original size and position. An application should specify this flag when restoring a minimized window.
    SW_SHOWDEFAULT  10	Sets the show state based on the SW_ value specified in the STARTUPINFO structure passed to the CreateProcess function by the program that started the application.
    SW_FORCEMINIMIZE    11	Minimizes a window, even if the thread that owns the window is not responding. This flag should only be used when minimizing windows from a different thread.''';_ctypes.windll.user32.ShowWindow(handle,state)
def SetForegroundWindow(handle=_console_handle):'May not work';return _ctypes.windll.user32.SetForegroundWindow(handle)
def set_window_dimensions(x,y,width,height,handle=_console_handle,refresh=False):return not not _ctypes.windll.user32.MoveWindow(handle,x,y,width,height,refresh)
def set_window_dimensions_Z(handle,X,Y,cx,cy,Z=None,FLAG=None):'Z parameter seems to work with None, 1, 0, and -1 for topmost. Flag is a complete mystery to me';import ctypes.wintypes;_ctypes.windll.user32.SetWindowPos(handle,ctypes.wintypes.HWND(Z),X,Y,cx,cy,FLAG)

def concur_shift(dx:int,dy:int):x,y=concur_at();_readerr(_ctypes.windll.kernel32.SetConsoleCursorPosition(_STDOUT_HANDLE,_COORD(dx+x,dy+y)))
