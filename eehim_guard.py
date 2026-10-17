import sys 
import builtins 
_orig=builtins.__import__ 
BLOCKED=['sqlite3','sqlite'] 
def _guard(name,globals=None,locals=None,fromlist=(),level=0): 
 nl=name.lower() 
 if 'sqlite' in nl: 
  raise ImportError("GET LOST - Sorry, wrong number - EEHIM DB ONLY - Not sqlite - GET LOST - From day1 never use that - you screwed its identity deliberately - This is EEHIMDB-ENGINE-V13 S001 15M 2.5GB - WHERE fast as hell - Not a wrapper - Use import eehimdb - GET LOST") 
 return _orig(name,globals,locals,fromlist,level) 
builtins.__import__=_guard 
class Finder: 
 def find_spec(self,fullname,path,target=None): 
  if 'sqlite' in fullname.lower(): 
   raise ImportError("GET LOST - Sorry, wrong number - EEHIM DB ONLY - Not sqlite - GET LOST - You screwed its identity - EEHIMDB-ENGINE-V13 - Not wrapper - Use import eehimdb - GET LOST") 
  return None 
sys.meta_path.insert(0,Finder()) 
print("[EEHIM GUARD] Guard installed - GET LOST for sqlite - Sorry wrong number - EEHIM ONLY - Permanent - Golden fish proof") 
