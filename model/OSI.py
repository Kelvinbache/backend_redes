import os 
import pathlib
from pydantic import BaseModel
from typing import List

class OsiLayer(BaseModel):
    level: int  
    name: str 
    function: str 
    pdu: str  
    examples: List[str]  

class TCPIPComparison(BaseModel):
    note: str
    key_difference: str

class OsiModel(BaseModel):
    title: str
    definition: str
    general_analogy: str
    layers: List[OsiLayer]  
    tcp_ip_comparison: TCPIPComparison  

class OsiModelCompleto(BaseModel):
    osi_model: OsiModel


split_path = os.getcwd().split("/")[0:6]
path = ""

for i in range(len(split_path)):
    path += split_path[i] + "/"

path_joint_osi = os.path.join(path, "json", "ISO.json")

json_path = pathlib.Path(path_joint_osi).read_text(encoding='utf-8')
modelo_osi = OsiModelCompleto.model_validate_json(json_path)

osi = modelo_osi.osi_model
