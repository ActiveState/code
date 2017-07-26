import ctypes

def XVID_MAKE_VERSION(a,b,c): return ((((a)&0xff)<<16) | (((b)&0xff)<<8) | ((c)&0xff))
XVID_VERSION=XVID_MAKE_VERSION(1,3,3)

XVID_GBL_INIT=0
XVID_GBL_INFO=1

XVID_DEC_CREATE=0
XVID_DEC_DESTROY=1
XVID_DEC_DECODE=2

XVID_CSP_RGB=(1<<16)

XVID_TYPE_VOL=-1

BUFFER_SIZE=2*1024*1024
BPP=3
XDIM=0
YDIM=0

class xvid_dec_create_t(ctypes.Structure):
 _fields_=[
  ('version', ctypes.c_int),
  ('width', ctypes.c_int),
  ('height', ctypes.c_int),
  
  ('handle', ctypes.c_void_p),
  
  ('fourcc', ctypes.c_int),
  ('num_threads', ctypes.c_int),
 ]

class xvid_gbl_init_t(ctypes.Structure):
 _fields_=[
  ('version',ctypes.c_int),
  ('cpu_flags',ctypes.c_uint),
  ('debug',ctypes.c_int),
 ]

class xvid_gbl_info_t(ctypes.Structure):
 _fields_=[
  ('version',ctypes.c_int),
  ('actual_version',ctypes.c_int),
  ('build',ctypes.c_char_p),
  ('cpu_flags',ctypes.c_uint),
  ('num_threads',ctypes.c_int),
 ]



class xvid_dec_stats_t__data__vol(ctypes.Structure):
 _fields_=[
  ('general',ctypes.c_int),
  ('width',ctypes.c_int),
  ('height',ctypes.c_int),
  ('par',ctypes.c_int),
  ('par_width',ctypes.c_int),
  ('par_height',ctypes.c_int),
 ]

class xvid_dec_stats_t__data__vop(ctypes.Structure):
 _fields_=[
  ('general',ctypes.c_int),
  ('time_base',ctypes.c_int),
  ('time_increment',ctypes.c_int),
  ('qscale',ctypes.POINTER(ctypes.c_int)),
  ('qscale_stride',ctypes.c_int),
 ]

class xvid_dec_stats_t__data(ctypes.Union):
 _fields_=[
  ('vop',xvid_dec_stats_t__data__vop),
  ('vol',xvid_dec_stats_t__data__vol),
 ]

class xvid_dec_stats_t(ctypes.Structure):
 _fields_=[
  ('version',ctypes.c_int),
  ('type',ctypes.c_int),
  ('data',xvid_dec_stats_t__data),
 ]



class xvid_image_t(ctypes.Structure):
 _fields_=[
  ('csp',ctypes.c_int),
  ('plane',ctypes.c_void_p*4),
  ('stride',ctypes.c_int*4),
 ]

class xvid_dec_frame_t(ctypes.Structure):
 _fields_=[
  ('version',ctypes.c_int),
  ('general',ctypes.c_int),
  ('bitstream',ctypes.c_void_p),
  ('length',ctypes.c_int),
  ('output',xvid_image_t),
  ('brightness',ctypes.c_int),
 ]



xvid_dec_create=None

def xvid_init():
 global xvid_dec_create

 xvid_gbl_info=xvid_gbl_info_t()
 xvid_gbl_info.version=XVID_VERSION
 ctypes.cdll.xvidcore.xvid_global(None,XVID_GBL_INFO,ctypes.byref(xvid_gbl_info),None)
 xvid_gbl_info.actual_version

 xvid_gbl_init=xvid_gbl_init_t()
 xvid_gbl_init.version=XVID_VERSION
 xvid_gbl_init.cpu_flags=0
 ctypes.cdll.xvidcore.xvid_global(None,XVID_GBL_INIT,ctypes.byref(xvid_gbl_init),None)

 xvid_dec_create=xvid_dec_create_t()
 xvid_dec_create.version=XVID_VERSION
 xvid_dec_create.num_threads=xvid_gbl_info.num_threads
 return ctypes.cdll.xvidcore.xvid_decore(None,XVID_DEC_CREATE,ctypes.byref(xvid_dec_create),None)

