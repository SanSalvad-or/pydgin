#=========================================================================
# parc-sim.py
#=========================================================================

import os
import sys

# ensure we know where the pypy source code is
try:
  sys.path.append( os.environ['PYDGIN_PYPY_SRC_DIR'] )
except KeyError as e:
  raise ImportError( 'Please define the PYDGIN_PYPY_SRC_DIR '
                     'environment variable!')

# need to add parent directory to get access to pydgin package
# TODO: cleaner way to do this?
sys.path.append('..')

from pydgin.sim     import Sim, init_sim
from pydgin.storage import Memory
# TODO: use load_program of pydgin.misc
#from pydgin.misc    import load_program
import elf

from bootstrap      import syscall_init, test_init, memory_size
from instruction    import Instruction
from isa            import decode, reg_map

#-------------------------------------------------------------------------
# ParcSim
#-------------------------------------------------------------------------
# PARC Simulator

class ParcSim( Sim ):

  def __init__( self ):
    Sim.__init__( self, "PARC", jit_enabled=True )

  #-----------------------------------------------------------------------
  # decode
  #-----------------------------------------------------------------------
  # The simulator calls architecture-specific decode to decode the
  # instruction bits

  def decode( self, bits ):
    # TODO add decode inside instruction:
    #return decode( bits )
    inst_str, exec_fun = decode( bits )
    return Instruction( bits, inst_str ), exec_fun

  #-----------------------------------------------------------------------
  # init_state
  #-----------------------------------------------------------------------
  # This method is called to load the program and initialize architectural
  # state

  def init_state( self, exe_file, run_argv, run_envp ):

    # Load the program into a memory object

    mem, breakpoint = load_program( exe_file )

    # Insert bootstrapping code into memory and initialize processor state

    # TODO: testbin is hardcoded false right now
    testbin = False

    if testbin: self.state = test_init   ( mem, debug )
    else:       self.state = syscall_init( mem, breakpoint, run_argv,
                                           run_envp, self.debug )

  #---------------------------------------------------------------------
  # run
  #---------------------------------------------------------------------
  # Override sim's run to print stat_ncycles on exit

  def run( self ):
    Sim.run( self )
    print "Instructions Executed in Stat Region =", self.state.stat_ncycles

#-----------------------------------------------------------------------
# load_program
#-----------------------------------------------------------------------
# TODO: refactor this as well

def load_program( fp ):
  mem_image = elf.elf_reader( fp )

  sections = mem_image.get_sections()
  mem      = Memory( size=memory_size, byte_storage=False )

  for section in sections:
    start_addr = section.addr
    for i, data in enumerate( section.data ):
      mem.write( start_addr+i, 1, ord( data ) )

  bss        = sections[-1]
  breakpoint = bss.addr + len( bss.data )
  return mem, breakpoint

# this initializes similator and allows translation and python
# interpretation

init_sim( ParcSim() )

