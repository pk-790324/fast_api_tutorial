from datetime import datetime
from typing import Optional

from pydantic import BaseModel,Field




class Contract(BaseModel):
    id:Optional[str]=None
    file_name:str
    original_name:str
    upload_data:str=""
    text_content:str=""
    page_count:int=0
    word_count:int=0
    status:str="uploaded"
    
    
def model_post_init(self,__context):
    if not self.upload_date:
        self.upload_date=datetime.now().isoformat()