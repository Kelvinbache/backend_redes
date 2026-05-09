import os 
import pathlib
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

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

class PuertoRed(BaseModel):
    title: str
    definition: str
    general_analogy: str
    classifications: List[Dict[str, Any]]

class Socket(BaseModel):
    title: str
    definition: str
    general_analogy: str
    properties: List[Dict[str, str]]
    types: List[Dict[str, str]]

class IEE8023(BaseModel):
    title: str
    definition: str
    general_analogy: str
    types: List[Dict[str, Any]]
    media_types: List[str]

class IEE80211(BaseModel):
    title: str
    definition: str
    general_analogy: str
    generations: List[Dict[str, Any]]
    modulations: List[str]
    frequency_bands: List[Dict[str, str]]

class TransmissionMethod(BaseModel):
    title: str
    definition: str
    general_analogy: str
    methods: List[Dict[str, Any]]

class RedesInvestigacionCompleta(BaseModel):
    network_ports: PuertoRed
    sockets: Socket
    ieee_802_3: IEE8023
    ieee_802_11: IEE80211
    transmission_methods: TransmissionMethod


# Construcción de la ruta al archivo JSON
split_path = os.getcwd().split("/")[0:6]
path = ""

for i in range(len(split_path)):
    path += split_path[i] + "/"

path_joint = os.path.join(path, "json", "Puertos.json")

# Cargar el JSON
json_path = pathlib.Path(path_joint).read_text(encoding='utf-8')
modelos = RedesInvestigacionCompleta.model_validate_json(json_path)

# Opcional: Exportar los datos individuales para fácil acceso
puertos_red = modelos.network_ports
sockets = modelos.sockets
ieee_802_3 = modelos.ieee_802_3
ieee_802_11 = modelos.ieee_802_11
transmission_methods = modelos.transmission_methods
