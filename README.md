# Documentação do Projeto "Sistema de Hotel com Django e Django REST Framework (DRF)"
### Introdução
O "Sistema de Hotel com Django e Django REST Framework" é uma aplicação desenvolvida utilizando Python com o framework Django, HTML e CSS, além de uma API utilizando o DRF. O sistema é simples e tem como objetivo gerenciar reservas, check-ins e check-outs de um hotel. Cada componente do projeto é organizado em apps individuais, focados em funcionalidades específicas.

## Estrutura do Projeto com respostas para o front-end
### Apps do Projeto
1. Usuários:
+ Responsável pela autenticação e controle de usuários do sistema.
2. Quartos:
+ Gerencia informações sobre os quartos disponíveis no hotel.
3. Portaria:
+ Lida com os dados dos membros da portaria responsáveis pelo atendimento.
4.Hóspedes:
+ Gerencia informações sobre os hóspedes, reservas, check-ins e check-outs.
## Funcionalidades Gerais
### Dashboard Principal (Index):
A página principal exibe uma dashboard com informações cruciais sobre o hotel, incluindo as 5 reservas próximas, check-ins e check-outs do dia, ocupação atual do hotel, número de hóspedes do mês e estatísticas gerais.

### Realizar Reserva:
Essa funcionalidade permite que a equipe da portaria realize uma nova reserva para um hóspede. É utilizado o formulário ReservaForm para coletar informações relevantes.

### Check-In e Check-Out:
A equipe da portaria pode realizar o check-in e o check-out de hóspedes diretamente pela interface. Dependendo do status do hóspede, são exibidos botões correspondentes para executar essas ações.

## Apps Individuais
### Usuários
Este app é responsável por lidar com a autenticação e controle de usuários. Ele utiliza o modelo Usuario que estende o modelo padrão do Django, permitindo a criação de usuários com diferentes permissões. Também é responsável pela exibição dos dados da dashboard.

### Quartos
Gerencia informações sobre os quartos disponíveis no hotel. Cada quarto possui um número, tipo (simples, padrão ou luxo), uma imagem e uma descrição.

### Portaria
Lida com os dados dos membros da portaria (atendentes), incluindo informações como nome completo, CPF, telefone e data de nascimento.

### Hóspedes
Responsável por gerenciar informações sobre os hóspedes, incluindo reservas, check-ins e check-outs. Os modelos principais são Hospede e Reserva. O primeiro representa um hóspede, e o segundo representa uma reserva feita por esse hóspede.

## Estrutura da API do projeto
As views para resposta em JSON estão todas dentro do APP de hóspedes, implementado dessa forma para facilitar a manutenção.

Em termos gerais, as views se "clonam" em funcionalidades, porém na API as respostas são em JSON. A view responsável por realizar uma reserva e criar um hóspede no projeto voltado ao front-end é uma view apenas, porém dentro da API foi dividida em duas views: uma para criar o hóspede e outra para realizar a reserva desse hóspede.

## Testes
O projeto conta com uma variedade de testes automatizados, utilizando o coverage para checar a cobertura e o pytest como script para executá-los.

O projeto atingiu 100% de cobertura dos testes, incluindo testes unitários e de integração.

Um exemplo de teste seria o para realização de check-in do hospede, como demonstrado abaixo (realização de check-in utilizando a API):
    
    def test_check_in_api_view_will_return_200_if_action_is_check_in(self):
        # pegando um usuario
        auth_data = self.get_auth_data()
        # pegando seu acesso com jwt token
        jwt_access = auth_data.get('jwt_access_token')

        api_url_hospede = reverse('hospedes:criar_hospede_api')
        self.make_quarto()
        # criando os dados para o hospede em JSON
        data_hospede = {
            "nome_completo": "Hospede 1 Test",
            "telefone": "35991445522",
            "cpf": "11122222456",
            "email": "seuemail@email.com",
            "horario_checkin": "2024-04-25",
            "horario_checkout": "2024-05-28",
            "registrado_por": "1"
        }

        response = self.client.post(
            api_url_hospede,
            data=data_hospede,
            HTTP_AUTHORIZATION=f'Bearer {jwt_access}'   # passando o acesso do
        )  # usuario para a autorizaçao

        # checando se foi recebido um code 201
        # (mostrando que usuario esta logado e criou um hospede com sucesso)
        self.assertEqual(response.status_code, 201)
        # verificando se a msg de sucesso esta contida
        self.assertIn(
            'Reserva do hóspede registrada com sucesso!',
            [msg.message for msg in messages.get_messages(response.wsgi_request)])  # noqa: E501

        # com hospede criado agora é simular a criaçao de uma reserva
        api_url_reserva = reverse('hospedes:realizar_reserva_api')
        data_reserva = {
            "forma_pagamento": "TED",
            "status_reserva": "CONFIRMADO",
            "registrado_por": "1",
            "horario_checkin": "2024-04-25",
            "horario_checkout": "2024-05-28",
            "quartos": ["1"]
        }
        response_reserva = self.client.post(
            api_url_reserva,
            data=data_reserva,
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {jwt_access}'   # passando o acesso do
        )  # usuario para a autorizaçao
        # checando se foi recebido um code 201
        # (mostrando que usuario esta logado e criou uma reserva para o hospede)  # noqa: E501
        self.assertEqual(response_reserva.status_code, 201)
        # checando se o status da reserva esta como "CONFIRMADO"
        self.assertEqual(
            response_reserva.data["status_reserva"],
            "CONFIRMADO"
        )

        hospede = Hospede.objects.all().first()
        api_url = reverse(
            'hospedes:check_in_api',
            kwargs={'id': hospede.id}
        )
        # Agora passar o action correto para realizar CHECK_IN
        data_checkin = {
            "id": 1,
            "nome_completo": "TEST",
            "telefone": "35991445522",
            "cpf": "11122222456",
            "email": "seuemail@email.com",
            "status": "AGUARDANDO_CHECKIN",
            "horario_checkin": "2024-04-25T00:00:00-03:00",
            "registrado_por": 1,
            "action": "check_in"
        }

        response = self.client.post(
            api_url,
            data=data_checkin,
            HTTP_AUTHORIZATION=f'Bearer {jwt_access}'   # passando o acesso do
        )  # usuario para a autorizaçao
        # checando se a msg de sucesso esta na resposta e se temos
        # status code 200
        self.assertEqual(
            response.data['message'],
            'Check-In do visitante realizado com sucesso'
        )
        self.assertEqual(response.status_code, 200)

Basicamente, trata-se de um teste que percorre todo o código da API. Ele começa criando um usuário, acessa o sistema utilizando o token JWT, em seguida, cria um hóspede e realiza uma reserva para ele. Após isso, executa o check-in, passando o parâmetro "action" como check-in para dentro da view.

A estrutura dos testes está bem organizada. Eles estão agrupados em pacotes nomeados como "tests", havendo um pacote desse tipo em cada aplicativo da aplicação. Além disso, cada pacote é dividido em arquivos que testam apenas uma funcionalidade específica, seja ela uma view, um modelo ou uma URL.


## Considerações Finais
O sistema oferece uma interface simples e eficiente para as atividades comuns de um hotel, permitindo que a equipe da portaria realize operações essenciais com facilidade. Ainda serão adicionadas mais funcionalidades, como a exibição dos quartos em um link separado (que não precisará de login, diferente do resto da aplicação), e possivelmente algumas melhorias.

Contribuições são sempre bem-vindas! Sinta-se à vontade para abrir um pull request ou relatar problemas abrindo uma issue.

Autor: Flauziino - Desenvolvedor






