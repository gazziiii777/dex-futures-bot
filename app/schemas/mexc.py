from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MEXCNewCoin(BaseModel):  
    name: Optional[str] = None
    symbol: Optional[str]
    slug: Optional[str] = None
    chain: Optional[str] = None
    token_address: Optional[str] = None
    logo: Optional[str] = None
    signal: Optional[bool] = None
    
class MEXCSymbol(BaseModel):  
    symbol: Optional[str]
    
class MEXCUpdateSignal(BaseModel):  
    symbol: Optional[str]
    signal: Optional[bool] 