# 🏎️ F1 Telemetry Viewer BLACKGSGO

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![FastF1 3.5+](https://img.shields.io/badge/FastF1-3.5%2B-orange.svg)](https://pypi.org/project/fastf1/)
[![Matplotlib 3.3+](https://img.shields.io/badge/Matplotlib-3.3%2B-green.svg)](https://pypi.org/project/matplotlib/)
[![CustomTkinter](https://img.shields.io/badge/CustomTkinter-Library-blue.svg)](https://github.com/TomSchimansky/CustomTkinter)
[![Status: Experimental](https://img.shields.io/badge/Status-Experimental-orange.svg)](https://github.com/seuusuario/f1-telemetry)

Bem-vindo ao **F1 Telemetry Viewer**, uma aplicação Python avançada para análise de dados de telemetria de Fórmula 1. Este projeto foi projetado para entusiastas e engenheiros que desejam explorar o desempenho dos pilotos e entender os detalhes técnicos das sessões de corrida. 🌍✨

---

## 🌟 Destaques do Projeto

- **📈 Análise Avançada**: Compare voltas, visualize dados de telemetria e explore métricas detalhadas como velocidade, aceleração, frenagem e mais.
- **🖼️ Exportação de Gráficos**: Salve gráficos como imagens PNG para compartilhar ou documentar análises.
- **⚡ Performance Otimizada**: Cache integrado para carregamento rápido de dados.
- **🌐 Suporte Internacional**: Dados de pilotos de várias nacionalidades, incluindo 🇧🇷, 🇬🇧, 🇩🇪, 🇮🇹, 🇪🇸 e 🇫🇷.
- **🔧 Personalização**: Configure cores de equipes, pneus e outros elementos visuais.

---

## 🛠️ Tecnologias Utilizadas

Este projeto utiliza as seguintes tecnologias e bibliotecas:

- **Linguagem**: Python 3.10+
- **Bibliotecas Principais**:
  - [`fastf1`](https://github.com/theOehrly/Fast-F1) para acesso a dados de telemetria.
  - [`matplotlib`](https://matplotlib.org/) para visualização de dados.
  - [`customtkinter`](https://github.com/TomSchimansky/CustomTkinter) para interface gráfica.
  - [`numpy`](https://numpy.org/) e [`pandas`](https://pandas.pydata.org/) para manipulação de dados.
  - [`mplcursors`](https://mplcursors.readthedocs.io/) para interatividade nos gráficos.

---

## 📂 Estrutura do Projeto

A organização do projeto é a seguinte:

```plaintext
├── src/
│   ├── __init__.py
│   ├── config.py         # Configurações de cores e constantes
│   ├── data_handler.py   # Manipulação e cache de dados
│   ├── main.py           # Ponto de entrada da aplicação
│   ├── plotter.py        # Geração de gráficos
│   ├── ui.py             # Interface gráfica
├── .gitignore
├── README.MD
```

---

## 🚀 Como Começar

### 1️⃣ Pré-requisitos

Certifique-se de ter o Python 3.10 ou superior instalado. Instale as dependências com o comando:

```sh
pip install -r requirements.txt
```

### 2️⃣ Executando o Projeto

Para iniciar a aplicação, execute o seguinte comando:

```sh
python src/main.py
```

### 3️⃣ Explorando os Dados

- Carregue os dados de telemetria de uma sessão específica.
- Compare voltas de diferentes pilotos.
- Exporte gráficos para análise posterior.

---

## 📊 Exemplos de Gráficos

Aqui estão alguns exemplos de gráficos que você pode gerar com o **F1 Telemetry Viewer**:

- **Velocidade vs. Distância**: 📈
- **Delta de Tempo entre Pilotos**: ⏱️
- **Uso de DRS**: 🟢
- **RPM e Troca de Marchas**: ⚙️

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Siga os passos abaixo para contribuir:

1. Faça um **fork** do repositório.

2. Crie um **branch** para sua feature ou correção:

   ```sh
   git checkout -b minha-feature
   ```

3. Faça **commit** das suas alterações:

   ```sh
   git commit -m "Adiciona minha nova feature"
   ```

4. Envie suas alterações:

   ```sh
   git push origin minha-feature
   ```

5. Abra um **Pull Request**.

---

## 📜 Licença

Este projeto é licenciado sob a [MIT License](LICENSE). Sinta-se à vontade para usá-lo e modificá-lo conforme necessário.

---

## 🏁 Agradecimentos

Agradecemos a todos os entusiastas de Fórmula 1 que inspiraram este projeto. Que a paixão pela velocidade continue nos movendo! 🚗💨
