---
title: "2.000 fotos después: por qué me hice mi propio conversor de imágenes"
date: 2026-08-25
excerpt: "Harto de depender de webs online para optimizar, recortar y marcar fotos al por mayor, escribí mi propia herramienta en Python. Se llama Alixeira — aligerar, en gallego — y lleva meses conmigo."
tags: python, side-project, imágenes
---

## El infierno de las dos mil fotos

Todo empezó por pura frustración. Para optimizar fotos, añadir la marca de agua,
recortar o convertir formatos siempre acababa dependiendo de páginas web. Con un
par de fotos, no había problema: subes, esperas tu turno, descargas y listo.

Pero cuando tienes que publicar **2.000 fotos repartidas en varias galerías de
WordPress**, la cosa se convierte en un infierno. Subir lotes a mano, respetar
límites de tamaño, aplicar la marca de agua una y otra vez, repetir el mismo
proceso decenas de veces en webs distintas... Lo que debía ser una tarde se
convertía en días.

## Nadie sabe lo que necesitas mejor que tú

Al final caí en la cuenta de algo muy simple: nadie mejor que yo sabía lo que
necesitaba y cómo lo necesitaba. Sabía programar, así que dejé de buscar la web
perfecta y me hice mi propia aplicación, adaptada exactamente a mi flujo de
trabajo.

Le puse **Alixeira** — *aligerar*, en gallego — porque de eso se trata: de aligerar
el trabajo pesado con imágenes.

## Qué hace

Es una herramienta de escritorio, en Python, que funciona **100% sin conexión**:

- Conversión por lotes a **WebP o JPEG**
- Ajuste de cada archivo a un **tamaño objetivo exacto en KB** (ideal para límites de CMS)
- **Redimensionado** masivo
- **Marca de agua** aplicada automáticamente a todo el lote
- Salida organizada en **ZIPs**, con **informes** de lo procesado

Lo que antes eran tardes de subir y descargar fotos en webs ajenas, ahora es un
proceso local que va solo.

## Meses después

No es un proyecto de escaparate: llevo **meses usándola de verdad** y estoy
realmente contento con el resultado. Tanto que he decidido publicar la versión
1.0 para quien esté en la misma situación.

- Descarga: [Alixeira.zip — release 1.0](https://github.com/jls-warten-dev/alixeira/releases/download/1.0/Alixeira.zip)
- Repositorio: [github.com/jls-warten-dev/alixeira](https://github.com/jls-warten-dev/alixeira)

Si alguna vez has tenido que preparar cientos de fotos para publicar, ya sabes
por qué existe.
