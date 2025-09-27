from utils.request_queue import request_queue

def get_score(id_client, cpf):
    """
    Função principal para obter score do CPF
    - id_client: Client ID fornecido pelo usuário
    - cpf: CPF a ser consultado
    Retorna: resultado da consulta ou erro
    """
    return request_queue.add_request(id_client, cpf)