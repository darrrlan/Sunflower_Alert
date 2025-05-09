
# 🌻 Sunflower Alert
![k4jzfmLxSx-](https://github.com/user-attachments/assets/f4098693-f0f3-4fe3-99a4-5bc26ad338e6)

**Sunflower Alert** é uma ferramenta automatizada para monitorar fazendas no jogo [Sunflower Land](https://sunflower-land.com/), notificando quando determinadas condições são atendidas, como a disponibilidade de recursos ou eventos específicos.

## 🧭 Sobre o Sunflower Land

[Sunflower Land](https://sunflower-land.com/) é um jogo de simulação de fazenda baseado em blockchain, onde os jogadores podem:

- Cultivar e colher diversas plantações.
- Pescar, minerar e coletar recursos.
- Criar animais e cozinhar receitas.
- Participar de eventos sazonais e especiais.
- Trocar e vender itens como NFTs no mercado.



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

1. Configure o arquivo script.py com as informações das fazendas que deseja monitorar. Modifique a URL para a fazenda que deseja acompanhar:

   ```bash
   url = "https://api.sunflower-land.com/visit/{id_fazenda}"
    ```

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

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

---

*Nota: As imagens utilizadas são de propriedade do Sunflower Land e são utilizadas aqui apenas para fins ilustrativos.*
