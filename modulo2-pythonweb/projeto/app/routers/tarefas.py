from fastapi import APIRouter, HTTPException, Path, Query, Response
from typing import Annotated, Optional
from app.models import TarefaEntrada, TarefaSaida, TarefaParcial, StatusAtualizacao, Comentario, ComentarioEntrada
from app.models import StatusEnum, PrioridadeEnum

router = APIRouter(prefix='/tarefas', tags=['Tarefas'])

# Banco simulado
banco: list[TarefaSaida] = [
    TarefaSaida(id=1, titulo='Configurar ambiente Python', responsavel='Carlos', prioridade='alta', status='concluida', tags=['python', 'env']),
    TarefaSaida(id=2, titulo='Criar modelos Pydantic', responsavel='Ana',    prioridade='alta', status='concluida', tags=['pydantic']),
    TarefaSaida(id=3, titulo='Implementar CRUD completo', responsavel='Carlos', prioridade='critica', status='em_andamento', tags=['fastapi', 'crud']),
    TarefaSaida(id=4, titulo='Conectar ao banco MySQL', responsavel='Bruno',  prioridade='alta', status='pendente', tags=['mysql', 'database']),
    TarefaSaida(id=5, titulo='Escrever documentacao', responsavel='Ana',    prioridade='baixa', status='pendente', tags=['docs']),
]
proximo_id = 6

# Banco simulado para comentarios (Desafio Extra)
banco_comentarios: list[Comentario] = []
proximo_id_comentario = 1

# <---------------------->
# GET /tarefas/estatisticas -- ANTES de /{tarefa_id}
@router.get('/estatisticas', summary='Estatisticas gerais das tarefas')
def estatisticas():
    por_status = {s.value: sum(1 for t in banco if t.status == s) for s in StatusEnum}
    por_prioridade = {p.value: sum(1 for t in banco if t.prioridade == p) for p in PrioridadeEnum}
    return {
        'total': len(banco),
        'por_status': por_status,
        'por_prioridade':por_prioridade,
    }

# GET /tarefas/prioridade/critica -- ANTES de /{tarefa_id}
@router.get('/prioridade/critica', response_model=list[TarefaSaida], summary='Lista tarefas criticas pendentes ou em andamento')
def listar_criticas():
    return [
        t for t in banco 
        if t.prioridade == PrioridadeEnum.critica 
        and t.status not in (StatusEnum.concluida, StatusEnum.cancelada)
    ]

# GET /tarefas/responsavel/{nome} -- ANTES de /{tarefa_id}
@router.get('/responsavel/{nome}', response_model=list[TarefaSaida], summary='Busca tarefas por um responsável específico')
def buscar_por_responsavel(nome: Annotated[str, Path(min_length=2)]):
    resultado = [t for t in banco if t.responsavel and nome.lower() in t.responsavel.lower()]
    if not resultado:
        raise HTTPException(status_code=404, detail='Nenhuma tarefa encontrada para este responsavel')
    return resultado
# <---------------------->

# GET /tarefas
@router.get('/', response_model=list[TarefaSaida], summary='Lista tarefas com filtros')
def listar(
    status: Annotated[Optional[StatusEnum], Query(description='Filtrar por status')] = None,
    prioridade: Annotated[Optional[PrioridadeEnum], Query(description='Filtrar por prioridade')] = None,
    responsavel: Annotated[Optional[str], Query(description='Filtrar por responsavel')] = None,
    limite: Annotated[int, Query(ge=1, le=100)] = 20,
    pagina: Annotated[int, Query(ge=1)] = 1,
):
    resultado = banco
    if status: resultado = [t for t in resultado if t.status == status]
    if prioridade: resultado = [t for t in resultado if t.prioridade == prioridade]
    if responsavel: resultado = [t for t in resultado if responsavel.lower() in (t.responsavel or '').lower()]
    inicio = (pagina - 1) * limite
    return resultado[inicio : inicio + limite]

# GET /tarefas/{tarefa_id}
@router.get('/{tarefa_id}', response_model=TarefaSaida, summary='Busca uma tarefa pelo ID')
def buscar(tarefa_id: Annotated[int, Path(ge=1)]):
    for t in banco:
        if t.id == tarefa_id: return t
    raise HTTPException(status_code=404, detail='Tarefa nao encontrada')

# POST /tarefas
@router.post('/', response_model=TarefaSaida, status_code=201, summary='Cria uma nova tarefa')
def criar(dados: TarefaEntrada):
    """
    Cria uma nova tarefa no sistema.
    - **titulo**: obrigatorio, 3 a 120 caracteres
    - **prioridade**: padrao 'media' se nao informada
    - **status**: padrao 'pendente' para novas tarefas
    - **prazo**: formato ISO 8601 -- YYYY-MM-DD
    """
    global proximo_id
    nova = TarefaSaida(id=proximo_id, **dados.model_dump())
    banco.append(nova)
    proximo_id += 1
    return nova

