import uvicorn
import os
import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from typing import List, Optional
from model.Protocolos_de_Red import ProtocoloRedCompleto, ProtocoloRed_Type, ProtocoloRed_Function, NetworkProtocols
from model.OSI import OsiModelCompleto, OsiLayer, TCPIPComparison
from model.Protocolos_de_Red import model_completo as protocoloRed
from model.OSI import modelo_osi


@strawberry.type
class GraphQLProtocoloRed_Type:
    category: str
    description: str
    examples: List[str]

@strawberry.type
class GraphQLProtocoloRed_Function:
    name: str
    detail: str

@strawberry.type
class GraphQLNetworkProtocols:
    title: str
    definition: str
    types: List[GraphQLProtocoloRed_Type]
    functions: List[GraphQLProtocoloRed_Function]

@strawberry.type
class GraphQLProtocoloRedCompleto:
    network_protocols: GraphQLNetworkProtocols

@strawberry.type
class GraphQLOsiLayer:
    level: int
    name: str
    function: str
    pdu: str
    examples: List[str]

@strawberry.type
class GraphQLTCPIPComparison:
    note: str
    key_difference: str

@strawberry.type
class GraphQLOsiModel:
    title: str
    definition: str
    general_analogy: str
    layers: List[GraphQLOsiLayer]
    tcp_ip_comparison: GraphQLTCPIPComparison

@strawberry.type
class GraphQLOsiModelCompleto:
    osi_model: GraphQLOsiModel


def convert_protocolo_to_graphql(protocolo_data: ProtocoloRedCompleto) -> GraphQLProtocoloRedCompleto:
    """Convierte el modelo Pydantic a tipo GraphQL"""
    network_protocols = protocolo_data.network_protocols
    
    types = [
        GraphQLProtocoloRed_Type(
            category=t.category,
            description=t.description,
            examples=t.examples
        )
        for t in network_protocols.types
    ]
    
    functions = [
        GraphQLProtocoloRed_Function(
            name=f.name,
            detail=f.detail
        )
        for f in network_protocols.functions
    ]
    
    return GraphQLProtocoloRedCompleto(
        network_protocols=GraphQLNetworkProtocols(
            title=network_protocols.title,
            definition=network_protocols.definition,
            types=types,
            functions=functions
        )
    )