def xvid_quit():
 global xvid_dec_create
 xvid_close()
 result=ctypes.cdll.xvidcore.xvid_decore(xvid_dec_create.handle,XVID_DEC_DESTROY,None,None)
 xvid_dec_create=None
 return result



_xvid_input_file=None
_xvid_input_file_eof=False
_xvid_mp4_buffer=None
_xvid_mp4_buffer_position=0
_xvid_mp4_ptr=None
_xvid_out_buffer=None

def xvid_open(fn):
 global _xvid_input_file,_xvid_mp4_buffer,_xvid_mp4_ptr,_xvid_mp4_buffer_position,_xvid_input_file_eof,xvid_dec_create
 if xvid_dec_create is None: xvid_init()
 xvid_close()
 _xvid_input_file=open(fn,'rb')
 _xvid_mp4_buffer=ctypes.create_string_buffer(BUFFER_SIZE)
 _xvid_mp4_buffer.value=_xvid_input_file.read(BUFFER_SIZE)
 _xvid_mp4_ptr=ctypes.pointer(_xvid_mp4_buffer)
 _xvid_mp4_buffer_position=0
 _xvid_input_file_eof=False

def xvid_close():
 global _xvid_input_file,_xvid_mp4_buffer_position
 if _xvid_input_file is None: return
 _xvid_input_file.close()
 _xvid_input_file=None
 _xvid_mp4_buffer_position=0

def xvid_decode_frame():
 global xvid_dec_create,_xvid_mp4_buffer,_xvid_mp4_buffer_position,_xvid_out_buffer,_xvid_mp4_ptr,_xvid_input_file,XDIM,YDIM,_xvid_input_file_eof

 if _xvid_mp4_buffer_position>BUFFER_SIZE-40: return False# shortest frames have around 38,39 bytes, at the end there could remain some (3 in my test vid) unusable bytes in buffer
 if xvid_dec_create is None: return False
 
 #input buffer check
 if _xvid_mp4_buffer_position>BUFFER_SIZE/2 and not _xvid_input_file_eof:
  chunksize=BUFFER_SIZE-_xvid_mp4_buffer_position
  chunk=_xvid_input_file.read(chunksize)
  if len(chunk)<chunksize: _xvid_input_file_eof=True
  _xvid_mp4_buffer.value=(_xvid_mp4_buffer.raw+chunk)[-BUFFER_SIZE:]
  _xvid_mp4_buffer_position=chunksize-len(chunk)
  _xvid_mp4_ptr=ctypes.pointer(_xvid_mp4_buffer)
 
 
 xvid_dec_stats=xvid_dec_stats_t()
 xvid_dec_stats.version=XVID_VERSION

 xvid_dec_frame=xvid_dec_frame_t()
 xvid_dec_frame.version=XVID_VERSION
 xvid_dec_frame.general=0
 xvid_dec_frame.bitstream=ctypes.cast(_xvid_mp4_ptr,ctypes.c_void_p)
 xvid_dec_frame.length=len(_xvid_mp4_buffer)-_xvid_mp4_buffer_position
 xvid_dec_frame.output.plane[0]=ctypes.cast(_xvid_out_buffer,ctypes.c_void_p)
 xvid_dec_frame.output.stride[0]=XDIM*BPP
 xvid_dec_frame.output.csp=XVID_CSP_RGB
 
 used=ctypes.cdll.xvidcore.xvid_decore(xvid_dec_create.handle,XVID_DEC_DECODE,ctypes.byref(xvid_dec_frame),ctypes.byref(xvid_dec_stats))
 _xvid_mp4_buffer_position+=used
 if used==0: print _xvid_mp4_buffer_position,BUFFER_SIZE,BUFFER_SIZE-_xvid_mp4_buffer_position
 _xvid_mp4_ptr=ctypes.cast(ctypes.cast(_xvid_mp4_buffer,ctypes.c_void_p).value+_xvid_mp4_buffer_position,ctypes.c_char_p)

 if xvid_dec_stats.type==XVID_TYPE_VOL:
  if XDIM*YDIM<xvid_dec_stats.data.vol.width*xvid_dec_stats.data.vol.height:
   XDIM=xvid_dec_stats.data.vol.width
   YDIM=xvid_dec_stats.data.vol.height
   _xvid_out_buffer=ctypes.create_string_buffer(XDIM*YDIM*4)
  return xvid_decode_frame()
 
 return _xvid_out_buffer.raw