# PUT /tarefas/{tarefa_id}
@router.put('/{tarefa_id}', response_model=TarefaSaida, summary='Substitui uma tarefa inteira')
def atualizar(tarefa_id: Annotated[int, Path(ge=1)], dados: TarefaEntrada):
    for i, t in enumerate(banco):
        if t.id == tarefa_id:
            banco[i] = TarefaSaida(id=tarefa_id, **dados.model_dump())
            return banco[i]
    raise HTTPException(status_code=404, detail='Tarefa nao encontrada')

# <---------------------->
# PATCH /tarefas/{tarefa_id}/status
@router.patch('/{tarefa_id}/status', response_model=TarefaSaida, summary='Muda apenas o status de uma tarefa')
def atualizar_status(tarefa_id: Annotated[int, Path(ge=1)], dados: StatusAtualizacao):
    for i, t in enumerate(banco):
        if t.id == tarefa_id:
            if t.status == StatusEnum.cancelada:
                raise HTTPException(status_code=400, detail='Nao e possivel alterar o status de uma tarefa cancelada')
            atual = t.model_dump()
            atual['status'] = dados.status
            banco[i] = TarefaSaida(**atual)
            return banco[i]
    raise HTTPException(status_code=404, detail='Tarefa nao encontrada')
# <---------------------->

# PATCH /tarefas/{tarefa_id}
@router.patch('/{tarefa_id}', response_model=TarefaSaida, summary='Atualiza campos especificos')
def atualizar_parcial(tarefa_id: Annotated[int, Path(ge=1)], dados: TarefaParcial):
    for i, t in enumerate(banco):
        if t.id == tarefa_id:
            atual = t.model_dump()
            atual.update(dados.model_dump(exclude_none=True))
            banco[i] = TarefaSaida(**atual)
            return banco[i]
    raise HTTPException(status_code=404, detail='Tarefa nao encontrada')

# DELETE /tarefas/{tarefa_id}
@router.delete('/{tarefa_id}', status_code=204, summary='Remove uma tarefa')
def deletar(tarefa_id: Annotated[int, Path(ge=1)]):
    for i, t in enumerate(banco):
        if t.id == tarefa_id:
            banco.pop(i)
            return Response(status_code=204)
    raise HTTPException(status_code=404, detail='Tarefa nao encontrada')

# <---------------------->
# --- DESAFIO EXTRA: COMENTÁRIOS ---

# POST /tarefas/{tarefa_id}/comentarios
@router.post('/{tarefa_id}/comentarios', response_model=Comentario, status_code=201, summary='Adiciona um comentário à tarefa')
def criar_comentario(tarefa_id: Annotated[int, Path(ge=1)], dados: ComentarioEntrada):
    global proximo_id_comentario
    tarefa_existe = any(t.id == tarefa_id for t in banco)
    if not tarefa_existe:
        raise HTTPException(status_code=404, detail='Tarefa nao encontrada')
    
    novo_comentario = Comentario(
        id=proximo_id_comentario,
        tarefa_id=tarefa_id,
        autor=dados.autor,
        texto=dados.texto
    )
    banco_comentarios.append(novo_comentario)
    proximo_id_comentario += 1
    return novo_comentario

# GET /tarefas/{tarefa_id}/comentarios
@router.get('/{tarefa_id}/comentarios', response_model=list[Comentario], summary='Listar comentários de uma tarefa')
def listar_comentarios(tarefa_id: Annotated[int, Path(ge=1)]):
    tarefa_existe = any(t.id == tarefa_id for t in banco)
    if not tarefa_existe:
        raise HTTPException(status_code=404, detail='Tarefa nao encontrada')
    return [c for c in banco_comentarios if c.tarefa_id == tarefa_id]
# <---------------------->

# from fastapi import APIRouter, HTTPException, Path, Query, Response
# from typing import Annotated, Optional
# from app.models import TarefaEntrada, TarefaSaida, TarefaParcial
# from app.models import StatusEnum, PrioridadeEnum

# router = APIRouter(prefix='/tarefas', tags=['Tarefas'])

