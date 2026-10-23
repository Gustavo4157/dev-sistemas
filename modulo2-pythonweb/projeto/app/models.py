from pydantic import BaseModel, field_validator, ConfigDict
from typing import Optional
from enum import Enum
# <---------------------->
from datetime import date

# Schema para o status dedicado (PATCH status)
class StatusAtualizacao(BaseModel):
    status: StatusEnum

# Schema do Desafio Extra
class ComentarioEntrada(BaseModel):
    autor: str
    texto: str

class Comentario(BaseModel):
    id: int
    tarefa_id: int
    autor: str
    texto: str
# <---------------------->

# Enums
class StatusEnum(str, Enum):
    pendente     = 'pendente'
    em_andamento = 'em_andamento'
    concluida    = 'concluida'
    cancelada    = 'cancelada'

class PrioridadeEnum(str, Enum):
    baixa   = 'baixa'
    media   = 'media'
    alta    = 'alta'
    critica = 'critica'

# Schema de entrada 
class TarefaEntrada(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={'example': {
            'titulo':      'Implementar autenticacao JWT',
            'descricao':   'Adicionar login com token na API',
            'responsavel': 'Carlos Silva',
            'prioridade':  'alta',
            'prazo':       '2025-12-31',
            'tags':        ['backend', 'seguranca']
        }}
    )
    titulo:      str
    descricao:   Optional[str]       = None
    responsavel: Optional[str]       = None
    prioridade:  PrioridadeEnum       = PrioridadeEnum.media
    status:      StatusEnum           = StatusEnum.pendente
# <---------------------->
    prazo:       Optional[date]       = None
    tags:        list[str]            = []

    @field_validator('tags')
    @classmethod
    def validar_tags(cls, v: list[str]) -> list[str]:
        if v:
            # Converte para minúsculo e remove duplicatas com set()
            tags_unicas = set(tag.lower().strip() for tag in v)
            return list(tags_unicas)
        return []
# <---------------------->

    @field_validator('titulo')
    @classmethod
    def validar_titulo(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 3:
            raise ValueError('O titulo deve ter pelo menos 3 caracteres')
        if len(v) > 120:
            raise ValueError('O titulo deve ter no maximo 120 caracteres')
        return v

    @field_validator('responsavel')
    @classmethod
    def validar_responsavel(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v = v.strip()
            if len(v) < 2:
                raise ValueError('Nome do responsavel deve ter pelo menos 2 caracteres')
            return v.title()
        return v

# Schema de saida
# <---------------------->
class TarefaSaida(BaseModel):
    id:          int
    titulo:      str
    descricao:   Optional[str]  = None
    responsavel: Optional[str]  = None
    prioridade:  PrioridadeEnum
    status:      StatusEnum
    prazo:       Optional[date] = None
    criado_em:   date           = date.today()
    tags:        list[str]      = []
# <---------------------->

# Schema para atualizacao parcial
class TarefaParcial(BaseModel):
    titulo:      Optional[str]            = None
    descricao:   Optional[str]            = None
    responsavel: Optional[str]            = None
    prioridade:  Optional[PrioridadeEnum] = None
    status:      Optional[StatusEnum]     = None
# <---------------------->
    prazo:       Optional[date]           = None
    tags:        Optional[list[str]]      = None

    @field_validator('tags')
    @classmethod
    def validar_tags(cls, v: Optional[list[str]]) -> Optional[list[str]]:
        if v is not None:
            return list(set(tag.lower().strip() for tag in v))
        return v
# <---------------------->

# from pydantic import BaseModel, field_validator, ConfigDict
# from typing import Optional
# from enum import Enum
# from datetime import date

# # Enums
# class StatusEnum(str, Enum):
#     pendente     = 'pendente'
#     em_andamento = 'em_andamento'
#     concluida    = 'concluida'
#     cancelada    = 'cancelada'

# class PrioridadeEnum(str, Enum):
#     baixa   = 'baixa'
#     media   = 'media'
#     alta    = 'alta'
#     critica = 'critica'

# # Schema de entrada 
# class TarefaEntrada(BaseModel):
#     model_config = ConfigDict(
#         json_schema_extra={'example': {
#             'titulo':      'Implementar autenticacao JWT',
#             'descricao':   'Adicionar login com token na API',
#             'responsavel': 'Carlos Silva',
#             'prioridade':  'alta',
#             'prazo':       '2025-12-31'
#         }}
#     )
#     titulo:      str
#     descricao:   Optional[str]       = None
#     responsavel: Optional[str]        = None
#     prioridade:  PrioridadeEnum       = PrioridadeEnum.media
#     status:      StatusEnum           = StatusEnum.pendente
#     prazo:       Optional[date]       = None

#     @field_validator('titulo')
#     @classmethod
#     def validar_titulo(cls, v: str) -> str:
#         v = v.strip()
#         if len(v) < 3:
#             raise ValueError('O titulo deve ter pelo menos 3 caracteres')
#         if len(v) > 120:
#             raise ValueError('O titulo deve ter no maximo 120 caracteres')
#         return v

#     @field_validator('responsavel')
#     @classmethod
#     def validar_responsavel(cls, v: Optional[str]) -> Optional[str]:
#         if v is not None:
#             v = v.strip()
#             if len(v) < 2:
#                 raise ValueError('Nome do responsavel deve ter pelo menos 2 caracteres')
#             return v.title()
#         return v

# # Schema de saida
# class TarefaSaida(BaseModel):
#     id:          int
#     titulo:      str
#     descricao:   Optional[str]  = None
#     responsavel: Optional[str]  = None
#     prioridade:  PrioridadeEnum
#     status:      StatusEnum
#     prazo:       Optional[date] = None

# # Schema para atualizacao parcial
# class TarefaParcial(BaseModel):
#     titulo:      Optional[str]            = None
#     descricao:   Optional[str]            = None
#     responsavel: Optional[str]            = None
#     prioridade:  Optional[PrioridadeEnum] = None
#     status:      Optional[StatusEnum]     = None
#     prazo:       Optional[date]           = None