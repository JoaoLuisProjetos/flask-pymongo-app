# utf-8


def populate_collections(db):

    if db['autores'].count_documents({}) == 0:
        db['autores'].insert_many([
            {'nome': 'Flavio Ribeiro'},
            {'nome': 'João da Silva'},
            {'nome': 'Livia P. Mourão'},
        ])

    if db['noticias'].count_documents({}) == 0:
        flavio = db['autores'].find_one({"nome": 'Flavio Ribeiro'})
        joao = db['autores'].find_one({"nome": 'João da Silva'})
        livia = db['autores'].find_one({"nome": 'Livia P. Mourão'})

        db['noticias'].insert_many([
            {'titulo': 'Júris em série', 'descricao': 'A Comarca de Juazeiro retomou esta semana os julgamentos prese' +
                'nciais no tribunal do júri. E promete descontar o atraso: marcou 12 em 15 dias. No primeiro, terça ' +
                'passada, Israel Ferreira da Cruz, acusado de homicídio, pegou seis anos de prisão. Hoje tem mais.',
                'autor': flavio['_id']},
            {'titulo': 'Arrombador de fóruns', 'descricao': 'O serviço de inteligência da polícia de Juazeiro derrubo' +
                'u o mistério que envolvia os arrombamentos dos fóruns de Ribeira do Pombal, no dia 20 de fevereiro, ' +
                'e de Tucano, no dia seguinte. Um suspeito foi preso. Os motivos não foram divulgados.',
                'autor': flavio['_id']},
            {'titulo': 'Meia-volta', 'descricao': 'Três das seis escolas estaduais de Teixeira de Freitas, no extremo' +
                'sul, reabriram, mas tiveram de fechar por causa da Covid. Nos meios educacionais se diz que, até a ' +
                'situação se normalizar, vai ter muito disso.', 'autor': joao['_id']},
            {'titulo': 'Bahia recebe novo lote com mais de 352 mil doses da vacina Coronavac',
                'descricao': 'Pela manhã, chegou à Bahia mais 362 mil doses do imunizante Pfizer; no total, estado re' +
                    'cebeu mais de meio milhão de doses em apenas um dia', 'autor': joao['_id']},
            {'titulo': 'Ministério da Saúde diz que 75% dos adultos já tomaram a primeira dose no Brasil',
                'descricao': 'O Ministério da Saúde informou nesta sexta-feira (20) que 120 milhões de brasileiros já' +
                    'receberam a primeira dose de vacinas contra a Covid-19 – o número corresponde a 75% da população' +
                    ' adulta no país.', 'autor': livia['_id']},
            {'titulo': 'MP aciona Justiça para que prefeitura garanta presença de acompanhantes em maternidade',
                'descricao': 'O meio do promotor de Justiça Thiago Castro Praxedes, pede ainda que a Justiça determi' +
                    'ne a adaptação das salas de pré-parto, parto e pós-parto para permitir, em todas as fases do par' +
                    'to, a permanência de acompanhante escolhido pela gestante, independente do seu gênero. Pede tamb' +
                    'ém que sejam tomadas as devidas medidas para garantir o direito à privacidade das demais parturi' +
                    'entes.', 'autor': livia['_id']},
        ])
