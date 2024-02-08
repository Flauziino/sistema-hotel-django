# Documentação do Projeto "Sistema Simples de Hotel"

## Introdução
O "Sistema Simples de Hotel" é uma aplicação desenvolvida utilizando Python com o framework Django, HTML e CSS. O sistema tem como objetivo gerenciar reservas, check-ins e check-outs de um hotel. Cada componente do projeto é organizado em apps individuais, focados em funcionalidades específicas.

## Estrutura do Projeto

### Apps do Projeto
1. Usuarios: 
    + Responsável pela autenticação e controle de usuários do sistema.
2. Quartos: 
    + Gerencia informações sobre os quartos disponíveis no hotel.
3. Portaria:
    + Lida com os dados dos membros da portaria responsáveis pelo atendimento.
5. Hospedes: 
    + Gerencia informações sobre os hóspedes, reservas, check-ins e check-outs.

## Funcionalidades Gerais

### Dashboard Principal (Index):
A página principal exibe uma dashboard com informações cruciais sobre o hotel, incluindo as 5 reservas próximas, check-ins e check-outs do dia, ocupação atual do hotel, número de hóspedes do mês e estatísticas gerais.

### Realizar Reserva:
A funcionalidade permite que a equipe de portaria realize uma nova reserva para um hóspede. É utilizado o formulário ReservaForm para coletar informações relevantes.

### Check-In e Check-Out:
A equipe de portaria pode realizar o check-in e o check-out de hóspedes diretamente pela interface. Dependendo do status do hóspede, são exibidos botões correspondentes para executar essas ações.

## Apps Individuais
### Usuarios
Este app é responsável por lidar com a autenticação e controle de usuários. Ele utiliza o modelo Usuario que estende o modelo padrão do Django, permitindo a criação de usuários com diferentes permissões.
Ele está responsável também pela exibição dos dados da dashboard.

### Quartos
Gerencia informações sobre os quartos disponíveis no hotel. Cada quarto possui um número, tipo (simples, padrão ou luxo), uma imagem e uma descrição.

### Portaria
Lida com os dados dos membros da portaria (atendentes), incluindo informações como nome completo, CPF, telefone e data de nascimento.

### Hospedes
Responsável por gerenciar informações sobre os hóspedes, incluindo reservas, check-ins e check-outs. Os modelos principais são Hospede e Reserva. O primeiro representa um hóspede, e o segundo representa uma reserva feita por esse hóspede.

## Considerações Finais
O sistema fornece uma interface simples e eficiente para as atividades comuns de um hotel, permitindo que a equipe da portaria realize operações essenciais com facilidade. Ainda sera adicionado mais funcionalidades como a exibição dos quartos em um link separado (que nao ira precisar de login, diferente do resto da aplicação) e possivelmente algumas melhorias.

Contribuições são sempre bem-vindas! Sinta-se à vontade para abrir um pull request ou relatar problemas abrindo uma issue.

Autor Flauziino - Desenvolvedor
