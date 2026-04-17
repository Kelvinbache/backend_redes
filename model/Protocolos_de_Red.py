import os 
import pathlib
from pydantic import BaseModel
from typing import List

class ProtocoloRed(BaseModel):
    title: str
    definition: str

class ProtocoloRed_Type(BaseModel):    
    category: str
    description: str
    examples: List[str] 

class ProtocoloRed_Function(BaseModel):    
    name: str
    detail: str

class NetworkProtocols(BaseModel):
    title: str
    definition: str
    types: List[ProtocoloRed_Type]
    functions: List[ProtocoloRed_Function]

class ProtocoloRedCompleto(BaseModel):
    network_protocols: NetworkProtocols



split_path = os.getcwd().split("/")[0:6]
path = ""

for i in range(len(split_path)):
    path += split_path[i] + "/"

path_joint_protocolos_red = os.path.join(path,"json","ProtocoloRed.json")

json_path = pathlib.Path(path_joint_protocolos_red).read_text(encoding='utf-8')

model_completo = ProtocoloRedCompleto.model_validate_json(json_path)

protocolo_red = model_completo.network_protocols
