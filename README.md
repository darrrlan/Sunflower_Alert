
# 🌻 Sunflower Alert

**Sunflower Alert** é uma ferramenta automatizada para monitorar fazendas no jogo [Sunflower Land](https://sunflower-land.com/), notificando quando determinadas condições são atendidas, como a disponibilidade de recursos ou eventos específicos.

## 🧭 Sobre o Sunflower Land

[Sunflower Land](https://sunflower-land.com/) é um jogo de simulação de fazenda baseado em blockchain, onde os jogadores podem:

- Cultivar e colher diversas plantações.
- Pescar, minerar e coletar recursos.
- Criar animais e cozinhar receitas.
- Participar de eventos sazonais e especiais.
- Trocar e vender itens como NFTs no mercado.

![Imagem do jogo](https://www.google.com/url?sa=i&url=https%3A%2F%2Fsunflower-land.com%2F&psig=AOvVaw03_vqT3xDhn3pQdOxiXJdg&ust=1746398928380000&source=images&cd=vfe&opi=89978449&ved=0CBMQjRxqFwoTCKiHnJKxiI0DFQAAAAAdAAAAABAQ)

## 🚀 Funcionalidades do Sunflower Alert

- Monitoramento contínuo de fazendas específicas.
- Notificações automáticas quando condições predefinidas são atendidas.
- Registro de fazendas já notificadas para evitar alertas duplicados.

## 🛠️ Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu-usuario/Sunflower_Alert.git
   cd Sunflower_Alert
   ```

2. Instale as dependências necessárias:

   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Uso

1. Configure o arquivo `dados_fazenda.json` com as informações das fazendas que deseja monitorar.

2. Execute o script principal:

   ```bash
   python script.py
   ```

   O script verificará periodicamente as condições das fazendas e enviará notificações conforme configurado.

## 📁 Estrutura do Projeto

```
Sunflower_Alert/
├── dados_fazenda.json       # Dados das fazendas a serem monitoradas
├── notificadas.json         # Registro de fazendas já notificadas
├── script.py                # Script principal de monitoramento
├── README.md                # Documentação do projeto
└── requirements.txt         # Dependências do projeto
```

## 📸 Imagens do Jogo

![Fazenda no jogo](https://sunflower-land.com/images/farm.png)

![Interface do jogo](https://sunflower-land.com/images/interface.png)

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

---

*Nota: As imagens utilizadas são de propriedade do Sunflower Land e são utilizadas aqui apenas para fins ilustrativos.*
