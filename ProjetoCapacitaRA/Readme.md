# Sistema WebXR de Controle Remoto

Guia rápido para executar o protótipo de Realidade Aumentada controlada em tempo real por sensores do smartphone via MQTT.

## Visão geral

O sistema usa dois dispositivos conectados à internet por um broker MQTT público. Um dispositivo funciona como Controlador (envia rotação e comando de ação). O outro exibe a cena AR no navegador e aplica as transformações em um modelo 3D.

## Estrutura do projeto

```
/projetoAR/
├── index.html          # Home com navegação
├── controle.html       # Controlador virtual (DeviceOrientation + MQTT)
├── displayAR.html      # Cena AR.js + A‑Frame, recebe MQTT
└── aviao_low_poly.glb  # Modelo 3D 
```

## Tecnologias

* A‑Frame + AR.js (marcador "hiro")
* MQTT via WebSockets no navegador (Paho MQTT JS)
* HTML e JavaScript puros

## Requisitos

1. Dois dispositivos com navegadores modernos:

   * Controlador: smartphone com giroscópio.
   * Display: smartphone, tablet ou computador com câmera.
2. Conexão à internet para acessar o broker MQTT público.
3. Marcador AR “hiro” visível à câmera do Display. Recomenda-se imprimir o marcador (pesquise por "AR.js hiro marker").

## Configuração de rede MQTT

* Broker: `wss://broker.emqx.io:8084/mqtt`
* Tópico único: `projetoAR/controle/dados`
* Formato das mensagens JSON publicadas pelo Controlador:

  * Orientação contínua (~20 Hz):

    ```json
    { "type": "orientation", "alpha": 0, "beta": 0, "gamma": 0, "t": 1710000000000 }
    ```
  * Ação (ao tocar no botão):

    ```json
    { "type": "action", "t": 1710000000000 }
    ```
* O Display assina o mesmo tópico e:

  * Mapeia `alpha→y`, `beta→x`, `gamma→z` para `rotation` do A‑Frame.
  * Dispara a animação embutida no `.glb` quando recebe `{ "type": "action" }`.

## Passo a passo

1. Abrir a home

   * Em ambos os dispositivos, abra `index.html` servindo no link 'https://ramqtt.netlify.app/'.
   * Dica: use um servidor estático (por exemplo, VS Code Live Server, http-server, ou outro). Em HTTPS, as permissões de câmera e sensores funcionam melhor.
2. Configurar o Controlador (smartphone)
   * Toque em **Controlador Virtual**.
   * Toque no botão **Acionar animação** uma vez para autorizar os sensores. Em iOS, você deve permitir “Movimento e Orientação”.
   * O painel exibirá os valores `alpha`, `beta` e `gamma`. A partir de agora, o telefone transmite rotação por MQTT.

3. Configurar o Display AR
   * No segundo dispositivo, toque em **Display AR**.
   * Permita o acesso à **câmera** quando solicitado.
   * Aponte a câmera para o **marcador hiro**. O avião aparecerá sobre o marcador.

4. Executar a experiência

   * Movimente o smartphone Controlador. O avião no Display deve rotacionar em tempo real.
   * Toque novamente no botão do Controlador para enviar o sinal de **ação**. O modelo deve executar a animação predefinida (girar a hélice).

## Onde trocar o modelo 3D

No `displayAR.html`, altere o caminho do ativo:

```html
<a-asset-item id="planeModel" src="./aviao_low_poly.glb"></a-asset-item>
```

Substitua por outro `.glb`/`.gltf` local e ajuste `scale` e `rotation` do elemento com `id="plane"` conforme necessário.

## Observações de segurança e privacidade

* O broker EMQX público é compartilhado. Não publique dados sensíveis.
* Em produção, use um broker próprio com autenticação, TLS gerenciado e tópicos namespaced.

## Solução de problemas

* **O modelo não aparece**

  * Verifique permissões da câmera e iluminação adequada no marcador.
  * Recarregue a página do Display e aponte a câmera para o marcador hiro.
* **O avião aparece mas não gira**

  * Confirme que o Controlador mostra valores mudando. Se necessário, toque no botão para reautorizar sensores.
  * Alguns navegadores exigem gesto do usuário antes de ler os sensores.
* **Sem conexão**

  * Verifique a internet dos dois dispositivos.
  * Confirme que ambos usam o mesmo broker e tópico (`wss://broker.emqx.io:8084/mqtt` e `projetoAR/controle/dados`).

## Licença

Este material é fornecido para fins educacionais e de demonstração.
Modelo criado com base no curso do Gustavo Rosa: https://www.udemy.com/share/102foGAkYYdldaRHQ=/
disponível download a partir do site sketchfab https://skfb.ly/6Srus