def convert_osi_to_graphql(osi_data: OsiModelCompleto) -> GraphQLOsiModelCompleto:
    """Convierte el modelo OSI Pydantic a tipo GraphQL"""
    osi_model = osi_data.osi_model
    
    layers = [
        GraphQLOsiLayer(
            level=l.level,
            name=l.name,
            function=l.function,
            pdu=l.pdu,
            examples=l.examples
        )
        for l in osi_model.layers
    ]
    
    return GraphQLOsiModelCompleto(
        osi_model=GraphQLOsiModel(
            title=osi_model.title,
            definition=osi_model.definition,
            general_analogy=osi_model.general_analogy,
            layers=layers,
            tcp_ip_comparison=GraphQLTCPIPComparison(
                note=osi_model.tcp_ip_comparison.note,
                key_difference=osi_model.tcp_ip_comparison.key_difference
            )
        )
    )


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello, World!"
    
    
    @strawberry.field
    def get_protocolos_red(self) -> GraphQLProtocoloRedCompleto:
        """Obtiene toda la información de Protocolos de Red"""
        return convert_protocolo_to_graphql(protocoloRed)
    
    @strawberry.field
    def get_protocolo_title(self) -> str:
        """Obtiene solo el título de Protocolos de Red"""
        return protocoloRed.network_protocols.title
    
    @strawberry.field
    def get_protocolo_types(self) -> List[GraphQLProtocoloRed_Type]:
        """Obtiene todos los tipos de protocolos"""
        return [
            GraphQLProtocoloRed_Type(
                category=t.category,
                description=t.description,
                examples=t.examples
            )
            for t in protocoloRed.network_protocols.types
        ]
    
    @strawberry.field
    def get_protocolo_functions(self) -> List[GraphQLProtocoloRed_Function]:
        """Obtiene todas las funciones de protocolos"""
        return [
            GraphQLProtocoloRed_Function(
                name=f.name,
                detail=f.detail
            )
            for f in protocoloRed.network_protocols.functions
        ]
    
    @strawberry.field
    def get_protocolo_by_category(self, category: str) -> Optional[GraphQLProtocoloRed_Type]:
        """Obtiene un tipo específico de protocolo por categoría"""
        for tipo in protocoloRed.network_protocols.types:
            if tipo.category.lower() == category.lower():
                return GraphQLProtocoloRed_Type(
                    category=tipo.category,
                    description=tipo.description,
                    examples=tipo.examples
                )
        return None
    
    
    @strawberry.field
    def get_osi_model(self) -> GraphQLOsiModelCompleto:
        """Obtiene toda la información del Modelo OSI"""
        return convert_osi_to_graphql(modelo_osi)
    
    @strawberry.field
    def get_osi_title(self) -> str:
        """Obtiene solo el título del Modelo OSI"""
        return modelo_osi.osi_model.title
    
    @strawberry.field
    def get_osi_layers(self) -> List[GraphQLOsiLayer]:
        """Obtiene todas las capas del Modelo OSI"""
        return [
            GraphQLOsiLayer(
                level=l.level,
                name=l.name,
                function=l.function,
                pdu=l.pdu,
                examples=l.examples
            )
            for l in modelo_osi.osi_model.layers
        ]
    
    @strawberry.field
    def get_osi_layer_by_level(self, level: int) -> Optional[GraphQLOsiLayer]:
        """Obtiene una capa específica del Modelo OSI por su nivel"""
        for layer in modelo_osi.osi_model.layers:
            if layer.level == level:
                return GraphQLOsiLayer(
                    level=layer.level,
                    name=layer.name,
                    function=layer.function,
                    pdu=layer.pdu,
                    examples=layer.examples
                )
        return None
    
    @strawberry.field
    def get_osi_upper_layers(self) -> List[GraphQLOsiLayer]:
        """Obtiene las capas superiores (5, 6, 7)"""
        return [
            GraphQLOsiLayer(
                level=l.level,
                name=l.name,
                function=l.function,
                pdu=l.pdu,
                examples=l.examples
            )
            for l in modelo_osi.osi_model.layers
            if l.level >= 5
        ]
    
    @strawberry.field
    def get_osi_lower_layers(self) -> List[GraphQLOsiLayer]:
        """Obtiene las capas inferiores (1, 2, 3, 4)"""
        return [
            GraphQLOsiLayer(
                level=l.level,
                name=l.name,
                function=l.function,
                pdu=l.pdu,
                examples=l.examples
            )
            for l in modelo_osi.osi_model.layers
            if l.level <= 4
        ]
    
    @strawberry.field
    def get_osi_comparison(self) -> GraphQLTCPIPComparison:
        """Obtiene la comparación con TCP/IP"""
        return GraphQLTCPIPComparison(
            note=modelo_osi.osi_model.tcp_ip_comparison.note,
            key_difference=modelo_osi.osi_model.tcp_ip_comparison.key_difference
        )
    
    @strawberry.field
    def search_osi_by_example(self, search_term: str) -> List[GraphQLOsiLayer]:
        """Busca capas que contengan un ejemplo específico"""
        result_layers = []
        for layer in modelo_osi.osi_model.layers:
            for example in layer.examples:
                if search_term.lower() in example.lower():
                    result_layers.append(
                        GraphQLOsiLayer(
                            level=layer.level,
                            name=layer.name,
                            function=layer.function,
                            pdu=layer.pdu,
                            examples=layer.examples
                        )
                    )
                    break
        return result_layers


app = FastAPI(
    title="API de Protocolos de Red y Modelo OSI",
    description="API GraphQL para consultar información sobre Protocolos de Red y el Modelo OSI",
    version="1.0.0"
)

schema = strawberry.Schema(query=Query)

graphql_app = GraphQLRouter(schema)

app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
def root():
    return {
        "message": "API de Protocolos de Red y Modelo OSI",
        "graphql_endpoint": "/graphql",
        "docs": "Usa GraphQL para consultar los datos"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "redes-api"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))