import uvicorn
import os
import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from typing import List, Optional, Dict, Any
from model.Puertos import ( 
    RedesInvestigacionCompleta,
    PuertoRed,
    Socket,
    IEE8023,
    IEE80211,
    TransmissionMethod,
    modelos  
)


# 1. Puertos de Red
@strawberry.type
class GraphQLPuertoClasificacion:
    type: str
    description: str
    range: Optional[str] = None
    examples: List[str]

@strawberry.type
class GraphQLPuertoRed:
    title: str
    definition: str
    general_analogy: str
    classifications: List[GraphQLPuertoClasificacion]


# 2. Sockets
@strawberry.type
class GraphQLSocketPropiedad:
    name: str
    description: str

@strawberry.type
class GraphQLSocketTipo:
    name: str
    description: str
    protocol: str

@strawberry.type
class GraphQLSocket:
    title: str
    definition: str
    general_analogy: str
    properties: List[GraphQLSocketPropiedad]
    types: List[GraphQLSocketTipo]


# 3. IEEE 802.3
@strawberry.type
class GraphQLIEEE8023Tipo:
    name: str
    speed: str
    medium: str
    max_distance: str

@strawberry.type
class GraphQLIEEE8023:
    title: str
    definition: str
    general_analogy: str
    types: List[GraphQLIEEE8023Tipo]
    media_types: List[str]


# 4. IEEE 802.11
@strawberry.type
class GraphQLIEEE80211Generacion:
    standard: str
    wi_fi_name: Optional[str]
    year: str
    speed: str
    frequency: str
    features: Optional[List[str]]
    status: Optional[str]

@strawberry.type
class GraphQLIEEE80211Banda:
    band: str
    characteristics: str

@strawberry.type
class GraphQLIEEE80211:
    title: str
    definition: str
    general_analogy: str
    generations: List[GraphQLIEEE80211Generacion]
    modulations: List[str]
    frequency_bands: List[GraphQLIEEE80211Banda]


# 5. Métodos de Transmisión
@strawberry.type
class GraphQLTransmissionMethod:
    type: str
    ratio: str
    description: str
    examples: List[str]
    address_example: str

@strawberry.type
class GraphQLTransmissionMethods:
    title: str
    definition: str
    general_analogy: str
    methods: List[GraphQLTransmissionMethod]


# Contenedor principal (opcional)
@strawberry.type
class GraphQLRedesInvestigacionCompleta:
    network_ports: GraphQLPuertoRed
    sockets: GraphQLSocket
    ieee_802_3: GraphQLIEEE8023
    ieee_802_11: GraphQLIEEE80211
    transmission_methods: GraphQLTransmissionMethods


# ============ CONVERSORES ============

def convert_puertos_to_graphql(puertos: PuertoRed) -> GraphQLPuertoRed:
    classifications = [
        GraphQLPuertoClasificacion(
            type=c.get("type", ""),
            description=c.get("description", ""),
            range=c.get("range"),
            examples=c.get("examples", [])
        )
        for c in puertos.classifications
    ]
    return GraphQLPuertoRed(
        title=puertos.title,
        definition=puertos.definition,
        general_analogy=puertos.general_analogy,
        classifications=classifications
    )

def convert_sockets_to_graphql(sockets: Socket) -> GraphQLSocket:
    properties = [
        GraphQLSocketPropiedad(
            name=p.get("name", ""),
            description=p.get("description", "")
        )
        for p in sockets.properties
    ]
    types = [
        GraphQLSocketTipo(
            name=t.get("name", ""),
            description=t.get("description", ""),
            protocol=t.get("protocol", "")
        )
        for t in sockets.types
    ]
    return GraphQLSocket(
        title=sockets.title,
        definition=sockets.definition,
        general_analogy=sockets.general_analogy,
        properties=properties,
        types=types
    )

def convert_8023_to_graphql(ieee: IEE8023) -> GraphQLIEEE8023:
    types = [
        GraphQLIEEE8023Tipo(
            name=t.get("name", ""),
            speed=t.get("speed", ""),
            medium=t.get("medium", ""),
            max_distance=t.get("max_distance", "")
        )
        for t in ieee.types
    ]
    return GraphQLIEEE8023(
        title=ieee.title,
        definition=ieee.definition,
        general_analogy=ieee.general_analogy,
        types=types,
        media_types=ieee.media_types
    )

def convert_80211_to_graphql(ieee11: IEE80211) -> GraphQLIEEE80211:
    generations = [
        GraphQLIEEE80211Generacion(
            standard=g.get("standard", ""),
            wi_fi_name=g.get("wi_fi_name"),
            year=str(g.get("year", "")),
            speed=g.get("speed", ""),
            frequency=g.get("frequency", ""),
            features=g.get("features"),
            status=g.get("status")
        )
        for g in ieee11.generations
    ]
    frequency_bands = [
        GraphQLIEEE80211Banda(
            band=b.get("band", ""),
            characteristics=b.get("characteristics", "")
        )
        for b in ieee11.frequency_bands
    ]
    return GraphQLIEEE80211(
        title=ieee11.title,
        definition=ieee11.definition,
        general_analogy=ieee11.general_analogy,
        generations=generations,
        modulations=ieee11.modulations,
        frequency_bands=frequency_bands
    )

