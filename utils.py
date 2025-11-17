"""
Funções utilitárias: normalização e validações simples.
"""

import re
from datetime import datetime
from validate_docbr import CNPJ, CPF


def normaliza_cnpj(cnpj:str) -> str:
    """Remove tudo que não for dígito. Retorna string vazia se None."""
    
    num_cnpj = CNPJ()
    
    if not num_cnpj:
        return ''
    else:
        if num_cnpj.validate(cnpj):
            return re.sub(r'\D', '', cnpj)
        else:
            print('CNPJ Inválido ❌')
    

if __name__ == '__main__':
    normaliza_cnpj('32677201000114')

