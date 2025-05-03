
# 🌻 Sunflower Alert

**Sunflower Alert** é uma ferramenta automatizada para monitorar fazendas no jogo [Sunflower Land](https://sunflower-land.com/), notificando quando determinadas condições são atendidas, como a disponibilidade de recursos ou eventos específicos.

## 🧭 Sobre o Sunflower Land

[Sunflower Land](https://sunflower-land.com/) é um jogo de simulação de fazenda baseado em blockchain, onde os jogadores podem:

- Cultivar e colher diversas plantações.
- Pescar, minerar e coletar recursos.
- Criar animais e cozinhar receitas.
- Participar de eventos sazonais e especiais.
- Trocar e vender itens como NFTs no mercado.

<p align="center">
  <img src="https://github.com/user-attachments/assets/8e7a5a73-834e-4fbf-9b2d-967ca84f0606" alt="farm b4df88b0" width="600"/>
</p>



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