def convert_transmission_to_graphql(trans: TransmissionMethod) -> GraphQLTransmissionMethods:
    methods = [
        GraphQLTransmissionMethod(
            type=m.get("type", ""),
            ratio=m.get("ratio", ""),
            description=m.get("description", ""),
            examples=m.get("examples", []),
            address_example=m.get("address_example", "")
        )
        for m in trans.methods
    ]
    return GraphQLTransmissionMethods(
        title=trans.title,
        definition=trans.definition,
        general_analogy=trans.general_analogy,
        methods=methods
    )


# ============ QUERY ============

@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello, World!"
    
    # ===== Consultas individuales =====
    
    @strawberry.field
    def get_puertos_red(self) -> GraphQLPuertoRed:
        """Obtiene toda la información de Puertos de Red"""
        return convert_puertos_to_graphql(modelos.network_ports)
    
    @strawberry.field
    def get_sockets(self) -> GraphQLSocket:
        """Obtiene toda la información de Sockets"""
        return convert_sockets_to_graphql(modelos.sockets)
    
    @strawberry.field
    def get_ieee_802_3(self) -> GraphQLIEEE8023:
        """Obtiene toda la información del estándar IEEE 802.3"""
        return convert_8023_to_graphql(modelos.ieee_802_3)
    
    @strawberry.field
    def get_ieee_802_11(self) -> GraphQLIEEE80211:
        """Obtiene toda la información del estándar IEEE 802.11"""
        return convert_80211_to_graphql(modelos.ieee_802_11)
    
    @strawberry.field
    def get_transmission_methods(self) -> GraphQLTransmissionMethods:
        """Obtiene toda la información de Métodos de Transmisión"""
        return convert_transmission_to_graphql(modelos.transmission_methods)
    
    # ===== Consulta completa (todos los temas juntos) =====
    
    @strawberry.field
    def get_all_redes_topics(self) -> GraphQLRedesInvestigacionCompleta:
        """Obtiene toda la información de todos los temas de redes"""
        return GraphQLRedesInvestigacionCompleta(
            network_ports=convert_puertos_to_graphql(modelos.network_ports),
            sockets=convert_sockets_to_graphql(modelos.sockets),
            ieee_802_3=convert_8023_to_graphql(modelos.ieee_802_3),
            ieee_802_11=convert_80211_to_graphql(modelos.ieee_802_11),
            transmission_methods=convert_transmission_to_graphql(modelos.transmission_methods)
        )
    
    # ===== Consultas específicas (filtros) =====
    
    @strawberry.field
    def get_puerto_by_type(self, type_name: str) -> Optional[GraphQLPuertoClasificacion]:
        """Obtiene una clasificación específica de puerto por nombre"""
        for c in modelos.network_ports.classifications:
            if c.get("type", "").lower() == type_name.lower():
                return GraphQLPuertoClasificacion(
                    type=c.get("type", ""),
                    description=c.get("description", ""),
                    range=c.get("range"),
                    examples=c.get("examples", [])
                )
        return None
    
    @strawberry.field
    def get_80211_by_standard(self, standard: str) -> Optional[GraphQLIEEE80211Generacion]:
        """Obtiene una generación específica de Wi-Fi por su estándar"""
        for g in modelos.ieee_802_11.generations:
            if g.get("standard", "").lower() == standard.lower():
                return GraphQLIEEE80211Generacion(
                    standard=g.get("standard", ""),
                    wi_fi_name=g.get("wi_fi_name"),
                    year=str(g.get("year", "")),
                    speed=g.get("speed", ""),
                    frequency=g.get("frequency", ""),
                    features=g.get("features"),
                    status=g.get("status")
                )
        return None
    
    @strawberry.field
    def get_transmission_by_type(self, method_type: str) -> Optional[GraphQLTransmissionMethod]:
        """Obtiene un método de transmisión específico por su tipo"""
        for m in modelos.transmission_methods.methods:
            if m.get("type", "").lower() == method_type.lower():
                return GraphQLTransmissionMethod(
                    type=m.get("type", ""),
                    ratio=m.get("ratio", ""),
                    description=m.get("description", ""),
                    examples=m.get("examples", []),
                    address_example=m.get("address_example", "")
                )
        return None


# ============ FASTAPI APP ============

app = FastAPI(
    title="API de Redes - Puertos, Sockets, IEEE Standards y Métodos de Transmisión",
    description="API GraphQL para consultar información sobre temas fundamentales de redes",
    version="2.0.0"
)

schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")


@app.get("/")
def root():
    return {
        "message": "API de Redes - Puertos, Sockets, IEEE 802.3, IEEE 802.11 y Métodos de Transmisión",
        "graphql_endpoint": "/graphql",
        "available_queries": [
            "get_puertos_red",
            "get_sockets", 
            "get_ieee_802_3",
            "get_ieee_802_11",
            "get_transmission_methods",
            "get_all_redes_topics",
            "get_puerto_by_type",
            "get_80211_by_standard",
            "get_transmission_by_type"
        ]
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "redes-api-v2"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)