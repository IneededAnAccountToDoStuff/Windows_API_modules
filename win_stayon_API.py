class WindowsLock:
    '''Prevent sleep/hibernate/display lock

    inhibit sleep allows processes to continue
    inhibit display keeps the screen on
    The code contains a ES_AWAYMODE_REQUIRED that I don't quite understand

    Honestly, inhibit_display is the only one that seems to work.
    '''
    ES_CONTINUOUS=0x80000000;ES_SYSTEM_REQUIRED=0x01;ES_DISPLAY_REQUIRED=0x02;ES_AWAYMODE_REQUIRED=0x40#ES_AWAYMODE_REQUIRED is only to be used in emergencies.
    import ctypes;__ca=ctypes.windll.kernel32.SetThreadExecutionState
    def inhibit_sleep(self=0):WindowsLock.__ca(WindowsLock.ES_CONTINUOUS|WindowsLock.ES_SYSTEM_REQUIRED)
    def inhibit_display(self=0):WindowsLock.__ca(WindowsLock.ES_CONTINUOUS|WindowsLock.ES_DISPLAY_REQUIRED)
    def uninhibit(self=0):WindowsLock.__ca(WindowsLock.ES_CONTINUOUS)
    def __init__(self,mode=0):self.m=mode
    def __enter__(self):self.inhibit_sleep()if self.m else self.inhibit_display()
    def __exit__(self,*a):self.uninhibit()
    #https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-setthreadexecutionstate


if'__main__'==__name__:
    import tkinter as tk;_=tk.Tk();_.title('Sleep Suspended');_.attributes('-toolwindow');tk.Label(text='Keeping Awake...').pack(side='left');q=lambda *x:_.destroy();tk.Button(text='Stop',command=q).pack(side='right');_.bind('<Shift-Escape>',q)
    with WindowsLock():_.mainloop()
