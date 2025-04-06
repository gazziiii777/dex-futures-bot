from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MEXCNewCoin(BaseModel):  
    name: Optional[str]
    symbol: Optional[str]
    slug: Optional[str] 
    chain: Optional[str]
    token_address: Optional[str] 
    logo: Optional[str] 
    signal: Optional[bool] 
    
class MEXCSymbol(BaseModel):  
    symbol: Optional[str]
    
class MEXCUpdateSignal(BaseModel):  
    symbol: Optional[str]
    signal: Optional[bool] 