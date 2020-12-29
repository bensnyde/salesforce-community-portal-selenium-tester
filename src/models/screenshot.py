from pydantic import BaseModel


class Screenshot(BaseModel):

    url : str 
    b64png : str
    cid : str