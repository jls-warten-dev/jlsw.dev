---
title: "2.000 fotos después: por qué me hice mi propio conversor de imágenes"
title_en: "2,000 photos later: why I built my own image converter"
date: 2026-08-25
excerpt: "Harto de depender de webs online para optimizar, recortar y marcar fotos al por mayor, escribí mi propia herramienta en Python. Se llama Alixeira (aligerar, en gallego) y lleva meses conmigo."
excerpt_en: "Tired of depending on web tools to optimise, crop and watermark photos in bulk, I wrote my own tool in Python. It is called Alixeira (to lighten, in Galician) and it has been with me for months."
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

Le puse **Alixeira** (*aligerar*, en gallego) porque de eso se trata: de aligerar
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

- Descarga: [Alixeira.zip, release 1.0](https://github.com/jls-warten-dev/alixeira/releases/download/1.0/Alixeira.zip)
- Repositorio: [github.com/jls-warten-dev/alixeira](https://github.com/jls-warten-dev/alixeira)

Si alguna vez has tenido que preparar cientos de fotos para publicar, ya sabes
por qué existe.

<!-- :en -->

## The hell of two thousand photos

It all started out of pure frustration. To optimise photos, add the watermark,
crop or convert formats I always ended up depending on web pages. With a
couple of photos there was no problem: upload, wait your turn, download and done.

But when you have to publish **2,000 photos spread across several WordPress
galleries**, things turn into hell. Uploading batches by hand, respecting size
limits, applying the watermark over and over, repeating the same process dozens
of times on different sites... What should have been an afternoon turned into days.

## Nobody knows what you need better than you do

In the end I realised something very simple: nobody knew better than I did what
I needed and how I needed it. I could program, so I stopped looking for the
perfect website and built my own application, tailored exactly to my workflow.

I called it **Alixeira** (*to lighten*, in Galician) because that is what it is
about: lightening the heavy work with images.

## What it does

It is a desktop tool, in Python, that works **100% offline**:

- Batch conversion to **WebP or JPEG**
- Adjusting every file to an **exact target size in KB** (ideal for CMS limits)
- Mass **resizing**
- **Watermark** applied automatically to the whole batch
- Output organised into **ZIPs**, with **reports** of what was processed

What used to be afternoons uploading and downloading photos on other people's
websites is now a local process that runs on its own.

## Months later

It is not a showcase project: I have been **using it for real for months** and I
am genuinely happy with the result. So much so that I decided to publish version
1.0 for anyone in the same situation.

- Download: [Alixeira.zip, release 1.0](https://github.com/jls-warten-dev/alixeira/releases/download/1.0/Alixeira.zip)
- Repository: [github.com/jls-warten-dev/alixeira](https://github.com/jls-warten-dev/alixeira)

If you have ever had to prepare hundreds of photos for publishing, you already
know why it exists.
