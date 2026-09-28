"""Public website QA entrypoint. Optional argument: exact deployment URL.
The film-only checks were superseded by the four-device interactive test, which
also exercises all three preserved films and writes only qa/interactive/.
"""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).with_name('verify_interactive.py')),run_name='__main__')
