# 🧭 Visão Geral — VoiceDraw

O **VoiceDraw** é um projeto de **extensão universitária** desenvolvido na **Pontifícia Universidade Católica de São Paulo (PUC-SP)**, como parte do programa de **Computação Aplicada à Inclusão Digital**.
Seu objetivo é promover **acessibilidade, inclusão e aprendizado tecnológico** através de uma aplicação interativa que permite **desenhar com a voz**.

---

## 🎯 Objetivo do projeto

O propósito do VoiceDraw é **reduzir barreiras de interação com o computador**.
Através do uso de **comandos de voz em português natural**, o usuário pode criar formas geométricas, controlar posições e alterar propriedades visuais sem a necessidade de dispositivos de entrada convencionais como mouse ou teclado.

O projeto busca:

* Proporcionar **autonomia digital** para pessoas com limitações motoras;
* Demonstrar a integração entre **linguagem natural, voz e interfaces gráficas**;
* Incentivar a **experimentação tecnológica** com impacto social positivo.

---

## 🧩 Estrutura conceitual

O VoiceDraw foi construído sobre uma arquitetura modular, permitindo que cada componente tenha um papel claro:

| Módulo            | Função principal                                                       |
| ----------------- | ---------------------------------------------------------------------- |
| `voice_engine.py` | Captura e transcreve o áudio do usuário em texto.                      |
| `nlp_parser.py`   | Interpreta o texto em comandos estruturados (ex: cor, forma, posição). |
| `app.py`          | Controla o fluxo da aplicação e coordena os módulos.                   |
| `ui_canvas.py`    | Desenha as formas no canvas Tkinter.                                   |
| `export.py`       | Exporta as imagens para formatos como PNG.                             |

Essa separação permite que o projeto seja **fácil de entender, adaptar e evoluir**, servindo como base didática para estudantes de computação, design e acessibilidade.

---

## 🌍 Impacto social e educacional

A aplicação foi pensada como **um meio de inclusão e aprendizado**:

* **Inclusão digital:** possibilita que pessoas com mobilidade reduzida explorem a criação visual por voz.
* **Educação tecnológica:** introduz estudantes ao uso de NLP, reconhecimento de voz e desenvolvimento de interfaces gráficas.
* **Abertura e colaboração:** o projeto é open-source e pode ser expandido por outras universidades, laboratórios e comunidades.

---

## 🧠 Metodologia

O desenvolvimento do VoiceDraw seguiu princípios de **aprendizado por projeto (project-based learning)** e **design centrado no usuário**.
O processo envolveu:

1. Pesquisa sobre necessidades de acessibilidade digital;
2. Definição de requisitos funcionais e não funcionais;
3. Implementação incremental com testes práticos;
4. Revisão contínua com foco em usabilidade e clareza de código.

---

## 🧾 Resultados esperados

* Ampliar a percepção dos alunos sobre o papel da tecnologia na inclusão social;
* Estimular o pensamento crítico sobre acessibilidade e ética na engenharia de software;
* Oferecer uma ferramenta real que possa ser usada como base para novos projetos de extensão ou pesquisa.

---

## 🪪 Créditos e autoria

Projeto desenvolvido por **César Santana** e equipe no contexto do programa de **Extensão em Computação Aplicada à Inclusão Digital — PUC-SP**.
Sob orientação dos professores do curso de **Ciência da Computação**.

---

> O VoiceDraw é mais do que um software — é um exercício prático de empatia, engenharia e propósito social, unindo voz, arte e tecnologia para ampliar o acesso digital de forma criativa e aberta.