# # Banco simulado
# banco: list[TarefaSaida] = [
#     TarefaSaida(id=1, titulo='Configurar ambiente Python', responsavel='Carlos', prioridade='alta', status='concluida'),
#     TarefaSaida(id=2, titulo='Criar modelos Pydantic', responsavel='Ana',    prioridade='alta', status='concluida'),
#     TarefaSaida(id=3, titulo='Implementar CRUD completo', responsavel='Carlos', prioridade='critica', status='em_andamento'),
#     TarefaSaida(id=4, titulo='Conectar ao banco MySQL', responsavel='Bruno',  prioridade='alta', status='pendente'),
#     TarefaSaida(id=5, titulo='Escrever documentacao', responsavel='Ana',    prioridade='baixa', status='pendente'),
# ]
# proximo_id = 6

# # GET /tarefas/estatisticas -- ANTES de /{tarefa_id}
# @router.get('/estatisticas', summary='Estatisticas gerais das tarefas')
# def estatisticas():
#     por_status = {s.value: sum(1 for t in banco if t.status == s) for s in StatusEnum}
#     por_prioridade = {p.value: sum(1 for t in banco if t.prioridade == p) for p in PrioridadeEnum}
#     return {
#         'total': len(banco),
#         'por_status': por_status,
#         'por_prioridade':por_prioridade,
#     }

# # GET /tarefas
# @router.get('/', response_model=list[TarefaSaida], summary='Lista tarefas com filtros')
# def listar(
#     status: Annotated[Optional[StatusEnum], Query(description='Filtrar por status')] = None,
#     prioridade: Annotated[Optional[PrioridadeEnum], Query(description='Filtrar por prioridade')] = None,
#     responsavel: Annotated[Optional[str], Query(description='Filtrar por responsavel')] = None,
#     limite: Annotated[int, Query(ge=1, le=100)] = 20,
#     pagina: Annotated[int, Query(ge=1)] = 1,
# ):
#     resultado = banco
#     if status: resultado = [t for t in resultado if t.status == status]
#     if prioridade: resultado = [t for t in resultado if t.prioridade == prioridade]
#     if responsavel: resultado = [t for t in resultado if responsavel.lower() in (t.responsavel or '').lower()]
#     inicio = (pagina - 1) * limite
#     return resultado[inicio : inicio + limite]

# # GET /tarefas/{tarefa_id}
# @router.get('/{tarefa_id}', response_model=TarefaSaida, summary='Busca uma tarefa pelo ID')
# def buscar(tarefa_id: Annotated[int, Path(ge=1)]):
#     for t in banco:
#         if t.id == tarefa_id: return t
#     raise HTTPException(status_code=404, detail='Tarefa nao encontrada')

# # POST /tarefas
# @router.post('/', response_model=TarefaSaida, status_code=201, summary='Cria uma nova tarefa')
# def criar(dados: TarefaEntrada):
#     """
#     Cria uma nova tarefa no sistema.
#     - **titulo**: obrigatorio, 3 a 120 caracteres
#     - **prioridade**: padrao 'media' se nao informada
#     - **status**: padrao 'pendente' para novas tarefas
#     - **prazo**: formato ISO 8601 -- YYYY-MM-DD
#     """
#     global proximo_id
#     nova = TarefaSaida(id=proximo_id, **dados.model_dump())
#     banco.append(nova)
#     proximo_id += 1
#     return nova

# # PUT /tarefas/{tarefa_id}
# @router.put('/{tarefa_id}', response_model=TarefaSaida, summary='Substitui uma tarefa inteira')
# def atualizar(tarefa_id: Annotated[int, Path(ge=1)], dados: TarefaEntrada):
#     for i, t in enumerate(banco):
#         if t.id == tarefa_id:
#             banco[i] = TarefaSaida(id=tarefa_id, **dados.model_dump())
#             return banco[i]
#     raise HTTPException(status_code=404, detail='Tarefa nao encontrada')

# # PATCH /tarefas/{tarefa_id}
# @router.patch('/{tarefa_id}', response_model=TarefaSaida, summary='Atualiza campos especificos')
# def atualizar_parcial(tarefa_id: Annotated[int, Path(ge=1)], dados: TarefaParcial):
#     for i, t in enumerate(banco):
#         if t.id == tarefa_id:
#             atual = t.model_dump()
#             atual.update(dados.model_dump(exclude_none=True))
#             banco[i] = TarefaSaida(**atual)
#             return banco[i]
#     raise HTTPException(status_code=404, detail='Tarefa nao encontrada')

# # DELETE /tarefas/{tarefa_id}
# @router.delete('/{tarefa_id}', status_code=204, summary='Remove uma tarefa')
# def deletar(tarefa_id: Annotated[int, Path(ge=1)]):
#     for i, t in enumerate(banco):
#         if t.id == tarefa_id:
#             banco.pop(i)
#             return Response(status_code=204)
#     raise HTTPException(status_code=404, detail='Tarefa nao encontrada')